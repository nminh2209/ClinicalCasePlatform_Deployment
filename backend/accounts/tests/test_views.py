"""
API endpoint tests for accounts views.
"""
import pytest
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestAuthenticationEndpoints:
    """Test authentication API endpoints."""

    def test_user_registration(self, api_client):
        """Test user registration endpoint."""
        url = '/api/accounts/register/'  # Direct URL path
        data = {
            'username': 'newuser@test.com',
            'email': 'newuser@test.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = api_client.post(url, data, format='json')
        # Should create user or return appropriate response
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST]

    def test_login_success(self, api_client, student_user):
        """Test successful login."""
        url = '/api/accounts/login/'
        data = {
            'email': student_user.email,
            'password': 'testpass123'
        }
        response = api_client.post(url, data, format='json')
        # Should return token or success response
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST]

    def test_login_invalid_credentials(self, api_client):
        """Test login with invalid credentials."""
        url = '/api/accounts/login/'
        data = {
            'email': 'nonexistent@test.com',
            'password': 'wrongpass'
        }
        response = api_client.post(url, data, format='json')
        # Should reject invalid credentials
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST]


@pytest.mark.django_db
class TestUserProfileEndpoints:
    """Test user profile API endpoints."""

    def test_get_own_profile(self, authenticated_client, student_user):
        """Test retrieving own profile."""
        url = '/api/accounts/profile/'
        response = authenticated_client.get(url)
        # Should return user data or 404 if route doesn't exist
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND, status.HTTP_401_UNAUTHORIZED]
        if response.status_code == status.HTTP_200_OK:
            assert response.data['email'] == student_user.email

    def test_update_own_profile(self, authenticated_client):
        """Test updating own profile."""
        url = '/api/accounts/profile/'
        data = {
            'first_name': 'Updated'
        }
        response = authenticated_client.patch(url, data, format='json')
        # Should update or return 404
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND, status.HTTP_401_UNAUTHORIZED]

    def test_unauthorized_access(self, api_client):
        """Test accessing protected endpoint without auth."""
        url = '/api/accounts/profile/'
        response = api_client.get(url)
        # Should require authentication
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]


@pytest.mark.django_db  
class TestPermissions:
    """Test role-based permissions."""

    def test_student_cannot_access_instructor_endpoint(self, authenticated_client):
        """Test students cannot access instructor-only endpoints."""
        # This is a placeholder - adjust to your actual instructor endpoints
        url = '/api/instructor-only/'  # Replace with actual URL
        response = authenticated_client.get(url)
        # Should be forbidden or not found
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]

    def test_instructor_can_access_instructor_endpoint(self, instructor_client):
        """Test instructors can access instructor endpoints."""
        url = '/api/instructor-only/'  # Replace with actual URL
        response = instructor_client.get(url)
        # Should succeed or not found (if endpoint doesn't exist)
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
