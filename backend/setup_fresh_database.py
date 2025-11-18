#!/usr/bin/env python
"""
Fresh Database Setup Script
============================

This script sets up a completely fresh database by:
1. Dropping all tables
2. Running all migrations properly
3. Creating initial data

Use this when setting up the project on a new machine or fixing migration issues.

USAGE:
------
python setup_fresh_database.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clinical_case_platform.settings")
django.setup()

from django.core.management import call_command
from django.db import connection


def drop_all_tables():
    """Drop all tables in the database."""
    print("🗑️  Dropping all tables...")
    with connection.cursor() as cursor:
        # Get all table names
        cursor.execute("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public'
        """)
        tables = cursor.fetchall()
        
        if tables:
            # Drop all tables
            cursor.execute("DROP SCHEMA public CASCADE;")
            cursor.execute("CREATE SCHEMA public;")
            cursor.execute("GRANT ALL ON SCHEMA public TO postgres;")
            cursor.execute("GRANT ALL ON SCHEMA public TO public;")
            print(f"   ✅ Dropped {len(tables)} tables")
        else:
            print("   ℹ️  No tables to drop")


def run_migrations():
    """Run all migrations from scratch."""
    print("\n📋 Running migrations...")
    call_command("migrate", verbosity=2)
    print("   ✅ All migrations applied")


def create_superuser():
    """Create initial superuser."""
    from accounts.models import User
    from cases.medical_models import Department
    
    print("\n👤 Creating superuser...")
    
    # Create a default department first
    dept, _ = Department.objects.get_or_create(
        code="ADMIN",
        defaults={
            "name": "Administration",
            "vietnamese_name": "Quản Trị",
            "description": "Khoa Quản Trị",
            "department_type": "administrative",
        }
    )
    
    if not User.objects.filter(email="admin@test.com").exists():
        User.objects.create_superuser(
            email="admin@test.com",
            username="admin",
            password="minh1234minh",
            first_name="Admin",
            last_name="User",
            department=dept,
        )
        print("   ✅ Superuser created (admin@test.com / minh1234minh)")
    else:
        print("   ℹ️  Superuser already exists")


def main():
    """Main setup function."""
    print("=" * 60)
    print("🚀 FRESH DATABASE SETUP")
    print("=" * 60)
    
    response = input("\n⚠️  This will DELETE ALL DATA in the database. Continue? (yes/no): ")
    if response.lower() != "yes":
        print("❌ Aborted")
        sys.exit(0)
    
    try:
        # Step 1: Drop all tables
        drop_all_tables()
        
        # Step 2: Run migrations
        run_migrations()
        
        # Step 3: Create superuser
        create_superuser()
        
        print("\n" + "=" * 60)
        print("✅ DATABASE SETUP COMPLETE!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Run: python populate_test_data.py")
        print("2. Start server: python manage.py runserver")
        print("\nLogin with: admin@test.com / minh1234minh")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
