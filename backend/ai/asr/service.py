"""
ASR Service - Automatic Speech Recognition
Supports Vietnamese using PhoWhisper model from VinAI Research
"""
import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Union, TYPE_CHECKING

logger = logging.getLogger(__name__)

# Check if ASR is enabled via environment variable
ASR_ENABLED = os.environ.get('ASR_ENABLED', 'true').lower() in ('true', '1', 'yes')
if not ASR_ENABLED:
    logger.info("ASR service disabled via ASR_ENABLED=false")

# Try to import ML libraries - they're optional
try:
    import torch
    import numpy as np
    from transformers import pipeline
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    DEPENDENCIES_AVAILABLE = False
    torch = None  # type: ignore
    np = None  # type: ignore
    pipeline = None  # type: ignore
    logger.warning(f"ASR dependencies not available: {str(e)}")
    logger.warning("Install with: pip install torch transformers accelerate soundfile librosa")


class ASRService:
    """
    ASR Service using VinAI's PhoWhisper model for Vietnamese speech recognition
    Model: vinai/PhoWhisper-medium
    
    Uses lazy loading - model only loads when first transcription is requested.
    """
    
    _instance = None
    _model = None
    _device = None
    _initialized = False  # Track if init has been attempted
    
    def __new__(cls):
        """Singleton pattern to load model only once"""
        if cls._instance is None:
            cls._instance = super(ASRService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize ASR service - does NOT load model yet (lazy loading)"""
        # Don't do anything here - model loads on first use
        pass
    
    def _ensure_model_loaded(self):
        """Lazy-load the model only when first needed"""
        if self._initialized:
            return
        self._initialized = True
        self._initialize_model()
    
    def _get_cache_dir(self) -> str:
        """Get the local cache directory for models"""
        current_dir = Path(__file__).parent
        cache_dir = current_dir / "phowhisper"
        cache_dir.mkdir(exist_ok=True)
        return str(cache_dir)
    
    def _initialize_model(self):
        """Initialize PhoWhisper model"""
        # Check if ASR is disabled
        if not ASR_ENABLED:
            logger.info("ASR disabled - skipping model initialization")
            self._model = None
            return
        
        # Check if dependencies are available
        if not DEPENDENCIES_AVAILABLE or torch is None or pipeline is None:
            logger.warning("ASR dependencies not installed. ASR service will not be available.")
            logger.info("To enable ASR: pip install torch transformers accelerate soundfile librosa")
            self._model = None
            return
        
        try:
            # Detect device (CPU/GPU)
            self._device = "cuda" if torch.cuda.is_available() else "cpu"  # type: ignore
            logger.info(f"Initializing ASR model on device: {self._device}")
            logger.info("Downloading PhoWhisper model if not cached (this may take a few minutes)...")
            
            # Load PhoWhisper model
            # Model: vinai/PhoWhisper-medium (~1.5GB)
            # Will be downloaded to: backend/ai/asr/phowhisper/
            # Optimized for Vietnamese language
            
            # Set cache directory via environment variable
            import os
            cache_dir = self._get_cache_dir()
            os.environ['TRANSFORMERS_CACHE'] = cache_dir
            os.environ['HF_HOME'] = cache_dir
            
            self._model = pipeline(  # type: ignore
                "automatic-speech-recognition",
                model="vinai/PhoWhisper-medium",
                device=0 if self._device == "cuda" else -1,
                chunk_length_s=30,  # Process audio in 30-second chunks
                stride_length_s=5,  # 5-second overlap between chunks
            )
            
            logger.info("ASR model initialized successfully")
            logger.info(f"Model device: {self._device}")
            
        except Exception as e:
            logger.error(f"Failed to initialize ASR model: {str(e)}")
            logger.error("Make sure you have internet connection for first-time model download")
            logger.warning("ASR service will not be available")
            self._model = None
    
    def is_available(self) -> bool:
        """Check if ASR service is available (triggers lazy load)"""
        self._ensure_model_loaded()
        return self._model is not None
    
    def transcribe(
        self,
        audio_file_path: str,
        language: str = "vi",
        return_timestamps: bool = False
    ) -> Dict[str, Any]:
        """
        Transcribe audio file to text
        
        Args:
            audio_file_path: Path to audio file (wav, mp3, flac, etc.)
            language: Language code (default: "vi" for Vietnamese)
            return_timestamps: Whether to return word-level timestamps
            
        Returns:
            Dict with transcription results:
            {
                "text": str,
                "language": str,
                "success": bool,
                "error": Optional[str],
                "chunks": Optional[List] (if return_timestamps=True)
            }
        """
        self._ensure_model_loaded()  # Lazy load
        
        if not self._model:
            return {
                "text": "",
                "language": language,
                "success": False,
                "error": "ASR service not available. Model failed to initialize."
            }
        
        if not os.path.exists(audio_file_path):
            return {
                "text": "",
                "language": language,
                "success": False,
                "error": f"Audio file not found: {audio_file_path}"
            }
        
        try:
            logger.info(f"Transcribing audio file: {audio_file_path}")
            
            # Configure transcription parameters
            generate_kwargs = {
                "language": language,
                "task": "transcribe",
            }
            
            # Transcribe audio
            result = self._model(  # type: ignore
                audio_file_path,
                generate_kwargs=generate_kwargs,
                return_timestamps=return_timestamps
            )
            
            # Extract text - handle both dict and list responses
            if isinstance(result, dict):
                text = result.get("text", "")
            elif isinstance(result, list) and len(result) > 0:
                text = result[0].get("text", "") if isinstance(result[0], dict) else str(result)
            else:
                text = str(result)
            
            response: Dict[str, Any] = {
                "text": text.strip(),
                "language": language,
                "success": True,
                "error": None
            }
            
            # Add timestamps if requested
            if return_timestamps:
                if isinstance(result, dict) and "chunks" in result:
                    response["chunks"] = result["chunks"]  # type: ignore
                elif isinstance(result, list):
                    response["chunks"] = result
            
            logger.info(f"Transcription successful: {len(text)} characters")
            return response
            
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}", exc_info=True)
            return {
                "text": "",
                "language": language,
                "success": False,
                "error": f"Transcription error: {str(e)}"
            }
    
    def transcribe_bytes(
        self,
        audio_bytes: bytes,
        language: str = "vi",
        return_timestamps: bool = False
    ) -> Dict[str, Any]:
        """
        Transcribe audio from bytes
        
        Args:
            audio_bytes: Audio data as bytes
            language: Language code (default: "vi" for Vietnamese)
            return_timestamps: Whether to return word-level timestamps
            
        Returns:
            Dict with transcription results (same as transcribe)
        """
        self._ensure_model_loaded()  # Lazy load
        
        if not self._model:
            return {
                "text": "",
                "language": language,
                "success": False,
                "error": "ASR service not available"
            }
        
        try:
            # Save bytes to temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(audio_bytes)
                tmp_path = tmp_file.name
            
            # Transcribe
            result = self.transcribe(
                tmp_path,
                language=language,
                return_timestamps=return_timestamps
            )
            
            # Clean up
            try:
                os.unlink(tmp_path)
            except:
                pass
            
            return result
            
        except Exception as e:
            logger.error(f"Transcription from bytes failed: {str(e)}")
            return {
                "text": "",
                "language": language,
                "success": False,
                "error": f"Transcription error: {str(e)}"
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        return {
            "available": self._model is not None,
            "model_loaded": self._initialized,
            "model_name": "vinai/PhoWhisper-medium" if self._model else None,
            "device": self._device if self._model else None,
            "language_support": ["vi", "en"],
            "description": "Vietnamese-optimized speech recognition using VinAI PhoWhisper"
        }


# Global instance - but model won't load until first use!
asr_service = ASRService()

