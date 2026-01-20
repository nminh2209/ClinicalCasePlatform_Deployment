# cases/specialty_views.py
"""
API views for Specialty and related models
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from .specialty_models import Specialty, CasePriorityLevel, CaseComplexityLevel
from .specialty_serializers import (
    SpecialtyListSerializer,
    SpecialtyDetailSerializer,
    SpecialtyCreateUpdateSerializer,
    CasePriorityLevelSerializer,
    CaseComplexityLevelSerializer,
)
from .permissions import IsInstructorPermission


class SpecialtyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing specialties

    Endpoints:
    - GET /api/specialties/ - List all active specialties
    - GET /api/specialties/{id}/ - Get specialty details
    - POST /api/specialties/ - Create new specialty (instructor only)
    - PUT /api/specialties/{id}/ - Update specialty (instructor only)
    - DELETE /api/specialties/{id}/ - Delete specialty (instructor only)
    """

    queryset = Specialty.objects.select_related("department")
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["department", "is_active"]
    search_fields = ["name", "english_name", "description"]
    ordering_fields = ["display_order", "name", "created_at"]
    ordering = ["display_order", "name"]

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action
        """
        if self.action == "list":
            return SpecialtyListSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return SpecialtyCreateUpdateSerializer
        return SpecialtyDetailSerializer

    def get_queryset(self):
        """
        Filter queryset based on user permissions
        """
        queryset = super().get_queryset()

        # Students only see active specialties
        if not self.request.user.is_instructor:
            queryset = queryset.filter(is_active=True)

        return queryset

    def get_permissions(self):
        """
        Instructors can create/update/delete, students can only view
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsInstructorPermission()]
        return [IsAuthenticated()]

    @action(detail=False, methods=["get"])
    def by_department(self, request):
        """
        Get specialties grouped by department

        GET /api/specialties/by_department/

        Returns:
        {
            "departments": [
                {
                    "id": 1,
                    "name": "Khoa Nội",
                    "specialties": [...]
                }
            ]
        }
        """
        from cases.medical_models import Department
        from cases.serializers import DepartmentSerializer

        departments = Department.objects.prefetch_related("specialties").filter(
            is_active=True
        )

        result = []
        for dept in departments:
            specialties = dept.specialties.filter(is_active=True).annotate(
                template_count=Count("templates")
            )
            dept_data = DepartmentSerializer(dept).data
            dept_data["specialties"] = SpecialtyListSerializer(
                specialties, many=True
            ).data
            result.append(dept_data)

        return Response({"departments": result})

    @action(detail=False, methods=["get"])
    def all_choices(self, request):
        """
        Get all active specialties as simple choice list

        GET /api/cases/specialties/all_choices/

        Returns:
        [
            {"id": 1, "name": "Tim Mạch", "department": "Khoa Nội"},
            ...
        ]
        """
        # Don't use get_queryset() to avoid any annotations
        specialties = Specialty.objects.select_related("department")

        # Filter by active status for students
        if not request.user.is_instructor:
            specialties = specialties.filter(is_active=True)

        result = [
            {
                "id": spec.id,
                "name": spec.name,
                "english_name": spec.english_name,
                "department": spec.department.name if spec.department else None,
                "department_id": spec.department.id if spec.department else None,
            }
            for spec in specialties
        ]

        return Response(result)


class CasePriorityLevelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for case priority levels (read-only)
    """

    queryset = CasePriorityLevel.objects.filter(is_active=True).order_by(
        "display_order"
    )
    serializer_class = CasePriorityLevelSerializer
    permission_classes = [IsAuthenticated]


class CaseComplexityLevelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for case complexity levels (read-only)
    """

    queryset = CaseComplexityLevel.objects.filter(is_active=True).order_by(
        "display_order"
    )
    serializer_class = CaseComplexityLevelSerializer
    permission_classes = [IsAuthenticated]
