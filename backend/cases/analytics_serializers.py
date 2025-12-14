"""
Serializers for Analytics System
"""

from rest_framework import serializers
from .analytics import (
    CaseAnalytics,
    StudentEngagementMetrics,
    CaseViewLog,
    PlatformUsageStatistics,
    DepartmentAnalytics,
)


class CaseAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for case analytics"""

    case_title = serializers.CharField(source="case.title", read_only=True)
    case_id = serializers.IntegerField(source="case.id", read_only=True)

    class Meta:  # type: ignore[misc, assignment]
        model = CaseAnalytics
        fields = [
            "id",
            "case_id",
            "case_title",
            "total_views",
            "unique_viewers",
            "average_time_spent_seconds",
            "completion_rate",
            "total_comments",
            "total_feedback",
            "total_shares",
            "bookmark_count",
            "average_grade",
            "pass_rate",
            "learning_objective_achievement",
            "average_rating",
            "difficulty_rating",
            "relevance_rating",
            "last_viewed_at",
            "last_updated_at",
        ]
        read_only_fields = fields


class StudentEngagementMetricsSerializer(serializers.ModelSerializer):
    """Serializer for student engagement metrics"""

    student_name = serializers.CharField(source="student.get_full_name", read_only=True)
    student_email = serializers.CharField(source="student.email", read_only=True)
    department_name = serializers.CharField(
        source="student.department.name", read_only=True
    )

    class Meta:  # type: ignore[misc, assignment]
        model = StudentEngagementMetrics
        fields = [
            "id",
            "student_name",
            "student_email",
            "department_name",
            "total_cases_viewed",
            "total_cases_completed",
            "total_cases_submitted",
            "total_study_time_hours",
            "average_session_duration_minutes",
            "last_active_at",
            "total_comments_made",
            "total_questions_asked",
            "total_feedback_received",
            "average_grade",
            "highest_grade",
            "lowest_grade",
            "improvement_rate",
            "current_streak_days",
            "longest_streak_days",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class CaseViewLogSerializer(serializers.ModelSerializer):
    """Serializer for case view logs"""

    case_title = serializers.CharField(source="case.title", read_only=True)
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:  # type: ignore[misc, assignment]
        model = CaseViewLog
        fields = [
            "id",
            "case",
            "case_title",
            "user",
            "user_name",
            "viewed_at",
            "time_spent_seconds",
            "completed",
            "access_method",
            "device_type",
            "ip_address",
        ]
        read_only_fields = ["id", "viewed_at"]


class PlatformUsageStatisticsSerializer(serializers.ModelSerializer):
    """Serializer for platform usage statistics"""

    class Meta:  # type: ignore[misc, assignment]
        model = PlatformUsageStatistics
        fields = [
            "id",
            "period_type",
            "period_start",
            "period_end",
            "total_active_users",
            "total_active_students",
            "total_active_instructors",
            "new_users",
            "total_cases_created",
            "total_cases_submitted",
            "total_cases_reviewed",
            "total_case_views",
            "total_comments",
            "total_feedback",
            "total_grades_given",
            "average_grade",
            "average_completion_time_hours",
            "total_storage_used_mb",
            "total_attachments_uploaded",
            "created_at",
        ]
        read_only_fields = fields


class DepartmentAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for department analytics"""

    department_name = serializers.CharField(source="department.name", read_only=True)
    department_code = serializers.CharField(source="department.code", read_only=True)

    class Meta:  # type: ignore[misc, assignment]
        model = DepartmentAnalytics
        fields = [
            "id",
            "department_name",
            "department_code",
            "period_start",
            "period_end",
            "total_students",
            "total_instructors",
            "active_students",
            "total_cases",
            "cases_submitted",
            "cases_reviewed",
            "average_grade",
            "pass_rate",
            "average_completion_rate",
            "total_comments",
            "total_feedback",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class AnalyticsDashboardSerializer(serializers.Serializer):
    """
    Comprehensive analytics dashboard data
    Combines multiple metrics for overview
    """

    # Overview metrics
    total_cases = serializers.IntegerField()
    total_students = serializers.IntegerField()
    total_instructors = serializers.IntegerField()
    active_users_today = serializers.IntegerField()

    # Recent activity
    cases_created_this_week = serializers.IntegerField()
    cases_submitted_this_week = serializers.IntegerField()
    total_views_this_week = serializers.IntegerField()

    # Performance metrics
    average_grade = serializers.FloatField()
    average_completion_rate = serializers.FloatField()

    # Top performers
    top_students = StudentEngagementMetricsSerializer(many=True)
    most_viewed_cases = CaseAnalyticsSerializer(many=True)

    # Department breakdown
    department_stats = DepartmentAnalyticsSerializer(many=True)


class StudentProgressReportSerializer(serializers.Serializer):
    """
    Detailed progress report for individual student
    """

    student_info = serializers.DictField()
    engagement_metrics = StudentEngagementMetricsSerializer()
    recent_cases = serializers.ListField()
    grade_history = serializers.ListField()
    activity_timeline = serializers.ListField()
    strengths = serializers.ListField()
    areas_for_improvement = serializers.ListField()
