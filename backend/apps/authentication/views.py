from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .services import build_auth_response


class AuthHealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response(build_auth_response(), status=status.HTTP_200_OK)


class DriverTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]


class DriverTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
