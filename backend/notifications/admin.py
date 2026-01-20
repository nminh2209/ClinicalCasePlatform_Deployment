# notifications/admin.py

from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "recipient",
        "notification_type",
        "title",
        "is_read",
        "created_at",
    ]
    list_filter = ["notification_type", "is_read", "created_at"]
    search_fields = ["title", "message", "recipient__email"]
    readonly_fields = ["created_at", "read_at"]
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Notification Info",
            {
                "fields": (
                    "recipient",
                    "notification_type",
                    "title",
                    "message",
                    "action_url",
                )
            },
        ),
        (
            "Related Objects",
            {
                "fields": (
                    "related_case",
                    "related_comment",
                    "related_grade",
                    "related_feedback",
                    "related_inquiry",
                )
            },
        ),
        ("Status", {"fields": ("is_read", "read_at", "created_at")}),
    )
