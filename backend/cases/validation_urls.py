"""
URL Configuration for Validation System
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .validation_views import (
    CaseValidationRuleViewSet,
    CaseValidationViewSet,
    CaseSubmissionWorkflowViewSet,
    MedicalTerminologyViewSet,
    CaseQualityMetricsViewSet,
)

router = DefaultRouter()
router.register(
    r"validation-rules", CaseValidationRuleViewSet, basename="validation-rules"
)
router.register(r"case-validation", CaseValidationViewSet, basename="case-validation")
router.register(
    r"submission-workflow",
    CaseSubmissionWorkflowViewSet,
    basename="submission-workflow",
)
router.register(
    r"medical-terminology", MedicalTerminologyViewSet, basename="medical-terminology"
)
router.register(
    r"case-quality-metrics", CaseQualityMetricsViewSet, basename="case-quality-metrics"
)

urlpatterns = [
    path("", include(router.urls)),
]
