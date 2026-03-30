# Tables and Images Handling - Future Sprint Roadmap

**Sprint:** Future Development  
**Priority:** Medium  
**Status:** Planned

## Context

The OCR pipeline currently focuses on **plain text extraction** using DocTR + VietOCR (4x faster).
Tables and images require different handling:

- **Tables**: Show content for user to copy (markdown if possible)
- **Images**: Show for user to view and manually extract content

---

## Tables Handling

### User Story

> As a user, I want to see extracted tables in a readable format in the "OCR" section, so I can copy the content as markdown.

### Recommended Approach: **Hybrid Detection**

Use DocTR for text, switch to PPStructure only for table regions.

```
1. DocTR detects all regions (fast, GPU)
2. Layout model identifies "table" regions
3. For table regions → call PPStructure for HTML extraction
4. Convert HTML to Markdown for display
```

### Implementation Options

| Option                       | Tool             | Pros                                  | Cons                     |
| ---------------------------- | ---------------- | ------------------------------------- | ------------------------ |
| **A. PPStructure (Current)** | PaddleOCR        | Already integrated, table HTML output | Slow (CPU), whole page   |
| **B. Table Transformer**     | TATR/Extractable | Fast, accurate structure              | Separate model, setup    |
| **C. Camelot**               | camelot-py       | Simple, text-based PDFs               | No image/scanned support |
| **D. pdfplumber**            | pdfplumber       | Good for structured PDFs              | No OCR for images        |

**Recommendation**: Start with **Option A** (PPStructure) for table-only pages, since it's already integrated.

### Tasks

- [ ] Detect pages with tables (layout analysis)
- [ ] Route table pages to PPStructure engine
- [ ] Convert PPStructure HTML → Markdown
- [ ] Display in "OCR" section of frontend

---

## Images Handling

### User Story

> As a user, I want embedded images (charts, ECG, X-rays) displayed in the OCR section, so I can view and manually copy relevant information.

### Recommended Approach: **Extract and Display**

```
1. Detect "figure" regions from layout analysis
2. Crop image region from original page
3. Save as separate image file
4. Return image URL in API response
5. Frontend displays in "OCR" section
```

### Implementation Options

| Option                 | Tool        | Pros                                 | Cons                          |
| ---------------------- | ----------- | ------------------------------------ | ----------------------------- |
| **A. PyMuPDF**         | pymupdf     | Direct extraction of embedded images | Vector graphics not supported |
| **B. DocTR Regions**   | DocTR       | Already detects "figure" type        | Need to crop from page        |
| **C. Layout Analysis** | PPStructure | Identifies "figure" label with bbox  | Already integrated            |

**Recommendation**: Use **Option C** (PPStructure layout) since it already identifies figure regions.

### Tasks

- [ ] Enable figure region detection in PPStructure
- [ ] Crop figure regions to separate images
- [ ] Save images to storage (MinIO/local)
- [ ] Return image URLs in OCR response
- [ ] Frontend: Display images in "OCR" section

---

## API Response Changes

### Current Response

```json
{
  "text": "...",
  "pages": [{ "regions": [...], "tables": [] }]
}
```

### Proposed Response

```json
{
  "text": "...",
  "pages": [{
    "regions": [...],
    "tables": [{
      "bbox": [x1, y1, x2, y2],
      "html": "<table>...</table>",
      "markdown": "| Col1 | Col2 |..."
    }],
    "images": [{
      "bbox": [x1, y1, x2, y2],
      "url": "/media/ocr/page1_fig1.png",
      "caption": "Figure 1"
    }]
  }]
}
```

---

## Sprint Breakdown

### Sprint N+1: Table Display

1. Add PPStructure fallback for table pages
2. HTML → Markdown converter
3. Frontend "OCR Tables" section

### Sprint N+2: Image Display

1. Figure region cropping
2. Image storage integration
3. Frontend image gallery in OCR section

---

## Dependencies

| Dependency     | Status           | Notes                  |
| -------------- | ---------------- | ---------------------- |
| PPStructure    | ✅ Installed     | CPU-only, ~50s/page    |
| PyMuPDF        | ❌ Not installed | `pip install pymupdf`  |
| markdown-table | ❌ Not installed | For HTML→MD conversion |
| MinIO storage  | ✅ Available     | For image storage      |

---

## Risks and Mitigations

| Risk                             | Impact        | Mitigation                               |
| -------------------------------- | ------------- | ---------------------------------------- |
| PPStructure slow on table pages  | UX delay      | Show loading indicator, async processing |
| Complex tables with merged cells | Poor markdown | Fall back to HTML display                |
| Large images bloat storage       | Storage costs | Compress/resize, cleanup old files       |
