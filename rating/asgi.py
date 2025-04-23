import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Установите настройки Django по умолчанию
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rating.settings')

# Базовое ASGI-приложение для HTTP
django_asgi_app = get_asgi_application()

# Импортируйте ваш WebSocket-роутер
from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    # HTTP-запросы будут обрабатываться стандартным Django-приложением
    "http": django_asgi_app,

    # WebSocket-запросы будут обрабатываться Channels
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})