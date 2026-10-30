"""Runtime smoke helper for live city metrics and nearby-driver snapshots."""

from __future__ import annotations

from apps.cities.seed import KATHMANDU_CITY_ID
from infrastructure.redis.state_store import DriverStateStore
from workers.location_processor import process_location_event


def _seed_demo_state(store: DriverStateStore | None = None) -> DriverStateStore:
    state_store = store or DriverStateStore()
    demo_events = [
        {
            'event_id': 'demo-1',
            'driver_id': 'driver-demo-1',
            'city_id': KATHMANDU_CITY_ID,
            'latitude': 27.7172,
            'longitude': 85.324,
            'timestamp_epoch': 1700000000,
            'event_version': 1,
            'availability_status': 'online',
        },
        {
            'event_id': 'demo-2',
            'driver_id': 'driver-demo-2',
            'city_id': KATHMANDU_CITY_ID,
            'latitude': 27.7180,
            'longitude': 85.3250,
            'timestamp_epoch': 1700000005,
            'event_version': 1,
            'availability_status': 'online',
        },
        {
            'event_id': 'demo-3',
            'driver_id': 'driver-demo-3',
            'city_id': KATHMANDU_CITY_ID,
            'latitude': 27.7500,
            'longitude': 85.3700,
            'timestamp_epoch': 1700000010,
            'event_version': 1,
            'availability_status': 'online',
        },
    ]

    for event in demo_events:
        process_location_event(event, state_store)

    return state_store


def build_demo_runtime_snapshot() -> dict:
    store = _seed_demo_state()
    city_id = KATHMANDU_CITY_ID
    live_drivers = [state for state in store.driver_states.values() if state.city_id == city_id and state.availability_status in {'online', 'available'}]
    total_driver_count = len(live_drivers)

    nearby = []
    for state in live_drivers:
        nearby.append({
            'driver_id': state.driver_id,
            'latitude': state.latitude,
            'longitude': state.longitude,
            'distance_meters': 0,
        })

    surge = {
        'city_id': city_id,
        'multiplier': 1.0,
        'active_requests': max(total_driver_count, 1),
        'available_drivers': total_driver_count,
        'explanation': 'Balanced demand and supply for the demo city snapshot.',
    }

    return {
        'city_id': city_id,
        'heatmap': {
            'total_driver_count': total_driver_count,
            'cells': sorted({state.current_h3_cell for state in live_drivers if state.current_h3_cell}),
        },
        'nearby_drivers': nearby,
        'surge': surge,
    }
