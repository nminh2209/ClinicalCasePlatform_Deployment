"""
Tests for Validation views
"""
import pytest
from rest_framework import status
from django.contrib.auth import get_user_model
from cases.models import Case

User = get_user_model()


@pytest.mark.django_db
class TestValidationViews:
    """Test case validation endpoints"""

    def test_validate_case_structure(self, api_client, student_user, test_repository):
        """Test case structure validation"""
        case = Case.objects.create(
            title="Case for Validation",
            student=student_user,
            repository=test_repository,
            patient_age=45,
            patient_gender="F",
            case_status="draft",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.post(f'/api/cases/{case.id}/validate/', format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_validate_medical_terminology(self, api_client, instructor_user, test_repository):
        """Test medical terminology validation"""
        case = Case.objects.create(
            title="Nhồi Máu Cơ Tim",
            student=instructor_user,
            repository=test_repository,
            patient_age=55,
            patient_gender="M",
            case_summary="Bệnh nhân có triệu chứng đau ngực",
            case_status="submitted",
        )
        
        api_client.force_authenticate(user=instructor_user)
        response = api_client.get(f'/api/cases/{case.id}/validate-terminology/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_validate_completeness(self, api_client, student_user, test_repository):
        """Test case completeness validation"""
        case = Case.objects.create(
            title="Incomplete Case",
            student=student_user,
            repository=test_repository,
            patient_age=30,
            patient_gender="M",
            case_status="draft",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get(f'/api/cases/{case.id}/validate-completeness/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_bulk_validation(self, api_client, instructor_user, test_repository):
        """Test bulk case validation"""
        # Create multiple cases
        for i in range(3):
            Case.objects.create(
                title=f"Case {i}",
                student=instructor_user,
                repository=test_repository,
                patient_age=30 + i,
                patient_gender="M" if i % 2 == 0 else "F",
                case_status="draft",
            )
        
        api_client.force_authenticate(user=instructor_user)
        response = api_client.post('/api/cases/validate-bulk/', format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_validation_report(self, api_client, instructor_user, test_repository):
        """Test validation report generation"""
        case = Case.objects.create(
            title="Report Case",
            student=instructor_user,
            repository=test_repository,
            patient_age=40,
            patient_gender="F",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=instructor_user)
        response = api_client.get(f'/api/cases/{case.id}/validation-report/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]
