import api from "./api";

export const exportService = {
  // Export case to PDF
  async exportToPDF(caseId: string) {
    const response = await api.get(`/exports/quick/cases/${caseId}/pdf/`, {
      responseType: "blob",
    });
    return response.data;
  },

  // Export case to Word document
  async exportToWord(caseId: string) {
    const response = await api.get(`/exports/cases/${caseId}/word/`, {
      responseType: "blob",
    });
    return response.data;
  },

  // Export case to JSON
  async exportToJSON(caseId: string) {
    const response = await api.get(`/exports/cases/${caseId}/json/`, {
      responseType: "blob",
    });
    return response.data;
  },

  // Download blob as file
  downloadBlob(blob: Blob, filename: string) {
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  },

  // Sanitize filename to be safe for file systems while preserving Vietnamese characters
  sanitizeFilename(filename: string): string {
    // Allow all Unicode letters, numbers, spaces, hyphens, and underscores
    // Replace other characters with underscores
    const sanitized = filename.replace(/[^\p{L}\p{N}\s\-_]/gu, '_');

    // Replace multiple consecutive underscores with single underscore
    // Remove leading/trailing underscores
    // Limit length to prevent filesystem issues
    return sanitized.replace(/_+/g, '_')
      .replace(/^_+|_+$/g, '')
      .substring(0, 100) || 'export';
  },

  // Export and download case in specified format
  async exportCase(caseId: string, format: string, caseTitle: string) {
    try {
      let blob;
      let extension;

      switch (format) {
        case "pdf":
          blob = await this.exportToPDF(caseId);
          extension = "pdf";
          break;
        case "word":
          blob = await this.exportToWord(caseId);
          extension = "docx";
          break;
        case "json":
          blob = await this.exportToJSON(caseId);
          extension = "json";
          break;
        default:
          throw new Error("Unsupported export format");
      }

      const filename = `${this.sanitizeFilename(caseTitle)}.${extension}`;
      this.downloadBlob(blob, filename);

      return true;
    } catch (error) {
      console.error("Export failed:", error);
      throw error;
    }
  },
};
