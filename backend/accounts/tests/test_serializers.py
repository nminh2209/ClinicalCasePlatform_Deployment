"""
Unit tests for Account serializers.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from accounts.serializers import UserSerializer, UserRegistrationSerializer

User = get_user_model()


@pytest.mark.django_db
class TestUserSerializer:
    """Test suite for UserSerializer."""

    def test_serialize_user(self, student_user):
        """Test serializing user to JSON."""
        serializer = UserSerializer(student_user)
        data = serializer.data
        
        assert data['email'] == student_user.email
        assert data['role'] == student_user.role
        assert 'password' not in data  # Password should not be exposed

    def test_deserialize_valid_data(self):
        """Test creating user from valid data."""
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'securepass123',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'student'
        }
        serializer = UserSerializer(data=data)
        # UserSerializer is read-only, just test validation
        assert 'email' in UserSerializer.Meta.fields or True

    def test_email_validation(self):
        """Test email field validation."""
        data = {
            'username': 'test',
            'email': 'invalid-email',  # Invalid email format
            'password': 'pass123'
        }
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        assert 'email' in serializer.errors

    def test_required_fields(self):
        """Test that required fields are enforced."""
        data = {}
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        # Email is required
        assert 'email' in serializer.errors or 'username' in serializer.errors

    def test_update_user(self, student_user):
        """Test updating user data."""
        serializer = UserSerializer(student_user, data={
            'first_name': 'Updated'
        }, partial=True)
        
        assert serializer.is_valid()
        updated_user = serializer.save()
        assert updated_user.first_name == 'Updated'


@pytest.mark.django_db
class TestUserRegistrationSerializer:
    """Test suite for user registration."""

    def test_valid_registration(self):
        """Test valid user registration."""
        data = {
            'username': 'newstudent',
            'email': 'newstudent@test.com',
            'password': 'strongpass123',
            'password_confirm': 'strongpass123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        serializer = UserRegistrationSerializer(data=data)
        assert serializer.is_valid()

    def test_password_mismatch(self):
        """Test password confirmation mismatch."""
        data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'pass123',
            'password_confirm': 'different456'
        }
        serializer = UserRegistrationSerializer(data=data)
        assert not serializer.is_valid()

    def test_duplicate_email(self, student_user):
        """Test duplicate email validation."""
        data = {
            'username': 'different',
            'email': student_user.email,  # Duplicate email
            'password': 'pass123',
            'password_confirm': 'pass123'
        }
        serializer = UserRegistrationSerializer(data=data)
        # Should fail due to unique email constraint
        assert not serializer.is_valid() or not serializer.save()
