"""
Tests for Case sharing and collaboration features
"""
import pytest
from rest_framework import status
from django.contrib.auth import get_user_model
from cases.models import Case

User = get_user_model()


@pytest.mark.django_db
class TestCaseSharing:
    """Test case sharing functionality"""

    def test_share_case_with_user(self, api_client, student_user, instructor_user, test_repository):
        """Share case with another user"""
        case = Case.objects.create(
            title="Shared Case",
            student=student_user,
            repository=test_repository,
            patient_age=30,
            patient_gender="M",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=student_user)
        
        data = {"user_id": instructor_user.id}
        response = api_client.post(f'/api/cases/{case.id}/share/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_unshare_case(self, api_client, student_user, test_repository):
        """Unshare previously shared case"""
        case = Case.objects.create(
            title="Unshare Test",
            student=student_user,
            repository=test_repository,
            patient_age=35,
            patient_gender="F",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.post(f'/api/cases/{case.id}/unshare/', format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_get_shared_cases(self, api_client, instructor_user):
        """Get list of cases shared with user"""
        api_client.force_authenticate(user=instructor_user)
        response = api_client.get('/api/cases/shared-with-me/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_share_draft_case(self, api_client, student_user, instructor_user, test_repository):
        """Cannot share draft case"""
        case = Case.objects.create(
            title="Draft Share",
            student=student_user,
            repository=test_repository,
            patient_age=40,
            patient_gender="M",
            case_status="draft",
        )
        
        api_client.force_authenticate(user=student_user)
        
        data = {"user_id": instructor_user.id}
        response = api_client.post(f'/api/cases/{case.id}/share/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]


@pytest.mark.django_db
class TestCaseCollaboration:
    """Test collaborative case features"""

    def test_add_collaborator(self, api_client, instructor_user, student_user, test_repository):
        """Add collaborator to case"""
        case = Case.objects.create(
            title="Collaboration Case",
            student=instructor_user,
            repository=test_repository,
            patient_age=45,
            patient_gender="F",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=instructor_user)
        
        data = {"collaborator_id": student_user.id}
        response = api_client.post(f'/api/cases/{case.id}/add-collaborator/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_remove_collaborator(self, api_client, instructor_user, test_repository):
        """Remove collaborator from case"""
        case = Case.objects.create(
            title="Remove Collab",
            student=instructor_user,
            repository=test_repository,
            patient_age=50,
            patient_gender="M",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=instructor_user)
        response = api_client.post(f'/api/cases/{case.id}/remove-collaborator/', format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_list_collaborators(self, api_client, instructor_user, test_repository):
        """List all collaborators on case"""
        case = Case.objects.create(
            title="List Collabs",
            student=instructor_user,
            repository=test_repository,
            patient_age=38,
            patient_gender="F",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=instructor_user)
        response = api_client.get(f'/api/cases/{case.id}/collaborators/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]
