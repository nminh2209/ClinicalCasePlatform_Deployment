# comments/urls.py

from django.urls import path

from .views import CommentDetailView, CommentListCreateView

urlpatterns = [
    # Comment CRUD
    path("", CommentListCreateView.as_view(), name="comment-list-create"),
    path("<int:pk>/", CommentDetailView.as_view(), name="comment-detail"),
]
