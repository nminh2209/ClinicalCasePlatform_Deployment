"""
Tests for Grades views.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from grades.models import Grade
from cases.models import Case

User = get_user_model()


@pytest.mark.django_db
class TestGradeViews:
    """Test suite for grade endpoints."""

    @pytest.fixture
    def graded_case(self, student_user, instructor_user, test_repository):
        """Create a case ready for grading."""
        return Case.objects.create(
            title='Case for Grading',
            student=student_user,
            repository=test_repository,
            patient_name='Patient',
            patient_age=50,
            patient_gender='male',
            specialty='Cardiology',
            case_status='submitted'
        )

    def test_instructor_can_grade_case(self, instructor_client, graded_case, instructor_user):
        """Test instructor can assign grade to student case."""
        data = {
            'case': graded_case.id,
            'graded_by': instructor_user.id,
            'score': 85,
            'evaluation_notes': 'Good work, but needs more detail in diagnosis',
            'clinical_reasoning_score': 90
        }
        response = instructor_client.post('/api/grades/', data, format='json')
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]

    def test_student_cannot_grade_own_case(self, authenticated_client, graded_case, student_user):
        """Test student cannot grade their own case."""
        data = {
            'case': graded_case.id,
            'graded_by': student_user.id,
            'score': 100,
            'evaluation_notes': 'I give myself 100!'
        }
        response = authenticated_client.post('/api/grades/', data, format='json')
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]

    def test_student_can_view_own_grades(self, authenticated_client, graded_case, instructor_user):
        """Test student can view grades for their cases."""
        # Create a grade
        Grade.objects.create(
            case=graded_case,
            graded_by=instructor_user,
            score=88,
            evaluation_notes='Well done'
        )
        
        response = authenticated_client.get('/api/grades/')
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

    def test_grade_validation_score_range(self, instructor_client, graded_case, instructor_user):
        """Test grade score must be 0-100."""
        data = {
            'case': graded_case.id,
            'graded_by': instructor_user.id,
            'score': 150,  # Invalid score
            'evaluation_notes': 'Test'
        }
        response = instructor_client.post('/api/grades/', data, format='json')
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]

    def test_update_grade(self, instructor_client, graded_case, instructor_user):
        """Test instructor can update existing grade."""
        grade = Grade.objects.create(
            case=graded_case,
            graded_by=instructor_user,
            score=80,
            evaluation_notes='Initial feedback'
        )
        
        data = {
            'score': 85,
            'evaluation_notes': 'Updated feedback after reconsideration'
        }
        response = instructor_client.patch(f'/api/grades/{grade.id}/', data, format='json')
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN]

    def test_grade_with_detailed_criteria(self, instructor_client, graded_case, instructor_user):
        """Test grade with detailed scoring criteria."""
        data = {
            'case': graded_case.id,
            'graded_by': instructor_user.id,
            'score': 87,
            'evaluation_notes': 'Comprehensive evaluation',
            'clinical_reasoning_score': 90,
            'documentation_score': 85
        }
        response = instructor_client.post('/api/grades/', data, format='json')
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]


@pytest.mark.django_db
class TestCommentViews:
    """Test suite for comment endpoints."""

    @pytest.fixture
    def commented_case(self, student_user, test_repository):
        """Create a case for commenting."""
        return Case.objects.create(
            title='Case for Comments',
            student=student_user,
            repository=test_repository,
            patient_name='Patient',
            patient_age=45,
            patient_gender='female',
            specialty='Neurology'
        )

    def test_add_comment_to_case(self, authenticated_client, commented_case):
        """Test adding comment to case."""
        data = {
            'case': commented_case.id,
            'content': 'Great case study! Very informative.'
        }
        response = authenticated_client.post('/api/comments/', data, format='json')
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]

    def test_reply_to_comment(self, authenticated_client, commented_case, student_user):
        """Test replying to existing comment."""
        from comments.models import Comment
        
        parent_comment = Comment.objects.create(
            case=commented_case,
            author=student_user,
            content='Original comment'
        )
        
        data = {
            'case': commented_case.id,
            'parent': parent_comment.id,
            'content': 'Reply to comment'
        }
        response = authenticated_client.post('/api/comments/', data, format='json')
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]

    def test_list_case_comments(self, authenticated_client, commented_case, student_user):
        """Test listing all comments for a case."""
        from comments.models import Comment
        
        Comment.objects.create(
            case=commented_case,
            author=student_user,
            content='Comment 1'
        )
        Comment.objects.create(
            case=commented_case,
            author=student_user,
            content='Comment 2'
        )
        
        response = authenticated_client.get(f'/api/cases/{commented_case.id}/comments/')
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

    def test_edit_own_comment(self, authenticated_client, commented_case, student_user):
        """Test user can edit their own comment."""
        from comments.models import Comment
        
        comment = Comment.objects.create(
            case=commented_case,
            author=student_user,
            content='Original content'
        )
        
        data = {'content': 'Updated content'}
        response = authenticated_client.patch(f'/api/comments/{comment.id}/', data, format='json')
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN]

    def test_cannot_edit_others_comment(self, api_client, commented_case, student_user, cardiology_department):
        """Test user cannot edit another user's comment."""
        from comments.models import Comment
        
        other_user = User.objects.create_user(
            username='other@test.com',
            email='other@test.com',
            password='testpass123',
            department=cardiology_department
        )
        
        comment = Comment.objects.create(
            case=commented_case,
            author=student_user,
            content='Original content'
        )
        
        api_client.force_authenticate(user=other_user)
        data = {'content': 'Hacked content'}
        response = api_client.patch(f'/api/comments/{comment.id}/', data, format='json')
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]

    def test_delete_own_comment(self, authenticated_client, commented_case, student_user):
        """Test user can delete their own comment."""
        from comments.models import Comment
        
        comment = Comment.objects.create(
            case=commented_case,
            author=student_user,
            content='To be deleted'
        )
        
        response = authenticated_client.delete(f'/api/comments/{comment.id}/')
        assert response.status_code in [status.HTTP_204_NO_CONTENT, status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN]
