"""Off-request location processing pipeline."""

from __future__ import annotations

from typing import Any

from apps.geospatial.services import get_h3_cell
from infrastructure.redis.state_store import DriverStateStore


def process_location_event(event: dict[str, Any], state_store: DriverStateStore | None = None) -> dict[str, Any]:
    store = state_store or DriverStateStore()
    latitude = float(event.get('latitude'))
    longitude = float(event.get('longitude'))
    city_id = event.get('city_id', 'ktm')
    h3_cell = get_h3_cell(latitude, longitude, 8)
    event_version = int(event.get('event_version', 1))
    timestamp_epoch = float(event.get('timestamp_epoch', 0.0)) or 0.0

    result = store.apply_location_update(
        driver_id=str(event.get('driver_id')),
        latitude=latitude,
        longitude=longitude,
        city_id=city_id,
        h3_cell=h3_cell,
        event_version=event_version,
        timestamp_epoch=timestamp_epoch,
        availability_status=event.get('availability_status', 'online'),
    )

    return {
        'event_id': event.get('event_id'),
        'driver_id': event.get('driver_id'),
        'status': 'processed',
        'city_id': city_id,
        'h3_cell': h3_cell,
        'result': result,
    }
