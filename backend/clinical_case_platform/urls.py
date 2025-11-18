"""
URL configuration for clinical_case_platform project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# Import ViewSets and functions that need top-level routing
from cases.views import CaseGroupViewSet, guest_access_case, my_shared_cases, accessible_cases, cleanup_expired_permissions

# Health check endpoint
def health_check(request):
    """Health check endpoint for deployment monitoring"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'Clinical Case Platform API',
        'version': '1.0.0',
        'database': 'connected'
    })

# Create router for top-level API endpoints
router = DefaultRouter()
router.register(r'case-groups', CaseGroupViewSet, basename='case-groups')

urlpatterns = [
    # Health check
    path("api/health/", health_check, name="health-check"),
    # Admin
    path("admin/", admin.site.urls),
    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path('api-auth/', include('rest_framework.urls')),
    
    # Top-level API router
    path("api/", include(router.urls)),
    # Top-level API endpoints
    path("api/guest-access/<str:access_token>/", guest_access_case, name="guest-access-case"),
    path("api/my-shared-cases/", my_shared_cases, name="my-shared-cases"),
    path("api/accessible-cases/", accessible_cases, name="accessible-cases"),
    path("api/cleanup-expired-permissions/", cleanup_expired_permissions, name="cleanup-expired-permissions"),
    # API endpoints
    path("api/auth/", include("accounts.urls")),
    path("api/cases/", include("cases.urls")),
    path("api/templates/", include("templates.urls")),
    path("api/repositories/", include("repositories.urls")),
    path("api/comments/", include("comments.urls")),
    path("api/feedback/", include("feedback.urls")),
    path("api/exports/", include("exports.urls")),
    path("api/grades/", include("grades.urls")),
    # Analytics URLs
    path('api/', include('cases.analytics_urls')),
    # Validation URLs
    path('api/', include('cases.validation_urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
