"""
Admin interfaces for Validation System
"""

from django.contrib import admin
from .validation import (
    CaseValidationRule,
    CaseValidationResult,
    CaseSubmissionWorkflow,
    MedicalTerminologyCheck,
    CaseQualityMetrics,
)


@admin.register(CaseValidationRule)
class CaseValidationRuleAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "rule_type",
        "severity",
        "target_field",
        "is_active",
        "created_at",
    ]
    list_filter = ["rule_type", "severity", "is_active", "created_at"]
    search_fields = ["name", "target_field", "error_message_vi"]
    readonly_fields = ["created_by", "created_at", "updated_at"]

    fieldsets = (
        (
            "Thông tin cơ bản",
            {"fields": ("name", "rule_type", "severity", "is_active")},
        ),
        ("Cấu hình quy tắc", {"fields": ("target_field", "rule_config")}),
        (
            "Phạm vi áp dụng",
            {"fields": ("applies_to_specialties",)},
        ),
        (
            "Thông báo lỗi",
            {"fields": ("error_message_vi", "error_message_en", "help_text")},
        ),
        (
            "Metadata",
            {
                "fields": ("created_by", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(CaseValidationResult)
class CaseValidationResultAdmin(admin.ModelAdmin):
    list_display = [
        "case",
        "validation_status",
        "overall_score",
        "rules_passed",
        "rules_failed",
        "warnings_count",
        "validated_at",
    ]
    list_filter = ["validation_status", "validation_type", "validated_at"]
    search_fields = ["case__title", "case__student__email"]
    readonly_fields = [
        "case",
        "validation_status",
        "total_rules_checked",
        "rules_passed",
        "rules_failed",
        "warnings_count",
        "validation_issues",
        "completeness_score",
        "quality_score",
        "overall_score",
        "validated_at",
        "validated_by",
        "validation_type",
    ]
    date_hierarchy = "validated_at"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # type: ignore[attr-defined]


@admin.register(CaseSubmissionWorkflow)
class CaseSubmissionWorkflowAdmin(admin.ModelAdmin):
    list_display = [
        "case",
        "current_status",
        "submitted_at",
        "assigned_reviewer",
        "revision_count",
        "updated_at",
    ]
    list_filter = ["current_status", "submitted_at", "approved_at"]
    search_fields = ["case__title", "case__student__email", "assigned_reviewer__email"]
    readonly_fields = [
        "submitted_at",
        "submitted_by",
        "review_started_at",
        "review_completed_at",
        "approved_at",
        "approved_by",
        "rejected_at",
        "last_revision_requested_at",
        "workflow_history",
        "created_at",
        "updated_at",
    ]
    date_hierarchy = "submitted_at"

    fieldsets = (
        ("Ca bệnh", {"fields": ("case", "current_status")}),
        ("Nộp bài", {"fields": ("submitted_at", "submitted_by")}),
        (
            "Xem xét",
            {
                "fields": (
                    "assigned_reviewer",
                    "review_started_at",
                    "review_completed_at",
                )
            },
        ),
        ("Phê duyệt", {"fields": ("approved_at", "approved_by")}),
        (
            "Sửa đổi",
            {
                "fields": (
                    "revision_count",
                    "revision_notes",
                    "last_revision_requested_at",
                )
            },
        ),
        ("Từ chối", {"fields": ("rejected_at", "rejection_reason")}),
        (
            "Lịch sử",
            {
                "fields": ("workflow_history", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(MedicalTerminologyCheck)
class MedicalTerminologyCheckAdmin(admin.ModelAdmin):
    list_display = [
        "term",
        "vietnamese_term",
        "category",
        "is_approved",
        "requires_context",
    ]
    list_filter = ["category", "is_approved", "requires_context"]
    search_fields = ["term", "vietnamese_term", "definition"]

    fieldsets = (
        ("Thuật ngữ", {"fields": ("term", "vietnamese_term", "category")}),
        ("Định nghĩa", {"fields": ("definition", "synonyms")}),
        ("Kiểm tra", {"fields": ("is_approved", "requires_context")}),
    )


@admin.register(CaseQualityMetrics)
class CaseQualityMetricsAdmin(admin.ModelAdmin):
    list_display = [
        "case",
        "overall_completeness",
        "overall_quality",
        "has_attachments",
        "last_calculated_at",
    ]
    list_filter = ["has_attachments", "last_calculated_at"]
    search_fields = ["case__title", "case__student__email"]
    readonly_fields = [
        "case",
        "clinical_history_completeness",
        "examination_completeness",
        "investigation_completeness",
        "diagnosis_completeness",
        "learning_objectives_completeness",
        "has_attachments",
        "attachment_quality_score",
        "terminology_accuracy",
        "vietnamese_language_quality",
        "overall_completeness",
        "overall_quality",
        "last_calculated_at",
    ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
