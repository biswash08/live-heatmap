from django.urls import path

from .views import DriverLocationInboundView, DriverStatusView

urlpatterns = [
    path('location/', DriverLocationInboundView.as_view(), name='driver-location-ingest'),
    path('status/', DriverStatusView.as_view(), name='driver-status-update'),
]
