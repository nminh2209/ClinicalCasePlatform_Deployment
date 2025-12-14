"""
Views for Validation System
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from .validation import (
    CaseValidationRule,
    CaseValidationResult,
    CaseSubmissionWorkflow,
    MedicalTerminologyCheck,
    CaseQualityMetrics,
)
from .validation_serializers import (
    CaseValidationRuleSerializer,
    CaseValidationResultSerializer,
    CaseSubmissionWorkflowSerializer,
    WorkflowTransitionSerializer,
    MedicalTerminologyCheckSerializer,
    CaseQualityMetricsSerializer,
    ValidationReportSerializer,
    BulkValidationSerializer,
)
from cases.models import Case


class CaseValidationRuleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing validation rules
    Admin and instructors can create and manage rules
    """

    queryset = CaseValidationRule.objects.all()
    serializer_class = CaseValidationRuleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by active status
        if self.request.query_params.get("active_only") == "true":
            queryset = queryset.filter(is_active=True)

        # Filter by rule type
        rule_type = self.request.query_params.get("rule_type")
        if rule_type:
            queryset = queryset.filter(rule_type=rule_type)

        # Filter by severity
        severity = self.request.query_params.get("severity")
        if severity:
            queryset = queryset.filter(severity=severity)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def toggle_active(self, request, pk=None):
        """
        Toggle rule active status
        POST /api/validation-rules/{id}/toggle_active/
        """
        rule = self.get_object()
        rule.is_active = not rule.is_active
        rule.save()

        return Response(
            {"message": "Đã cập nhật trạng thái quy tắc", "is_active": rule.is_active}
        )


class CaseValidationViewSet(viewsets.ViewSet):
    """
    ViewSet for case validation operations
    Handles validation execution and results
    """

    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"])
    def validate_case(self, request):
        """
        Validate a single case
        POST /api/case-validation/validate_case/
        Body: {"case_id": 123, "validation_type": "pre_submission"}
        """
        case_id = request.data.get("case_id")
        validation_type = request.data.get("validation_type", "automatic")

        try:
            case = Case.objects.get(id=case_id)
        except Case.DoesNotExist:
            return Response(
                {"error": "Ca bệnh không tồn tại"}, status=status.HTTP_404_NOT_FOUND
            )

        # Check permissions
        if request.user.role == "student" and case.student != request.user:
            return Response(
                {"error": "Không có quyền kiểm tra ca bệnh này"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get applicable rules
        rules = CaseValidationRule.objects.filter(is_active=True)

        # Filter by template
        if case.template:
            rules = rules.filter(
                Q(applies_to_templates__isnull=True)
                | Q(applies_to_templates=case.template)
            )

        # Filter by specialty
        rules = rules.filter(
            Q(applies_to_specialties=[])
            | Q(applies_to_specialties__contains=[case.specialty])
        )

        # Validate against each rule
        validation_issues = []
        rules_passed = 0
        rules_failed = 0
        warnings_count = 0

        for rule in rules:
            is_valid, error_message = rule.validate_case(case)

            if not is_valid:
                issue = {
                    "rule_name": rule.name,
                    "severity": rule.severity,
                    "field": rule.target_field,
                    "message": error_message,
                    "help_text": rule.help_text,
                }
                validation_issues.append(issue)

                if rule.severity == "error":
                    rules_failed += 1
                elif rule.severity == "warning":
                    warnings_count += 1
            else:
                rules_passed += 1

        # Determine overall status
        if rules_failed > 0:
            validation_status = "failed"
        elif warnings_count > 0:
            validation_status = "warning"
        else:
            validation_status = "passed"

        # Calculate quality metrics
        quality_metrics, created = CaseQualityMetrics.objects.get_or_create(case=case)
        quality_metrics.calculate_completeness()

        # Calculate scores
        total_rules = rules.count()
        completeness_score = (
            (rules_passed / total_rules * 100) if total_rules > 0 else 0
        )
        quality_score = quality_metrics.overall_quality
        overall_score = completeness_score * 0.6 + quality_score * 0.4

        # Create validation result
        validation_result = CaseValidationResult.objects.create(
            case=case,
            validation_status=validation_status,
            total_rules_checked=total_rules,
            rules_passed=rules_passed,
            rules_failed=rules_failed,
            warnings_count=warnings_count,
            validation_issues=validation_issues,
            completeness_score=completeness_score,
            quality_score=quality_score,
            overall_score=overall_score,
            validated_by=request.user if validation_type == "manual" else None,
            validation_type=validation_type,
        )

        serializer = CaseValidationResultSerializer(validation_result)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def bulk_validate(self, request):
        """
        Validate multiple cases
        POST /api/case-validation/bulk_validate/
        Body: {"case_ids": [1, 2, 3], "validation_type": "automatic"}
        """
        serializer = BulkValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        case_ids = serializer.validated_data["case_ids"]
        validation_type = serializer.validated_data["validation_type"]

        results = []

        for case_id in case_ids:
            try:
                case = Case.objects.get(id=case_id)

                # Check permissions
                if request.user.role == "student" and case.student != request.user:
                    continue

                # Validate (simplified version)
                response = self.validate_case(  # type: ignore[misc, assignment]
                    type(
                        "Request",
                        (),
                        {
                            "data": {
                                "case_id": case_id,
                                "validation_type": validation_type,
                            },
                            "user": request.user,
                        },
                    )()
                )

                if response.status_code == 200:
                    results.append(response.data)

            except Case.DoesNotExist:
                continue

        return Response({"total_validated": len(results), "results": results})

    @action(detail=False, methods=["get"])
    def validation_report(self, request):
        """
        Get comprehensive validation report for a case
        GET /api/case-validation/validation_report/?case_id=123
        """
        case_id = request.query_params.get("case_id")

        if not case_id:
            return Response(
                {"error": "case_id là bắt buộc"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            case = Case.objects.get(id=case_id)
        except Case.DoesNotExist:
            return Response(
                {"error": "Ca bệnh không tồn tại"}, status=status.HTTP_404_NOT_FOUND
            )

        # Check permissions
        if request.user.role == "student" and case.student != request.user:
            return Response(
                {"error": "Không có quyền xem báo cáo này"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get latest validation result
        validation_result = (
            CaseValidationResult.objects.filter(case=case)
            .order_by("-validated_at")
            .first()
        )

        # Get quality metrics
        quality_metrics = CaseQualityMetrics.objects.filter(case=case).first()

        # Get workflow status
        workflow = CaseSubmissionWorkflow.objects.filter(case=case).first()
        workflow_status = workflow.current_status if workflow else "draft"
        can_submit = workflow.can_submit() if workflow else True

        # Categorize issues
        blocking_issues = []
        warnings = []
        recommendations = []

        if validation_result:
            for issue in validation_result.validation_issues:
                if issue["severity"] == "error":
                    blocking_issues.append(issue)
                elif issue["severity"] == "warning":
                    warnings.append(issue)
                else:
                    recommendations.append(issue)

        report_data = {
            "case_id": case.id,  # type: ignore[misc, assignment]
            "case_title": case.title,
            "validation_result": (
                CaseValidationResultSerializer(validation_result).data
                if validation_result
                else None
            ),
            "quality_metrics": (
                CaseQualityMetricsSerializer(quality_metrics).data
                if quality_metrics
                else None
            ),
            "workflow_status": workflow_status,
            "can_submit": can_submit and len(blocking_issues) == 0,
            "blocking_issues": blocking_issues,
            "warnings": warnings,
            "recommendations": recommendations,
        }

        serializer = ValidationReportSerializer(report_data)
        return Response(serializer.data)


class CaseSubmissionWorkflowViewSet(viewsets.ModelViewSet):
    """
    ViewSet for case submission workflow
    Manages the review and approval process
    """

    queryset = CaseSubmissionWorkflow.objects.all()
    serializer_class = CaseSubmissionWorkflowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # Students see their own workflows
        if user.role == "student":  # type: ignore[misc, assignment]
            queryset = queryset.filter(case__student=user)
        # Instructors see workflows assigned to them or in their department
        elif user.role == "instructor":  # type: ignore[misc, assignment]
            queryset = queryset.filter(
                Q(assigned_reviewer=user) | Q(case__student__department=user.department)  # type: ignore[misc, assignment]
            )

        # Filter by status
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(current_status=status_filter)

        return queryset

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def submit(self, request, pk=None):
        """
        Submit a case for review
        POST /api/submission-workflow/{id}/submit/
        """
        workflow = self.get_object()

        # Check permissions
        if workflow.case.student != request.user:
            return Response(
                {"error": "Chỉ sinh viên sở hữu ca bệnh mới có thể nộp"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Check if can submit
        if not workflow.can_submit():
            return Response(
                {
                    "error": f"Không thể nộp ca bệnh ở trạng thái {workflow.get_current_status_display()}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate case first
        validation_result = (
            CaseValidationResult.objects.filter(case=workflow.case)
            .order_by("-validated_at")
            .first()
        )

        if not validation_result or validation_result.validation_status == "failed":
            return Response(
                {
                    "error": "Ca bệnh chưa đạt yêu cầu kiểm tra. Vui lòng kiểm tra và sửa các lỗi trước khi nộp."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Transition to submitted
        workflow.transition_to(
            CaseSubmissionWorkflow.WorkflowStatus.SUBMITTED,
            user=request.user,
            notes="Ca bệnh đã được nộp để xem xét",
        )

        # Update case status
        workflow.case.case_status = "submitted"
        workflow.case.submitted_at = timezone.now()
        workflow.case.save()

        serializer = self.get_serializer(workflow)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def assign_reviewer(self, request, pk=None):
        """
        Assign a reviewer to the case
        POST /api/submission-workflow/{id}/assign_reviewer/
        Body: {"reviewer_id": 5}
        """
        workflow = self.get_object()

        # Only instructors and admins can assign reviewers
        if request.user.role not in ["instructor", "admin"]:
            return Response(
                {"error": "Không có quyền chỉ định người xem xét"},
                status=status.HTTP_403_FORBIDDEN,
            )

        reviewer_id = request.data.get("reviewer_id")

        from accounts.models import User

        try:
            reviewer = User.objects.get(
                id=reviewer_id, role__in=["instructor", "admin"]
            )
        except User.DoesNotExist:
            return Response(
                {"error": "Người xem xét không hợp lệ"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        workflow.assigned_reviewer = reviewer

        if workflow.current_status == CaseSubmissionWorkflow.WorkflowStatus.SUBMITTED:
            workflow.transition_to(
                CaseSubmissionWorkflow.WorkflowStatus.UNDER_REVIEW,
                user=request.user,
                notes=f"Đã chỉ định {reviewer.get_full_name()} xem xét",
            )
        else:
            workflow.save()

        serializer = self.get_serializer(workflow)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def approve(self, request, pk=None):
        """
        Approve a case
        POST /api/submission-workflow/{id}/approve/
        Body: {"notes": "Excellent work!"}
        """
        workflow = self.get_object()

        # Only assigned reviewer or admin can approve
        if request.user.role not in ["instructor", "admin"]:
            return Response(
                {"error": "Không có quyền phê duyệt"}, status=status.HTTP_403_FORBIDDEN
            )

        if not workflow.can_approve():
            return Response(
                {
                    "error": f"Không thể phê duyệt ca bệnh ở trạng thái {workflow.get_current_status_display()}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        notes = request.data.get("notes", "")

        workflow.transition_to(
            CaseSubmissionWorkflow.WorkflowStatus.APPROVED,
            user=request.user,
            notes=notes,
        )

        # Update case status
        workflow.case.case_status = "approved"
        workflow.case.reviewed_at = timezone.now()
        workflow.case.reviewed_by = request.user
        workflow.case.save()

        serializer = self.get_serializer(workflow)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def request_revision(self, request, pk=None):
        """
        Request revisions to a case
        POST /api/submission-workflow/{id}/request_revision/
        Body: {"notes": "Please add more details to the diagnosis section"}
        """
        workflow = self.get_object()

        # Only assigned reviewer or admin can request revisions
        if request.user.role not in ["instructor", "admin"]:
            return Response(
                {"error": "Không có quyền yêu cầu sửa đổi"},
                status=status.HTTP_403_FORBIDDEN,
            )

        notes = request.data.get("notes", "")

        if not notes:
            return Response(
                {"error": "Vui lòng cung cấp ghi chú về những gì cần sửa đổi"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        workflow.transition_to(
            CaseSubmissionWorkflow.WorkflowStatus.REVISION_REQUESTED,
            user=request.user,
            notes=notes,
        )

        serializer = self.get_serializer(workflow)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def reject(self, request, pk=None):
        """
        Reject a case
        POST /api/submission-workflow/{id}/reject/
        Body: {"reason": "Does not meet educational standards"}
        """
        workflow = self.get_object()

        # Only assigned reviewer or admin can reject
        if request.user.role not in ["instructor", "admin"]:
            return Response(
                {"error": "Không có quyền từ chối"}, status=status.HTTP_403_FORBIDDEN
            )

        reason = request.data.get("reason", "")

        if not reason:
            return Response(
                {"error": "Vui lòng cung cấp lý do từ chối"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        workflow.transition_to(
            CaseSubmissionWorkflow.WorkflowStatus.REJECTED,
            user=request.user,
            notes=reason,
        )

        # Update case status
        workflow.case.case_status = "draft"
        workflow.case.save()

        serializer = self.get_serializer(workflow)
        return Response(serializer.data)


class MedicalTerminologyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for medical terminology management
    """

    queryset = MedicalTerminologyCheck.objects.all()
    serializer_class = MedicalTerminologyCheckSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by category
        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category=category)

        # Search by term
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(term__icontains=search) | Q(vietnamese_term__icontains=search)
            )

        # Only approved terms
        if self.request.query_params.get("approved_only") == "true":
            queryset = queryset.filter(is_approved=True)

        return queryset

    @action(detail=False, methods=["get"])
    def categories(self, request):
        """
        Get list of all categories
        GET /api/medical-terminology/categories/
        """
        categories = (
            MedicalTerminologyCheck.objects.values_list("category", flat=True)
            .distinct()
            .order_by("category")
        )

        return Response(list(categories))


class CaseQualityMetricsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for case quality metrics
    Read-only access to quality assessments
    """

    queryset = CaseQualityMetrics.objects.all()
    serializer_class = CaseQualityMetricsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # Students see their own metrics
        if user.role == "student":  # type: ignore[misc, assignment]
            queryset = queryset.filter(case__student=user)
        # Instructors see metrics for cases in their department
        elif user.role == "instructor" and user.department:  # type: ignore[misc, assignment]
            queryset = queryset.filter(case__student__department=user.department)  # type: ignore[misc, assignment]

        return queryset

    @action(detail=True, methods=["post"])
    def recalculate(self, request, pk=None):
        """
        Recalculate quality metrics for a case
        POST /api/case-quality-metrics/{id}/recalculate/
        """
        metrics = self.get_object()
        metrics.calculate_completeness()

        serializer = self.get_serializer(metrics)
        return Response(serializer.data)
