"""
Unit tests for Case model in cases app.
"""

import pytest
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone
from cases.models import Case
from cases.medical_models import Department
from repositories.models import Repository

User = get_user_model()


@pytest.mark.django_db
class TestCaseModel:
    """Test suite for the Case model."""

    @pytest.fixture
    def setup_test_data(self):
        """Setup common test data."""
        # Create department
        dept = Department.objects.create(
            name="Cardiology", code="CARD", vietnamese_name="Khoa Tim mạch"
        )

        # Create instructor
        instructor = User.objects.create_user(
            username="instructor@test.com",
            email="instructor@test.com",
            password="testpass123",
            role="instructor",
            first_name="Dr. Jane",
            last_name="Smith",
            department=dept,
        )

        # Create student
        student = User.objects.create_user(
            username="student@test.com",
            email="student@test.com",
            password="testpass123",
            role="student",
            first_name="John",
            last_name="Doe",
            department=dept,
        )

        # Create repository
        repository = Repository.objects.create(
            name="Test Repository", description="Test repository", owner=instructor
        )

        return {
            "dept": dept,
            "instructor": instructor,
            "student": student,
            "repository": repository,
        }

    def test_create_case_minimal_fields(self, setup_test_data):
        """Test creating a case with minimal required fields."""
        data = setup_test_data
        case = Case.objects.create(
            title="Test Case - Myocardial Infarction",
            student=data["student"],
            repository=data["repository"],
            patient_name="Test Patient",
            patient_age=55,
            patient_gender="male",
            specialty="Cardiology",
        )

        assert case.title == "Test Case - Myocardial Infarction"
        assert case.student == data["student"]
        assert case.patient_age == 55
        assert case.case_status == Case.StatusChoices.DRAFT
        assert not case.is_public
        assert not case.is_archived
        assert case.view_count == 0

    def test_case_status_choices(self, setup_test_data):
        """Test different case status transitions."""
        data = setup_test_data
        case = Case.objects.create(
            title="Status Test Case",
            student=data["student"],
            repository=data["repository"],
            patient_name="Patient",
            patient_age=30,
            patient_gender="female",
            specialty="General Medicine",
        )

        # Test status transitions
        assert case.case_status == Case.StatusChoices.DRAFT

        case.case_status = Case.StatusChoices.SUBMITTED
        case.save()
        assert case.case_status == Case.StatusChoices.SUBMITTED

        case.case_status = Case.StatusChoices.REVIEWED
        case.save()
        assert case.case_status == Case.StatusChoices.REVIEWED

        case.case_status = Case.StatusChoices.APPROVED
        case.save()
        assert case.case_status == Case.StatusChoices.APPROVED

    def test_case_priority_levels(self, setup_test_data):
        """Test case priority levels."""
        data = setup_test_data

        for priority in ["low", "medium", "high", "urgent"]:
            case = Case.objects.create(
                title=f"Priority {priority} Case",
                student=data["student"],
                repository=data["repository"],
                patient_name="Patient",
                patient_age=40,
                patient_gender="male",
                specialty="Emergency",
                priority_level=priority,
            )
            assert case.priority_level == priority

    def test_case_complexity_levels(self, setup_test_data):
        """Test case complexity levels."""
        data = setup_test_data

        for complexity in ["basic", "intermediate", "advanced", "expert"]:
            case = Case.objects.create(
                title=f"Complexity {complexity} Case",
                student=data["student"],
                repository=data["repository"],
                patient_name="Patient",
                patient_age=40,
                patient_gender="male",
                specialty="Medicine",
                complexity_level=complexity,
            )
            assert case.complexity_level == complexity

    def test_case_with_dates(self, setup_test_data):
        """Test case with admission and discharge dates."""
        data = setup_test_data
        admission = date.today() - timedelta(days=5)
        discharge = date.today()

        case = Case.objects.create(
            title="Date Test Case",
            student=data["student"],
            repository=data["repository"],
            patient_name="Patient",
            patient_age=45,
            patient_gender="male",
            specialty="Surgery",
            admission_date=admission,
            discharge_date=discharge,
        )

        assert case.admission_date == admission
        assert case.discharge_date == discharge

    def test_case_is_instructor_template(self, setup_test_data):
        """Test instructor template case."""
        data = setup_test_data
        template_case = Case.objects.create(
            title="Template Case",
            student=data["instructor"],
            repository=data["repository"],
            patient_name="Template Patient",
            patient_age=50,
            patient_gender="female",
            specialty="Cardiology",
            is_instructor_template=True,
        )
        assert template_case.student == data["instructor"]

    def test_case_cloning(self, setup_test_data):
        """Test case cloning functionality."""
        data = setup_test_data

        # Create original case
        original = Case.objects.create(
            title="Original Case",
            student=data["instructor"],
            repository=data["repository"],
            patient_name="Original Patient",
            patient_age=60,
            patient_gender="male",
            specialty="Cardiology",
            is_instructor_template=True,
        )

        # Create cloned case
        cloned = Case.objects.create(
            title="Cloned Case",
            student=data["student"],
            repository=data["repository"],
            patient_name="Cloned Patient",
            patient_age=60,
            patient_gender="male",
            specialty="Cardiology",
            cloned_from_title=original.title,
            cloned_from_instructor_name=original.published_by,
        )

        assert cloned.cloned_from_title == original.title
        assert original.clones.count() == 1
        assert original.clones.first() == cloned

    def test_case_view_count(self, setup_test_data):
        """Test case view count increment."""
        data = setup_test_data
        case = Case.objects.create(
            title="View Count Test",
            student=data["student"],
            repository=data["repository"],
            patient_name="Patient",
            patient_age=35,
            patient_gender="female",
            specialty="General",
        )

        assert case.view_count == 0

        case.view_count += 1
        case.save()
        assert case.view_count == 1

    def test_case_with_tags_and_keywords(self, setup_test_data):
        """Test case with learning tags and keywords."""
        data = setup_test_data
        case = Case.objects.create(
            title="Tagged Case",
            student=data["student"],
            repository=data["repository"],
            patient_name="Patient",
            patient_age=45,
            patient_gender="male",
            specialty="Cardiology",
            learning_tags="ecg,cardiac,emergency",
            keywords="heart attack,myocardial infarction,chest pain",
        )

        assert case.learning_tags == "ecg,cardiac,emergency"
        assert case.keywords == "heart attack,myocardial infarction,chest pain"

    def test_case_follow_up(self, setup_test_data):
        """Test case follow-up functionality."""
        data = setup_test_data
        follow_up = date.today() + timedelta(days=7)

        case = Case.objects.create(
            title="Follow-up Case",
            student=data["student"],
            repository=data["repository"],
            patient_name="Patient",
            patient_age=50,
            patient_gender="female",
            specialty="Medicine",
            requires_follow_up=True,
            follow_up_date=follow_up,
        )

        assert case.requires_follow_up
        assert case.follow_up_date == follow_up

    def test_case_archiving(self, setup_test_data):
        """Test case archiving."""
        data = setup_test_data
        case = Case.objects.create(
            title="Archive Test",
            student=data["student"],
            repository=data["repository"],
            patient_name="Patient",
            patient_age=40,
            patient_gender="male",
            specialty="General",
        )

        assert not case.is_archived

        case.is_archived = True
        case.save()
        assert case.is_archived

    def test_case_timestamps(self, setup_test_data):
        """Test case timestamps."""
        data = setup_test_data
        case = Case.objects.create(
            title="Timestamp Test",
            student=data["student"],
            repository=data["repository"],
            patient_name="Patient",
            patient_age=40,
            patient_gender="male",
            specialty="General",
        )

        assert case.created_at is not None
        assert case.updated_at is not None
        assert case.created_at <= case.updated_at
