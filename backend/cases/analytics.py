"""
Case Analytics and Metrics System
Comprehensive analytics for tracking case usage, student engagement, and learning outcomes
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class CaseAnalytics(models.Model):
    """
    Analytics tracking for individual cases
    Tracks usage patterns, engagement metrics, and educational effectiveness
    """

    case = models.OneToOneField(
        "cases.Case",
        on_delete=models.CASCADE,
        related_name="analytics",
        help_text="Ca bệnh được theo dõi",
    )

    # Usage Metrics
    total_views = models.PositiveIntegerField(default=0, help_text="Tổng số lượt xem")
    unique_viewers = models.PositiveIntegerField(
        default=0, help_text="Số người xem duy nhất"
    )
    average_time_spent_seconds = models.PositiveIntegerField(
        default=0, help_text="Thời gian xem trung bình (giây)"
    )
    completion_rate = models.FloatField(default=0.0, help_text="Tỷ lệ hoàn thành (%)")

    # Engagement Metrics
    total_comments = models.PositiveIntegerField(
        default=0, help_text="Tổng số bình luận"
    )
    total_feedback = models.PositiveIntegerField(
        default=0, help_text="Tổng số phản hồi từ giảng viên"
    )
    total_shares = models.PositiveIntegerField(default=0, help_text="Số lần chia sẻ")
    bookmark_count = models.PositiveIntegerField(default=0, help_text="Số lần đánh dấu")

    # Learning Outcome Metrics
    average_grade = models.FloatField(
        null=True, blank=True, help_text="Điểm trung bình"
    )
    pass_rate = models.FloatField(default=0.0, help_text="Tỷ lệ đạt (%)")
    learning_objective_achievement = models.FloatField(
        default=0.0, help_text="Tỷ lệ đạt mục tiêu học tập (%)"
    )

    # Quality Metrics
    average_rating = models.FloatField(
        null=True, blank=True, help_text="Đánh giá trung bình (1-5)"
    )
    difficulty_rating = models.FloatField(
        null=True, blank=True, help_text="Đánh giá độ khó (1-5)"
    )
    relevance_rating = models.FloatField(
        null=True, blank=True, help_text="Đánh giá mức độ liên quan (1-5)"
    )

    # Timestamps
    last_viewed_at = models.DateTimeField(
        null=True, blank=True, help_text="Lần xem cuối"
    )
    last_updated_at = models.DateTimeField(
        auto_now=True, help_text="Lần cập nhật analytics cuối"
    )

    class Meta:
        db_table = "cases_caseanalytics"
        verbose_name = "Case Analytics"
        verbose_name_plural = "Case Analytics"

    def __str__(self):
        return f"Analytics for {self.case.title}"

    def update_view_metrics(self, user, time_spent_seconds=0):
        """Update view-related metrics"""
        self.total_views += 1
        self.last_viewed_at = timezone.now()

        # Update average time spent
        if time_spent_seconds > 0:
            total_time = self.average_time_spent_seconds * (self.total_views - 1)
            self.average_time_spent_seconds = int(
                (total_time + time_spent_seconds) / self.total_views
            )

        # Track unique viewers through CaseViewLog
        unique_count = (
            CaseViewLog.objects.filter(case=self.case).values("user").distinct().count()
        )
        self.unique_viewers = unique_count

        self.save()

    def recalculate_engagement_metrics(self):
        """Recalculate all engagement metrics"""
        from cases.models import Case
        from comments.models import Comment
        from feedback.models import Feedback

        case = self.case

        # Comments
        self.total_comments = Comment.objects.filter(case=case).count()

        # Feedback
        self.total_feedback = Feedback.objects.filter(case=case).count()

        # Shares (from permissions)
        from cases.models import CasePermission

        self.total_shares = CasePermission.objects.filter(case=case).count()

        self.save()

    def recalculate_learning_metrics(self):
        """Recalculate learning outcome metrics"""
        from grades.models import Grade

        grades = Grade.objects.filter(case=self.case)

        if grades.exists():
            # Average grade
            self.average_grade = grades.aggregate(models.Avg("total_score"))[
                "total_score__avg"
            ]

            # Pass rate (assuming 50% is passing)
            passing_grades = grades.filter(total_score__gte=50).count()
            self.pass_rate = (
                (passing_grades / grades.count()) * 100 if grades.count() > 0 else 0.0
            )

        self.save()


class StudentEngagementMetrics(models.Model):
    """
    Track individual student engagement across all cases
    Provides insights into student learning patterns and progress
    """

    student = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="engagement_metrics",
        limit_choices_to={"role": "student"},
        help_text="Sinh viên",
    )

    # Activity Metrics
    total_cases_viewed = models.PositiveIntegerField(
        default=0, help_text="Tổng số ca bệnh đã xem"
    )
    total_cases_completed = models.PositiveIntegerField(
        default=0, help_text="Tổng số ca bệnh hoàn thành"
    )
    total_cases_submitted = models.PositiveIntegerField(
        default=0, help_text="Tổng số ca bệnh đã nộp"
    )

    # Time Metrics
    total_study_time_hours = models.FloatField(
        default=0.0, help_text="Tổng thời gian học (giờ)"
    )
    average_session_duration_minutes = models.FloatField(
        default=0.0, help_text="Thời lượng phiên trung bình (phút)"
    )
    last_active_at = models.DateTimeField(
        null=True, blank=True, help_text="Lần hoạt động cuối"
    )

    # Engagement Metrics
    total_comments_made = models.PositiveIntegerField(
        default=0, help_text="Tổng số bình luận"
    )
    total_questions_asked = models.PositiveIntegerField(
        default=0, help_text="Tổng số câu hỏi"
    )
    total_feedback_received = models.PositiveIntegerField(
        default=0, help_text="Tổng số phản hồi nhận được"
    )

    # Performance Metrics
    average_grade = models.FloatField(
        null=True, blank=True, help_text="Điểm trung bình"
    )
    highest_grade = models.FloatField(null=True, blank=True, help_text="Điểm cao nhất")
    lowest_grade = models.FloatField(null=True, blank=True, help_text="Điểm thấp nhất")
    improvement_rate = models.FloatField(default=0.0, help_text="Tỷ lệ cải thiện (%)")

    # Streak Tracking
    current_streak_days = models.PositiveIntegerField(
        default=0, help_text="Chuỗi ngày học liên tiếp hiện tại"
    )
    longest_streak_days = models.PositiveIntegerField(
        default=0, help_text="Chuỗi ngày học liên tiếp dài nhất"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cases_studentengagementmetrics"
        verbose_name = "Student Engagement Metrics"
        verbose_name_plural = "Student Engagement Metrics"

    def __str__(self):
        return f"Engagement metrics for {self.student.get_full_name()}"

    def update_activity(self):
        """Update activity metrics"""
        from cases.models import Case

        # Cases viewed
        self.total_cases_viewed = (
            CaseViewLog.objects.filter(user=self.student)
            .values("case")
            .distinct()
            .count()
        )

        # Cases submitted
        self.total_cases_submitted = Case.objects.filter(
            student=self.student, case_status__in=["submitted", "reviewed", "approved"]
        ).count()

        # Update last active
        self.last_active_at = timezone.now()

        self.save()

    def update_performance_metrics(self):
        """Update performance metrics from grades"""
        from grades.models import Grade

        grades = Grade.objects.filter(case__student=self.student)

        if grades.exists():
            scores = grades.values_list("total_score", flat=True)
            self.average_grade = sum(scores) / len(scores)
            self.highest_grade = max(scores)
            self.lowest_grade = min(scores)

            # Calculate improvement rate (compare first half vs second half)
            if len(scores) >= 4:
                mid_point = len(scores) // 2
                first_half_avg = sum(scores[:mid_point]) / mid_point
                second_half_avg = sum(scores[mid_point:]) / (len(scores) - mid_point)

                if first_half_avg > 0:
                    self.improvement_rate = (
                        (second_half_avg - first_half_avg) / first_half_avg
                    ) * 100

        self.save()

    def update_streak(self):
        """Update learning streak based on activity"""
        today = timezone.now().date()

        # Get recent activity dates
        recent_views = (
            CaseViewLog.objects.filter(
                user=self.student, viewed_at__gte=today - timedelta(days=90)
            )
            .values_list("viewed_at__date", flat=True)
            .distinct()
            .order_by("-viewed_at__date")
        )

        if not recent_views:
            self.current_streak_days = 0
            self.save()
            return

        # Calculate current streak
        streak = 0
        check_date = today

        for view_date in recent_views:
            if view_date == check_date or view_date == check_date - timedelta(days=1):
                streak += 1
                check_date = view_date - timedelta(days=1)
            else:
                break

        self.current_streak_days = streak

        if streak > self.longest_streak_days:
            self.longest_streak_days = streak

        self.save()


class CaseViewLog(models.Model):
    """
    Detailed log of case views for analytics
    Tracks who viewed what and when
    """

    case = models.ForeignKey(
        "cases.Case",
        on_delete=models.CASCADE,
        related_name="view_logs",
        help_text="Ca bệnh được xem",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="case_views",
        help_text="Người xem",
    )

    # View Details
    viewed_at = models.DateTimeField(auto_now_add=True, help_text="Thời gian xem")
    time_spent_seconds = models.PositiveIntegerField(
        default=0, help_text="Thời gian xem (giây)"
    )
    completed = models.BooleanField(default=False, help_text="Đã xem hết")

    # Context
    access_method = models.CharField(
        max_length=50,
        choices=[
            ("direct", "Trực tiếp"),
            ("search", "Tìm kiếm"),
            ("shared", "Chia sẻ"),
            ("assignment", "Bài tập"),
        ],
        default="direct",
        help_text="Phương thức truy cập",
    )
    device_type = models.CharField(max_length=50, blank=True, help_text="Loại thiết bị")
    ip_address = models.GenericIPAddressField(
        null=True, blank=True, help_text="Địa chỉ IP"
    )

    class Meta:
        db_table = "cases_caseviewlog"
        verbose_name = "Case View Log"
        verbose_name_plural = "Case View Logs"
        ordering = ["-viewed_at"]
        indexes = [
            models.Index(fields=["case", "user"]),
            models.Index(fields=["viewed_at"]),
            models.Index(fields=["user", "viewed_at"]),
        ]

    def __str__(self):
        return (
            f"{self.user.get_full_name()} viewed {self.case.title} at {self.viewed_at}"
        )


class PlatformUsageStatistics(models.Model):
    """
    Platform-wide usage statistics
    Aggregated daily/weekly/monthly metrics for administrators
    """

    class PeriodType(models.TextChoices):
        DAILY = "daily", "Hàng ngày"
        WEEKLY = "weekly", "Hàng tuần"
        MONTHLY = "monthly", "Hàng tháng"

    period_type = models.CharField(
        max_length=20, choices=PeriodType.choices, help_text="Loại chu kỳ"
    )
    period_start = models.DateField(help_text="Ngày bắt đầu chu kỳ")
    period_end = models.DateField(help_text="Ngày kết thúc chu kỳ")

    # User Metrics
    total_active_users = models.PositiveIntegerField(
        default=0, help_text="Tổng số người dùng hoạt động"
    )
    total_active_students = models.PositiveIntegerField(
        default=0, help_text="Tổng số sinh viên hoạt động"
    )
    total_active_instructors = models.PositiveIntegerField(
        default=0, help_text="Tổng số giảng viên hoạt động"
    )
    new_users = models.PositiveIntegerField(default=0, help_text="Số người dùng mới")

    # Case Metrics
    total_cases_created = models.PositiveIntegerField(
        default=0, help_text="Tổng số ca bệnh tạo mới"
    )
    total_cases_submitted = models.PositiveIntegerField(
        default=0, help_text="Tổng số ca bệnh nộp"
    )
    total_cases_reviewed = models.PositiveIntegerField(
        default=0, help_text="Tổng số ca bệnh xem xét"
    )
    total_case_views = models.PositiveIntegerField(
        default=0, help_text="Tổng số lượt xem ca bệnh"
    )

    # Engagement Metrics
    total_comments = models.PositiveIntegerField(
        default=0, help_text="Tổng số bình luận"
    )
    total_feedback = models.PositiveIntegerField(
        default=0, help_text="Tổng số phản hồi"
    )
    total_grades_given = models.PositiveIntegerField(
        default=0, help_text="Tổng số điểm đã chấm"
    )

    # Performance Metrics
    average_grade = models.FloatField(
        null=True, blank=True, help_text="Điểm trung bình"
    )
    average_completion_time_hours = models.FloatField(
        null=True, blank=True, help_text="Thời gian hoàn thành trung bình (giờ)"
    )

    # System Metrics
    total_storage_used_mb = models.FloatField(
        default=0.0, help_text="Dung lượng lưu trữ sử dụng (MB)"
    )
    total_attachments_uploaded = models.PositiveIntegerField(
        default=0, help_text="Tổng số tệp đính kèm tải lên"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cases_platformusagestatistics"
        verbose_name = "Platform Usage Statistics"
        verbose_name_plural = "Platform Usage Statistics"
        ordering = ["-period_start"]
        unique_together = [["period_type", "period_start"]]
        indexes = [
            models.Index(fields=["period_type", "period_start"]),
        ]

    def __str__(self):
        return f"{self.get_period_type_display()} stats for {self.period_start}"


class DepartmentAnalytics(models.Model):
    """
    Department-level analytics
    Track performance and usage by department
    """

    department = models.ForeignKey(
        "cases.Department",
        on_delete=models.CASCADE,
        related_name="analytics",
        help_text="Khoa phòng",
    )
    period_start = models.DateField(help_text="Ngày bắt đầu chu kỳ")
    period_end = models.DateField(help_text="Ngày kết thúc chu kỳ")

    # User Metrics
    total_students = models.PositiveIntegerField(
        default=0, help_text="Tổng số sinh viên"
    )
    total_instructors = models.PositiveIntegerField(
        default=0, help_text="Tổng số giảng viên"
    )
    active_students = models.PositiveIntegerField(
        default=0, help_text="Số sinh viên hoạt động"
    )

    # Case Metrics
    total_cases = models.PositiveIntegerField(default=0, help_text="Tổng số ca bệnh")
    cases_submitted = models.PositiveIntegerField(
        default=0, help_text="Số ca bệnh đã nộp"
    )
    cases_reviewed = models.PositiveIntegerField(
        default=0, help_text="Số ca bệnh đã xem xét"
    )

    # Performance Metrics
    average_grade = models.FloatField(
        null=True, blank=True, help_text="Điểm trung bình"
    )
    pass_rate = models.FloatField(default=0.0, help_text="Tỷ lệ đạt (%)")
    average_completion_rate = models.FloatField(
        default=0.0, help_text="Tỷ lệ hoàn thành trung bình (%)"
    )

    # Engagement Metrics
    total_comments = models.PositiveIntegerField(
        default=0, help_text="Tổng số bình luận"
    )
    total_feedback = models.PositiveIntegerField(
        default=0, help_text="Tổng số phản hồi"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cases_departmentanalytics"
        verbose_name = "Department Analytics"
        verbose_name_plural = "Department Analytics"
        ordering = ["-period_start"]
        unique_together = [["department", "period_start"]]
        indexes = [
            models.Index(fields=["department", "period_start"]),
        ]

    def __str__(self):
        return f"Analytics for {self.department.name} ({self.period_start})"
