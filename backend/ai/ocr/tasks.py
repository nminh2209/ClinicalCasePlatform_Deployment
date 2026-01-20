from celery import shared_task
from .ocr_service import ocr_service
import os

@shared_task(bind=True)
def process_ocr_task(self, file_path, mime_type):
    """
    Async Celery task for full OCR processing (text extraction).
    Used for very large files.
    """
    try:
        result = ocr_service.process(file_path, mime_type)
        
        # Clean up temp file if needed
        if os.path.exists(file_path) and '/tmp/' in file_path:
            os.remove(file_path)
            
        return {
            "status": "done",
            **result
        }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }


@shared_task(
    bind=True,
    max_retries=3,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
)
def extract_tables_images_task(self, file_path, mime_type):
    """
    Async Celery task for table and image extraction using PPStructure.
    This is Phase 2 of the two-phase OCR flow.
    
    Takes ~50s/page using PPStructure for layout analysis.
    
    Retry Policy:
        - max_retries=3: Try up to 3 times on failure
        - retry_backoff=True: Exponential delay (60s → 120s → 240s)
        - retry_backoff_max=600: Max wait 10 minutes
    """
    import logging
    logger = logging.getLogger(__name__)
    
    print(f"[CELERY TASK] Starting extract_tables_images_task")
    print(f"[CELERY TASK] File path: {file_path}")
    print(f"[CELERY TASK] MIME type: {mime_type}")
    print(f"[CELERY TASK] File exists: {os.path.exists(file_path)}")
    
    try:
        tables = []
        images = []
        
        # Extract tables using PPStructure
        print("[CELERY TASK] Extracting tables...")
        tables = ocr_service.extract_tables(file_path, mime_type)
        print(f"[CELERY TASK] Tables extracted: {len(tables)}")
        
        # Extract images (crop figure regions)
        print("[CELERY TASK] Extracting images...")
        images = ocr_service.extract_images(file_path, mime_type)
        print(f"[CELERY TASK] Images extracted: {len(images)}")
        
        # Clean up temp file
        if os.path.exists(file_path) and '/tmp/' in file_path:
            os.remove(file_path)
            print(f"[CELERY TASK] Cleaned up temp file: {file_path}")
            
        print("[CELERY TASK] Task completed successfully!")
        return {
            "status": "done",
            "tables": tables,
            "images": images
        }
    except Exception as e:
        print(f"[CELERY TASK] ERROR: {e}")
        import traceback
        traceback.print_exc()
        
        # Cleanup on error
        if os.path.exists(file_path) and '/tmp/' in file_path:
            try:
                os.remove(file_path)
            except:
                pass
        return {
            "status": "failed",
            "error": str(e),
            "tables": [],
            "images": []
        }