# Generated migration for Comment reactions

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        # Make content field optional for reactions
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(blank=True),
        ),
        
        # Add reaction fields
        migrations.AddField(
            model_name='comment',
            name='is_reaction',
            field=models.BooleanField(default=False, help_text='True if this is a reaction/like, False if regular comment'),
        ),
        migrations.AddField(
            model_name='comment',
            name='reaction_type',
            field=models.CharField(
                blank=True,
                choices=[
                    ('like', '👍 Thích'),
                    ('love', '❤️ Yêu thích'),
                    ('insightful', '💡 Hữu ích'),
                    ('learned', '📚 Học được nhiều')
                ],
                help_text='Type of reaction if is_reaction=True',
                max_length=20
            ),
        ),
        
        # Add unique constraint: one reaction per user per case
        migrations.AddConstraint(
            model_name='comment',
            constraint=models.UniqueConstraint(
                condition=models.Q(is_reaction=True),
                fields=('case', 'author'),
                name='unique_reaction_per_user_per_case'
            ),
        ),
        
        # Add index for reactions
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['case', 'is_reaction'], name='comments_comm_case_react_idx'),
        ),
    ]
