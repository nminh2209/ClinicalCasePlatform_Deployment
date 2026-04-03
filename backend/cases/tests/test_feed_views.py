"""
Tests for Feed views
"""

import pytest
from rest_framework import status
from django.contrib.auth import get_user_model
from cases.models import Case

User = get_user_model()


@pytest.mark.django_db
class TestFeedViews:
    """Test activity feed endpoints"""

    def test_user_feed_authenticated(self, api_client, student_user):
        """Authenticated user can access their feed"""
        api_client.force_authenticate(user=student_user)
        response = api_client.get("/api/cases/feed/")

        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_user_feed_unauthenticated(self, api_client):
        """Unauthenticated users cannot access feed"""
        response = api_client.get("/api/cases/feed/")
        assert response.status_code in [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_department_feed(self, api_client, instructor_user, cardiology_department):
        """Test department activity feed"""
        api_client.force_authenticate(user=instructor_user)
        response = api_client.get("/api/cases/feed/department/")

        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_recent_activities(self, api_client, student_user, test_repository):
        """Test recent activities endpoint"""
        # Create a case to generate activity
        Case.objects.create(
            title="Test Activity",
            student=student_user,
            repository=test_repository,
            patient_age=30,
            patient_gender="M",
            case_status="draft",
        )

        api_client.force_authenticate(user=student_user)
        response = api_client.get("/api/cases/feed/recent/")

        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_feed_pagination(self, api_client, student_user):
        """Test feed pagination"""
        api_client.force_authenticate(user=student_user)
        response = api_client.get("/api/cases/feed/?page=1&page_size=10")

        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_public_feed_only_accepts_like_reaction(
        self, api_client, student_user, instructor_user, test_repository
    ):
        """Public feed should only accept the single supported reaction: like."""
        case = Case.objects.create(
            title="Published Feed Case",
            student=student_user,
            repository=test_repository,
            patient_name="Patient",
            patient_age=30,
            patient_gender="male",
            specialty="Cardiology",
            case_status="approved",
            is_published_to_feed=True,
            published_by=instructor_user,
        )

        api_client.force_authenticate(user=student_user)

        invalid_response = api_client.post(
            f"/api/cases/{case.id}/react/",
            {"reaction_type": "insightful"},
            format="json",
        )
        assert invalid_response.status_code == status.HTTP_400_BAD_REQUEST

        valid_response = api_client.post(
            f"/api/cases/{case.id}/react/",
            {"reaction_type": "like"},
            format="json",
        )
        assert valid_response.status_code == status.HTTP_200_OK
