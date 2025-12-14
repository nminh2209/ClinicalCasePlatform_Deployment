"""
Views for Analytics System
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Q, Sum
from django.utils import timezone
from datetime import timedelta

from .analytics import (
    CaseAnalytics,
    StudentEngagementMetrics,
    CaseViewLog,
    PlatformUsageStatistics,
    DepartmentAnalytics,
)
from .analytics_serializers import (
    CaseAnalyticsSerializer,
    StudentEngagementMetricsSerializer,
    CaseViewLogSerializer,
    PlatformUsageStatisticsSerializer,
    DepartmentAnalyticsSerializer,
    AnalyticsDashboardSerializer,
    StudentProgressReportSerializer,
)
from cases.models import Case
from accounts.models import User


class CaseAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for case analytics
    Provides read-only access to case usage and engagement metrics
    """

    queryset = CaseAnalytics.objects.all()
    serializer_class = CaseAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # Students can only see analytics for their own cases
        if user.role == "student":  # type: ignore[attr-defined]
            queryset = queryset.filter(case__student=user)
        # Instructors can see analytics for cases in their department
        elif user.role == "instructor" and user.department:  # type: ignore[attr-defined]
            queryset = queryset.filter(
                Q(case__student__department=user.department)  # type: ignore[attr-defined]
                | Q(case__repository__department=user.department)  # type: ignore[attr-defined]
            )

        return queryset

    @action(detail=True, methods=["post"])
    def record_view(self, request, pk=None):
        """
        Record a case view
        POST /api/case-analytics/{id}/record_view/
        Body: {"time_spent_seconds": 120, "completed": true}
        """
        analytics = self.get_object()
        time_spent = request.data.get("time_spent_seconds", 0)

        # Create view log
        CaseViewLog.objects.create(
            case=analytics.case,
            user=request.user,
            time_spent_seconds=time_spent,
            completed=request.data.get("completed", False),
            access_method=request.data.get("access_method", "direct"),
            device_type=request.data.get("device_type", ""),
            ip_address=request.META.get("REMOTE_ADDR"),
        )

        # Update analytics
        analytics.update_view_metrics(request.user, time_spent)

        return Response(
            {"message": "Đã ghi nhận lượt xem", "total_views": analytics.total_views}
        )

    @action(detail=False, methods=["get"])
    def top_cases(self, request):
        """
        Get top performing cases
        GET /api/case-analytics/top_cases/?metric=views&limit=10
        """
        metric = request.query_params.get("metric", "views")
        limit = int(request.query_params.get("limit", 10))

        order_field = {
            "views": "-total_views",
            "engagement": "-total_comments",
            "rating": "-average_rating",
            "completion": "-completion_rate",
        }.get(metric, "-total_views")

        top_cases = self.get_queryset().order_by(order_field)[:limit]
        serializer = self.get_serializer(top_cases, many=True)

        return Response(serializer.data)


class StudentEngagementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for student engagement metrics
    Tracks student learning patterns and progress
    """

    queryset = StudentEngagementMetrics.objects.all()
    serializer_class = StudentEngagementMetricsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # Students can only see their own metrics
        if user.role == "student":  # type: ignore[attr-defined]
            queryset = queryset.filter(student=user)
        # Instructors can see metrics for students in their department
        elif user.role == "instructor" and user.department:  # type: ignore[attr-defined]
            queryset = queryset.filter(student__department=user.department)  # type: ignore[attr-defined]

        return queryset

    @action(detail=True, methods=["get"])
    def progress_report(self, request, pk=None):
        """
        Get detailed progress report for a student
        GET /api/student-engagement/{id}/progress_report/
        """
        metrics = self.get_object()
        student = metrics.student

        # Get recent cases
        recent_cases = Case.objects.filter(student=student).order_by("-created_at")[:10]

        # Get grade history
        from grades.models import Grade

        grades = Grade.objects.filter(case__student=student).order_by("created_at")
        grade_history = [
            {
                "date": g.created_at.date().isoformat(),  # type: ignore[attr-defined]
                "score": g.total_score,  # type: ignore[attr-defined]
                "case_title": g.case.title,
            }
            for g in grades
        ]

        # Get activity timeline
        recent_views = CaseViewLog.objects.filter(user=student).order_by("-viewed_at")[
            :20
        ]

        activity_timeline = [
            {
                "date": v.viewed_at.isoformat(),
                "action": "viewed_case",
                "case_title": v.case.title,
                "time_spent": v.time_spent_seconds,
            }
            for v in recent_views
        ]

        # Analyze strengths and areas for improvement
        strengths = []
        areas_for_improvement = []

        if metrics.current_streak_days >= 7:
            strengths.append(
                "Học tập đều đặn với chuỗi {} ngày liên tiếp".format(
                    metrics.current_streak_days
                )
            )

        if metrics.average_grade and metrics.average_grade >= 80:
            strengths.append(
                "Điểm số cao với trung bình {:.1f}".format(metrics.average_grade)
            )

        if metrics.improvement_rate > 10:
            strengths.append(
                "Tiến bộ tốt với tỷ lệ cải thiện {:.1f}%".format(
                    metrics.improvement_rate
                )
            )

        if metrics.total_comments_made < 5:
            areas_for_improvement.append(
                "Nên tham gia bình luận và thảo luận nhiều hơn"
            )

        if metrics.current_streak_days == 0:
            areas_for_improvement.append("Cần học tập đều đặn hơn")

        if metrics.average_grade and metrics.average_grade < 60:
            areas_for_improvement.append("Cần cải thiện điểm số")

        report_data = {
            "student_info": {
                "name": student.get_full_name(),
                "email": student.email,
                "student_id": student.student_id,
                "department": student.department.name if student.department else None,
            },
            "engagement_metrics": StudentEngagementMetricsSerializer(metrics).data,
            "recent_cases": [
                {
                    "id": c.id,  # type: ignore[attr-defined]
                    "title": c.title,
                    "status": c.case_status,
                    "created_at": c.created_at.isoformat(),
                }
                for c in recent_cases
            ],
            "grade_history": grade_history,
            "activity_timeline": activity_timeline,
            "strengths": strengths,
            "areas_for_improvement": areas_for_improvement,
        }

        serializer = StudentProgressReportSerializer(report_data)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def leaderboard(self, request):
        """
        Get student leaderboard
        GET /api/student-engagement/leaderboard/?metric=grade&limit=20
        """
        metric = request.query_params.get("metric", "grade")
        limit = int(request.query_params.get("limit", 20))

        order_field = {
            "grade": "-average_grade",
            "cases": "-total_cases_completed",
            "streak": "-current_streak_days",
            "improvement": "-improvement_rate",
        }.get(metric, "-average_grade")

        top_students = self.get_queryset().order_by(order_field)[:limit]
        serializer = self.get_serializer(top_students, many=True)

        return Response(serializer.data)


class AnalyticsDashboardViewSet(viewsets.ViewSet):
    """
    Comprehensive analytics dashboard
    Provides overview metrics for administrators and instructors
    """

    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"])
    def overview(self, request):
        """
        Get dashboard overview
        GET /api/analytics-dashboard/overview/
        """
        user = request.user

        # Calculate date ranges
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)

        # Base querysets
        cases_qs = Case.objects.all()
        students_qs = User.objects.filter(role="student")
        instructors_qs = User.objects.filter(role="instructor")

        # Filter by department for instructors
        if user.role == "instructor" and user.department:
            cases_qs = cases_qs.filter(
                Q(student__department=user.department)
                | Q(repository__department=user.department)
            )
            students_qs = students_qs.filter(department=user.department)
            instructors_qs = instructors_qs.filter(department=user.department)

        # Overview metrics
        total_cases = cases_qs.count()
        total_students = students_qs.count()
        total_instructors = instructors_qs.count()

        # Active users today
        active_today = (
            CaseViewLog.objects.filter(viewed_at__date=today)
            .values("user")
            .distinct()
            .count()
        )

        # Recent activity
        cases_created_this_week = cases_qs.filter(
            created_at__date__gte=week_ago
        ).count()
        cases_submitted_this_week = cases_qs.filter(
            submitted_at__date__gte=week_ago
        ).count()

        total_views_this_week = CaseViewLog.objects.filter(
            viewed_at__date__gte=week_ago
        ).count()

        # Performance metrics
        from grades.models import Grade

        grades_qs = Grade.objects.all()
        if user.role == "instructor" and user.department:
            grades_qs = grades_qs.filter(case__student__department=user.department)

        avg_grade = grades_qs.aggregate(Avg("total_score"))["total_score__avg"] or 0.0

        # Completion rate
        completed_cases = cases_qs.filter(case_status="approved").count()
        avg_completion_rate = (
            (completed_cases / total_cases * 100) if total_cases > 0 else 0.0
        )

        # Top students
        top_students_qs = StudentEngagementMetrics.objects.all()
        if user.role == "instructor" and user.department:
            top_students_qs = top_students_qs.filter(
                student__department=user.department
            )

        top_students = top_students_qs.order_by("-average_grade")[:5]

        # Most viewed cases
        most_viewed_qs = CaseAnalytics.objects.all()
        if user.role == "instructor" and user.department:
            most_viewed_qs = most_viewed_qs.filter(
                Q(case__student__department=user.department)
                | Q(case__repository__department=user.department)
            )

        most_viewed = most_viewed_qs.order_by("-total_views")[:5]

        # Department stats
        department_stats = []
        if user.role == "admin":
            recent_dept_analytics = (
                DepartmentAnalytics.objects.filter(period_start__gte=week_ago)
                .order_by("department", "-period_start")
                .distinct("department")[:10]
            )
            department_stats = DepartmentAnalyticsSerializer(
                recent_dept_analytics, many=True
            ).data

        dashboard_data = {
            "total_cases": total_cases,
            "total_students": total_students,
            "total_instructors": total_instructors,
            "active_users_today": active_today,
            "cases_created_this_week": cases_created_this_week,
            "cases_submitted_this_week": cases_submitted_this_week,
            "total_views_this_week": total_views_this_week,
            "average_grade": round(avg_grade, 2),
            "average_completion_rate": round(avg_completion_rate, 2),
            "top_students": StudentEngagementMetricsSerializer(
                top_students, many=True
            ).data,
            "most_viewed_cases": CaseAnalyticsSerializer(most_viewed, many=True).data,
            "department_stats": department_stats,
        }

        serializer = AnalyticsDashboardSerializer(dashboard_data)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def trends(self, request):
        """
        Get trend data over time
        GET /api/analytics-dashboard/trends/?period=30
        """
        days = int(request.query_params.get("period", 30))
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)

        # Daily statistics
        daily_stats = []
        current_date = start_date

        while current_date <= end_date:
            views = CaseViewLog.objects.filter(viewed_at__date=current_date).count()
            cases_created = Case.objects.filter(created_at__date=current_date).count()
            cases_submitted = Case.objects.filter(
                submitted_at__date=current_date
            ).count()

            daily_stats.append(
                {
                    "date": current_date.isoformat(),
                    "views": views,
                    "cases_created": cases_created,
                    "cases_submitted": cases_submitted,
                }
            )

            current_date += timedelta(days=1)

        return Response(
            {
                "period_days": days,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "daily_stats": daily_stats,
            }
        )


class PlatformStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Platform-wide usage statistics
    Admin-only access to system-level metrics
    """

    queryset = PlatformUsageStatistics.objects.all()
    serializer_class = PlatformUsageStatisticsSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=["post"])
    def generate_daily(self, request):
        """
        Generate daily statistics
        POST /api/platform-statistics/generate_daily/
        """
        today = timezone.now().date()

        # Check if already exists
        if PlatformUsageStatistics.objects.filter(
            period_type="daily", period_start=today
        ).exists():
            return Response(
                {"message": "Thống kê hôm nay đã tồn tại"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Calculate metrics
        active_users = (
            CaseViewLog.objects.filter(viewed_at__date=today)
            .values("user")
            .distinct()
            .count()
        )

        active_students = (
            CaseViewLog.objects.filter(viewed_at__date=today, user__role="student")
            .values("user")
            .distinct()
            .count()
        )

        active_instructors = (
            CaseViewLog.objects.filter(viewed_at__date=today, user__role="instructor")
            .values("user")
            .distinct()
            .count()
        )

        new_users = User.objects.filter(created_at__date=today).count()

        cases_created = Case.objects.filter(created_at__date=today).count()
        cases_submitted = Case.objects.filter(submitted_at__date=today).count()
        case_views = CaseViewLog.objects.filter(viewed_at__date=today).count()

        from comments.models import Comment
        from feedback.models import Feedback
        from grades.models import Grade

        comments = Comment.objects.filter(created_at__date=today).count()
        feedback = Feedback.objects.filter(created_at__date=today).count()
        grades = Grade.objects.filter(created_at__date=today).count()

        avg_grade = Grade.objects.filter(created_at__date=today).aggregate(
            Avg("total_score")
        )["total_score__avg"]

        # Create statistics
        stats = PlatformUsageStatistics.objects.create(
            period_type="daily",
            period_start=today,
            period_end=today,
            total_active_users=active_users,
            total_active_students=active_students,
            total_active_instructors=active_instructors,
            new_users=new_users,
            total_cases_created=cases_created,
            total_cases_submitted=cases_submitted,
            total_case_views=case_views,
            total_comments=comments,
            total_feedback=feedback,
            total_grades_given=grades,
            average_grade=avg_grade,
        )

        serializer = self.get_serializer(stats)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
