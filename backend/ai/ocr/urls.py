from django.urls import path
from .views import OCRExtractView, OCRJobStatusView, OCRAutofillView

urlpatterns = [
    path('extract/', OCRExtractView.as_view(), name='ocr-extract'),
    path('jobs/<str:job_id>/', OCRJobStatusView.as_view(), name='ocr-job-status'),
    path('autofill/', OCRAutofillView.as_view(), name='ocr-autofill'),
]
