"""
Tests for Case serializers.
"""
import pytest
from django.contrib.auth import get_user_model
from cases.serializers import CaseDetailSerializer, CaseListSerializer, CaseCreateUpdateSerializer
from cases.models import Case

User = get_user_model()


@pytest.mark.django_db
class TestCaseSerializer:
    """Test suite for CaseSerializer."""

    @pytest.fixture
    def case_data(self, student_user, test_repository):
        """Setup case test data."""
        return {
            'title': 'Test Case',
            'student': student_user.id,
            'repository': test_repository.id,
            'patient_name': 'Test Patient',
            'patient_age': 50,
            'patient_gender': 'male',
            'specialty': 'Cardiology'
        }

    def test_serialize_case(self, student_user, test_repository):
        """Test serializing case to JSON."""
        case = Case.objects.create(
            title='Serialization Test',
            student=student_user,
            repository=test_repository,
            patient_name='Patient',
            patient_age=45,
            patient_gender='female',
            specialty='Neurology'
        )
        
        serializer = CaseDetailSerializer(case)
        data = serializer.data
        
        assert data['title'] == 'Serialization Test'
        assert data['patient_name'] == 'Patient'
        assert data['patient_age'] == 45

    def test_list_serializer(self, student_user, test_repository):
        """Test CaseListSerializer."""
        case = Case.objects.create(
            title='List Test',
            student=student_user,
            repository=test_repository,
            patient_name='Patient',
            patient_age=50,
            patient_gender='male',
            specialty='Cardiology'
        )
        
        serializer = CaseListSerializer(case)
        data = serializer.data
        
        assert 'title' in data
        assert 'case_status' in data
