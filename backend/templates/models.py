from django.db import models
from django.conf import settings


class CaseTemplate(models.Model):
    """
    Standardized case templates for different medical specialties
    """

    name = models.CharField(max_length=200)
    vietnamese_name = models.CharField(
        max_length=200, blank=True, help_text="Tên tiếng Việt"
    )
    description = models.TextField()
    fields_schema = models.JSONField(
        help_text="JSON schema defining the template structure and required fields"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_templates",
    )
    department = models.ForeignKey(
        "cases.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="templates",
        help_text="Khoa phòng sở hữu template này",
    )
    is_standard = models.BooleanField(
        default=False, help_text="Template chuẩn do hệ thống cung cấp"
    )
    specialty = models.CharField(
        max_length=100, help_text="Chuyên khoa mà template này được thiết kế"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "templates_casetemplate"
        verbose_name = "Mẫu hồ sơ bệnh án"
        verbose_name_plural = "Mẫu hồ sơ bệnh án"
        ordering = ["specialty", "name"]

    def __str__(self):
        return f"{self.name} ({self.specialty})"
