from rest_framework import serializers  # type: ignore[reportMissingTypeStubs]
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User
from typing import Any, Dict


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "role",
            "password",
            "password_confirm",
        ]

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data: Dict[str, Any]) -> User:
        # Remove password_confirm before creating the user
        validated_data.pop("password_confirm", None)
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled")
            attrs["user"] = user
            return attrs
        else:
            raise serializers.ValidationError("Must include email and password")


class UserProfileSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)
    department_vietnamese_name = serializers.CharField(source="department.vietnamese_name", read_only=True)
    
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "role",
            "department",
            "department_name",
            "department_vietnamese_name",
            "specialization",
            "student_id",
            "employee_id",
            "created_at",
        ]
        read_only_fields = ["id", "email", "created_at"]


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)
    department_vietnamese_name = serializers.CharField(source="department.vietnamese_name", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "department",
            "department_name",
            "department_vietnamese_name",
            "specialization",
            "student_id",
            "employee_id",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
