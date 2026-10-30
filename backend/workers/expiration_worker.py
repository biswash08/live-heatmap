"""Driver expiration worker."""

from __future__ import annotations


def expire_drivers(driver_ids: list[str]) -> list[str]:
    return [driver_id for driver_id in driver_ids if driver_id]
