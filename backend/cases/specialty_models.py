# cases/specialty_models.py
"""
Database models for managing specialties dynamically
Allows admins to add/edit/delete specialties via Django admin
"""

from django.db import models


class Specialty(models.Model):
    """
    Medical specialty that can be managed via admin panel
    Replaces hardcoded specialty values in frontend
    NOW LINKED TO DEPARTMENTS for proper hierarchy
    """

    name = models.CharField(
        max_length=100,
        verbose_name="Tên chuyên khoa",
        help_text="Tên chuyên khoa bằng tiếng Việt (ví dụ: Tim mạch, Gan bướu, Hô hấp)",
    )

    english_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="English name",
        help_text="Optional English translation (e.g., Cardiology, Hepatology, Pulmonology)",
    )

    department = models.ForeignKey(
        "Department",
        on_delete=models.CASCADE,
        related_name="specialties",
        verbose_name="Khoa phòng",
        help_text="Khoa phòng chứa chuyên khoa này (ví dụ: Tim mạch thuộc Khoa Nội)",
        null=True,  # Temporary nullable for migration
        blank=True,
    )

    description = models.TextField(
        blank=True,
        verbose_name="Mô tả",
        help_text="Mô tả chi tiết về chuyên khoa này",
    )

    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Icon",
        help_text="Tên icon để hiển thị trong giao diện (ví dụ: heart, lungs, liver)",
    )

    color = models.CharField(
        max_length=20,
        default="blue",
        verbose_name="Màu sắc",
        help_text="Màu để hiển thị trong giao diện (red, blue, green, purple, orange)",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Đang hoạt động",
        help_text="Bỏ chọn để ẩn chuyên khoa này khỏi dropdown (không xóa dữ liệu cũ)",
    )

    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Thứ tự hiển thị",
        help_text="Chuyên khoa có số thứ tự nhỏ hơn sẽ hiển thị trước",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        db_table = "specialties"
        verbose_name = "Chuyên khoa"
        verbose_name_plural = "Chuyên khoa"
        ordering = ["department", "display_order", "name"]
        unique_together = [
            ["name", "department"]
        ]  # Same name OK in different departments

    def __str__(self):
        return (
            f"{self.name} ({self.department.vietnamese_name or self.department.name})"
        )


class CasePriorityLevel(models.Model):
    """
    Priority levels that can be managed via admin panel
    Examples: Thấp, Trung bình, Cao, Khẩn cấp
    """

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Tên mức độ ưu tiên",
    )

    key = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Khóa",
        help_text="Khóa duy nhất để sử dụng trong code (ví dụ: low, medium, high, urgent)",
    )

    color = models.CharField(
        max_length=20,
        default="gray",
        verbose_name="Màu hiển thị",
        help_text="Màu để hiển thị trong giao diện (red, yellow, green, gray, blue)",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Đang hoạt động",
    )

    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Thứ tự hiển thị",
    )

    class Meta:
        db_table = "case_priority_levels"
        verbose_name = "Mức độ ưu tiên"
        verbose_name_plural = "Mức độ ưu tiên"
        ordering = ["display_order"]

    def __str__(self):
        return self.name


class CaseComplexityLevel(models.Model):
    """
    Complexity levels that can be managed via admin panel
    Examples: Dễ, Trung bình, Khó, Rất khó
    """

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Tên mức độ phức tạp",
    )

    key = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Khóa",
        help_text="Khóa duy nhất để sử dụng trong code (ví dụ: easy, medium, hard, very_hard)",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Mô tả",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Đang hoạt động",
    )

    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Thứ tự hiển thị",
    )

    class Meta:
        db_table = "case_complexity_levels"
        verbose_name = "Mức độ phức tạp"
        verbose_name_plural = "Mức độ phức tạp"
        ordering = ["display_order"]

    def __str__(self):
        return self.name
