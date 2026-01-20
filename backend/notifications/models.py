# notifications/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone


class Notification(models.Model):
    """
    Notification model for user notifications
    """

    class NotificationType(models.TextChoices):
        GRADE = "grade", "Grade"
        COMMENT = "comment", "Comment"
        SUBMISSION = "submission", "Submission"
        ASSIGNMENT = "assignment", "Assignment"
        REMINDER = "reminder", "Reminder"
        FEEDBACK = "feedback", "Feedback"
        CASE_REVIEW = "case_review", "Case Review"
        PERMISSION_GRANTED = "permission_granted", "Permission Granted"
        INQUIRY = "inquiry", "Inquiry"
        SYSTEM = "system", "System"

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        help_text="User who will receive this notification",
    )

    notification_type = models.CharField(
        max_length=50,
        choices=NotificationType.choices,
        help_text="Type of notification",
    )

    title = models.CharField(max_length=200, help_text="Notification title")

    message = models.TextField(help_text="Notification message content")

    # Related objects (optional)
    related_case = models.ForeignKey(
        "cases.Case",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
        help_text="Related case if applicable",
    )

    related_comment = models.ForeignKey(
        "comments.Comment",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
        help_text="Related comment if applicable",
    )

    related_grade = models.ForeignKey(
        "grades.Grade",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
        help_text="Related grade if applicable",
    )

    related_feedback = models.ForeignKey(
        "feedback.Feedback",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
        help_text="Related feedback if applicable",
    )

    related_inquiry = models.ForeignKey(
        "inquiries.Inquiry",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
        help_text="Related inquiry if applicable",
    )

    # Action URL (for navigation)
    action_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="URL to navigate to when clicking notification",
    )

    # Status
    is_read = models.BooleanField(
        default=False, help_text="Whether notification has been read"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "notifications_notification"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["recipient", "-created_at"]),
            models.Index(fields=["recipient", "is_read"]),
            models.Index(fields=["notification_type"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.recipient.get_full_name()}"

    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=["is_read", "read_at"])

    @classmethod
    def create_grade_notification(cls, grade, case):
        """Create notification when a case is graded"""
        return cls.objects.create(
            recipient=case.student,
            notification_type=cls.NotificationType.GRADE,
            title="Bệnh án đã được chấm điểm",
            message=f"Bài nộp của bạn cho '{case.title}' đã được chấm điểm: {grade.score}%",
            related_case=case,
            related_grade=grade,
            action_url=f"/cases/{case.id}",
        )

    @classmethod
    def create_comment_notification(cls, comment, case):
        """Create notification when someone comments on a case"""
        # Notify case owner if someone else comments
        if comment.author != case.student:
            return cls.objects.create(
                recipient=case.student,
                notification_type=cls.NotificationType.COMMENT,
                title="Nhận xét mới",
                message=f"{comment.author.get_full_name()} đã nhận xét về bệnh án '{case.title}'",
                related_case=case,
                related_comment=comment,
                action_url=f"/cases/{case.id}#comments",
            )

    @classmethod
    def create_submission_notification(cls, case):
        """Create notification when a student submits a case"""
        # Notify instructor when student submits
        if case.reviewed_by:
            return cls.objects.create(
                recipient=case.reviewed_by,
                notification_type=cls.NotificationType.SUBMISSION,
                title="Sinh viên nộp bài",
                message=f"{case.student.get_full_name()} đã nộp bệnh án '{case.title}'",
                related_case=case,
                action_url=f"/cases/{case.id}",
            )

    @classmethod
    def create_feedback_notification(cls, feedback, case):
        """Create notification when feedback is given"""
        return cls.objects.create(
            recipient=case.student,
            notification_type=cls.NotificationType.FEEDBACK,
            title="Phản hồi mới",
            message=f"Bạn đã nhận được phản hồi mới cho bệnh án '{case.title}'",
            related_case=case,
            related_feedback=feedback,
            action_url=f"/cases/{case.id}#feedback",
        )

    @classmethod
    def create_reminder_notification(cls, user, case, days_left):
        """Create reminder notification for upcoming deadline"""
        return cls.objects.create(
            recipient=user,
            notification_type=cls.NotificationType.REMINDER,
            title="Nhắc nhở hạn nộp",
            message=f"Bệnh án '{case.title}' sẽ hết hạn trong {days_left} ngày",
            related_case=case,
            action_url=f"/cases/{case.id}",
        )

    @classmethod
    def create_inquiry_notification(cls, inquiry, recipient, title, message):
        """Create notification for inquiry-related events"""
        return cls.objects.create(
            recipient=recipient,
            notification_type=cls.NotificationType.INQUIRY,
            title=title,
            message=message,
            related_inquiry=inquiry,
            related_case=inquiry.case,
            action_url=f"/inquiries/{inquiry.id}",
        )
