"""
Serializers for Validation System
"""

from rest_framework import serializers
from .validation import (
    CaseValidationRule,
    CaseValidationResult,
    CaseSubmissionWorkflow,
    MedicalTerminologyCheck,
    CaseQualityMetrics,
)


class CaseValidationRuleSerializer(serializers.ModelSerializer):
    """Serializer for validation rules"""

    created_by_name = serializers.CharField(
        source="created_by.get_full_name", read_only=True
    )
    template_names = serializers.SerializerMethodField()

    class Meta:
        model = CaseValidationRule
        fields = [
            "id",
            "name",
            "rule_type",
            "severity",
            "target_field",
            "rule_config",
            "applies_to_specialties",
            "is_active",
            "error_message_vi",
            "error_message_en",
            "help_text",
            "created_by",
            "created_by_name",
            "template_names",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_by", "created_at", "updated_at"]

    def get_template_names(self, obj):
        return [t.name for t in obj.applies_to_templates.all()]


class CaseValidationResultSerializer(serializers.ModelSerializer):
    """Serializer for validation results"""

    case_title = serializers.CharField(source="case.title", read_only=True)
    validated_by_name = serializers.CharField(
        source="validated_by.get_full_name", read_only=True
    )

    class Meta:
        model = CaseValidationResult
        fields = [
            "id",
            "case",
            "case_title",
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
            "validated_by_name",
            "validation_type",
        ]
        read_only_fields = fields


class CaseSubmissionWorkflowSerializer(serializers.ModelSerializer):
    """Serializer for submission workflow"""

    case_title = serializers.CharField(source="case.title", read_only=True)
    submitted_by_name = serializers.CharField(
        source="submitted_by.get_full_name", read_only=True
    )
    assigned_reviewer_name = serializers.CharField(
        source="assigned_reviewer.get_full_name", read_only=True
    )
    approved_by_name = serializers.CharField(
        source="approved_by.get_full_name", read_only=True
    )

    class Meta:
        model = CaseSubmissionWorkflow
        fields = [
            "id",
            "case",
            "case_title",
            "current_status",
            "submitted_at",
            "submitted_by",
            "submitted_by_name",
            "assigned_reviewer",
            "assigned_reviewer_name",
            "review_started_at",
            "review_completed_at",
            "approved_at",
            "approved_by",
            "approved_by_name",
            "revision_count",
            "revision_notes",
            "last_revision_requested_at",
            "rejected_at",
            "rejection_reason",
            "workflow_history",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "submitted_at",
            "review_started_at",
            "review_completed_at",
            "approved_at",
            "rejected_at",
            "last_revision_requested_at",
            "workflow_history",
            "created_at",
            "updated_at",
        ]


class WorkflowTransitionSerializer(serializers.Serializer):
    """Serializer for workflow transitions"""

    new_status = serializers.ChoiceField(
        choices=CaseSubmissionWorkflow.WorkflowStatus.choices
    )
    notes = serializers.CharField(required=False, allow_blank=True)
    assigned_reviewer_id = serializers.IntegerField(required=False, allow_null=True)


class MedicalTerminologyCheckSerializer(serializers.ModelSerializer):
    """Serializer for medical terminology"""

    class Meta:
        model = MedicalTerminologyCheck
        fields = [
            "id",
            "term",
            "vietnamese_term",
            "category",
            "definition",
            "synonyms",
            "is_approved",
            "requires_context",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class CaseQualityMetricsSerializer(serializers.ModelSerializer):
    """Serializer for case quality metrics"""

    case_title = serializers.CharField(source="case.title", read_only=True)

    class Meta:
        model = CaseQualityMetrics
        fields = [
            "id",
            "case",
            "case_title",
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
        read_only_fields = fields


class ValidationReportSerializer(serializers.Serializer):
    """
    Comprehensive validation report for a case
    """

    case_id = serializers.IntegerField()
    case_title = serializers.CharField()
    validation_result = CaseValidationResultSerializer()
    quality_metrics = CaseQualityMetricsSerializer()
    workflow_status = serializers.CharField()
    can_submit = serializers.BooleanField()
    blocking_issues = serializers.ListField()
    warnings = serializers.ListField()
    recommendations = serializers.ListField()


class BulkValidationSerializer(serializers.Serializer):
    """Serializer for bulk validation requests"""

    case_ids = serializers.ListField(
        child=serializers.IntegerField(), help_text="Danh sách ID ca bệnh cần kiểm tra"
    )
    validation_type = serializers.ChoiceField(
        choices=[
            ("automatic", "Tự động"),
            ("manual", "Thủ công"),
            ("pre_submission", "Trước khi nộp"),
        ],
        default="automatic",
    )
