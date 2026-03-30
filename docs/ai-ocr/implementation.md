# OCR Implementation Documentation

## Overview

The Clinical Case Platform OCR system extracts text, tables, and images from medical documents (PDFs/images) and auto-fills case forms using semantic matching.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           FRONTEND (Vue.js)                         │
├─────────────────────────────────────────────────────────────────────┤
│  AttachmentsStep.vue          OCRResultsStep.vue                    │
│  ├── File Upload              ├── Table Display                     │
│  ├── OCR Button (locked)      ├── Image Display                     │
│  └── runOCR() → API           └── pollTableImageJob() → Polling     │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                           BACKEND (Django)                          │
├─────────────────────────────────────────────────────────────────────┤
│  /api/ocr/extract/           /api/ocr/jobs/{id}/                    │
│  ├── Phase 1: Text           └── Celery AsyncResult                 │
│  ├── SBERT Autofill                                                 │
│  └── Queue Celery Task                                              │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        CELERY WORKER (Redis)                        │
├─────────────────────────────────────────────────────────────────────┤
│  extract_tables_images_task                                         │
│  ├── PaddleX Table Recognition                                      │
│  ├── Figure Cropping                                                │
│  └── Cleanup Temp Files                                             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Model Stack

### 1. Text Detection - DocTR (GPU)

- **Model**: `db_resnet50`
- **Framework**: DocTR (PyTorch)
- **Purpose**: Fast GPU-based text region detection
- **Performance**: ~2-3s per page on GPU
- **File**: `ocr_service.py` → `_get_doctr_detector()`

### 2. Text Recognition - VietOCR

- **Model**: `vgg_transformer`
- **Framework**: VietOCR (PyTorch)
- **Purpose**: Vietnamese text recognition with diacritics
- **Performance**: 15-20 lines/second
- **Config**: Beam search disabled for speed
- **File**: `ocr_service.py` → `_get_recognizer()`

### 3. Table/Image Extraction - PaddleX

- **Pipeline**: `table_recognition`
- **Framework**: PaddleX
- **Models loaded**:
  - SLANet_plus (table structure)
  - PP-OCRv4_server_det (detection)
  - PP-OCRv4_server_rec_doc (recognition)
- **Size**: ~200MB (much lighter than PPStructureV3's 3GB)
- **File**: `ocr_service.py` → `_get_layout_engine()`

### 4. Semantic Matching - Vietnamese SBERT

- **Model**: `keepitreal/vietnamese-sbert`
- **Framework**: sentence-transformers
- **Purpose**: Match OCR headings to form fields
- **Confidence threshold**: 0.6
- **File**: `heading_matcher.py`

---

## Two-Phase Processing Flow

### Phase 1: Synchronous Text Extraction

```python
# views.py - OCRExtractView.post()

1. Receive file upload with mode="full"
2. Save to temp file (media/tmp/ocr_temp_{uuid}.{ext})
3. Convert to images:
   - PDF: pdf2image + poppler
   - Image: PIL.Image
4. Text detection (DocTR):
   - GPU-accelerated db_resnet50
   - Returns bounding boxes for text regions
5. Text recognition (VietOCR):
   - Process each detected region
   - Vietnamese diacritics support
6. Post-processing:
   - Sort lines by position (top-to-bottom, left-to-right)
   - Filter garbage text (repetition, gibberish)
   - Merge into full document text
7. SBERT semantic matching:
   - Extract headings (lines ending with ":")
   - Match to form field synonyms
   - Return structured autofill data
8. Queue Celery task for tables/images
9. Return response:
   {
     "text": "...",
     "structured_data": {...},
     "table_job_id": "uuid",
     "table_job_status": "queued"
   }
```

### Phase 2: Asynchronous Table/Image Extraction

```python
# tasks.py - extract_tables_images_task()

1. Celery worker receives task with file_path
2. Load PaddleX table_recognition pipeline
3. Convert file to images
4. For each page:
   a. Run table recognition → Extract HTML tables
   b. Detect figure/image regions
   c. Crop and save images to media/ocr_images/
5. Cleanup temp file
6. Return result:
   {
     "status": "done",
     "tables": [{"html": "...", "page": 1}],
     "images": [{"url": "/media/...", "caption": "..."}]
   }
```

---

## SBERT Semantic Matching

The system uses Vietnamese SBERT for semantic similarity matching between OCR-extracted headings and predefined form field labels.

### Process Flow

```python
# heading_matcher.py

1. Extract headings from OCR text
   - Pattern: Lines ending with ":"
   - Example: "Họ và tên:", "Ngày sinh:", "Địa chỉ:"

2. Load predefined field synonyms
   field_synonyms = {
       "patient_name": ["Họ tên", "Tên bệnh nhân", "Họ và tên"],
       "date_of_birth": ["Ngày sinh", "Sinh ngày", "NS"],
       "gender": ["Giới tính", "Giới", "Nam/Nữ"],
       "address": ["Địa chỉ", "Nơi ở", "Địa chỉ thường trú"],
       ...
   }

3. Embed headings with SBERT
   heading_embeddings = model.encode(headings)

4. Compute cosine similarity with each field's synonyms
   for heading in headings:
       for field, synonyms in field_synonyms.items():
           similarity = cosine_similarity(heading, synonyms)
           if max(similarity) >= 0.6:
               matches[field] = extract_value_after_heading(heading)

5. Return structured autofill data
```

### Matched Fields

| Category | Fields                                |
| -------- | ------------------------------------- |
| Patient  | name, DOB, gender, address, phone, ID |
| Case     | diagnosis, symptoms, medical history  |
| Hospital | admission date, department, doctor    |
| Clinical | vital signs, medications, procedures  |

---

## Celery Async Implementation

### Configuration

```python
# clinical_case_platform/celery.py

from celery import Celery

app = Celery('clinical_case_platform')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Broker: Redis
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
```

### Task Definition

```python
# ai/ocr/tasks.py

@shared_task(bind=True)
def extract_tables_images_task(self, file_path, mime_type):
    """
    Async Celery task for table and image extraction.
    Phase 2 of two-phase OCR flow.
    """
    tables = ocr_service.extract_tables(file_path, mime_type)
    images = ocr_service.extract_images(file_path, mime_type)

    # Cleanup temp file
    if os.path.exists(file_path) and '/tmp/' in file_path:
        os.remove(file_path)

    return {
        "status": "done",
        "tables": tables,
        "images": images
    }
```

### Job Status API

```python
# ai/ocr/views.py

class OCRJobStatusView(views.APIView):
    def get(self, request, job_id):
        result = AsyncResult(job_id)

        if result.state == 'PENDING':
            return Response({"status": "queued"})
        elif result.state == 'STARTED':
            return Response({"status": "running"})
        elif result.state == 'SUCCESS':
            return Response({
                "status": "done",
                "tables": result.result.get("tables", []),
                "images": result.result.get("images", [])
            })
        elif result.state == 'FAILURE':
            return Response({"status": "failed", "error": str(result.result)})
```

### Startup Script Integration

```bash
# start_all.sh

# Purge old Celery tasks for clean start
celery -A clinical_case_platform purge -f

# Start Celery worker
celery -A clinical_case_platform worker -l info
```

---

## Guardrails & Error Handling

### 1. Frontend OCR Button Lock (Serial Pipeline)

```typescript
// AttachmentsStep.vue

const isOcrProcessing = computed(() => {
  // Text extraction in progress
  if (ocrProcessing.value || localData.value?.ocrProcessing === true) {
    return true;
  }

  // Celery table/image extraction pending
  const tableJobStatus = localData.value?.ocrResult?.table_job_status;
  if (tableJobStatus === "queued" || tableJobStatus === "running") {
    return true;
  }

  return false;
});

// Button stays locked until ENTIRE pipeline completes
```

### 2. AbortController for Request Cancellation

```typescript
// AttachmentsStep.vue

let currentAbortController: AbortController | null = null;

onUnmounted(() => {
  if (currentAbortController) {
    console.log("🛑 Canceling ongoing OCR request on unmount");
    currentAbortController.abort();
    currentAbortController = null;
  }
});

// In runOCR:
currentAbortController = new AbortController();
const { ocr, autofill } = await ocrService.extractAndAutofill(
  file,
  0.6,
  "full",
  currentAbortController.signal
);
```

### 3. Polling Cancellation

```typescript
// OCRResultsStep.vue

let currentPollingJobId: string | null = null;
let pollAbortController: AbortController | null = null;

const pollTableImageJob = async (jobId: string) => {
  // Cancel previous poll if different job
  if (currentPollingJobId && currentPollingJobId !== jobId) {
    pollAbortController?.abort();
  }

  // Skip if already polling this job
  if (currentPollingJobId === jobId && tableJobLoading.value) {
    return;
  }

  currentPollingJobId = jobId;
  pollAbortController = new AbortController();
  // ... polling logic with signal
};
```

### 4. File Object Preservation

```typescript
// AttachmentsStep.vue

// ❌ WRONG - JSON.stringify destroys File objects
const tempData = JSON.parse(JSON.stringify(localData.value));

// ✅ CORRECT - Spread operator preserves File references
const currentAttachments = localData.value.attachments || [];
localData.value = {
  ...localData.value,
  attachments: currentAttachments,
  ocrProcessing: true,
};
```

### 5. Graceful Error Handling

```typescript
// Handle cancelled requests silently (no alert)
if (error.message?.includes("cancelled") || error.name === "AbortError") {
  console.log("🛑 OCR request was cancelled");
} else {
  alert(`Lỗi OCR: ${error.message}`);
}
```

---

## File Structure

```
backend/ai/ocr/
├── __init__.py
├── apps.py              # Django app config, prewarm on startup
├── urls.py              # Route definitions
├── views.py             # API endpoints (extract, job status, autofill)
├── tasks.py             # Celery async tasks
├── ocr_service.py       # Main OCR class with all models
├── heading_matcher.py   # SBERT semantic matching
└── docs/
    ├── implementation.md    # This file
    └── future_improvements.md

frontend/src/
├── services/
│   └── ocr.ts           # OCR API client
└── components/CreateCaseWizard/
    ├── AttachmentsStep.vue   # File upload + OCR button
    └── OCRResultsStep.vue    # Table/image display + polling
```

---

## API Endpoints

| Endpoint              | Method | Purpose                     | Response                                |
| --------------------- | ------ | --------------------------- | --------------------------------------- |
| `/api/ocr/extract/`   | POST   | Extract text + queue Celery | `{text, structured_data, table_job_id}` |
| `/api/ocr/jobs/{id}/` | GET    | Poll Celery job status      | `{status, tables, images}`              |
| `/api/ocr/autofill/`  | POST   | SBERT semantic matching     | `{matches, confidence}`                 |

---

## Performance Metrics

| Metric                      | Current | Notes             |
| --------------------------- | ------- | ----------------- |
| Text extraction (per page)  | 8-12s   | DocTR + VietOCR   |
| Table extraction (per page) | 40-60s  | PaddleX           |
| SBERT matching              | <500ms  | Cached embeddings |
| End-to-end (1 page)         | 50-70s  | Sequential phases |
