"""
Unit tests for Comments and Feedback models.
"""
import pytest
from django.contrib.auth import get_user_model
from comments.models import Comment
from feedback.models import Feedback
from cases.models import Case

User = get_user_model()


@pytest.mark.django_db
class TestCommentModel:
    """Test suite for Comment model."""

    @pytest.fixture
    def comment_setup(self, instructor_user, student_user, test_repository):
        """Setup comment test data."""
        case = Case.objects.create(
            title='Case with Comments',
            student=student_user,
            repository=test_repository,
            patient_name='Patient',
            patient_age=45,
            patient_gender='female',
            specialty='Cardiology'
        )
        return {'case': case, 'user': instructor_user}

    def test_create_comment(self, comment_setup):
        """Test creating a comment."""
        comment = Comment.objects.create(
            case=comment_setup['case'],
            user=comment_setup['user'],
            content='This is a test comment'
        )
        assert comment.content == 'This is a test comment'
        assert comment.user == comment_setup['user']
        assert comment.case == comment_setup['case']

    def test_comment_timestamps(self, comment_setup):
        """Test comment has creation and update timestamps."""
        comment = Comment.objects.create(
            case=comment_setup['case'],
            user=comment_setup['user'],
            content='Test'
        )
        assert comment.created_at is not None
        assert comment.updated_at is not None

    def test_nested_comments(self, comment_setup):
        """Test reply/nested comment functionality."""
        parent_comment = Comment.objects.create(
            case=comment_setup['case'],
            user=comment_setup['user'],
            content='Parent comment'
        )
        reply = Comment.objects.create(
            case=comment_setup['case'],
            user=comment_setup['user'],
            content='Reply comment',
            parent=parent_comment
        )
        assert reply.parent == parent_comment


@pytest.mark.django_db
class TestFeedbackModel:
    """Test suite for Feedback model."""

    @pytest.fixture
    def feedback_setup(self, student_user, test_repository):
        """Setup feedback test data."""
        case = Case.objects.create(
            title='Case for Feedback',
            student=student_user,
            repository=test_repository,
            patient_name='Patient',
            patient_age=60,
            patient_gender='male',
            specialty='Surgery'
        )
        return {'case': case, 'student': student_user}

    def test_create_feedback(self, feedback_setup):
        """Test creating feedback."""
        feedback = Feedback.objects.create(
            case=feedback_setup['case'],
            user=feedback_setup['student'],
            rating=5,
            comment='Great learning experience'
        )
        assert feedback.rating == 5
        assert feedback.comment == 'Great learning experience'

    def test_feedback_rating_range(self, feedback_setup):
        """Test feedback rating is within valid range."""
        feedback = Feedback.objects.create(
            case=feedback_setup['case'],
            user=feedback_setup['student'],
            rating=4
        )
        assert 1 <= feedback.rating <= 5

    def test_feedback_timestamps(self, feedback_setup):
        """Test feedback timestamps."""
        feedback = Feedback.objects.create(
            case=feedback_setup['case'],
            user=feedback_setup['student'],
            rating=5
        )
        assert feedback.created_at is not None
