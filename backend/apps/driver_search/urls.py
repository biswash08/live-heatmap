from django.urls import path

from .views import NearbyDriversView

urlpatterns = [
    path('nearby-drivers/', NearbyDriversView.as_view(), name='nearby-drivers'),
]
