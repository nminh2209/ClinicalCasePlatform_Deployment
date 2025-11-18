from django.urls import path
from .views import FeedbackListCreateView, FeedbackDetailView

urlpatterns = [
    # Feedback CRUD
    path("", FeedbackListCreateView.as_view(), name="feedback-list-create"),
    path("<int:pk>/", FeedbackDetailView.as_view(), name="feedback-detail"),
]
