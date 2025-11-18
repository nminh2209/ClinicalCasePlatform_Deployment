"""
Admin interfaces for Analytics System
"""

from django.contrib import admin
from .analytics import (
    CaseAnalytics,
    StudentEngagementMetrics,
    CaseViewLog,
    PlatformUsageStatistics,
    DepartmentAnalytics,
)


@admin.register(CaseAnalytics)
class CaseAnalyticsAdmin(admin.ModelAdmin):
    list_display = [
        "case",
        "total_views",
        "unique_viewers",
        "completion_rate",
        "average_grade",
        "pass_rate",
        "last_viewed_at",
    ]
    list_filter = ["last_viewed_at"]
    search_fields = ["case__title", "case__student__email"]
    readonly_fields = [
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

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(StudentEngagementMetrics)
class StudentEngagementMetricsAdmin(admin.ModelAdmin):
    list_display = [
        "student",
        "total_cases_viewed",
        "total_cases_completed",
        "average_grade",
        "current_streak_days",
        "last_active_at",
    ]
    list_filter = ["last_active_at", "student__department"]
    search_fields = ["student__email", "student__first_name", "student__last_name"]
    readonly_fields = [
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

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CaseViewLog)
class CaseViewLogAdmin(admin.ModelAdmin):
    list_display = [
        "case",
        "user",
        "viewed_at",
        "time_spent_seconds",
        "completed",
        "access_method",
    ]
    list_filter = ["viewed_at", "completed", "access_method"]
    search_fields = ["case__title", "user__email"]
    readonly_fields = ["viewed_at"]
    date_hierarchy = "viewed_at"

    def has_add_permission(self, request):
        return False


@admin.register(PlatformUsageStatistics)
class PlatformUsageStatisticsAdmin(admin.ModelAdmin):
    list_display = [
        "period_type",
        "period_start",
        "period_end",
        "total_active_users",
        "total_cases_created",
        "total_case_views",
        "average_grade",
    ]
    list_filter = ["period_type", "period_start"]
    readonly_fields = [
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
    date_hierarchy = "period_start"


@admin.register(DepartmentAnalytics)
class DepartmentAnalyticsAdmin(admin.ModelAdmin):
    list_display = [
        "department",
        "period_start",
        "period_end",
        "total_students",
        "active_students",
        "total_cases",
        "average_grade",
        "pass_rate",
    ]
    list_filter = ["department", "period_start"]
    readonly_fields = [
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
    date_hierarchy = "period_start"
