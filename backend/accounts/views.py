from rest_framework import status, generics, permissions  # type: ignore[reportMissingTypeStubs]
from rest_framework.decorators import api_view, permission_classes  # type: ignore[reportMissingTypeStubs]
from rest_framework.response import Response  # type: ignore[reportMissingTypeStubs]
from rest_framework_simplejwt.tokens import RefreshToken  # type: ignore[reportMissingTypeStubs]
from rest_framework_simplejwt.views import TokenObtainPairView  # type: ignore[reportMissingTypeStubs]

# from django.contrib.auth import login
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
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
            user = User.objects.select_related('department').get(pk=request.user.pk)
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
        user = User.objects.select_related('department').get(pk=user.pk)

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
        return User.objects.select_related('department')

    def get_object(self):
        return self.get_queryset().get(pk=self.request.user.pk)


class UserListView(generics.ListAPIView):
    """
    List all users (for instructors to see students)
    """

    queryset = User.objects.all().select_related('department')
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
