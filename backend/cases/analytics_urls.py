"""
URL Configuration for Analytics System
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .analytics_views import (
    CaseAnalyticsViewSet,
    StudentEngagementViewSet,
    AnalyticsDashboardViewSet,
    PlatformStatisticsViewSet,
)

router = DefaultRouter()
router.register(r"case-analytics", CaseAnalyticsViewSet, basename="case-analytics")
router.register(
    r"student-engagement", StudentEngagementViewSet, basename="student-engagement"
)
router.register(
    r"analytics-dashboard", AnalyticsDashboardViewSet, basename="analytics-dashboard"
)
router.register(
    r"platform-statistics", PlatformStatisticsViewSet, basename="platform-statistics"
)

urlpatterns = [
    path("", include(router.urls)),
]
