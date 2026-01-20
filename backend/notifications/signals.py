from django.db.models.signals import post_save
from django.dispatch import receiver
from cases.models import Case
from grades.models import Grade
from comments.models import Comment
from feedback.models import Feedback
from .models import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_notification_to_user(user_id, notification_data):
    """
    Send notification to user via WebSocket
    """
    channel_layer = get_channel_layer()
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            f"notifications_{user_id}",
            {"type": "notification_message", "notification": notification_data},
        )


@receiver(post_save, sender=Grade)
def create_grade_notification(sender, instance, created, **kwargs):
    """Create notification when a case is graded"""
    if created:
        notification = Notification.create_grade_notification(instance, instance.case)
        if notification:
            # Send real-time notification (fails gracefully if Redis is down)
            try:
                send_notification_to_user(
                    notification.recipient.id,
                    {
                        "id": notification.id,
                        "type": notification.notification_type,
                        "title": notification.title,
                        "message": notification.message,
                        "action_url": notification.action_url,
                        "is_read": notification.is_read,
                        "created_at": notification.created_at.isoformat(),
                    },
                )
            except Exception as e:
                # Log but don't fail - notification is already saved to database
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Failed to send real-time notification: {e}")


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """Create notification when someone comments on a case"""
    if created and instance.case:
        notification = Notification.create_comment_notification(instance, instance.case)
        if notification:
            # Send real-time notification (fails gracefully if Redis is down)
            try:
                send_notification_to_user(
                    notification.recipient.id,
                    {
                        "id": notification.id,
                        "type": notification.notification_type,
                        "title": notification.title,
                        "message": notification.message,
                        "action_url": notification.action_url,
                        "is_read": notification.is_read,
                        "created_at": notification.created_at.isoformat(),
                    },
                )
            except Exception as e:
                # Log but don't fail - notification is already saved to database
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Failed to send real-time notification: {e}")


@receiver(post_save, sender=Case)
def create_case_notification(sender, instance, created, **kwargs):
    """Create notification when case status changes to submitted"""
    if not created and instance.case_status == "submitted":
        # Check if status just changed to submitted
        old_case = Case.objects.filter(pk=instance.pk).first()
        if old_case and old_case.case_status != "submitted":
            notification = Notification.create_submission_notification(instance)
            if notification:
                # Send real-time notification (fails gracefully if Redis is down)
                try:
                    send_notification_to_user(
                        notification.recipient.id,
                        {
                            "id": notification.id,
                            "type": notification.notification_type,
                            "title": notification.title,
                            "message": notification.message,
                            "action_url": notification.action_url,
                            "is_read": notification.is_read,
                            "created_at": notification.created_at.isoformat(),
                        },
                    )
                except Exception as e:
                    # Log but don't fail - notification is already saved to database
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(f"Failed to send real-time notification: {e}")


@receiver(post_save, sender=Feedback)
def create_feedback_notification(sender, instance, created, **kwargs):
    """Create notification when feedback is given"""
    if created and instance.case:
        notification = Notification.create_feedback_notification(instance, instance.case)
        if notification:
            # Send real-time notification (fails gracefully if Redis is down)
            try:
                send_notification_to_user(
                    notification.recipient.id,
                    {
                        "id": notification.id,
                        "type": notification.notification_type,
                        "title": notification.title,
                        "message": notification.message,
                        "action_url": notification.action_url,
                        "is_read": notification.is_read,
                        "created_at": notification.created_at.isoformat(),
                    },
                )
            except Exception as e:
                # Log but don't fail - notification is already saved to database
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Failed to send real-time notification: {e}")

