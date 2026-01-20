# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    Supports both students and instructors
    """

    class RoleChoices(models.TextChoices):
        STUDENT = "student", "Sinh viên"
        INSTRUCTOR = "instructor", "Giảng viên"
        ADMIN = "admin", "Quản trị viên"

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20, choices=RoleChoices.choices, default=RoleChoices.STUDENT
    )
    specialization = models.CharField(
        max_length=100, blank=True, help_text="Chuyên ngành (dành cho giảng viên)"
    )
    department = models.ForeignKey(
        "cases.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        help_text="Khoa phòng",
    )
    student_id = models.CharField(
        max_length=20, blank=True, help_text="Mã số sinh viên"
    )
    employee_id = models.CharField(
        max_length=20, blank=True, help_text="Mã số nhân viên"
    )
    academic_year = models.CharField(
        max_length=20, blank=True, help_text="Năm học (VD: 2024-2025)"
    )
    phone_number = models.CharField(
        max_length=20, blank=True, help_text="Số điện thoại"
    )
    profile_picture_url = models.URLField(blank=True, help_text="URL ảnh đại diện")
    bio = models.TextField(blank=True, help_text="Tiểu sử cá nhân")
    language_preference = models.CharField(
        max_length=10,
        choices=[
            ("vi", "Tiếng Việt"),
            ("en", "English"),
        ],
        default="vi",
        help_text="Ngôn ngữ ưa thích",
    )
    notification_settings = models.JSONField(
        default=dict,
        help_text="Cài đặt thông báo (email, in-app, etc.)",
    )
    email_verified = models.BooleanField(
        default=False, help_text="Email đã được xác minh"
    )
    password_changed_at = models.DateTimeField(
        null=True, blank=True, help_text="Lần cuối thay đổi mật khẩu"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Override username to use email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:  # type: ignore[misc]
        db_table = "accounts_user"
        verbose_name = "Người dùng"
        verbose_name_plural = "Người dùng"

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"  # type: ignore[attr-defined]

    @property
    def is_student(self):
        return self.role == self.RoleChoices.STUDENT.value

    @property
    def is_instructor(self):
        return self.role == self.RoleChoices.INSTRUCTOR.value

    @property
    def is_admin_user(self):
        return self.role == self.RoleChoices.ADMIN.value

    def get_department_name(self):
        return self.department.name if self.department else "Chưa phân khoa"


class Session(models.Model):
    """
    Custom session model for JWT token management
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")
    jwt_token_id = models.CharField(
        max_length=255,
        unique=True,
        help_text="Unique JWT token identifier",
        default="legacy-token",  # Default for existing records
    )
    refresh_token_hash = models.CharField(
        max_length=255,
        help_text="Hashed refresh token",
        default="",  # Default for existing records
    )
    session_token = models.CharField(
        max_length=255, unique=True
    )  # Keep for backward compatibility
    device_info = models.TextField(
        blank=True, help_text="Device and browser information"
    )
    ip_address = models.GenericIPAddressField(
        null=True, blank=True, help_text="IP address of the session"
    )
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # type: ignore[call-arg]

    class Meta:
        db_table = "accounts_session"
        verbose_name = "Session"
        verbose_name_plural = "Sessions"

    def __str__(self):
        user: User = self.user  # type: ignore[assignment]
        return f"Session for {user.email}"
