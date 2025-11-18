# Generated migration for social media feed feature

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cases', '0013_remove_medicalattachment_is_confidential_and_more'),
    ]

    operations = [
        # Add social media feed fields to Case model
        migrations.AddField(
            model_name='case',
            name='is_published_to_feed',
            field=models.BooleanField(default=False, help_text='Ca bệnh đã được xuất bản lên feed công khai'),
        ),
        migrations.AddField(
            model_name='case',
            name='published_to_feed_at',
            field=models.DateTimeField(blank=True, help_text='Thời điểm xuất bản lên feed', null=True),
        ),
        migrations.AddField(
            model_name='case',
            name='published_by',
            field=models.ForeignKey(
                blank=True,
                help_text='Giảng viên xuất bản ca bệnh lên feed',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='published_feed_cases',
                to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name='case',
            name='feed_visibility',
            field=models.CharField(
                choices=[('department', 'Cùng khoa'), ('university', 'Toàn trường')],
                default='department',
                help_text='Phạm vi hiển thị trên feed công khai',
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='case',
            name='is_featured',
            field=models.BooleanField(default=False, help_text='Ca bệnh nổi bật (được chọn bởi giảng viên)'),
        ),
        migrations.AddField(
            model_name='case',
            name='reaction_count',
            field=models.PositiveIntegerField(default=0, help_text='Tổng số reactions (likes, loves, etc.)'),
        ),
        
        # Add indexes for performance
        migrations.AddIndex(
            model_name='case',
            index=models.Index(fields=['-published_to_feed_at'], name='cases_case_pub_feed_idx'),
        ),
        migrations.AddIndex(
            model_name='case',
            index=models.Index(fields=['is_published_to_feed', 'feed_visibility'], name='cases_case_feed_vis_idx'),
        ),
        migrations.AddIndex(
            model_name='case',
            index=models.Index(fields=['is_featured'], name='cases_case_featured_idx'),
        ),
    ]
