from django.urls import path

from .views import HeatmapView

urlpatterns = [
    path('<str:city_id>/', HeatmapView.as_view(), name='heatmap-city-view'),
]
