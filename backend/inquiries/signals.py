# inquiries/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Inquiry, InquiryResponse
from notifications.models import Notification


def send_realtime_notification(user_id, notification_data):
    """Helper to send WS message"""
    channel_layer = get_channel_layer()
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            f"notifications_{user_id}",
            {"type": "notification_message", "notification": notification_data},
        )


@receiver(post_save, sender=Inquiry)
def notify_on_inquiry_creation(sender, instance, created, **kwargs):
    """
    Notify student when an instructor creates an inquiry on their case.
    """
    if created:
        # Always save notification to database
        notification = Notification.create_inquiry_notification(
            inquiry=instance,
            recipient=instance.student,
            title="Thắc mắc mới từ giảng viên",
            message=f"{instance.instructor.get_full_name()} đã đặt câu hỏi về ca bệnh '{instance.case.title}': {instance.title}",
        )

        # Try to send real-time notification via WebSocket (fails gracefully if Redis is down)
        try:
            send_realtime_notification(
                instance.student.id,
                {
                    "id": notification.id,  # type: ignore[attr-defined]
                    "type": notification.notification_type,
                    "title": notification.title,
                    "message": notification.message,
                    "action_url": notification.action_url,
                    "created_at": notification.created_at.isoformat(),
                },
            )
        except Exception as e:
            # Log but don't fail - notification is already saved to database
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to send real-time notification: {e}")


@receiver(post_save, sender=InquiryResponse)
def notify_on_inquiry_response(sender, instance, created, **kwargs):
    """
    Notify the other party when a response is added.
    """
    if created:
        inquiry = instance.inquiry
        responder = instance.author

        # If instructor replied, notify student
        if responder == inquiry.instructor:
            recipient = inquiry.student
            title = "Phản hồi từ giảng viên"
            message = (
                f"{responder.get_full_name()} đã trả lời thắc mắc '{inquiry.title}'"
            )
        # If student replied, notify instructor
        elif responder == inquiry.student:
            recipient = inquiry.instructor
            title = "Phản hồi từ sinh viên"
            message = (
                f"{responder.get_full_name()} đã trả lời thắc mắc '{inquiry.title}'"
            )
        else:
            return  # Should not happen given permissions

        # Use the classmethod instead of direct create
        notification = Notification.create_inquiry_notification(
            inquiry=inquiry,
            recipient=recipient,
            title=title,
            message=message,
        )

        # Try to send real-time notification (fails gracefully if Redis is down)
        try:
            send_realtime_notification(
                recipient.id,
                {
                    "id": notification.id,  # type: ignore[attr-defined]
                    "type": notification.notification_type,
                    "title": notification.title,
                    "message": notification.message,
                    "action_url": notification.action_url,
                    "created_at": notification.created_at.isoformat(),
                },
            )
        except Exception as e:
            # Log but don't fail - notification is already saved to database
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to send real-time notification: {e}")
