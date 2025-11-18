"""
Script to create test accounts for all user roles
Run this from the backend directory with: python create_test_users.py
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinical_case_platform.settings')
django.setup()

from accounts.models import User

def create_test_accounts():
    """Create test accounts for student, instructor, and admin roles"""
    
    test_users = [
        {
            'email': 'student@test.com',
            'username': 'student1',
            'password': 'testpass123',
            'first_name': 'John',
            'last_name': 'Student',
            'role': 'student',
            'student_id': 'S2024001'
        },
        {
            'email': 'instructor@test.com',
            'username': 'instructor1',
            'password': 'testpass123',
            'first_name': 'Jane',
            'last_name': 'Instructor',
            'role': 'instructor',
            'employee_id': 'E2024001',
            'specialization': 'Cardiology'
        },
        {
            'email': 'admin@test.com',
            'username': 'admin1',
            'password': 'testpass123',
            'first_name': 'Admin',
            'last_name': 'User',
            'role': 'admin',
            'employee_id': 'A2024001'
        }
    ]
    
    print("Creating test accounts...\n")
    
    for user_data in test_users:
        email = user_data['email']
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            print(f"⚠️  User {email} already exists, skipping...")
            continue
        
        # Create user
        try:
            user = User.objects.create_user(
                email=user_data['email'],
                username=user_data['username'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                role=user_data['role']
            )
            
            # Set additional fields
            if 'student_id' in user_data:
                user.student_id = user_data['student_id']
            if 'employee_id' in user_data:
                user.employee_id = user_data['employee_id']
            if 'specialization' in user_data:
                user.specialization = user_data['specialization']
            
            user.save()
            
            print(f"✅ Created {user_data['role'].upper()} account:")
            print(f"   Email: {email}")
            print(f"   Password: {user_data['password']}")
            print(f"   Role: {user_data['role']}\n")
            
        except Exception as e:
            print(f"❌ Error creating user {email}: {str(e)}\n")
    
    print("=" * 60)
    print("Test accounts summary:")
    print("=" * 60)
    print("STUDENT    → student@test.com / testpass123")
    print("INSTRUCTOR → instructor@test.com / testpass123")
    print("ADMIN      → admin@test.com / testpass123")
    print("=" * 60)
    print("\n✨ You can now test role-based login at http://localhost:5173/login")

if __name__ == '__main__':
    create_test_accounts()