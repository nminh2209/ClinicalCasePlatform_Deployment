# backend/cases/permissions.py

from rest_framework import permissions


class IsInstructorPermission(permissions.BasePermission):
    """
    Permission class that only allows instructors to access the view.
    """

    message = "Only instructors can perform this action."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "is_instructor", False)
        )
