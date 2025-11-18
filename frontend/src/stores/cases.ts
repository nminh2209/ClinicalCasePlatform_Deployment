import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { casesService } from "@/services/cases";

export const useCasesStore = defineStore("cases", () => {
  const cases = ref<any[]>([]);
  const currentCase = ref<any>(null);
  const loading = ref(false);
  const error = ref(null);
  const pagination = ref({
    count: 0,
    next: null,
    previous: null,
    current_page: 1,
    total_pages: 1,
  });

  const draftCases = computed(() =>
    cases.value.filter((c) => c.case_status === "draft")
  );

  const submittedCases = computed(() =>
    cases.value.filter((c) => c.case_status === "submitted")
  );

  const reviewedCases = computed(() =>
    cases.value.filter((c) => c.case_status === "reviewed")
  );

  async function fetchCases(filters = {}) {
    loading.value = true;
    error.value = null;
    try {
      const response = await casesService.getCases(filters);
      if (response.results) {
        // Paginated response
        cases.value = response.results;
        pagination.value = {
          count: response.count,
          next: response.next,
          previous: response.previous,
          current_page: Math.ceil(response.count / 20) || 1,
          total_pages: Math.ceil(response.count / 20) || 1,
        };
      } else {
        // Simple array response
        cases.value = response;
      }
    } catch (err: any) {
      error.value = err.response?.data?.message || "Failed to fetch cases";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function fetchCase(id: string) {
    loading.value = true;
    error.value = null;
    try {
      currentCase.value = await casesService.getCase(id);
    } catch (err: any) {
      error.value = err.response?.data?.message || "Failed to fetch case";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function createCase(caseData: any) {
    loading.value = true;
    error.value = null;
    try {
      const newCase = await casesService.createCase(caseData);
      cases.value.unshift(newCase);
      return newCase;
    } catch (err: any) {
      error.value = err.response?.data?.message || "Failed to create case";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function updateCase(id: string, caseData: any) {
    loading.value = true;
    error.value = null;
    try {
      const updatedCase = await casesService.updateCase(id, caseData);
      const index = cases.value.findIndex((c) => c.id === id);
      if (index !== -1) {
        cases.value[index] = updatedCase;
      }
      if (currentCase.value?.id === id) {
        currentCase.value = updatedCase;
      }
      return updatedCase;
    } catch (err: any) {
      error.value = err.response?.data?.message || "Failed to update case";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function deleteCase(id: string) {
    loading.value = true;
    error.value = null;
    try {
      await casesService.deleteCase(id);
      const index = cases.value.findIndex((c) => c.id === id);
      if (index !== -1) {
        cases.value.splice(index, 1);
      }
    } catch (err: any) {
      error.value = err.response?.data?.message || "Failed to delete case";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function searchCases(query: string) {
    loading.value = true;
    error.value = null;
    try {
      const results = await casesService.searchCases(query);
      cases.value = results.results || results;
      return results;
    } catch (err: any) {
      error.value = err.response?.data?.message || "Search failed";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  function clearError() {
    error.value = null;
  }

  function clearCurrentCase() {
    currentCase.value = null;
  }

  return {
    cases,
    currentCase,
    loading,
    error,
    pagination,
    draftCases,
    submittedCases,
    reviewedCases,
    fetchCases,
    fetchCase,
    createCase,
    updateCase,
    deleteCase,
    searchCases,
    clearError,
    clearCurrentCase,
  };
});
