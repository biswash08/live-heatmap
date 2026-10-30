"""Redis-backed live driver state management for H3 cell membership."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

try:
    import redis
except ImportError:  # pragma: no cover
    redis = None


@dataclass
class DriverState:
    driver_id: str
    latitude: float
    longitude: float
    current_h3_cell: str | None = None
    city_id: str | None = None
    availability_status: str = 'online'
    last_seen: float = 0.0
    event_version: int = 0


class DriverStateStore:
    """Mutable in-memory state store used as the Redis state model in tests and local dev.

    The production deployment should replace this with a Redis-backed implementation while
    preserving the same contract and invariants.
    """

    _shared_instance: 'DriverStateStore | None' = None

    def __init__(self) -> None:
        self.driver_states: dict[str, DriverState] = {}
        self.cell_members: dict[str, set[str]] = {}
        self.cell_counts: dict[str, int] = {}

    @classmethod
    def shared(cls) -> 'DriverStateStore':
        if cls._shared_instance is None:
            cls._shared_instance = cls()
        return cls._shared_instance

    def _cell_key(self, city_id: str, h3_cell: str) -> str:
        return f'cell:{city_id}:{h3_cell}'

    def _driver_is_countable(self, state: DriverState | None) -> bool:
        if state is None:
            return False
        return state.availability_status in {'online', 'available'}

    def _remove_member(self, city_id: str, h3_cell: str, driver_id: str) -> None:
        if not city_id or not h3_cell:
            return
        cell_key = self._cell_key(city_id, h3_cell)
        members = self.cell_members.setdefault(cell_key, set())
        if driver_id in members:
            members.remove(driver_id)
        self.cell_counts[cell_key] = max(len(members), 0)

    def _add_member(self, city_id: str, h3_cell: str, driver_id: str) -> None:
        if not city_id or not h3_cell:
            return
        cell_key = self._cell_key(city_id, h3_cell)
        members = self.cell_members.setdefault(cell_key, set())
        members.add(driver_id)
        self.cell_counts[cell_key] = len(members)

    def apply_location_update(
        self,
        driver_id: str,
        latitude: float,
        longitude: float,
        city_id: str,
        h3_cell: str,
        event_version: int,
        timestamp_epoch: float,
        availability_status: str = 'online',
    ) -> dict[str, Any]:
        current_state = self.driver_states.get(driver_id)
        previous_cell = current_state.current_h3_cell if current_state else None

        if current_state and event_version < current_state.event_version:
            return {
                'updated': False,
                'reason': 'stale_event_version',
                'driver_id': driver_id,
                'current_h3_cell': previous_cell,
            }

        if current_state and previous_cell and previous_cell != h3_cell:
            self._remove_member(current_state.city_id or city_id, previous_cell, driver_id)

        if self._driver_is_countable(
            DriverState(
                driver_id=driver_id,
                latitude=latitude,
                longitude=longitude,
                current_h3_cell=h3_cell,
                city_id=city_id,
                availability_status=availability_status,
                last_seen=timestamp_epoch,
                event_version=event_version,
            )
        ):
            self._add_member(city_id, h3_cell, driver_id)

        state = DriverState(
            driver_id=driver_id,
            latitude=latitude,
            longitude=longitude,
            current_h3_cell=h3_cell,
            city_id=city_id,
            availability_status=availability_status,
            last_seen=timestamp_epoch,
            event_version=event_version,
        )
        self.driver_states[driver_id] = state

        return {
            'updated': True,
            'driver_id': driver_id,
            'previous_h3_cell': previous_cell,
            'new_h3_cell': h3_cell,
            'cell_count': self.cell_counts.get(self._cell_key(city_id, h3_cell), 0),
            'current_state': state.__dict__,
        }

    def mark_driver_inactive(self, driver_id: str) -> dict[str, Any]:
        state = self.driver_states.get(driver_id)
        if not state:
            return {'updated': False, 'driver_id': driver_id}

        previous_cell = state.current_h3_cell
        if previous_cell and state.city_id:
            self._remove_member(state.city_id, previous_cell, driver_id)

        state.availability_status = 'offline'
        state.event_version += 1
        self.driver_states[driver_id] = state
        return {'updated': True, 'driver_id': driver_id, 'previous_h3_cell': previous_cell}

    def expire_stale_drivers(self, now: float, ttl_seconds: int = 30, city_id: str | None = None) -> list[str]:
        expired: list[str] = []
        for driver_id, state in list(self.driver_states.items()):
            if state.availability_status not in {'online', 'available'}:
                continue

            if now - state.last_seen <= ttl_seconds:
                continue

            if state.current_h3_cell and state.city_id:
                self._remove_member(state.city_id, state.current_h3_cell, driver_id)

            state.availability_status = 'offline'
            state.event_version += 1
            self.driver_states[driver_id] = state
            expired.append(driver_id)

        if city_id is not None:
            self.reconcile_cell_counts(city_id)

        return expired

    def reconcile_cell_counts(self, city_id: str | None = None) -> int:
        total = 0
        for cell_key, members in list(self.cell_members.items()):
            if city_id is not None and not cell_key.startswith(f'cell:{city_id}:'):
                continue

            count = len(members)
            self.cell_counts[cell_key] = count
            total += count

        return total

    def get_cell_count(self, city_id: str, h3_cell: str) -> int:
        return self.cell_counts.get(self._cell_key(city_id, h3_cell), 0)

    def get_driver_state(self, driver_id: str) -> DriverState | None:
        return self.driver_states.get(driver_id)


class RedisStateStore(DriverStateStore):
    """Redis-backed mirror for live heatmap state with in-memory fallback."""

    def __init__(self, redis_url: str | None = None, redis_client: Any | None = None) -> None:
        super().__init__()
        self.redis_url = redis_url or os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0')
        self.redis_client = redis_client
        self._redis_ready = False
        if self.redis_client is None:
            self._redis_ready = self._connect()
        else:
            self._redis_ready = True

    def _connect(self) -> bool:
        if redis is None:
            return False
        try:
            self.redis_client = redis.Redis.from_url(self.redis_url, decode_responses=True)
            self.redis_client.ping()
            return True
        except Exception:
            self.redis_client = None
            return False

    def _sync_driver_state(self, state: DriverState) -> None:
        if not self._redis_ready or self.redis_client is None:
            return
        self.redis_client.hset(
            f'driver:{state.driver_id}',
            mapping={
                'driver_id': state.driver_id,
                'latitude': str(state.latitude),
                'longitude': str(state.longitude),
                'current_h3_cell': state.current_h3_cell or '',
                'city_id': state.city_id or '',
                'availability_status': state.availability_status,
                'last_seen': str(state.last_seen),
                'event_version': str(state.event_version),
            },
        )
        if state.current_h3_cell and state.city_id:
            self.redis_client.sadd(f'cell:{state.city_id}:{state.current_h3_cell}', state.driver_id)
            self.redis_client.hset('cell_counts', f'{state.city_id}:{state.current_h3_cell}', str(len(self.cell_members.get(f'cell:{state.city_id}:{state.current_h3_cell}', set()))))

    def apply_location_update(
        self,
        driver_id: str,
        latitude: float,
        longitude: float,
        city_id: str,
        h3_cell: str,
        event_version: int,
        timestamp_epoch: float,
        availability_status: str = 'online',
    ) -> dict[str, Any]:
        result = super().apply_location_update(
            driver_id=driver_id,
            latitude=latitude,
            longitude=longitude,
            city_id=city_id,
            h3_cell=h3_cell,
            event_version=event_version,
            timestamp_epoch=timestamp_epoch,
            availability_status=availability_status,
        )
        state = self.driver_states.get(driver_id)
        if state is not None:
            self._sync_driver_state(state)
        return result

    def mark_driver_inactive(self, driver_id: str) -> dict[str, Any]:
        result = super().mark_driver_inactive(driver_id)
        state = self.driver_states.get(driver_id)
        if state is not None:
            self._sync_driver_state(state)
        return result

    def reconcile_cell_counts(self, city_id: str | None = None) -> int:
        total = super().reconcile_cell_counts(city_id)
        if self._redis_ready and self.redis_client is not None:
            for cell_key, members in self.cell_members.items():
                if city_id is not None and not cell_key.startswith(f'cell:{city_id}:'):
                    continue
                self.redis_client.hset('cell_counts', cell_key, str(len(members)))
        return total


def get_state_store() -> DriverStateStore:
    if os.getenv('USE_REDIS_STATE', 'false').lower() == 'true':
        try:
            return RedisStateStore()
        except Exception:
            pass
    return DriverStateStore.shared()
