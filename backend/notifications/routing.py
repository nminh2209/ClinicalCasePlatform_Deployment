from django.urls import re_path
from . import consumers

# Import OCR routing
from ai.ocr.routing import websocket_urlpatterns as ocr_websocket_urlpatterns

websocket_urlpatterns = [
    re_path(r"ws/notifications/$", consumers.NotificationConsumer.as_asgi()),
] + ocr_websocket_urlpatterns

