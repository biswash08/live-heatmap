"""Location processing service layer."""

import json
import os
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from apps.cities.seed import get_best_matching_address_for_coordinates, get_city_by_id

GOOGLE_GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'


def _pick_first_value(address_components: list[dict], *types: str) -> str | None:
    for component in address_components:
        component_types = component.get('types', [])
        if any(item in component_types for item in types):
            value = component.get('long_name') or component.get('short_name')
            if value:
                return value
    return None


def _normalize_google_address_components(address_components: list[dict]) -> dict:
    components = {
        'street_number': _pick_first_value(address_components, 'street_number'),
        'route': _pick_first_value(address_components, 'route'),
        'premise': _pick_first_value(address_components, 'premise'),
        'subpremise': _pick_first_value(address_components, 'subpremise'),
        'neighborhood': _pick_first_value(address_components, 'neighborhood'),
        'sublocality': _pick_first_value(address_components, 'sublocality', 'sublocality_level_1'),
        'locality': _pick_first_value(address_components, 'locality'),
        'district': _pick_first_value(address_components, 'administrative_area_level_2'),
        'state': _pick_first_value(address_components, 'administrative_area_level_1'),
        'country': _pick_first_value(address_components, 'country'),
        'postal_code': _pick_first_value(address_components, 'postal_code'),
    }
    return components


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


def _google_reverse_geocode(latitude: float, longitude: float) -> dict | None:
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        return None

    enabled = os.getenv('GOOGLE_MAPS_GEOCODE_ENABLED', 'true').strip().lower() not in {'0', 'false', 'no'}
    if not enabled:
        return None

    timeout_seconds = 5
    try:
        timeout_seconds = int(os.getenv('GOOGLE_MAPS_TIMEOUT_SECONDS', '5'))
    except ValueError:
        timeout_seconds = 5

    params = {
        'latlng': f'{latitude},{longitude}',
        'key': api_key,
        'language': 'en',
        'result_type': 'street_address|route|neighborhood|premise|subpremise|sublocality|locality',
    }
    url = f'{GOOGLE_GEOCODE_URL}?{urlencode(params)}'

    try:
        request = Request(url, headers={'User-Agent': 'RideFlow-Nepal/1.0'})
        with urlopen(request, timeout=timeout_seconds) as response:
            payload = json.loads(response.read().decode('utf-8'))
    except Exception:
        return None

    results = payload.get('results') or []
    if not results:
        return None

    first = results[0]
    components = _normalize_google_address_components(first.get('address_components', []))

    street_number = components.get('street_number')
    route = components.get('route')
    premise = components.get('premise')
    subpremise = components.get('subpremise')
    neighborhood = components.get('neighborhood')
    sublocality = components.get('sublocality')
    locality = components.get('locality')
    district = components.get('district')
    state = components.get('state')
    country = components.get('country')

    street_label = route or neighborhood or sublocality or locality
    if street_number and street_label:
        street_label = f'{street_number} {street_label}'

    landmark = premise or subpremise or street_label or neighborhood or sublocality or locality
    city_name = locality or sublocality or neighborhood or district or state or 'Unknown area'
    formatted = first.get('formatted_address') or ', '.join(filter(None, [landmark, city_name, country]))

    return {
        'source': 'google',
        'formatted_address': formatted,
        'city': city_name,
        'district': district or state,
        'municipality': locality or sublocality or neighborhood,
        'street': route,
        'house_number': street_number,
        'building': premise or subpremise,
        'landmark': landmark,
        'latitude': latitude,
        'longitude': longitude,
    }


def resolve_location_from_coordinates(latitude: float, longitude: float, city_id: str | None = None) -> dict | None:
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except (TypeError, ValueError):
        return None

    if not (-90.0 <= latitude <= 90.0 and -180.0 <= longitude <= 180.0):
        return None

    google_result = _google_reverse_geocode(latitude, longitude)
    if google_result:
        google_result['city_id'] = city_id
        google_result['city_name'] = google_result.get('city') or (get_city_by_id(city_id).get('name') if get_city_by_id(city_id) else None)
        google_result['country'] = 'Nepal' if 'Nepal' in str(google_result.get('formatted_address', '')) else None
        return google_result

    fallback = get_best_matching_address_for_coordinates(latitude, longitude, city_id=city_id)
    if fallback is None:
        return {
            'source': 'local_fallback',
            'formatted_address': 'Unknown location',
            'city_id': city_id,
            'city_name': get_city_by_id(city_id).get('name') if get_city_by_id(city_id) else None,
            'landmark': 'Unknown landmark',
            'latitude': latitude,
            'longitude': longitude,
        }

    city = get_city_by_id(fallback.get('city_id')) if fallback.get('city_id') else None

    return {
        'source': 'local_fallback',
        'city_id': fallback.get('city_id'),
        'city_name': city.get('name') if city else None,
        'district': fallback.get('district'),
        'municipality': fallback.get('municipality'),
        'ward': fallback.get('ward'),
        'area': fallback.get('area'),
        'street': fallback.get('street'),
        'landmark': fallback.get('landmark'),
        'formatted_address': fallback.get('formatted_address'),
        'latitude': fallback.get('latitude', latitude),
        'longitude': fallback.get('longitude', longitude),
        'distance_km': fallback.get('distance_km'),
    }
