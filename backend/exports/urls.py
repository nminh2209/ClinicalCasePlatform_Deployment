from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # ViewSets
    ExportTemplateViewSet,
    CaseExportViewSet,
    BatchExportViewSet,
    # Export Views
    quick_export_pdf,
    export_case_word,
    export_case_json,
    # Utility Views
    export_formats,
)

app_name = "exports"

# Create router for ViewSets
router = DefaultRouter()
router.register(r"templates", ExportTemplateViewSet, basename="template")
router.register(r"case-exports", CaseExportViewSet, basename="case-export")
router.register(r"batch-exports", BatchExportViewSet, basename="batch-export")

urlpatterns = [
    # Router URLs
    path("", include(router.urls)),
    
    # Quick Export APIs (Synchronous, immediate download)
    path(
        "quick/cases/<int:case_id>/pdf/",
        quick_export_pdf,
        name="quick-export-pdf",
    ),
    path(
        "cases/<int:case_id>/word/",
        export_case_word,
        name="export-case-word",
    ),
    path(
        "cases/<int:case_id>/json/",
        export_case_json,
        name="export-case-json",
    ),
    
    # Utility endpoints
    path("formats/", export_formats, name="export-formats"),
]