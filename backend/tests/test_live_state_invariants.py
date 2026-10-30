from apps.geospatial.services import get_h3_cell
from infrastructure.redis.state_store import DriverStateStore
from workers.location_processor import process_location_event


def test_same_cell_repeated_updates_do_not_double_count():
    store = DriverStateStore()
    event = {
        'event_id': 'e1',
        'driver_id': 'driver-100',
        'city_id': 'ktm',
        'latitude': 27.7172,
        'longitude': 85.324,
        'timestamp_epoch': 100,
        'event_version': 1,
        'availability_status': 'online',
    }

    process_location_event(event, store)
    process_location_event({**event, 'event_id': 'e2', 'event_version': 2, 'timestamp_epoch': 110}, store)

    cell_id = get_h3_cell(27.7172, 85.324, 8)
    assert store.get_cell_count('ktm', cell_id) == 1


def test_moving_between_cells_is_atomic_and_count_correct():
    store = DriverStateStore()
    first = {
        'event_id': 'e1',
        'driver_id': 'driver-200',
        'city_id': 'ktm',
        'latitude': 27.7172,
        'longitude': 85.324,
        'timestamp_epoch': 100,
        'event_version': 1,
        'availability_status': 'online',
    }
    second = {
        'event_id': 'e2',
        'driver_id': 'driver-200',
        'city_id': 'ktm',
        'latitude': 27.8,
        'longitude': 85.4,
        'timestamp_epoch': 200,
        'event_version': 2,
        'availability_status': 'online',
    }

    process_location_event(first, store)
    process_location_event(second, store)

    old_cell = get_h3_cell(27.7172, 85.324, 8)
    new_cell = get_h3_cell(27.8, 85.4, 8)

    assert store.get_cell_count('ktm', old_cell) == 0
    assert store.get_cell_count('ktm', new_cell) == 1


def test_stale_event_version_does_not_overwrite_newer_state():
    store = DriverStateStore()
    event_a = {
        'event_id': 'e1',
        'driver_id': 'driver-300',
        'city_id': 'ktm',
        'latitude': 27.7172,
        'longitude': 85.324,
        'timestamp_epoch': 100,
        'event_version': 3,
        'availability_status': 'online',
    }
    event_b = {
        'event_id': 'e2',
        'driver_id': 'driver-300',
        'city_id': 'ktm',
        'latitude': 27.7300,
        'longitude': 85.3400,
        'timestamp_epoch': 90,
        'event_version': 2,
        'availability_status': 'online',
    }

    process_location_event(event_a, store)
    result = process_location_event(event_b, store)

    assert result['result']['updated'] is False
    state = store.get_driver_state('driver-300')
    assert state is not None
    assert state.event_version == 3
