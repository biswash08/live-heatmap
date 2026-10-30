from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import build_heatmap_response


class HeatmapView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, city_id, *args, **kwargs):
        try:
            north = float(request.query_params.get('north', 28.0))
            south = float(request.query_params.get('south', 27.0))
            east = float(request.query_params.get('east', 86.0))
            west = float(request.query_params.get('west', 84.0))
            resolution = int(request.query_params.get('resolution', 8))
        except ValueError:
            return Response({'detail': 'Invalid viewport parameters.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            build_heatmap_response(city_id, north, south, east, west, resolution),
            status=status.HTTP_200_OK,
        )
