"""
ASR API Views
"""
import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from .service import asr_service

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def asr_status(request):
    """
    Get ASR service status and model information
    
    GET /api/asr/status/
    """
    try:
        info = asr_service.get_model_info()
        return Response(info, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error getting ASR status: {str(e)}")
        return Response(
            {"error": "Failed to get ASR status"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transcribe_audio(request):
    """
    Transcribe audio file to text
    
    POST /api/asr/transcribe/
    
    Request body (multipart/form-data):
        - audio: Audio file (required)
        - language: Language code (optional, default: "vi")
        - return_timestamps: Boolean (optional, default: false)
    
    Response:
        {
            "text": "transcribed text",
            "language": "vi",
            "success": true,
            "error": null,
            "chunks": [...] (if return_timestamps=true)
        }
    """
    try:
        # Check if ASR is available
        if not asr_service.is_available():
            return Response(
                {
                    "text": "",
                    "success": False,
                    "error": "ASR service is not available. Please ensure the model is installed."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Validate audio file
        if 'audio' not in request.FILES:
            return Response(
                {"error": "No audio file provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        audio_file = request.FILES['audio']
        language = request.data.get('language', 'vi')
        return_timestamps = request.data.get('return_timestamps', 'false').lower() == 'true'
        
        # Validate file size (max 50MB)
        max_size = 50 * 1024 * 1024  # 50MB
        if audio_file.size > max_size:
            return Response(
                {"error": "Audio file too large. Maximum size is 50MB."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Process audio file
        logger.info(f"Transcribing audio file: {audio_file.name} ({audio_file.size} bytes)")
        
        # Save to temporary location if needed
        if isinstance(audio_file, InMemoryUploadedFile):
            # Read file content for in-memory files
            audio_bytes = audio_file.read()
            result = asr_service.transcribe_bytes(
                audio_bytes,
                language=language,
                return_timestamps=return_timestamps
            )
        else:
            # Use file path for temporary uploaded files
            result = asr_service.transcribe(
                audio_file.temporary_file_path(),
                language=language,
                return_timestamps=return_timestamps
            )
        
        # Return result
        if result['success']:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}", exc_info=True)
        return Response(
            {
                "text": "",
                "success": False,
                "error": f"Transcription failed: {str(e)}"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def supported_languages(request):
    """
    Get list of supported languages
    
    GET /api/asr/languages/
    """
    languages = [
        {
            "code": "vi",
            "name": "Vietnamese",
            "native_name": "Tiếng Việt",
            "default": True
        },
        {
            "code": "en",
            "name": "English",
            "native_name": "English",
            "default": False
        }
    ]
    
    return Response({"languages": languages}, status=status.HTTP_200_OK)
