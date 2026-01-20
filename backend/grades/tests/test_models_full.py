"""
Unit tests for Grade model
"""
import pytest
from django.contrib.auth import get_user_model
from grades.models import Grade
from cases.models import Case

User = get_user_model()


@pytest.mark.django_db
class TestGradeModel:
    """Test Grade model functionality"""

    def test_create_grade(self, student_user, instructor_user, test_repository):
        """Test creating a grade"""
        case = Case.objects.create(
            title="Graded Case",
            student=student_user,
            repository=test_repository,
            patient_age=40,
            patient_gender="M",
        )
        
        grade = Grade.objects.create(
            case=case,
            graded_by=instructor_user,
            score=85.5,
            letter_grade="B",
            evaluation_notes="Trình bày tốt, cần cải thiện chẩn đoán phân biệt",
        )
        
        assert grade.score == 85.5
        assert grade.letter_grade == "B"
        assert grade.graded_by == instructor_user
        assert "Trình bày tốt" in grade.evaluation_notes

    def test_grade_score_range(self, student_user, instructor_user, test_repository):
        """Test different grade scores"""
        case = Case.objects.create(
            title="Score Test",
            student=student_user,
            repository=test_repository,
            patient_age=35,
            patient_gender="F",
        )
        
        # Test excellent score
        grade_a = Grade.objects.create(
            case=case,
            graded_by=instructor_user,
            score=95.0,
            letter_grade="A",
            evaluation_notes="Xuất sắc",
        )
        assert grade_a.score == 95.0
        assert grade_a.letter_grade == "A"

    def test_grade_with_detailed_notes(self, student_user, instructor_user, test_repository):
        """Test grade with comprehensive evaluation notes"""
        case = Case.objects.create(
            title="Detailed Evaluation",
            student=student_user,
            repository=test_repository,
            patient_age=50,
            patient_gender="M",
        )
        
        detailed_notes = """
        Điểm mạnh:
        - Thu thập tiền sử bệnh rất chi tiết
        - Khám lâm sàng có hệ thống
        
        Cần cải thiện:
        - Chẩn đoán phân biệt chưa đầy đủ
        - Kế hoạch điều trị cần cụ thể hơn
        """
        
        grade = Grade.objects.create(
            case=case,
            graded_by=instructor_user,
            score=78.0,
            letter_grade="C",
            evaluation_notes=detailed_notes,
        )
        
        assert "Điểm mạnh" in grade.evaluation_notes
        assert "Cần cải thiện" in grade.evaluation_notes
        assert grade.score == 78.0

    def test_grade_string_representation(self, student_user, instructor_user, test_repository):
        """Test grade string representation"""
        case = Case.objects.create(
            title="String Test",
            student=student_user,
            repository=test_repository,
            patient_age=45,
            patient_gender="F",
        )
        
        grade = Grade.objects.create(
            case=case,
            graded_by=instructor_user,
            score=88.0,
            letter_grade="B",
        )
        
        grade_str = str(grade)
        assert case.title in grade_str or str(grade.score) in grade_str
