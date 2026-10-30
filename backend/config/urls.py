from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/drivers/', include('apps.drivers.urls')),
    path('api/v1/locations/', include('apps.locations.urls')),
    path('api/v1/heatmap/', include('apps.heatmap.urls')),
    path('api/v1/riders/', include('apps.driver_search.urls')),
    path('api/v1/pricing/', include('apps.surge_pricing.urls')),
]
