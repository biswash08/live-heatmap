from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from apps.heatmap.consumers import HeatmapConsumer

application = ProtocolTypeRouter({
    'http': None,
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/v1/heatmap/<str:city_id>/', HeatmapConsumer.as_asgi()),
        ])
    ),
})
