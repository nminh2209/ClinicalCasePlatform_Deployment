"""
Unit tests for Case serializers
"""
import pytest
from django.contrib.auth import get_user_model
from cases.serializers import CaseListSerializer, CaseDetailSerializer, CaseCreateUpdateSerializer
from cases.models import Case

User = get_user_model()


@pytest.mark.django_db
class TestCaseListSerializer:
    """Test CaseListSerializer for list views"""

    def test_list_serializer_fields(self, student_user, test_repository):
        """Test list serializer includes required fields"""
        case = Case.objects.create(
            title="Nhồi Máu Cơ Tim Cấp",
            student=student_user,
            repository=test_repository,
            patient_age=55,
            patient_gender="M",
            case_status="approved",
        )
        
        serializer = CaseListSerializer(case)
        data = serializer.data
        
        assert "id" in data
        assert "title" in data
        assert data["title"] == "Nhồi Máu Cơ Tim Cấp"


@pytest.mark.django_db
class TestCaseDetailSerializer:
    """Test CaseDetailSerializer"""

    def test_detail_serializer(self, student_user, test_repository):
        """Test detail serializer with full case data"""
        case = Case.objects.create(
            title="Viêm Phổi Cộng Đồng",
            student=student_user,
            repository=test_repository,
            patient_age=42,
            patient_gender="F",
            case_summary="Bệnh nhân nữ 42 tuổi, sốt cao và ho",
            case_status="submitted",
        )
        
        serializer = CaseDetailSerializer(case)
        data = serializer.data
        
        assert data["title"] == "Viêm Phổi Cộng Đồng"
        assert data["patient_age"] == 42
        assert data["patient_gender"] == "F"
