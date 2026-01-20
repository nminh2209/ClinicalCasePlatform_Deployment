"""
WebSocket routing for OCR module.
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/ocr/(?P<job_id>[a-f0-9-]+)/$", consumers.OCRProgressConsumer.as_asgi()),
]
