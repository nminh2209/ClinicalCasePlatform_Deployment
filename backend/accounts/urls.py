# accounts/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,  # type: ignore[reportMissingTypeStubs]
)

from .views import (
    AdminUserViewSet,
    ChangePasswordView,
    GoogleLoginView,
    MicrosoftLoginView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    RoleModificationRequestCreateView,
    RoleModificationRequestListView,
    RoleModificationRequestDetailView,
    RoleModificationRequestMyView,
    approve_role_request,
    reject_role_request,
    UserListView,
    UserLoginView,
    UserProfileView,
    UserRegistrationView,
    logout_view,
    # CustomTokenObtainPairView,
)

# Router for admin user management
router = DefaultRouter()
router.register(r"admin/users", AdminUserViewSet, basename="admin-user")

urlpatterns = [
    # Authentication endpoints
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("logout/", logout_view, name="user-logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    # Social authentication
    path("google/", GoogleLoginView.as_view(), name="google-login"),
    path("microsoft/", MicrosoftLoginView.as_view(), name="microsoft-login"),
    # Password reset
    path(
        "password-reset/",
        PasswordResetRequestView.as_view(),
        name="password-reset-request",
    ),
    path(
        "password-reset-confirm/",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    # User management
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("users/", UserListView.as_view(), name="user-list"),
    # Admin user management (ViewSet routes)
    path("", include(router.urls)),

    # Role modification requests
    path(
        "role-requests/",
        RoleModificationRequestCreateView.as_view(),
        name="role-request-create",
    ),
    path(
        "role-requests/my/",
        RoleModificationRequestMyView.as_view(),
        name="role-request-my",
    ),
    path(
        "role-requests/list/",
        RoleModificationRequestListView.as_view(),
        name="role-request-list",
    ),
    path(
        "role-requests/<int:pk>/",
        RoleModificationRequestDetailView.as_view(),
        name="role-request-detail",
    ),
    path(
        "role-requests/<int:pk>/approve/",
        approve_role_request,
        name="role-request-approve",
    ),
    path(
        "role-requests/<int:pk>/reject/",
        reject_role_request,
        name="role-request-reject",
    ),
]
