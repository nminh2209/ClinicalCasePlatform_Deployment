import { ref } from "vue";
import api from "@/services/api";
import axios from "axios";

// Define the expected shape of a case template matching backend structure
export interface CaseTemplate {
  id: string | number;
  name: string;
  vietnamese_name?: string;
  description?: string;
  specialty?: string;
  created_by_name?: string;
  department_name?: string;
  department_vietnamese_name?: string;
  is_standard?: boolean;
  is_active?: boolean;
  created_at?: string;
  fields_schema?: {
    sections?: string[];
    required_fields?: string[];
  };
}

export function useCaseTemplates() {
  const caseTemplates = ref<CaseTemplate[]>([]);
  const loading = ref(false);
  const error = ref(null);

  const fetchCaseTemplates = async () => {
    loading.value = true;
    error.value = null;

    try {
      const response = await api.get("/templates/");

      // Backend returns paginated data with 'results' array
      caseTemplates.value = response.data.results || response.data;
      console.log(`✅ Successfully loaded ${caseTemplates.value.length} templates:`, caseTemplates.value);
    } catch (err: any) {
      error.value = err.message || "Failed to fetch case templates";

      if (err.response?.status === 404) {
        console.error("404 Error: This endpoint does not exist");
      } else if (err.code === 'ERR_NETWORK') {
        console.error("Network Error: Server may not be running");
      }
      
      caseTemplates.value = []; // Clear on error
    } finally {
      loading.value = false;
    }
  };

  const getTemplateById = (id: string) => {
    return caseTemplates.value.find((template) => template.id === id);
  };

  return {
    caseTemplates,
    loading,
    error,
    fetchCaseTemplates,
    getTemplateById,
  };
}
