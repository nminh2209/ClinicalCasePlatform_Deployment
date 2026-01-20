# inquiries/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InquiryViewSet, InquiryResponseViewSet

router = DefaultRouter()
router.register(r"threads", InquiryViewSet, basename="inquiry")
router.register(r"responses", InquiryResponseViewSet, basename="inquiry-response")

urlpatterns = [
    path("", include(router.urls)),
]
