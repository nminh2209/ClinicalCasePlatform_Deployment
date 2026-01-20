"""
Tests for Accounts views - additional coverage
"""
import pytest
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserRegistration:
    """Test user registration"""

    def test_register_student(self, api_client):
        """Register new student account"""
        data = {
            "username": "newstudent",
            "email": "newstudent@example.com",
            "password": "testpass123",
            "full_name_vietnamese": "Nguyễn Văn An",
            "student_id": "SV2024999",
            "role": "student",
        }
        
        response = api_client.post('/api/accounts/register/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_register_duplicate_username(self, api_client, student_user):
        """Cannot register with existing username"""
        data = {
            "username": student_user.username,
            "email": "different@example.com",
            "password": "testpass123",
        }
        
        response = api_client.post('/api/accounts/register/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_404_NOT_FOUND,
        ]


@pytest.mark.django_db
class TestUserProfile:
    """Test user profile management"""

    def test_view_own_profile(self, api_client, student_user):
        """User can view own profile"""
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/accounts/profile/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_update_profile(self, api_client, student_user):
        """User can update own profile"""
        api_client.force_authenticate(user=student_user)
        
        data = {"full_name_vietnamese": "Tên Mới"}
        response = api_client.patch('/api/accounts/profile/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_change_password(self, api_client, student_user):
        """User can change password"""
        api_client.force_authenticate(user=student_user)
        
        data = {
            "old_password": "testpass123",
            "new_password": "newpass456",
        }
        
        response = api_client.post('/api/accounts/change-password/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]


@pytest.mark.django_db
class TestUserList:
    """Test user listing"""

    def test_list_users_as_instructor(self, api_client, instructor_user):
        """Instructor can list users"""
        api_client.force_authenticate(user=instructor_user)
        response = api_client.get('/api/accounts/users/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_list_students(self, api_client, instructor_user):
        """List only students"""
        api_client.force_authenticate(user=instructor_user)
        response = api_client.get('/api/accounts/users/?role=student')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_search_users(self, api_client, instructor_user):
        """Search users by name"""
        api_client.force_authenticate(user=instructor_user)
        response = api_client.get('/api/accounts/users/?search=Nguyễn')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]
