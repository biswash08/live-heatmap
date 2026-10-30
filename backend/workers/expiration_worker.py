"""Driver expiration worker."""

from __future__ import annotations

from infrastructure.redis.state_store import DriverStateStore


def expire_drivers(driver_ids: list[str], state_store: DriverStateStore | None = None) -> list[str]:
    store = state_store or DriverStateStore.shared()
    expired: list[str] = []

    for driver_id in driver_ids:
        if not driver_id:
            continue

        state = store.get_driver_state(driver_id)
        if state is None:
            continue

        if state.availability_status == 'offline':
            continue

        store.mark_driver_inactive(driver_id)
        expired.append(driver_id)

    return expired
