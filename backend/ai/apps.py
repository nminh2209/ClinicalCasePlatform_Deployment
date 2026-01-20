from django.apps import AppConfig
import os


class AiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai'

    def ready(self):
        """Pre-load OCR models when Django starts."""
        # Only run in the main process (not in management commands or migrations)
        run_main = os.environ.get('RUN_MAIN')
        if run_main != 'true':
            return
        
        try:
            from ai.ocr.ocr_service import prewarm_models
            prewarm_models()
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"OCR pre-warming skipped: {e}")
