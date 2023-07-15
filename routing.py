from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from websocket_app.consumers import ProctorConsumer

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(
                [
                    re_path(r'ws/video_stream/$', ProctorConsumer.as_asgi()),
                ]
            )
        ),
    }
)
