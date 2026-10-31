from apps.cities.seed import (
    KATHMANDU_CITY_ID,
    get_address_by_id,
    get_city_address_index,
    search_city_addresses,
)
from apps.locations.services import resolve_location_from_coordinates


def test_kathmandu_address_index_contains_exact_location_details():
    city_addresses = get_city_address_index(KATHMANDU_CITY_ID)

    assert len(city_addresses) >= 8
    first = city_addresses[0]
    assert 'province' in first
    assert 'district' in first
    assert 'municipality' in first
    assert 'ward' in first
    assert 'landmark' in first
    assert 'latitude' in first
    assert 'longitude' in first
    assert 'formatted_address' in first


def test_search_city_addresses_matches_exact_neighborhoods():
    results = search_city_addresses(KATHMANDU_CITY_ID, 'baluwatar')

    assert len(results) >= 1
    assert any('Baluwatar' in item['formatted_address'] for item in results)
    assert any('ward' in item for item in results[0])


def test_get_address_by_id_returns_exact_address_record():
    item = get_address_by_id(KATHMANDU_CITY_ID, 'ktm-baluwatar-ward-10')

    assert item is not None
    assert item['municipality'] == 'Kathmandu Metropolitan City'
    assert item['ward'] == 'Ward 10'
    assert item['landmark'] == 'Baluwatar Community Hall'


def test_resolve_location_from_coordinates_uses_local_fallback_for_exact_places():
    resolved = resolve_location_from_coordinates(27.6758, 85.4316)

    assert resolved is not None
    assert resolved['source'] == 'local_fallback'
    assert resolved['city_id'] == 'bkt'
    assert resolved['landmark'] in {'Bajeko Nilo Pul', 'Duwakot', 'Manau Bakery'}


def test_bhaktapur_specific_locations_are_indexed():
    duwakot = search_city_addresses('bkt', 'duwakot')
    bajeko = search_city_addresses('bkt', 'bajeko nilo pul')

    assert any('Duwakot' in item['formatted_address'] for item in duwakot)
    assert any('Bajeko Nilo Pul' in item['formatted_address'] for item in bajeko)


def test_resolve_location_from_coordinates_prefers_google_when_available(monkeypatch):
    monkeypatch.setenv('GOOGLE_MAPS_API_KEY', 'test-google-key')

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return b'{"results": [{"formatted_address": "Bajeko Nilo Pul, Bhaktapur, Nepal", "address_components": [{"long_name": "Bajeko Nilo Pul", "types": ["route"]}, {"long_name": "Bhaktapur", "types": ["locality"]}, {"long_name": "Bagmati Province", "types": ["administrative_area_level_1"]}, {"long_name": "Nepal", "types": ["country"]}]}], "status": "OK"}'

    monkeypatch.setattr('apps.locations.services.urlopen', lambda *args, **kwargs: FakeResponse())

    resolved = resolve_location_from_coordinates(27.6758, 85.4316)

    assert resolved is not None
    assert resolved['source'] == 'google'
    assert resolved['formatted_address'] == 'Bajeko Nilo Pul, Bhaktapur, Nepal'
    assert resolved['landmark'] == 'Bajeko Nilo Pul'
