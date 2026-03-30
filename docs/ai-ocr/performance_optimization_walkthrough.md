# OCR Performance Optimization - Walkthrough

**Date:** January 2026  
**Sprint:** Performance Optimization

## Goal

Reduce OCR processing time from **50s/page** to **~10-15s/page** while maintaining Vietnamese text quality.

## Results

| Metric              | Before   | After           |
| ------------------- | -------- | --------------- |
| Processing time     | 50s/page | **12-14s/page** |
| Speedup             | -        | **4x faster**   |
| Vietnamese accuracy | Good     | Excellent ✅    |

## Changes Made

### 1. Added DocTR Detection Engine

- Added `OCR_ENGINE` environment variable (default: `DOCTR`)
- Created `_get_doctr_detector()` method with GPU support
- Created `_process_page_doctr()` with line merging optimization
- Updated `prewarm_models()` to load correct engine

### 2. Engine Selection

```bash
# Fast mode (default) - 12-14s/page, no tables
export OCR_ENGINE=DOCTR

# Full mode - 50s/page, with table extraction
export OCR_ENGINE=PPSTRUCTURE
```

### 3. Pipeline Timing Breakdown

```
1. PDF conversion:    0.12s ✅
2. DocTR detection:   0.26s ✅ (GPU)
3. Box merging:       0.002s ✅
4. VietOCR (34 lines): 12.4s (365ms/line)
```

## Verification

Tested with medical documents showing:

- ✅ Vietnamese diacritics: Perfect (ư, ệ, ọ, ổ)
- ✅ Medical terms: SpO2, mmHg, EF correctly recognized
- ✅ Numbers/dates: 15h16 25/3/2025 accurate
- ✅ Line structure preserved with bounding boxes

## Remaining Work

Tables and images are handled manually by users in the current implementation.
See `tables_images_roadmap.md` for future sprint plan.
