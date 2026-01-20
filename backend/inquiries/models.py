# inquiries/models.py

import os

from django.conf import settings
from django.db import models
from django.utils import timezone


def inquiry_file_upload_to(instance, filename):
    """
    Dynamic path for inquiry attachments: inquiries/case_{id}/inquiry_{id}/{filename}
    """
    inquiry_id = instance.inquiry.id if instance.inquiry else "unknown"
    # If attached to a response, we still group by the parent inquiry
    if instance.response:
        inquiry_id = instance.response.inquiry.id

    # Sanitize filename
    base, ext = os.path.splitext(filename)
    safe_base = base.replace(" ", "_").replace("/", "_")
    return f"inquiries/inquiry_{inquiry_id}/{safe_base}{ext}"


class Inquiry(models.Model):
    """
    Top-level inquiry (question) initiated by an instructor regarding a student's case.
    Acts as the root of a threaded discussion (1-level deep).
    """

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        RESOLVED = "resolved", "Resolved"
        CLOSED = "closed", "Closed"

    case = models.ForeignKey(
        "cases.Case",
        on_delete=models.CASCADE,
        related_name="inquiries",
        help_text="The case this inquiry discusses",
    )

    # Creator (Must be instructor)
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_inquiries",
        limit_choices_to={"role": "instructor"},
    )

    # Recipient (Derived from case owner, but stored for query efficiency)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_inquiries",
        limit_choices_to={"role": "student"},
    )

    title = models.CharField(max_length=255, help_text="Subject of the inquiry")
    content = models.TextField(help_text="Markdown supported content")

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
    )

    # Searchable tags (optional)
    topic = models.CharField(
        max_length=100,
        blank=True,
        help_text="Topic/Category (e.g., Diagnosis, Treatment, Documentation)",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "inquiries_inquiry"
        verbose_name = "Inquiry"
        verbose_name_plural = "Inquiries"
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["case"]),
            models.Index(fields=["status"]),
            models.Index(fields=["instructor"]),
            models.Index(fields=["student"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.case.title}"

    @property
    def response_count(self):
        return self.responses.count()  # type: ignore[attr-defined]

    def resolve(self, resolved_by):
        """Mark inquiry as resolved"""
        if self.status == self.Status.CLOSED:
            raise ValueError("Cannot resolve a closed inquiry")

        self.status = self.Status.RESOLVED
        self.save(update_fields=["status", "updated_at"])

    def close(self, closed_by):
        """Close inquiry (final state)"""
        if closed_by != self.instructor:
            raise PermissionError("Only the instructor can close inquiries")

        self.status = self.Status.CLOSED
        self.save(update_fields=["status", "updated_at"])


class InquiryResponse(models.Model):
    """
    Response to an inquiry. Can be from the student (answering) or the instructor (follow-up).
    """

    inquiry = models.ForeignKey(
        Inquiry,
        on_delete=models.CASCADE,
        related_name="responses",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="inquiry_responses",
    )
    content = models.TextField(help_text="Markdown supported content")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "inquiries_inquiryresponse"
        verbose_name = "Inquiry Response"
        verbose_name_plural = "Inquiry Responses"
        ordering = ["created_at"]

    def __str__(self):
        return f"Response by {self.author.get_full_name()} to {self.inquiry.title}"


class InquiryAttachment(models.Model):
    """
    Files attached to an inquiry or a response.
    """

    inquiry = models.ForeignKey(
        Inquiry,
        on_delete=models.CASCADE,
        related_name="attachments",
        null=True,
        blank=True,
        help_text="Attach to the main inquiry",
    )
    response = models.ForeignKey(
        InquiryResponse,
        on_delete=models.CASCADE,
        related_name="attachments",
        null=True,
        blank=True,
        help_text="Attach to a specific response",
    )

    file = models.FileField(upload_to=inquiry_file_upload_to)
    filename = models.CharField(max_length=255, blank=True)
    file_size = models.PositiveIntegerField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "inquiries_inquiryattachment"

    def clean(self):
        """Ensure attachment is linked to inquiry XOR response"""
        from django.core.exceptions import ValidationError

        if self.inquiry and self.response:
            raise ValidationError(
                "Attachment cannot belong to both inquiry and response"
            )
        if not self.inquiry and not self.response:
            raise ValidationError(
                "Attachment must belong to either an inquiry or a response"
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # Run validation
        if self.file:
            self.filename = self.file.name
            self.file_size = self.file.size
        super().save(*args, **kwargs)

    def __str__(self):
        return self.filename or f"Attachment {self.id}"  # type: ignore[attr-defined]
