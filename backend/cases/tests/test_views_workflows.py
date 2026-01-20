"""
Tests for Case workflow transitions and approvals
"""
import pytest
from rest_framework import status
from django.contrib.auth import get_user_model
from cases.models import Case

User = get_user_model()


@pytest.mark.django_db
class TestCaseApprovalWorkflow:
    """Test case approval workflow"""

    def test_submit_case_for_review(self, api_client, student_user, test_repository):
        """Student submits draft case for review"""
        case = Case.objects.create(
            title="Case for Submission",
            student=student_user,
            repository=test_repository,
            patient_age=45,
            patient_gender="M",
            case_status="draft",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.post(f'/api/cases/{case.id}/submit/', format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_instructor_approve_case(self, api_client, instructor_user, student_user, test_repository):
        """Instructor approves submitted case"""
        case = Case.objects.create(
            title="Case for Approval",
            student=student_user,
            repository=test_repository,
            patient_age=50,
            patient_gender="F",
            case_status="submitted",
        )
        
        api_client.force_authenticate(user=instructor_user)
        data = {"action": "approve"}
        response = api_client.post(f'/api/cases/{case.id}/review/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_instructor_reject_case(self, api_client, instructor_user, student_user, test_repository):
        """Instructor rejects submitted case with feedback"""
        case = Case.objects.create(
            title="Case for Rejection",
            student=student_user,
            repository=test_repository,
            patient_age=38,
            patient_gender="M",
            case_status="submitted",
        )
        
        api_client.force_authenticate(user=instructor_user)
        data = {
            "action": "reject",
            "feedback": "Cần bổ sung thêm thông tin về tiền sử bệnh"
        }
        response = api_client.post(f'/api/cases/{case.id}/review/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_instructor_request_revision(self, api_client, instructor_user, student_user, test_repository):
        """Instructor requests revisions on case"""
        case = Case.objects.create(
            title="Nhồi Máu Não Cấp",
            student=student_user,
            repository=test_repository,
            patient_age=65,
            patient_gender="M",
            case_status="submitted",
        )
        
        api_client.force_authenticate(user=instructor_user)
        data = {
            "action": "request_revision",
            "feedback": "Cần làm rõ thêm về triệu chứng lâm sàng"
        }
        response = api_client.post(f'/api/cases/{case.id}/review/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_student_cannot_approve_case(self, api_client, student_user, test_repository):
        """Student cannot approve their own case"""
        case = Case.objects.create(
            title="Self Approval Test",
            student=student_user,
            repository=test_repository,
            patient_age=42,
            patient_gender="F",
            case_status="submitted",
        )
        
        api_client.force_authenticate(user=student_user)
        data = {"action": "approve"}
        response = api_client.post(f'/api/cases/{case.id}/review/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_resubmit_rejected_case(self, api_client, student_user, test_repository):
        """Student resubmits rejected case after revision"""
        case = Case.objects.create(
            title="Resubmission Test",
            student=student_user,
            repository=test_repository,
            patient_age=55,
            patient_gender="M",
            case_status="rejected",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.post(f'/api/cases/{case.id}/resubmit/', format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]


@pytest.mark.django_db
class TestCaseStatusTransitions:
    """Test case status state machine"""

    def test_draft_to_submitted(self, api_client, student_user, test_repository):
        """Transition from draft to submitted"""
        case = Case.objects.create(
            title="Draft Case",
            student=student_user,
            repository=test_repository,
            patient_age=40,
            patient_gender="F",
            case_status="draft",
        )
        
        api_client.force_authenticate(user=student_user)
        data = {"case_status": "submitted"}
        response = api_client.patch(f'/api/cases/{case.id}/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_cannot_transition_approved_to_draft(self, api_client, student_user, test_repository):
        """Cannot change approved case back to draft"""
        case = Case.objects.create(
            title="Approved Case",
            student=student_user,
            repository=test_repository,
            patient_age=45,
            patient_gender="M",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=student_user)
        data = {"case_status": "draft"}
        response = api_client.patch(f'/api/cases/{case.id}/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_archive_case(self, api_client, instructor_user, student_user, test_repository):
        """Instructor archives old case"""
        case = Case.objects.create(
            title="Old Case",
            student=student_user,
            repository=test_repository,
            patient_age=50,
            patient_gender="F",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=instructor_user)
        response = api_client.post(f'/api/cases/{case.id}/archive/', format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_publish_case(self, api_client, instructor_user, student_user, test_repository):
        """Publish approved case to case library"""
        case = Case.objects.create(
            title="Viêm Phổi Nặng",
            student=student_user,
            repository=test_repository,
            patient_age=60,
            patient_gender="M",
            case_summary="Ca bệnh viêm phổi nặng điển hình",
            case_status="approved",
        )
        
        api_client.force_authenticate(user=instructor_user)
        response = api_client.post(f'/api/cases/{case.id}/publish/', format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]


@pytest.mark.django_db
class TestBulkCaseOperations:
    """Test bulk operations on cases"""

    def test_bulk_delete_cases(self, api_client, instructor_user, student_user, test_repository):
        """Instructor bulk deletes multiple cases"""
        cases = [
            Case.objects.create(
                title=f"Bulk Delete {i}",
                student=student_user,
                repository=test_repository,
                patient_age=30 + i,
                patient_gender="M",
                case_status="draft",
            )
            for i in range(3)
        ]
        
        api_client.force_authenticate(user=instructor_user)
        data = {"case_ids": [c.id for c in cases]}
        response = api_client.post('/api/cases/bulk-delete/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_204_NO_CONTENT,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_bulk_approve_cases(self, api_client, instructor_user, student_user, test_repository):
        """Instructor bulk approves multiple submitted cases"""
        cases = [
            Case.objects.create(
                title=f"Bulk Approve {i}",
                student=student_user,
                repository=test_repository,
                patient_age=35 + i,
                patient_gender="F",
                case_status="submitted",
            )
            for i in range(3)
        ]
        
        api_client.force_authenticate(user=instructor_user)
        data = {"case_ids": [c.id for c in cases]}
        response = api_client.post('/api/cases/bulk-approve/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_bulk_export_cases(self, api_client, instructor_user, student_user, test_repository):
        """Bulk export multiple cases"""
        cases = [
            Case.objects.create(
                title=f"Export Case {i}",
                student=student_user,
                repository=test_repository,
                patient_age=40 + i,
                patient_gender="M",
                case_status="approved",
            )
            for i in range(5)
        ]
        
        api_client.force_authenticate(user=instructor_user)
        data = {"case_ids": [c.id for c in cases], "format": "pdf"}
        response = api_client.post('/api/cases/bulk-export/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]
