from rest_framework import serializers
from .models import Repository


class RepositorySerializer(serializers.ModelSerializer):
    """
    Full serializer for Repository model
    """

    owner_name = serializers.CharField(source="owner.get_full_name", read_only=True)
    owner_email = serializers.CharField(source="owner.email", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)
    department_vietnamese_name = serializers.CharField(
        source="department.vietnamese_name", read_only=True
    )
    case_count = serializers.IntegerField(read_only=True)

    class Meta:  # type: ignore[misc, assignment]
        model = Repository
        fields = [
            "id",
            "name",
            "vietnamese_name",
            "description",
            "owner",
            "owner_name",
            "owner_email",
            "department",
            "department_name",
            "department_vietnamese_name",
            "is_public",
            "access_level",
            "case_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["owner", "created_at", "updated_at"]

    def validate_access_level(self, value):
        """
        Validate access level matches is_public setting
        """
        if value == "public" and not self.initial_data.get("is_public", False):
            raise serializers.ValidationError(
                "Public access level requires is_public to be True"
            )
        return value


class RepositoryListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing repositories
    """

    owner_name = serializers.CharField(source="owner.get_full_name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)
    case_count = serializers.IntegerField(read_only=True)

    class Meta:  # type: ignore[misc, assignment]
        model = Repository
        fields = [
            "id",
            "name",
            "vietnamese_name",
            "owner_name",
            "department_name",
            "access_level",
            "is_public",
            "case_count",
            "created_at",
        ]
