"""
Unit tests for feedback models
"""

import pytest
from django.contrib.auth import get_user_model
from feedback.models import Feedback

User = get_user_model()


@pytest.fixture
def instructor_user(db):
    """Create instructor user"""
    return User.objects.create_user(
        username="instructor_feedback",
        email="instructor@test.com",
        password="test123",
        role="instructor",
    )


@pytest.mark.django_db
def test_feedback_model_fields():
    """Test feedback model has correct fields"""
    assert hasattr(Feedback, 'case')
    assert hasattr(Feedback, 'instructor')
    assert hasattr(Feedback, 'content')
    assert hasattr(Feedback, 'feedback_type')
    assert hasattr(Feedback, 'is_public')


@pytest.mark.django_db  
def test_feedback_type_choices():
    """Test feedback type choices are defined"""
    assert Feedback.FeedbackType.GENERAL == "general"
    assert Feedback.FeedbackType.CLINICAL_REASONING == "clinical_reasoning"
    assert Feedback.FeedbackType.DOCUMENTATION == "documentation"
    assert Feedback.FeedbackType.PRESENTATION == "presentation"
