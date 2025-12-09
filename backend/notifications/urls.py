from django.urls import path
from .views import (
    NotificationListView,
    NotificationDetailView,
    mark_notification_as_read,
    mark_all_as_read,
    unread_count,
    delete_notification,
)

urlpatterns = [
    path("", NotificationListView.as_view(), name="notification-list"),
    path("<int:pk>/", NotificationDetailView.as_view(), name="notification-detail"),
    path(
        "<int:pk>/mark-read/",
        mark_notification_as_read,
        name="notification-mark-read",
    ),
    path("mark-all-read/", mark_all_as_read, name="notification-mark-all-read"),
    path("unread-count/", unread_count, name="notification-unread-count"),
    path("<int:pk>/delete/", delete_notification, name="notification-delete"),
]
