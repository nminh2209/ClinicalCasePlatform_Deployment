import api from "./api";
import type {
  InstructorCase,
  CreateInstructorCaseRequest,
  CloneCaseRequest,
  CloneCaseResponse,
  InstructorCaseAuditLog,
  ListCasesParams,
  CaseListResponse,
} from "../types/instructor";

export const casesService = {
  async getCases(params = {}) {
    const response = await api.get("/cases/", { params });
    return response.data;
  },

  async getCase(id: string) {
    const response = await api.get(`/cases/${id}/`);
    const caseData = response.data;

    // Check if medical_attachments already included in response
    if (!caseData.medical_attachments) {
      // Fetch medical attachments for this case as fallback
      try {
        const attachmentsResponse = await api.get(`/cases/${id}/attachments/`);
        caseData.medical_attachments = attachmentsResponse.data;
        console.log('📎 Fetched attachments from separate endpoint:', caseData.medical_attachments);
      } catch (error) {
        console.warn("Failed to fetch medical attachments:", error);
        caseData.medical_attachments = [];
      }
    } else {
      console.log('📎 Attachments already in case response:', caseData.medical_attachments);
    }

    return caseData;
  },

  async createCase(caseData: any) {
    const response = await api.post("/cases/", caseData);
    return response.data;
  },

  async updateCase(id: string, caseData: any) {
    const response = await api.put(`/cases/${id}/`, caseData);
    return response.data;
  },

  async deleteCase(id: string) {
    await api.delete(`/cases/${id}/`);
  },

  async submitCase(id: string) {
    const response = await api.post(`/cases/${id}/submit/`);
    return response.data;
  },

  async getCasePermissions(caseId: string) {
    const response = await api.get(`/cases/${caseId}/permissions/`);
    return response.data;
  },

  async shareCaseWithUser(caseId: string, userId: string, permissionType: any) {
    const response = await api.post(`/cases/${caseId}/permissions/`, {
      user: userId,
      permission_type: permissionType,
    });
    return response.data;
  },

  async searchCases(query: string) {
    const response = await api.get("/cases/search/", { params: { q: query } });
    return response.data;
  },

  // Medical Attachments
  async getCaseAttachments(caseId: string) {
    const response = await api.get(`/cases/${caseId}/attachments/`);
    return response.data;
  },

  async downloadAttachment(attachmentId: string) {
    const response = await api.get(`/cases/attachments/${attachmentId}/`, {
      responseType: "blob",
    });
    return response;
  },

  async uploadAttachment(caseId: string, formData: any) {
    const response = await api.post(`/cases/${caseId}/attachments/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  },

  // Student Notes
  async getStudentNotes(caseId: string) {
    try {
      const response = await api.get(`/cases/${caseId}/notes/`);
      console.log('getStudentNotes API response:', response.data);
      // Handle paginated response
      if (response.data.results && response.data.results.length > 0) {
        return response.data.results[0];
      }
      // Fallback for non-paginated response
      return response.data.length > 0 ? response.data[0] : null;
    } catch (error) {
      console.error("Failed to fetch student notes:", error);
      return null;
    }
  },

  async saveStudentNotes(caseId: string, notesData: any) {
    const response = await api.post(`/cases/${caseId}/notes/`, notesData);
    return response.data;
  },

  async updateStudentNotes(noteId: string, notesData: any) {
    const response = await api.put(`/cases/notes/${noteId}/`, notesData);
    return response.data;
  },

  // Case Summary & Statistics (NEW - using backend API)
  async getCaseSummary() {
    const response = await api.get("/cases/summary/");
    return response.data;
  },

  async getCaseSummaryStatistics(params = {}) {
    const response = await api.get("/cases/summary/statistics/", { params });
    return response.data;
  },

  async getCaseSummaryList(params = {}) {
    const response = await api.get("/cases/summary/list/", { params });
    return response.data;
  },

  async exportCaseSummary(options: {
    format?: 'json' | 'csv';
    include_statistics?: boolean;
    include_details?: boolean;
    department?: string;
    date_from?: string;
    date_to?: string;
    status?: string;
  } = {}) {
    const response = await api.post("/cases/summary/export/", options, {
      responseType: options.format === 'csv' ? 'blob' : 'json'
    });
    return response;
  },

  // ========================================================================
  // INSTRUCTOR CASE FEATURES
  // ========================================================================

  /**
   * Create a new instructor template case (auto-approved, public by default)
   * Accessible only by instructors via IsInstructorPermission
   */
  async createInstructorCase(caseData: CreateInstructorCaseRequest): Promise<InstructorCase> {
    const response = await api.post("/cases/instructor/", caseData);
    return response.data;
  },

  /**
   * Clone a case (for any public approved case)
   * Creates a deep copy with medical sections and attachments
   * Sets cloned_from to original case ID
   */
  async cloneCase(caseId: string | number, cloneData?: CloneCaseRequest): Promise<CloneCaseResponse> {
    const response = await api.post(`/cases/${caseId}/clone/`, cloneData || {});
    return response.data;
  },

  /**
   * Get instructor case audit logs
   * Shows who changed the template, what changed, and when
   */
  async getInstructorCaseAuditLogs(caseId?: string | number): Promise<InstructorCaseAuditLog[]> {
    if (caseId) {
      const response = await api.get(`/cases/${caseId}/audit/`);
      return response.data;
    }
    // Get all audit logs for all instructor cases
    const response = await api.get("/instructor-cases/audit/");
    return response.data;
  },

  /**
   * Get a specific audit log entry
   */
  async getAuditLogDetail(auditId: string | number): Promise<InstructorCaseAuditLog> {
    const response = await api.get(`/instructor-cases/audit/${auditId}/`);
    return response.data;
  },
};
