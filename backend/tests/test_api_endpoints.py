from rest_framework.test import APIRequestFactory

from apps.driver_search.views import NearbyDriversView
from apps.heatmap.views import HeatmapView
from apps.surge_pricing.views import SurgePricingView
from infrastructure.redis.state_store import DriverStateStore


def test_heatmap_view_returns_cells_for_city():
    state_store = DriverStateStore.shared()
    state_store.driver_states['driver-1'] = type('State', (), {
        'city_id': 'ktm',
        'latitude': 27.7172,
        'longitude': 85.324,
        'current_h3_cell': 'cell-abc',
        'availability_status': 'online',
    })()
    state_store.cell_counts['cell:ktm:cell-abc'] = 1

    request = APIRequestFactory().get('/api/v1/heatmap/ktm/?north=28&south=27&east=86&west=84&resolution=8')
    response = HeatmapView.as_view()(request, city_id='ktm')

    assert response.status_code == 200
    assert response.data['city_id'] == 'ktm'
    assert len(response.data['cells']) >= 1


def test_nearby_driver_view_returns_closest_drivers():
    state_store = DriverStateStore.shared()
    state_store.driver_states['driver-2'] = type('State', (), {
        'driver_id': 'driver-2',
        'latitude': 27.7172,
        'longitude': 85.324,
        'availability_status': 'online',
    })()

    request = APIRequestFactory().get('/api/v1/riders/nearby-drivers/?latitude=27.718&longitude=85.325&radius=2000&limit=5')
    response = NearbyDriversView.as_view()(request)

    assert response.status_code == 200
    assert 'nearby_drivers' in response.data


def test_surge_pricing_view_returns_multiplier():
    request = APIRequestFactory().get('/api/v1/pricing/surge/?latitude=27.7172&longitude=85.324&vehicle_type=car')
    response = SurgePricingView.as_view()(request)

    assert response.status_code == 200
    assert 'surge_multiplier' in response.data
    assert response.data['surge_multiplier'] >= 1.0
