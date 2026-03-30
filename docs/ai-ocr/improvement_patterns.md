# OCR Improvement Patterns

> Transferable patterns for production ML systems

---

## 1. Celery Retries with Exponential Backoff

### Problem

External services fail. OCR models crash. Without retries, one failure = permanent failure.

### Pattern

```python
@shared_task(
    bind=True,
    max_retries=3,
    autoretry_for=(Exception,),
    retry_backoff=True,        # Exponential: 60s → 120s → 240s
    retry_backoff_max=600,
)
def my_task(self, ...):
    # Celery handles retries automatically
```

### Concept: Exponential Backoff

```
Attempt 1: Fail → Wait 60s
Attempt 2: Fail → Wait 120s (2x)
Attempt 3: Fail → Wait 240s (4x)
```

Transient failures resolve themselves. Increasing delays give systems time to recover.

---

## 2. FP16 Quantization (Half Precision)

### Problem

32-bit floats use 4 bytes/weight. 100M params = 400MB VRAM.

### Pattern

```python
# Convert model to half precision
if torch.cuda.is_available():
    model = model.half()
```

### Impact

| Metric   | FP32     | FP16   |
| -------- | -------- | ------ |
| Memory   | 100%     | 50%    |
| Speed    | 1x       | 1.3-2x |
| Accuracy | Baseline | ~99.9% |

For classification tasks (OCR), 3 decimal digits precision is sufficient.

---

## 3. Parallel Processing (ThreadPoolExecutor)

### Problem

10 pages × 10s each = 100s total (sequential).

### Pattern

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

with ThreadPoolExecutor(max_workers=2) as executor:
    futures = {executor.submit(process, item): i for i, item in enumerate(items)}
    results = [None] * len(items)
    for future in as_completed(futures):
        results[futures[future]] = future.result()
```

### Rule of Thumb

- **CPU-bound**: Use `ProcessPoolExecutor` or GPU
- **I/O-bound**: Use `ThreadPoolExecutor` or `asyncio`

For GPU inference, 2-3 workers optimal (limited by VRAM).

---

## 4. WebSocket Push vs HTTP Polling

### Problem

Polling wastes bandwidth. 1000 users × 1 req/3s = 333 req/s.

### Pattern

**Server (Django Channels):**

```python
class ProgressConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.job_id = self.scope['url_route']['kwargs']['job_id']
        await self.channel_layer.group_add(f"job_{self.job_id}", self.channel_name)
        await self.accept()

    async def progress_update(self, event):
        await self.send_json(event["data"])
```

**Task (sends progress):**

```python
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

async_to_sync(channel_layer.group_send)(
    f"job_{job_id}",
    {"type": "progress.update", "data": {"page": 1, "total": 10}}
)
```

**Client:**

```javascript
const ws = new WebSocket(`ws://host/ws/job/${id}/`);
ws.onmessage = (e) => updateUI(JSON.parse(e.data));
```

---

## 5. Confidence Display

### Problem

Backend computes confidence but frontend doesn't show it.

### Pattern

```vue
<span :class="conf >= 0.8 ? 'green' : conf >= 0.6 ? 'yellow' : 'red'">
  {{ (conf * 100).toFixed(0) }}%
</span>
<span v-if="conf < 0.7">⚠️ Verify this field</span>
```

### Concept: Calibrated Confidence

Users trust AI more when they understand uncertainty:

- 90% confident → right 90% of the time
- 60% confident → right 60% of the time

---

## Summary

| Pattern         | Problem               | When to Use              |
| --------------- | --------------------- | ------------------------ |
| Retry + Backoff | Transient failures    | External service calls   |
| FP16            | GPU memory/speed      | Neural network inference |
| Parallel        | Sequential bottleneck | Batch processing         |
| WebSocket       | Polling overhead      | Real-time updates        |
| Confidence      | User trust            | AI predictions           |
