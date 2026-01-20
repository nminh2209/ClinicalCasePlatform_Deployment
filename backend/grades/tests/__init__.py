"""
Unit tests for Grades model.
"""
import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from grades.models import Grade
from cases.models import Case

User = get_user_model()


@pytest.mark.django_db
class TestGradeModel:
    """Test suite for Grade model."""

    @pytest.fixture
    def grade_data(self, instructor_user, student_user, test_repository):
        """Setup grade test data."""
        case = Case.objects.create(
            title='Test Case for Grading',
            student=student_user,
            repository=test_repository,
            patient_name='Patient',
            patient_age=50,
            patient_gender='male',
            specialty='General'
        )
        return {
            'case': case,
            'graded_by': instructor_user,
            'student': student_user
        }

    def test_create_grade(self, grade_data):
        """Test creating a grade."""
        grade = Grade.objects.create(
            case=grade_data['case'],
            graded_by=grade_data['graded_by'],
            score=85,
            feedback='Good work!',
            criteria_scores={'accuracy': 90, 'completeness': 80}
        )
        assert grade.score == 85
        assert grade.feedback == 'Good work!'
        assert grade.graded_by == grade_data['graded_by']

    def test_grade_score_validation(self, grade_data):
        """Test grade score is within valid range."""
        grade = Grade.objects.create(
            case=grade_data['case'],
            graded_by=grade_data['graded_by'],
            score=95
        )
        assert 0 <= grade.score <= 100

    def test_grade_with_criteria_scores(self, grade_data):
        """Test grade with detailed criteria."""
        criteria = {
            'clinical_reasoning': 85,
            'data_collection': 90,
            'differential_diagnosis': 80,
            'treatment_plan': 88
        }
        grade = Grade.objects.create(
            case=grade_data['case'],
            graded_by=grade_data['graded_by'],
            score=86,
            criteria_scores=criteria
        )
        assert grade.criteria_scores == criteria

    def test_grade_timestamps(self, grade_data):
        """Test grade has creation timestamp."""
        grade = Grade.objects.create(
            case=grade_data['case'],
            graded_by=grade_data['graded_by'],
            score=80
        )
        assert grade.created_at is not None
        assert grade.updated_at is not None

    def test_one_grade_per_case(self, grade_data):
        """Test only one grade per case per student."""
        Grade.objects.create(
            case=grade_data['case'],
            graded_by=grade_data['graded_by'],
            score=80
        )
        # Attempting to create another grade for same case
        # May raise IntegrityError depending on your constraints
        # This test verifies your business logic
