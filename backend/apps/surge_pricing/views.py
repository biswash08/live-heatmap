from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import compute_surge_multiplier


class SurgePricingView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            latitude = float(request.query_params.get('latitude'))
            longitude = float(request.query_params.get('longitude'))
            vehicle_type = request.query_params.get('vehicle_type', 'car')
        except (TypeError, ValueError):
            return Response({'detail': 'latitude and longitude are required.'}, status=status.HTTP_400_BAD_REQUEST)

        available_drivers = 5
        active_requests = 30
        multiplier = compute_surge_multiplier(available_drivers, active_requests)
        return Response({
            'h3_cell': 'ktm-demo-cell',
            'latitude': latitude,
            'longitude': longitude,
            'available_drivers': available_drivers,
            'active_requests': active_requests,
            'surge_multiplier': round(multiplier, 2),
            'surge_status': 'high_demand' if multiplier > 1.2 else 'normal',
            'vehicle_type': vehicle_type,
        }, status=status.HTTP_200_OK)
