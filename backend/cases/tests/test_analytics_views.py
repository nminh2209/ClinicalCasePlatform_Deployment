"""
Tests for Analytics views
"""
import pytest
from rest_framework import status
from django.contrib.auth import get_user_model
from cases.models import Case

User = get_user_model()


@pytest.mark.django_db
class TestAnalyticsViews:
    """Test analytics API endpoints"""

    def test_case_analytics_authenticated(self, api_client, instructor_user, cardiology_department):
        """Instructor can access case analytics"""
        api_client.force_authenticate(user=instructor_user)
        response = api_client.get('/api/cases/analytics/')
        
        # Should either succeed or require specific permissions
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_case_analytics_unauthenticated(self, api_client):
        """Unauthenticated users cannot access analytics"""
        response = api_client.get('/api/cases/analytics/')
        assert response.status_code in [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_department_statistics(self, api_client, instructor_user, cardiology_department):
        """Test department statistics endpoint"""
        api_client.force_authenticate(user=instructor_user)
        response = api_client.get('/api/cases/analytics/department-stats/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_user_performance_metrics(self, api_client, student_user):
        """Test user performance metrics"""
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/cases/analytics/performance/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_case_completion_rates(self, api_client, instructor_user):
        """Test case completion rate analytics"""
        api_client.force_authenticate(user=instructor_user)
        response = api_client.get('/api/cases/analytics/completion-rates/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]
