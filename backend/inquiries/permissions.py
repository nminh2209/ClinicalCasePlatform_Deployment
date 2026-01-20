# inquiries/permissions.py

from rest_framework import permissions


class IsInquiryParticipantOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow:
    - Instructors (creators)
    - Students (recipients)
    - Admins
    to view and respond to inquiries.
    """

    def has_permission(self, request, view):
        """Check if user can access list/create views"""
        if not request.user.is_authenticated:
            return False

        # Admins can do anything
        if request.user.is_superuser or getattr(request.user, "role", "") == "admin":  # type: ignore[attr-defined]
            return True

        # Instructors and students can access their own inquiries
        return getattr(request.user, "is_instructor", False) or getattr(
            request.user, "is_student", False
        )

    def has_object_permission(self, request, view, obj):
        """Check if user can access specific inquiry/response"""
        # Admin access
        if request.user.is_superuser or getattr(request.user, "role", "") == "admin":  # type: ignore[attr-defined]
            return True

        # Check if obj is Inquiry
        if hasattr(obj, "instructor"):
            return request.user == obj.instructor or request.user == obj.student

        # Check if obj is InquiryResponse
        if hasattr(obj, "inquiry"):
            return (
                request.user == obj.inquiry.instructor
                or request.user == obj.inquiry.student
            )

        return False
