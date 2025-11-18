from django.urls import path
from .views import CaseTemplateListCreateView, CaseTemplateDetailView

urlpatterns = [
    # Case Template CRUD
    path("", CaseTemplateListCreateView.as_view(), name="template-list-create"),
    path("<int:pk>/", CaseTemplateDetailView.as_view(), name="template-detail"),
]
