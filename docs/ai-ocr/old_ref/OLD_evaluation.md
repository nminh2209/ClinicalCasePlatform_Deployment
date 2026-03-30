# 📑 OCR Feature Evaluation & Architectural Pivot

**Date:** 2026-01-09
**Project:** Medical Case Input Aid
**Context:** Analysis of OCR performance on Vietnamese medical records (PDFs/Images).

---

## 1. Executive Summary

This document records the evaluation of our OCR pipeline's evolution. While we have achieved **High Text Accuracy (~99%)** using a Hybrid approach (Paddle Detection + VietOCR), we have identified critical failures regarding **Layout Analysis** (Tables) and **Image Noise** (Hallucinations).

**Strategic Decision:** We will **NOT** abandon the current Hybrid architecture. Instead, we will upgrade the "Detection" layer to a "Structure Analysis" layer to filter non-text elements before recognition.

---

## 2. Component Evaluation 1: Text Recognition (The "Brain")

We tested three engines to solve the specific challenge of Vietnamese medical terminology (diacritics/tones).

| Engine             | Configuration | Accuracy | Status          | Findings                                                                                          |
| :----------------- | :------------ | :------- | :-------------- | :------------------------------------------------------------------------------------------------ |
| **Tesseract 5**    | `lang='vie'`  | ~85%     | ❌ Rejected     | Failed on stacked tones (e.g., `Huyền` vs `Huyễn`). Confused digits with brackets (`71` -> `7]`). |
| **Pure PaddleOCR** | `lang='vi'`   | ~90%     | ⚠️ Fallback     | Fast, but frequently drops tones on standard fonts (e.g., `Nhận định` -> `Nhân dinh`).            |
| **VietOCR**        | `vgg_seq2seq` | **~99%** | ✅ **Selected** | **SOTA Accuracy.** Correctly infers context for ambiguous accents. Essential for medical safety.  |

**Verdict:** We **must** retain VietOCR for the recognition layer. Pure Paddle or Tesseract are insufficient for patient safety.

---

## 3. Component Evaluation 2: Detection & Layout (The "Eyes")

We evaluated how the system finds text amidst medical charts, ECGs, and tables.

### Current Implementation: Text Detection (DBNet)

- **Method:** Scans image for "blobs of ink" and assumes everything is text.
- **Result:**
  - ✅ Excellent on clean paragraphs.
  - ❌ **Critical Failure on Diagrams:** The model "hallucinates" text from ECG waves and X-rays (e.g., outputting garbage tokens like `STANKS`, `SHAFT`, `BULLIE`).
  - ❌ **Critical Failure on Tables:** Detects individual cells as separate paragraphs, reading them Left-to-Right instead of Row-by-Row, destroying lab result associations.

### Proposed Implementation: Layout Analysis (PP-Structure)

- **Method:** Scans image for **Regions** (Text, Table, Figure, Title).
- **Projected Result:**
  - **Figures:** Classified as `figure` -> **SKIP** (Solves Hallucinations).
  - **Tables:** Classified as `table` -> **Use Table Structure Recovery**.
  - **Text:** Classified as `text` -> **Send to VietOCR**.

---

## 4. Limitation Analysis (From `ocr_limitations.md`)

| Limitation            | Severity    | Root Cause                                                    | Fix Strategy                                                                                  |
| :-------------------- | :---------- | :------------------------------------------------------------ | :-------------------------------------------------------------------------------------------- |
| **Hallucinations**    | 🔴 Critical | OCR Engine forces text prediction on image noise (ECG lines). | **Layout Analysis:** Detect `figure` regions and mask them out before OCR.                    |
| **Table Destruction** | 🟠 High     | Standard OCR reads linearly across columns.                   | **Structure Recovery:** Use `PP-Structure` to map cell coordinates.                           |
| **Heading Mismatch**  | 🟡 Medium   | Hard-coded string matching fails on synonyms.                 | **Semantic Search:** Implemented `sentence-transformers` to match vectors instead of strings. |

---

## 5. Architectural Pivot Plan

We are moving from a **2-Stage Pipeline** to a **3-Stage Layout-Aware Pipeline**.

### Old Flow (Current Limitations)

1.  **Input:** Image.
2.  **Detect:** Find all text boxes (blind to layout).
3.  **Recognize:** VietOCR reads boxes (reads garbage from charts).

### New Recommended Flow

1.  **Input:** Image.
2.  **Structure Analysis (PP-Structure):**
    - Identify regions: `[Table, Figure, Text]`.
3.  **Route:**
    - If `Figure`: **Discard**.
    - If `Table`: **Extract Rows/Cols**.
    - If `Text`: **Send to VietOCR**.
4.  **Semantic Match:** Map headers to Case Template using Embeddings.

---

## 6. Code Adaptation Requirement

To implement this pivot, the `OCRService` initialization must change from standard `PaddleOCR` to `PPStructure`.

```python
# PROPOSED CHANGE in ocr_service.py

# Old (Current)
# self.ocr = PaddleOCR(use_angle_cls=True, lang='vi')

# New (Recommended)
from paddleocr import PPStructure
self.layout_engine = PPStructure(
    table=False,       # Set True later for table extraction
    ocr=False,         # We only want layout boxes, not text yet
    show_log=False
)
```
