"""
ASR API URLs
"""
from django.urls import path
from . import views

app_name = 'asr'

urlpatterns = [
    path('status/', views.asr_status, name='asr-status'),
    path('transcribe/', views.transcribe_audio, name='transcribe'),
    path('languages/', views.supported_languages, name='languages'),
]
