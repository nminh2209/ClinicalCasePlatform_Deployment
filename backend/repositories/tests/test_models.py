"""
Unit tests for repository models
"""

import pytest
from django.contrib.auth import get_user_model
from repositories.models import Repository
from cases.medical_models import Department

User = get_user_model()


@pytest.fixture
def instructor_user(db):
    """Create instructor user"""
    return User.objects.create_user(
        username="pham.thi.hoa",
        email="pham.thi.hoa@test.com",
        password="test123",
        role="instructor",
        first_name="Hoa",
        last_name="Phạm Thị",
        specialization="Hô Hấp",
        employee_id="GV004",
    )


@pytest.fixture
def department(db):
    """Create test department"""
    return Department.objects.create(
        name="Respiratory Medicine",
        vietnamese_name="Khoa Hô Hấp",
        code="HH",
        description="Khoa chuyên về các bệnh lý hô hấp",
        department_type="clinical",
    )


@pytest.mark.django_db
def test_repository_creation(instructor_user, department):
    """Test creating a repository"""
    repo = Repository.objects.create(
        name="Cardiology Cases",
        vietnamese_name="Kho Bệnh Án Tim Mạch",
        description="Kho lưu trữ các ca bệnh tim mạch cho sinh viên và giảng viên",
        owner=instructor_user,
        department=department,
    )
    assert repo.name == "Cardiology Cases"
    assert repo.vietnamese_name == "Kho Bệnh Án Tim Mạch"
    assert repo.owner == instructor_user
    assert repo.department == department


@pytest.mark.django_db
def test_repository_access_levels(instructor_user):
    """Test different access levels"""
    public_repo = Repository.objects.create(
        name="Public Medical Cases",
        vietnamese_name="Kho Bệnh Án Công Khai",
        description="Các ca bệnh điển hình cho tất cả sinh viên",
        owner=instructor_user,
        access_level="public",
        is_public=True,
    )
    private_repo = Repository.objects.create(
        name="Private Research Cases",
        vietnamese_name="Kho Bệnh Án Nghiên Cứu Riêng",
        description="Các ca bệnh nghiên cứu nội bộ",
        owner=instructor_user,
        access_level="private",
        is_public=False,
    )
    assert public_repo.access_level == "public"
    assert public_repo.is_public is True
    assert private_repo.access_level == "private"
    assert private_repo.is_public is False


@pytest.mark.django_db
def test_repository_department_access(instructor_user, department):
    """Test department-level access"""
    repo = Repository.objects.create(
        name="Department Repository",
        vietnamese_name="Kho khoa phòng",
        owner=instructor_user,
        department=department,
        access_level="department",
    )
    assert repo.access_level == "department"
    assert repo.department == department


@pytest.mark.django_db
def test_repository_string_representation(instructor_user):
    """Test repository string representation"""
    repo = Repository.objects.create(
        name="Test Repository",
        vietnamese_name="Kho kiểm tra",
        owner=instructor_user,
    )
    assert "Test Repository" in str(repo)
