#!/usr/bin/env python
"""
Verify database integrity after fix
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clinical_case_platform.settings")
django.setup()

from cases.models import Case
from accounts.models import User
from repositories.models import Repository
from django.db import connection

def verify_database():
    """Run comprehensive database verification"""
    print("🔍 Verifying Database Integrity...\n")
    
    # 1. Check Case model can query with all fields
    print("1️⃣ Testing Case model queries...")
    try:
        total_cases = Case.objects.count()
        print(f"   ✅ Total cases: {total_cases}")
        
        # Test feed-related fields
        published_to_feed = Case.objects.filter(is_published_to_feed=True).count()
        print(f"   ✅ Cases published to feed: {published_to_feed}")
        
        featured_cases = Case.objects.filter(is_featured=True).count()
        print(f"   ✅ Featured cases: {featured_cases}")
        
        # Test complex query
        draft_cases = Case.objects.filter(
            case_status='draft',
            is_published_to_feed=False
        ).count()
        print(f"   ✅ Draft cases (not published): {draft_cases}")
        
    except Exception as e:
        print(f"   ❌ Error querying Case model: {e}")
        return False
    
    # 2. Check foreign key relationships
    print("\n2️⃣ Testing Foreign Key Relationships...")
    try:
        # Get a case with all relationships
        case = Case.objects.select_related(
            'student', 
            'repository', 
            'template',
            'published_by'
        ).first()
        
        if case:
            print(f"   ✅ Case FK to student: {case.student.email if case.student else 'None'}")
            print(f"   ✅ Case FK to repository: {case.repository.name if case.repository else 'None'}")
            print(f"   ✅ Case FK to template: {case.template.name if case.template else 'None'}")
            print(f"   ✅ Case FK to published_by: {case.published_by.email if case.published_by else 'None'}")
        else:
            print("   ℹ️ No cases found to test relationships")
            
    except Exception as e:
        print(f"   ❌ Error testing relationships: {e}")
        return False
    
    # 3. Check all feed-related columns exist and are accessible
    print("\n3️⃣ Testing Feed-Related Columns...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    is_published_to_feed,
                    published_to_feed_at,
                    published_by_id,
                    feed_visibility,
                    is_featured,
                    reaction_count
                FROM cases_case
                LIMIT 1;
            """)
            result = cursor.fetchone()
            if result:
                print(f"   ✅ All 6 feed columns are accessible via SQL")
            else:
                print(f"   ℹ️ No data to test, but columns exist")
    except Exception as e:
        print(f"   ❌ Error accessing feed columns: {e}")
        return False
    
    # 4. Test creating a new case
    print("\n4️⃣ Testing Case Creation...")
    try:
        student = User.objects.filter(role='student').first()
        repo = Repository.objects.first()
        
        if student and repo:
            test_case = Case(
                title="Test Case - Verification",
                student=student,
                repository=repo,
                patient_name="Test Patient",
                patient_age=30,
                patient_gender="male",
                specialty="Test",
                priority_level="low",
                is_published_to_feed=False,
                feed_visibility="department",
                is_featured=False,
                reaction_count=0
            )
            # Don't save, just validate
            test_case.full_clean()
            print("   ✅ Case model validation passed")
        else:
            print("   ℹ️ Skipping case creation test (no student or repository)")
            
    except Exception as e:
        print(f"   ❌ Error creating test case: {e}")
        return False
    
    # 5. Summary
    print("\n" + "="*60)
    print("✅ DATABASE VERIFICATION COMPLETE")
    print("="*60)
    print("All tests passed! Database is in good working order.")
    print("\n📊 Current Data:")
    print(f"   • Users: {User.objects.count()}")
    print(f"   • Cases: {Case.objects.count()}")
    print(f"   • Repositories: {Repository.objects.count()}")
    
    return True

if __name__ == "__main__":
    try:
        success = verify_database()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ VERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
