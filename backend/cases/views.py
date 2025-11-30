from rest_framework import generics, permissions, status, filters, viewsets, parsers
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta
import secrets
from django.core.cache import cache
from difflib import SequenceMatcher

# Type hints to help Pylance
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rest_framework.request import Request
    from accounts.models import User

from .models import Case, CasePermission, GuestAccess, CaseGroup, PermissionAuditLog
from .medical_models import MedicalTerm, ICD10Code, MedicalAbbreviation
from .medical_models import (
    Department,
    # ClinicalHistory,
    # PhysicalExamination,
    # Investigations,
    # DiagnosisManagement,
    # LearningOutcomes,
    MedicalAttachment,
    StudentNotes,
)
from .serializers import (
    CaseListSerializer,
    CaseDetailSerializer,
    CaseCreateUpdateSerializer,
    CasePermissionSerializer,
    GuestAccessSerializer,
    CaseGroupSerializer,
    PermissionAuditLogSerializer,
    BulkPermissionSerializer,
    MedicalAttachmentSerializer,
    StudentNotesSerializer,
    DepartmentSerializer,
    MedicalTermSerializer,
    ICD10Serializer,
    AbbreviationSerializer,
    CaseSummarySerializer,
)


class CaseListCreateView(generics.ListCreateAPIView):
    """
    List cases with advanced filtering and create new cases

    Query parameters:
    - specialty: Filter by specialty
    - case_status: Filter by status (draft, submitted, reviewed, approved)
    - priority_level: Filter by priority (low, medium, high, urgent)
    - complexity_level: Filter by complexity (basic, intermediate, advanced, expert)
    - date_from: Filter cases created after this date (YYYY-MM-DD)
    - date_to: Filter cases created before this date (YYYY-MM-DD)
    - admission_from: Filter by admission date after (YYYY-MM-DD)
    - admission_to: Filter by admission date before (YYYY-MM-DD)
    - department: Filter by department ID
    - search: Search in title, diagnosis, patient_name, keywords
    - ordering: Order by created_at, updated_at, title, priority_level
    """

    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "specialty",
        "case_status",
        "priority_level",
        "complexity_level",
        "student__role",
    ]
    search_fields = ["title", "keywords", "patient_name", "case_summary"]
    ordering_fields = [
        "created_at",
        "updated_at",
        "title",
        "priority_level",
        "admission_date",
    ]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = Case.objects.annotate(
            comment_count=Count("comments")
        ).select_related("student", "repository")

        user = self.request.user

        # Role & permission-based visibility filtering
        # Instructors: see cases from their department, public cases, or cases shared to them (individual),
        # department-shared (target_department), or public-share_type permissions.
        # Students: only their own, public, or shared cases
        if user.is_authenticated and getattr(user, "is_instructor", False):
            department_id = user.department_id
            # Active (and not expired) permission-based access
            permission_active_q = Q(permissions__is_active=True) & (
                Q(permissions__expires_at__isnull=True)
                | Q(permissions__expires_at__gte=timezone.now())
            )
            permission_q = permission_active_q & (
                Q(permissions__user=user)  # individual share
                | Q(
                    permissions__share_type="department",
                    permissions__target_department_id=department_id,
                )
                | Q(permissions__share_type="public")
            )

            queryset = queryset.filter(
                Q(student__department_id=department_id)
                | Q(repository__department_id=department_id)
                | Q(is_public=True)
                | permission_q
            ).distinct()

        # Students: only their own cases, public cases, or cases shared to them/department/public
        elif user.is_authenticated and getattr(user, "is_student", False):
            department_id = user.department_id
            permission_active_q = Q(permissions__is_active=True) & (
                Q(permissions__expires_at__isnull=True)
                | Q(permissions__expires_at__gte=timezone.now())
            )
            permission_q = permission_active_q & (
                Q(permissions__user=user)
                | Q(
                    permissions__share_type="department",
                    permissions__target_department_id=department_id,
                )
                | Q(permissions__share_type="public")
            )

            queryset = queryset.filter(
                Q(student=user) | Q(is_public=True) | permission_q
            ).distinct()

        # Date range filtering
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")
        if date_from:
            parsed_date = parse_date(date_from)
            if parsed_date:
                queryset = queryset.filter(created_at__gte=parsed_date)
        if date_to:
            parsed_date = parse_date(date_to)
            if parsed_date:
                queryset = queryset.filter(created_at__lte=parsed_date)

        # Admission date filtering
        admission_from = self.request.query_params.get("admission_from")
        admission_to = self.request.query_params.get("admission_to")
        if admission_from:
            parsed_date = parse_date(admission_from)
            if parsed_date:
                queryset = queryset.filter(admission_date__gte=parsed_date)
        if admission_to:
            parsed_date = parse_date(admission_to)
            if parsed_date:
                queryset = queryset.filter(admission_date__lte=parsed_date)

        # Department filtering through repository
        department_id = self.request.query_params.get("department")
        if department_id:
            queryset = queryset.filter(repository__department_id=department_id)

        # Custom Q object searches for multi-field matching
        q_search = self.request.query_params.get("q")
        if q_search:
            queryset = queryset.filter(
                Q(title__icontains=q_search)
                | Q(patient_name__icontains=q_search)
                | Q(keywords__icontains=q_search)
                | Q(case_summary__icontains=q_search)
                | Q(specialty__icontains=q_search)
            )

        # Public cases filter
        is_public = self.request.query_params.get("is_public")
        if is_public is not None:
            queryset = queryset.filter(is_public=is_public.lower() == "true")

        return queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CaseCreateUpdateSerializer
        return CaseListSerializer

    def create(self, request, *args, **kwargs):
        """
        Handle case creation with potential file uploads
        """
        # If request has multipart data with 'data' field, parse it
        if hasattr(request, 'data') and 'data' in request.data:
            import json
            try:
                case_data = json.loads(request.data['data'])
                # Create a new request-like object with parsed data
                from django.http import QueryDict
                from django.utils.datastructures import MultiValueDict
                
                # Create a mutable copy of request.data
                mutable_data = MultiValueDict()
                for key, value in request.data.items():
                    if key != 'data':
                        mutable_data[key] = value
                
                # Add parsed JSON data
                for key, value in case_data.items():
                    mutable_data[key] = value
                
                # Replace request.data with the combined data
                request._full_data = mutable_data
                request._data = mutable_data
                
            except (json.JSONDecodeError, KeyError):
                pass
        
        return super().create(request, *args, **kwargs)


class CaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific case with detailed medical sections
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Case.objects.select_related(
            "student", "template", "repository"
        ).prefetch_related(
            "clinical_history",
            "physical_examination",
            "investigations_detail",
            "diagnosis_management",
            "learning_outcomes",
            "medical_attachments",
        )

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return CaseCreateUpdateSerializer
        return CaseDetailSerializer

    def get_object(self):
        case = super().get_object()
        user = self.request.user

        # Check permissions
        if case.student == user:
            return case  # Owner has full access

        # Check if user has permission to view this case (with expiry check)
        if user.is_instructor and case.repository.is_public:
            return case

        # Check active permissions with expiry
        active_permission = CasePermission.objects.filter(
            case=case, 
            user=user, 
            is_active=True
        ).filter(
            Q(expires_at__isnull=True) | Q(expires_at__gte=timezone.now())
        ).exists()
        
        if active_permission:
            return case

        # If no permission, check if it's a public repository
        if case.repository.is_public:
            return case

        # No access
        from django.core.exceptions import PermissionDenied

        raise PermissionDenied("You don't have permission to access this case")
    
    def perform_update(self, serializer):
        """Only owner can update their own draft cases"""
        case = self.get_object()
        user = self.request.user
        
        # Only the case owner can update
        if case.student != user:
            raise PermissionDenied("Only the case owner can update this case")
        
        # Only drafts can be updated
        if case.case_status != 'draft':
            raise PermissionDenied("Only draft cases can be updated")
        
        serializer.save()
    
    def perform_destroy(self, instance):
        """Only owner can delete their own cases"""
        user = self.request.user
        
        # Only the case owner or instructors can delete
        if instance.student != user and not user.is_instructor:
            raise PermissionDenied("Only the case owner or instructors can delete this case")
        
        instance.delete()


class CasePermissionListCreateView(generics.ListCreateAPIView):
    """
    List and create case permissions for sharing cases

    POST body for single permission:
    {
        "user": 2,
        "permission_type": "view"
    }

    POST body for bulk permissions:
    {
        "users": [2, 3, 4],
        "permission_type": "comment"
    }
    """

    serializer_class = CasePermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        case_id = self.kwargs.get("case_pk")
        return CasePermission.objects.filter(case_id=case_id).select_related(
            "user", "granted_by"
        )

    def perform_create(self, serializer):
        case_id = self.kwargs.get("case_pk")
        case = Case.objects.get(id=case_id)

        # Only case owner or instructors can grant permissions
        if case.student != self.request.user and not self.request.user.is_instructor:
            raise PermissionDenied(
                "Only the case owner or instructors can grant permissions"
            )

        serializer.save(case=case)

    def create(self, request, *args, **kwargs):
        """
        Enhanced create with bulk permission support
        """
        case_id = self.kwargs.get("case_pk")
        case = Case.objects.get(id=case_id)

        # Check if case owner or instructor
        if case.student != request.user and not request.user.is_instructor:
            raise PermissionDenied(
                "Only the case owner or instructors can grant permissions"
            )

        # Check for bulk creation
        users_list = request.data.get("users")
        if users_list:
            # Bulk permission creation
            permission_type = request.data.get("permission_type", "view")
            created_permissions = []

            for user_id in users_list:
                # Check if permission already exists
                existing = CasePermission.objects.filter(
                    case=case, user_id=user_id
                ).first()

                if existing:
                    # Update existing permission
                    existing.permission_type = permission_type
                    existing.is_active = True
                    existing.save()
                    created_permissions.append(existing)
                else:
                    # Create new permission
                    permission = CasePermission.objects.create(
                        case=case,
                        user_id=user_id,
                        permission_type=permission_type,
                        granted_by=request.user,
                    )
                    created_permissions.append(permission)

            serializer = self.get_serializer(created_permissions, many=True)
            return Response(
                {
                    "message": f"Granted {len(created_permissions)} permissions",
                    "permissions": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        # Single permission creation
        return super().create(request, *args, **kwargs)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def revoke_case_permission(request, case_pk, permission_id):
    """
    Revoke a specific case permission
    DELETE /api/cases/{case_pk}/permissions/{permission_id}/revoke/
    """
    try:
        case = Case.objects.get(id=case_pk)
        permission = CasePermission.objects.get(id=permission_id, case=case)

        # Only case owner or instructors can revoke
        if case.student != request.user and not request.user.is_instructor:
            raise PermissionDenied(
                "Only the case owner or instructors can revoke permissions"
            )

        permission.is_active = False
        permission.save()

        return Response(
            {"message": "Permission revoked successfully"}, status=status.HTTP_200_OK
        )
    except Case.DoesNotExist:
        return Response({"error": "Case not found"}, status=status.HTTP_404_NOT_FOUND)
    except CasePermission.DoesNotExist:
        return Response(
            {"error": "Permission not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def check_case_permission(request, pk):
    """
    Check if current user has permission to access a case
    POST /api/cases/{pk}/check-permission/

    Returns:
    {
        "has_access": true,
        "permission_type": "view",
        "is_owner": false,
        "can_edit": false,
        "can_comment": true
    }
    """
    try:
        case = Case.objects.get(id=pk)
        user = request.user

        # Check if owner
        if case.student == user:
            return Response(
                {
                    "has_access": True,
                    "permission_type": "owner",
                    "is_owner": True,
                    "can_edit": True,
                    "can_comment": True,
                    "can_share": True,
                },
                status=status.HTTP_200_OK,
            )

        # Check if instructor
        if user.is_instructor:
            return Response(
                {
                    "has_access": True,
                    "permission_type": "instructor",
                    "is_owner": False,
                    "can_edit": True,
                    "can_comment": True,
                    "can_share": True,
                },
                status=status.HTTP_200_OK,
            )

        # Check explicit permission
        permission = CasePermission.objects.filter(
            case=case, user=user, is_active=True
        ).first()

        if permission:
            return Response(
                {
                    "has_access": True,
                    "permission_type": permission.permission_type,
                    "is_owner": False,
                    "can_edit": permission.permission_type == "edit",
                    "can_comment": permission.permission_type in ["comment", "edit"],
                    "can_share": False,
                },
                status=status.HTTP_200_OK,
            )

        # No permission
        return Response(
            {
                "has_access": False,
                "permission_type": None,
                "is_owner": False,
                "can_edit": False,
                "can_comment": False,
                "can_share": False,
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    except Case.DoesNotExist:
        return Response({"error": "Case not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def submit_case_for_review(request, pk):
    """
    Submit a case for instructor review
    Changes status: DRAFT -> SUBMITTED
    """
    try:
        case = Case.objects.get(pk=pk)

        # Only the case owner can submit for review
        if case.student != request.user:
            return Response(
                {"error": "Only the case owner can submit for review"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if case.case_status == Case.StatusChoices.DRAFT:
            case.case_status = Case.StatusChoices.SUBMITTED
            case.submitted_at = timezone.now()
            case.save()
            return Response(
                {
                    "message": "Case submitted for review",
                    "case_status": case.case_status,
                    "submitted_at": case.submitted_at,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "error": f"Case must be in draft status. Current status: {case.get_case_status_display()}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    except Case.DoesNotExist:
        return Response({"error": "Case not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def review_case(request, pk):
    """
    Mark a case as reviewed by instructor
    Changes status: SUBMITTED -> REVIEWED
    Only instructors and admins can review cases
    """
    try:
        case = Case.objects.get(pk=pk)

        # Only instructors and admins can review
        if not (request.user.is_instructor or request.user.is_admin_user):
            return Response(
                {"error": "Only instructors and admins can review cases"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if case.case_status == Case.StatusChoices.SUBMITTED:
            case.case_status = Case.StatusChoices.REVIEWED
            case.reviewed_at = timezone.now()
            case.reviewed_by = request.user
            case.save()

            return Response(
                {
                    "message": "Case marked as reviewed",
                    "case_status": case.case_status,
                    "reviewed_at": case.reviewed_at,
                    "reviewed_by": request.user.get_full_name(),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "error": f"Case must be submitted for review. Current status: {case.get_case_status_display()}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    except Case.DoesNotExist:
        return Response({"error": "Case not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def approve_case(request, pk):
    """
    Approve a case (final approval)
    Changes status: REVIEWED -> APPROVED (or SUBMITTED -> APPROVED)
    Only instructors and admins can approve cases
    """
    try:
        case = Case.objects.get(pk=pk)

        # Only instructors and admins can approve
        if not (request.user.is_instructor or request.user.is_admin_user):
            return Response(
                {"error": "Only instructors and admins can approve cases"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Can approve from SUBMITTED or REVIEWED status
        if case.case_status in [
            Case.StatusChoices.SUBMITTED,
            Case.StatusChoices.REVIEWED,
        ]:
            # If coming from SUBMITTED, set reviewed fields too
            if case.case_status == Case.StatusChoices.SUBMITTED:
                case.reviewed_at = timezone.now()
                case.reviewed_by = request.user

            case.case_status = Case.StatusChoices.APPROVED
            case.save()

            return Response(
                {
                    "message": "Case approved successfully",
                    "case_status": case.case_status,
                    "reviewed_by": request.user.get_full_name(),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "error": f"Case must be submitted or reviewed to approve. Current status: {case.get_case_status_display()}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    except Case.DoesNotExist:
        return Response({"error": "Case not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def reject_case(request, pk):
    """
    Reject a case and send back to draft
    Changes status: SUBMITTED/REVIEWED -> DRAFT
    Only instructors and admins can reject cases
    Optional: include rejection reason in request body
    """
    try:
        case = Case.objects.get(pk=pk)

        # Only instructors and admins can reject
        if not (request.user.is_instructor or request.user.is_admin_user):
            return Response(
                {"error": "Only instructors and admins can reject cases"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Can reject from SUBMITTED or REVIEWED status
        if case.case_status in [
            Case.StatusChoices.SUBMITTED,
            Case.StatusChoices.REVIEWED,
        ]:
            rejection_reason = request.data.get("reason", "")

            # Return to draft status
            case.case_status = Case.StatusChoices.DRAFT
            case.reviewed_at = timezone.now()
            case.reviewed_by = request.user
            case.save()

            # Optionally add rejection reason as a comment (if you want to track this)
            response_data = {
                "message": "Case rejected and returned to draft",
                "case_status": case.case_status,
                "reviewed_by": request.user.get_full_name(),
            }

            if rejection_reason:
                response_data["rejection_reason"] = rejection_reason

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    "error": f"Case must be submitted or reviewed to reject. Current status: {case.get_case_status_display()}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    except Case.DoesNotExist:
        return Response({"error": "Case not found"}, status=status.HTTP_404_NOT_FOUND)


class MedicalAttachmentListCreateView(generics.ListCreateAPIView):
    """
    List and create medical attachments for a specific case
    """

    serializer_class = MedicalAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_queryset(self):
        user = self.request.user
        case_id = self.kwargs.get("case_pk")
        attachments = MedicalAttachment.objects.filter(case_id=case_id).select_related(
            "case", "department", "uploaded_by"
        )

        allowed = []
        for att in attachments:
            level = att.confidentiality_level

            if level == MedicalAttachment.ConfidentialityLevel.PUBLIC:
                allowed.append(att)
            elif level == MedicalAttachment.ConfidentialityLevel.CONFIDENTIAL:
                if user == att.case.student or user.is_instructor:
                    allowed.append(att)
            elif level == MedicalAttachment.ConfidentialityLevel.RESTRICTED:
                if user == att.case.student or (
                    user.is_instructor and user in att.allowed_instructors.all()
                ):
                    allowed.append(att)
            elif level == MedicalAttachment.ConfidentialityLevel.DEPARTMENT:
                if (
                    user.department
                    and att.department
                    and user.department == att.department
                ):
                    allowed.append(att)

        return allowed

    def perform_create(self, serializer):
        case_id = self.kwargs.get("case_pk")
        case = Case.objects.get(id=case_id)

        # Check permissions
        user = self.request.user
        if case.student != user and not user.is_instructor:
            raise PermissionDenied(
                "You don't have permission to upload attachments to this case"
            )

        serializer.save(case=case, uploaded_by=user)


class MedicalTermListCreateView(generics.ListCreateAPIView):
    """List and create medical terms"""

    serializer_class = MedicalTermSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = MedicalTerm.objects.filter(is_active=True)
        specialty = self.request.query_params.get("specialty")
        if specialty:
            qs = qs.filter(specialty__iexact=specialty)
        return qs.order_by("vietnamese_term", "term")


class MedicalTermRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MedicalTermSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = MedicalTerm.objects.all()


class MedicalTermAutocompleteView(generics.ListAPIView):
    """Autocomplete endpoint for medical terms with fuzzy matching and caching"""

    serializer_class = MedicalTermSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        q = request.query_params.get("q", "")
        specialty = request.query_params.get("specialty")
        limit = int(request.query_params.get("limit", 20))

        cache_key = f"term_autocomplete:{q}:{specialty}:{limit}"
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)

        # Basic exact / icontains matches first
        qs = MedicalTerm.objects.filter(is_active=True)
        if specialty:
            qs = qs.filter(specialty__iexact=specialty)

        if q.strip() == "":
            results = qs.order_by("vietnamese_term")[:limit]
            serialized = self.get_serializer(results, many=True).data
            cache.set(cache_key, serialized, 60 * 5)
            return Response(serialized)

        # Narrow by simple icontains
        icontains_qs = qs.filter(
            Q(vietnamese_term__icontains=q)
            | Q(term__icontains=q)
            | Q(english_term__icontains=q)
        )[:100]

        # Score remaining candidates using SequenceMatcher
        candidates = list(icontains_qs)
        # If too few candidates, expand search by all terms in specialty (limit 500)
        if len(candidates) < 10:
            extra_qs = qs.exclude(id__in=[c.id for c in candidates])[:500]
            candidates.extend(list(extra_qs))

        scored = []
        for term in candidates:
            name = (term.vietnamese_term or term.term or term.english_term).lower()
            score = SequenceMatcher(None, q.lower(), name).ratio()
            scored.append((score, term))

        scored.sort(key=lambda s: s[0], reverse=True)
        top = [t for _, t in scored[:limit]]
        serialized = self.get_serializer(top, many=True).data
        cache.set(cache_key, serialized, 60 * 5)
        return Response(serialized)


class ICD10ListView(generics.ListAPIView):
    serializer_class = ICD10Serializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = ICD10Code.objects.filter(is_active=True)
        q = self.request.query_params.get("q")
        code = self.request.query_params.get("code")
        if code:
            qs = qs.filter(code__istartswith=code)
        elif q:
            qs = qs.filter(
                Q(description_vi__icontains=q)
                | Q(description_en__icontains=q)
                | Q(code__icontains=q)
            )
        return qs.order_by("code")[:200]


class AbbreviationListCreateView(generics.ListCreateAPIView):
    serializer_class = AbbreviationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = MedicalAbbreviation.objects.filter(is_active=True)
        q = self.request.query_params.get("q")
        if q:
            qs = qs.filter(Q(abbr__icontains=q) | Q(expansion__icontains=q))
        return qs.order_by("abbr")


class MedicalAttachmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a medical attachment
    """

    serializer_class = MedicalAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MedicalAttachment.objects.select_related(
            "case", "department", "uploaded_by"
        )

    def get_object(self):
        attachment = super().get_object()
        user = self.request.user

        # Check permissions
        if attachment.case.student != user and not user.is_instructor:
            if attachment.is_confidential and not user.is_instructor:
                raise PermissionDenied(
                    "You don't have permission to access this confidential attachment"
                )

        return attachment


class StudentNotesListCreateView(generics.ListCreateAPIView):
    """
    List and create student notes for cases
    """

    serializer_class = StudentNotesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        case_id = self.kwargs.get("case_id")

        # Students can only see their own notes
        if user.role == "student":
            return StudentNotes.objects.filter(case_id=case_id, student=user)

        # Instructors can see all notes for a case
        return StudentNotes.objects.filter(case_id=case_id)

    def perform_create(self, serializer):
        case_id = self.kwargs.get("case_id")
        # Use update_or_create to handle both creation and updates
        # This prevents duplicate key errors when notes already exist
        student = self.request.user
        
        # Check if notes already exist for this case and student
        existing_notes = StudentNotes.objects.filter(case_id=case_id, student=student).first()
        
        if existing_notes:
            # Update existing notes
            for key, value in serializer.validated_data.items():
                setattr(existing_notes, key, value)
            existing_notes.save()
            serializer.instance = existing_notes
        else:
            # Create new notes
            serializer.save(student=student, case_id=case_id)


class StudentNotesDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete student notes
    """

    serializer_class = StudentNotesSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        user = self.request.user

        # Students can only access their own notes
        if user.role == "student":
            return StudentNotes.objects.filter(student=user)

        # Instructors can access all notes
        return StudentNotes.objects.all()

    def get_object(self):
        notes = super().get_object()
        user = self.request.user

        # Check permissions - students can only edit their own unsubmitted notes
        if user.role == "student":
            if notes.student != user:
                raise PermissionDenied(
                    "You don't have permission to access these notes"
                )
            if self.request.method in ["PUT", "PATCH", "DELETE"] and notes.is_submitted:
                raise PermissionDenied("You cannot modify submitted notes")

        return notes


class DepartmentListCreateView(generics.ListCreateAPIView):
    """
    List and create departments
    """

    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "vietnamese_name", "code"]
    ordering_fields = ["name", "code"]
    ordering = ["name"]

    def get_queryset(self):
        return Department.objects.all()

    def perform_create(self, serializer):
        # Only instructors can create departments
        if not self.request.user.is_instructor:
            raise PermissionDenied("Only instructors can create departments")
        serializer.save()


class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a department
    """

    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Department.objects.all()

    def perform_update(self, serializer):
        # Only instructors can update departments
        if not self.request.user.is_instructor:
            raise PermissionDenied("Only instructors can update departments")
        serializer.save()

    def perform_destroy(self, instance):
        # Only instructors can delete departments
        if not self.request.user.is_instructor:
            raise PermissionDenied("Only instructors can delete departments")
        instance.delete()


# =============================================================================
# ENHANCED PERMISSION MANAGEMENT SYSTEM
# =============================================================================


class CaseSharingPermission(permissions.BasePermission):
    """
    Custom permission for case sharing operations
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Case owners and instructors can manage permissions
        if hasattr(obj, "student"):  # This is a Case object
            return (
                obj.student == request.user
                or request.user.is_instructor
                or request.user.is_admin_user
            )

        # For permission objects, check if user can modify
        if hasattr(obj, "case"):  # This is a CasePermission/GuestAccess/etc
            case = obj.case
            return (
                case.student == request.user
                or request.user.is_instructor
                or request.user.is_admin_user
                or obj.granted_by == request.user
            )

        return False


class EnhancedCasePermissionViewSet(viewsets.ModelViewSet):
    """
    Enhanced ViewSet for case permissions with time-limited access and group sharing

    Endpoints:
    - GET /api/cases/{case_id}/permissions/ - List case permissions
    - POST /api/cases/{case_id}/permissions/ - Create permission
    - GET /api/cases/{case_id}/permissions/{id}/ - Get permission detail
    - PUT/PATCH /api/cases/{case_id}/permissions/{id}/ - Update permission
    - DELETE /api/cases/{case_id}/permissions/{id}/ - Remove permission
    - POST /api/cases/{case_id}/permissions/bulk_grant/ - Bulk grant permissions
    - POST /api/cases/{case_id}/permissions/bulk_revoke/ - Bulk revoke permissions
    - GET /api/cases/{case_id}/permissions/audit_log/ - Get audit log
    """

    serializer_class = CasePermissionSerializer
    permission_classes = [CaseSharingPermission]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["share_type", "permission_type", "is_active"]
    search_fields = [
        "user__email",
        "user__first_name",
        "user__last_name",
        "class_group",
    ]
    ordering_fields = ["granted_at", "expires_at", "access_count"]
    ordering = ["-granted_at"]

    def get_queryset(self):
        case_id = self.kwargs.get("case_pk")
        case = get_object_or_404(Case, id=case_id)

        # Check if user has permission to view case permissions
        if not (
            case.student == self.request.user
            or self.request.user.is_instructor
            or self.request.user.is_admin_user
        ):
            raise PermissionDenied(
                "Bạn không có quyền xem danh sách chia sẻ của ca bệnh này"
            )

        return CasePermission.objects.filter(case_id=case_id).select_related(
            "user", "granted_by", "target_department"
        )

    def perform_create(self, serializer):
        case_id = self.kwargs.get("case_pk")
        case = get_object_or_404(Case, id=case_id)

        permission = serializer.save(case=case, granted_by=self.request.user)

        # Log the permission grant
        PermissionAuditLog.log_permission_change(
            case=case,
            target_user=permission.user,
            actor_user=self.request.user,
            action=PermissionAuditLog.ActionChoices.GRANTED,
            permission_type=permission.permission_type,
            description=f"Granted {permission.get_permission_type_display()} permission via {permission.get_share_type_display()}",
            request=self.request,
            additional_data={"permission_id": permission.id},
        )

    def perform_update(self, serializer):
        original_permission = self.get_object()
        updated_permission = serializer.save()

        # Log the permission modification
        PermissionAuditLog.log_permission_change(
            case=updated_permission.case,
            target_user=updated_permission.user,
            actor_user=self.request.user,
            action=PermissionAuditLog.ActionChoices.MODIFIED,
            permission_type=updated_permission.permission_type,
            description=f"Modified permission from {original_permission.get_permission_type_display()} to {updated_permission.get_permission_type_display()}",
            request=self.request,
            additional_data={
                "permission_id": updated_permission.id,
                "original_type": original_permission.permission_type,
                "new_type": updated_permission.permission_type,
            },
        )

    def perform_destroy(self, instance):
        # Log the permission revocation
        PermissionAuditLog.log_permission_change(
            case=instance.case,
            target_user=instance.user,
            actor_user=self.request.user,
            action=PermissionAuditLog.ActionChoices.REVOKED,
            permission_type=instance.permission_type,
            description=f"Revoked {instance.get_permission_type_display()} permission",
            request=self.request,
            additional_data={"permission_id": instance.id},
        )

        instance.delete()

    @action(detail=False, methods=["post"])
    def bulk_grant(self, request, case_pk=None):
        """
        Bulk grant permissions to multiple users/groups for a single case

        Body example:
        {
            "share_type": "individual",
            "users_ids": [1, 2, 3],
            "permission_type": "view",
            "expires_hours": 72,
            "notes": "Assignment access"
        }
        """
        case = get_object_or_404(Case, id=case_pk)

        # Simple validation instead of using BulkPermissionSerializer
        data = request.data
        share_type = data.get("share_type", "individual")
        permission_type = data.get("permission_type", "view")
        expires_hours = data.get("expires_hours")
        notes = data.get("notes", "")

        if share_type not in dict(CasePermission.ShareTypeChoices.choices):
            return Response(
                {"error": "Invalid share_type"}, status=status.HTTP_400_BAD_REQUEST
            )

        if permission_type not in dict(CasePermission.PermissionChoices.choices):
            return Response(
                {"error": "Invalid permission_type"}, status=status.HTTP_400_BAD_REQUEST
            )

        created_permissions = []
        expires_at = None

        if expires_hours:
            expires_at = timezone.now() + timedelta(hours=expires_hours)

        # Individual sharing
        if share_type == CasePermission.ShareTypeChoices.INDIVIDUAL:
            users_ids = data.get("users_ids", [])
            if not users_ids:
                return Response(
                    {"error": "users_ids is required for individual sharing"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            for user_id in users_ids:
                # Skip if user is the case owner
                if case.student.id == user_id:
                    continue

                permission, created = CasePermission.objects.get_or_create(
                    case=case,
                    user_id=user_id,
                    defaults={
                        "permission_type": permission_type,
                        "granted_by": request.user,
                        "share_type": share_type,
                        "expires_at": expires_at,
                        "notes": notes,
                    },
                )
                if created:
                    created_permissions.append(permission)

        # Department sharing
        elif share_type == CasePermission.ShareTypeChoices.DEPARTMENT:
            department_id = data.get("department_id")
            if not department_id:
                return Response(
                    {"error": "department_id is required for department sharing"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            permission, created = CasePermission.objects.get_or_create(
                case=case,
                target_department_id=department_id,
                share_type=share_type,
                defaults={
                    "permission_type": permission_type,
                    "granted_by": request.user,
                    "expires_at": expires_at,
                    "notes": notes,
                },
            )
            if created:
                created_permissions.append(permission)

        # Class group sharing
        elif share_type == CasePermission.ShareTypeChoices.CLASS_GROUP:
            class_group = data["class_group"]
            permission, created = CasePermission.objects.get_or_create(
                case=case,
                class_group=class_group,
                share_type=share_type,
                defaults={
                    "permission_type": permission_type,
                    "granted_by": request.user,
                    "expires_at": expires_at,
                    "notes": notes,
                },
            )
            if created:
                created_permissions.append(permission)

        # Log bulk grant operation
        PermissionAuditLog.log_permission_change(
            case=case,
            target_user=None,
            actor_user=request.user,
            action=PermissionAuditLog.ActionChoices.GRANTED,
            permission_type=permission_type,
            description=f"Bulk granted {len(created_permissions)} permissions via {share_type}",
            request=request,
            additional_data={
                "permissions_count": len(created_permissions),
                "share_type": share_type,
                "expires_hours": expires_hours,
            },
        )

        return Response(
            {
                "message": f"Successfully granted {len(created_permissions)} permissions",
                "created_count": len(created_permissions),
                "permissions": CasePermissionSerializer(
                    created_permissions, many=True
                ).data,
            }
        )

    @action(detail=False, methods=["post"])
    def bulk_revoke(self, request, case_pk=None):
        """
        Bulk revoke permissions

        Body example:
        {
            "permission_ids": [1, 2, 3]
        }
        """
        case = get_object_or_404(Case, id=case_pk)
        permission_ids = request.data.get("permission_ids", [])

        if not permission_ids:
            return Response(
                {"error": "permission_ids is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        permissions_to_delete = CasePermission.objects.filter(
            id__in=permission_ids, case=case
        )

        deleted_count = permissions_to_delete.count()
        permissions_to_delete.delete()

        # Log bulk revoke operation
        PermissionAuditLog.log_permission_change(
            case=case,
            target_user=None,
            actor_user=request.user,
            action=PermissionAuditLog.ActionChoices.REVOKED,
            description=f"Bulk revoked {deleted_count} permissions",
            request=request,
            additional_data={
                "permissions_count": deleted_count,
                "permission_ids": permission_ids,
            },
        )

        return Response(
            {
                "message": f"Successfully revoked {deleted_count} permissions",
                "revoked_count": deleted_count,
            }
        )

    @action(detail=False, methods=["get"])
    def audit_log(self, request, case_pk=None):
        """Get permission audit log for a case"""
        case = get_object_or_404(Case, id=case_pk)

        logs = PermissionAuditLog.objects.filter(case=case).select_related(
            "target_user", "actor_user"
        )[:50]  # Limit to recent 50 entries

        serializer = PermissionAuditLogSerializer(logs, many=True)
        return Response(serializer.data)


class GuestAccessViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing guest access to cases

    Endpoints:
    - GET /api/cases/{case_id}/guest-access/ - List guest accesses
    - POST /api/cases/{case_id}/guest-access/ - Create guest access
    - GET /api/cases/{case_id}/guest-access/{id}/ - Get guest access detail
    - PUT/PATCH /api/cases/{case_id}/guest-access/{id}/ - Update guest access
    - DELETE /api/cases/{case_id}/guest-access/{id}/ - Remove guest access
    - POST /api/cases/{case_id}/guest-access/{id}/extend/ - Extend expiration
    """

    serializer_class = GuestAccessSerializer
    permission_classes = [CaseSharingPermission]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["is_active", "permission_type"]
    ordering_fields = ["created_at", "expires_at", "access_count"]
    ordering = ["-created_at"]

    def get_queryset(self):
        case_id = self.kwargs.get("case_pk")
        case = get_object_or_404(Case, id=case_id)

        # Check permissions
        if not (
            case.student == self.request.user
            or self.request.user.is_instructor
            or self.request.user.is_admin_user
        ):
            raise PermissionDenied(
                "Bạn không có quyền xem guest access của ca bệnh này"
            )

        return GuestAccess.objects.filter(case_id=case_id)

    def perform_create(self, serializer):
        case_id = self.kwargs.get("case_pk")
        case = get_object_or_404(Case, id=case_id)

        guest_access = serializer.save(case=case, created_by=self.request.user)

        # Log guest access creation
        PermissionAuditLog.log_permission_change(
            case=case,
            target_user=None,
            actor_user=self.request.user,
            action=PermissionAuditLog.ActionChoices.GRANTED,
            permission_type=guest_access.permission_type,
            description=f"Created guest access for {guest_access.guest_email}",
            request=self.request,
            additional_data={
                "guest_email": guest_access.guest_email,
                "access_token": guest_access.access_token[:10]
                + "...",  # Partial token for security
                "expires_at": guest_access.expires_at.isoformat(),
            },
        )

    @action(detail=True, methods=["post"])
    def extend(self, request, case_pk=None, pk=None):
        """
        Extend guest access expiration

        Body example:
        {
            "additional_hours": 24
        }
        """
        guest_access = self.get_object()
        additional_hours = request.data.get("additional_hours", 24)

        if additional_hours <= 0 or additional_hours > 168:  # Max 1 week
            return Response(
                {"error": "additional_hours must be between 1 and 168"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Extend expiration
        original_expires = guest_access.expires_at
        guest_access.expires_at = max(timezone.now(), original_expires) + timedelta(
            hours=additional_hours
        )
        guest_access.save(update_fields=["expires_at"])

        # Log the extension
        PermissionAuditLog.log_permission_change(
            case=guest_access.case,
            target_user=None,
            actor_user=request.user,
            action=PermissionAuditLog.ActionChoices.MODIFIED,
            description=f"Extended guest access for {guest_access.guest_email} by {additional_hours} hours",
            request=request,
            additional_data={
                "guest_email": guest_access.guest_email,
                "original_expires": original_expires.isoformat(),
                "new_expires": guest_access.expires_at.isoformat(),
                "additional_hours": additional_hours,
            },
        )

        serializer = self.get_serializer(guest_access)
        return Response(serializer.data)


class CaseGroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet for case groups and bulk permission management

    Endpoints:
    - GET /api/case-groups/ - List case groups
    - POST /api/case-groups/ - Create case group
    - GET /api/case-groups/{id}/ - Get case group detail
    - PUT/PATCH /api/case-groups/{id}/ - Update case group
    - DELETE /api/case-groups/{id}/ - Remove case group
    - POST /api/case-groups/{id}/grant_permissions/ - Grant permissions to group members
    - POST /api/case-groups/{id}/add_cases/ - Add cases to group
    - POST /api/case-groups/{id}/remove_cases/ - Remove cases from group
    """

    serializer_class = CaseGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["group_type", "department", "is_active", "is_public"]
    search_fields = ["name", "description", "class_identifier"]
    ordering_fields = ["created_at", "updated_at", "name"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        queryset = CaseGroup.objects.select_related("created_by", "department")

        # Filter based on user role and access
        if user.is_admin_user:
            return queryset.all()
        elif user.is_instructor:
            # Instructors can see their own groups and public ones in their department
            return queryset.filter(
                Q(created_by=user)
                | Q(is_public=True, department=user.department)
                | Q(is_public=True, department=None)
            )
        else:
            # Students can only see public groups they have access to
            return queryset.filter(
                Q(is_public=True) | Q(department=user.department, is_public=True)
            )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"], url_path="grant-permissions")
    def grant_permissions(self, request, pk=None):
        """
        Grant permissions for all cases in group to specified users/groups

        Body example:
        {
            "target_users": [1, 2, 3],
            "permission_type": "view",
            "expires_hours": 72
        }
        """
        case_group = self.get_object()
        target_users = request.data.get("target_users", [])
        permission_type = request.data.get("permission_type", "view")
        expires_hours = request.data.get("expires_hours")

        if not target_users:
            return Response(
                {"error": "target_users is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get users
        from accounts.models import User

        users = User.objects.filter(id__in=target_users)

        if len(users) != len(target_users):
            return Response(
                {"error": "Some user IDs are invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Grant permissions using the case group method
        created_count = case_group.add_bulk_permissions(
            users=users, permission_type=permission_type
        )

        # If expiration is set, update the permissions
        if expires_hours:
            expires_at = timezone.now() + timedelta(hours=expires_hours)
            CasePermission.objects.filter(
                case__in=case_group.cases.all(), user__in=users, granted_by=request.user
            ).update(expires_at=expires_at)

        return Response(
            {
                "message": f"Successfully granted permissions to {len(users)} users for {case_group.cases.count()} cases",
                "users_count": len(users),
                "cases_count": case_group.cases.count(),
                "created_permissions": created_count,
            }
        )

    @action(detail=True, methods=["post"])
    def add_cases(self, request, pk=None):
        """
        Add cases to the group

        Body example:
        {
            "case_ids": [1, 2, 3]
        }
        """
        case_group = self.get_object()
        case_ids = request.data.get("case_ids", [])

        if not case_ids:
            return Response(
                {"error": "case_ids is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        cases_to_add = Case.objects.filter(id__in=case_ids)
        added_count = cases_to_add.count()

        case_group.cases.add(*cases_to_add)

        return Response(
            {
                "message": f"Successfully added {added_count} cases to the group",
                "added_count": added_count,
            }
        )

    @action(detail=True, methods=["post"])
    def remove_cases(self, request, pk=None):
        """
        Remove cases from the group

        Body example:
        {
            "case_ids": [1, 2, 3]
        }
        """
        case_group = self.get_object()
        case_ids = request.data.get("case_ids", [])

        if not case_ids:
            return Response(
                {"error": "case_ids is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        cases_to_remove = Case.objects.filter(id__in=case_ids)
        removed_count = cases_to_remove.count()

        case_group.cases.remove(*cases_to_remove)

        return Response(
            {
                "message": f"Successfully removed {removed_count} cases from the group",
                "removed_count": removed_count,
            }
        )


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def guest_access_case(request, access_token):
    """
    Access case via guest token

    GET /api/guest-access/{access_token}/
    """
    try:
        guest_access = GuestAccess.objects.select_related("case", "created_by").get(
            access_token=access_token, is_active=True
        )

        # Check if expired
        if guest_access.is_expired:
            return Response(
                {"error": "Guest access has expired"}, status=status.HTTP_403_FORBIDDEN
            )

        # Update access tracking
        ip_address = request.META.get(
            "HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR")
        )
        guest_access.update_access(ip_address)

        # Log the access
        PermissionAuditLog.log_permission_change(
            case=guest_access.case,
            target_user=None,
            actor_user=None,
            action=PermissionAuditLog.ActionChoices.ACCESSED,
            description=f"Guest access by {guest_access.guest_email}",
            request=request,
            additional_data={
                "guest_email": guest_access.guest_email,
                "access_token": access_token[:10] + "...",
                "permission_type": guest_access.permission_type,
            },
        )

        # Return case data based on permission level
        case = guest_access.case

        if guest_access.permission_type in ["view", "comment", "analyze"]:
            from .serializers import CaseDetailSerializer

            case_data = CaseDetailSerializer(case).data

            # Remove sensitive fields for guests
            restricted_fields = ["student", "medical_record_number"]
            for field in restricted_fields:
                case_data.pop(field, None)

            return Response(
                {
                    "case": case_data,
                    "guest_access": {
                        "permission_type": guest_access.permission_type,
                        "guest_name": guest_access.guest_name,
                        "expires_at": guest_access.expires_at,
                        "access_count": guest_access.access_count,
                    },
                }
            )

        return Response(
            {"error": "Insufficient permissions"}, status=status.HTTP_403_FORBIDDEN
        )

    except GuestAccess.DoesNotExist:
        return Response(
            {"error": "Invalid or inactive guest access token"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def my_shared_cases(request):
    """
    Get cases shared with the current user

    GET /api/my-shared-cases/
    """
    user = request.user

    # Get cases shared directly with user
    direct_permissions = (
        CasePermission.objects.filter(user=user, is_active=True)
        .exclude(case__student=user)  # Exclude own cases
        .select_related("case", "granted_by")
    )

    # Filter out expired permissions
    valid_permissions = [p for p in direct_permissions if not p.is_expired]

    # Get cases shared with user's department
    department_permissions = []
    if user.department:
        dept_permissions = CasePermission.objects.filter(
            target_department=user.department,
            share_type=CasePermission.ShareTypeChoices.DEPARTMENT,
            is_active=True,
        ).select_related("case", "granted_by")

        department_permissions = [p for p in dept_permissions if not p.is_expired]

    # Get public cases (limit to 20 for performance)
    public_permissions = CasePermission.objects.filter(
        share_type=CasePermission.ShareTypeChoices.PUBLIC, is_active=True
    ).select_related("case", "granted_by")[:20]

    # Combine and serialize
    all_permissions = (
        valid_permissions + department_permissions + list(public_permissions)
    )

    # Remove duplicates by case ID
    seen_cases = set()
    unique_permissions = []
    for perm in all_permissions:
        if perm.case.id not in seen_cases:
            seen_cases.add(perm.case.id)
            unique_permissions.append(perm)

    serializer = CasePermissionSerializer(unique_permissions, many=True)

    return Response(
        {
            "shared_cases": serializer.data,
            "total_count": len(unique_permissions),
            "direct_count": len(valid_permissions),
            "department_count": len(department_permissions),
            "public_count": len(list(public_permissions)),
        }
    )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def accessible_cases(request):
    """
    Get all cases accessible to the current user (own + shared + department + public)

    GET /api/accessible-cases/
    """
    user = request.user

    # Get user's own cases
    own_cases = Case.objects.filter(student=user)

    # Get cases shared directly with user
    direct_permissions = CasePermission.objects.filter(
        user=user, is_active=True
    ).select_related("case")

    # Get cases shared with user's department
    department_permissions = []
    if user.department:
        department_permissions = CasePermission.objects.filter(
            target_department=user.department,
            share_type=CasePermission.ShareTypeChoices.DEPARTMENT,
            is_active=True,
        ).select_related("case")

    # Get public cases
    public_permissions = CasePermission.objects.filter(
        share_type=CasePermission.ShareTypeChoices.PUBLIC, is_active=True
    ).select_related("case")

    # Collect all accessible case IDs
    accessible_case_ids = set()

    # Add own cases
    for case in own_cases:
        accessible_case_ids.add(case.id)

    # Add shared cases (filter expired)
    for perm in direct_permissions:
        if not perm.is_expired:
            accessible_case_ids.add(perm.case.id)

    for perm in department_permissions:
        if not perm.is_expired:
            accessible_case_ids.add(perm.case.id)

    for perm in public_permissions:
        if not perm.is_expired:
            accessible_case_ids.add(perm.case.id)

    # Get all accessible cases
    accessible_cases = Case.objects.filter(id__in=accessible_case_ids).select_related(
        "student", "department"
    )

    # Serialize cases
    from .serializers import CaseSerializer

    serializer = CaseSerializer(accessible_cases, many=True)

    return Response(
        {"accessible_cases": serializer.data, "total_count": len(accessible_cases)}
    )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def cleanup_expired_permissions(request):
    """
    Cleanup expired permissions and guest accesses (Admin/Instructor only)

    POST /api/cleanup-expired-permissions/
    """
    user = request.user

    if not (user.is_instructor or user.is_admin_user):
        raise PermissionDenied(
            "Only instructors and admins can cleanup expired permissions"
        )

    # Cleanup expired permissions
    expired_permissions = CasePermission.objects.filter(
        expires_at__lte=timezone.now(), is_active=True
    )

    permissions_count = expired_permissions.count()

    # Log each expired permission
    for permission in expired_permissions:
        PermissionAuditLog.log_permission_change(
            case=permission.case,
            target_user=permission.user,
            actor_user=user,
            action=PermissionAuditLog.ActionChoices.EXPIRED,
            permission_type=permission.permission_type,
            description="Permission expired - cleaned up by system",
            request=request,
        )

    # Mark as inactive instead of deleting for audit trail
    expired_permissions.update(is_active=False)

    # Cleanup expired guest accesses
    expired_guests = GuestAccess.objects.filter(
        expires_at__lte=timezone.now(), is_active=True
    )

    guests_count = expired_guests.count()
    expired_guests.update(is_active=False)

    return Response(
        {
            "message": "Successfully cleaned up expired access",
            "expired_permissions": permissions_count,
            "expired_guest_accesses": guests_count,
        }
    )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def case_summary_view(request):
    """
    Comprehensive case summary endpoint
    GET /api/cases/summary/
    Returns statistics and analytics for all cases
    """
    user: User = request.user  # type: ignore
    
    # Get all cases accessible to user
    if user.role == "instructor":
        # Instructors see all cases
        cases = Case.objects.all()
    else:
        # Students see their own cases and shared cases
        cases = Case.objects.filter(
            Q(student=user) | 
            Q(permissions__user=user, permissions__is_active=True) |
            Q(permissions__share_type=CasePermission.ShareTypeChoices.PUBLIC, permissions__is_active=True)
        ).distinct()
    
    # Total cases
    total_cases = cases.count()
    
    # Cases by status
    by_status = {}
    for status_choice in Case.StatusChoices.choices:
        status_value = status_choice[0]
        count = cases.filter(case_status=status_value).count()
        by_status[status_value] = {
            "count": count,
            "label": status_choice[1],
            "percentage": round((count / total_cases * 100) if total_cases > 0 else 0, 1)
        }
    
    # Cases by specialty
    specialty_data = cases.values('specialty').annotate(count=Count('id')).order_by('-count')
    by_specialty = {
        item['specialty']: item['count'] 
        for item in specialty_data if item['specialty']
    }
    
    # Cases by priority
    priority_data = cases.values('priority_level').annotate(count=Count('id'))
    by_priority = {
        item['priority_level']: item['count'] 
        for item in priority_data if item['priority_level']
    }
    
    # Cases by complexity
    complexity_data = cases.values('complexity_level').annotate(count=Count('id'))
    by_complexity = {
        item['complexity_level']: item['count'] 
        for item in complexity_data if item['complexity_level']
    }
    
    # Completion statistics
    completion_stats = {
        "total_submitted": cases.filter(case_status__in=['submitted', 'reviewed', 'approved']).count(),
        "total_drafts": cases.filter(case_status='draft').count(),
        "completion_rate": round(
            (cases.filter(case_status__in=['submitted', 'reviewed', 'approved']).count() / total_cases * 100)
            if total_cases > 0 else 0, 1
        ),
        "approval_rate": round(
            (cases.filter(case_status='approved').count() / total_cases * 100)
            if total_cases > 0 else 0, 1
        )
    }
    
    # Recent cases (last 10)
    recent_cases = cases.order_by('-created_at')[:10]
    recent_cases_data = CaseListSerializer(recent_cases, many=True, context={'request': request}).data
    
    # Top specialties (top 5)
    top_specialties = [
        {"specialty": item['specialty'], "count": item['count']}
        for item in specialty_data[:5]
    ]
    
    # Learning metrics
    total_study_hours = sum([case.estimated_study_hours or 0 for case in cases])
    avg_study_hours = round(total_study_hours / total_cases, 1) if total_cases > 0 else 0
    
    # Count cases with learning outcomes (using filter instead of exclude)
    cases_with_outcomes = 0
    try:
        from .medical_models import LearningOutcomes
        cases_with_outcomes = LearningOutcomes.objects.filter(case__in=cases).count()
    except Exception:
        pass
    
    learning_metrics = {
        "total_study_hours": total_study_hours,
        "average_study_hours_per_case": avg_study_hours,
        "total_cases_with_learning_outcomes": cases_with_outcomes,
        "cases_created_this_month": cases.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count(),
        "cases_created_this_week": cases.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count()
    }
    
    # Prepare summary data
    summary_data = {
        "total_cases": total_cases,
        "by_status": by_status,
        "by_specialty": by_specialty,
        "by_priority": by_priority,
        "by_complexity": by_complexity,
        "completion_stats": completion_stats,
        "recent_cases": recent_cases_data,
        "top_specialties": top_specialties,
        "learning_metrics": learning_metrics
    }
    
    serializer = CaseSummarySerializer(summary_data)
    return Response(serializer.data)
