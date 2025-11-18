import api from "./api";

export const gradesService = {
  /**
   * Get grade for a specific case
   */
  async getGrade(caseId: string) {
    const response = await api.get(`/grades/?case_id=${caseId}`);
    return response.data.results?.[0] || null;
  },

  /**
   * Save grade (draft) without finalizing
   */
  async saveGrade(gradeData: any) {
    const response = await api.post("/grades/", {
      ...gradeData,
      is_final: false,
    });
    return response.data;
  },

  /**
   * Submit grade (finalized) - student will see this
   */
  async submitGrade(gradeData: any) {
    const response = await api.post("/grades/", {
      ...gradeData,
      is_final: true,
    });
    return response.data;
  },

  /**
   * Update existing grade
   */
  async updateGrade(gradeId: string, gradeData: any) {
    const response = await api.patch(`/grades/${gradeId}/`, gradeData);
    return response.data;
  },

  /**
   * Get all grades for an instructor
   */
  async getInstructorGrades() {
    const response = await api.get("/grades/");
    return response.data.results;
  },

  /**
   * Get all grades for a student
   */
  async getStudentGrades() {
    const response = await api.get("/grades/?student=me");
    return response.data.results;
  },
};
