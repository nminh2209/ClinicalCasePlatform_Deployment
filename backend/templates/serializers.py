from rest_framework import serializers
from .models import CaseTemplate
from accounts.serializers import UserSerializer


class CaseTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer for CaseTemplate model
    """

    created_by_name = serializers.CharField(
        source="created_by.get_full_name", read_only=True
    )
    department_name = serializers.CharField(source="department.name", read_only=True)
    department_vietnamese_name = serializers.CharField(
        source="department.vietnamese_name", read_only=True
    )

    class Meta:  # type: ignore[misc, assignment]
        model = CaseTemplate
        fields = [
            "id",
            "name",
            "vietnamese_name",
            "description",
            "fields_schema",
            "created_by",
            "created_by_name",
            "department",
            "department_name",
            "department_vietnamese_name",
            "is_standard",
            "specialty",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_by", "created_at", "updated_at"]

    def validate_fields_schema(self, value):
        """
        Validate that fields_schema is a valid JSON structure
        """
        if not isinstance(value, dict):
            raise serializers.ValidationError(
                "fields_schema must be a valid JSON object"
            )

        # Optionally validate schema structure
        if "sections" not in value:
            raise serializers.ValidationError(
                "fields_schema must contain a 'sections' key"
            )

        return value


class CaseTemplateListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing templates
    """

    created_by_name = serializers.CharField(
        source="created_by.get_full_name", read_only=True
    )
    department_name = serializers.CharField(source="department.name", read_only=True)
    department_vietnamese_name = serializers.CharField(
        source="department.vietnamese_name", read_only=True
    )

    class Meta:  # type: ignore[misc, assignment]
        model = CaseTemplate
        fields = [
            "id",
            "name",
            "vietnamese_name",
            "description",
            "fields_schema",
            "specialty",
            "created_by_name",
            "department_name",
            "department_vietnamese_name",
            "is_standard",
            "is_active",
            "created_at",
        ]
