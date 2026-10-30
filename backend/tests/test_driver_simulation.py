from infrastructure.simulation.fleet_simulator import build_location_event, simulate_driver_path


def test_build_location_event_uses_driver_and_version_fields():
    event = build_location_event(
        driver_id='driver-900',
        city_id='ktm',
        latitude=27.7172,
        longitude=85.324,
        event_version=2,
        timestamp_epoch=1700000002,
    )

    assert event['driver_id'] == 'driver-900'
    assert event['city_id'] == 'ktm'
    assert event['event_version'] == 2
    assert event['timestamp_epoch'] == 1700000002


def test_simulate_driver_path_updates_live_state_for_each_waypoint():
    events = simulate_driver_path(
        driver_id='driver-901',
        city_id='ktm',
        waypoints=[
            (27.7172, 85.324),
            (27.72, 85.33),
            (27.725, 85.34),
        ],
        start_time=1700000000,
        interval_seconds=5,
    )

    assert len(events) == 3
    assert events[0]['driver_id'] == 'driver-901'
    assert events[0]['status'] == 'processed'
    assert events[2]['result']['updated'] is True
