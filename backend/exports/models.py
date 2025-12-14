from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone
import os
import hashlib


class ExportTemplate(models.Model):
    """
    Custom export templates for different use cases
    """

    class TemplateType(models.TextChoices):
        STANDARD = "standard", "Standard Medical Case"
        ACADEMIC = "academic", "Academic/Teaching"
        RESEARCH = "research", "Research Publication"
        CLINICAL = "clinical", "Clinical Documentation"
        PRESENTATION = "presentation", "Presentation Format"
        ANONYMIZED = "anonymized", "Anonymized/De-identified"

    name = models.CharField(max_length=200, unique=True)
    vietnamese_name = models.CharField(max_length=200, help_text="Tên tiếng Việt")
    description = models.TextField(blank=True)
    template_type = models.CharField(
        max_length=50, choices=TemplateType.choices, default=TemplateType.STANDARD
    )

    # Template configuration
    include_patient_details = models.BooleanField(default=True)
    include_medical_history = models.BooleanField(default=True)
    include_examination = models.BooleanField(default=True)
    include_investigations = models.BooleanField(default=True)
    include_diagnosis = models.BooleanField(default=True)
    include_treatment = models.BooleanField(default=True)
    include_learning_objectives = models.BooleanField(default=True)
    include_comments = models.BooleanField(default=False)
    include_attachments = models.BooleanField(default=True)
    include_grades = models.BooleanField(default=False)

    # Formatting options
    anonymize_patient = models.BooleanField(default=False)
    add_watermark = models.BooleanField(default=False)
    watermark_text = models.CharField(max_length=200, blank=True)
    header_text = models.TextField(blank=True, help_text="Custom header content")
    footer_text = models.TextField(blank=True, help_text="Custom footer content")
    logo_url = models.URLField(blank=True, help_text="Institution logo URL")

    # Template metadata
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_export_templates",
    )
    is_active = models.BooleanField(default=True)
    is_system_template = models.BooleanField(
        default=False, help_text="System-provided template (cannot be deleted)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "exports_exporttemplate"
        verbose_name = "Export Template"
        verbose_name_plural = "Export Templates"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"  # type: ignore[attr-defined]


class CaseExport(models.Model):
    """
    Case export records for tracking exported files with audit trail
    """

    class ExportFormat(models.TextChoices):
        PDF = "pdf", "PDF Document"
        WORD = "word", "Word Document"
        POWERPOINT = "powerpoint", "PowerPoint Presentation"
        JSON = "json", "JSON Data"

    class ExportStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"
        EXPIRED = "expired", "Expired"

    # Export identification
    case = models.ForeignKey(
        "cases.Case", on_delete=models.CASCADE, related_name="exports"
    )
    exported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="exports"
    )
    export_format = models.CharField(max_length=20, choices=ExportFormat.choices)
    status = models.CharField(
        max_length=20, choices=ExportStatus.choices, default=ExportStatus.PENDING
    )

    # File information
    file_path = models.FileField(
        upload_to="exports/%Y/%m/%d/",
        null=True,
        blank=True,
        help_text="Path to the exported file",
    )
    file_size = models.PositiveIntegerField(
        null=True, blank=True, help_text="File size in bytes"
    )
    file_hash = models.CharField(
        max_length=64, blank=True, help_text="SHA-256 hash of the file"
    )

    # Template and settings
    template_used = models.ForeignKey(
        ExportTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="exports",
    )
    export_settings = models.JSONField(
        default=dict,
        help_text="Settings used during export (e.g., include comments, anonymize)",
    )

    # Export metadata
    exported_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    download_count = models.PositiveIntegerField(default=0)
    last_downloaded_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(
        null=True, blank=True, help_text="When this export file should be deleted"
    )

    # Error handling
    error_message = models.TextField(blank=True, help_text="Error message if failed")
    retry_count = models.PositiveIntegerField(default=0)

    # Audit trail
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)

    class Meta:
        db_table = "exports_caseexport"
        verbose_name = "Case Export"
        verbose_name_plural = "Case Exports"
        ordering = ["-exported_at"]
        indexes = [
            models.Index(fields=["exported_by", "-exported_at"]),
            models.Index(fields=["case", "-exported_at"]),
            models.Index(fields=["status", "-exported_at"]),
        ]

    def __str__(self):
        return f"{self.case.title} - {self.export_format.upper()} export by {self.exported_by.username}"

    def calculate_file_hash(self):
        """Calculate SHA-256 hash of the exported file"""
        if self.file_path:
            hasher = hashlib.sha256()
            with self.file_path.open("rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            self.file_hash = hasher.hexdigest()
            self.save(update_fields=["file_hash"])
            return self.file_hash
        return None

    def increment_download_count(self):
        """Increment download counter"""
        self.download_count += 1
        self.last_downloaded_at = timezone.now()
        self.save(update_fields=["download_count", "last_downloaded_at"])

    def is_expired(self):
        """Check if export has expired"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

    def mark_completed(self):
        """Mark export as completed"""
        self.status = self.ExportStatus.COMPLETED
        self.completed_at = timezone.now()
        self.save(update_fields=["status", "completed_at"])

    def mark_failed(self, error_message):
        """Mark export as failed"""
        self.status = self.ExportStatus.FAILED
        self.error_message = error_message
        self.save(update_fields=["status", "error_message"])


class BatchExport(models.Model):
    """
    Batch export for multiple cases
    """

    class BatchStatus(models.TextChoices):
        QUEUED = "queued", "Queued"
        PROCESSING = "processing", "Processing"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"

    # Batch identification
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="batch_exports"
    )
    cases = models.ManyToManyField("cases.Case", related_name="batch_exports")
    export_format = models.CharField(
        max_length=20, choices=CaseExport.ExportFormat.choices
    )
    template_used = models.ForeignKey(
        ExportTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="batch_exports",
    )

    # Batch configuration
    batch_name = models.CharField(max_length=200, blank=True)
    export_settings = models.JSONField(default=dict)
    compress_output = models.BooleanField(
        default=True, help_text="Compress exports into a ZIP file"
    )

    # Status tracking
    status = models.CharField(
        max_length=20, choices=BatchStatus.choices, default=BatchStatus.QUEUED
    )
    total_cases = models.PositiveIntegerField(default=0)
    processed_cases = models.PositiveIntegerField(default=0)
    failed_cases = models.PositiveIntegerField(default=0)

    # Output file
    zip_file = models.FileField(
        upload_to="exports/batch/%Y/%m/%d/", null=True, blank=True
    )
    zip_file_size = models.PositiveIntegerField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    # Celery task tracking
    task_id = models.CharField(max_length=255, blank=True, help_text="Celery task ID")

    # Error handling
    error_message = models.TextField(blank=True)

    class Meta:
        db_table = "exports_batchexport"
        verbose_name = "Batch Export"
        verbose_name_plural = "Batch Exports"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["status", "-created_at"]),
        ]

    def __str__(self):
        return f"Batch Export #{self.id} - {self.total_cases} cases - {self.status}"  # type: ignore[attr-defined]

    def update_progress(self, processed=0, failed=0):
        """Update batch export progress"""
        self.processed_cases = processed
        self.failed_cases = failed
        self.save(update_fields=["processed_cases", "failed_cases"])

    @property
    def filename(self):
        return os.path.basename(self.zip_file.name) if self.zip_file else None

