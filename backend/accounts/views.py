# accounts/views.py

import requests
import logging
from typing import Any, Dict
from rest_framework import (  # type: ignore[reportMissingTypeStubs]
    generics,
    permissions,
    status,
    viewsets,
    filters,
)
from rest_framework.decorators import (  # type: ignore[reportMissingTypeStubs]
    api_view,
    permission_classes,
    action,
)
from rest_framework.response import Response  # type: ignore[reportMissingTypeStubs]
from rest_framework.exceptions import ValidationError  # type: ignore[reportMissingTypeStubs]
from rest_framework_simplejwt.tokens import (
    RefreshToken,  # type: ignore[reportMissingTypeStubs]
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # type: ignore[reportMissingTypeStubs]
)
from django_filters.rest_framework import DjangoFilterBackend  # type: ignore[reportMissingTypeStubs]
from django.conf import settings

# from django.contrib.auth import login
from django.utils import timezone
from .models import User, RoleModificationRequest
from .serializers import (
    AdminUserSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    RoleModificationRequestSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)


logger = logging.getLogger(__name__)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token view that includes user data in response
    """

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            # Get user data with department
            user = User.objects.select_related("department").get(pk=request.user.pk)
            user_serializer = UserSerializer(user)
            response.data["user"] = user_serializer.data
        return response


class UserRegistrationView(generics.CreateAPIView):
    """
    Register a new user
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response(
            {
                "user": UserSerializer(user).data,
                "tokens": {"access": access_token, "refresh": refresh_token},
                "message": "User registered successfully",
            },
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(generics.GenericAPIView):
    """
    Login user and return JWT tokens
    """

    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data["user"]

            # Try eager loading department, but don't fail login if relation loading breaks.
            try:
                user = User.objects.select_related("department").get(pk=user.pk)
            except Exception:
                logger.exception("Failed to prefetch department during login")

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response(
                {
                    "user": UserSerializer(user).data,
                    "tokens": {"access": access_token, "refresh": refresh_token},
                    "message": "Login successful",
                },
                status=status.HTTP_200_OK,
            )
        except ValidationError as exc:
            return Response(exc.detail, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            logger.exception("Unhandled error during login")
            return Response(
                {"detail": "Login failed due to a server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Get and update user profile
    """

    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.select_related("department")

    def get_object(self):
        return self.get_queryset().get(pk=self.request.user.pk)


class ChangePasswordView(generics.GenericAPIView):
    """
    Allow authenticated users to change their own password.
    POST /api/auth/change-password/
    """

    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Mật khẩu đã được thay đổi thành công"},
            status=status.HTTP_200_OK,
        )


class IsInstructorOrAdmin(permissions.BasePermission):
    """Allow access only to instructors or admin/superusers."""

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return getattr(request.user, "role", None) in ("instructor", "admin") or request.user.is_staff


class IsRoleAdmin(permissions.BasePermission):
    """Allow access only to users with role=admin or Django staff flag."""

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return getattr(request.user, "role", None) == "admin" or request.user.is_staff


class UserListView(generics.ListAPIView):
    """
    List all users (for instructors to see students, admins to manage users)
    """

    queryset = User.objects.all().select_related("department")
    serializer_class = UserSerializer
    permission_classes = [IsInstructorOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get("role", None)
        if role:
            queryset = queryset.filter(role=role)
        department = self.request.query_params.get("department", None)
        if department:
            queryset = queryset.filter(department_id=department)
        return queryset


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    Logout user by blacklisting the refresh token
    """
    try:
        refresh_token = request.data.get("refresh_token")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminUserViewSet(viewsets.ModelViewSet):
    """
    Admin-only ViewSet for full user CRUD operations.
    Allows admins to create, read, update, and delete users.
    """

    queryset = User.objects.all().select_related("department").order_by("-created_at")
    serializer_class = AdminUserSerializer
    permission_classes = [IsRoleAdmin]
    pagination_class = None  # return all users; frontend handles filtering
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["role", "department", "is_active"]
    search_fields = [
        "username",
        "email",
        "first_name",
        "last_name",
        "student_id",
        "employee_id",
    ]
    ordering_fields = ["created_at", "username", "email", "role"]

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        """Activate a user account"""
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response(
            {"message": "User activated successfully"}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        """Deactivate a user account"""
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response(
            {"message": "User deactivated successfully"}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def reset_password(self, request, pk=None):
        """Reset user password"""
        user = self.get_object()
        new_password = request.data.get("password")

        if not new_password:
            return Response(
                {"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()
        return Response(
            {"message": "Password reset successfully"}, status=status.HTTP_200_OK
        )


class PasswordResetRequestView(generics.GenericAPIView):
    """
    Request password reset via email
    """

    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(result, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    """
    Confirm password reset with token
    """

    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Password has been reset successfully"},
            status=status.HTTP_200_OK,
        )


class GoogleLoginView(generics.GenericAPIView):
    """
    Login/Register with Google OAuth
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """Exchange Google access token for JWT"""
        access_token = request.data.get("access_token")

        if not access_token:
            return Response(
                {"error": "Access token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Verify token with Google
            google_response = requests.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            )

            if google_response.status_code != 200:
                return Response(
                    {"error": "Invalid Google access token"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            google_data = google_response.json()
            email = google_data.get("email")

            if not email:
                return Response(
                    {"error": "Email not provided by Google"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Get or create user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "username": email.split("@")[0],
                    "first_name": google_data.get("given_name", ""),
                    "last_name": google_data.get("family_name", ""),
                    "role": "student",  # Default role
                    "is_active": True,
                },
            )

            if created:
                # Set unusable password for OAuth users
                user.set_unusable_password()
                user.save()

            # Reload user with department data
            user = User.objects.select_related("department").get(pk=user.pk)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token_jwt = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response(
                {
                    "user": UserSerializer(user).data,
                    "tokens": {"access": access_token_jwt, "refresh": refresh_token},
                    "message": (
                        "Login successful"
                        if not created
                        else "Account created successfully"
                    ),
                    "is_new_user": created,
                },
                status=status.HTTP_200_OK,
            )

        except requests.RequestException as e:
            return Response(
                {"error": f"Failed to verify Google token: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except Exception as e:
            return Response(
                {"error": f"Authentication failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class MicrosoftLoginView(generics.GenericAPIView):
    """
    Login/Register with Microsoft OAuth (Azure AD)
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """Exchange Microsoft access token for JWT"""
        access_token = request.data.get("access_token")

        if not access_token:
            return Response(
                {"error": "Access token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Verify token with Microsoft Graph API
            microsoft_response = requests.get(
                "https://graph.microsoft.com/v1.0/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )

            if microsoft_response.status_code != 200:
                return Response(
                    {"error": "Invalid Microsoft access token"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            microsoft_data = microsoft_response.json()
            email = microsoft_data.get("mail") or microsoft_data.get(
                "userPrincipalName"
            )

            if not email:
                return Response(
                    {"error": "Email not provided by Microsoft"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Get or create user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "username": email.split("@")[0],
                    "first_name": microsoft_data.get("givenName", ""),
                    "last_name": microsoft_data.get("surname", ""),
                    "role": "student",  # Default role
                    "is_active": True,
                },
            )

            if created:
                # Set unusable password for OAuth users
                user.set_unusable_password()
                user.save()

            # Reload user with department data
            user = User.objects.select_related("department").get(pk=user.pk)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token_jwt = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response(
                {
                    "user": UserSerializer(user).data,
                    "tokens": {"access": access_token_jwt, "refresh": refresh_token},
                    "message": (
                        "Login successful"
                        if not created
                        else "Account created successfully"
                    ),
                    "is_new_user": created,
                },
                status=status.HTTP_200_OK,
            )

        except requests.RequestException as e:
            return Response(
                {"error": f"Failed to verify Microsoft token: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except Exception as e:
            return Response(
                {"error": f"Authentication failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


def _push_notification_via_ws(notification) -> None:
    """Push a Notification instance to the recipient's WebSocket channel group."""
    try:
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync

        channel_layer = get_channel_layer()
        if not channel_layer:
            return
        async_to_sync(channel_layer.group_send)(
            f"notifications_{notification.recipient_id}",
            {
                "type": "notification_message",
                "notification": {
                    "id": notification.id,
                    "type": notification.notification_type,
                    "title": notification.title,
                    "message": notification.message,
                    "action_url": notification.action_url,
                    "is_read": notification.is_read,
                },
            },
        )
    except Exception:
        pass  # WS push failure must never block the HTTP response


class IsStudent(permissions.BasePermission):
    """Allow access only to users with role=student."""

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return getattr(request.user, "role", None) == "student"


class RoleModificationRequestMyView(generics.ListAPIView):
    """
    Students retrieve only their own past role modification requests.
    GET /api/auth/role-requests/my/
    """

    serializer_class = RoleModificationRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RoleModificationRequest.objects.filter(
            requester=self.request.user
        ).select_related("department", "reviewed_by")


class RoleModificationRequestCreateView(generics.CreateAPIView):
    """
    Students submit a role modification request (student → instructor).
    POST /api/auth/role-requests/
    """

    serializer_class = RoleModificationRequestSerializer
    permission_classes = [IsStudent]

    def perform_create(self, serializer):
        from notifications.models import Notification

        role_request = serializer.save(requester=self.request.user)

        # Notify all admin users about the new request
        admin_users = User.objects.filter(role="admin", is_active=True)
        for admin in admin_users:
            notif = Notification.objects.create(
                recipient=admin,
                notification_type=Notification.NotificationType.ROLE_REQUEST,
                title="Yêu cầu thay đổi vai trò mới",
                message=(
                    f"{role_request.requester.get_full_name()} (MSSV: {role_request.student_id}) "
                    f"đã gửi yêu cầu trở thành Giảng viên."
                ),
                action_url="/admin/role-approval",
            )
            _push_notification_via_ws(notif)


class RoleModificationRequestListView(generics.ListAPIView):
    """
    Admins retrieve all role modification requests.
    GET /api/auth/role-requests/
    """

    serializer_class = RoleModificationRequestSerializer
    permission_classes = [IsRoleAdmin]

    def get_queryset(self):
        qs = RoleModificationRequest.objects.select_related(
            "requester", "department", "reviewed_by"
        )
        status_param = self.request.query_params.get("status")
        if status_param:
            qs = qs.filter(status=status_param)
        return qs


class RoleModificationRequestDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single role modification request.
    GET /api/auth/role-requests/{id}/
    """

    serializer_class = RoleModificationRequestSerializer
    permission_classes = [IsRoleAdmin]
    queryset = RoleModificationRequest.objects.select_related(
        "requester", "department", "reviewed_by"
    )


@api_view(["POST"])
@permission_classes([IsRoleAdmin])
def approve_role_request(request, pk):
    """
    Approve a role modification request.
    Updates the requester's role to instructor and notifies them.
    POST /api/auth/role-requests/{id}/approve/
    """
    from notifications.models import Notification

    try:
        role_request = RoleModificationRequest.objects.select_related(
            "requester"
        ).get(pk=pk, status="pending")
    except RoleModificationRequest.DoesNotExist:
        return Response(
            {"error": "Request not found or already processed."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Promote the user
    requester = role_request.requester
    requester.role = User.RoleChoices.INSTRUCTOR
    requester.save(update_fields=["role", "updated_at"])

    # Mark request as approved
    role_request.status = RoleModificationRequest.StatusChoices.APPROVED
    role_request.reviewed_by = request.user
    role_request.reviewed_at = timezone.now()
    role_request.save(update_fields=["status", "reviewed_by", "reviewed_at", "updated_at"])

    # Notify requester
    notif = Notification.objects.create(
        recipient=requester,
        notification_type=Notification.NotificationType.ROLE_APPROVED,
        title="Yêu cầu thay đổi vai trò đã được chấp thuận",
        message=(
            "Chúc mừng! Yêu cầu trở thành Giảng viên của bạn đã được chấp thuận. "
            "Vui lòng đăng xuất và đăng nhập lại để vai trò mới có hiệu lực."
        ),
        action_url="/home",
    )
    _push_notification_via_ws(notif)

    return Response(
        {"message": "Request approved. User role updated to instructor."},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsRoleAdmin])
def reject_role_request(request, pk):
    """
    Reject a role modification request. Requires a rejection_reason.
    POST /api/auth/role-requests/{id}/reject/
    """
    from notifications.models import Notification

    rejection_reason = request.data.get("rejection_reason", "").strip()
    if not rejection_reason:
        return Response(
            {"error": "rejection_reason is required when rejecting a request."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        role_request = RoleModificationRequest.objects.select_related(
            "requester"
        ).get(pk=pk, status="pending")
    except RoleModificationRequest.DoesNotExist:
        return Response(
            {"error": "Request not found or already processed."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Mark request as rejected
    role_request.status = RoleModificationRequest.StatusChoices.REJECTED
    role_request.rejection_reason = rejection_reason
    role_request.reviewed_by = request.user
    role_request.reviewed_at = timezone.now()
    role_request.save(
        update_fields=["status", "rejection_reason", "reviewed_by", "reviewed_at", "updated_at"]
    )

    # Notify requester
    notif = Notification.objects.create(
        recipient=role_request.requester,
        notification_type=Notification.NotificationType.ROLE_REJECTED,
        title="Yêu cầu thay đổi vai trò bị từ chối",
        message=(
            f"Yêu cầu trở thành Giảng viên của bạn đã bị từ chối. "
            f"Lý do: {rejection_reason}"
        ),
        action_url="/role-request",
    )
    _push_notification_via_ws(notif)

    return Response(
        {"message": "Request rejected."},
        status=status.HTTP_200_OK,
    )
