#!/usr/bin/env python
"""
Database Reset Script for Clinical Case Platform
=================================================

This script safely clears all data from the database and optionally
repopulates it with fresh test data.

USAGE:
------
1. Activate virtual environment:
   source venv/bin/activate  # Linux/Mac
   venv\\Scripts\\activate     # Windows

2. Run the script:
   python reset_database.py

3. Or use Django shell:
   python manage.py shell < reset_database.py

WARNING: This will DELETE ALL DATA in the database!

OPTIONS:
--------
Set REPOPULATE = True to automatically run populate_test_data after reset
Set REPOPULATE = False to just clear the database
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clinical_case_platform.settings")
django.setup()

from django.core.management import call_command
from accounts.models import User
from cases.models import Case, CasePermission
from cases.medical_models import (
    Department,
    ClinicalHistory,
    PhysicalExamination,
    Investigations,
    DiagnosisManagement,
    LearningOutcomes,
    MedicalAttachment,
    StudentNotes,
)
from repositories.models import Repository
from comments.models import Comment
from grades.models import Grade
from feedback.models import Feedback

# Configuration
REPOPULATE = True  # Set to False if you just want to clear without repopulating
DEPARTMENTAL_SCOPE_REPOPULATE = True  # Use new department-scoped creation logic


def reset_database():
    """
    Delete all data from the database in the correct order (respecting foreign keys)
    """
    print("=" * 60)
    print("🗑️  DATABASE RESET")
    print("=" * 60)
    print("\n⚠️  WARNING: This will delete ALL data from the database!")
    
    response = input("\nAre you sure you want to continue? (yes/y/no/n): ").lower().strip()
    if response not in ["yes", "y"]:
        print("❌ Operation cancelled.")
        return False
    
    print("\n🧹 Starting database cleanup...\n")
    
    # Use raw SQL with CASCADE to force delete all tables
    from django.db import connection
    
    # First delete all child tables, then parent tables
    tables_to_clear_raw = [
        # Child tables first (those that reference other tables)
        ("feedback_feedback", "Feedback"),
        ("grades_grade", "Grades"),
        ("comments_comment", "Comments"),
        ("cases_medicalattachment", "Medical Attachments"),
        ("cases_studentnotes", "Student Notes"),
        ("cases_learningoutcomes", "Learning Outcomes"),
        ("cases_diagnosismanagement", "Diagnosis & Management"),
        ("cases_investigations", "Investigations"),
        ("cases_physicalexamination", "Physical Examinations"),
        ("cases_clinicalhistory", "Clinical Histories"),
        ("cases_casepermission", "Case Permissions"),
        # Now delete the main tables
        ("cases_case", "Cases"),
        ("repositories_repository", "Repositories"),
        # Finally users and departments
        ("accounts_user", "Users"),
        ("cases_department", "Departments"),
    ]
    
    try:
        with connection.cursor() as cursor:
            for table_name, display_name in tables_to_clear_raw:
                try:
                    # Use CASCADE to delete even with foreign keys
                    cursor.execute(f"TRUNCATE TABLE {table_name} CASCADE")
                    print(f"   ✅ Cleared {display_name}")
                except Exception as e:
                    # If TRUNCATE fails, try DELETE
                    try:
                        cursor.execute(f"DELETE FROM {table_name}")
                        rows = cursor.rowcount
                        if rows > 0:
                            print(f"   ✅ Deleted {rows} {display_name}")
                        else:
                            print(f"   ⚪ No {display_name} to delete")
                    except Exception as e2:
                        print(f"   ⚠️  Skipped {display_name}: {str(e2)[:50]}")
    except Exception as e:
        print(f"   ⚠️  Database error: {str(e)[:80]}")
    
    # No need for ORM deletion since we already cleared everything
    models_to_clear = []
    
    for model, name in models_to_clear:
        try:
            count = model.objects.count()
            if count > 0:
                model.objects.all().delete()
                print(f"   ✅ Deleted {count} {name}")
            else:
                print(f"   ⚪ No {name} to delete")
        except Exception as e:
            print(f"   ⚠️  Skipped {name}: {str(e)[:60]}")
    
    print("\n✅ Database cleanup complete!")
    return True


def repopulate_database():
    """
    Run the populate_test_data script to create fresh test data
    """
    print("\n" + "=" * 60)
    print("📦 REPOPULATING DATABASE")
    print("=" * 60)
    
    try:
        from populate_test_data import create_test_data
        # Department-scoped test data; keep existing admin or recreate
        create_test_data(clear_existing=False)
        print("\n✅ Database repopulation complete!")
        return True
    except Exception as e:
        print(f"\n❌ Error during repopulation: {e}")
        return False


def main():
    """
    Main execution function
    """
    # Reset the database
    if not reset_database():
        return
    
    # Optionally repopulate
    if REPOPULATE:
        print("\n")
        repopulate = input("Do you want to repopulate with test data? (yes/no): ").lower()
        if repopulate == "yes":
            repopulate_database()
        else:
            print("\n💡 Tip: Run 'python populate_test_data.py' to create test data later.")
    
    print("\n" + "=" * 60)
    print("🎉 RESET COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()