from rest_framework.test import APIRequestFactory
from apps.rides.views import RideRequestCreateView

payload = {
    'pickup_address': 'Bajeko Nilo Pul',
    'pickup_latitude': 27.6758,
    'pickup_longitude': 85.4316,
    'destination_address': 'Manau Bakery',
    'destination_latitude': 27.6722,
    'destination_longitude': 85.4289,
    'estimated_fare': 1200,
    'surge_multiplier': 1.2,
    'vehicle_type': 'car',
}

request = APIRequestFactory().post('/api/v1/rides/requests/', payload, format='json')
response = RideRequestCreateView.as_view()(request)
print(response.status_code)
print(response.data)
