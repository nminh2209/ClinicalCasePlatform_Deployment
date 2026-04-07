from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_initial"),
        ("cases", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RoleModificationRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "full_name",
                    models.CharField(
                        help_text="Full legal name of requester", max_length=200
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="Email address for verification",
                        max_length=254,
                    ),
                ),
                (
                    "student_id",
                    models.CharField(
                        help_text="Student ID for verification", max_length=50
                    ),
                ),
                (
                    "requested_role",
                    models.CharField(
                        choices=[("instructor", "Giảng viên")],
                        default="instructor",
                        help_text="The role being requested (always instructor)",
                        max_length=20,
                    ),
                ),
                (
                    "specialty",
                    models.CharField(
                        help_text="Medical specialty or field", max_length=200
                    ),
                ),
                (
                    "reason",
                    models.TextField(
                        help_text="Justification for requesting the role change"
                    ),
                ),
                (
                    "employee_id",
                    models.CharField(
                        blank=True,
                        help_text="Staff/employee ID if already appointed",
                        max_length=50,
                    ),
                ),
                (
                    "institution",
                    models.CharField(
                        blank=True,
                        help_text="Hospital or institution affiliation",
                        max_length=200,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Đang chờ xét duyệt"),
                            ("approved", "Đã chấp thuận"),
                            ("rejected", "Đã từ chối"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                (
                    "rejection_reason",
                    models.TextField(
                        blank=True,
                        help_text="Admin's reason for rejection (required when rejecting)",
                    ),
                ),
                ("reviewed_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "department",
                    models.ForeignKey(
                        help_text="Department/faculty of the requester",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="role_requests",
                        to="cases.department",
                    ),
                ),
                (
                    "requester",
                    models.ForeignKey(
                        help_text="User submitting the request",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="role_requests",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "reviewed_by",
                    models.ForeignKey(
                        blank=True,
                        help_text="Admin who reviewed this request",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="reviewed_role_requests",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Yêu cầu thay đổi vai trò",
                "verbose_name_plural": "Yêu cầu thay đổi vai trò",
                "db_table": "accounts_role_modification_request",
                "ordering": ["-created_at"],
            },
        ),
    ]
