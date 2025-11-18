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

    console.log("🔄 Fetching case templates from /api/templates/...");

    try {
      const response = await api.get("/templates/");
        
      // Backend returns paginated data with 'results' array
      caseTemplates.value = response.data.results || response.data;
      console.log(`✅ Successfully loaded ${caseTemplates.value.length} templates:`, caseTemplates.value);
    } catch (err: any) {
      error.value = err.message || "Failed to fetch case templates";
      console.error("❌ Error fetching case templates:");
      console.error("  - Error:", err);
      console.error("  - Status:", err.response?.status);
      console.error("  - URL:", err.config?.url);
      console.error("  - Full URL:", err.config?.baseURL + err.config?.url);
      console.error("  - Response Data:", err.response?.data);
      
      if (err.response?.status === 404) {
        console.error("⚠️ 404 Error: The endpoint /api/templates/ does not exist on the backend");
        console.error("   Check backend URL routing in clinical_case_platform/urls.py");
      } else if (err.code === 'ERR_NETWORK') {
        console.error("⚠️ Network Error: Backend server may not be running");
        console.error("   Make sure Django is running on http://localhost:8000");
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
