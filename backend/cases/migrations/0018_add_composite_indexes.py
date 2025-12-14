# Generated manually for performance optimization

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0017_add_investigation_lab_fields'),
    ]

    operations = [
        # Composite index for case listing filtered by status and student
        migrations.AddIndex(
            model_name='case',
            index=models.Index(
                fields=['case_status', 'student', '-created_at'],
                name='cases_case_status_student_idx'
            ),
        ),
        # Composite index for instructor dashboard queries (repository-based)
        migrations.AddIndex(
            model_name='case',
            index=models.Index(
                fields=['case_status', 'repository', '-updated_at'],
                name='cases_case_status_repo_updated_idx'
            ),
        ),
        # Composite index for public case queries
        migrations.AddIndex(
            model_name='case',
            index=models.Index(
                fields=['is_public', 'case_status', '-created_at'],
                name='cases_case_public_status_idx'
            ),
        ),
        # Composite index for admission date filtering
        migrations.AddIndex(
            model_name='case',
            index=models.Index(
                fields=['admission_date', 'case_status'],
                name='cases_case_admission_status_idx'
            ),
        ),
        # Composite index for permission queries with expiration
        migrations.AddIndex(
            model_name='casepermission',
            index=models.Index(
                fields=['case', 'is_active', 'expires_at'],
                name='cases_perm_case_active_exp_idx'
            ),
        ),
        # Composite index for department-based permission queries
        migrations.AddIndex(
            model_name='casepermission',
            index=models.Index(
                fields=['target_department', 'share_type', 'is_active'],
                name='cases_perm_dept_type_act_idx'
            ),
        ),
    ]
