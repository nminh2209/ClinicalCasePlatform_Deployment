"""
Test script for ASR service
Run this to verify PhoWhisper model is working correctly

Usage:
  cd backend
  python ai/asr/test_asr_service.py
  
  Or from ai/asr directory:
  python test_asr_service.py
"""
import os
import sys
import django

# Add parent directories to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(os.path.dirname(script_dir))
sys.path.insert(0, backend_dir)

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinical_case_platform.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Failed to setup Django: {e}")
    print("\nMake sure you're running from backend directory:")
    print("  cd backend")
    print("  python ai/asr/test_asr_service.py")
    sys.exit(1)

from ai.asr.service import asr_service, DEPENDENCIES_AVAILABLE


def test_asr_service():
    """Test ASR service initialization and info"""
    print("=" * 60)
    print("ASR Service Test")
    print("=" * 60)
    print()
    
    # Check dependencies first
    if not DEPENDENCIES_AVAILABLE:
        print("❌ ASR dependencies not installed")
        print()
        print("ASR service requires additional packages:")
        print("  - torch (PyTorch)")
        print("  - transformers (Hugging Face)")
        print("  - soundfile (audio processing)")
        print("  - librosa (audio processing)")
        print()
        print("To install ASR dependencies:")
        print("  1. Run: python ai/asr/install_asr.py")
        print("  2. Or manually: pip install torch transformers soundfile librosa")
        print()
        print("Note: The VoiceToText component will still work using")
        print("      Web Speech API in Chrome/Edge/Safari browsers.")
        print()
        print("=" * 60)
        return
    
    # Get service info
    info = asr_service.get_model_info()
    
    print("Service Status:")
    print(f"  Available: {'✅ YES' if info['available'] else '❌ NO'}")
    
    if info['available']:
        print(f"  Model: {info['model_name']}")
        print(f"  Device: {info['device']}")
        print(f"  Languages: {', '.join(info['language_support'])}")
        print(f"  Description: {info['description']}")
        print()
        print("✅ ASR service is ready!")
        print()
        print("Next steps:")
        print("  1. Start Django server: python manage.py runserver")
        print("  2. Test endpoint: curl http://localhost:8000/api/asr/status/")
        print("  3. Use VoiceToText component in frontend")
    else:
        print()
        print("❌ ASR service is not available")
        print()
        print("To enable ASR service:")
        print("  1. Install dependencies:")
        print("     python ai/asr/install_asr.py")
        print()
        print("  2. Or manually:")
        print("     pip install torch transformers accelerate soundfile librosa")
        print()
        print("  3. Download model:")
        print("     python -c \"from transformers import pipeline; pipeline('automatic-speech-recognition', model='vinai/PhoWhisper-medium')\"")
        print()
        print("  4. Run this test again")
    
    print()
    print("=" * 60)


if __name__ == '__main__':
    try:
        test_asr_service()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print()
        print("Make sure you're running from backend directory:")
        print("  cd backend")
        print("  python ai/asr/test_asr_service.py")
        sys.exit(1)
