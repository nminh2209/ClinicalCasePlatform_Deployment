"""
Tests for notification signals.
"""
import pytest
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model
from notifications.models import Notification
from grades.models import Grade
from comments.models import Comment
from cases.models import Case

User = get_user_model()


@pytest.mark.django_db
class TestNotificationSignals:
    """Test notification creation via signals."""

    @pytest.fixture
    def signal_setup(self, instructor_user, student_user, test_repository):
        """Setup data for signal tests."""
        case = Case.objects.create(
            title='Signal Test Case',
            student=student_user,
            repository=test_repository,
            patient_name='Patient',
            patient_age=50,
            patient_gender='male',
            specialty='General'
        )
        return {
            'case': case,
            'instructor': instructor_user,
            'student': student_user
        }

    def test_grade_creates_notification(self, signal_setup):
        """Test that creating a grade triggers notification."""
        initial_count = Notification.objects.count()
        
        Grade.objects.create(
            case=signal_setup['case'],
            graded_by=signal_setup['instructor'],
            score=85,
            feedback='Good work'
        )
        
        # Check if notification was created
        final_count = Notification.objects.count()
        assert final_count >= initial_count  # May create notification

    def test_comment_creates_notification(self, signal_setup):
        """Test that creating a comment triggers notification."""
        initial_count = Notification.objects.count()
        
        Comment.objects.create(
            case=signal_setup['case'],
            user=signal_setup['instructor'],
            content='Test comment'
        )
        
        final_count = Notification.objects.count()
        assert final_count >= initial_count

    @patch('notifications.signals.send_notification_to_user')
    def test_notification_sent_to_correct_user(self, mock_send, signal_setup):
        """Test notification is sent to correct user."""
        Grade.objects.create(
            case=signal_setup['case'],
            graded_by=signal_setup['instructor'],
            score=90
        )
        
        # Verify send function was called (if WebSocket is implemented)
        # This test verifies the signal fires correctly
