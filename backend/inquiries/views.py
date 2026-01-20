# inquiries/views.py

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Inquiry, InquiryResponse
from .serializers import InquirySerializer, InquiryResponseSerializer
from .permissions import IsInquiryParticipantOrAdmin
from cases.models import Case


class InquiryPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class InquiryViewSet(viewsets.ModelViewSet):
    """
    CRUD for Inquiries.
    - Instructors create inquiries on student cases.
    - Students view and respond.
    """

    serializer_class = InquirySerializer
    permission_classes = [permissions.IsAuthenticated, IsInquiryParticipantOrAdmin]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    pagination_class = InquiryPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "case", "topic", "instructor", "student"]
    search_fields = ["title", "content", "topic", "case__title"]
    ordering_fields = ["created_at", "updated_at", "status"]
    ordering = ["-updated_at"]

    def get_queryset(self):
        user = self.request.user
        qs = Inquiry.objects.select_related(
            "case", "instructor", "student"
        ).prefetch_related("responses__author", "responses__attachments", "attachments")

        if user.is_superuser or getattr(user, "role", "") == "admin":  # type: ignore[attr-defined]
            return qs

        if getattr(user, "is_instructor", False):
            return qs.filter(instructor=user)

        if getattr(user, "is_student", False):
            return qs.filter(student=user)

        return Inquiry.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        # Only instructors can create inquiries
        if not getattr(user, "is_instructor", False):
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied("Only instructors can create inquiries.")

        case_id = self.request.data.get("case")
        case = get_object_or_404(Case, id=case_id)

        # Ensure student exists
        if not case.student:
            from rest_framework.exceptions import ValidationError

            raise ValidationError("Cannot create inquiry for case without a student.")

        serializer.save(instructor=user, student=case.student)

    @action(detail=True, methods=["post"])
    def close(self, request, pk=None):
        """Close an inquiry"""
        inquiry = self.get_object()

        try:
            inquiry.close(closed_by=request.user)
            return Response({"status": "closed"})
        except PermissionError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_403_FORBIDDEN,
            )

    @action(detail=True, methods=["post"])
    def resolve(self, request, pk=None):
        """Mark inquiry as resolved"""
        inquiry = self.get_object()

        try:
            inquiry.resolve(resolved_by=request.user)
            return Response({"status": "resolved"})
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class InquiryResponseViewSet(viewsets.ModelViewSet):
    """
    Manage responses to inquiries.
    """

    serializer_class = InquiryResponseSerializer
    permission_classes = [permissions.IsAuthenticated, IsInquiryParticipantOrAdmin]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        # Usually accessed via nested route or filtered by inquiry,
        # but here restricting generally to visible inquiries
        user = self.request.user
        return InquiryResponse.objects.filter(
            Q(inquiry__instructor=user) | Q(inquiry__student=user)
        )

    def perform_create(self, serializer):
        inquiry_id = self.request.data.get("inquiry")
        inquiry = get_object_or_404(Inquiry, id=inquiry_id)

        # Check permission (must be instructor or student of the inquiry)
        user = self.request.user
        if user != inquiry.instructor and user != inquiry.student:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied("You are not a participant in this inquiry.")

        # If student responds, mark resolved? Or keep open.
        # Business logic: If instructor replies, maybe Open. If student replies, maybe Resolved?
        # Leaving status logic simple for now, can be enhanced via signals.

        serializer.save(author=user)
