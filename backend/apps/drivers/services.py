"""Driver business logic layer."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4


def build_location_acknowledgement() -> dict:
    event_id = f'location_event_{uuid4().hex[:12]}'
    return {
        'success': True,
        'message': 'Location event accepted',
        'event_id': event_id,
    }


def validate_driver_event(payload: dict) -> tuple[bool, str | None]:
    if payload.get('latitude') is None or payload.get('longitude') is None:
        return False, 'Latitude and longitude are required.'

    if not (-90.0 <= float(payload['latitude']) <= 90.0):
        return False, 'Latitude is out of range.'

    if not (-180.0 <= float(payload['longitude']) <= 180.0):
        return False, 'Longitude is out of range.'

    timestamp = payload.get('timestamp')
    if timestamp is None:
        return False, 'Timestamp is required.'

    try:
        parsed = datetime.fromisoformat(str(timestamp).replace('Z', '+00:00'))
    except ValueError:
        return False, 'Timestamp is invalid.'

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    if (datetime.now(timezone.utc) - parsed).total_seconds() > 300:
        return False, 'Timestamp is stale.'

    return True, None
