"""
pytest configuration and fixtures for the entire backend test suite.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from unittest.mock import patch
from cases.medical_models import Department
from repositories.models import Repository

User = get_user_model()


@pytest.fixture(scope="session", autouse=True)
def mock_notifications():
    """Mock WebSocket notifications that require Redis"""
    with patch("notifications.signals.send_notification_to_user"):
        yield


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Setup test database with minimal data needed for all tests.
    """
    pass


@pytest.fixture
def api_client():
    """
    Provide a DRF API client for testing.
    """
    return APIClient()


@pytest.fixture
def admin_user(db):
    """
    Create an admin user for testing.
    """
    return User.objects.create_superuser(
        username='admin@test.com',
        email='admin@test.com',
        password='testpass123',
        first_name='Admin',
        last_name='User'
    )


@pytest.fixture
def instructor_user(db, cardiology_department):
    """
    Create an instructor user for testing.
    """
    return User.objects.create_user(
        username='tran.thi.bich',
        email='tran.thi.bich@test.com',
        password='testpass123',
        role='instructor',
        first_name='Bích',
        last_name='Trần Thị',
        specialization='Tim Mạch',
        employee_id='GV001',
        department=cardiology_department
    )


@pytest.fixture
def student_user(db, cardiology_department):
    """
    Create a student user for testing.
    """
    return User.objects.create_user(
        username='vo.thi.yen',
        email='vo.thi.yen@student.com',
        password='testpass123',
        role='student',
        first_name='Yến',
        last_name='Võ Thị',
        student_id='SV2024001',
        department=cardiology_department
    )


@pytest.fixture
def cardiology_department(db):
    """
    Create a Cardiology department for testing.
    """
    return Department.objects.get_or_create(
        code='TIM',
        defaults={
            'name': 'Cardiology',
            'vietnamese_name': 'Khoa Tim Mạch',
            'description': 'Khoa chuyên về các bệnh lý tim mạch',
            'department_type': 'clinical'
        }
    )[0]


@pytest.fixture
def test_repository(db, instructor_user, cardiology_department):
    """
    Create a test repository for testing.
    """
    return Repository.objects.create(
        name='Clinical Cases Repository',
        vietnamese_name='Kho Hồ Sơ Bệnh Án Lâm Sàng',
        description='Kho lưu trữ các ca bệnh lâm sàng cho sinh viên và giảng viên',
        owner=instructor_user,
        department=cardiology_department,
        access_level='department'
    )


@pytest.fixture
def authenticated_client(api_client, student_user):
    """
    Provide an authenticated API client.
    """
    api_client.force_authenticate(user=student_user)
    return api_client


@pytest.fixture
def instructor_client(api_client, instructor_user):
    """
    Provide an authenticated instructor API client.
    """
    api_client.force_authenticate(user=instructor_user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    """
    Provide an authenticated admin API client.
    """
    api_client.force_authenticate(user=admin_user)
    return api_client
