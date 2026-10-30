from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LocationEventSerializer
from .services import validate_event_structure


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
