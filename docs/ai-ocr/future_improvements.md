# Future Improvements

## Performance Optimizations

### 1. VietOCR Batch Processing

**Current**: ~15-20 lines/second (sequential)
**Target**: 50+ lines/second

```python
# Current: Process one line at a time
for region in regions:
    text = recognizer.predict(region)

# Improved: Batch multiple regions
batch_size = 16
for i in range(0, len(regions), batch_size):
    batch = regions[i:i+batch_size]
    texts = recognizer.predict_batch(batch)
```

**Implementation**:

- Modify VietOCR predictor to accept batches
- Pad images to same size for batching
- Use GPU efficiently with larger batch sizes

### 2. TensorRT Optimization

**Expected speedup**: 2-3x for GPU inference

```python
# Convert VietOCR model to TensorRT
import torch_tensorrt

model = torch.load("vgg_transformer.pth")
trt_model = torch_tensorrt.compile(model,
    inputs=[torch_tensorrt.Input(shape=[1, 3, 32, 128])],
    enabled_precisions={torch.float16}
)
```

### 3. Parallel Page Processing

**Current**: Sequential page processing
**Target**: Process multiple pages concurrently

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def process_document(images):
    with ThreadPoolExecutor(max_workers=4) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(executor, process_page, img, i)
            for i, img in enumerate(images)
        ]
        results = await asyncio.gather(*tasks)
    return merge_results(results)
```

### 4. Model Quantization

**Approach**: FP16 or INT8 quantization

```python
# FP16 for VietOCR
model = model.half()  # Convert to FP16

# INT8 for DocTR (more aggressive)
from torch.quantization import quantize_dynamic
model = quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
```

---

## Architecture Improvements

### 1. WebSocket Streaming

**Current**: Polling every 3 seconds
**Target**: Real-time progress updates

```typescript
// Frontend
const ws = new WebSocket(`/ws/ocr/${jobId}/`);
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  updateProgress(data.page, data.total, data.status);
};

// Backend (Django Channels)
async def ocr_progress(self, event):
    await self.send(text_data=json.dumps({
        'page': event['page'],
        'total': event['total'],
        'status': event['status']
    }))
```

### 2. Task Priority Queue

**Approach**: Priority based on document size/urgency

```python
# High priority for small documents (quick turnaround)
if file_size < 1_000_000:  # < 1MB
    extract_task.apply_async(priority=0)  # Highest
else:
    extract_task.apply_async(priority=5)  # Normal
```

### 3. Dead Letter Queue

**Purpose**: Handle failed tasks gracefully

```python
# celery.py
app.conf.task_routes = {
    'ai.ocr.tasks.*': {
        'queue': 'ocr',
        'dead_letter_exchange': 'ocr_dlx',
        'dead_letter_routing_key': 'ocr_failed'
    }
}

# Retry failed tasks with exponential backoff
@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def extract_tables_images_task(self, file_path, mime_type):
    try:
        ...
    except Exception as e:
        self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
```

### 4. Model Warm-Start Service

**Current**: Models loaded on first request (cold start ~40s)
**Target**: Keep models warm in dedicated service

```python
# ocr_worker.py - Long-running OCR service
class OCRWorkerService:
    def __init__(self):
        self.detector = load_doctr()
        self.recognizer = load_vietocr()
        self.layout = load_paddlex()

    def process(self, request):
        # Models already loaded, instant processing
        return self._run_ocr(request)

# Run as daemon
if __name__ == "__main__":
    service = OCRWorkerService()
    service.listen()  # Listen for RPC calls
```

---

## Quality Improvements

### 1. Confidence Score Display

**Purpose**: Show users which fields need review

```typescript
// Frontend
<div v-for="field in autofillFields">
  <span>{{ field.value }}</span>
  <span :class="confidenceClass(field.confidence)">
    {{ (field.confidence * 100).toFixed(0) }}%
  </span>
  <span v-if="field.confidence < 0.7" class="warning">
    ⚠️ Low confidence - please verify
  </span>
</div>
```

### 2. Learning from Corrections

**Purpose**: Improve SBERT matching over time

```python
# When user corrects an autofill field:
def record_correction(heading, field, correct_value):
    # Store in database
    Correction.objects.create(
        heading=heading,
        predicted_field=field,
        correct_field=correct_field,
        timestamp=now()
    )

# Periodically retrain synonym embeddings
def update_synonyms():
    corrections = Correction.objects.all()
    for c in corrections:
        field_synonyms[c.correct_field].append(c.heading)
    recalculate_embeddings()
```

### 3. Advanced Garbage Filtering

**Current**: Regex-based repetition detection
**Target**: ML-based quality filtering

```python
# Use language model perplexity
from transformers import GPT2LMHeadModel, GPT2Tokenizer

def calculate_perplexity(text):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs, labels=inputs["input_ids"])
    return math.exp(outputs.loss.item())

def is_garbage(text):
    perplexity = calculate_perplexity(text)
    return perplexity > 1000  # High perplexity = likely garbage
```

### 4. Table Structure Validation

**Purpose**: Verify extracted tables are well-formed

```python
def validate_table(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Check structure
    rows = soup.find_all('tr')
    if len(rows) < 2:
        return False, "Table has insufficient rows"

    # Check consistency
    cell_counts = [len(row.find_all(['td', 'th'])) for row in rows]
    if len(set(cell_counts)) > 2:
        return False, "Inconsistent column count"

    return True, None
```

---

## Scalability Improvements

### 1. Horizontal Scaling

**Current**: Single Celery worker
**Target**: Multiple workers with load balancing

```yaml
# docker-compose.yml
services:
  celery-worker:
    image: clinical-case-platform
    command: celery -A clinical_case_platform worker -l info
    deploy:
      replicas: 3 # Scale horizontally
      resources:
        limits:
          memory: 4G
```

### 2. GPU Resource Pooling

**Purpose**: Share GPUs across workers efficiently

```python
# Use NVIDIA MPS for concurrent GPU access
# Or implement GPU scheduling

class GPUPool:
    def __init__(self, num_gpus=1):
        self.semaphore = asyncio.Semaphore(num_gpus)

    async def acquire(self):
        await self.semaphore.acquire()
        return self._get_available_gpu()

    def release(self, gpu_id):
        self.semaphore.release()
```

### 3. Caching Layer

**Purpose**: Cache repeated OCR results

```python
import hashlib
from django.core.cache import cache

def get_cached_ocr(file_content):
    file_hash = hashlib.md5(file_content).hexdigest()
    cached = cache.get(f"ocr:{file_hash}")
    if cached:
        return cached

    result = run_ocr(file_content)
    cache.set(f"ocr:{file_hash}", result, timeout=86400)  # 24h
    return result
```

---

## Integration Improvements

### 1. Multi-Language Support

**Current**: Vietnamese only
**Target**: Vietnamese + English + Chinese

```python
# Language detection
from langdetect import detect

def get_recognizer(text_sample):
    lang = detect(text_sample)
    if lang == 'vi':
        return VietOCR()
    elif lang == 'zh':
        return PaddleOCR(lang='ch')
    else:
        return TesseractOCR(lang='eng')
```

### 2. Document Classification

**Purpose**: Auto-detect document type for better field mapping

```python
# Classify document before OCR
from transformers import pipeline

classifier = pipeline("text-classification", model="medical-doc-classifier")

def classify_document(text):
    result = classifier(text[:512])  # First 512 chars
    return result[0]['label']  # e.g., "discharge_summary", "lab_report"

# Use document-type-specific field mappings
field_synonyms = FIELD_SYNONYMS[doc_type]
```

### 3. Export Formats

**Purpose**: Support multiple output formats

```python
def export_ocr_result(result, format='json'):
    if format == 'json':
        return json.dumps(result)
    elif format == 'csv':
        return pandas.DataFrame(result['structured_data']).to_csv()
    elif format == 'pdf':
        return generate_searchable_pdf(result)
    elif format == 'docx':
        return generate_word_doc(result)
```

---

## Priority Roadmap

| Priority  | Improvement               | Impact             | Effort |
| --------- | ------------------------- | ------------------ | ------ |
| 🔴 High   | VietOCR batch processing  | 2-3x speedup       | Medium |
| 🔴 High   | Confidence display        | Better UX          | Low    |
| 🟡 Medium | WebSocket streaming       | Real-time feedback | Medium |
| 🟡 Medium | Learning from corrections | Accuracy over time | Medium |
| 🟢 Low    | Multi-language support    | Broader use        | High   |
| 🟢 Low    | Horizontal scaling        | Enterprise ready   | High   |
