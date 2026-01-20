import api from "./api";

export interface OCRResult {
  text: string;
  pages: Array<{
    page: number;
    text: string;
    confidence: number;
    warnings: string[];
  }>;
  structured: Record<string, any>;
  metadata: {
    page_count: number;
    elapsed_ms: number;
    engine: string;
    text_extraction_ms?: number;
  };
  // Phase 2: Table/Image extraction job (if mode="full")
  table_job_id?: string;
  table_job_status?: string;
}

export interface OCRJobStatus {
  status: 'queued' | 'running' | 'done' | 'failed';
  progress?: any;
  result?: OCRResult;
  error?: string;
}

export interface TableResult {
  page: number;
  bbox: number[];
  html: string;
  markdown: string;
}

export interface ImageResult {
  page: number;
  bbox: number[];
  url: string;
  caption: string;
}

export interface TableImageJobResult {
  status: 'queued' | 'running' | 'done' | 'failed';
  tables: TableResult[];
  images: ImageResult[];
  error?: string;
}

export interface AutofillResult {
  structured: Record<string, any>;
  matches: Record<string, {
    value: string;
    confidence: number;
    matched_heading: string;
  }>;
  metadata: {
    fields_matched: number;
    elapsed_ms: number;
  };
}

export const ocrService = {
  /**
   * Extract text from image or PDF
   * 
   * @param file - The file to process
   * @param mode - "text" (default) for fast text only, "full" to also extract tables/images
   * @param signal - Optional AbortController signal for request cancellation
   */
  async extractText(file: File, mode: 'text' | 'full' = 'text', signal?: AbortSignal): Promise<OCRResult> {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("mode", mode);

    const response = await api.post("/ocr/extract/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      signal, // Pass AbortController signal to axios
    });

    // If 202 Accepted, it's an async job (very large file)
    if (response.status === 202) {
      const jobId = response.data.job_id;
      return this.pollJobStatus(jobId, 1000, 120000, signal);
    }

    // If 200 OK, return result directly
    return response.data;
  },

  /**
   * Poll for async OCR job completion (text extraction)
   */
  async pollJobStatus(jobId: string, intervalMs = 1000, timeoutMs = 120000, signal?: AbortSignal): Promise<OCRResult> {
    const startTime = Date.now();

    return new Promise((resolve, reject) => {
      const checkStatus = async () => {
        try {
          // Check if aborted
          if (signal?.aborted) {
            reject(new Error("OCR request was cancelled"));
            return;
          }

          if (Date.now() - startTime > timeoutMs) {
            reject(new Error("OCR processing timed out"));
            return;
          }

          const response = await api.get(`/ocr/jobs/${jobId}/`, { signal });
          const data = response.data as OCRJobStatus;

          if (data.status === 'done' && data.result) {
            resolve(data.result);
          } else if (data.status === 'failed') {
            reject(new Error(data.error || "OCR processing failed"));
          } else {
            // Still running/queued, wait and retry
            setTimeout(checkStatus, intervalMs);
          }
        } catch (error: any) {
          // Handle abort error gracefully
          if (error.name === 'AbortError' || error.name === 'CanceledError') {
            reject(new Error("OCR request was cancelled"));
          } else {
            reject(error);
          }
        }
      };

      checkStatus();
    });
  },

  /**
   * Poll for table/image extraction job completion
   */
  async pollTableImageJob(jobId: string, intervalMs = 2000, timeoutMs = 300000): Promise<TableImageJobResult> {
    const startTime = Date.now();

    return new Promise((resolve, reject) => {
      const checkStatus = async () => {
        try {
          if (Date.now() - startTime > timeoutMs) {
            reject(new Error("Table/image extraction timed out"));
            return;
          }

          const response = await api.get(`/ocr/jobs/${jobId}/`);
          const data = response.data as TableImageJobResult;

          if (data.status === 'done') {
            resolve(data);
          } else if (data.status === 'failed') {
            reject(new Error(data.error || "Table/image extraction failed"));
          } else {
            // Still running/queued, wait and retry
            setTimeout(checkStatus, intervalMs);
          }
        } catch (error) {
          reject(error);
        }
      };

      checkStatus();
    });
  },

  /**
   * Auto-fill case template fields from OCR text using semantic matching.
   * Uses Vietnamese SBERT for heading-to-field matching.
   */
  async autofill(ocrText: string, confidenceThreshold = 0.6): Promise<AutofillResult> {
    const response = await api.post("/ocr/autofill/", {
      text: ocrText,
      confidence_threshold: confidenceThreshold
    });
    return response.data;
  },

  /**
   * Extract text and auto-fill in one step.
   * Optionally queues table/image extraction (mode="full").
   * @param signal - Optional AbortController signal for request cancellation
   */
  async extractAndAutofill(file: File, confidenceThreshold = 0.6, mode: 'text' | 'full' = 'text', signal?: AbortSignal): Promise<{
    ocr: OCRResult;
    autofill: AutofillResult;
  }> {
    const ocr = await this.extractText(file, mode, signal);
    
    // Skip autofill if OCR returned no text
    if (!ocr.text || ocr.text.trim() === '') {
      console.warn('OCR returned empty text, skipping autofill');
      return {
        ocr,
        autofill: {
          structured: {},
          matches: {},
          metadata: { fields_matched: 0, elapsed_ms: 0 }
        }
      };
    }
    
    const autofill = await this.autofill(ocr.text, confidenceThreshold);
    return { ocr, autofill };
  }
};
