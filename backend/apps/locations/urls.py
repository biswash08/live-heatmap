from django.urls import path

from .views import LocationEventView, LocationHealthView

urlpatterns = [
    path('health/', LocationHealthView.as_view(), name='locations-health'),
    path('events/', LocationEventView.as_view(), name='location-event'),
]
