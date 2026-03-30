# 🌟 Feature Implementation: OCR (Image-to-Text) Input Aid

## 💡 Overview

This document outlines the implementation plan for the **OCR (Optical Character Recognition) Input Aid** feature. This feature will allow users to upload image and PDF documents during case creation and file uploads, automatically transforming the visual data into pure, structured, and validated text using an OCR pipeline. This significantly improves data entry efficiency and accuracy.

## 🚀 GPU Acceleration Status (Updated 2026-01-04)

- **Status**: ✅ **ENABLED**
- **Hardware**: NVIDIA GeForce GTX 1650 detected.
- **Software**:
  - PyTorch (CUDA 12.1 compatible)
  - PaddlePaddle (CPU/Standard, but compatible)
  - `vgg_transformer` model enabled with `beamsearch=True`.
- **Performance**:
  - **Resolution**: High (300 DPI) for medical records.
  - **Speed**: ~20-30s per page (Transformer limited).
  - **Accuracy**: Significantly improved (58%+) especially on critical medical terms.

## ✅ Definition of Done (DoD)

The successful implementation of this feature is defined by the fulfillment of the following seven criteria:

### 1. Input Handling

- **Accepted Formats:** The system must correctly accept the following file formats:
  - **Images:** `JPG`, `JPEG`, `PNG`, `WEBP`
  - **Documents:** Single and multi-page `PDF` files.
- **Validation Rules:** Robust validation must be in place, including:
  - Enforcing file size limits (defined in Section 4).
  - Strict MIME type verification.
  - Graceful handling and reporting of corrupt or malformed files.

### 2. OCR Pipeline

The core OCR process must include the following stages for optimal accuracy, especially for Vietnamese text:

| Stage               | Description                                                      | Key Operations                                                                                                                                                            |
| :------------------ | :--------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Preprocessing**   | Standardize and enhance the image quality for the OCR engine.    | **300 DPI Conversion** (GPU enabled), Grayscale conversion, Denoising (e.g., median filter), Binarization (adaptive thresholding).                                        |
| **OCR Execution**   | Run the selected OCR engine (chosen from prior research/Task 1). | Image/page-to-text conversion using **PaddleOCR (Detection) + VietOCR (Transformer Recognition)**.                                                                        |
| **Post-processing** | Clean and validate the raw output from the OCR engine.           | Unicode normalization (NFC or NFKC), Specific Vietnamese diacritic validation, Comprehensive whitespace cleanup (e.g., removing extra spaces, standardizing line breaks). |

### 3. Output

The final output must meet strict quality and structuring requirements:

- **Text Encoding:** Pure UTF-8 Vietnamese text.
- **Structuring:** Text must be structured per page, especially for multi-page PDFs.
- **Quality Metadata:** A confidence score must be provided per text block or per page to assess extraction reliability.

### 4. Performance Constraints

The implementation must adhere to critical performance and resource constraints:

- **Latency:** The maximum acceptable OCR latency must be documented and benchmarked.
- **Max File Size:** A definitive maximum file size limit must be defined and enforced for both images and PDFs.
- **Fallback:** Support for a CPU-only fallback execution mode is required to ensure compatibility and stability in environments without dedicated GPU resources.

### 5. Error Handling

Comprehensive error handling is required to provide informative feedback:

- Detection and reporting of unsupported languages (non-Vietnamese/English).
- Graceful handling of empty or near-empty OCR results.
- Issuance of partial extraction warnings (e.g., low confidence sections).

### 6. Integration Readiness

The OCR functionality must be provided as a clean, reliable, and backend-safe service:

- **API Specification (Python):** The module must expose a simple, standardized function signature:
  ```python
  text, metadata = ocr_service.process(file_path)
  ```
- **Design Principle:** The service must be **stateless** (no stored session data between calls) and designed to be safely deployed in a backend service environment (e.g., an API endpoint or worker queue).

### 7. Deliverables

The following artifacts must be produced upon completion:

- **OCR Module:** The fully implemented and tested source code.
- **Sample Inputs & Outputs:** A collection of diverse sample files with their corresponding, validated text outputs.
- **Performance Benchmark:** A detailed report on the speed and accuracy metrics against the defined performance constraints.
- **Reporting:** A comprehensive report detailing the architecture, setup, performance results, and usage instructions, to be placed in a `README` file within the designated AI directory.
