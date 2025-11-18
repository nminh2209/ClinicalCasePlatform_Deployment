from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import ExportTemplate, CaseExport, BatchExport


@admin.register(ExportTemplate)
class ExportTemplateAdmin(admin.ModelAdmin):
    """
    Admin interface for export templates
    """

    list_display = [
        "name",
        "vietnamese_name",
        "template_type",
        "is_active",
        "is_system_template",
        "created_by",
        "created_at",
    ]
    list_filter = [
        "template_type",
        "is_active",
        "is_system_template",
        "created_at",
    ]
    search_fields = ["name", "vietnamese_name", "description"]
    readonly_fields = ["created_at", "updated_at"]
    filter_horizontal = []

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "vietnamese_name",
                    "description",
                    "template_type",
                )
            },
        ),
        (
            "Content Inclusion",
            {
                "fields": (
                    "include_patient_details",
                    "include_medical_history",
                    "include_examination",
                    "include_investigations",
                    "include_diagnosis",
                    "include_treatment",
                    "include_learning_objectives",
                    "include_comments",
                    "include_attachments",
                    "include_grades",
                )
            },
        ),
        (
            "Formatting Options",
            {
                "fields": (
                    "anonymize_patient",
                    "add_watermark",
                    "watermark_text",
                    "header_text",
                    "footer_text",
                    "logo_url",
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "created_by",
                    "is_active",
                    "is_system_template",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # New object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(CaseExport)
class CaseExportAdmin(admin.ModelAdmin):
    """
    Admin interface for case exports
    """

    list_display = [
        "id",
        "case_link",
        "user_link",
        "export_format",
        "status",
        "file_size_display",
        "download_count",
        "exported_at",
        "download_link",
    ]
    list_filter = [
        "export_format",
        "status",
        "exported_at",
        "template_used",
    ]
    search_fields = [
        "case__title",
        "user__username",
        "user__email",
    ]
    readonly_fields = [
        "exported_at",
        "completed_at",
        "file_hash",
        "download_count",
        "last_downloaded_at",
        "ip_address",
        "user_agent",
    ]
    date_hierarchy = "exported_at"

    fieldsets = (
        (
            "Export Information",
            {
                "fields": (
                    "case",
                    "user",
                    "export_format",
                    "status",
                    "template_used",
                )
            },
        ),
        (
            "File Information",
            {
                "fields": (
                    "file_path",
                    "file_size",
                    "file_hash",
                )
            },
        ),
        (
            "Settings & Metadata",
            {
                "fields": (
                    "export_settings",
                    "exported_at",
                    "completed_at",
                    "expires_at",
                )
            },
        ),
        (
            "Usage Statistics",
            {
                "fields": (
                    "download_count",
                    "last_downloaded_at",
                )
            },
        ),
        (
            "Error Information",
            {
                "fields": (
                    "error_message",
                    "retry_count",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Audit Trail",
            {
                "fields": (
                    "ip_address",
                    "user_agent",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def case_link(self, obj):
        """Link to the case"""
        url = reverse("admin:cases_case_change", args=[obj.case.id])
        return format_html('<a href="{}">{}</a>', url, obj.case.title[:50])

    case_link.short_description = "Case"

    def user_link(self, obj):
        """Link to the user"""
        url = reverse("admin:accounts_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)

    user_link.short_description = "User"

    def file_size_display(self, obj):
        """Display file size in human-readable format"""
        if obj.file_size:
            size = obj.file_size
            for unit in ["B", "KB", "MB", "GB"]:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        return "-"

    file_size_display.short_description = "File Size"

    def download_link(self, obj):
        """Display download link if file is available"""
        if obj.status == CaseExport.ExportStatus.COMPLETED and obj.file_path:
            return format_html(
                '<a href="{}" target="_blank">Download</a>', obj.file_path.url
            )
        return "-"

    download_link.short_description = "Download"

    actions = ["mark_expired", "recalculate_hash"]

    def mark_expired(self, request, queryset):
        """Mark selected exports as expired"""
        count = queryset.update(status=CaseExport.ExportStatus.EXPIRED)
        self.message_user(request, f"{count} exports marked as expired.")

    mark_expired.short_description = "Mark selected exports as expired"

    def recalculate_hash(self, request, queryset):
        """Recalculate file hash for selected exports"""
        count = 0
        for export in queryset:
            if export.calculate_file_hash():
                count += 1
        self.message_user(request, f"Recalculated hash for {count} exports.")

    recalculate_hash.short_description = "Recalculate file hash"


@admin.register(BatchExport)
class BatchExportAdmin(admin.ModelAdmin):
    """
    Admin interface for batch exports
    """

    list_display = [
        "id",
        "user_link",
        "export_format",
        "status",
        "progress_display",
        "total_cases",
        "created_at",
        "download_link",
    ]
    list_filter = [
        "export_format",
        "status",
        "created_at",
        "compress_output",
    ]
    search_fields = [
        "user__username",
        "user__email",
        "batch_name",
    ]
    readonly_fields = [
        "total_cases",
        "processed_cases",
        "failed_cases",
        "created_at",
        "started_at",
        "completed_at",
        "task_id",
        "zip_file_size",
    ]
    date_hierarchy = "created_at"
    filter_horizontal = ["cases"]

    fieldsets = (
        (
            "Batch Information",
            {
                "fields": (
                    "user",
                    "batch_name",
                    "export_format",
                    "template_used",
                    "status",
                )
            },
        ),
        (
            "Cases",
            {
                "fields": ("cases",)
            },
        ),
        (
            "Configuration",
            {
                "fields": (
                    "export_settings",
                    "compress_output",
                    "expires_at",
                )
            },
        ),
        (
            "Progress",
            {
                "fields": (
                    "total_cases",
                    "processed_cases",
                    "failed_cases",
                )
            },
        ),
        (
            "Output",
            {
                "fields": (
                    "zip_file",
                    "zip_file_size",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "started_at",
                    "completed_at",
                )
            },
        ),
        (
            "Task Information",
            {
                "fields": (
                    "task_id",
                    "error_message",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def user_link(self, obj):
        """Link to the user"""
        url = reverse("admin:accounts_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)

    user_link.short_description = "User"

    def progress_display(self, obj):
        """Display progress bar"""
        if obj.total_cases == 0:
            percentage = 0
        else:
            percentage = (obj.processed_cases / obj.total_cases) * 100

        color = "green" if obj.status == BatchExport.BatchStatus.COMPLETED else "blue"
        if obj.status == BatchExport.BatchStatus.FAILED:
            color = "red"

        return format_html(
            '<div style="width:100px; background-color:#f0f0f0;">'
            '<div style="width:{}%; background-color:{}; height:20px;"></div>'
            "</div>"
            '<small>{}/{} ({}%)</small>',
            percentage,
            color,
            obj.processed_cases,
            obj.total_cases,
            round(percentage, 1),
        )

    progress_display.short_description = "Progress"

    def download_link(self, obj):
        """Display download link if ZIP file is available"""
        if obj.status == BatchExport.BatchStatus.COMPLETED and obj.zip_file:
            return format_html(
                '<a href="{}" target="_blank">Download ZIP</a>', obj.zip_file.url
            )
        return "-"

    download_link.short_description = "Download"

    actions = ["cancel_batch", "retry_batch"]

    def cancel_batch(self, request, queryset):
        """Cancel selected batch exports"""
        count = queryset.filter(
            status__in=[BatchExport.BatchStatus.QUEUED, BatchExport.BatchStatus.PROCESSING]
        ).update(status=BatchExport.BatchStatus.CANCELLED)
        self.message_user(request, f"{count} batch exports cancelled.")

    cancel_batch.short_description = "Cancel selected batch exports"

    def retry_batch(self, request, queryset):
        """Retry failed batch exports"""
        from .tasks import process_batch_export

        count = 0
        for batch in queryset.filter(status=BatchExport.BatchStatus.FAILED):
            batch.status = BatchExport.BatchStatus.QUEUED
            batch.error_message = ""
            batch.save()
            task = process_batch_export.delay(batch.id)
            batch.task_id = task.id
            batch.save()
            count += 1

        self.message_user(request, f"{count} batch exports queued for retry.")

    retry_batch.short_description = "Retry failed batch exports"