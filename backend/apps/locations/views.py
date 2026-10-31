from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LocationEventSerializer
from .services import resolve_location_from_coordinates, validate_event_structure


class LocationHealthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'status': 'ok', 'service': 'locations'}, status=status.HTTP_200_OK)


class LocationEventView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = LocationEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        valid, error = validate_event_structure(serializer.validated_data)
        if not valid:
            return Response({'detail': error}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {'success': True, 'message': 'Location event accepted for processing', 'driver_id': str(request.user.id)},
            status=status.HTTP_202_ACCEPTED,
        )


class LocationResolveView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')
        city_id = request.query_params.get('city_id')

        if latitude is None or longitude is None:
            return Response({'detail': 'latitude and longitude are required.'}, status=status.HTTP_400_BAD_REQUEST)

        resolved = resolve_location_from_coordinates(latitude, longitude, city_id=city_id)
        if resolved is None:
            return Response({'detail': 'Could not resolve location from coordinates.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(resolved)

    def post(self, request, *args, **kwargs):
        payload = request.data or {}
        latitude = payload.get('latitude')
        longitude = payload.get('longitude')
        city_id = payload.get('city_id')

        if latitude is None or longitude is None:
            return Response({'detail': 'latitude and longitude are required.'}, status=status.HTTP_400_BAD_REQUEST)

        resolved = resolve_location_from_coordinates(latitude, longitude, city_id=city_id)
        if resolved is None:
            return Response({'detail': 'Could not resolve location from coordinates.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(resolved)
