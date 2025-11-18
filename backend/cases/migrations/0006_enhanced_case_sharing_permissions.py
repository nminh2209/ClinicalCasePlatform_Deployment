# Generated migration for enhanced case sharing permissions

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0005_alter_case_archived_by_alter_case_reviewed_by_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # First, add new fields to existing CasePermission model
        migrations.AddField(
            model_name='casepermission',
            name='share_type',
            field=models.CharField(
                choices=[
                    ('individual', 'Cá nhân'),
                    ('department', 'Khoa phòng'),
                    ('class_group', 'Lớp học'),
                    ('public', 'Công khai')
                ],
                default='individual',
                help_text='Loại chia sẻ',
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='casepermission',
            name='target_department',
            field=models.ForeignKey(
                blank=True,
                help_text='Khoa được chia sẻ',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='shared_cases',
                to='cases.department'
            ),
        ),
        migrations.AddField(
            model_name='casepermission',
            name='class_group',
            field=models.CharField(
                blank=True,
                help_text='Nhóm lớp học (VD: K15, Y6, etc.)',
                max_length=100
            ),
        ),
        migrations.AddField(
            model_name='casepermission',
            name='expires_at',
            field=models.DateTimeField(
                blank=True,
                help_text='Thời gian hết hạn (để trống nếu không giới hạn)',
                null=True
            ),
        ),
        migrations.AddField(
            model_name='casepermission',
            name='notes',
            field=models.TextField(
                blank=True,
                help_text='Ghi chú về quyền truy cập này'
            ),
        ),
        migrations.AddField(
            model_name='casepermission',
            name='access_count',
            field=models.PositiveIntegerField(
                default=0,
                help_text='Số lần truy cập'
            ),
        ),
        migrations.AddField(
            model_name='casepermission',
            name='last_accessed',
            field=models.DateTimeField(
                blank=True,
                help_text='Lần cuối truy cập',
                null=True
            ),
        ),
        # Update existing permission choices
        migrations.AlterField(
            model_name='casepermission',
            name='permission_type',
            field=models.CharField(
                choices=[
                    ('view', 'Chỉ xem'),
                    ('comment', 'Xem và bình luận'),
                    ('analyze', 'Xem, bình luận và phân tích'),
                    ('edit', 'Toàn quyền chỉnh sửa')
                ],
                default='view',
                max_length=20
            ),
        ),
        # Make user field nullable for group sharing
        migrations.AlterField(
            model_name='casepermission',
            name='user',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='case_permissions',
                to=settings.AUTH_USER_MODEL
            ),
        ),
        # Update meta options
        migrations.AlterModelOptions(
            name='casepermission',
            options={
                'verbose_name': 'Quyền truy cập ca bệnh',
                'verbose_name_plural': 'Quyền truy cập ca bệnh'
            },
        ),
        # Remove unique constraint and add indexes
        migrations.AlterUniqueTogether(
            name='casepermission',
            unique_together=set(),
        ),
        migrations.AddIndex(
            model_name='casepermission',
            index=models.Index(fields=['case', 'user'], name='cases_caseperm_case_user_idx'),
        ),
        migrations.AddIndex(
            model_name='casepermission',
            index=models.Index(fields=['case', 'share_type'], name='cases_caseperm_case_share_idx'),
        ),
        migrations.AddIndex(
            model_name='casepermission',
            index=models.Index(fields=['target_department'], name='cases_caseperm_dept_idx'),
        ),
        migrations.AddIndex(
            model_name='casepermission',
            index=models.Index(fields=['expires_at'], name='cases_caseperm_expires_idx'),
        ),
        
        # Create GuestAccess model
        migrations.CreateModel(
            name='GuestAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(help_text='Token truy cập duy nhất cho khách', max_length=255, unique=True)),
                ('guest_email', models.EmailField(help_text='Email người được mời', max_length=254)),
                ('guest_name', models.CharField(blank=True, help_text='Tên người được mời', max_length=200)),
                ('permission_type', models.CharField(choices=[('view', 'Chỉ xem'), ('comment', 'Xem và bình luận'), ('analyze', 'Xem, bình luận và phân tích'), ('edit', 'Toàn quyền chỉnh sửa')], default='view', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(help_text='Thời gian hết hạn (bắt buộc)')),
                ('is_active', models.BooleanField(default=True)),
                ('access_count', models.PositiveIntegerField(default=0)),
                ('last_accessed', models.DateTimeField(blank=True, null=True)),
                ('accessed_ips', models.JSONField(default=list, help_text='Danh sách IP đã truy cập')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guest_accesses', to='cases.case')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_guest_accesses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Truy cập khách',
                'verbose_name_plural': 'Truy cập khách',
                'db_table': 'cases_guestaccess',
            },
        ),
        migrations.AddIndex(
            model_name='guestaccess',
            index=models.Index(fields=['access_token'], name='cases_guestaccess_token_idx'),
        ),
        migrations.AddIndex(
            model_name='guestaccess',
            index=models.Index(fields=['case'], name='cases_guestaccess_case_idx'),
        ),
        migrations.AddIndex(
            model_name='guestaccess',
            index=models.Index(fields=['expires_at'], name='cases_guestaccess_expires_idx'),
        ),

        # Create CaseGroup model
        migrations.CreateModel(
            name='CaseGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Tên nhóm ca bệnh', max_length=200)),
                ('description', models.TextField(blank=True, help_text='Mô tả')),
                ('group_type', models.CharField(choices=[('department', 'Bộ sưu tập khoa'), ('class', 'Bộ sưu tập lớp'), ('assignment', 'Bài tập'), ('curriculum', 'Chương trình học')], default='assignment', max_length=20)),
                ('class_identifier', models.CharField(blank=True, help_text='Mã lớp (VD: K15Y1, Y6-ICU, etc.)', max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('is_public', models.BooleanField(default=False, help_text='Nhóm công khai (tất cả có thể xem)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cases', models.ManyToManyField(blank=True, help_text='Ca bệnh trong nhóm', related_name='case_groups', to='cases.case')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_case_groups', to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='case_groups', to='cases.department')),
            ],
            options={
                'verbose_name': 'Nhóm ca bệnh',
                'verbose_name_plural': 'Nhóm ca bệnh',
                'db_table': 'cases_casegroup',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='casegroup',
            index=models.Index(fields=['department', 'group_type'], name='cases_casegroup_dept_type_idx'),
        ),
        migrations.AddIndex(
            model_name='casegroup',
            index=models.Index(fields=['class_identifier'], name='cases_casegroup_class_idx'),
        ),
        migrations.AddIndex(
            model_name='casegroup',
            index=models.Index(fields=['created_by'], name='cases_casegroup_creator_idx'),
        ),

        # Create PermissionAuditLog model
        migrations.CreateModel(
            name='PermissionAuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('granted', 'Cấp quyền'), ('revoked', 'Thu hồi quyền'), ('modified', 'Thay đổi quyền'), ('accessed', 'Truy cập'), ('expired', 'Hết hạn')], help_text='Hành động được thực hiện', max_length=20)),
                ('permission_type', models.CharField(blank=True, choices=[('view', 'Chỉ xem'), ('comment', 'Xem và bình luận'), ('analyze', 'Xem, bình luận và phân tích'), ('edit', 'Toàn quyền chỉnh sửa')], help_text='Loại quyền', max_length=20)),
                ('description', models.TextField(blank=True, help_text='Mô tả chi tiết hành động')),
                ('ip_address', models.GenericIPAddressField(blank=True, help_text='Địa chỉ IP', null=True)),
                ('user_agent', models.TextField(blank=True, help_text='Thông tin trình duyệt/thiết bị')),
                ('additional_data', models.JSONField(default=dict, help_text='Dữ liệu bổ sung')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('actor_user', models.ForeignKey(blank=True, help_text='Người thực hiện hành động', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='performed_audit_logs', to=settings.AUTH_USER_MODEL)),
                ('case', models.ForeignKey(help_text='Ca bệnh liên quan', on_delete=django.db.models.deletion.CASCADE, related_name='permission_audit_logs', to='cases.case')),
                ('target_user', models.ForeignKey(blank=True, help_text='Người dùng được ảnh hưởng', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='permission_audit_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Nhật ký kiểm toán quyền',
                'verbose_name_plural': 'Nhật ký kiểm toán quyền',
                'db_table': 'cases_permissionauditlog',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='permissionauditlog',
            index=models.Index(fields=['case', 'action'], name='cases_auditlog_case_action_idx'),
        ),
        migrations.AddIndex(
            model_name='permissionauditlog',
            index=models.Index(fields=['target_user'], name='cases_auditlog_target_idx'),
        ),
        migrations.AddIndex(
            model_name='permissionauditlog',
            index=models.Index(fields=['actor_user'], name='cases_auditlog_actor_idx'),
        ),
        migrations.AddIndex(
            model_name='permissionauditlog',
            index=models.Index(fields=['created_at'], name='cases_auditlog_created_idx'),
        ),
    ]