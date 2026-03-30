# OCR Feature — Complete Flow Documentation

## 1. Overview

The OCR ("Input Aid") feature extracts text from medical documents (images/PDFs) using **PaddleOCR** (detection) + **VietOCR** (Vietnamese recognition), then optionally auto-fills case wizard fields.

---

## 2. Files Involved

| Layer | File | Purpose |
|-------|------|---------|
| **Frontend** | `frontend/src/services/ocr.ts` | API client: uploads file, handles sync/async responses, polls job status |
| **Frontend** | `frontend/src/components/CreateCaseWizard/AttachmentsStep.vue` | UI: upload area, OCR button, auto-fill merge logic |
| **Frontend** | `frontend/src/components/MedicalAttachments.vue` | Alternative UI for existing cases (view/download/OCR) |
| **Backend** | `backend/ai/ocr/urls.py` | URL routing: `/api/ocr/extract/`, `/api/ocr/jobs/<id>/` |
| **Backend** | `backend/ai/ocr/views.py` | REST endpoints: `OCRExtractView`, `OCRJobStatusView` |
| **Backend** | `backend/ai/ocr/ocr_service.py` | Core OCR logic: `OCRService` singleton |
| **Backend** | `backend/ai/ocr/tasks.py` | Celery task for async processing |
| **Backend** | `backend/clinical_case_platform/urls.py` | Mounts `ai.ocr.urls` at `/api/ocr/` |
| **Backend** | `backend/clinical_case_platform/settings.py` | Registers `ai` app in `INSTALLED_APPS` |

---

## 3. High-Level Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│  AttachmentsStep.vue                                                        │
│    ├─ User clicks "OCR" button on uploaded file                             │
│    ├─ Calls: ocrService.extractText(file: File)                             │
│    │                                                                        │
│  ocr.ts                                                                     │
│    ├─ POST /api/ocr/extract/ (multipart/form-data)                          │
│    │   └─ Body: { file: <binary> }                                          │
│    │                                                                        │
│    ├─ If response.status === 200 (sync)                                     │
│    │   └─ Return OCRResult immediately                                      │
│    │                                                                        │
│    ├─ If response.status === 202 (async)                                    │
│    │   └─ Poll GET /api/ocr/jobs/{job_id}/ until done                       │
│    │                                                                        │
│    └─ Return OCRResult { text, pages[], structured{}, metadata{} }          │
│                                                                             │
│  AttachmentsStep.vue                                                        │
│    └─ Merges result.structured into caseData (auto-fill)                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  urls.py                                                                    │
│    path("api/ocr/", include("ai.ocr.urls"))                                 │
│      ├─ extract/      → OCRExtractView.post()                               │
│      └─ jobs/<id>/    → OCRJobStatusView.get()                              │
│                                                                             │
│  views.py :: OCRExtractView.post(request)                                   │
│    ├─ Validate file (size ≤ 10MB, type in [jpeg, png, webp, pdf])           │
│    ├─ Save to temp: MEDIA_ROOT/tmp/ocr_temp_<uuid>.<ext>                    │
│    ├─ Decision:                                                             │
│    │   ├─ Small file → Sync: ocr_service.process(path, mime)                │
│    │   └─ Large file → Async: process_ocr_task.delay(path, mime) → 202      │
│    └─ Return JSON { text, pages, structured, metadata }                     │
│                                                                             │
│  ocr_service.py :: OCRService.process(file_path, mime_type)                 │
│    ├─ _load_images(path, mime) → List[np.ndarray]                           │
│    │     ├─ PDF: pdf2image.convert_from_path() → cv2 images                 │
│    │     └─ Image: cv2.imread()                                             │
│    │                                                                        │
│    ├─ For each page image:                                                  │
│    │     └─ _process_page(img) → (text, confidence, boxes)                  │
│    │           ├─ PaddleOCR.ocr(img) → detection boxes                      │
│    │           ├─ Sort boxes top-to-bottom, left-to-right                   │
│    │           ├─ For each box:                                             │
│    │           │     ├─ Crop region from image                              │
│    │           │     └─ VietOCR.predict(pil_crop) → text line               │
│    │           └─ Join lines → page_text                                    │
│    │                                                                        │
│    ├─ Aggregate pages → full_text                                           │
│    ├─ _extract_structured_data(full_text) → { clinical_history: {...}, ... }│
│    └─ Return (full_text, pages[], structured{}, metadata{})                 │
│                                                                             │
│  tasks.py :: process_ocr_task(file_path, mime_type)                         │
│    └─ Wraps ocr_service.process() in Celery task for background execution   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Detailed Method Signatures

### Frontend

#### `ocr.ts`

```typescript
interface OCRResult {
  text: string;
  pages: Array<{
    page: number;
    text: string;
    confidence: number;
    warnings: string[];
  }>;
  structured: Record<string, any>;  // e.g. { clinical_history: { chief_complaint: "..." } }
  metadata: {
    page_count: number;
    elapsed_ms: number;
    engine: string;
  };
}

ocrService.extractText(file: File): Promise<OCRResult>
  - POST /api/ocr/extract/ with FormData { file }
  - If 202 → poll /api/ocr/jobs/{job_id}/ every 1s (timeout 60s)
  - Returns OCRResult

ocrService.pollJobStatus(jobId: string, intervalMs?, timeoutMs?): Promise<OCRResult>
  - Recursively GET /api/ocr/jobs/{jobId}/
  - Resolves when status === 'done'
```

### Backend

#### `views.py`

```python
class OCRExtractView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request) -> Response:
        # Input: request.FILES['file']
        # Output (sync):  { text, pages, structured, metadata }
        # Output (async): { job_id, status: "queued", message }
```

#### `ocr_service.py`

```python
class OCRService:
    def process(self, file_path: str, mime_type: str) -> Tuple[str, List, Dict, Dict]:
        """
        Returns:
          - full_text: str (all pages concatenated)
          - pages: List[{ page, text, confidence, warnings }]
          - structured: Dict (auto-mapped fields)
          - metadata: Dict { page_count, elapsed_ms, engine }
        """

    def _load_images(self, file_path, mime_type) -> List[np.ndarray]:
        """Convert PDF/image to list of OpenCV images"""

    def _process_page(self, img: np.ndarray) -> Tuple[str, float, List]:
        """
        Returns:
          - page_text: str
          - avg_confidence: float
          - boxes: List (detection boxes)
        """

    def _extract_structured_data(self, text: str) -> Dict:
        """Heuristic keyword matching to map text sections to case fields"""
```

---

## 5. Current Bug Analysis

### Error Message
```
ERROR OCR Processing failed: string index out of range
```

### Root Cause

In `_process_page()`, the PaddleOCR 3.3.2 output format differs from older versions:

```python
boxes = result[0]  # This is correct for detection
...
for box in boxes:
    box = np.array(box).astype(np.int32)  # ← BUG HERE
```

**PaddleOCR 3.x with full pipeline (rec=True, which is default)** returns:
```python
result[0] = [
    [ [[x1,y1], [x2,y2], [x3,y3], [x4,y4]], ("detected_text", 0.95) ],
    ...
]
```

Each element is `[box_coords, (text, score)]`, NOT just `box_coords`.

So when we do `box = np.array(box).astype(np.int32)`, we're trying to convert a tuple like `[[[coords]], ("text", score)]` to an array, and then access `box[0][1]` for sorting — causing "string index out of range" when it tries to index into the text string.

### Solution

We need to properly unpack the PaddleOCR result structure.

---

## 6. Fix Required

File: `backend/ai/ocr/ocr_service.py`

The `_process_page()` method needs to handle the actual PaddleOCR 3.x output format properly.
