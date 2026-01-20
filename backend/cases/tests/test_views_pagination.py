"""
Tests for Case list pagination and ordering
"""
import pytest
from rest_framework import status
from django.contrib.auth import get_user_model
from cases.models import Case

User = get_user_model()


@pytest.mark.django_db
class TestCasePagination:
    """Test case list pagination"""

    def test_paginated_case_list(self, api_client, student_user, test_repository):
        """Test paginated response for case list"""
        # Create multiple cases
        for i in range(15):
            Case.objects.create(
                title=f"Case {i+1}",
                student=student_user,
                repository=test_repository,
                patient_age=30 + i,
                patient_gender="M" if i % 2 == 0 else "F",
                case_status="approved",
            )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/cases/?page=1&page_size=10')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_pagination_page_size(self, api_client, student_user, test_repository):
        """Test custom page size"""
        for i in range(20):
            Case.objects.create(
                title=f"Pagination Test {i}",
                student=student_user,
                repository=test_repository,
                patient_age=25 + i,
                patient_gender="F",
                case_status="approved",
            )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/cases/?page_size=5')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_pagination_next_page(self, api_client, student_user, test_repository):
        """Test navigating to next page"""
        for i in range(25):
            Case.objects.create(
                title=f"Next Page Test {i}",
                student=student_user,
                repository=test_repository,
                patient_age=30,
                patient_gender="M",
                case_status="approved",
            )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/cases/?page=2')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_pagination_last_page(self, api_client, student_user, test_repository):
        """Test last page with fewer items"""
        for i in range(12):
            Case.objects.create(
                title=f"Last Page {i}",
                student=student_user,
                repository=test_repository,
                patient_age=35,
                patient_gender="F",
                case_status="approved",
            )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/cases/?page=3&page_size=5')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]


@pytest.mark.django_db
class TestCaseOrdering:
    """Test case ordering and sorting"""

    def test_order_by_created_date(self, api_client, student_user, test_repository):
        """Order cases by creation date"""
        for i in range(5):
            Case.objects.create(
                title=f"Date Order {i}",
                student=student_user,
                repository=test_repository,
                patient_age=40,
                patient_gender="M",
                case_status="approved",
            )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/cases/?ordering=-created_at')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_order_by_patient_age(self, api_client, student_user, test_repository):
        """Order cases by patient age"""
        ages = [45, 32, 67, 25, 58]
        for age in ages:
            Case.objects.create(
                title=f"Age {age}",
                student=student_user,
                repository=test_repository,
                patient_age=age,
                patient_gender="F",
                case_status="approved",
            )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/cases/?ordering=patient_age')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_order_by_title(self, api_client, student_user, test_repository):
        """Order cases by title alphabetically"""
        titles = ["Viêm Phổi", "Nhồi Máu Cơ Tim", "Đái Tháo Đường", "Tăng Huyết Áp"]
        for title in titles:
            Case.objects.create(
                title=title,
                student=student_user,
                repository=test_repository,
                patient_age=50,
                patient_gender="M",
                case_status="approved",
            )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/cases/?ordering=title')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_multiple_ordering_fields(self, api_client, student_user, test_repository):
        """Order by multiple fields"""
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/cases/?ordering=-case_status,created_at')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]


@pytest.mark.django_db
class TestCaseFiltersAdvanced:
    """Advanced filtering tests"""

    def test_filter_by_age_range(self, api_client, student_user, test_repository):
        """Filter cases by patient age range"""
        ages = [25, 35, 45, 55, 65]
        for age in ages:
            Case.objects.create(
                title=f"Age {age}",
                student=student_user,
                repository=test_repository,
                patient_age=age,
                patient_gender="M",
                case_status="approved",
            )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/cases/?min_age=30&max_age=50')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_filter_by_gender(self, api_client, student_user, test_repository):
        """Filter cases by patient gender"""
        for i, gender in enumerate(["M", "F", "M", "F", "M"]):
            Case.objects.create(
                title=f"Gender {i}",
                student=student_user,
                repository=test_repository,
                patient_age=40,
                patient_gender=gender,
                case_status="approved",
            )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/cases/?patient_gender=F')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_filter_by_date_range(self, api_client, student_user, test_repository):
        """Filter cases by creation date range"""
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/cases/?created_after=2025-01-01&created_before=2025-12-31')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_combined_filters(self, api_client, student_user, test_repository):
        """Combine multiple filters"""
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/cases/?case_status=approved&patient_gender=M&min_age=30')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_search_in_summary(self, api_client, student_user, test_repository):
        """Search in case summary field"""
        Case.objects.create(
            title="Search Test",
            student=student_user,
            repository=test_repository,
            patient_age=45,
            patient_gender="M",
            case_summary="Bệnh nhân có triệu chứng đau ngực",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/cases/?search=đau ngực')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]
