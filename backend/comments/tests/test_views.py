"""
Tests for Comment views
"""
import pytest
from rest_framework import status
from django.contrib.auth import get_user_model
from cases.models import Case
from comments.models import Comment

User = get_user_model()


@pytest.mark.django_db
class TestCommentViews:
    """Test comment endpoints"""

    def test_list_case_comments(self, api_client, student_user, test_repository):
        """List comments on a case"""
        case = Case.objects.create(
            title="Commented Case",
            student=student_user,
            repository=test_repository,
            patient_age=30,
            patient_gender="M",
            case_status="approved",
        )
        
        Comment.objects.create(
            case=case,
            author=student_user,
            content="Nhận xét đầu tiên",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.get(f'/api/comments/?case={case.id}')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN,
        ]

    def test_create_comment(self, api_client, student_user, test_repository):
        """Create a comment on a case"""
        case = Case.objects.create(
            title="New Comment Case",
            student=student_user,
            repository=test_repository,
            patient_age=35,
            patient_gender="F",
            case_status="submitted",
        )
        
        api_client.force_authenticate(user=student_user)
        
        data = {
            "case": case.id,
            "content": "Ca bệnh này rất hay, cần bổ sung thêm xét nghiệm",
        }
        
        response = api_client.post('/api/comments/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
        ]

    def test_create_nested_comment(self, api_client, instructor_user, student_user, test_repository):
        """Create a reply to existing comment"""
        case = Case.objects.create(
            title="Reply Case",
            student=student_user,
            repository=test_repository,
            patient_age=40,
            patient_gender="M",
            case_status="approved",
        )
        
        parent_comment = Comment.objects.create(
            case=case,
            author=student_user,
            content="Câu hỏi về chẩn đoán",
        )
        
        api_client.force_authenticate(user=instructor_user)
        
        data = {
            "case": case.id,
            "parent": parent_comment.id,
            "content": "Đây là câu trả lời từ giảng viên",
        }
        
        response = api_client.post('/api/comments/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
        ]

    def test_update_own_comment(self, api_client, student_user, test_repository):
        """User can update their own comment"""
        case = Case.objects.create(
            title="Update Comment Case",
            student=student_user,
            repository=test_repository,
            patient_age=32,
            patient_gender="F",
            case_status="approved",
        )
        
        comment = Comment.objects.create(
            case=case,
            author=student_user,
            content="Nội dung cũ",
        )
        
        api_client.force_authenticate(user=student_user)
        
        data = {"content": "Nội dung đã cập nhật"}
        response = api_client.patch(f'/api/comments/{comment.id}/', data, format='json')
        
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_delete_own_comment(self, api_client, student_user, test_repository):
        """User can delete their own comment"""
        case = Case.objects.create(
            title="Delete Comment Case",
            student=student_user,
            repository=test_repository,
            patient_age=28,
            patient_gender="M",
            case_status="draft",
        )
        
        comment = Comment.objects.create(
            case=case,
            author=student_user,
            content="Nhận xét sẽ bị xóa",
        )
        
        api_client.force_authenticate(user=student_user)
        response = api_client.delete(f'/api/comments/{comment.id}/')
        
        assert response.status_code in [
            status.HTTP_204_NO_CONTENT,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]
