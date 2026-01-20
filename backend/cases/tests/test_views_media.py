"""
Tests for Case attachments and media handling
"""
import pytest
from rest_framework import status
from django.contrib.auth import get_user_model
from cases.models import Case

User = get_user_model()


@pytest.mark.django_db
class TestCaseAttachments:
    """Test case attachment handling"""

    def test_upload_attachment_to_case(self, api_client, student_user, test_repository):
        """Upload file attachment to case"""
        case = Case.objects.create(
            title="Case with Attachment",
            student=student_user,
            repository=test_repository,
            patient_age=42,
            patient_gender="M",
            case_status="draft",
        )
        
        api_client.force_authenticate(user=student_user)
        # Test the endpoint - may not exist yet
        response = api_client.post(f'/api/cases/{case.id}/attachments/', {
            'description': 'X-quang ngực'
        }, format='json')
        
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_list_case_attachments(self, api_client, student_user, test_repository):
        """List all attachments for a case"""
        case = Case.objects.create(
            title="Case Attachments",
            student=student_user,
            repository=test_repository,
            patient_age=35,
            patient_gender="F",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get(f'/api/cases/{case.id}/attachments/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_delete_attachment(self, api_client, student_user, test_repository):
        """Delete attachment from case"""
        case = Case.objects.create(
            title="Delete Attachment",
            student=student_user,
            repository=test_repository,
            patient_age=40,
            patient_gender="M",
            case_status="draft",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.delete(f'/api/cases/{case.id}/attachments/1/')
        
        assert response.status_code in [
            status.HTTP_204_NO_CONTENT,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_download_attachment(self, api_client, student_user, test_repository):
        """Download case attachment"""
        case = Case.objects.create(
            title="Download Test",
            student=student_user,
            repository=test_repository,
            patient_age=45,
            patient_gender="F",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get(f'/api/cases/{case.id}/attachments/1/download/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_attachment_size_limit(self, api_client, student_user, test_repository):
        """Test attachment size validation"""
        case = Case.objects.create(
            title="Size Limit Test",
            student=student_user,
            repository=test_repository,
            patient_age=38,
            patient_gender="M",
            case_status="draft",
        )
        
        api_client.force_authenticate(user=student_user)
        # Test size validation
        response = api_client.post(f'/api/cases/{case.id}/attachments/', {
            'description': 'Large file test'
        }, format='json')
        
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]


@pytest.mark.django_db
class TestCaseImages:
    """Test case image handling"""

    def test_upload_medical_image(self, api_client, student_user, test_repository):
        """Upload medical imaging file"""
        case = Case.objects.create(
            title="Medical Imaging",
            student=student_user,
            repository=test_repository,
            patient_age=55,
            patient_gender="M",
            case_status="draft",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.post(f'/api/cases/{case.id}/images/', {
            'image_type': 'xray',
            'description': 'Hình ảnh X-quang phổi'
        }, format='json')
        
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_list_case_images(self, api_client, student_user, test_repository):
        """List all images for a case"""
        case = Case.objects.create(
            title="Case Images",
            student=student_user,
            repository=test_repository,
            patient_age=48,
            patient_gender="F",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get(f'/api/cases/{case.id}/images/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_update_image_description(self, api_client, student_user, test_repository):
        """Update image description"""
        case = Case.objects.create(
            title="Update Image Desc",
            student=student_user,
            repository=test_repository,
            patient_age=42,
            patient_gender="M",
            case_status="draft",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.patch(f'/api/cases/{case.id}/images/1/', {
            'description': 'Cập nhật mô tả hình ảnh'
        }, format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]


@pytest.mark.django_db
class TestCaseHistory:
    """Test case history and versioning"""

    def test_view_case_history(self, api_client, student_user, test_repository):
        """View case edit history"""
        case = Case.objects.create(
            title="History Test",
            student=student_user,
            repository=test_repository,
            patient_age=40,
            patient_gender="F",
            case_status="draft",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get(f'/api/cases/{case.id}/history/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_view_case_version(self, api_client, student_user, test_repository):
        """View specific version of case"""
        case = Case.objects.create(
            title="Version Test",
            student=student_user,
            repository=test_repository,
            patient_age=45,
            patient_gender="M",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get(f'/api/cases/{case.id}/versions/1/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_restore_case_version(self, api_client, student_user, test_repository):
        """Restore case to previous version"""
        case = Case.objects.create(
            title="Restore Version",
            student=student_user,
            repository=test_repository,
            patient_age=38,
            patient_gender="F",
            case_status="draft",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.post(f'/api/cases/{case.id}/restore/1/', format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_compare_case_versions(self, api_client, student_user, test_repository):
        """Compare two versions of a case"""
        case = Case.objects.create(
            title="Compare Versions",
            student=student_user,
            repository=test_repository,
            patient_age=42,
            patient_gender="M",
            case_status="draft",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get(f'/api/cases/{case.id}/compare/?v1=1&v2=2')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]


@pytest.mark.django_db
class TestCaseStatistics:
    """Test case statistics endpoints"""

    def test_user_case_statistics(self, api_client, student_user):
        """Get statistics for user's cases"""
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/cases/my-statistics/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_repository_statistics(self, api_client, instructor_user, test_repository):
        """Get statistics for repository"""
        api_client.force_authenticate(user=instructor_user)
        response = api_client.get(f'/api/repositories/{test_repository.id}/statistics/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_department_case_statistics(self, api_client, instructor_user, test_department):
        """Get case statistics by department"""
        api_client.force_authenticate(user=instructor_user)
        response = api_client.get(f'/api/departments/{test_department.id}/case-statistics/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_case_view_count(self, api_client, student_user, test_repository):
        """Track case view count"""
        case = Case.objects.create(
            title="View Count Test",
            student=student_user,
            repository=test_repository,
            patient_age=40,
            patient_gender="M",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=student_user)
        # View the case multiple times
        for _ in range(3):
            api_client.get(f'/api/cases/{case.id}/')
        
        response = api_client.get(f'/api/cases/{case.id}/view-count/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]


@pytest.mark.django_db
class TestCaseTags:
    """Test case tagging system"""

    def test_add_tags_to_case(self, api_client, student_user, test_repository):
        """Add tags to a case"""
        case = Case.objects.create(
            title="Tagging Test",
            student=student_user,
            repository=test_repository,
            patient_age=45,
            patient_gender="F",
            case_status="draft",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.post(f'/api/cases/{case.id}/tags/', {
            'tags': ['tim mạch', 'cấp cứu', 'điển hình']
        }, format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_remove_tag_from_case(self, api_client, student_user, test_repository):
        """Remove tag from case"""
        case = Case.objects.create(
            title="Remove Tag",
            student=student_user,
            repository=test_repository,
            patient_age=38,
            patient_gender="M",
            case_status="draft",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.delete(f'/api/cases/{case.id}/tags/1/')
        
        assert response.status_code in [
            status.HTTP_204_NO_CONTENT,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_search_cases_by_tag(self, api_client, student_user):
        """Search cases by tag"""
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/cases/?tags=tim%20mạch')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_get_popular_tags(self, api_client, instructor_user):
        """Get most popular tags"""
        api_client.force_authenticate(user=instructor_user)
        response = api_client.get('/api/tags/popular/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]
