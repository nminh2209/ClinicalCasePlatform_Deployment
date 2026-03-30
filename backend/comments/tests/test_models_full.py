"""
Unit tests for Comment model
"""

import pytest
from django.contrib.auth import get_user_model
from comments.models import Comment
from cases.models import Case

User = get_user_model()


@pytest.mark.django_db
class TestCommentModel:
    """Test Comment model functionality"""

    def test_create_comment(self, student_user, instructor_user, test_repository):
        """Test creating a comment"""
        case = Case.objects.create(
            title="Commented Case",
            student=student_user,
            repository=test_repository,
            patient_age=38,
            patient_gender="M",
        )

        comment = Comment.objects.create(
            case=case,
            author=instructor_user,
            content="Trình bày ca bệnh rất tốt, cần bổ sung thêm các xét nghiệm chẩn đoán.",
        )

        assert comment.case == case
        assert comment.author == instructor_user
        assert "Trình bày ca bệnh rất tốt" in comment.content

    def test_nested_comments(self, student_user, instructor_user, test_repository):
        """Test creating nested replies"""
        case = Case.objects.create(
            title="Discussion Case",
            student=student_user,
            repository=test_repository,
            patient_age=42,
            patient_gender="F",
        )

        # Parent comment
        parent_comment = Comment.objects.create(
            case=case,
            author=instructor_user,
            content="Chẩn đoán ban đầu của bạn thế nào?",
        )

        # Reply comment
        reply = Comment.objects.create(
            case=case,
            author=student_user,
            content="Em nghĩ đây là trường hợp nhồi máu cơ tim cấp.",
            parent=parent_comment,
        )

        assert reply.parent == parent_comment
        assert reply.author == student_user

    def test_comment_reactions(self, student_user, instructor_user, test_repository):
        """Test comment reactions"""
        case = Case.objects.create(
            title="Reaction Test",
            student=student_user,
            repository=test_repository,
            patient_age=30,
            patient_gender="M",
        )

        comment = Comment.objects.create(
            case=case,
            author=instructor_user,
            content="Phân tích rất hay!",
        )

        reaction = Comment.objects.create(
            case=case,
            author=student_user,
            content="👍",
            parent=comment,
            is_reaction=True,
            reaction_type="like",
        )

        assert reaction.is_reaction is True
        assert reaction.reaction_type == "like"
        assert reaction.parent == comment

    def test_multiple_comments_on_case(
        self, student_user, instructor_user, test_repository
    ):
        """Test multiple comments on same case"""
        case = Case.objects.create(
            title="Multi Comment Case",
            student=student_user,
            repository=test_repository,
            patient_age=55,
            patient_gender="M",
        )

        comment1 = Comment.objects.create(
            case=case,
            author=instructor_user,
            content="Nhận xét lần 1: Tiền sử bệnh đầy đủ",
        )

        comment2 = Comment.objects.create(
            case=case,
            author=instructor_user,
            content="Nhận xét lần 2: Cần bổ sung khám lâm sàng",
        )

        case_comments = Comment.objects.filter(case=case, is_reaction=False)
        assert case_comments.count() == 2
        assert comment1 in case_comments
        assert comment2 in case_comments
