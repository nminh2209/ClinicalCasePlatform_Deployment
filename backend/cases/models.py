from django.db import models
from django.conf import settings
from .medical_models import (
    # Department,
    ClinicalHistory,
    PhysicalExamination,
    Investigations,
    DiagnosisManagement,
    LearningOutcomes,
    StudentNotes,
)


class Case(models.Model):
    """
    Main Case model for storing patient case information
    Enhanced with detailed medical sections
    """

    class StatusChoices(models.TextChoices):
        DRAFT = "draft", "Bản nháp"
        SUBMITTED = "submitted", "Đã nộp"
        REVIEWED = "reviewed", "Đã xem xét"
        APPROVED = "approved", "Đã phê duyệt"

    # Basic case information
    title = models.CharField(max_length=300)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_cases",
        limit_choices_to={"role": "student"},
    )
    template = models.ForeignKey(
        "templates.CaseTemplate",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cases",
    )
    repository = models.ForeignKey(
        "repositories.Repository", on_delete=models.CASCADE, related_name="cases"
    )

    # Patient information
    patient_name = models.CharField(
        max_length=200, help_text="Tên bệnh nhân (có thể ẩn danh)"
    )
    patient_age = models.PositiveIntegerField(help_text="Tuổi")
    patient_gender = models.CharField(
        max_length=20,
        choices=[
            ("male", "Nam"),
            ("female", "Nữ"),
            ("other", "Khác"),
            ("not_specified", "Không xác định"),
        ],
        help_text="Giới tính",
    )
    medical_record_number = models.CharField(
        max_length=50, blank=True, help_text="Số hồ sơ bệnh án (ẩn danh)"
    )
    admission_date = models.DateField(null=True, blank=True, help_text="Ngày nhập viện")
    discharge_date = models.DateField(null=True, blank=True, help_text="Ngày xuất viện")

    # # Legacy fields (kept for backward compatibility)
    # history = models.TextField(
    #     blank=True,
    #     help_text="Tiền sử bệnh nhân (sử dụng clinical_history để chi tiết hơn)",
    # )
    # examination = models.TextField(
    #     blank=True,
    #     help_text="Khám lâm sàng (sử dụng physical_examination để chi tiết hơn)",
    # )
    # diagnosis = models.TextField(
    #     blank=True, help_text="Chẩn đoán (sử dụng diagnosis_management để chi tiết hơn)"
    # )
    # treatment = models.TextField(
    #     blank=True, help_text="Điều trị (sử dụng diagnosis_management để chi tiết hơn)"
    # )
    # investigations = models.TextField(
    #     blank=True,
    #     help_text="Xét nghiệm (sử dụng investigations_detail để chi tiết hơn)",
    # )
    # follow_up = models.TextField(blank=True, help_text="Theo dõi")
    # learning_objectives = models.TextField(
    #     blank=True,
    #     help_text="Mục tiêu học tập (sử dụng learning_outcomes để chi tiết hơn)",
    # )

    # Case metadata
    case_status = models.CharField(
        max_length=20, choices=StatusChoices.choices, default=StatusChoices.DRAFT
    )
    specialty = models.CharField(
        max_length=100, help_text="Chuyên khoa liên quan đến ca bệnh này"
    )
    priority_level = models.CharField(
        max_length=20,
        choices=[
            ("low", "Thấp"),
            ("medium", "Trung bình"),
            ("high", "Cao"),
            ("urgent", "Khẩn cấp"),
        ],
        default="medium",
        help_text="Mức độ ưu tiên",
    )
    complexity_level = models.CharField(
        max_length=20,
        choices=[
            ("basic", "Cơ bản"),
            ("intermediate", "Trung cấp"),
            ("advanced", "Nâng cao"),
            ("expert", "Chuyên gia"),
        ],
        default="basic",
        help_text="Mức độ phức tạp",
    )
    case_summary = models.TextField(blank=True, help_text="Tóm tắt ca bệnh")
    learning_tags = models.CharField(
        max_length=500,
        blank=True,
        help_text="Tags học tập, phân cách bằng dấu phẩy",
    )
    estimated_study_hours = models.PositiveIntegerField(
        null=True, blank=True, help_text="Số giờ học ước tính"
    )
    patient_ethnicity = models.CharField(
        max_length=50, blank=True, help_text="Dân tộc bệnh nhân"
    )
    patient_occupation = models.CharField(
        max_length=100, blank=True, help_text="Nghề nghiệp bệnh nhân"
    )
    chief_complaint_brief = models.CharField(
        max_length=200, blank=True, help_text="Lý do khám ngắn gọn"
    )
    requires_follow_up = models.BooleanField(
        default=False, help_text="Yêu cầu theo dõi"
    )
    follow_up_date = models.DateField(null=True, blank=True, help_text="Ngày theo dõi")
    is_public = models.BooleanField(default=False, help_text="Ca bệnh công khai")
    is_template_based = models.BooleanField(
        default=False, help_text="Dựa trên template"
    )
    is_archived = models.BooleanField(default=False, help_text="Đã lưu trữ")
    view_count = models.PositiveIntegerField(default=0, help_text="Số lượt xem")
    average_rating = models.FloatField(
        null=True, blank=True, help_text="Đánh giá trung bình"
    )
    keywords = models.CharField(
        max_length=500,
        blank=True,
        help_text="Từ khóa tìm kiếm, phân cách bằng dấu phẩy",
    )

    # Social Media Feed Fields
    is_published_to_feed = models.BooleanField(
        default=False, help_text="Ca bệnh đã được xuất bản lên feed công khai"
    )
    published_to_feed_at = models.DateTimeField(
        null=True, blank=True, help_text="Thời điểm xuất bản lên feed"
    )
    published_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="published_feed_cases",
        help_text="Giảng viên xuất bản ca bệnh lên feed",
    )
    feed_visibility = models.CharField(
        max_length=20,
        choices=[
            ("department", "Cùng khoa"),
            ("university", "Toàn trường"),
        ],
        default="department",
        help_text="Phạm vi hiển thị trên feed công khai",
    )
    is_featured = models.BooleanField(
        default=False, help_text="Ca bệnh nổi bật (được chọn bởi giảng viên)"
    )
    reaction_count = models.PositiveIntegerField(
        default=0, help_text="Tổng số reactions (likes, loves, etc.)"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_cases",
        help_text="Người xem xét ca bệnh",
    )
    archived_at = models.DateTimeField(null=True, blank=True)
    archived_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="archived_cases",
        help_text="Người lưu trữ ca bệnh",
    )

    class Meta:
        db_table = "cases_case"
        verbose_name = "Hồ sơ bệnh án"
        verbose_name_plural = "Hồ sơ bệnh án"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["specialty"]),
            models.Index(fields=["case_status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.student.get_full_name()}"

    def get_comment_count(self):
        return self.comments.count()  # type: ignore[attr-defined]

    @property
    def has_grade(self):
        return hasattr(self, "grade")

    @property
    def has_detailed_sections(self):
        """Check if case has detailed medical sections"""
        return (
            hasattr(self, "clinical_history")
            or hasattr(self, "physical_examination")
            or hasattr(self, "investigations_detail")
            or hasattr(self, "diagnosis_management")
            or hasattr(self, "learning_outcomes")
        )

    def create_detailed_sections(self):
        """Create empty detailed sections for this case"""
        if not hasattr(self, "clinical_history"):
            ClinicalHistory.objects.create(
                case=self, chief_complaint="", history_present_illness=""
            )
        if not hasattr(self, "physical_examination"):
            PhysicalExamination.objects.create(
                case=self, general_appearance="", vital_signs=""
            )
        if not hasattr(self, "investigations_detail"):
            Investigations.objects.create(case=self)
        if not hasattr(self, "diagnosis_management"):
            DiagnosisManagement.objects.create(
                case=self, primary_diagnosis="", treatment_plan=""
            )
        if not hasattr(self, "learning_outcomes"):
            LearningOutcomes.objects.create(case=self, learning_objectives="")

    def get_reaction_summary(self):
        """Get summary of reactions for this case"""
        from comments.models import Comment
        from django.db.models import Count

        reactions = (
            Comment.objects.filter(case=self, is_reaction=True)
            .values("reaction_type")
            .annotate(count=Count("id"))
        )

        summary = {
            "total": self.reaction_count,
            "breakdown": {r["reaction_type"]: r["count"] for r in reactions},
        }
        return summary

    def can_be_published(self):
        """Check if case can be published to public feed"""
        return (
            self.case_status == self.StatusChoices.APPROVED
            and not self.is_published_to_feed
        )


class CasePermission(models.Model):
    """
    Enhanced permissions for case sharing and collaboration
    Supports time-limited access, department/class sharing, and detailed permissions
    """

    class PermissionChoices(models.TextChoices):
        VIEW = "view", "Chỉ xem"
        COMMENT = "comment", "Xem và bình luận"
        ANALYZE = "analyze", "Xem, bình luận và phân tích"
        EDIT = "edit", "Toàn quyền chỉnh sửa"

    class ShareTypeChoices(models.TextChoices):
        INDIVIDUAL = "individual", "Cá nhân"
        DEPARTMENT = "department", "Khoa phòng"
        CLASS_GROUP = "class_group", "Lớp học"
        PUBLIC = "public", "Công khai"

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="permissions")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="case_permissions",
        null=True,
        blank=True,
    )

    # Group sharing fields
    share_type = models.CharField(
        max_length=20,
        choices=ShareTypeChoices.choices,
        default=ShareTypeChoices.INDIVIDUAL,
        help_text="Loại chia sẻ",
    )
    target_department = models.ForeignKey(
        "cases.Department",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="shared_cases",
        help_text="Khoa được chia sẻ",
    )
    class_group = models.CharField(
        max_length=100, blank=True, help_text="Nhóm lớp học (VD: K15, Y6, etc.)"
    )

    # Permission details
    permission_type = models.CharField(
        max_length=20, choices=PermissionChoices.choices, default=PermissionChoices.VIEW
    )
    granted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="granted_permissions",
    )

    # Time-limited access
    granted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Thời gian hết hạn (để trống nếu không giới hạn)",
    )

    # Status and metadata
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, help_text="Ghi chú về quyền truy cập này")
    access_count = models.PositiveIntegerField(default=0, help_text="Số lần truy cập")
    last_accessed = models.DateTimeField(
        null=True, blank=True, help_text="Lần cuối truy cập"
    )

    class Meta:
        db_table = "cases_casepermission"
        verbose_name = "Quyền truy cập ca bệnh"
        verbose_name_plural = "Quyền truy cập ca bệnh"
        indexes = [
            models.Index(fields=["case", "user"]),
            models.Index(fields=["case", "share_type"]),
            models.Index(fields=["target_department"]),
            models.Index(fields=["expires_at"]),
        ]

    def __str__(self):
        if self.user:
            return f"{self.user.get_full_name()} - {self.get_permission_type_display()} on {self.case.title}"  # type: ignore[attr-defined]

        return f"{self.get_share_type_display()} - {self.get_permission_type_display()} on {self.case.title}"  # type: ignore[attr-defined]

    @property
    def is_expired(self):
        """Check if permission has expired"""
        if not self.expires_at:
            return False
        from django.utils import timezone

        return timezone.now() > self.expires_at

    def update_access(self):
        """Update access count and last accessed time"""
        from django.utils import timezone

        self.access_count += 1
        self.last_accessed = timezone.now()
        self.save(update_fields=["access_count", "last_accessed"])


class GuestAccess(models.Model):
    """
    Temporary access system for external reviewers and guests
    """

    case = models.ForeignKey(
        Case, on_delete=models.CASCADE, related_name="guest_accesses"
    )
    access_token = models.CharField(
        max_length=255, unique=True, help_text="Token truy cập duy nhất cho khách"
    )
    guest_email = models.EmailField(help_text="Email người được mời")
    guest_name = models.CharField(
        max_length=200, blank=True, help_text="Tên người được mời"
    )
    permission_type = models.CharField(
        max_length=20,
        choices=CasePermission.PermissionChoices.choices,
        default=CasePermission.PermissionChoices.VIEW,
    )

    # Access control
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_guest_accesses",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(help_text="Thời gian hết hạn (bắt buộc)")

    # Usage tracking
    is_active = models.BooleanField(default=True)
    access_count = models.PositiveIntegerField(default=0)
    last_accessed = models.DateTimeField(null=True, blank=True)
    accessed_ips = models.JSONField(default=list, help_text="Danh sách IP đã truy cập")

    class Meta:
        db_table = "cases_guestaccess"
        verbose_name = "Truy cập khách"
        verbose_name_plural = "Truy cập khách"
        indexes = [
            models.Index(fields=["access_token"]),
            models.Index(fields=["case"]),
            models.Index(fields=["expires_at"]),
        ]

    def __str__(self):
        return f"Guest access for {self.guest_email} on {self.case.title}"

    @property
    def is_expired(self):
        """Check if guest access has expired"""
        from django.utils import timezone

        return timezone.now() > self.expires_at

    def update_access(self, ip_address=None):
        """Update access count and tracking info"""
        from django.utils import timezone

        self.access_count += 1
        self.last_accessed = timezone.now()

        if ip_address and ip_address not in self.accessed_ips:
            self.accessed_ips.append(ip_address)

        self.save(update_fields=["access_count", "last_accessed", "accessed_ips"])


class CaseGroup(models.Model):
    """
    Case collections for bulk permission management
    Enables department/class-based case sharing
    """

    class GroupTypeChoices(models.TextChoices):
        DEPARTMENT = "department", "Bộ sưu tập khoa"
        CLASS = "class", "Bộ sưu tập lớp"
        ASSIGNMENT = "assignment", "Bài tập"
        CURRICULUM = "curriculum", "Chương trình học"

    name = models.CharField(max_length=200, help_text="Tên nhóm ca bệnh")
    description = models.TextField(blank=True, help_text="Mô tả")
    group_type = models.CharField(
        max_length=20,
        choices=GroupTypeChoices.choices,
        default=GroupTypeChoices.ASSIGNMENT,
    )

    # Ownership and organization
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_case_groups",
    )
    department = models.ForeignKey(
        "cases.Department",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="case_groups",
    )
    class_identifier = models.CharField(
        max_length=100, blank=True, help_text="Mã lớp (VD: K15Y1, Y6-ICU, etc.)"
    )

    # Cases and members
    cases = models.ManyToManyField(
        Case, related_name="case_groups", blank=True, help_text="Ca bệnh trong nhóm"
    )

    # Access control
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(
        default=False, help_text="Nhóm công khai (tất cả có thể xem)"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cases_casegroup"
        verbose_name = "Nhóm ca bệnh"
        verbose_name_plural = "Nhóm ca bệnh"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["department", "group_type"]),
            models.Index(fields=["class_identifier"]),
            models.Index(fields=["created_by"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_group_type_display()})"  # type: ignore[attr-defined]

    def add_bulk_permissions(self, users, permission_type="view"):
        """Add permissions for all cases to multiple users"""
        permissions_to_create = []

        for case in self.cases.all():
            for user in users:
                # Check if permission doesn't exist
                if not CasePermission.objects.filter(case=case, user=user).exists():
                    permissions_to_create.append(
                        CasePermission(
                            case=case,
                            user=user,
                            permission_type=permission_type,
                            granted_by=self.created_by,
                            share_type=CasePermission.ShareTypeChoices.CLASS_GROUP,
                            class_group=self.class_identifier,
                        )
                    )

        CasePermission.objects.bulk_create(permissions_to_create, ignore_conflicts=True)
        return len(permissions_to_create)


class PermissionAuditLog(models.Model):
    """
    Audit log for permission changes and access tracking
    Security and compliance tracking
    """

    class ActionChoices(models.TextChoices):
        GRANTED = "granted", "Cấp quyền"
        REVOKED = "revoked", "Thu hồi quyền"
        MODIFIED = "modified", "Thay đổi quyền"
        ACCESSED = "accessed", "Truy cập"
        EXPIRED = "expired", "Hết hạn"

    # Core audit info
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="permission_audit_logs",
        help_text="Ca bệnh liên quan",
    )
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="permission_audit_logs",
        help_text="Người dùng được ảnh hưởng",
    )
    actor_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="performed_audit_logs",
        help_text="Người thực hiện hành động",
    )

    # Action details
    action = models.CharField(
        max_length=20,
        choices=ActionChoices.choices,
        help_text="Hành động được thực hiện",
    )
    permission_type = models.CharField(
        max_length=20,
        choices=CasePermission.PermissionChoices.choices,
        blank=True,
        help_text="Loại quyền",
    )

    # Context and metadata
    description = models.TextField(blank=True, help_text="Mô tả chi tiết hành động")
    ip_address = models.GenericIPAddressField(
        null=True, blank=True, help_text="Địa chỉ IP"
    )
    user_agent = models.TextField(
        blank=True, help_text="Thông tin trình duyệt/thiết bị"
    )
    additional_data = models.JSONField(default=dict, help_text="Dữ liệu bổ sung")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cases_permissionauditlog"
        verbose_name = "Nhật ký kiểm toán quyền"
        verbose_name_plural = "Nhật ký kiểm toán quyền"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["case", "action"]),
            models.Index(fields=["target_user"]),
            models.Index(fields=["actor_user"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        target_info = self.target_user.get_full_name() if self.target_user else "System"
        actor_info = self.actor_user.get_full_name() if self.actor_user else "System"
        return f"{self.get_action_display()}: {target_info} by {actor_info} on {self.case.title}"  # type: ignore[attr-defined]

    @classmethod
    def log_permission_change(
        cls,
        case,
        target_user,
        actor_user,
        action,
        permission_type="",
        description="",
        request=None,
        additional_data=None,
    ):
        """Convenience method to log permission changes"""
        ip_address = None
        user_agent = ""

        if request:
            ip_address = request.META.get(
                "HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR")
            )
            user_agent = request.META.get("HTTP_USER_AGENT", "")

        cls.objects.create(
            case=case,
            target_user=target_user,
            actor_user=actor_user,
            action=action,
            permission_type=permission_type,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent,
            additional_data=additional_data or {},
        )
