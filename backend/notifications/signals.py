from django.db.models.signals import post_save
from django.dispatch import receiver
from cases.models import Case
from grades.models import Grade
from comments.models import Comment
from feedback.models import Feedback
from .models import Notification


@receiver(post_save, sender=Grade)
def create_grade_notification(sender, instance, created, **kwargs):
    """Create notification when a case is graded"""
    if created:
        Notification.create_grade_notification(instance, instance.case)


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """Create notification when someone comments on a case"""
    if created and instance.case:
        Notification.create_comment_notification(instance, instance.case)


@receiver(post_save, sender=Case)
def create_case_notification(sender, instance, created, **kwargs):
    """Create notification when case status changes to submitted"""
    if not created and instance.case_status == "submitted":
        # Check if status just changed to submitted
        old_case = Case.objects.filter(pk=instance.pk).first()
        if old_case and old_case.case_status != "submitted":
            Notification.create_submission_notification(instance)


@receiver(post_save, sender=Feedback)
def create_feedback_notification(sender, instance, created, **kwargs):
    """Create notification when feedback is given"""
    if created and instance.case:
        Notification.create_feedback_notification(instance, instance.case)
