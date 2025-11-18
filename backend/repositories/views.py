from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from django.db.models import Count
from .models import Repository
from .serializers import RepositorySerializer, RepositoryListSerializer


class RepositoryListCreateView(generics.ListCreateAPIView):
    """
    List repositories and create new repositories
    """

    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["access_level", "is_public", "department"]
    search_fields = ["name", "vietnamese_name", "description"]
    ordering_fields = ["created_at", "name", "case_count"]
    ordering = ["-created_at"]

    def get_queryset(self):
        # Return repositories based on user permissions
        user = self.request.user
        queryset = Repository.objects.annotate(
            case_count=Count("cases")
        ).select_related("owner", "department")

        if user.is_instructor:
            # Instructors can see all repositories
            return queryset
        else:
            # Students see public repositories and their own
            return queryset.filter(models.Q(is_public=True) | models.Q(owner=user))

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RepositoryListSerializer
        return RepositorySerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RepositoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a repository
    """

    serializer_class = RepositorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Repository.objects.annotate(
            case_count=Count("cases")
        ).select_related("owner", "department")

        if user.is_instructor:
            return queryset
        else:
            return queryset.filter(models.Q(is_public=True) | models.Q(owner=user))
