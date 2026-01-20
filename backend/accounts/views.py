# accounts/views.py

import requests
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
from rest_framework_simplejwt.tokens import (
    RefreshToken,  # type: ignore[reportMissingTypeStubs]
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # type: ignore[reportMissingTypeStubs]
)
from django_filters.rest_framework import DjangoFilterBackend  # type: ignore[reportMissingTypeStubs]
from django.conf import settings

# from django.contrib.auth import login
from .models import User
from .serializers import (
    AdminUserSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)


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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # Reload user with department data
        user = User.objects.select_related("department").get(pk=user.pk)

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


class UserListView(generics.ListAPIView):
    """
    List all users (for instructors to see students)
    """

    queryset = User.objects.all().select_related("department")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["role", "department", "is_active"]
    search_fields = ["username", "email", "first_name", "last_name", "student_id", "employee_id"]
    ordering_fields = ["created_at", "username", "email", "role"]

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        """Activate a user account"""
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({"message": "User activated successfully"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        """Deactivate a user account"""
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({"message": "User deactivated successfully"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def reset_password(self, request, pk=None):
        """Reset user password"""
        user = self.get_object()
        new_password = request.data.get("password")
        
        if not new_password:
            return Response(
                {"error": "Password is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)


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
            status=status.HTTP_200_OK
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
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Verify token with Google
            google_response = requests.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if google_response.status_code != 200:
                return Response(
                    {"error": "Invalid Google access token"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            google_data = google_response.json()
            email = google_data.get("email")
            
            if not email:
                return Response(
                    {"error": "Email not provided by Google"},
                    status=status.HTTP_400_BAD_REQUEST
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
                }
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
                    "message": "Login successful" if not created else "Account created successfully",
                    "is_new_user": created,
                },
                status=status.HTTP_200_OK,
            )
            
        except requests.RequestException as e:
            return Response(
                {"error": f"Failed to verify Google token: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            return Response(
                {"error": f"Authentication failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Verify token with Microsoft Graph API
            microsoft_response = requests.get(
                "https://graph.microsoft.com/v1.0/me",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if microsoft_response.status_code != 200:
                return Response(
                    {"error": "Invalid Microsoft access token"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            microsoft_data = microsoft_response.json()
            email = microsoft_data.get("mail") or microsoft_data.get("userPrincipalName")
            
            if not email:
                return Response(
                    {"error": "Email not provided by Microsoft"},
                    status=status.HTTP_400_BAD_REQUEST
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
                }
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
                    "message": "Login successful" if not created else "Account created successfully",
                    "is_new_user": created,
                },
                status=status.HTTP_200_OK,
            )
            
        except requests.RequestException as e:
            return Response(
                {"error": f"Failed to verify Microsoft token: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            return Response(
                {"error": f"Authentication failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
