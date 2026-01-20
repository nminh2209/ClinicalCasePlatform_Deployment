from rest_framework import views, status, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
import uuid
import time
from celery.result import AsyncResult
from .ocr_service import ocr_service
from .tasks import process_ocr_task

class OCRExtractView(views.APIView):
    """
    Extract text from images/PDFs using OCR.
    
    Two-phase processing:
    - Phase 1 (sync): Text extraction + autofill (DocTR+VietOCR+SBERT, ~10s)
    - Phase 2 (async): Table/image extraction (PPStructure, ~50s, background)
    
    Parameters:
        file: The uploaded file
        mode: "text" (default) | "full" (queues table/image extraction)
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Get extraction mode: "text" (default) or "full" (includes tables/images)
        mode = request.data.get('mode', 'text')  # "text" | "full"
        print(f"[OCR Extract] Received mode='{mode}' from request")

        # 1. Validation
        if file_obj.size > 10 * 1024 * 1024: # 10MB
            return Response({"error": "File size exceeds 10MB limit"}, status=status.HTTP_400_BAD_REQUEST)

        allowed_types = ['image/jpeg', 'image/png', 'image/webp', 'application/pdf']
        if file_obj.content_type not in allowed_types:
            return Response({"error": "Unsupported file type"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Save temp file
        ext = os.path.splitext(file_obj.name)[1]
        temp_filename = f"ocr_temp_{uuid.uuid4()}{ext}"
        file_path = default_storage.save(f"tmp/{temp_filename}", ContentFile(file_obj.read()))
        abs_file_path = os.path.join(settings.MEDIA_ROOT, file_path)

        # 3. Decision: Fully async for very large files
        is_very_large = file_obj.size > 5 * 1024 * 1024  # > 5MB -> fully async
        
        if is_very_large:
            # Fully async path for very large files
            task = process_ocr_task.delay(abs_file_path, file_obj.content_type)
            return Response({
                "job_id": task.id,
                "status": "queued",
                "message": "File is large, processing in background"
            }, status=status.HTTP_202_ACCEPTED)
        
        # 4. Phase 1: Sync text extraction (always runs)
        try:
            start = time.time()
            result = ocr_service.process(abs_file_path)
            text_elapsed = time.time() - start
            
            response_data = {
                **result,
                "metadata": {
                    **result.get("metadata", {}),
                    "text_extraction_ms": int(text_elapsed * 1000)
                }
            }
            
            # 5. Phase 2: Async table/image extraction (if mode="full")
            # Frontend decides whether to use mode=full (with Celery) or mode=text (skip)
            # Hints are included in response for frontend to make informed decisions
            if mode == 'full':
                try:
                    from .tasks import extract_tables_images_task
                    # Don't delete temp file - task needs it
                    job = extract_tables_images_task.delay(abs_file_path, file_obj.content_type)
                    response_data["table_job_id"] = job.id
                    response_data["table_job_status"] = "queued"
                    print(f"[OCR] Celery task queued for table/image extraction")
                except Exception as celery_error:
                    # Celery broker not available - skip table/image extraction
                    print(f"CRITICAL CELERY ERROR: {celery_error}")
                    import logging
                    logging.warning(f"Celery task failed: {celery_error}")
                    response_data["table_job_status"] = "unavailable"
                    response_data["table_job_error"] = "Background task service unavailable."
                    # Cleanup temp file since task won't run
                    if os.path.exists(abs_file_path):
                        os.remove(abs_file_path)
            else:
                # Text-only mode - no Celery, cleanup temp file
                response_data["table_job_status"] = "not_requested"
                if os.path.exists(abs_file_path):
                    os.remove(abs_file_path)

            return Response(response_data)
            
        except Exception as e:
            import traceback
            print(f"CRITICAL ERROR in OCR View: {e}")
            traceback.print_exc()

            # Queue table extraction
            # Cleanup on error
            if os.path.exists(abs_file_path):
                os.remove(abs_file_path)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OCRJobStatusView(views.APIView):
    """
    Check status of async OCR job
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, job_id):
        result = AsyncResult(job_id)
        
        if result.state == 'PENDING':
            return Response({"status": "queued"})
        elif result.state == 'STARTED':
            return Response({"status": "running"})
        elif result.state == 'SUCCESS':
            # Include status field so frontend knows polling is complete
            task_result = result.result or {}
            return Response({
                "status": "done",
                "tables": task_result.get("tables", []),
                "images": task_result.get("images", []),
            })
        elif result.state == 'FAILURE':
            return Response({"status": "failed", "error": str(result.result)})
            
        return Response({"status": result.state})


class OCRAutofillView(views.APIView):
    """
    Auto-fill case template fields from OCR output using Vietnamese SBERT
    semantic matching.
    
    POST /api/ocr/autofill
    Request: { "text": "..." } or { "ocr_result": {...} }
    Response: { "structured_data": {...}, "matches": {...} }
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        from .heading_matcher import autofill_from_ocr
        
        # Accept either raw text or full OCR result
        ocr_text = request.data.get('text')
        if not ocr_text:
            ocr_result = request.data.get('ocr_result', {})
            ocr_text = ocr_result.get('text', '')
        
        if not ocr_text:
            return Response(
                {"error": "No text provided. Send 'text' or 'ocr_result.text'"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get optional confidence threshold
        confidence = float(request.data.get('confidence_threshold', 0.6))
        
        try:
            # Run semantic matching
            start = time.time()
            structured_data = autofill_from_ocr(ocr_text, confidence)
            elapsed_ms = int((time.time() - start) * 1000)
            
            # Flatten to simple key-value for frontend
            flat_data = {}
            for key, value in structured_data.items():
                if isinstance(value, dict) and 'value' in value:
                    # Top-level field
                    flat_data[key] = value['value']
                elif isinstance(value, dict):
                    # Nested object (e.g., clinical_history)
                    flat_data[key] = {}
                    for child_key, child_value in value.items():
                        if isinstance(child_value, dict) and 'value' in child_value:
                            flat_data[key][child_key] = child_value['value']
            
            return Response({
                "structured": flat_data,
                "matches": structured_data,
                "metadata": {
                    "fields_matched": len(structured_data),
                    "elapsed_ms": elapsed_ms
                }
            })
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {"error": f"Auto-fill failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

