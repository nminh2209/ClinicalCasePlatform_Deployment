"""
Test case creation to debug the 400 error
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Case
from .medical_models import Department
from repositories.models import Repository

User = get_user_model()


class CaseCreationTest(APITestCase):
    """Test case creation to debug 400 errors"""

    def setUp(self):
        # Create test user
        self.student = User.objects.create_user(  # type: ignore[attr-defined]
            username="teststudent@test.com",
            email="teststudent@test.com",
            password="testpass123",
            role="student",
            first_name="Test",
            last_name="Student",
        )

        # Create repository
        self.repository = Repository.objects.create(
            name="Test Repository",
            description="Test repo",
            owner=self.student,
            is_public=True,
        )

    def test_case_creation_minimal(self):
        """Test creating a case with minimal data"""
        self.client.force_authenticate(user=self.student)

        # Minimal payload that should work
        data = {
            "title": "Test Case",
            "patient_name": "Test Patient",
            "patient_age": 30,
            "patient_gender": "male",
            "specialty": "General",
            "repository": self.repository.id,  # type: ignore[attr-defined]
            "clinical_history": {"chief_complaint": "Test complaint"},
        }

        print("=== SENDING PAYLOAD ===")
        print(data)

        response = self.client.post("/api/cases/", data, format="json")

        print("=== RESPONSE ===")
        print(f"Status: {response.status_code}")
        if response.status_code != 201:
            print(f"Error: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

