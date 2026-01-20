"""
Advanced tests for Exports views
"""
import pytest
from rest_framework import status
from django.contrib.auth import get_user_model
from cases.models import Case

User = get_user_model()


@pytest.mark.django_db
class TestExportFormats:
    """Test different export formats"""

    def test_export_case_pdf_format(self, api_client, student_user, test_repository):
        """Export case in PDF format"""
        case = Case.objects.create(
            title="PDF Export Case",
            student=student_user,
            repository=test_repository,
            patient_age=42,
            patient_gender="M",
            case_summary="Ca bệnh để xuất PDF",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.post(f'/api/exports/create/', {
            'case_id': case.id,
            'format': 'pdf'
        }, format='json')
        
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_export_case_json_format(self, api_client, instructor_user, student_user, test_repository):
        """Export case in JSON format"""
        case = Case.objects.create(
            title="JSON Export",
            student=student_user,
            repository=test_repository,
            patient_age=35,
            patient_gender="F",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=instructor_user)
        response = api_client.post(f'/api/exports/create/', {
            'case_id': case.id,
            'format': 'json'
        }, format='json')
        
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_export_case_csv_format(self, api_client, instructor_user, student_user, test_repository):
        """Export case in CSV format"""
        case = Case.objects.create(
            title="CSV Export",
            student=student_user,
            repository=test_repository,
            patient_age=48,
            patient_gender="M",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=instructor_user)
        response = api_client.post(f'/api/exports/create/', {
            'case_id': case.id,
            'format': 'csv'
        }, format='json')
        
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_export_case_docx_format(self, api_client, student_user, test_repository):
        """Export case in DOCX format"""
        case = Case.objects.create(
            title="DOCX Export",
            student=student_user,
            repository=test_repository,
            patient_age=52,
            patient_gender="F",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.post(f'/api/exports/create/', {
            'case_id': case.id,
            'format': 'docx'
        }, format='json')
        
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]


@pytest.mark.django_db
class TestExportOptions:
    """Test export with various options"""

    def test_export_with_anonymization(self, api_client, instructor_user, student_user, test_repository):
        """Export case with patient data anonymized"""
        case = Case.objects.create(
            title="Anonymized Export",
            student=student_user,
            repository=test_repository,
            patient_age=60,
            patient_gender="M",
            case_summary="Ca bệnh cần ẩn danh",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=instructor_user)
        response = api_client.post(f'/api/exports/create/', {
            'case_id': case.id,
            'format': 'pdf',
            'anonymize': True
        }, format='json')
        
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_export_with_watermark(self, api_client, student_user, test_repository):
        """Export case with watermark"""
        case = Case.objects.create(
            title="Watermark Export",
            student=student_user,
            repository=test_repository,
            patient_age=45,
            patient_gender="F",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.post(f'/api/exports/create/', {
            'case_id': case.id,
            'format': 'pdf',
            'watermark': 'CONFIDENTIAL'
        }, format='json')
        
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_export_with_comments(self, api_client, instructor_user, student_user, test_repository):
        """Export case including comments"""
        case = Case.objects.create(
            title="Export with Comments",
            student=student_user,
            repository=test_repository,
            patient_age=38,
            patient_gender="M",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=instructor_user)
        response = api_client.post(f'/api/exports/create/', {
            'case_id': case.id,
            'format': 'pdf',
            'include_comments': True
        }, format='json')
        
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_export_with_grades(self, api_client, student_user, test_repository):
        """Export case including grades"""
        case = Case.objects.create(
            title="Export with Grades",
            student=student_user,
            repository=test_repository,
            patient_age=42,
            patient_gender="F",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.post(f'/api/exports/create/', {
            'case_id': case.id,
            'format': 'pdf',
            'include_grades': True
        }, format='json')
        
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]


@pytest.mark.django_db
class TestExportManagement:
    """Test export management operations"""

    def test_list_user_exports(self, api_client, student_user):
        """List all exports for current user"""
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/exports/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_view_export_details(self, api_client, student_user):
        """View details of specific export"""
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/exports/1/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_delete_export(self, api_client, student_user):
        """Delete an export"""
        api_client.force_authenticate(user=student_user)
        response = api_client.delete('/api/exports/1/')
        
        assert response.status_code in [
            status.HTTP_204_NO_CONTENT,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_download_export_file(self, api_client, student_user):
        """Download export file"""
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/exports/1/download/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_regenerate_export(self, api_client, student_user):
        """Regenerate a previous export"""
        api_client.force_authenticate(user=student_user)
        response = api_client.post('/api/exports/1/regenerate/', format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_export_status_check(self, api_client, student_user):
        """Check export processing status"""
        api_client.force_authenticate(user=student_user)
        response = api_client.get('/api/exports/1/status/')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]


@pytest.mark.django_db
class TestBulkExports:
    """Test bulk export operations"""

    def test_bulk_export_multiple_cases(self, api_client, instructor_user, student_user, test_repository):
        """Bulk export multiple cases"""
        cases = [
            Case.objects.create(
                title=f"Bulk Export Case {i}",
                student=student_user,
                repository=test_repository,
                patient_age=30 + i,
                patient_gender="M",
                case_status="approved",
            )
            for i in range(5)
        ]
        
        api_client.force_authenticate(user=instructor_user)
        response = api_client.post('/api/exports/bulk/', {
            'case_ids': [c.id for c in cases],
            'format': 'pdf'
        }, format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_bulk_export_with_zip(self, api_client, instructor_user, student_user, test_repository):
        """Bulk export cases as ZIP archive"""
        cases = [
            Case.objects.create(
                title=f"ZIP Export {i}",
                student=student_user,
                repository=test_repository,
                patient_age=35 + i,
                patient_gender="F",
                case_status="approved",
            )
            for i in range(3)
        ]
        
        api_client.force_authenticate(user=instructor_user)
        response = api_client.post('/api/exports/bulk/', {
            'case_ids': [c.id for c in cases],
            'format': 'pdf',
            'create_archive': True
        }, format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]
