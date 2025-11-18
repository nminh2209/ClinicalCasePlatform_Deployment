"""
Celery tasks for asynchronous export processing
"""

try:
    from celery import shared_task
    CELERY_AVAILABLE = True
except ImportError:
    # Celery not installed, create a dummy decorator
    CELERY_AVAILABLE = False
    def shared_task(*args, **kwargs):
        def decorator(func):
            return func
        if len(args) == 1 and callable(args[0]):
            return args[0]
        return decorator

from django.core.files.base import ContentFile
from django.utils import timezone
from datetime import timedelta
import zipfile
import io
import os
from .models import CaseExport, BatchExport, ExportTemplate
from .utils import PDFExporter, PDFExporterHTML, WordExporter, JSONExporter
from cases.models import Case


@shared_task(bind=True, max_retries=3)
def process_case_export(self, export_id):
    """
    Process a single case export asynchronously
    """
    try:
        export = CaseExport.objects.get(id=export_id)
        export.status = CaseExport.ExportStatus.PROCESSING
        export.save()

        case = export.case
        template = export.template_used

        # Generate export based on format
        if export.export_format == CaseExport.ExportFormat.PDF:
            exporter = PDFExporterHTML(template=template)  # HTML-based for better Vietnamese support
            file_extension = "pdf"
            content_type = "application/pdf"
        elif export.export_format == CaseExport.ExportFormat.WORD:
            exporter = WordExporter(template=template)
            file_extension = "docx"
            content_type = (
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        elif export.export_format == CaseExport.ExportFormat.JSON:
            exporter = JSONExporter(template=template)
            file_extension = "json"
            content_type = "application/json"
        else:
            raise ValueError(f"Unsupported export format: {export.export_format}")

        # Generate the export
        buffer = exporter.generate(case)

        # Save the file
        filename = f"{case.title}_{export.export_format}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{file_extension}"
        # Clean filename
        filename = "".join(
            c for c in filename if c.isalnum() or c in (" ", ".", "_", "-")
        ).rstrip()

        export.file_path.save(filename, ContentFile(buffer.getvalue()), save=False)
        export.file_size = buffer.getbuffer().nbytes
        export.status = CaseExport.ExportStatus.COMPLETED
        export.completed_at = timezone.now()

        # Set expiration (default 30 days)
        if not export.expires_at:
            export.expires_at = timezone.now() + timedelta(days=30)

        export.save()

        # Calculate file hash
        export.calculate_file_hash()

        return {
            "status": "success",
            "export_id": export.id,
            "file_size": export.file_size,
        }

    except CaseExport.DoesNotExist:
        return {"status": "error", "message": "Export not found"}
    except Exception as exc:
        export.status = CaseExport.ExportStatus.FAILED
        export.error_message = str(exc)
        export.retry_count += 1
        export.save()

        # Retry if not exceeded max retries
        if export.retry_count < 3:
            raise self.retry(exc=exc, countdown=60 * export.retry_count)

        return {"status": "error", "message": str(exc)}


@shared_task(bind=True)
def process_batch_export(self, batch_export_id):
    """
    Process batch export of multiple cases
    """
    try:
        batch = BatchExport.objects.get(id=batch_export_id)
        batch.status = BatchExport.BatchStatus.PROCESSING
        batch.started_at = timezone.now()
        batch.save()

        cases = batch.cases.all()
        batch.total_cases = cases.count()
        batch.save()

        # Create a ZIP file to contain all exports
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            processed = 0
            failed = 0

            for case in cases:
                try:
                    # Generate export based on format
                    template = batch.template_used

                    if batch.export_format == CaseExport.ExportFormat.PDF:
                        exporter = PDFExporterHTML(template=template)  # HTML-based for better Vietnamese support
                        file_extension = "pdf"
                    elif batch.export_format == CaseExport.ExportFormat.WORD:
                        exporter = WordExporter(template=template)
                        file_extension = "docx"
                    elif batch.export_format == CaseExport.ExportFormat.JSON:
                        exporter = JSONExporter(template=template)
                        file_extension = "json"
                    else:
                        failed += 1
                        continue

                    # Generate the export
                    buffer = exporter.generate(case)

                    # Add to ZIP
                    filename = f"{case.id}_{case.title[:50]}.{file_extension}"
                    # Clean filename
                    filename = "".join(
                        c for c in filename if c.isalnum() or c in (" ", ".", "_", "-")
                    ).rstrip()

                    zip_file.writestr(filename, buffer.getvalue())

                    processed += 1
                    batch.update_progress(processed=processed, failed=failed)

                except Exception as e:
                    failed += 1
                    batch.update_progress(processed=processed, failed=failed)
                    # Log error but continue processing other cases
                    print(f"Error processing case {case.id}: {str(e)}")

        # Save ZIP file
        zip_buffer.seek(0)
        zip_filename = f"batch_export_{batch.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.zip"

        batch.zip_file.save(zip_filename, ContentFile(zip_buffer.getvalue()), save=False)
        batch.zip_file_size = zip_buffer.getbuffer().nbytes
        batch.status = BatchExport.BatchStatus.COMPLETED
        batch.completed_at = timezone.now()

        # Set expiration (default 7 days for batch exports)
        if not batch.expires_at:
            batch.expires_at = timezone.now() + timedelta(days=7)

        batch.save()

        return {
            "status": "success",
            "batch_id": batch.id,
            "processed": processed,
            "failed": failed,
            "total": batch.total_cases,
        }

    except BatchExport.DoesNotExist:
        return {"status": "error", "message": "Batch export not found"}
    except Exception as exc:
        batch.status = BatchExport.BatchStatus.FAILED
        batch.error_message = str(exc)
        batch.save()
        return {"status": "error", "message": str(exc)}


@shared_task
def cleanup_expired_exports():
    """
    Periodic task to clean up expired export files
    """
    from django.utils import timezone

    # Find expired exports
    expired_exports = CaseExport.objects.filter(
        expires_at__lt=timezone.now(), status=CaseExport.ExportStatus.COMPLETED
    )

    count = 0
    for export in expired_exports:
        try:
            # Delete the file
            if export.file_path:
                export.file_path.delete(save=False)

            # Mark as expired
            export.status = CaseExport.ExportStatus.EXPIRED
            export.save()
            count += 1
        except Exception as e:
            print(f"Error cleaning up export {export.id}: {str(e)}")

    # Clean up expired batch exports
    expired_batches = BatchExport.objects.filter(
        expires_at__lt=timezone.now(), status=BatchExport.BatchStatus.COMPLETED
    )

    batch_count = 0
    for batch in expired_batches:
        try:
            # Delete the ZIP file
            if batch.zip_file:
                batch.zip_file.delete(save=False)

            batch.status = BatchExport.BatchStatus.CANCELLED
            batch.save()
            batch_count += 1
        except Exception as e:
            print(f"Error cleaning up batch export {batch.id}: {str(e)}")

    return {
        "status": "success",
        "cleaned_exports": count,
        "cleaned_batches": batch_count,
    }


@shared_task
def generate_export_report(user_id, start_date=None, end_date=None):
    """
    Generate export usage report for a user
    """
    from django.contrib.auth import get_user_model
    from django.db.models import Count, Sum

    User = get_user_model()

    try:
        user = User.objects.get(id=user_id)

        # Build query filters
        filters = {"user": user}
        if start_date:
            filters["exported_at__gte"] = start_date
        if end_date:
            filters["exported_at__lte"] = end_date

        # Get export statistics
        exports = CaseExport.objects.filter(**filters)

        stats = {
            "total_exports": exports.count(),
            "exports_by_format": dict(
                exports.values("export_format").annotate(count=Count("id"))
            ),
            "exports_by_status": dict(
                exports.values("status").annotate(count=Count("id"))
            ),
            "total_downloads": exports.aggregate(Sum("download_count"))[
                "download_count__sum"
            ]
            or 0,
            "total_file_size": exports.aggregate(Sum("file_size"))["file_size__sum"]
            or 0,
        }

        return {"status": "success", "stats": stats}

    except User.DoesNotExist:
        return {"status": "error", "message": "User not found"}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}
