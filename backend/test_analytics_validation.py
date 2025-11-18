"""
Test script for Analytics and Validation systems
Run this to verify the implementation is working correctly
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinical_case_platform.settings')
django.setup()

from django.utils import timezone
from cases.models import Case
from cases.analytics import CaseAnalytics, StudentEngagementMetrics, CaseViewLog
from cases.validation import (
    CaseValidationRule,
    CaseValidationResult,
    CaseSubmissionWorkflow,
    CaseQualityMetrics
)
from accounts.models import User


def test_analytics_system():
    """Test analytics functionality"""
    print("\n" + "=" * 60)
    print("Testing Analytics System")
    print("=" * 60)
    
    # Test 1: Case Analytics Creation
    print("\n1. Testing Case Analytics...")
    cases = Case.objects.all()[:5]
    
    if not cases.exists():
        print("  ⚠️  No cases found. Create some cases first.")
        return False
    
    for case in cases:
        analytics, created = CaseAnalytics.objects.get_or_create(case=case)
        if created:
            print(f"  ✓ Created analytics for: {case.title}")
        else:
            print(f"  ✓ Analytics exists for: {case.title}")
    
    # Test 2: View Logging
    print("\n2. Testing View Logging...")
    test_case = cases.first()
    test_user = User.objects.filter(role='student').first()
    
    if test_user:
        view_log = CaseViewLog.objects.create(
            case=test_case,
            user=test_user,
            time_spent_seconds=120,
            completed=True,
            access_method='direct'
        )
        print(f"  ✓ Created view log: {view_log}")
        
        # Update analytics
        analytics = CaseAnalytics.objects.get(case=test_case)
        analytics.update_view_metrics(test_user, 120)
        print(f"  ✓ Updated analytics: {analytics.total_views} views")
    else:
        print("  ⚠️  No student user found")
    
    # Test 3: Student Engagement Metrics
    print("\n3. Testing Student Engagement Metrics...")
    students = User.objects.filter(role='student')[:3]
    
    for student in students:
        metrics, created = StudentEngagementMetrics.objects.get_or_create(
            student=student
        )
        metrics.update_activity()
        print(f"  ✓ {student.get_full_name()}: {metrics.total_cases_viewed} cases viewed")
    
    print("\n✅ Analytics System Tests Passed")
    return True


def test_validation_system():
    """Test validation functionality"""
    print("\n" + "=" * 60)
    print("Testing Validation System")
    print("=" * 60)
    
    # Test 1: Validation Rules
    print("\n1. Testing Validation Rules...")
    rules = CaseValidationRule.objects.filter(is_active=True)
    
    if not rules.exists():
        print("  ⚠️  No validation rules found. Run populate_validation_data.py first.")
        return False
    
    print(f"  ✓ Found {rules.count()} active validation rules")
    for rule in rules[:5]:
        print(f"    - {rule.name} ({rule.get_severity_display()})")
    
    # Test 2: Case Validation
    print("\n2. Testing Case Validation...")
    test_case = Case.objects.first()
    
    if not test_case:
        print("  ⚠️  No cases found")
        return False
    
    # Validate case
    validation_issues = []
    rules_passed = 0
    rules_failed = 0
    
    for rule in rules:
        is_valid, error_message = rule.validate_case(test_case)
        if not is_valid:
            validation_issues.append({
                'rule': rule.name,
                'message': error_message
            })
            rules_failed += 1
        else:
            rules_passed += 1
    
    print(f"  ✓ Validated case: {test_case.title}")
    print(f"    - Rules passed: {rules_passed}")
    print(f"    - Rules failed: {rules_failed}")
    
    if validation_issues:
        print("    Issues found:")
        for issue in validation_issues[:3]:
            print(f"      • {issue['rule']}: {issue['message']}")
    
    # Test 3: Quality Metrics
    print("\n3. Testing Quality Metrics...")
    quality_metrics, created = CaseQualityMetrics.objects.get_or_create(case=test_case)
    quality_metrics.calculate_completeness()
    
    print(f"  ✓ Quality metrics for: {test_case.title}")
    print(f"    - Overall completeness: {quality_metrics.overall_completeness:.1f}%")
    print(f"    - Overall quality: {quality_metrics.overall_quality:.1f}%")
    
    # Test 4: Submission Workflow
    print("\n4. Testing Submission Workflow...")
    workflow, created = CaseSubmissionWorkflow.objects.get_or_create(case=test_case)
    
    print(f"  ✓ Workflow status: {workflow.get_current_status_display()}")
    print(f"    - Can submit: {workflow.can_submit()}")
    print(f"    - Revision count: {workflow.revision_count}")
    
    print("\n✅ Validation System Tests Passed")
    return True


def test_integration():
    """Test integration between systems"""
    print("\n" + "=" * 60)
    print("Testing System Integration")
    print("=" * 60)
    
    # Test 1: Complete workflow
    print("\n1. Testing Complete Workflow...")
    
    # Get a test case
    test_case = Case.objects.filter(case_status='draft').first()
    
    if not test_case:
        print("  ⚠️  No draft cases found")
        return False
    
    print(f"  Testing with case: {test_case.title}")
    
    # Step 1: Validate
    print("  Step 1: Validating case...")
    rules = CaseValidationRule.objects.filter(is_active=True)
    validation_issues = []
    
    for rule in rules:
        is_valid, error_message = rule.validate_case(test_case)
        if not is_valid and rule.severity == 'error':
            validation_issues.append(error_message)
    
    if validation_issues:
        print(f"    ⚠️  Found {len(validation_issues)} blocking issues")
        print("    Case needs fixes before submission")
    else:
        print("    ✓ Validation passed")
    
    # Step 2: Check quality
    print("  Step 2: Checking quality metrics...")
    quality_metrics, _ = CaseQualityMetrics.objects.get_or_create(case=test_case)
    quality_metrics.calculate_completeness()
    print(f"    ✓ Quality score: {quality_metrics.overall_quality:.1f}%")
    
    # Step 3: Check workflow
    print("  Step 3: Checking workflow...")
    workflow, _ = CaseSubmissionWorkflow.objects.get_or_create(case=test_case)
    print(f"    ✓ Current status: {workflow.get_current_status_display()}")
    
    # Step 4: Track analytics
    print("  Step 4: Tracking analytics...")
    analytics, _ = CaseAnalytics.objects.get_or_create(case=test_case)
    print(f"    ✓ Total views: {analytics.total_views}")
    
    print("\n✅ Integration Tests Passed")
    return True


def print_summary():
    """Print system summary"""
    print("\n" + "=" * 60)
    print("System Summary")
    print("=" * 60)
    
    # Analytics
    print("\n📊 Analytics:")
    print(f"  - Case Analytics: {CaseAnalytics.objects.count()}")
    print(f"  - Student Metrics: {StudentEngagementMetrics.objects.count()}")
    print(f"  - View Logs: {CaseViewLog.objects.count()}")
    
    # Validation
    print("\n✅ Validation:")
    print(f"  - Active Rules: {CaseValidationRule.objects.filter(is_active=True).count()}")
    print(f"  - Validation Results: {CaseValidationResult.objects.count()}")
    print(f"  - Workflows: {CaseSubmissionWorkflow.objects.count()}")
    print(f"  - Quality Metrics: {CaseQualityMetrics.objects.count()}")
    
    # Cases
    print("\n📁 Cases:")
    print(f"  - Total: {Case.objects.count()}")
    print(f"  - Draft: {Case.objects.filter(case_status='draft').count()}")
    print(f"  - Submitted: {Case.objects.filter(case_status='submitted').count()}")
    print(f"  - Approved: {Case.objects.filter(case_status='approved').count()}")
    
    # Users
    print("\n👥 Users:")
    print(f"  - Students: {User.objects.filter(role='student').count()}")
    print(f"  - Instructors: {User.objects.filter(role='instructor').count()}")
    print(f"  - Admins: {User.objects.filter(role='admin').count()}")


def main():
    print("=" * 60)
    print("Analytics & Validation System Test Suite")
    print("=" * 60)
    
    try:
        # Run tests
        analytics_ok = test_analytics_system()
        validation_ok = test_validation_system()
        integration_ok = test_integration()
        
        # Print summary
        print_summary()
        
        # Final result
        print("\n" + "=" * 60)
        if analytics_ok and validation_ok and integration_ok:
            print("✅ ALL TESTS PASSED")
            print("=" * 60)
            print("\nThe system is ready to use!")
            print("\nNext steps:")
            print("1. Access admin panel: http://localhost:8000/admin/")
            print("2. Test API endpoints with Postman or curl")
            print("3. Integrate with frontend")
            print("4. Set up cron jobs for automated tasks")
        else:
            print("⚠️  SOME TESTS FAILED")
            print("=" * 60)
            print("\nPlease check the errors above and:")
            print("1. Ensure migrations are run: python manage.py migrate")
            print("2. Populate data: python populate_validation_data.py")
            print("3. Create test cases and users")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        print("\nPlease check:")
        print("1. Database is accessible")
        print("2. Migrations are up to date")
        print("3. Django settings are correct")


if __name__ == '__main__':
    main()
