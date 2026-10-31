from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import RideRequest
from .serializers import RideRequestSerializer


class RideRequestCreateView(generics.CreateAPIView):
    queryset = RideRequest.objects.all()
    serializer_class = RideRequestSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ride_request = serializer.save(status='pending')
        return Response(
            {
                'message': 'Ride request created successfully.',
                'request_id': ride_request.request_id,
                'status': ride_request.status,
                'ride': RideRequestSerializer(ride_request).data,
            },
            status=status.HTTP_201_CREATED,
        )


class RideRequestListView(generics.ListAPIView):
    queryset = RideRequest.objects.all().order_by('-created_at')
    serializer_class = RideRequestSerializer
    permission_classes = [AllowAny]
