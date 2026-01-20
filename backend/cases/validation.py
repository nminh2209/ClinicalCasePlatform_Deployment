"""
Case Validation and Submission System
Comprehensive validation ensuring clinical cases meet educational standards
"""

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q
import re


class CaseValidationRule(models.Model):
    """
    Configurable validation rules for cases
    Allows administrators to define and manage validation criteria
    """

    class RuleType(models.TextChoices):
        REQUIRED_FIELD = "required_field", "Trường bắt buộc"
        MIN_LENGTH = "min_length", "Độ dài tối thiểu"
        MAX_LENGTH = "max_length", "Độ dài tối đa"
        PATTERN_MATCH = "pattern_match", "Khớp mẫu"
        ATTACHMENT_REQUIRED = "attachment_required", "Yêu cầu tệp đính kèm"
        TERMINOLOGY_CHECK = "terminology_check", "Kiểm tra thuật ngữ"
        LEARNING_OBJECTIVE = "learning_objective", "Mục tiêu học tập"

    class Severity(models.TextChoices):
        ERROR = "error", "Lỗi (chặn nộp)"
        WARNING = "warning", "Cảnh báo"
        INFO = "info", "Thông tin"

    name = models.CharField(max_length=200, help_text="Tên quy tắc")
    rule_type = models.CharField(
        max_length=50, choices=RuleType.choices, help_text="Loại quy tắc"
    )
    severity = models.CharField(
        max_length=20,
        choices=Severity.choices,
        default=Severity.ERROR,
        help_text="Mức độ nghiêm trọng",
    )

    # Rule Configuration
    target_field = models.CharField(
        max_length=100,
        help_text="Trường áp dụng (VD: title, diagnosis, clinical_history.chief_complaint)",
    )
    rule_config = models.JSONField(
        default=dict, help_text="Cấu hình quy tắc (min_length, pattern, etc.)"
    )

    # Applicability
    applies_to_specialties = models.JSONField(
        default=list, help_text="Áp dụng cho các chuyên khoa cụ thể"
    )

    # Status
    is_active = models.BooleanField(default=True, help_text="Quy tắc đang hoạt động")
    error_message_vi = models.TextField(help_text="Thông báo lỗi (tiếng Việt)")
    error_message_en = models.TextField(
        blank=True, help_text="Thông báo lỗi (tiếng Anh)"
    )
    help_text = models.TextField(blank=True, help_text="Hướng dẫn khắc phục")

    # Metadata
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_validation_rules",
        help_text="Người tạo quy tắc",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cases_casevalidationrule"
        verbose_name = "Case Validation Rule"
        verbose_name_plural = "Case Validation Rules"
        ordering = ["severity", "name"]

    def __str__(self):
        return f"{self.name} ({self.get_severity_display()})"  # type: ignore[attr-defined]

    def validate_case(self, case):
        """
        Validate a case against this rule
        Returns (is_valid, error_message)
        """

        if (
            self.applies_to_specialties
            and case.specialty not in self.applies_to_specialties
        ):
            return True, None

        # Get field value
        field_value = self._get_field_value(case, self.target_field)

        # Apply validation based on rule type
        if self.rule_type == self.RuleType.REQUIRED_FIELD:
            if not field_value or (
                isinstance(field_value, str) and not field_value.strip()
            ):
                return False, self.error_message_vi

        elif self.rule_type == self.RuleType.MIN_LENGTH:
            min_length = self.rule_config.get("min_length", 0)
            if isinstance(field_value, str) and len(field_value.strip()) < min_length:
                return False, self.error_message_vi.format(min_length=min_length)

        elif self.rule_type == self.RuleType.MAX_LENGTH:
            max_length = self.rule_config.get("max_length", 10000)
            if isinstance(field_value, str) and len(field_value) > max_length:
                return False, self.error_message_vi.format(max_length=max_length)

        elif self.rule_type == self.RuleType.PATTERN_MATCH:
            pattern = self.rule_config.get("pattern", "")
            if isinstance(field_value, str) and pattern:
                if not re.search(pattern, field_value):
                    return False, self.error_message_vi

        elif self.rule_type == self.RuleType.ATTACHMENT_REQUIRED:
            required_types = self.rule_config.get("attachment_types", [])
            attachments = case.medical_attachments.all()

            if required_types:
                for req_type in required_types:
                    if not attachments.filter(attachment_type=req_type).exists():
                        return False, self.error_message_vi.format(type=req_type)
            elif not attachments.exists():
                return False, self.error_message_vi

        elif self.rule_type == self.RuleType.LEARNING_OBJECTIVE:
            if not hasattr(case, "learning_outcomes"):
                return False, self.error_message_vi

            learning_outcomes = case.learning_outcomes
            if (
                not learning_outcomes.learning_objectives
                or not learning_outcomes.learning_objectives.strip()
            ):
                return False, self.error_message_vi

        return True, None

    def _get_field_value(self, case, field_path):
        """Get nested field value using dot notation"""
        parts = field_path.split(".")
        value = case

        for part in parts:
            if hasattr(value, part):
                value = getattr(value, part)
            else:
                return None

        return value


class CaseValidationResult(models.Model):
    """
    Results of case validation
    Stores validation history and issues found
    """

    class ValidationStatus(models.TextChoices):
        PASSED = "passed", "Đạt"
        FAILED = "failed", "Không đạt"
        WARNING = "warning", "Cảnh báo"
        PENDING = "pending", "Đang chờ"

    case = models.ForeignKey(
        "cases.Case",
        on_delete=models.CASCADE,
        related_name="validation_results",
        help_text="Ca bệnh được kiểm tra",
    )
    validation_status = models.CharField(
        max_length=20,
        choices=ValidationStatus.choices,
        default=ValidationStatus.PENDING,
        help_text="Trạng thái kiểm tra",
    )

    # Validation Details
    total_rules_checked = models.PositiveIntegerField(
        default=0, help_text="Tổng số quy tắc kiểm tra"
    )
    rules_passed = models.PositiveIntegerField(default=0, help_text="Số quy tắc đạt")
    rules_failed = models.PositiveIntegerField(
        default=0, help_text="Số quy tắc không đạt"
    )
    warnings_count = models.PositiveIntegerField(default=0, help_text="Số cảnh báo")

    # Issues Found
    validation_issues = models.JSONField(
        default=list, help_text="Danh sách vấn đề tìm thấy"
    )

    # Scores
    completeness_score = models.FloatField(
        default=0.0, help_text="Điểm độ hoàn thiện (0-100)"
    )
    quality_score = models.FloatField(default=0.0, help_text="Điểm chất lượng (0-100)")
    overall_score = models.FloatField(default=0.0, help_text="Điểm tổng thể (0-100)")

    # Metadata
    validated_at = models.DateTimeField(
        auto_now_add=True, help_text="Thời gian kiểm tra"
    )
    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="performed_validations",
        help_text="Người thực hiện kiểm tra (null = tự động)",
    )
    validation_type = models.CharField(
        max_length=50,
        choices=[
            ("automatic", "Tự động"),
            ("manual", "Thủ công"),
            ("pre_submission", "Trước khi nộp"),
            ("review", "Xem xét"),
        ],
        default="automatic",
        help_text="Loại kiểm tra",
    )

    class Meta:
        db_table = "cases_casevalidationresult"
        verbose_name = "Case Validation Result"
        verbose_name_plural = "Case Validation Results"
        ordering = ["-validated_at"]
        indexes = [
            models.Index(fields=["case", "validation_status"]),
            models.Index(fields=["validated_at"]),
        ]

    def __str__(self):
        return f"Validation for {self.case.title} - {self.get_validation_status_display()}"  # type: ignore[attr-defined]


class CaseSubmissionWorkflow(models.Model):
    """
    Workflow tracking for case submission and review process
    Manages the approval pipeline
    """

    class WorkflowStatus(models.TextChoices):
        DRAFT = "draft", "Bản nháp"
        VALIDATION_PENDING = "validation_pending", "Đang kiểm tra"
        VALIDATION_FAILED = "validation_failed", "Kiểm tra không đạt"
        SUBMITTED = "submitted", "Đã nộp"
        UNDER_REVIEW = "under_review", "Đang xem xét"
        REVISION_REQUESTED = "revision_requested", "Yêu cầu sửa"
        APPROVED = "approved", "Đã phê duyệt"
        REJECTED = "rejected", "Từ chối"
        PUBLISHED = "published", "Đã xuất bản"

    case = models.OneToOneField(
        "cases.Case",
        on_delete=models.CASCADE,
        related_name="submission_workflow",
        help_text="Ca bệnh",
    )
    current_status = models.CharField(
        max_length=50,
        choices=WorkflowStatus.choices,
        default=WorkflowStatus.DRAFT,
        help_text="Trạng thái hiện tại",
    )

    # Submission Details
    submitted_at = models.DateTimeField(
        null=True, blank=True, help_text="Thời gian nộp"
    )
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="submitted_cases",
        help_text="Người nộp",
    )

    # Review Details
    assigned_reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_case_reviews",
        limit_choices_to={"role__in": ["instructor", "admin"]},
        help_text="Người xem xét được chỉ định",
    )
    review_started_at = models.DateTimeField(
        null=True, blank=True, help_text="Thời gian bắt đầu xem xét"
    )
    review_completed_at = models.DateTimeField(
        null=True, blank=True, help_text="Thời gian hoàn thành xem xét"
    )

    # Approval Details
    approved_at = models.DateTimeField(
        null=True, blank=True, help_text="Thời gian phê duyệt"
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_cases",
        help_text="Người phê duyệt",
    )

    # Revision Details
    revision_count = models.PositiveIntegerField(
        default=0, help_text="Số lần yêu cầu sửa"
    )
    revision_notes = models.TextField(blank=True, help_text="Ghi chú yêu cầu sửa")
    last_revision_requested_at = models.DateTimeField(
        null=True, blank=True, help_text="Lần cuối yêu cầu sửa"
    )

    # Rejection Details
    rejected_at = models.DateTimeField(
        null=True, blank=True, help_text="Thời gian từ chối"
    )
    rejection_reason = models.TextField(blank=True, help_text="Lý do từ chối")

    # Workflow Metadata
    workflow_history = models.JSONField(
        default=list, help_text="Lịch sử thay đổi trạng thái"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cases_casesubmissionworkflow"
        verbose_name = "Case Submission Workflow"
        verbose_name_plural = "Case Submission Workflows"
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["current_status"]),
            models.Index(fields=["assigned_reviewer"]),
            models.Index(fields=["submitted_at"]),
        ]

    def __str__(self):
        return f"Workflow for {self.case.title} - {self.get_current_status_display()}"  # type: ignore[attr-defined]

    def transition_to(self, new_status, user=None, notes=""):
        """
        Transition workflow to a new status
        Records the change in history
        """
        old_status = self.current_status
        self.current_status = new_status

        # Update relevant timestamps
        now = timezone.now()

        if new_status == self.WorkflowStatus.SUBMITTED:
            self.submitted_at = now
            self.submitted_by = user
        elif new_status == self.WorkflowStatus.UNDER_REVIEW:
            self.review_started_at = now
        elif new_status == self.WorkflowStatus.APPROVED:
            self.approved_at = now
            self.approved_by = user
            self.review_completed_at = now
        elif new_status == self.WorkflowStatus.REVISION_REQUESTED:
            self.revision_count += 1
            self.last_revision_requested_at = now
            self.revision_notes = notes
        elif new_status == self.WorkflowStatus.REJECTED:
            self.rejected_at = now
            self.rejection_reason = notes
            self.review_completed_at = now

        # Record in history
        history_entry = {
            "from_status": old_status,
            "to_status": new_status,
            "changed_at": now.isoformat(),
            "changed_by": user.get_full_name() if user else "System",
            "notes": notes,
        }

        if not isinstance(self.workflow_history, list):
            self.workflow_history = []

        self.workflow_history.append(history_entry)
        self.save()

    def can_submit(self):
        """Check if case can be submitted"""
        return self.current_status in [
            self.WorkflowStatus.DRAFT,
            self.WorkflowStatus.VALIDATION_FAILED,
            self.WorkflowStatus.REVISION_REQUESTED,
        ]

    def can_approve(self):
        """Check if case can be approved"""
        return self.current_status in [
            self.WorkflowStatus.SUBMITTED,
            self.WorkflowStatus.UNDER_REVIEW,
        ]


class MedicalTerminologyCheck(models.Model):
    """
    Medical terminology validation
    Maintains a dictionary of approved medical terms
    """

    term = models.CharField(max_length=200, unique=True, help_text="Thuật ngữ y khoa")
    vietnamese_term = models.CharField(max_length=200, help_text="Thuật ngữ tiếng Việt")
    category = models.CharField(
        max_length=100, help_text="Danh mục (VD: Anatomy, Disease, Procedure)"
    )
    definition = models.TextField(blank=True, help_text="Định nghĩa")
    synonyms = models.JSONField(default=list, help_text="Từ đồng nghĩa")

    # Validation
    is_approved = models.BooleanField(
        default=True, help_text="Thuật ngữ được phê duyệt"
    )
    requires_context = models.BooleanField(
        default=False, help_text="Yêu cầu ngữ cảnh cụ thể"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cases_medicalterminologycheck"
        verbose_name = "Medical Terminology"
        verbose_name_plural = "Medical Terminologies"
        ordering = ["term"]
        indexes = [
            models.Index(fields=["term"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return f"{self.term} ({self.vietnamese_term})"


class CaseQualityMetrics(models.Model):
    """
    Quality assessment metrics for cases
    Tracks various quality indicators
    """

    case = models.OneToOneField(
        "cases.Case",
        on_delete=models.CASCADE,
        related_name="quality_metrics",
        help_text="Ca bệnh",
    )

    # Completeness Metrics (0-100)
    clinical_history_completeness = models.FloatField(
        default=0.0, help_text="Độ hoàn thiện tiền sử lâm sàng"
    )
    examination_completeness = models.FloatField(
        default=0.0, help_text="Độ hoàn thiện khám lâm sàng"
    )
    investigation_completeness = models.FloatField(
        default=0.0, help_text="Độ hoàn thiện xét nghiệm"
    )
    diagnosis_completeness = models.FloatField(
        default=0.0, help_text="Độ hoàn thiện chẩn đoán"
    )
    learning_objectives_completeness = models.FloatField(
        default=0.0, help_text="Độ hoàn thiện mục tiêu học tập"
    )

    # Quality Indicators
    has_attachments = models.BooleanField(default=False, help_text="Có tệp đính kèm")
    attachment_quality_score = models.FloatField(
        default=0.0, help_text="Điểm chất lượng tệp đính kèm"
    )
    terminology_accuracy = models.FloatField(
        default=0.0, help_text="Độ chính xác thuật ngữ"
    )
    vietnamese_language_quality = models.FloatField(
        default=0.0, help_text="Chất lượng tiếng Việt"
    )

    # Overall Scores
    overall_completeness = models.FloatField(
        default=0.0, help_text="Độ hoàn thiện tổng thể"
    )
    overall_quality = models.FloatField(default=0.0, help_text="Chất lượng tổng thể")

    # Timestamps
    last_calculated_at = models.DateTimeField(
        auto_now=True, help_text="Lần tính toán cuối"
    )

    class Meta:
        db_table = "cases_casequalitymetrics"
        verbose_name = "Case Quality Metrics"
        verbose_name_plural = "Case Quality Metrics"

    def __str__(self):
        return f"Quality metrics for {self.case.title}"

    def calculate_completeness(self):
        """Calculate all completeness metrics"""
        case = self.case

        # Clinical History
        if hasattr(case, "clinical_history"):
            ch = case.clinical_history
            fields = [
                ch.chief_complaint,
                ch.history_present_illness,
                ch.past_medical_history,
                ch.medications,
            ]
            filled = sum(1 for f in fields if f and f.strip())
            self.clinical_history_completeness = (filled / len(fields)) * 100

        # Physical Examination
        if hasattr(case, "physical_examination"):
            pe = case.physical_examination
            fields = [
                pe.general_appearance,
                pe.vital_signs,
                pe.cardiovascular,
                pe.respiratory,
            ]
            filled = sum(1 for f in fields if f and f.strip())
            self.examination_completeness = (filled / len(fields)) * 100

        # Investigations
        if hasattr(case, "investigations_detail"):
            inv = case.investigations_detail
            fields = [inv.laboratory_results, inv.imaging_studies]
            filled = sum(1 for f in fields if f and f.strip())
            self.investigation_completeness = (filled / len(fields)) * 100

        # Diagnosis
        if hasattr(case, "diagnosis_management"):
            dm = case.diagnosis_management
            fields = [dm.primary_diagnosis, dm.treatment_plan]
            filled = sum(1 for f in fields if f and f.strip())
            self.diagnosis_completeness = (filled / len(fields)) * 100

        # Learning Objectives
        if hasattr(case, "learning_outcomes"):
            lo = case.learning_outcomes
            fields = [lo.learning_objectives, lo.key_concepts]
            filled = sum(1 for f in fields if f and f.strip())
            self.learning_objectives_completeness = (filled / len(fields)) * 100

        # Overall completeness
        scores = [
            self.clinical_history_completeness,
            self.examination_completeness,
            self.investigation_completeness,
            self.diagnosis_completeness,
            self.learning_objectives_completeness,
        ]
        self.overall_completeness = sum(scores) / len(scores) if scores else 0.0

        # Attachments
        self.has_attachments = case.medical_attachments.exists()
        if self.has_attachments:
            attachment_count = case.medical_attachments.count()
            self.attachment_quality_score = min(100, attachment_count * 20)

        # Overall quality (weighted average)
        self.overall_quality = (
            self.overall_completeness * 0.6
            + self.attachment_quality_score * 0.2
            + self.terminology_accuracy * 0.1
            + self.vietnamese_language_quality * 0.1
        )

        self.save()
