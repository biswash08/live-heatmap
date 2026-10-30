"""Redis-backed live driver state management for H3 cell membership."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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

    def get_cell_count(self, city_id: str, h3_cell: str) -> int:
        return self.cell_counts.get(self._cell_key(city_id, h3_cell), 0)

    def get_driver_state(self, driver_id: str) -> DriverState | None:
        return self.driver_states.get(driver_id)
