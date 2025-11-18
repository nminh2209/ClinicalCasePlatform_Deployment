"""
Public Feed Views - Social Media Style Case Sharing
Using existing Case and Comment models (no new tables)
"""

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.db.models import Count, Q, Prefetch
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import Case
from comments.models import Comment
from .serializers import PublicFeedSerializer, CaseDetailSerializer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from accounts.models import User


class PublicFeedListView(generics.ListAPIView):
    """
    GET /api/cases/public-feed/
    
    List all cases published to public feed
    - Filters: department, specialty, is_featured
    - Sorted by: published_to_feed_at (newest first)
    - Includes: reaction counts, comment counts
    
    Query Parameters:
    - filter: 'all', 'department', 'featured'
    - specialty: filter by specialty
    - department_id: filter by specific department
    """
    serializer_class = PublicFeedSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user: User = self.request.user
        queryset = Case.objects.filter(
            is_published_to_feed=True,
            case_status=Case.StatusChoices.APPROVED
        ).select_related(
            'student',
            'student__department',
            'published_by',
            'repository'
        ).annotate(
            comments_count=Count('comments', filter=Q(comments__is_reaction=False)),
        ).order_by('-published_to_feed_at')
        
        # Filter by user's department or all
        filter_type = self.request.query_params.get('filter', 'department')
        
        if filter_type == 'department' and user.department:
            queryset = queryset.filter(
                Q(feed_visibility='department', student__department=user.department) |
                Q(feed_visibility='university')
            )
        elif filter_type == 'featured':
            queryset = queryset.filter(is_featured=True)
        # 'all' shows all university-wide + own department
        
        # Additional filters
        specialty = self.request.query_params.get('specialty')
        if specialty:
            queryset = queryset.filter(specialty=specialty)
        
        department_id = self.request.query_params.get('department_id')
        if department_id:
            queryset = queryset.filter(student__department_id=department_id)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = self.get_paginated_response(serializer.data)
            return response_data
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PublicFeedDetailView(generics.RetrieveAPIView):
    """
    GET /api/cases/public-feed/{id}/
    
    Get detailed view of a published case
    Includes full case data, reactions, and comments
    Increments view count
    """
    serializer_class = CaseDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Case.objects.filter(
            is_published_to_feed=True,
            case_status=Case.StatusChoices.APPROVED
        ).select_related(
            'student',
            'student__department',
            'published_by',
            'repository'
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Increment view count
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        
        serializer = self.get_serializer(instance)
        data = serializer.data
        
        # Add reaction summary
        data['reactions'] = instance.get_reaction_summary()
        
        # Get user's reaction if exists
        user_reaction = Comment.objects.filter(
            case=instance,
            author=request.user,
            is_reaction=True
        ).first()
        data['user_reaction'] = user_reaction.reaction_type if user_reaction else None
        
        return Response(data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def publish_to_feed(request, pk):
    """
    POST /api/cases/{id}/publish-to-feed/
    
    Publish an approved case to public feed (Instructor only)
    
    Body:
    {
        "feed_visibility": "department" | "university",
        "is_featured": false
    }
    """
    user: User = request.user
    
    if not user.is_instructor:
        raise PermissionDenied("Only instructors can publish cases to feed")
    
    case = get_object_or_404(Case, pk=pk)
    
    # Check if case can be published
    if not case.can_be_published():
        return Response(
            {"error": "Case must be approved and not already published"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Update case
    case.is_published_to_feed = True
    case.published_to_feed_at = timezone.now()
    case.published_by = user
    case.feed_visibility = request.data.get('feed_visibility', 'department')
    case.is_featured = request.data.get('is_featured', False)
    case.save()
    
    return Response({
        "message": "Case published to feed successfully",
        "case_id": case.id,
        "published_at": case.published_to_feed_at,
        "visibility": case.feed_visibility
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unpublish_from_feed(request, pk):
    """
    POST /api/cases/{id}/unpublish-from-feed/
    
    Remove case from public feed (Instructor only)
    """
    user: User = request.user
    
    if not user.is_instructor:
        raise PermissionDenied("Only instructors can unpublish cases from feed")
    
    case = get_object_or_404(Case, pk=pk)
    
    if not case.is_published_to_feed:
        return Response(
            {"error": "Case is not published to feed"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Update case
    case.is_published_to_feed = False
    case.is_featured = False
    case.save()
    
    return Response({
        "message": "Case unpublished from feed successfully",
        "case_id": case.id
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def react_to_case(request, pk):
    """
    POST /api/cases/{id}/react/
    
    Add or update user's reaction to a case
    
    Body:
    {
        "reaction_type": "like" | "love" | "insightful" | "learned"
    }
    """
    user: User = request.user
    case = get_object_or_404(Case, pk=pk, is_published_to_feed=True)
    
    reaction_type = request.data.get('reaction_type')
    if reaction_type not in ['like', 'love', 'insightful', 'learned']:
        return Response(
            {"error": "Invalid reaction type"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get or create reaction (using Comment model)
    reaction, created = Comment.objects.update_or_create(
        case=case,
        author=user,
        is_reaction=True,
        defaults={
            'reaction_type': reaction_type,
            'content': '',  # Empty content for reactions
        }
    )
    
    # Update case reaction count
    case.reaction_count = Comment.objects.filter(case=case, is_reaction=True).count()
    case.save(update_fields=['reaction_count'])
    
    action = 'added' if created else 'updated'
    
    return Response({
        "message": f"Reaction {action} successfully",
        "reaction_type": reaction_type,
        "total_reactions": case.reaction_count
    })


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_reaction(request, pk):
    """
    DELETE /api/cases/{id}/react/
    
    Remove user's reaction from a case
    """
    user: User = request.user
    case = get_object_or_404(Case, pk=pk, is_published_to_feed=True)
    
    # Delete reaction
    deleted_count, _ = Comment.objects.filter(
        case=case,
        author=user,
        is_reaction=True
    ).delete()
    
    if deleted_count == 0:
        return Response(
            {"error": "No reaction found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Update case reaction count
    case.reaction_count = Comment.objects.filter(case=case, is_reaction=True).count()
    case.save(update_fields=['reaction_count'])
    
    return Response({
        "message": "Reaction removed successfully",
        "total_reactions": case.reaction_count
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_case_reactions(request, pk):
    """
    GET /api/cases/{id}/reactions/
    
    Get detailed reaction summary for a case
    
    Returns:
    {
        "total": 45,
        "breakdown": {
            "like": 20,
            "love": 15,
            "insightful": 8,
            "learned": 2
        },
        "user_reaction": "like",
        "recent_reactions": [...]
    }
    """
    case = get_object_or_404(Case, pk=pk, is_published_to_feed=True)
    user: User = request.user
    
    # Get reaction summary
    summary = case.get_reaction_summary()
    
    # Get user's reaction
    user_reaction = Comment.objects.filter(
        case=case,
        author=user,
        is_reaction=True
    ).first()
    
    summary['user_reaction'] = user_reaction.reaction_type if user_reaction else None
    
    # Get recent reactions with user info
    recent_reactions = Comment.objects.filter(
        case=case,
        is_reaction=True
    ).select_related('author').order_by('-created_at')[:10]
    
    summary['recent_reactions'] = [{
        'user': r.author.get_full_name(),
        'reaction_type': r.reaction_type,
        'created_at': r.created_at
    } for r in recent_reactions]
    
    return Response(summary)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def feed_statistics(request):
    """
    GET /api/cases/feed-statistics/
    
    Get public feed statistics
    - Total published cases
    - Most reacted cases
    - Featured cases
    - Department breakdown
    """
    user: User = request.user
    
    # Base queryset
    queryset = Case.objects.filter(is_published_to_feed=True)
    
    # Filter by department if requested
    if user.department:
        department_cases = queryset.filter(student__department=user.department)
    else:
        department_cases = queryset.none()
    
    stats = {
        'total_published': queryset.count(),
        'department_published': department_cases.count(),
        'featured_count': queryset.filter(is_featured=True).count(),
        'total_reactions': sum(c.reaction_count for c in queryset),
        'most_reacted': queryset.order_by('-reaction_count')[:5].values(
            'id', 'title', 'reaction_count', 'specialty'
        ),
        'most_viewed': queryset.order_by('-view_count')[:5].values(
            'id', 'title', 'view_count', 'specialty'
        ),
        'recent_featured': queryset.filter(is_featured=True).order_by(
            '-published_to_feed_at'
        )[:3].values('id', 'title', 'specialty', 'published_to_feed_at'),
    }
    
    return Response(stats)
