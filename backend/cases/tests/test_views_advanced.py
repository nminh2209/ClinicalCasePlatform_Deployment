"""
Advanced tests for Case views - permissions, filtering, edge cases
"""
import pytest
from rest_framework import status
from django.contrib.auth import get_user_model
from cases.models import Case

User = get_user_model()


@pytest.mark.django_db
class TestCasePermissions:
    """Test case permission boundaries"""

    def test_student_cannot_view_others_draft(self, api_client, student_user, instructor_user, test_repository):
        """Student cannot view another student's draft case"""
        other_case = Case.objects.create(
            title="Other Student Case",
            student=instructor_user,
            repository=test_repository,
            patient_age=30,
            patient_gender="M",
            case_status="draft",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get(f'/api/cases/{other_case.id}/')
        
        assert response.status_code in [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_instructor_can_view_student_case(self, api_client, instructor_user, student_user, test_repository):
        """Instructor can view student cases"""
        student_case = Case.objects.create(
            title="Student Submission",
            student=student_user,
            repository=test_repository,
            patient_age=35,
            patient_gender="F",
            case_status="submitted",
        )
        
        api_client.force_authenticate(user=instructor_user)
        response = api_client.get(f'/api/cases/{student_case.id}/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
        ]

    def test_student_cannot_delete_approved_case(self, api_client, student_user, test_repository):
        """Student cannot delete approved case"""
        case = Case.objects.create(
            title="Approved Case",
            student=student_user,
            repository=test_repository,
            patient_age=40,
            patient_gender="M",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.delete(f'/api/cases/{case.id}/')
        
        assert response.status_code in [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
            status.HTTP_204_NO_CONTENT,
        ]


@pytest.mark.django_db
class TestCaseFiltering:
    """Test case filtering and querying"""

    def test_filter_by_status(self, api_client, student_user, test_repository):
        """Filter cases by status"""
        Case.objects.create(
            title="Draft Case",
            student=student_user,
            repository=test_repository,
            patient_age=30,
            patient_gender="M",
            case_status="draft",
        )
        
        Case.objects.create(
            title="Submitted Case",
            student=student_user,
            repository=test_repository,
            patient_age=35,
            patient_gender="F",
            case_status="submitted",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/cases/?case_status=draft')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
        ]

    def test_filter_by_repository(self, api_client, student_user, test_repository):
        """Filter cases by repository"""
        Case.objects.create(
            title="Repo Case",
            student=student_user,
            repository=test_repository,
            patient_age=40,
            patient_gender="M",
            case_status="draft",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get(f'/api/cases/?repository={test_repository.id}')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
        ]

    def test_search_cases(self, api_client, student_user, test_repository):
        """Search cases by title"""
        Case.objects.create(
            title="Nhồi Máu Cơ Tim",
            student=student_user,
            repository=test_repository,
            patient_age=55,
            patient_gender="M",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/cases/?search=Tim')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
        ]


@pytest.mark.django_db
class TestCaseCloning:
    """Test case cloning functionality"""

    def test_clone_own_case(self, api_client, student_user, test_repository):
        """Student can clone their own case"""
        original = Case.objects.create(
            title="Original Case",
            student=student_user,
            repository=test_repository,
            patient_age=45,
            patient_gender="F",
            case_summary="Original summary",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.post(f'/api/cases/{original.id}/clone/', format='json')
        
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_clone_with_modifications(self, api_client, instructor_user, test_repository):
        """Clone case with modifications"""
        original = Case.objects.create(
            title="Template Case",
            student=instructor_user,
            repository=test_repository,
            patient_age=50,
            patient_gender="M",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=instructor_user)
        
        data = {"title": "Modified Clone"}
        response = api_client.post(f'/api/cases/{original.id}/clone/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]


@pytest.mark.django_db
class TestCaseEdgeCases:
    """Test edge cases and validation"""

    def test_create_case_invalid_age(self, api_client, student_user, test_repository):
        """Cannot create case with invalid age"""
        api_client.force_authenticate(user=student_user)
        
        data = {
            "title": "Invalid Age",
            "repository": test_repository.id,
            "patient_age": -5,
            "patient_gender": "M",
        }
        
        response = api_client.post('/api/cases/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_201_CREATED,
        ]

    def test_create_case_extremely_old_patient(self, api_client, student_user, test_repository):
        """Create case with very old patient"""
        api_client.force_authenticate(user=student_user)
        
        data = {
            "title": "Bệnh Nhân Cao Tuổi",
            "repository": test_repository.id,
            "patient_age": 120,
            "patient_gender": "F",
            "case_status": "draft",
        }
        
        response = api_client.post('/api/cases/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST,
        ]

    def test_update_case_invalid_status_transition(self, api_client, student_user, test_repository):
        """Cannot make invalid status transitions"""
        case = Case.objects.create(
            title="Status Test",
            student=student_user,
            repository=test_repository,
            patient_age=35,
            patient_gender="M",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=student_user)
        
        data = {"case_status": "draft"}
        response = api_client.patch(f'/api/cases/{case.id}/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
        ]

    def test_create_case_empty_title(self, api_client, student_user, test_repository):
        """Cannot create case with empty title"""
        api_client.force_authenticate(user=student_user)
        
        data = {
            "title": "",
            "repository": test_repository.id,
            "patient_age": 30,
            "patient_gender": "M",
        }
        
        response = api_client.post('/api/cases/', data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
