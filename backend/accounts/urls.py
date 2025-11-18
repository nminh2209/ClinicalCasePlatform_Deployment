from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView  # type: ignore[reportMissingTypeStubs]
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserListView,
    logout_view,
    # CustomTokenObtainPairView,
)

urlpatterns = [
    # Authentication endpoints
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("logout/", logout_view, name="user-logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    # User management
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("users/", UserListView.as_view(), name="user-list"),
]
