from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from infrastructure.redis.state_store import DriverStateStore
from .services import distance_meters_between


class NearbyDriversView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            latitude = float(request.query_params.get('latitude'))
            longitude = float(request.query_params.get('longitude'))
            radius = float(request.query_params.get('radius', 2000))
            limit = int(request.query_params.get('limit', 10))
        except (TypeError, ValueError):
            return Response({'detail': 'latitude, longitude and radius are required.'}, status=status.HTTP_400_BAD_REQUEST)

        nearby = []
        store = DriverStateStore.shared()
        for state in store.driver_states.values():
            availability_status = getattr(state, 'availability_status', 'online')
            if availability_status not in {'online', 'available'}:
                continue

            state_latitude = float(getattr(state, 'latitude', 0.0))
            state_longitude = float(getattr(state, 'longitude', 0.0))
            dist = distance_meters_between(latitude, longitude, state_latitude, state_longitude)
            if dist <= radius:
                nearby.append({
                    'driver_id': getattr(state, 'driver_id', getattr(state, 'id', 'unknown-driver')),
                    'latitude': state_latitude,
                    'longitude': state_longitude,
                    'distance_meters': round(dist, 2),
                })

        nearby.sort(key=lambda item: item['distance_meters'])
        return Response({'nearby_drivers': nearby[:limit]}, status=status.HTTP_200_OK)
