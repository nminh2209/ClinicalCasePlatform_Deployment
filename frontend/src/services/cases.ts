import api from "./api";

export const casesService = {
  async getCases(params = {}) {
    const response = await api.get("/cases/", { params });
    return response.data;
  },

  async getCase(id: string) {
    const response = await api.get(`/cases/${id}/`);
    const caseData = response.data;

    // Fetch medical attachments for this case
    try {
      const attachmentsResponse = await api.get(`/cases/${id}/attachments/`);
      caseData.medical_attachments = attachmentsResponse.data;
    } catch (error) {
      console.warn("Failed to fetch medical attachments:", error);
      caseData.medical_attachments = [];
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
      // Return the first note if available, or null
      return response.data.length > 0 ? response.data[0] : null;
    } catch (error) {
      console.warn("Failed to fetch student notes:", error);
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

  async getCaseSummary() {
    const response = await api.get("/cases/summary/");
    return response.data;
  },
};
