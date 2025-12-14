from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Grade(models.Model):
    """
    Instructor grades and evaluations for cases
    """

    class GradeScale(models.TextChoices):
        PERCENTAGE = "percentage", "Percentage (0-100)"
        LETTER = "letter", "Letter Grade (A-F)"
        PASS_FAIL = "pass_fail", "Pass/Fail"
        POINTS = "points", "Points"

    case = models.OneToOneField(
        "cases.Case", on_delete=models.CASCADE, related_name="grade"
    )
    graded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="grades_given",
        limit_choices_to={"role": "instructor"},
        help_text="The instructor who assigned this grade",
    )

    # Grading details
    grade_scale = models.CharField(
        max_length=20, choices=GradeScale.choices, default=GradeScale.PERCENTAGE
    )
    score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Numeric score (0-100 for percentage, or custom range)",
    )
    letter_grade = models.CharField(
        max_length=5, blank=True, help_text="Letter grade (A, B, C, D, F, etc.)"
    )

    # Detailed evaluation
    clinical_reasoning_score = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Score for clinical reasoning (0-100)",
    )
    documentation_score = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Score for documentation quality (0-100)",
    )
    presentation_score = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Score for presentation (0-100)",
    )

    # Detailed grading criteria breakdown
    grading_criteria = models.JSONField(
        null=True,
        blank=True,
        help_text="Detailed grading criteria: {history, examination, differential, treatment, presentation}",
    )

    # Qualitative assessment
    evaluation_notes = models.TextField(
        blank=True, help_text="Detailed evaluation notes and comments"
    )
    strengths = models.TextField(
        blank=True, help_text="Student's strengths demonstrated in this case"
    )
    weaknesses = models.TextField(blank=True, help_text="Areas needing improvement")
    recommendations = models.TextField(
        blank=True, help_text="Recommendations for future learning"
    )

    # Metadata
    is_final = models.BooleanField(
        default=True, help_text="Whether this is the final grade or a draft"
    )
    graded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "grades_grade"
        verbose_name = "Grade"
        verbose_name_plural = "Grades"
        ordering = ["-graded_at"]

    def __str__(self):
        return f"Grade for {self.case.title}: {self.score}%"

    @property
    def student(self):
        """Get the student for this grade via the case relationship"""
        return self.case.student

    @property
    def overall_grade_letter(self):
        """Convert numeric score to letter grade"""
        if self.score >= 90:
            return "A"
        elif self.score >= 80:
            return "B"
        elif self.score >= 70:
            return "C"
        elif self.score >= 60:
            return "D"
        else:
            return "F"
