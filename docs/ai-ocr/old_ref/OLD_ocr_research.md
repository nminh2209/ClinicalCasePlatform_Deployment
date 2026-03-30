# OCR Pipeline Optimization & Infrastructure Research**

Context: High-accuracy medical OCR pipeline (PaddleOCR \+ VietOCR).  
Current Status: Functional but facing scalability risks (Memory usage & GPU crashes).  
Goal: strict efficiency analysis of the extraction step and infrastructure adaptation for GPU stability.

## **Part 1: PDF Extraction Efficiency Audit**

### **1\. The Diagnosis**

Your current code in ocr\_service.py uses:

from pdf2image import convert\_from\_path  
\# ...  
pages \= convert\_from\_path(file\_path, dpi=300)  \# ⚠️ DANGER ZONE

**Why this is inefficient:**

* **RAM Explosion:** convert\_from\_path by default loads **ALL** pages into RAM as uncompressed PIL.Image objects.  
  * *Math:* A single A4 page at 300 DPI is \~2480x3508 pixels. In RGB (3 bytes/pixel), that is **\~25 MB raw RAM per page**.  
  * *Impact:* A 100-page medical record will consume **2.5 GB of RAM** just for the images, before OCR even starts. If you process 4 concurrent requests, you crash the server.  
* **Speed:** pdf2image wraps poppler (subprocess), which is decent, but creating Python objects for every page blocks the main thread.

### **2\. The Solution: Stream Processing & Faster Libraries**

We recommend switching to **PyMuPDF (fitz)** or optimizing pdf2image to "stream" pages.

#### **Recommendation A: Switch to PyMuPDF (Fitz) \[Fastest\]**

Benchmarks consistently show PyMuPDF is 3-5x faster than pdf2image and allows direct pixel access without the overhead.

**Optimized Code Pattern:**

import fitz  \# PyMuPDF

def extract\_images\_optimized(pdf\_path, dpi=300):  
    doc \= fitz.open(pdf\_path)  
    zoom \= dpi / 72  \# standard PDF is 72 pt  
    mat \= fitz.Matrix(zoom, zoom)  
      
    for page in doc:  
        \# Render ONLY the current page to memory  
        pix \= page.get\_pixmap(matrix=mat)  
          
        \# Convert to PIL/OpenCV format immediately and yield  
        \# This keeps RAM usage constant (only 1 page in memory at a time)  
        img\_data \= Image.frombytes("RGB", \[pix.width, pix.height\], pix.samples)  
        yield img\_data

#### **Recommendation B: Strict pdf2image Optimization \[Minimal Change\]**

If you must keep pdf2image, you **must** use a generator to process pages one by one.

**Optimized Code Pattern:**

from pdf2image import pdfinfo\_from\_path, convert\_from\_path

def extract\_images\_stream(pdf\_path, dpi=300):  
    \# Get page count first  
    info \= pdfinfo\_from\_path(pdf\_path)  
    max\_pages \= info\["Pages"\]  
      
    \# Process in chunks of 1 to keep RAM low  
    for i in range(1, max\_pages \+ 1):  
        \# Only convert one page at a time  
        batch \= convert\_from\_path(pdf\_path, dpi=dpi, first\_page=i, last\_page=i)  
        for page in batch:  
            yield page

## **Part 2: Infrastructure & GPU Concurrency Research**

### **1\. The "Sequential GPU" Crash Explained**

You noted that *"running parallel leads to crashes due to CUDA context conflicts."* This is a known architectural constraint, not just a configuration bug.

**The "Poison Fork" Problem:**

* **Context:** In Linux, Python's default multiprocessing uses fork(). This copies the parent process's memory to the child.  
* **The Crash:** If you initialize CUDA (load a model) in the *Parent* process (e.g., Django/Celery main process) and then fork, the *Child* process inherits a broken pointer to the GPU. When the child tries to access the GPU, it causes a specific crash (often CUDA error: initialization error).  
* **The Lock:** Even if you fix the fork issue (by using spawn), a single GPU cannot execute two heavy CUDA kernels perfectly simultaneously without context switching overhead.

### **2\. Viable Architecture Models**

#### **Level 1: The "Solo" Worker (Simplest / Current Fix)**

Force your worker queue (Celery/RQ) to handle tasks sequentially.

* **Config:** Set concurrency \= 1 and pool \= solo.  
* **Pros:** 100% stable. Zero CUDA conflicts.  
* **Cons:** Slow. One massive file blocks everyone else.

#### **Level 2: The "Spawn" Method (Native Parallelism)**

Force Python to create fresh processes that *don't* inherit the broken GPU handle.

* **Implementation:**  
  import multiprocessing  
  multiprocessing.set\_start\_method('spawn', force=True)

* **Pros:** Can utilize multiple GPUs if you have them.  
* **Cons:** High startup overhead (reloading models for every single task). **Not recommended** for heavy models like VietOCR.

#### **Level 3: The "Inference Server" Pattern (Production Standard)**

Decouple the web logic from the GPU logic.

* **Architecture:**  
  1. **Web/Django:** Extracts the PDF images (CPU task).  
  2. **Queue (Redis):** Pushes the *images* (bytes) to a queue.  
  3. **GPU Worker:** A standalone script (separate from Django) that keeps the models loaded in memory permanently. It pulls images one by one and processes them.  
* **Pros:** Zero model reloading time. Perfect stability. The Web server can handle 1000 requests, and the GPU worker churns through them at max speed without crashing.

### **3\. Recommendation**

**Immediate Action (Code Level):**

1. Replace the pdf2image full-load logic with the **Generator Pattern** (Recommendation B or A).  
2. Do **not** use multiprocessing inside your ocr\_service.py for the inference step if you are running inside a web server.

Infrastructure Action:  
If you use Celery, use the Inference Server Pattern logic:

* Create a specialized queue: celery \-A proj worker \-Q ocr\_queue \-c 1 \--pool=solo  
* This ensures only **one** process ever touches the GPU, preventing conflicts, while your web server remains responsive.