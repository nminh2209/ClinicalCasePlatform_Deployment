from django.db import models
from django.conf import settings


class Comment(models.Model):
    """
    Comments on cases for discussion and collaboration
    Also used for reactions (likes) on public feed cases
    """

    case = models.ForeignKey(
        "cases.Case", on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField(blank=True)  # Allow blank for reactions
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
        help_text="Parent comment for threaded discussions",
    )
    is_instructor_feedback = models.BooleanField(
        default=False, help_text="Whether this comment is official instructor feedback"
    )
    
    # Social Media Reaction Fields
    is_reaction = models.BooleanField(
        default=False, help_text="True if this is a reaction/like, False if regular comment"
    )
    reaction_type = models.CharField(
        max_length=20,
        blank=True,
        choices=[
            ('like', '👍 Thích'),
            ('love', '❤️ Yêu thích'),
            ('insightful', '💡 Hữu ích'),
            ('learned', '📚 Học được nhiều'),
        ],
        help_text="Type of reaction if is_reaction=True",
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    class Meta:
        db_table = "comments_comment"
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=['case', 'author'],
                condition=models.Q(is_reaction=True),
                name='unique_reaction_per_user_per_case'
            )
        ]

    def __str__(self):
        if self.is_reaction:
            return f"{self.get_reaction_type_display()} by {self.author.get_full_name()} on {self.case.title}"
        return f"Comment by {self.author.get_full_name()} on {self.case.title}"

    @property
    def reply_count(self):
        return self.replies.count()
