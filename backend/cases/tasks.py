"""
Celery tasks for case-related heavy operations
"""
from celery import shared_task
from django.core.cache import cache
from django.utils import timezone
from django.db.models import Count, Q
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def generate_case_statistics_task(self, filters=None):
    """
    Generate comprehensive case statistics in background
    
    Args:
        filters: Dictionary of filters to apply
        
    Returns:
        Task ID for retrieving results from cache
    """
    try:
        from cases.models import Case
        
        queryset = Case.objects.all()
        
        # Apply filters
        if filters:
            if 'department' in filters:
                queryset = queryset.filter(
                    Q(student__department_id=filters['department']) |
                    Q(repository__department_id=filters['department'])
                )
            if 'date_from' in filters:
                queryset = queryset.filter(created_at__gte=filters['date_from'])
            if 'date_to' in filters:
                queryset = queryset.filter(created_at__lte=filters['date_to'])
            if 'status' in filters:
                queryset = queryset.filter(case_status=filters['status'])
        
        # Generate statistics
        statistics = {
            'total_cases': queryset.count(),
            'by_status': list(queryset.values('case_status').annotate(count=Count('id'))),
            'by_specialty': list(queryset.values('specialty').annotate(count=Count('id')).order_by('-count')[:10]),
            'by_priority': list(queryset.values('priority_level').annotate(count=Count('id'))),
            'generated_at': timezone.now().isoformat()
        }
        
        # Cache results for 1 hour
        cache_key = f"case_statistics_{self.request.id}"
        cache.set(cache_key, statistics, 3600)
        
        logger.info(f"Generated case statistics: {statistics['total_cases']} cases")
        
        return {
            'status': 'completed',
            'task_id': self.request.id,
            'cache_key': cache_key,
            'total_cases': statistics['total_cases']
        }
        
    except Exception as exc:
        logger.error(f"Error generating case statistics: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def bulk_update_case_status(self, case_ids, new_status, updated_by_id):
    """
    Update status for multiple cases in background
    
    Args:
        case_ids: List of case IDs to update
        new_status: New status to set
        updated_by_id: User ID performing the update
    """
    try:
        from cases.models import Case
        from accounts.models import User
        
        updated_by = User.objects.get(id=updated_by_id)
        cases = Case.objects.filter(id__in=case_ids)
        
        updated_count = cases.update(
            case_status=new_status,
            updated_at=timezone.now()
        )
        
        # Create notifications for affected students
        from notifications.models import Notification
        for case in cases:
            Notification.objects.create(
                recipient=case.student,
                notification_type='case_review',
                title='Case Status Updated',
                message=f'Your case "{case.title}" status was updated to {new_status}',
                related_case=case,
                action_url=f'/cases/{case.id}'
            )
        
        logger.info(f"Bulk updated {updated_count} cases to status {new_status} by user {updated_by_id}")
        
        return {
            'status': 'completed',
            'updated_count': updated_count,
            'new_status': new_status
        }
        
    except Exception as exc:
        logger.error(f"Error in bulk status update: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True)
def cleanup_old_case_data(self, days=365):
    """
    Clean up old draft cases and expired permissions
    
    Args:
        days: Number of days to keep data (default 365)
    """
    try:
        from cases.models import Case, CasePermission
        from datetime import timedelta
        
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Delete old draft cases
        old_drafts = Case.objects.filter(
            case_status='draft',
            created_at__lt=cutoff_date
        )
        draft_count = old_drafts.count()
        old_drafts.delete()
        
        # Delete expired permissions
        expired_perms = CasePermission.objects.filter(
            expires_at__lt=timezone.now(),
            is_active=True
        )
        perm_count = expired_perms.count()
        expired_perms.update(is_active=False)
        
        logger.info(f"Cleaned up {draft_count} old drafts and {perm_count} expired permissions")
        
        return {
            'status': 'completed',
            'drafts_deleted': draft_count,
            'permissions_deactivated': perm_count
        }
        
    except Exception as exc:
        logger.error(f"Error cleaning up old data: {exc}")
        return {'status': 'failed', 'error': str(exc)}


@shared_task(bind=True, max_retries=3)
def generate_department_analytics(self, department_id, period_days=30):
    """
    Generate comprehensive analytics for a department
    
    Args:
        department_id: Department ID
        period_days: Analysis period in days
    """
    try:
        from cases.models import Case
        from cases.medical_models import Department
        from datetime import timedelta
        
        department = Department.objects.get(id=department_id)
        start_date = timezone.now() - timedelta(days=period_days)
        
        # Get cases from this department
        cases = Case.objects.filter(
            Q(student__department=department) | Q(repository__department=department),
            created_at__gte=start_date
        )
        
        analytics = {
            'department': {
                'id': department.id,
                'name': department.name,
                'vietnamese_name': department.vietnamese_name
            },
            'period': {
                'days': period_days,
                'start_date': start_date.isoformat(),
                'end_date': timezone.now().isoformat()
            },
            'summary': {
                'total_cases': cases.count(),
                'by_status': list(cases.values('case_status').annotate(count=Count('id'))),
                'by_specialty': list(cases.values('specialty').annotate(count=Count('id')).order_by('-count')[:5]),
                'unique_students': cases.values('student').distinct().count()
            }
        }
        
        # Cache results
        cache_key = f"dept_analytics_{department_id}_{self.request.id}"
        cache.set(cache_key, analytics, 7200)  # 2 hours
        
        logger.info(f"Generated analytics for department {department.name}: {analytics['summary']['total_cases']} cases")
        
        return {
            'status': 'completed',
            'task_id': self.request.id,
            'cache_key': cache_key
        }
        
    except Exception as exc:
        logger.error(f"Error generating department analytics: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_bulk_notifications(self, notification_data_list):
    """
    Send multiple notifications in background
    
    Args:
        notification_data_list: List of notification dictionaries
    """
    try:
        from notifications.models import Notification
        
        notifications = []
        for data in notification_data_list:
            notifications.append(Notification(**data))
        
        created = Notification.objects.bulk_create(notifications)
        
        logger.info(f"Created {len(created)} bulk notifications")
        
        return {
            'status': 'completed',
            'count': len(created)
        }
        
    except Exception as exc:
        logger.error(f"Error sending bulk notifications: {exc}")
        raise self.retry(exc=exc, countdown=30)
