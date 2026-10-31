from django.urls import path

from .views import RideRequestCreateView, RideRequestListView

urlpatterns = [
    path('requests/', RideRequestCreateView.as_view(), name='ride-request-create'),
    path('requests/list/', RideRequestListView.as_view(), name='ride-request-list'),
]
