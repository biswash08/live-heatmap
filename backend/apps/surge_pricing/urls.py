from django.urls import path

from .views import SurgePricingView

urlpatterns = [
    path('surge/', SurgePricingView.as_view(), name='surge-pricing'),
]
