# ASR (Automatic Speech Recognition)

Voice-to-text system with Vietnamese optimization using PhoWhisper.

## Quick Setup

```bash
cd backend
python ai/asr/install_asr.py
```

This will:
- Install dependencies (~1.4GB)
- Download PhoWhisper model (~1.5GB) to `backend/ai/asr/phowhisper/`
- Verify installation

**Time:** 10-20 minutes  
**Total size:** ~3GB

## Model Storage

The PhoWhisper model is stored locally in:
```
backend/ai/asr/phowhisper/
```

**Easy cleanup:** To free up space, just delete the `phowhisper/` folder. The system will automatically re-download it when needed.

## Full Documentation

See [ASR_COMPLETE_GUIDE.md](ASR_COMPLETE_GUIDE.md) for:
- Frontend integration
- Component API
- Troubleshooting
- Production deployment

## Quick Test

```bash
# Test ASR service
python ai/asr/test_asr_service.py

# Check endpoint
curl http://localhost:8000/api/asr/status/
```

## Files

- `install_asr.py` - Automated installer
- `service.py` - PhoWhisper ASR service
- `views.py` - Django API endpoints
- `urls.py` - URL routing
- `test_asr_service.py` - Test script
- `phowhisper/` - Model cache (created after installation)
