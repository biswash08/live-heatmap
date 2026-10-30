from datetime import datetime, timedelta, timezone

from apps.cities.seed import KATHMANDU_CITY_ID, get_city_by_id
from apps.drivers.services import validate_driver_event
from apps.geospatial.services import get_h3_cell
from apps.heatmap.services import classify_density
from apps.surge_pricing.services import compute_surge_multiplier


def test_valid_driver_event_accepts_recent_payload():
    payload = {
        'latitude': 27.7172,
        'longitude': 85.324,
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }

    valid, error = validate_driver_event(payload)

    assert valid is True
    assert error is None


def test_valid_driver_event_rejects_stale_payload():
    payload = {
        'latitude': 27.7172,
        'longitude': 85.324,
        'timestamp': (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat(),
    }

    valid, error = validate_driver_event(payload)

    assert valid is False
    assert 'stale' in error.lower()


def test_h3_cell_generation_for_nepal_kathmandu():
    cell = get_h3_cell(27.7172, 85.324, 8)

    assert isinstance(cell, str)
    assert len(cell) > 10


def test_kathmandu_city_definition_is_available():
    city = get_city_by_id(KATHMANDU_CITY_ID)

    assert city is not None
    assert 'Kathmandu' in city['name']
    assert city['country'] == 'Nepal'
    assert city['lat'] == 27.7172
    assert city['lng'] == 85.324


def test_density_classification_ranges():
    assert classify_density(0) == 'empty'
    assert classify_density(2) == 'very_low'
    assert classify_density(8) == 'low'
    assert classify_density(18) == 'medium'
    assert classify_density(40) == 'high'
    assert classify_density(120) == 'very_high'


def test_surge_multiplier_increases_with_demand():
    multiplier = compute_surge_multiplier(available_drivers=5, active_requests=30)

    assert multiplier >= 1.0
    assert multiplier > 1.0
