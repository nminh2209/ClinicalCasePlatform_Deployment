from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """
    List all notifications for the current user
    """

    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).select_related(
            "related_case", "related_comment", "related_grade", "related_feedback"
        )


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a notification
    """

    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_as_read(request, pk):
    """
    Mark a specific notification as read
    """
    try:
        notification = Notification.objects.get(pk=pk, recipient=request.user)
        notification.mark_as_read()
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)
    except Notification.DoesNotExist:
        return Response(
            {"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def mark_all_as_read(request):
    """
    Mark all notifications as read for the current user
    """
    updated = Notification.objects.filter(
        recipient=request.user, is_read=False
    ).update(is_read=True, read_at=timezone.now())

    return Response({"marked_read": updated})


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def unread_count(request):
    """
    Get count of unread notifications for the current user
    """
    count = Notification.objects.filter(
        recipient=request.user, is_read=False
    ).count()

    return Response({"unread_count": count})


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_notification(request, pk):
    """
    Delete a specific notification
    """
    try:
        notification = Notification.objects.get(pk=pk, recipient=request.user)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Notification.DoesNotExist:
        return Response(
            {"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND
        )
