from django.db import models
from django.conf import settings


class Feedback(models.Model):
    """
    Structured feedback from instructors on cases
    """

    class FeedbackType(models.TextChoices):
        GENERAL = "general", "General Feedback"
        CLINICAL_REASONING = "clinical_reasoning", "Clinical Reasoning"
        DOCUMENTATION = "documentation", "Documentation Quality"
        PRESENTATION = "presentation", "Presentation Skills"

    case = models.ForeignKey(
        "cases.Case", on_delete=models.CASCADE, related_name="feedback"
    )
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="given_feedback",
        limit_choices_to={"role": "instructor"},
    )
    feedback_type = models.CharField(
        max_length=30, choices=FeedbackType.choices, default=FeedbackType.GENERAL
    )
    content = models.TextField()
    strengths = models.TextField(blank=True, help_text="What the student did well")
    areas_for_improvement = models.TextField(
        blank=True, help_text="Areas where the student can improve"
    )
    recommendations = models.TextField(
        blank=True, help_text="Specific recommendations for improvement"
    )
    is_public = models.BooleanField(
        default=True, help_text="Whether this feedback is visible to the student"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "feedback_feedback"
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Feedback on {self.case.title} by {self.instructor.get_full_name()}"
