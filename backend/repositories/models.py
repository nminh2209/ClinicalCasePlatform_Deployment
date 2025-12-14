from django.db import models
from django.conf import settings


class Repository(models.Model):
    """
    Case repository for organizing and storing cases
    """

    name = models.CharField(max_length=200)
    vietnamese_name = models.CharField(
        max_length=200, blank=True, help_text="Tên tiếng Việt"
    )
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_repositories",
    )
    department = models.ForeignKey(
        "cases.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="repositories",
        help_text="Khoa phòng sở hữu kho lưu trữ này",
    )
    is_public = models.BooleanField(
        default=False, help_text="Kho lưu trữ có hiển thị với tất cả người dùng"
    )
    access_level = models.CharField(
        max_length=20,
        choices=[
            ("public", "Công khai"),
            ("department", "Khoa phòng"),
            ("private", "Riêng tư"),
        ],
        default="private",
        help_text="Mức độ truy cập",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "repositories_repository"
        verbose_name = "Kho lưu trữ"
        verbose_name_plural = "Kho lưu trữ"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.get_access_level_display()})"  # type: ignore[attr-defined]

    @property
    def case_count(self):
        return self.cases.count()  # type: ignore[attr-defined]
