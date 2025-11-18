"""
Management command to generate analytics data
Usage: python manage.py generate_analytics --period daily
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Avg
from datetime import timedelta

from cases.analytics import (
    CaseAnalytics,
    StudentEngagementMetrics,
    PlatformUsageStatistics,
    DepartmentAnalytics,
    CaseViewLog,
)
from cases.models import Case
from accounts.models import User
from cases.medical_models import Department


class Command(BaseCommand):
    help = "Generate analytics data for cases, students, and platform usage"

    def add_arguments(self, parser):
        parser.add_argument(
            "--period",
            type=str,
            default="daily",
            choices=["daily", "weekly", "monthly"],
            help="Period type for statistics generation",
        )
        parser.add_argument(
            "--date",
            type=str,
            help="Specific date (YYYY-MM-DD) for analytics generation",
        )

    def handle(self, *args, **options):
        period = options["period"]

        if options["date"]:
            from datetime import datetime

            target_date = datetime.strptime(options["date"], "%Y-%m-%d").date()
        else:
            target_date = timezone.now().date()

        self.stdout.write(f"Generating {period} analytics for {target_date}...")

        # Initialize case analytics
        self.generate_case_analytics()

        # Update student engagement metrics
        self.update_student_engagement()

        # Generate platform statistics
        self.generate_platform_statistics(period, target_date)

        # Generate department analytics
        self.generate_department_analytics(target_date)

        self.stdout.write(self.style.SUCCESS("Analytics generation completed!"))

    def generate_case_analytics(self):
        """Initialize or update case analytics"""
        self.stdout.write("Generating case analytics...")

        cases = Case.objects.all()
        created_count = 0
        updated_count = 0

        for case in cases:
            analytics, created = CaseAnalytics.objects.get_or_create(case=case)

            if created:
                created_count += 1
            else:
                updated_count += 1

            # Recalculate metrics
            analytics.recalculate_engagement_metrics()
            analytics.recalculate_learning_metrics()

        self.stdout.write(f"  Created: {created_count}, Updated: {updated_count}")

    def update_student_engagement(self):
        """Update student engagement metrics"""
        self.stdout.write("Updating student engagement metrics...")

        students = User.objects.filter(role="student")
        updated_count = 0

        for student in students:
            metrics, created = StudentEngagementMetrics.objects.get_or_create(
                student=student
            )

            # Update all metrics
            metrics.update_activity()
            metrics.update_performance_metrics()
            metrics.update_streak()

            updated_count += 1

        self.stdout.write(f"  Updated {updated_count} student metrics")

    def generate_platform_statistics(self, period, target_date):
        """Generate platform-wide statistics"""
        self.stdout.write(f"Generating {period} platform statistics...")

        # Determine date range
        if period == "daily":
            period_start = target_date
            period_end = target_date
        elif period == "weekly":
            period_start = target_date - timedelta(days=target_date.weekday())
            period_end = period_start + timedelta(days=6)
        else:  # monthly
            period_start = target_date.replace(day=1)
            next_month = period_start.replace(day=28) + timedelta(days=4)
            period_end = next_month - timedelta(days=next_month.day)

        # Check if already exists
        existing = PlatformUsageStatistics.objects.filter(
            period_type=period, period_start=period_start
        ).first()

        if existing:
            self.stdout.write(
                self.style.WARNING(
                    f"  Statistics for {period_start} already exist. Skipping."
                )
            )
            return

        # Calculate metrics
        active_users = (
            CaseViewLog.objects.filter(
                viewed_at__date__gte=period_start, viewed_at__date__lte=period_end
            )
            .values("user")
            .distinct()
            .count()
        )

        active_students = (
            CaseViewLog.objects.filter(
                viewed_at__date__gte=period_start,
                viewed_at__date__lte=period_end,
                user__role="student",
            )
            .values("user")
            .distinct()
            .count()
        )

        active_instructors = (
            CaseViewLog.objects.filter(
                viewed_at__date__gte=period_start,
                viewed_at__date__lte=period_end,
                user__role="instructor",
            )
            .values("user")
            .distinct()
            .count()
        )

        new_users = User.objects.filter(
            created_at__date__gte=period_start, created_at__date__lte=period_end
        ).count()

        cases_created = Case.objects.filter(
            created_at__date__gte=period_start, created_at__date__lte=period_end
        ).count()

        cases_submitted = Case.objects.filter(
            submitted_at__date__gte=period_start, submitted_at__date__lte=period_end
        ).count()

        case_views = CaseViewLog.objects.filter(
            viewed_at__date__gte=period_start, viewed_at__date__lte=period_end
        ).count()

        # Create statistics
        stats = PlatformUsageStatistics.objects.create(
            period_type=period,
            period_start=period_start,
            period_end=period_end,
            total_active_users=active_users,
            total_active_students=active_students,
            total_active_instructors=active_instructors,
            new_users=new_users,
            total_cases_created=cases_created,
            total_cases_submitted=cases_submitted,
            total_case_views=case_views,
        )

        self.stdout.write(
            self.style.SUCCESS(f"  Created {period} statistics for {period_start}")
        )

    def generate_department_analytics(self, target_date):
        """Generate department-level analytics"""
        self.stdout.write("Generating department analytics...")

        departments = Department.objects.filter(is_active=True)

        # Weekly period
        period_start = target_date - timedelta(days=target_date.weekday())
        period_end = period_start + timedelta(days=6)

        for department in departments:
            # Check if already exists
            existing = DepartmentAnalytics.objects.filter(
                department=department, period_start=period_start
            ).first()

            if existing:
                continue

            # Calculate metrics
            total_students = User.objects.filter(
                role="student", department=department
            ).count()

            total_instructors = User.objects.filter(
                role="instructor", department=department
            ).count()

            active_students = (
                CaseViewLog.objects.filter(
                    viewed_at__date__gte=period_start,
                    viewed_at__date__lte=period_end,
                    user__role="student",
                    user__department=department,
                )
                .values("user")
                .distinct()
                .count()
            )

            total_cases = Case.objects.filter(student__department=department).count()

            cases_submitted = Case.objects.filter(
                student__department=department,
                submitted_at__date__gte=period_start,
                submitted_at__date__lte=period_end,
            ).count()

            # Create analytics
            DepartmentAnalytics.objects.create(
                department=department,
                period_start=period_start,
                period_end=period_end,
                total_students=total_students,
                total_instructors=total_instructors,
                active_students=active_students,
                total_cases=total_cases,
                cases_submitted=cases_submitted,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"  Created analytics for {departments.count()} departments"
            )
        )
