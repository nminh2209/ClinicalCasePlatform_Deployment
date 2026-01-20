# notifications/serializers.py

from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model"""

    time_ago = serializers.SerializerMethodField()

    class Meta:  # type: ignore[misc, assignment]
        model = Notification
        fields = [
            "id",
            "notification_type",
            "title",
            "message",
            "action_url",
            "is_read",
            "created_at",
            "read_at",
            "time_ago",
            "related_case",
            "related_comment",
            "related_grade",
            "related_feedback",
            "related_inquiry",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "read_at",
            "time_ago",
        ]

    def get_time_ago(self, obj):
        """Calculate human-readable time ago"""
        from django.utils import timezone
        from datetime import timedelta

        now = timezone.now()
        diff = now - obj.created_at

        if diff < timedelta(minutes=1):
            return "Vừa xong"
        elif diff < timedelta(hours=1):
            minutes = int(diff.total_seconds() / 60)
            return f"{minutes} phút trước"
        elif diff < timedelta(days=1):
            hours = int(diff.total_seconds() / 3600)
            return f"{hours} giờ trước"
        elif diff < timedelta(days=7):
            days = diff.days
            return f"{days} ngày trước"
        elif diff < timedelta(days=30):
            weeks = int(diff.days / 7)
            return f"{weeks} tuần trước"
        else:
            months = int(diff.days / 30)
            return f"{months} tháng trước"
