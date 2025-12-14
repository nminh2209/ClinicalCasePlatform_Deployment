import io
from datetime import timedelta
from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count, Sum, Q
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from cases.models import Case
from .models import CaseExport, ExportTemplate, BatchExport
from .serializers import (
    CaseExportSerializer,
    CaseExportListSerializer,
    CaseExportCreateSerializer,
    ExportTemplateSerializer,
    ExportTemplateListSerializer,
    BatchExportSerializer,
    BatchExportCreateSerializer,
    ExportStatsSerializer,
)
from .utils import PDFExporter, PDFExporterHTML, WordExporter, JSONExporter

try:
    from .tasks import process_case_export, process_batch_export

    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False
    process_case_export = None
    process_batch_export = None

# Try to import export libraries (install if needed)
# ============================================================================
# Permissions & Utility Functions
# ============================================================================


class IsOwnerOrInstructor(permissions.BasePermission):
    """
    Custom permission: Users can only access their own exports or instructors/admins can access any
    """

    def has_object_permission(self, request, view, obj):
        # Admins and instructors can access any export
        if request.user.role in ["admin", "instructor"]:  # type: ignore[attr-defined]
            return True

        # Users can access their own exports
        if hasattr(obj, "exported_by"):
            return obj.exported_by == request.user

        # For case exports, check if user created the case
        if hasattr(obj, "case"):
            return obj.case.student == request.user

        return False


def can_export_case(user, case):
    """Check if user has permission to export a case"""
    if not user:
        return False

    if user.role in ["admin", "instructor"]:
        return True

    if user.role == "student" and case.student == user:
        return True

    return False


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to be safe for file systems while preserving Vietnamese characters
    """
    import re
    import unicodedata

    # Allow all Unicode letters (including Vietnamese), numbers, spaces, hyphens, and underscores
    # Replace other characters with underscores
    sanitized = re.sub(r"[^\w\s\-]", "_", filename, flags=re.UNICODE)

    # Replace multiple consecutive underscores with single underscore
    sanitized = re.sub(r"_+", "_", sanitized)

    # Remove leading/trailing underscores
    sanitized = sanitized.strip("_")

    # Limit length to prevent filesystem issues
    return sanitized[:100] if sanitized else "export"


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination for export lists"""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


# ============================================================================
# Export Template ViewSet
# ============================================================================


class ExportTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing export templates

    Lists, creates, retrieves, updates, and deletes export templates.
    Instructors and admins can manage templates, students can view.
    """

    queryset = ExportTemplate.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == "list":
            return ExportTemplateListSerializer
        return ExportTemplateSerializer

    def get_queryset(self):
        """Filter active templates, instructors/admins see all"""
        queryset = ExportTemplate.objects.all()

        # Students only see active templates
        if self.request.user.role == "student":  # type: ignore[attr-defined]
            queryset = queryset.filter(is_active=True)

        # Filter by type if specified
        template_type = self.request.query_params.get("type", None)
        if template_type:
            queryset = queryset.filter(template_type=template_type)

        return queryset.order_by("-created_at")

    def perform_create(self, serializer):
        """Set created_by to current user"""
        # Only instructors and admins can create templates
        if self.request.user.role not in ["admin", "instructor"]:  # type: ignore[attr-defined]
            raise permissions.PermissionDenied(  # type: ignore[attr-defined]
                "Only instructors and admins can create templates"
            )

        serializer.save(created_by=self.request.user)

    def perform_destroy(self, instance):
        """Prevent deletion of system templates"""
        if instance.is_system_template:
            raise permissions.PermissionDenied("Cannot delete system templates")  # type: ignore[attr-defined]

        # Only creator, instructors, or admins can delete
        if instance.created_by != self.request.user and self.request.user.role not in [  # type: ignore[attr-defined]
            "admin",
            "instructor",
        ]:
            raise permissions.PermissionDenied(  # type: ignore[attr-defined]
                "You don't have permission to delete this template"
            )

        instance.delete()


# ============================================================================
# Case Export ViewSet
# ============================================================================


class CaseExportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing case exports

    Supports creating, listing, retrieving, and deleting case exports.
    Provides filtering, search, and download functionality.
    """

    queryset = CaseExport.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrInstructor]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == "create":
            return CaseExportCreateSerializer
        elif self.action == "list":
            return CaseExportListSerializer
        return CaseExportSerializer

    def get_queryset(self):
        """Filter exports based on user role and query parameters"""
        user = self.request.user
        queryset = CaseExport.objects.select_related(
            "case", "exported_by", "template_used"
        ).all()

        # Students can only see their own exports
        if user.role == "student":  # type: ignore[attr-defined]
            queryset = queryset.filter(Q(exported_by=user) | Q(case__student=user))
        # Instructors can see exports from their department
        elif user.role == "instructor" and hasattr(user, "department"):  # type: ignore[attr-defined]
            # Can add department filtering here
            pass
        # Admins can see all exports

        # Filter by status
        status_filter = self.request.query_params.get("status", None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Filter by format
        format_filter = self.request.query_params.get("format", None)
        if format_filter:
            queryset = queryset.filter(export_format=format_filter)

        # Filter by case
        case_id = self.request.query_params.get("case", None)
        if case_id:
            queryset = queryset.filter(case_id=case_id)

        # Filter by date range
        start_date = self.request.query_params.get("start_date", None)
        if start_date:
            queryset = queryset.filter(exported_at__gte=start_date)

        end_date = self.request.query_params.get("end_date", None)
        if end_date:
            queryset = queryset.filter(exported_at__lte=end_date)

        return queryset.order_by("-exported_at")

    def perform_create(self, serializer):
        """Create export and optionally process asynchronously"""
        export = serializer.save()

        # Check if async processing is requested
        use_async = self.request.data.get("async", True)

        if use_async and CELERY_AVAILABLE:
            # Queue the export task
            process_case_export.delay(export.id)  # type: ignore[attr-defined]
        elif CELERY_AVAILABLE:
            # Process synchronously (for small exports)
            process_case_export(export.id)  # type: ignore[attr-defined]
        else:
            # Celery not available, mark as pending
            export.status = CaseExport.ExportStatus.PENDING
            export.save()

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        """Download exported file"""
        export = self.get_object()

        # Check if export is completed
        if export.status != CaseExport.ExportStatus.COMPLETED:
            return Response(
                {
                    "error": f"Export is not ready. Current status: {export.get_status_display()}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if export has expired
        if export.is_expired():
            return Response(
                {"error": "Export has expired"}, status=status.HTTP_410_GONE
            )

        # Check if file exists
        if not export.file_path:
            return Response(
                {"error": "Export file not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Increment download count
        export.increment_download_count()

        # Return file
        response = FileResponse(
            export.file_path.open("rb"),
            as_attachment=True,
            filename=export.file_path.name.split("/")[-1],
        )
        return response

    @action(detail=False, methods=["get"])
    def stats(self, request):
        """Get export statistics for current user"""
        user = request.user

        # Build query based on user role
        if user.role == "student":
            exports = CaseExport.objects.filter(
                Q(exported_by=user) | Q(case__student=user)
            )
        else:
            exports = CaseExport.objects.all()

        # Calculate statistics
        total_exports = exports.count()

        exports_by_format = dict(
            exports.values("export_format")
            .annotate(count=Count("id"))
            .values_list("export_format", "count")
        )

        exports_by_status = dict(
            exports.values("status")
            .annotate(count=Count("id"))
            .values_list("status", "count")
        )

        total_downloads = (
            exports.aggregate(Sum("download_count"))["download_count__sum"] or 0
        )

        total_file_size = exports.aggregate(Sum("file_size"))["file_size__sum"] or 0

        recent_exports = exports.order_by("-exported_at")[:5]

        # Popular templates
        popular_templates = (
            exports.filter(template_used__isnull=False)
            .values("template_used__name")
            .annotate(count=Count("id"))
            .order_by("-count")[:5]
        )

        stats_data = {
            "total_exports": total_exports,
            "exports_by_format": exports_by_format,
            "exports_by_status": exports_by_status,
            "total_downloads": total_downloads,
            "total_file_size": total_file_size,
            "recent_exports": CaseExportListSerializer(
                recent_exports, many=True, context={"request": request}
            ).data,
            "popular_templates": list(popular_templates),
        }

        serializer = ExportStatsSerializer(stats_data)
        return Response(serializer.data)


# ============================================================================
# Batch Export ViewSet
# ============================================================================


class BatchExportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing batch exports

    Allows exporting multiple cases at once, with progress tracking.
    """

    queryset = BatchExport.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrInstructor]
    pagination_class = StandardResultsSetPagination
    http_method_names = ["get", "post", "delete"]  # No PUT/PATCH

    def get_serializer_class(self):
        if self.action == "create":
            return BatchExportCreateSerializer
        return BatchExportSerializer

    def get_queryset(self):
        """Filter batch exports based on user"""
        user = self.request.user
        queryset = BatchExport.objects.prefetch_related("cases").all()

        # Students can only see their own batch exports
        if user.role == "student":  # type: ignore[attr-defined]
            queryset = queryset.filter(user=user)

        # Filter by status
        status_filter = self.request.query_params.get("status", None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset.order_by("-created_at")

    def perform_create(self, serializer):
        """Create batch export and queue processing"""
        batch = serializer.save()

        if CELERY_AVAILABLE:
            # Queue the batch export task
            task = process_batch_export.delay(batch.id)  # type: ignore[attr-defined]
            batch.task_id = task.id
            batch.save()
        else:
            # Celery not available, mark as queued
            batch.status = BatchExport.BatchStatus.QUEUED
            batch.save()

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        """Download batch export ZIP file"""
        batch = self.get_object()

        # Check if batch is completed
        if batch.status != BatchExport.BatchStatus.COMPLETED:
            return Response(
                {
                    "error": f"Batch export is not ready. Current status: {batch.get_status_display()}",
                    "progress": {
                        "processed": batch.processed_cases,
                        "total": batch.total_cases,
                        "failed": batch.failed_cases,
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if ZIP file exists
        if not batch.zip_file:
            return Response(
                {"error": "Batch export file not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Return file
        response = FileResponse(
            batch.zip_file.open("rb"),
            as_attachment=True,
            filename=batch.zip_file.name.split("/")[-1],
        )
        return response

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """Cancel a queued or processing batch export"""
        batch = self.get_object()

        if batch.status not in [
            BatchExport.BatchStatus.QUEUED,
            BatchExport.BatchStatus.PROCESSING,
        ]:
            return Response(
                {"error": "Can only cancel queued or processing batch exports"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Revoke Celery task if exists
        if batch.task_id and CELERY_AVAILABLE:
            try:
                from celery import current_app

                current_app.control.revoke(batch.task_id, terminate=True)  # type: ignore[attr-defined]
            except ImportError:
                pass

        batch.status = BatchExport.BatchStatus.CANCELLED
        batch.save()

        return Response({"status": "Batch export cancelled"})


# ============================================================================
# Quick Export API Views (Synchronous)
# ============================================================================


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def quick_export_pdf(request, case_id):
    """
    Quick PDF export (synchronous) for immediate download
    Use for single cases that need immediate export
    Uses HTML-based PDF generation for better Vietnamese support
    """
    try:
        case = get_object_or_404(Case, id=case_id)

        # Check permissions
        if not can_export_case(request.user, case):
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        # Get template if specified
        template_id = request.query_params.get("template", None)
        template = None
        if template_id:
            template = ExportTemplate.objects.filter(id=template_id).first()

        # Generate PDF using HTML-based exporter (better Vietnamese support)
        exporter = PDFExporterHTML(template=template)
        buffer = exporter.generate(case)

        # Create export record
        export = CaseExport.objects.create(
            case=case,
            exported_by=request.user,
            export_format=CaseExport.ExportFormat.PDF,
            template_used=template,
            status=CaseExport.ExportStatus.COMPLETED,
            completed_at=timezone.now(),
            file_size=len(buffer.getvalue()),
        )

        # Return response
        buffer.seek(0)
        response = HttpResponse(buffer.read(), content_type="application/pdf")

        # Safely encode filename for Content-Disposition header
        safe_filename = case.title.replace('"', "").replace("\\", "")[:100] + ".pdf"
        response["Content-Disposition"] = f'attachment; filename="{safe_filename}"'

        return response

    except Exception as e:
        # Log the error for debugging
        import logging

        logger = logging.getLogger(__name__)
        logger.error(f"PDF export failed for case {case_id}: {str(e)}", exc_info=True)

        return Response(
            {"error": f"Export failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def export_case_word(request, case_id):
    """Export case to Word format (legacy) - redirects to quick export"""
    try:
        case = get_object_or_404(Case, id=case_id)

        # Check permissions
        if not can_export_case(request.user, case):
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        # Get template if specified
        template_id = request.query_params.get("template", None)
        template = None
        if template_id:
            template = ExportTemplate.objects.filter(id=template_id).first()

        # Generate Word document
        exporter = WordExporter(template=template)
        buffer = exporter.generate(case)

        # Create export record
        export = CaseExport.objects.create(
            case=case,
            exported_by=request.user,
            export_format=CaseExport.ExportFormat.WORD,
            template_used=template,
            status=CaseExport.ExportStatus.COMPLETED,
            completed_at=timezone.now(),
            file_size=len(buffer.getvalue()),
        )

        # Return response
        buffer.seek(0)
        response = HttpResponse(
            buffer.read(),
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        safe_filename = case.title.replace('"', "").replace("\\", "")[:100] + ".docx"
        response["Content-Disposition"] = f'attachment; filename="{safe_filename}"'

        return response

    except Exception as e:
        return Response(
            {"error": f"Export failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def export_case_json(request, case_id):
    """Export case to JSON format (legacy) - redirects to quick export"""
    try:
        case = get_object_or_404(Case, id=case_id)

        # Check permissions
        if not can_export_case(request.user, case):
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        # Get template if specified
        template_id = request.query_params.get("template", None)
        template = None
        if template_id:
            template = ExportTemplate.objects.filter(id=template_id).first()

        # Generate JSON
        exporter = JSONExporter(template=template)
        buffer = exporter.generate(case)

        # Create export record
        export = CaseExport.objects.create(
            case=case,
            exported_by=request.user,
            export_format=CaseExport.ExportFormat.JSON,
            template_used=template,
            status=CaseExport.ExportStatus.COMPLETED,
            completed_at=timezone.now(),
            file_size=len(buffer.getvalue()),
        )

        # Return response
        buffer.seek(0)
        response = HttpResponse(
            buffer.read(),
            content_type="application/json; charset=utf-8",
        )
        safe_filename = case.title.replace('"', "").replace("\\", "")[:100] + ".json"
        response["Content-Disposition"] = f'attachment; filename="{safe_filename}"'

        return response

    except Exception as e:
        return Response(
            {"error": f"Export failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ============================================================================
# Utility Views
# ============================================================================


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def export_formats(request):
    """List available export formats and their capabilities"""
    formats = [
        {
            "format": "pdf",
            "name": "PDF Document",
            "description": "Professional medical case report in PDF format",
            "supports_vietnamese": True,
            "editable": False,
            "best_for": "Printing, sharing, archival",
        },
        {
            "format": "word",
            "name": "Word Document",
            "description": "Editable Word document (.docx)",
            "supports_vietnamese": True,
            "editable": True,
            "best_for": "Editing, collaboration",
        },
        {
            "format": "json",
            "name": "JSON Data",
            "description": "Structured data export for integration",
            "supports_vietnamese": True,
            "editable": True,
            "best_for": "Data exchange, backup, API integration",
        },
    ]

    return Response(formats)


# ============================================================================
# Export Format Utility Views
# ============================================================================

