// frontend/src/composables/useChoices.ts
/**
 * Composable for fetching and managing dynamic choices from backend
 * Replaces hardcoded dropdowns with database-driven values
 */

import { ref, onMounted } from "vue";
import api from "@/services/api";

interface Specialty {
  id: number;
  name: string;
  english_name: string;
  description: string;
}

interface PriorityLevel {
  id: number;
  name: string;
  key: string;
  color: string;
}

interface ComplexityLevel {
  id: number;
  name: string;
  key: string;
  description: string;
}

interface GenderChoice {
  key: string;
  label: string;
}

interface StatusChoice {
  key: string;
  label: string;
}

interface AllChoices {
  specialties: Specialty[];
  priorities: PriorityLevel[];
  complexities: ComplexityLevel[];
}

// Singleton cache to avoid multiple API calls
let cachedChoices: AllChoices | null = null;
let cachePromise: Promise<AllChoices> | null = null;
let staleRetryCount = 0;
const MAX_STALE_RETRIES = 2;

export function useChoices() {
  const specialties = ref<Specialty[]>([]);
  const priorities = ref<PriorityLevel[]>([]);
  const complexities = ref<ComplexityLevel[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Hardcoded gender choices (stable, rarely change)
  const genders = ref<GenderChoice[]>([
    { key: "male", label: "Nam" },
    { key: "female", label: "Nữ" },
    { key: "other", label: "Khác" },
    { key: "not_specified", label: "Không xác định" },
  ]);

  // Hardcoded status choices (defined by business logic)
  const statuses = ref<StatusChoice[]>([
    { key: "draft", label: "Bản nháp" },
    { key: "submitted", label: "Đã nộp" },
    { key: "reviewed", label: "Đã xem xét" },
    { key: "approved", label: "Đã phê duyệt" },
  ]);

  const fetchChoices = async (): Promise<AllChoices> => {
    // Return cached data if available and non-empty
    if (cachedChoices) {
      if (
        cachedChoices.priorities.length === 0 ||
        cachedChoices.complexities.length === 0
      ) {
        // Detected stale/empty cache. Retry max N times, then give up
        if (staleRetryCount >= MAX_STALE_RETRIES) {
          console.warn(
            `Stale cache detected after ${MAX_STALE_RETRIES} retries. Returning empty data.`
          );
          return cachedChoices; // Return as-is instead of infinite loop
        }
        staleRetryCount++;
        cachedChoices = null;
        cachePromise = null; // Explicitly clear to force fresh fetch
      } else {
        staleRetryCount = 0; // Reset on success
        specialties.value = cachedChoices.specialties;
        priorities.value = cachedChoices.priorities;
        complexities.value = cachedChoices.complexities;
        return cachedChoices;
      }
    }

    // Return pending promise if already fetching
    if (cachePromise) {
      return cachePromise;
    }

    loading.value = true;
    error.value = null;

    cachePromise = Promise.allSettled([
      api.get("/cases/specialties/all_choices/"),
      api.get("/cases/priority-levels/"),
      api.get("/cases/complexity-levels/"),
    ])
      .then((results) => {
        const specialtiesRes =
          results[0].status === "fulfilled" ? results[0].value : null;
        const prioritiesRes =
          results[1].status === "fulfilled" ? results[1].value : null;
        const complexitiesRes =
          results[2].status === "fulfilled" ? results[2].value : null;

        if (!specialtiesRes || !prioritiesRes || !complexitiesRes) {
          console.warn("Choices API partial failure:", {
            specialties: results[0].status,
            priorities: results[1].status,
            complexities: results[2].status,
          });
        }

        const specialtiesData = specialtiesRes
          ? Array.isArray(specialtiesRes.data)
            ? specialtiesRes.data
            : specialtiesRes.data.results || []
          : [];
        const prioritiesData = prioritiesRes
          ? Array.isArray(prioritiesRes.data)
            ? prioritiesRes.data
            : prioritiesRes.data.results || []
          : [];
        const complexitiesData = complexitiesRes
          ? Array.isArray(complexitiesRes.data)
            ? complexitiesRes.data
            : complexitiesRes.data.results || []
          : [];

        // Deep clone to prevent external mutations of cached data
        const data: AllChoices = {
          specialties: structuredClone(specialtiesData.filter(Boolean)),
          priorities: structuredClone(prioritiesData.filter(Boolean)),
          complexities: structuredClone(complexitiesData.filter(Boolean)),
        };

        staleRetryCount = 0; // Reset retry count on success
        cachedChoices = data;
        specialties.value = data.specialties;
        priorities.value = data.priorities;
        complexities.value = data.complexities;
        console.log("Choices loaded:", {
          specialties: data.specialties.length,
          priorities: data.priorities.length,
          complexities: data.complexities.length,
        });
        return data;
      })
      .catch((err) => {
        error.value = "Không thể tải danh sách lựa chọn";
        console.error("Failed to fetch choices:", err);
        // Explicitly clear promise & cache on error to prevent promise leak
        cachePromise = null;
        cachedChoices = null;
        staleRetryCount = 0;
        throw err;
      })
      .finally(() => {
        loading.value = false;
      });

    return cachePromise;
  };

  const refresh = async () => {
    cachedChoices = null;
    cachePromise = null;
    await fetchChoices();
  };

  // Format functions - convert keys to labels
  const formatGender = (key: string): string => {
    const gender = genders.value.find((g) => g.key === key);
    return gender?.label || key;
  };

  const formatStatus = (key: string): string => {
    const status = statuses.value.find((s) => s.key === key);
    return status?.label || key;
  };

  const formatPriority = (key: string): string => {
    const priority = priorities.value.find((p) => p.key === key);
    return priority?.name || key;
  };

  const formatComplexity = (key: string): string => {
    const complexity = complexities.value.find((c) => c.key === key);
    return complexity?.name || key;
  };

  // Get priority color for UI styling
  const getPriorityColor = (key: string): string => {
    const priority = priorities.value.find((p) => p.key === key);
    return priority?.color || "gray";
  };

  // Auto-fetch on mount
  onMounted(() => {
    fetchChoices();
  });

  return {
    // Data
    specialties,
    priorities,
    complexities,
    genders,
    statuses,
    loading,
    error,

    // Methods
    fetchChoices,
    refresh,

    // Formatters
    formatGender,
    formatStatus,
    formatPriority,
    formatComplexity,
    getPriorityColor,
  };
}
