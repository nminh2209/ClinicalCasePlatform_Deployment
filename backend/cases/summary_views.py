"""
Case Summarization Views - Aggregate and export multiple cases
"""
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Q, Avg, F
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from datetime import datetime, timedelta
import logging

from cases.models import Case
from cases.medical_models import Department
from cases.serializers import CaseDetailSerializer

logger = logging.getLogger(__name__)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def case_summary_statistics(request):
    """
    Get aggregated statistics for cases with filtering
    
    Query Parameters:
    - department: Filter by department ID
    - date_from: Start date (YYYY-MM-DD)
    - date_to: End date (YYYY-MM-DD)
    - status: Filter by case status
    - specialty: Filter by specialty
    - student: Filter by student ID
    
    Returns comprehensive statistics about cases
    """
    try:
        user = request.user
        
        # Build base queryset based on user permissions
        queryset = Case.objects.all()
        
        # Role-based filtering
        try:
            if user.is_student:
                queryset = queryset.filter(student=user)
            elif user.is_instructor and hasattr(user, 'department') and user.department:
                # Instructors see their department's cases
                queryset = queryset.filter(
                    Q(student__department=user.department) |
                    Q(repository__department=user.department) |
                    Q(permissions__user=user, permissions__is_active=True)
                ).distinct()
        except AttributeError:
            # If user doesn't have role properties, show all (admin)
            pass
        
        # Apply filters
        department_id = request.query_params.get('department')
        if department_id:
            queryset = queryset.filter(
                Q(student__department_id=department_id) |
                Q(repository__department_id=department_id)
            )
        
        date_from = request.query_params.get('date_from')
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        
        date_to = request.query_params.get('date_to')
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)
        
        case_status = request.query_params.get('status')
        if case_status:
            queryset = queryset.filter(case_status=case_status)
        
        specialty = request.query_params.get('specialty')
        if specialty:
            queryset = queryset.filter(specialty=specialty)
        
        student_id = request.query_params.get('student')
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        # Calculate statistics
        total_cases = queryset.count()
        
        # Status distribution
        status_stats = queryset.values('case_status').annotate(
            count=Count('id')
        ).order_by('case_status')
        
        # Specialty distribution
        specialty_stats = queryset.values('specialty').annotate(
            count=Count('id')
        ).order_by('-count')[:10]  # Top 10 specialties
        
        # Priority distribution
        priority_stats = queryset.values('priority_level').annotate(
            count=Count('id')
        ).order_by('priority_level')
        
        # Complexity distribution
        complexity_stats = queryset.values('complexity_level').annotate(
            count=Count('id')
        ).order_by('complexity_level')
        
        # Department distribution
        department_stats = queryset.values(
            'student__department__name',
            'student__department__vietnamese_name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Time-based statistics (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_cases = queryset.filter(created_at__gte=thirty_days_ago)
        
        # Cases per day for the last 30 days
        daily_stats = recent_cases.extra(
            select={'day': 'DATE(created_at)'}
        ).values('day').annotate(
            count=Count('id')
        ).order_by('day')
        
        # Average grade if grades exist
        avg_grades = None
        if queryset.filter(grade__isnull=False).exists():
            from grades.models import Grade
            grades_queryset = Grade.objects.filter(case__in=queryset)
            # Only aggregate the overall score (grading_criteria is JSONB - can't use Avg directly)
            avg_grades = grades_queryset.aggregate(
                avg_score=Avg('score'),
                total_graded=Count('id')
            )
    
        return Response({
            'summary': {
                'total_cases': total_cases,
                'date_range': {
                    'from': date_from,
                    'to': date_to
                },
                'filters_applied': {
                    'department': department_id,
                    'status': case_status,
                    'specialty': specialty,
                    'student': student_id
                }
            },
            'distributions': {
                'by_status': list(status_stats),
                'by_specialty': list(specialty_stats),
                'by_priority': list(priority_stats),
                'by_complexity': list(complexity_stats),
                'by_department': list(department_stats)
            },
            'trends': {
                'last_30_days': {
                    'total': recent_cases.count(),
                    'daily': list(daily_stats)
                }
            },
            'performance': avg_grades
        })
    
    except Exception as e:
        logger.error(f"Error in case_summary_statistics: {str(e)}", exc_info=True)
        return Response({
            'error': str(e),
            'summary': {'total_cases': 0},
            'distributions': {},
            'trends': {},
            'performance': None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def case_summary_list(request):
    """
    Get aggregated list of cases with summaries and key information
    
    Supports all filtering options and returns condensed case information
    suitable for summarization documents
    """
    user = request.user
    
    # Check cache first
    cache_key = f"case_summary_list_{user.id}_{hash(str(request.query_params))}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return Response(cached_data)
    
    # Build queryset with optimizations
    queryset = Case.objects.select_related(
        'student', 'student__department', 'repository', 'template'
    ).prefetch_related('medical_attachments', 'grade')
    
    # Role-based filtering
    try:
        if user.is_student:
            queryset = queryset.filter(student=user)
        elif user.is_instructor and hasattr(user, 'department') and user.department:
            queryset = queryset.filter(
                Q(student__department=user.department) |
                Q(repository__department=user.department) |
                Q(permissions__user=user, permissions__is_active=True)
            ).distinct()
    except AttributeError:
        # If user doesn't have role properties, show all (admin)
        pass
    
    # Apply filters (reuse logic from above)
    department_id = request.query_params.get('department')
    if department_id:
        queryset = queryset.filter(
            Q(student__department_id=department_id) |
            Q(repository__department_id=department_id)
        )
    
    date_from = request.query_params.get('date_from')
    if date_from:
        queryset = queryset.filter(created_at__gte=date_from)
    
    date_to = request.query_params.get('date_to')
    if date_to:
        queryset = queryset.filter(created_at__lte=date_to)
    
    case_status = request.query_params.get('status')
    if case_status:
        queryset = queryset.filter(case_status=case_status)
    
    specialty = request.query_params.get('specialty')
    if specialty:
        queryset = queryset.filter(specialty=specialty)
    
    # Limit results
    limit = min(int(request.query_params.get('limit', 100)), 500)  # Max 500
    queryset = queryset[:limit]
    
    # Serialize data
    serializer = CaseDetailSerializer(queryset, many=True)
    
    response_data = {
        'count': queryset.count(),
        'cases': serializer.data
    }
    
    # Cache for 5 minutes
    from django.conf import settings
    cache.set(cache_key, response_data, settings.CACHE_TTL.get('CASE_SUMMARY', 300))
    
    return Response(response_data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def export_case_summary(request):
    """
    Generate and export case summary document
    
    Request Body:
    {
        "format": "json|csv|excel",  # pdf/word via Celery task
        "filters": {
            "department": <id>,
            "date_from": "YYYY-MM-DD",
            "date_to": "YYYY-MM-DD",
            "status": "<status>",
            "specialty": "<specialty>"
        },
        "include_statistics": true,
        "include_details": false
    }
    """
    export_format = request.data.get('format', 'json')
    filters = request.data.get('filters', {})
    include_statistics = request.data.get('include_statistics', True)
    include_details = request.data.get('include_details', False)
    
    user = request.user
    
    # Build queryset
    queryset = Case.objects.select_related(
        'student', 'student__department'
    )
    
    # Apply role-based filtering
    try:
        if user.is_student:
            queryset = queryset.filter(student=user)
        elif user.is_instructor and hasattr(user, 'department') and user.department:
            queryset = queryset.filter(
                Q(student__department=user.department) |
                Q(repository__department=user.department)
            ).distinct()
    except AttributeError:
        # If user doesn't have role properties, show all (admin)
        pass
    
    # Apply filters
    for key, value in filters.items():
        if value:
            if key == 'department':
                queryset = queryset.filter(
                    Q(student__department_id=value) |
                    Q(repository__department_id=value)
                )
            elif key in ['date_from', 'date_to', 'status', 'specialty']:
                filter_map = {
                    'date_from': 'created_at__gte',
                    'date_to': 'created_at__lte',
                    'status': 'case_status',
                    'specialty': 'specialty'
                }
                queryset = queryset.filter(**{filter_map[key]: value})
    
    # Generate export based on format
    if export_format == 'json':
        serializer = CaseDetailSerializer(queryset, many=True) if include_details else None
        
        response_data = {
            'export_date': timezone.now().isoformat(),
            'exported_by': {
                'id': user.id,
                'name': user.get_full_name(),
                'email': user.email
            },
            'filters': filters,
            'count': queryset.count()
        }
        
        if include_statistics:
            # Reuse statistics endpoint logic
            stats_request = type('obj', (object,), {
                'user': user,
                'query_params': filters
            })()
            # Add statistics here (simplified for now)
            response_data['statistics'] = {
                'total_cases': queryset.count(),
                'by_status': list(queryset.values('case_status').annotate(count=Count('id')))
            }
        
        if include_details:
            response_data['cases'] = serializer.data
        
        return Response(response_data)
    
    elif export_format == 'csv':
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Write headers
        headers = ['ID', 'Title', 'Student', 'Department', 'Specialty', 'Status', 'Created At']
        writer.writerow(headers)
        
        # Write data
        for case in queryset:
            writer.writerow([
                case.id,
                case.title,
                case.student.get_full_name(),
                case.student.department.name if case.student.department else '',
                case.specialty or '',
                case.case_status,
                case.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="case_summary_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        logger.info(f"User {user.id} exported {queryset.count()} cases as CSV")
        
        return response
    
    else:
        return Response(
            {'error': f'Unsupported export format: {export_format}'},
            status=status.HTTP_400_BAD_REQUEST
        )
