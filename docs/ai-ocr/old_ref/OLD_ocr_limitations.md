# 📉 OCR Failure Analysis & Limitations Report

## 🔍 Diagnosis Summary

Based on the analysis of `02. BenhAnTongHop.pdf` running on the **GPU-accelerated 300 DPI Transformer** pipeline, we have identified specific failure modes that define the current accuracy ceiling (~58%).

While the OCR engine now clearly reads standard text ("Viêm phổi nặng" is perfect), it fails catastrophically in sections containing mixed media (images, tables, diagrams).

## ⚠️ Identified Failure Scenarios

### 1. Diagram Interference (The "Hallucination" Effect)

**Location:** Page 7 (Subclinical Results), Page 2, Page 8.
**Symptom:** The OCR engine attempts to read text from medical diagrams, ECG waves, or X-ray annotations.
**Result:**

- High 300 DPI resolution turns image noise into "character-like" shapes.
- The Transformer model (trained to find words) "hallucinates" English words from these shapes.
- **Observed Garbage:** `STANKS`, `SHAFT`, `BULLIE`, `CONTRANSMENTALIZED`, `CLATS`, `TELE`.
- **Impact:** These garbage tokens are inserted into the text stream, breaking the `is_header` logic and polluting the content extraction.
- **Metric:** Page 7 has a **30% garbage density** (English/Nonsense tokens vs total text).

### 2. Table Layout Destruction

**Location:** Page 8 (Treatment Plan), Page 5 (Lab Results).
**Symptom:** Text within grid-lines (tables) is detected as separate text boxes, often read column-by-column or row-by-row inconsistent with the reading order.
**Result:**

- Key-Value pairs are dissociated (e.g., "Result" is separated from "Value" by 30 lines of other text).
- **Impact:** The parser fails to extract structured data like `treatment_plan` or `lab_results` because the Regex expects proximity between the test name and result.
- **Metric:** `treatment_plan` extraction score is **10.6%** (content exists but structure is lost).

### 3. Header Confusion

**Location:** Page 2, Page 8.
**Symptom:** Garbage text appearing before a valid header (e.g., `03600001012\n1\nPA1: Hỏi bệnh`).
**Result:**

- The parser's `is_header` logic might reject valid headers if they are preceded by specific noise patterns or if the header itself is merged with noise ("1. Viêm phổi").
- **Impact:** Entire sections (like `chief_complaint` on Page 1/2) are skipped because the "Clinical History" header wasn't cleanly identified.

## 🛑 Limits of the Current Model

| Scenario             | Performance             | Recommendation                                                                      |
| :------------------- | :---------------------- | :---------------------------------------------------------------------------------- |
| **Clean Paragraphs** | ✅ **Excellent** (>95%) | Ideal for History of Present Illness, Notes.                                        |
| **Headers**          | ⚠️ **Good** (80%)       | Vulnerable to preceding noise.                                                      |
| **Tables / Grids**   | ❌ **Poor** (<40%)      | Structure is lost; requires specialized Table OCR model.                            |
| **Embedded Images**  | ❌ **Critical Failure** | Causes hallucinations; requires Layout Analysis / Image Segmentation pre-filtering. |

## 🔧 Action Plan (Mitigation)

1.  **Blacklist Filter (Implemented):** Added observed hallucinations (`STANKS`, `SHAFT`, etc.) to the garbage collector.
2.  **Layout Analysis (Future):** Implement a "Layout Parser" (e.g., PaddleLayout) to distinguish `Figure` regions from `Text` regions and crop them out _before_ sending to OCR.
3.  **Table Recovery (Future):** Use a dedicated Table Extraction model (e.g., `TableTransformer`) instead of raw text OCR for pages with grids.

## 📄 Proof

- **Page 7 Analysis**: 794 chars found, **208 digits** (correct for labs), but **30% noise**.
- **Missing Fields**: `vital_signs` (Page 2), `treatment_plan` (Page 8) correlate exactly with high-noise pages.
