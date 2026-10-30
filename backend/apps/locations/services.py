"""Location processing service layer."""

from datetime import datetime, timezone


def validate_event_structure(payload: dict) -> tuple[bool, str | None]:
    if 'latitude' not in payload or 'longitude' not in payload:
        return False, 'latitude and longitude are required.'

    if not (-90.0 <= float(payload['latitude']) <= 90.0):
        return False, 'latitude out of range.'

    if not (-180.0 <= float(payload['longitude']) <= 180.0):
        return False, 'longitude out of range.'

    if 'timestamp' not in payload:
        return False, 'timestamp is required.'

    try:
        parsed = datetime.fromisoformat(str(payload['timestamp']).replace('Z', '+00:00'))
    except ValueError:
        return False, 'timestamp is invalid.'

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    if (datetime.now(timezone.utc) - parsed).total_seconds() > 300:
        return False, 'timestamp is stale.'

    return True, None
