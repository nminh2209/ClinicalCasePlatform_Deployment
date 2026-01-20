#!/usr/bin/env python
"""
Database Health Check and Management Utility

This script provides various database management tasks:
- Check database health
- Verify migrations
- Quick data summary
- Schema verification

Usage:
    python db_health_check.py [--check-migrations] [--check-schema] [--summary]
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import sys
import django
import argparse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clinical_case_platform.settings")
django.setup()

from django.db import connection
from django.core.management import call_command
from cases.models import Case
from cases.medical_models import Department
from accounts.models import User
from repositories.models import Repository
from templates.models import CaseTemplate


def check_migrations():
    """Check if all migrations are applied"""
    print("📋 Checking Migration Status...")
    
    try:
        from django.db.migrations.executor import MigrationExecutor
        executor = MigrationExecutor(connection)
        
        # Get list of unapplied migrations
        targets = executor.loader.graph.leaf_nodes()
        plan = executor.migration_plan(targets)
        
        if plan:
            print("   ⚠️ Unapplied migrations found:")
            for migration, backwards in plan:
                print(f"      • {migration.app_label}.{migration.name}")
            return False
        else:
            print("   ✅ All migrations are up to date")
            return True
            
    except Exception as e:
        print(f"   ❌ Error checking migrations: {e}")
        return False


def verify_schema():
    """Verify critical schema elements"""
    print("\n🔍 Verifying Database Schema...")
    
    critical_tables = [
        'accounts_user',
        'cases_case',
        'cases_department',
        'repositories_repository',
        'templates_casetemplate',
    ]
    
    all_ok = True
    with connection.cursor() as cursor:
        for table in critical_tables:
            cursor.execute(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = '{table}'
                );
            """)
            exists = cursor.fetchone()[0]
            
            if exists:
                print(f"   ✅ Table exists: {table}")
            else:
                print(f"   ❌ Table missing: {table}")
                all_ok = False
        
        # Check for feed columns in cases_case
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='cases_case' 
            AND column_name IN (
                'is_published_to_feed',
                'published_to_feed_at',
                'published_by_id',
                'feed_visibility',
                'is_featured',
                'reaction_count'
            )
            ORDER BY column_name;
        """)
        feed_columns = [row[0] for row in cursor.fetchall()]
        
        expected_feed_columns = [
            'feed_visibility',
            'is_featured',
            'is_published_to_feed',
            'published_by_id',
            'published_to_feed_at',
            'reaction_count'
        ]
        
        if len(feed_columns) == 6:
            print(f"   ✅ All 6 feed columns present in cases_case")
        else:
            print(f"   ⚠️ Feed columns: {len(feed_columns)}/6 found")
            missing = set(expected_feed_columns) - set(feed_columns)
            if missing:
                print(f"      Missing: {', '.join(missing)}")
            all_ok = False
    
    return all_ok


def print_summary():
    """Print database summary"""
    print("\n📊 Database Summary")
    print("=" * 60)
    
    try:
        # Count records in each model
        departments = Department.objects.count()
        users = User.objects.count()
        students = User.objects.filter(role='student').count()
        instructors = User.objects.filter(role='instructor').count()
        admins = User.objects.filter(role='admin').count()
        repositories = Repository.objects.count()
        templates = CaseTemplate.objects.count()
        cases = Case.objects.count()
        
        # Case status breakdown
        draft_cases = Case.objects.filter(case_status='draft').count()
        submitted_cases = Case.objects.filter(case_status='submitted').count()
        reviewed_cases = Case.objects.filter(case_status='reviewed').count()
        approved_cases = Case.objects.filter(case_status='approved').count()
        
        # Feed statistics
        published_to_feed = Case.objects.filter(is_published_to_feed=True).count()
        featured_cases = Case.objects.filter(is_featured=True).count()
        
        print(f"   🏥 Departments: {departments}")
        print(f"   👥 Users: {users}")
        print(f"      ├─ Students: {students}")
        print(f"      ├─ Instructors: {instructors}")
        print(f"      └─ Admins: {admins}")
        print(f"   📁 Repositories: {repositories}")
        print(f"   📋 Templates: {templates}")
        print(f"   📝 Cases: {cases}")
        print(f"      ├─ Draft: {draft_cases}")
        print(f"      ├─ Submitted: {submitted_cases}")
        print(f"      ├─ Reviewed: {reviewed_cases}")
        print(f"      ├─ Approved: {approved_cases}")
        print(f"      ├─ Published to Feed: {published_to_feed}")
        print(f"      └─ Featured: {featured_cases}")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"   ❌ Error generating summary: {e}")


def check_database_connection():
    """Verify database connection"""
    print("🔌 Checking Database Connection...")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"   ✅ Connected to PostgreSQL")
            print(f"      Version: {version.split(',')[0]}")
            
            cursor.execute("SELECT current_database();")
            db_name = cursor.fetchone()[0]
            print(f"      Database: {db_name}")
            
        return True
        
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Database Health Check and Management Utility'
    )
    parser.add_argument(
        '--check-migrations',
        action='store_true',
        help='Check migration status'
    )
    parser.add_argument(
        '--check-schema',
        action='store_true',
        help='Verify database schema'
    )
    parser.add_argument(
        '--summary',
        action='store_true',
        help='Print database summary'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Run all checks'
    )
    
    args = parser.parse_args()
    
    # If no arguments, run all checks
    if not any([args.check_migrations, args.check_schema, args.summary, args.all]):
        args.all = True
    
    print("🏥 Clinical Case Platform - Database Health Check")
    print("=" * 60)
    print()
    
    all_ok = True
    
    # Check database connection first
    if not check_database_connection():
        print("\n❌ Cannot proceed: Database connection failed")
        sys.exit(1)
    
    print()
    
    # Run requested checks
    if args.all or args.check_migrations:
        if not check_migrations():
            all_ok = False
    
    if args.all or args.check_schema:
        if not verify_schema():
            all_ok = False
    
    if args.all or args.summary:
        print_summary()
    
    # Final status
    print()
    if all_ok:
        print("✅ All checks passed! Database is healthy.")
        sys.exit(0)
    else:
        print("⚠️ Some issues detected. Please review the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
