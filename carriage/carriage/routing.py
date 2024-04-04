from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from myapp.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:room_id>/', ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})