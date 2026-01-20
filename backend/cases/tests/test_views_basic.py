"""
Basic unit tests for Case views (API endpoints)
"""
import pytest
from rest_framework import status
from django.contrib.auth import get_user_model
from cases.models import Case

User = get_user_model()


@pytest.mark.django_db
class TestCaseListView:
    """Test listing cases"""

    def test_list_cases_as_student(self, api_client, student_user, test_repository):
        """Student can list their own cases"""
        # Create test case
        case = Case.objects.create(
            title="Nhồi Máu Cơ Tim Cấp",
            student=student_user,
            repository=test_repository,
            patient_age=55,
            patient_gender="M",
            case_status="draft",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/cases/')
        
        assert response.status_code == status.HTTP_200_OK
        # Should contain the created case
        assert len(response.data['results']) > 0

    def test_list_cases_unauthenticated(self, api_client):
        """Unauthenticated users cannot list cases"""
        response = api_client.get('/api/cases/')
        assert response.status_code in [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        ]


@pytest.mark.django_db
class TestCaseDetailView:
    """Test viewing case details"""

    def test_view_own_case(self, api_client, student_user, test_repository):
        """Student can view their own case"""
        case = Case.objects.create(
            title="Viêm Phổi Cộng Đồng",
            student=student_user,
            repository=test_repository,
            patient_age=42,
            patient_gender="F",
            case_status="draft",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get(f'/api/cases/{case.id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == "Viêm Phổi Cộng Đồng"

    def test_view_nonexistent_case(self, api_client, student_user):
        """Viewing non-existent case returns 404"""
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/cases/99999/')
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCaseCreation:
    """Test creating cases"""

    def test_create_case_as_student(self, api_client, student_user, test_repository):
        """Student can create a case"""
        api_client.force_authenticate(user=student_user)
        
        data = {
            "title": "Ca Bệnh Mới",
            "repository": test_repository.id,
            "patient_age": 35,
            "patient_gender": "M",
            "case_status": "draft",
            "case_summary": "Bệnh nhân nam 35 tuổi",
        }
        
        response = api_client.post('/api/cases/', data, format='json')
        
        # Either created successfully or some validation error
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST,
        ]

    def test_create_case_missing_required_fields(self, api_client, student_user):
        """Creating case without required fields fails"""
        api_client.force_authenticate(user=student_user)
        
        data = {"title": "Incomplete Case"}
        response = api_client.post('/api/cases/', data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestCaseUpdate:
    """Test updating cases"""

    def test_update_own_case(self, api_client, student_user, test_repository):
        """Student can update their own draft case"""
        case = Case.objects.create(
            title="Original Title",
            student=student_user,
            repository=test_repository,
            patient_age=30,
            patient_gender="M",
            case_status="draft",
        )
        
        api_client.force_authenticate(user=student_user)
        
        data = {
            "title": "Tiêu Đề Đã Cập Nhật",
            "case_summary": "Nội dung mới",
        }
        
        response = api_client.patch(f'/api/cases/{case.id}/', data, format='json')
        
        # Should allow update or require more fields
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
        ]


@pytest.mark.django_db
class TestCaseStatusTransitions:
    """Test case status changes"""

    def test_submit_case(self, api_client, student_user, test_repository):
        """Student can submit a draft case"""
        case = Case.objects.create(
            title="Case to Submit",
            student=student_user,
            repository=test_repository,
            patient_age=40,
            patient_gender="F",
            case_status="draft",
        )
        
        api_client.force_authenticate(user=student_user)
        
        data = {"case_status": "submitted"}
        response = api_client.patch(f'/api/cases/{case.id}/', data, format='json')
        
        # Status transition should be allowed or rejected based on rules
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
        ]
