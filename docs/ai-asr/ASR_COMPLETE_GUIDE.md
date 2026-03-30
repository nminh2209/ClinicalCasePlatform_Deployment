# ASR (Automatic Speech Recognition) - Complete Guide

## Overview

Voice-to-text system with intelligent fallback strategy:
- **Primary**: Browser's Web Speech API (instant, no server load)
- **Fallback**: VinAI PhoWhisper model (high accuracy Vietnamese ASR)

## Quick Start

### Installation

**Automated (Recommended):**
```bash
cd backend
python install_asr.py
```

**Manual:**
```bash
# Install dependencies (~2GB)
pip install torch>=2.0.0 --index-url https://download.pytorch.org/whl/cpu
pip install transformers>=4.35.0 accelerate soundfile librosa

# Download model (~1.5GB)
python -c "from transformers import pipeline; pipeline('automatic-speech-recognition', model='vinai/PhoWhisper-medium')"
```

### Verification

```bash
# Test service
python test_asr_service.py

# Check endpoint
curl http://localhost:8000/api/asr/status/
```

## Frontend Integration

### Basic Usage

```vue
<script setup>
import VoiceToText from '@/components/VoiceToText.vue'
import { ref } from 'vue'

const text = ref('')
</script>

<template>
  <VoiceToText v-model="text" />
</template>
```

### Compact Inline Button (36x36px)

```vue
<!-- Right side of input (recommended) -->
<div class="flex gap-2 items-start">
  <Input v-model="text" class="flex-1" />
  <VoiceToText v-model="text" />
</div>

<!-- With textarea -->
<div class="flex gap-2 items-start">
  <Textarea v-model="description" rows="4" class="flex-1" />
  <VoiceToText v-model="description" :max-duration="120" />
</div>
```

### Current Implementation

**Location:** `frontend/src/components/CreateCaseWizard/BasicInfoStep.vue`

```vue
<div class="space-y-2 md:col-span-2">
  <Label for="title">{{ t('createCase.caseTitle') }} *</Label>
  <Input id="title" v-model="localData.title" />
  
  <VoiceToText
    v-model="localData.title"
    language="vi-VN"
    :max-duration="60"
    idle-text="🎤 Nhấn để nhập bằng giọng nói"
  />
</div>
```

## Component API

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `modelValue` | String | `''` | v-model binding |
| `language` | String | `'vi-VN'` | Language code |
| `maxDuration` | Number | `60` | Max recording seconds |
| `autoApply` | Boolean | `true` | Auto-update v-model |
| `continuous` | Boolean | `false` | Continue after pause |
| `idleText` | String | - | Idle state text |
| `recordingText` | String | - | Recording state text |
| `processingText` | String | - | Processing state text |

### Events

| Event | Payload | Description |
|-------|---------|-------------|
| `update:modelValue` | `string` | v-model update |
| `transcription` | `string` | Transcribed text |
| `error` | `string` | Error occurred |
| `recording-start` | - | Recording started |
| `recording-stop` | - | Recording stopped |

### Visual States

- **Idle:** Gray button (36x36px) with hover effect
- **Recording:** Red with pulse animation + timer badge
- **Processing:** Blue with spinner animation

## Backend API

### Endpoints

```
GET  /api/asr/status/       - Check ASR service status
POST /api/asr/transcribe/   - Transcribe audio file
GET  /api/asr/languages/    - Get supported languages
```

### Status Response

```json
{
  "available": true,
  "model_name": "vinai/PhoWhisper-medium",
  "device": "cuda",
  "language_support": ["vi", "en"],
  "description": "Vietnamese-optimized speech recognition"
}
```

## System Requirements

### Minimum
- Python 3.8+
- 4GB RAM
- 5GB disk space
- Internet connection (first-time setup)

### Recommended
- Python 3.10+
- 8GB RAM
- 10GB disk space
- GPU with 4GB+ VRAM (optional)

### Dependencies Overview

| Package | Size | Purpose |
|---------|------|---------|
| torch | ~800MB | Deep learning framework |
| transformers | ~400MB | Model loading |
| accelerate | ~50MB | Optimization |
| soundfile | ~10MB | Audio reading |
| librosa | ~100MB | Audio processing |
| **Total** | **~1.4GB** | |

## How It Works

### Automatic Fallback Flow

```
Component starts → Detects Web Speech API
  ├─ ✅ Available (Chrome/Edge/Safari) → Use browser native (instant)
  └─ ❌ Not available (Firefox) → Use PhoWhisper backend (3-10s)
```

### Model Download Flow

```
1. Run: python install_asr.py
2. Script calls: pipeline("asr", model="vinai/PhoWhisper-medium")
3. Transformers checks cache → Downloads if needed → Saves to cache
4. Model cached for future use
```

### Cache Location

**Local Project Directory (Easy to Delete!):**
```
backend/ai/asr/phowhisper/
└── models--vinai--PhoWhisper-medium/
    └── snapshots/
        └── <hash>/
            └── pytorch_model.bin (~1.5GB)
```

**Why local?** Easy to find and delete if you need to free up space. Just delete the `phowhisper/` folder!

## Language Support

| Language | Web Speech API | PhoWhisper Backend |
|----------|---------------|-------------------|
| **Vietnamese** | Good | ⭐ Excellent (Optimized) |
| **English** | Excellent | Good |

## Troubleshooting

### ASR Dependencies Not Installed

```bash
python install_asr.py
```

### Failed to Download Model

**Causes:** No internet, firewall, insufficient disk space

**Solution:**
```bash
# Check internet
ping huggingface.co

# Retry download
python -c "from transformers import pipeline; pipeline('automatic-speech-recognition', model='vinai/PhoWhisper-medium')"
```

### Microphone Permission Denied

1. Click browser permission icon
2. Allow microphone access
3. Try HTTPS (required for some browsers)

### Slow Backend Processing

**Use GPU acceleration:**
```bash
# Check GPU
python -c "import torch; print(torch.cuda.is_available())"

# Install GPU PyTorch
pip install torch>=2.0.0 --index-url https://download.pytorch.org/whl/cu118
```

### Poor Vietnamese Accuracy (Web Speech API)

Use backend PhoWhisper for better Vietnamese accuracy - it's specifically optimized for Vietnamese.

## Performance

### Web Speech API
- Latency: Instant (real-time)
- Vietnamese: Good
- English: Excellent
- Offline: ❌

### PhoWhisper Backend
- **CPU:** 10-20s for 10s audio (real-time factor: ~2-3x)
- **GPU:** 2-3s for 10s audio (real-time factor: ~0.3x)
- Vietnamese: Excellent
- English: Good
- Offline: ✅ Yes

## Best Practices

### Field Positioning
1. Position button on the right (better UX)
2. Use with textareas for longer text
3. Set appropriate max-duration:
   - Short fields (title): 30-60s
   - Medium fields (symptoms): 60-120s
   - Long fields (history): 120-300s

### Recommended Fields
✅ **Highly Recommended:**
- Case Title
- Chief Complaint
- History of Present Illness
- Past Medical History
- Physical Examination Findings

❌ **Not Recommended:**
- Numeric fields (age, ID)
- Dropdowns (gender)
- Dates (use date picker)

## Production Deployment

### Environment Variables
```env
ASR_MODEL_NAME=vinai/PhoWhisper-medium
ASR_DEVICE=cuda
ASR_MAX_FILE_SIZE=52428800  # 50MB
```

### Server Requirements
**Recommended:**
- CPU: 8 cores
- RAM: 16GB
- GPU: NVIDIA with 4GB+ VRAM
- Storage: 20GB SSD

### Pre-load Model
```bash
python -c "from transformers import pipeline; pipeline('automatic-speech-recognition', model='vinai/PhoWhisper-medium')"
```

## Usage Examples

### Form Integration
```vue
<template>
  <form @submit.prevent="submitCase">
    <!-- Case Title -->
    <div class="space-y-2">
      <Label>Case Title</Label>
      <div class="flex gap-2">
        <Input v-model="caseData.title" class="flex-1" />
        <VoiceToText v-model="caseData.title" />
      </div>
    </div>

    <!-- Chief Complaint -->
    <div class="space-y-2">
      <Label>Chief Complaint</Label>
      <div class="flex gap-2 items-start">
        <Textarea v-model="caseData.complaint" rows="3" class="flex-1" />
        <VoiceToText v-model="caseData.complaint" :max-duration="120" />
      </div>
    </div>

    <button type="submit">Submit</button>
  </form>
</template>
```

### With Event Handlers
```vue
<VoiceToText
  v-model="text"
  @transcription="handleTranscription"
  @error="handleError"
  @recording-start="onStart"
  @recording-stop="onStop"
/>
```

### Programmatic Control
```vue
<template>
  <VoiceToText ref="voiceRef" v-model="text" />
  <button @click="voiceRef.startRecording()">Start</button>
  <button @click="voiceRef.stopRecording()">Stop</button>
</template>

<script setup>
const voiceRef = ref(null)
</script>
```

## Fixed Issues

### ✅ Resolved

1. **Missing Dependency Handling** - Added graceful degradation
2. **Model Download** - Automatic on first use
3. **Installation Instructions** - Created automated script
4. **Error Messages** - Comprehensive error handling
5. **Documentation** - Complete setup guides

### Service States

| State | Dependencies | Model | Status | Frontend Behavior |
|-------|-------------|-------|--------|-------------------|
| Not Installed | ❌ | ❌ | Unavailable | Uses Web Speech API |
| Deps Installed | ✅ | ❌ | Downloads on first use | Transitioning |
| Fully Operational | ✅ | ✅ | Available | Uses backend for Firefox |

## Files Structure

```
backend/ai/asr/
├── __init__.py                    # Module init
├── service.py                     # PhoWhisper service
├── views.py                       # Django API endpoints
├── urls.py                        # URL routing
├── requirements.txt               # Dependencies
├── install_asr.py                 # Automated installer
├── test_asr_service.py           # Test script
└── ASR_COMPLETE_GUIDE.md         # This file

frontend/src/components/
└── VoiceToText.vue               # Reusable component
```

## Quick Reference

### Installation Time
- Dependencies: 5-10 min (~1.4GB)
- Model: 3-8 min (~1.5GB)
- **Total: 10-20 min (~3GB)**

### Browser Support
- ✅ Chrome/Edge: Web Speech API (instant)
- ✅ Safari: Web Speech API (good)
- ⚠️ Firefox: PhoWhisper backend required

### Copy-Paste Templates

**Standard Input:**
```vue
<div class="flex gap-2">
  <Input v-model="field" class="flex-1" />
  <VoiceToText v-model="field" />
</div>
```

**Textarea:**
```vue
<div class="flex gap-2 items-start">
  <Textarea v-model="field" rows="4" class="flex-1" />
  <VoiceToText v-model="field" :max-duration="120" />
</div>
```

## Resources

- **PhoWhisper:** https://github.com/VinAIResearch/PhoWhisper
- **Web Speech API:** https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API
- **Transformers:** https://huggingface.co/docs/transformers

## Summary

✅ **Zero Configuration** - Works out of the box
✅ **Automatic Fallback** - Smart browser detection
✅ **Vietnamese Optimized** - PhoWhisper for accuracy
✅ **Compact Design** - 36x36px inline button
✅ **Easy Integration** - One-line component
✅ **Production Ready** - Comprehensive error handling

**Get Started:** Just add `<VoiceToText v-model="yourField" />` to any form field!
