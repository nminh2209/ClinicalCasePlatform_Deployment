"""
Unit tests for User model in accounts app.
"""
import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from cases.medical_models import Department

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Test suite for the User model."""

    def test_create_user(self):
        """Test creating a regular user."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        assert user.email == 'test@example.com'
        assert user.username == 'testuser'
        assert user.check_password('testpass123')
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser

    def test_create_superuser(self):
        """Test creating a superuser."""
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        assert admin.is_staff
        assert admin.is_superuser
        assert admin.is_active

    def test_user_email_unique(self):
        """Test that email must be unique."""
        User.objects.create_user(
            username='user1',
            email='duplicate@example.com',
            password='pass123'
        )
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                username='user2',
                email='duplicate@example.com',
                password='pass456'
            )

    def test_user_str_representation(self):
        """Test the string representation of user."""
        user = User.objects.create_user(
            username='john',
            email='john@example.com',
            password='pass123',
            first_name='John',
            last_name='Doe',
            role=User.RoleChoices.STUDENT
        )
        assert str(user) == 'John Doe (Sinh viên)'

    def test_user_role_default(self):
        """Test that default role is STUDENT."""
        user = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='pass123'
        )
        assert user.role == User.RoleChoices.STUDENT

    def test_user_role_choices(self):
        """Test different user roles."""
        student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='pass123',
            role=User.RoleChoices.STUDENT
        )
        instructor = User.objects.create_user(
            username='instructor',
            email='instructor@example.com',
            password='pass123',
            role=User.RoleChoices.INSTRUCTOR
        )
        admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='pass123',
            role=User.RoleChoices.ADMIN
        )
        
        assert student.is_student
        assert not student.is_instructor
        assert not student.is_admin_user
        
        assert not instructor.is_student
        assert instructor.is_instructor
        assert not instructor.is_admin_user
        
        assert not admin.is_student
        assert not admin.is_instructor
        assert admin.is_admin_user

    def test_user_with_department(self):
        """Test user with department assignment."""
        dept = Department.objects.create(
            name='Cardiology',
            code='CARD',
            vietnamese_name='Khoa Tim mạch'
        )
        user = User.objects.create_user(
            username='doctor',
            email='doctor@example.com',
            password='pass123',
            department=dept
        )
        assert user.department == dept
        assert user.get_department_name() == 'Cardiology'

    def test_user_without_department(self):
        """Test user without department."""
        user = User.objects.create_user(
            username='nodept',
            email='nodept@example.com',
            password='pass123'
        )
        assert user.department is None
        assert user.get_department_name() == 'Chưa phân khoa'

    def test_user_optional_fields(self):
        """Test user with optional fields."""
        user = User.objects.create_user(
            username='complete',
            email='complete@example.com',
            password='pass123',
            student_id='SV001',
            academic_year='2024-2025',
            phone_number='+84123456789',
            bio='Test bio',
            language_preference='en'
        )
        assert user.student_id == 'SV001'
        assert user.academic_year == '2024-2025'
        assert user.phone_number == '+84123456789'
        assert user.bio == 'Test bio'
        assert user.language_preference == 'en'

    def test_user_notification_settings_default(self):
        """Test that notification_settings defaults to empty dict."""
        user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='pass123'
        )
        assert user.notification_settings == {}
        assert isinstance(user.notification_settings, dict)

    def test_user_email_verified_default(self):
        """Test that email_verified defaults to False."""
        user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='pass123'
        )
        assert user.email_verified is False

    def test_user_timestamps(self):
        """Test that created_at and updated_at are set automatically."""
        user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='pass123'
        )
        assert user.created_at is not None
        assert user.updated_at is not None
        assert user.created_at <= user.updated_at

    def test_instructor_with_specialization(self):
        """Test instructor with specialization."""
        instructor = User.objects.create_user(
            username='instructor',
            email='instructor@example.com',
            password='pass123',
            role=User.RoleChoices.INSTRUCTOR,
            specialization='Cardiology',
            employee_id='EMP001'
        )
        assert instructor.is_instructor
        assert instructor.specialization == 'Cardiology'
        assert instructor.employee_id == 'EMP001'
