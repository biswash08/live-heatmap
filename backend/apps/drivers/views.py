from uuid import uuid4

from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cities.seed import get_default_city
from workers.kafka_producer import DriverLocationProducer
from .serializers import DriverLocationRequestSerializer, DriverStatusSerializer
from .services import build_location_acknowledgement, validate_driver_event


class DriverLocationInboundView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = DriverLocationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        valid, error = validate_driver_event(serializer.validated_data)
        if not valid:
            return Response({'detail': error}, status=status.HTTP_400_BAD_REQUEST)

        payload = dict(serializer.validated_data)
        payload['driver_id'] = str(request.user.id)
        payload['event_id'] = f'location_event_{uuid4().hex[:12]}'
        payload['city_id'] = get_default_city()['id']

        try:
            producer = DriverLocationProducer(
                settings.KAFKA_BOOTSTRAP_SERVERS,
                settings.KAFKA_TOPIC_DRIVER_LOCATION,
            )
            producer.send(payload['driver_id'], payload)
            producer.flush()
        except Exception:
            pass

        acknowledgement = build_location_acknowledgement()
        acknowledgement['driver_id'] = payload['driver_id']
        acknowledgement['event_id'] = payload['event_id']
        return Response(acknowledgement, status=status.HTTP_202_ACCEPTED)


class DriverStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = DriverStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {
                'success': True,
                'driver_id': str(request.user.id),
                'status': serializer.validated_data['status'],
            },
            status=status.HTTP_200_OK,
        )
