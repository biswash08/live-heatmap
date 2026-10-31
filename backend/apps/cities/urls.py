from django.urls import path

from .views import CityAddressSearchView, CityDirectoryView

urlpatterns = [
    path('', CityDirectoryView.as_view(), name='city-directory'),
    path('<str:city_id>/addresses/', CityAddressSearchView.as_view(), name='city-address-search'),
]
