# cases/specialty_serializers.py
"""
Serializers for Specialty and related models
"""

from rest_framework import serializers
from .specialty_models import Specialty, CasePriorityLevel, CaseComplexityLevel
from .medical_models import Department


class SpecialtyListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing specialties
    """

    department_name = serializers.CharField(source="department.name", read_only=True)
    department_vietnamese_name = serializers.CharField(
        source="department.vietnamese_name", read_only=True
    )

    class Meta:  # type: ignore[misc, assignment]
        model = Specialty
        fields = [
            "id",
            "name",
            "english_name",
            "department",
            "department_name",
            "department_vietnamese_name",
            "icon",
            "color",
            "is_active",
            "display_order",
        ]


class SpecialtyDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for specialty with full information
    """

    department_name = serializers.CharField(source="department.name", read_only=True)
    department_vietnamese_name = serializers.CharField(
        source="department.vietnamese_name", read_only=True
    )

    class Meta:  # type: ignore[misc, assignment]
        model = Specialty
        fields = [
            "id",
            "name",
            "english_name",
            "description",
            "department",
            "department_name",
            "department_vietnamese_name",
            "icon",
            "color",
            "is_active",
            "display_order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class SpecialtyCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating specialties
    """

    class Meta:  # type: ignore[misc, assignment]
        model = Specialty
        fields = [
            "name",
            "english_name",
            "description",
            "department",
            "icon",
            "color",
            "is_active",
            "display_order",
        ]

    def validate_name(self, value):
        """Ensure specialty name is unique within department"""
        department = self.initial_data.get("department")
        instance = self.instance

        # Check for duplicates
        query = Specialty.objects.filter(name=value, department=department)
        if instance:
            query = query.exclude(pk=instance.pk)

        if query.exists():
            raise serializers.ValidationError(
                "A specialty with this name already exists in this department."
            )

        return value


class CasePriorityLevelSerializer(serializers.ModelSerializer):
    """
    Serializer for case priority levels
    """

    class Meta:  # type: ignore[misc, assignment]
        model = CasePriorityLevel
        fields = [
            "id",
            "name",
            "key",
            "color",
            "is_active",
            "display_order",
        ]


class CaseComplexityLevelSerializer(serializers.ModelSerializer):
    """
    Serializer for case complexity levels
    """

    class Meta:  # type: ignore[misc, assignment]
        model = CaseComplexityLevel
        fields = [
            "id",
            "name",
            "key",
            "description",
            "is_active",
            "display_order",
        ]
