# accounts/serializers.py

from typing import Any, Dict

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers  # type: ignore[reportMissingTypeStubs]

from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:  # type: ignore[misc, assignment]
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
    department_vietnamese_name = serializers.CharField(
        source="department.vietnamese_name", read_only=True
    )

    class Meta:  # type: ignore[misc, assignment]
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
    department_vietnamese_name = serializers.CharField(
        source="department.vietnamese_name", read_only=True
    )

    class Meta:  # type: ignore[misc, assignment]
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


class AdminUserSerializer(serializers.ModelSerializer):
    """
    Admin-only serializer for full user CRUD operations.
    Includes password setting and all user fields.
    """
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    department_name = serializers.CharField(source="department.name", read_only=True)
    department_vietnamese_name = serializers.CharField(
        source="department.vietnamese_name", read_only=True
    )
    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:  # type: ignore[misc, assignment]
        model = User
        fields = [
            "id",
            "email",
            "username",
            "password",
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
            "is_active",
            "is_staff",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data: Dict[str, Any]) -> User:
        """Create user with hashed password"""
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            # Set a random password if none provided
            user.set_password(User.objects.make_random_password())
        user.save()
        return user

    def update(self, instance: User, validated_data: Dict[str, Any]) -> User:
        """Update user, hash password if provided"""
        password = validated_data.pop('password', None)
        
        # Update all other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update password if provided
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer for requesting password reset"""
    email = serializers.EmailField()

    def validate_email(self, value: str) -> str:
        """Check if email exists"""
        try:
            User.objects.get(email=value, is_active=True)
        except User.DoesNotExist:
            # For security, don't reveal if email exists
            # Still return success but don't send email
            pass
        return value

    def save(self) -> Dict[str, str]:
        """Send password reset email"""
        email = self.validated_data["email"]
        
        try:
            user = User.objects.get(email=email, is_active=True)
            
            # Generate token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Create reset link
            reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            
            # Send email
            subject = "Đặt lại mật khẩu - Clinical Case Platform"
            message = f"""
Xin chào {user.get_full_name()},

Bạn đã yêu cầu đặt lại mật khẩu cho tài khoản của mình.

Vui lòng nhấp vào liên kết dưới đây để đặt lại mật khẩu:
{reset_link}

Liên kết này sẽ hết hạn sau 24 giờ.

Nếu bạn không yêu cầu đặt lại mật khẩu, vui lòng bỏ qua email này.

Trân trọng,
Clinical Case Platform Team
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        except User.DoesNotExist:
            # For security, don't reveal if email doesn't exist
            pass
        
        return {"detail": "If the email exists, a password reset link has been sent."}


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for confirming password reset"""
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """Validate passwords match and token is valid"""
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError({"new_password_confirm": "Passwords don't match"})
        
        # Decode uid and validate token
        try:
            uid = force_str(urlsafe_base64_decode(attrs["uid"]))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({"uid": "Invalid reset link"})
        
        if not default_token_generator.check_token(user, attrs["token"]):
            raise serializers.ValidationError({"token": "Invalid or expired reset link"})
        
        attrs["user"] = user
        return attrs

    def save(self) -> User:
        """Reset the password"""
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
