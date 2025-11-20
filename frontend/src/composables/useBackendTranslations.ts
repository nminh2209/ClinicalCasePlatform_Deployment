import { useI18n } from "vue-i18n";

/**
 * Provides dynamic translation for backend-provided values
 * Maps backend values to i18n keys and falls back to original value if not found
 */
export function useBackendTranslations() {
  const { t, locale } = useI18n();

  // Mapping of backend values to translation keys
  const backendTranslationMap: Record<string, Record<string, string>> = {
    specialty: {
      Cardiology: "createCase.cardiology",
      Neurology: "createCase.neurology",
      Orthopedics: "createCase.orthopedics",
      Pediatrics: "createCase.pediatrics",
      Gastroenterology: "createCase.gastroenterology",
      Respiratory: "createCase.respiratory",
      Emergency: "createCase.emergency",
      Surgery: "createCase.surgery",
      "Internal Medicine": "createCase.internalMedicine",
    },
    department: {
      Cardiology: "createCase.cardiology",
      Neurology: "createCase.neurology",
      Orthopedics: "createCase.orthopedics",
      Pediatrics: "createCase.pediatrics",
      Gastroenterology: "createCase.gastroenterology",
      Respiratory: "createCase.respiratory",
      Emergency: "createCase.emergency",
      Surgery: "createCase.surgery",
      "Internal Medicine": "createCase.internalMedicine",
    },
  };

  /**
   * Translate specialty values from backend
   */
  const translateSpecialty = (value: string | null | undefined): string => {
    if (!value) return "";

    // Check if value exists in mapping
    const key = backendTranslationMap.specialty?.[value];
    if (key) {
      try {
        return t(key as any);
      } catch {
        return value;
      }
    }

    // Fallback: try to match by lowercase
    const lowerValue = value.toLowerCase();
    const specialtyMap = backendTranslationMap.specialty || {};
    for (const [mapKey, mapKeyPath] of Object.entries(specialtyMap)) {
      if (mapKey.toLowerCase() === lowerValue) {
        try {
          return t(mapKeyPath as any);
        } catch {
          return value;
        }
      }
    }

    return value;
  };

  /**
   * Translate department values from backend
   */
  const translateDepartment = (value: string | null | undefined): string => {
    if (!value) return "";

    // Check if value exists in mapping
    const key = backendTranslationMap.department?.[value];
    if (key) {
      try {
        return t(key as any);
      } catch {
        return value;
      }
    }

    // Fallback: try to match by lowercase
    const lowerValue = value.toLowerCase();
    const departmentMap = backendTranslationMap.department || {};
    for (const [mapKey, mapKeyPath] of Object.entries(departmentMap)) {
      if (mapKey.toLowerCase() === lowerValue) {
        try {
          return t(mapKeyPath as any);
        } catch {
          return value;
        }
      }
    }

    return value;
  };

  /**
   * Register a new backend value translation mapping
   */
  const registerMapping = (
    category: "specialty" | "department" | string,
    backendValue: string,
    translationKey: string
  ) => {
    if (!backendTranslationMap[category]) {
      backendTranslationMap[category] = {};
    }
    backendTranslationMap[category][backendValue] = translationKey;
  };

  return {
    translateSpecialty,
    translateDepartment,
    registerMapping,
    locale,
  };
}
