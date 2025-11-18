from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from django.db.models import Count
from .models import CaseTemplate
from .serializers import CaseTemplateSerializer, CaseTemplateListSerializer


class CaseTemplateListCreateView(generics.ListCreateAPIView):
    """
    List case templates and create new templates
    """

    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["specialty", "is_standard", "is_active", "department"]
    search_fields = ["name", "vietnamese_name", "description", "specialty"]
    ordering_fields = ["created_at", "name", "specialty"]
    ordering = ["specialty", "name"]

    def get_queryset(self):
        # Return templates based on user permissions
        user = self.request.user
        queryset = CaseTemplate.objects.annotate(case_count=Count("cases"))

        if user.is_instructor:
            # Instructors can see all templates
            return queryset
        else:
            # Students see active templates only
            return queryset.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CaseTemplateListSerializer
        return CaseTemplateSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CaseTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a case template
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_instructor:
            return CaseTemplate.objects.all()
        else:
            # Students see active templates or templates they created
            return CaseTemplate.objects.filter(
                models.Q(is_active=True) | models.Q(created_by=user)
            )

    def get_serializer_class(self):
        from rest_framework import serializers

        class CaseTemplateSerializer(serializers.ModelSerializer):
            class Meta:
                model = CaseTemplate
                fields = "__all__"
                read_only_fields = ("created_by", "created_at", "updated_at")

        return CaseTemplateSerializer
