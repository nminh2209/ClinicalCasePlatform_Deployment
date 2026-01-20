<template>
  <div class="fixed inset-0 bg-black/50 z-50 overflow-y-auto">
    <div class="min-h-screen p-4 md:p-6 flex items-center justify-center">
      <div class="max-w-4xl w-full">
        <Card class="bg-white">
          <!-- Instructor Template Banner -->
          <div
            v-if="isInstructor"
            class="bg-amber-50 border-b border-amber-200 px-6 py-3"
          >
            <div class="flex items-center gap-2 text-amber-800">
              <span class="text-lg">📚</span>
              <span class="font-medium">Đang tạo Hồ sơ mẫu (Template)</span>
              <span class="text-sm text-amber-600"
                >- Hồ sơ sẽ được phê duyệt tự động và công khai cho sinh
                viên</span
              >
            </div>
          </div>

          <CardHeader class="border-b">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div
                  :class="[
                    'w-10 h-10 rounded-lg flex items-center justify-center',
                    isInstructor ? 'bg-amber-100' : 'bg-blue-100',
                  ]"
                >
                  <component
                    :is="steps[currentStep]?.icon"
                    :class="[
                      'w-5 h-5',
                      isInstructor ? 'text-amber-600' : 'text-blue-600',
                    ]"
                  />
                </div>
                <div>
                  <CardTitle>{{ steps[currentStep]?.title }}</CardTitle>
                  <CardDescription>
                    {{ t("wizard.step") }} {{ currentStep + 1 }}/{{
                      steps.length
                    }}</CardDescription
                  >
                </div>
              </div>
              <Button variant="ghost" size="sm" @click="$emit('close')">
                <X class="h-4 w-4" />
              </Button>
            </div>

            <!-- Clickable Step Navigation -->
            <div class="mt-4">
              <div class="flex gap-2">
                <button
                  v-for="(step, index) in steps"
                  :key="step.id"
                  @click="currentStep = index"
                  :class="`h-10 flex-1 rounded-lg transition-all flex items-center justify-center gap-2 ${
                    currentStep === index
                      ? isInstructor
                        ? 'bg-amber-500 text-white shadow-md'
                        : 'bg-blue-500 text-white shadow-md'
                      : currentStep > index
                      ? 'bg-green-500 text-white hover:bg-green-600'
                      : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
                  }`"
                  :title="step.title"
                >
                  <component :is="step.icon" class="w-4 h-4" />
                  <span class="text-xs font-medium hidden md:inline">{{
                    index + 1
                  }}</span>
                </button>
              </div>
            </div>
          </CardHeader>

          <CardContent class="p-6">
            <!-- Step Content with max height -->
            <div class="max-h-[calc(100vh-300px)] overflow-y-auto pr-2">
              <component
                :is="currentStepComponent"
                :case-data="caseData"
                :student-department="studentDepartment"
                @update:case-data="updateCaseData"
                @validation-changed="onValidationChanged"
                ref="currentStepRef"
              />
            </div>

            <!-- Navigation Buttons -->
            <div class="flex items-center justify-between mt-6 pt-6 border-t">
              <Button
                v-if="!isInstructor"
                variant="outline"
                size="sm"
                @click="handleSaveDraft"
              >
                <Save class="h-4 w-4 mr-2" />
                {{ t("wizard.saveDraft") }}
              </Button>

              <div class="flex gap-2">
                <Button
                  v-if="currentStep > 0"
                  variant="outline"
                  @click="handleBack"
                >
                  <ArrowLeft class="h-4 w-4 mr-2" />
                  {{ t("wizard.back") }}
                </Button>

                <Button
                  class="text-white"
                  v-if="currentStep < steps.length - 1"
                  @click="handleNext"
                  :disabled="stepValidations[currentStep] === false"
                >
                  {{ t("wizard.next") }}
                  <ArrowRight class="h-4 w-4 ml-2" />
                </Button>
                <Button
                  v-else
                  @click="handleComplete"
                  :class="
                    isInstructor
                      ? 'text-white bg-amber-600 hover:bg-amber-700'
                      : 'text-white bg-green-600 hover:bg-green-700'
                  "
                  :disabled="stepValidations[currentStep] === false"
                >
                  <CheckCircle class="text-white h-4 w-4 mr-2" />
                  {{
                    isInstructor ? "📚 Tạo hồ sơ mẫu" : t("wizard.createCase")
                  }}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineAsyncComponent } from "vue";
import { useI18n } from "vue-i18n";
import { useToast } from "@/composables/useToast";
import Card from "@/components/ui/Card.vue";
import CardContent from "@/components/ui/CardContent.vue";
import CardDescription from "@/components/ui/CardDescription.vue";
import CardHeader from "@/components/ui/CardHeader.vue";
import CardTitle from "@/components/ui/CardTitle.vue";
import Button from "@/components/ui/Button.vue";
import X from "@/components/icons/X.vue";
import {
  ArrowLeft,
  ArrowRight,
  Save,
  CheckCircle,
  User,
  FileText,
  Activity,
  FlaskConical,
  Paperclip,
  Sparkles,
  FileSearch,
} from "@/components/icons";
import { Stethoscope } from "lucide-vue-next";
import api from "@/services/api";
import { casesService } from "@/services/cases";
import { useAuthStore } from "@/stores/auth";
import { onMounted } from "vue";

const props = defineProps({
  studentDepartment: {
    type: String,
    required: true,
  },
  caseId: {
    type: String,
    default: null,
  },
});

const emit = defineEmits(["close", "complete"]);

const { toast } = useToast();
const { t } = useI18n();
const authStore = useAuthStore();

// Check if user is instructor - they create templates instead of regular cases
const isInstructor = computed(() => authStore.user?.role === "instructor");

const currentStep = ref(0); // Start at 0 for template selection
const selectedTemplate = ref(null);
const currentStepRef = ref(null);
const stepValidations = ref<Record<number, boolean>>({});

const caseData = ref<Record<string, any>>({
  // Case Basic Fields (from Case model)
  title: "",
  patient_name: "",
  repository: null,
  specialty: "",
  priority_level: "medium",
  complexity_level: "intermediate",
  patient_age: null,
  patient_gender: "",
  medical_record_number: "",
  admission_date: null,
  discharge_date: null,
  case_summary: "",
  chief_complaint_brief: "",
  keywords: "",
  learning_tags: "",
  patient_ethnicity: "",
  patient_occupation: "",
  estimated_study_hours: null,
  requires_follow_up: false,
  follow_up_date: null,

  // ClinicalHistory (OneToOne)
  clinical_history: {
    chief_complaint: "",
    history_present_illness: "",
    past_medical_history: "",
    family_history: "",
    social_history: "",
    medications: "",
    allergies: "",
    immunizations: "",
    surgical_history: "",
    review_of_systems: "",
    symptom_duration_days: null,
    symptom_onset: "",
    symptom_progression: "",
    review_systems: "",
  },

  // PhysicalExamination (OneToOne)
  physical_examination: {
    general_appearance: "",
    consciousness_level: "alert",
    vital_signs: "",
    vital_signs_bp: "",
    vital_signs_hr: null,
    vital_signs_rr: null,
    vital_signs_temp: null,
    vital_signs_spo2: null,
    weight_kg: null,
    height_cm: null,
    bmi: null,
    head_neck: "",
    cardiovascular: "",
    respiratory: "",
    abdominal: "",
    neurological: "",
    musculoskeletal: "",
    skin: "",
    other_systems: "",
  },

  // Investigations (OneToOne as investigations_detail)
  detailed_investigations: {
    laboratory_results: "",
    hemoglobin_level: null,
    white_cell_count: null,
    platelet_count: null,
    sodium_level: null,
    potassium_level: null,
    glucose_level: null,
    creatinine_level: null,
    imaging_studies: "",
    ecg_findings: "",
    ecg_rhythm: "",
    ecg_rate: null,
    pathology_results: "",
    microbiology_results: "",
    other_investigations: "",
    arterial_blood_gas: "",
    ph_level: null,
    special_tests: "",
    microbiology: "",
    biochemistry: "",
    hematology: "",
  },

  // DiagnosisManagement (OneToOne)
  diagnosis_management: {
    primary_diagnosis: "",
    differential_diagnosis: "",
    icd10_codes: "",
    treatment_plan: "",
    medications_prescribed: "",
    procedures_performed: "",
    follow_up_plan: "",
    prognosis: "",
    complications: "",
  },

  // LearningOutcomes (OneToOne)
  learning_outcomes: {
    learning_objectives: "",
    key_concepts: "",
    clinical_pearls: "",
    references: "",
    discussion_points: "",
    assessment_criteria: "",
  },

  // Medical attachments (will be uploaded separately)
  attachments: [],
});

const steps = computed(() => [
  {
    id: 0,
    title: t("wizard.attachmentsStep"),
    icon: Paperclip,
    description: t("wizard.attachmentsDesc"),
  },
  {
    id: 1,
    title: t("wizard.basicInfo"),
    icon: User,
    description: t("wizard.basicInfoDesc"),
  },
  {
    id: 2,
    title: t("wizard.vitalSigns"),
    icon: Activity,
    description: t("wizard.vitalSignsDesc"),
  },
  {
    id: 3,
    title: t("wizard.physicalExam"),
    icon: Stethoscope,
    description: t("wizard.physicalExamDesc"),
  },
  {
    id: 4,
    title: t("wizard.diagnosticWorkup"),
    icon: FlaskConical,
    description: t("wizard.diagnosticWorkupDesc"),
  },
  {
    id: 5,
    title: t("wizard.assessmentPlan"),
    icon: FileText,
    description: t("wizard.assessmentPlanDesc"),
  },
  {
    id: 6,
    title: "OCR",
    icon: FileSearch,
    description: "Xem bảng và hình ảnh đã trích xuất",
  },
]);

const currentStepComponent = computed(() => {
  switch (currentStep.value) {
    case 0:
      return AttachmentsStep; // First: upload documents for OCR autofill
    case 1:
      return BasicInfoStep;
    case 2:
      return VitalSignsStep;
    case 3:
      return PhysicalExamStep;
    case 4:
      return DiagnosticWorkupStep;
    case 5:
      return AssessmentPlanStep;
    case 6:
      return OCRResultsStep; // New: view extracted tables/images
    default:
      return null;
  }
});

// Lazy load step components
const AttachmentsStep = defineAsyncComponent(
  () => import("./CreateCaseWizard/AttachmentsStep.vue")
);
const BasicInfoStep = defineAsyncComponent(
  () => import("./CreateCaseWizard/BasicInfoStep.vue")
);
const VitalSignsStep = defineAsyncComponent(
  () => import("./CreateCaseWizard/VitalSignsStep.vue")
);
const PhysicalExamStep = defineAsyncComponent(
  () => import("./CreateCaseWizard/PhysicalExamStep.vue")
);
const DiagnosticWorkupStep = defineAsyncComponent(
  () => import("./CreateCaseWizard/DiagnosticWorkupStep.vue")
);
const AssessmentPlanStep = defineAsyncComponent(
  () => import("./CreateCaseWizard/AssessmentPlanStep.vue")
);
const OCRResultsStep = defineAsyncComponent(
  () => import("./CreateCaseWizard/OCRResultsStep.vue")
);

const updateField = (field: keyof typeof caseData.value, value: any) => {
  caseData.value[field] = value;
};

const handleNext = () => {
  // Check if current step is valid
  const isValid = stepValidations.value[currentStep.value] !== false;
  if (!isValid) {
    toast.error(t("wizard.completionRequired"));
    return;
  }

  if (currentStep.value < steps.value.length - 1) {
    currentStep.value++;
  }
};

const handleBack = () => {
  if (currentStep.value > 0) {
    currentStep.value--;
  }
};

const handleStepClick = (stepIndex: number) => {
  // Allow navigation to any step
  currentStep.value = stepIndex;
};

// Load existing case data if editing
onMounted(async () => {
  if (props.caseId) {
    try {
      const existingCase = await casesService.getCase(props.caseId);
      console.log("Loading existing case:", existingCase);

      // Populate all fields from existing case
      Object.assign(caseData.value, {
        title: existingCase.title || "",
        patient_name: existingCase.patient_name || "",
        repository: existingCase.repository || null,
        specialty: existingCase.specialty || "",
        complexity_level: existingCase.complexity_level || "intermediate",
        patient_age: existingCase.patient_age || null,
        patient_gender: existingCase.patient_gender || "",
        medical_record_number: existingCase.medical_record_number || "",
        admission_date: existingCase.admission_date || null,
        discharge_date: existingCase.discharge_date || null,
        case_summary: existingCase.case_summary || "",
        chief_complaint_brief: existingCase.chief_complaint_brief || "",
        keywords: existingCase.keywords || "",
        patient_ethnicity: existingCase.patient_ethnicity || "",
        patient_occupation: existingCase.patient_occupation || "",
        estimated_study_hours: existingCase.estimated_study_hours || null,
        requires_follow_up: existingCase.requires_follow_up || false,
        follow_up_date: existingCase.follow_up_date || null,
        learning_tags: existingCase.learning_tags || "",
        template: existingCase.template || null,
      });

      if (existingCase.template) {
        selectedTemplate.value = existingCase.template;
      }

      // Load nested models
      if (existingCase.clinical_history) {
        Object.assign(
          caseData.value.clinical_history,
          existingCase.clinical_history
        );
      }
      if (existingCase.physical_examination) {
        Object.assign(
          caseData.value.physical_examination,
          existingCase.physical_examination
        );
      }
      if (existingCase.detailed_investigations) {
        Object.assign(
          caseData.value.detailed_investigations,
          existingCase.detailed_investigations
        );
      }
      if (existingCase.diagnosis_management) {
        Object.assign(
          caseData.value.diagnosis_management,
          existingCase.diagnosis_management
        );
      }
      if (existingCase.learning_outcomes) {
        Object.assign(
          caseData.value.learning_outcomes,
          existingCase.learning_outcomes
        );
      }

      console.log("Case data loaded successfully");
    } catch (error) {
      console.error("Error loading case:", error);
      toast.error("Không thể tải dữ liệu ca bệnh");
    }
  }
});

const handleSaveDraft = async () => {
  try {
    // Prepare the case data payload with draft status
    const payload = {
      title: caseData.value.title,
      patient_name: caseData.value.patient_name || caseData.value.title,
      repository: caseData.value.repository || 1,
      specialty: caseData.value.specialty,
      complexity_level: caseData.value.complexity_level,
      patient_age: caseData.value.patient_age,
      patient_gender: caseData.value.patient_gender,
      patient_ethnicity: caseData.value.patient_ethnicity,
      patient_occupation: caseData.value.patient_occupation,
      medical_record_number: caseData.value.medical_record_number,
      admission_date: caseData.value.admission_date,
      discharge_date: caseData.value.discharge_date,
      chief_complaint_brief: caseData.value.chief_complaint_brief,
      case_summary: caseData.value.case_summary,
      keywords: caseData.value.keywords,
      learning_tags: caseData.value.learning_tags,
      estimated_study_hours: caseData.value.estimated_study_hours,
      requires_follow_up: caseData.value.requires_follow_up,
      follow_up_date: caseData.value.follow_up_date,
      template: caseData.value.template,
      case_status: "draft", // Explicitly set as draft

      // Nested models
      clinical_history: caseData.value.clinical_history,
      physical_examination: caseData.value.physical_examination,
      detailed_investigations: caseData.value.detailed_investigations,
      diagnosis_management: caseData.value.diagnosis_management,
      learning_outcomes: caseData.value.learning_outcomes,
    };

    let response;

    if (props.caseId) {
      // Update existing draft
      response = await api.put(`/cases/${props.caseId}/`, payload);
      toast.success("Đã cập nhật nháp!");
    } else {
      // Create new draft - check if there are attachments
      const hasAttachments =
        caseData.value.attachments && caseData.value.attachments.length > 0;

      if (hasAttachments) {
        // Use FormData for multipart upload
        const formData = new FormData();
        formData.append("data", JSON.stringify(payload));

        caseData.value.attachments.forEach((file: File, index: number) => {
          formData.append(`attachment_${index}`, file);
        });

        response = await api.post("/cases/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
      } else {
        // Use regular JSON for cases without attachments
        response = await api.post("/cases/", payload);
      }
      toast.success(t("wizard.caseSavedDraft"));
    }

    // Navigate to the case
    setTimeout(() => {
      emit("complete", {
        caseId: response.data.id || props.caseId,
        caseData: response.data,
      });
    }, 500);
  } catch (error: any) {
    console.error("Error saving draft:", error);
    const errorMessage =
      error.response?.data?.message ||
      error.response?.data?.detail ||
      t("wizard.failedToDraft");
    toast.error(errorMessage);
  }
};

const handleComplete = async () => {
  // Check if final step is valid
  const isValid = stepValidations.value[currentStep.value] !== false;
  if (!isValid) {
    toast.error(t("wizard.completeRequired"));
    return;
  }

  try {
    // Helper function to remove empty fields from nested objects
    // Only returns the object if it has non-empty values
    const cleanObject = (obj: any) => {
      if (!obj || typeof obj !== "object") return undefined;

      const cleaned: any = {};
      let hasNonEmptyValue = false;

      for (const [key, value] of Object.entries(obj)) {
        // Skip undefined, null, and empty strings
        if (value === undefined || value === null || value === "") {
          continue;
        }
        // For numbers, keep 0 as valid but skip NaN
        if (typeof value === "number" && isNaN(value)) {
          continue;
        }
        cleaned[key] = value;
        hasNonEmptyValue = true;
      }

      // Only return the object if it has at least one non-empty value
      return hasNonEmptyValue ? cleaned : undefined;
    };

    // Helper function to format date to YYYY-MM-DD or null
    const formatDate = (dateValue: any) => {
      if (!dateValue || dateValue === "") return null;
      // If already in YYYY-MM-DD format, return as-is
      if (
        typeof dateValue === "string" &&
        /^\d{4}-\d{2}-\d{2}$/.test(dateValue)
      ) {
        return dateValue;
      }
      // Try to parse and format
      try {
        const date = new Date(dateValue);
        if (isNaN(date.getTime())) return null;
        return date.toISOString().split("T")[0];
      } catch {
        return null;
      }
    };

    // Prepare the case data payload
    const payload: any = {
      title: caseData.value.title,
      patient_name: caseData.value.patient_name || caseData.value.title, // Use title as fallback
      repository: caseData.value.repository || 1, // Default to repository 1 if not specified
      specialty: caseData.value.specialty,
      complexity_level: caseData.value.complexity_level || "easy", // Use key from complexity levels API
      priority_level: caseData.value.priority_level || "medium", // Use key from priority levels API
      patient_age: caseData.value.patient_age || 25, // Default age if not provided
    };

    // Add optional basic fields only if they have values
    if (caseData.value.template) {
      // If template is an object, extract the ID
      payload.template =
        typeof caseData.value.template === "object"
          ? caseData.value.template.id
          : caseData.value.template;
    }
    if (caseData.value.patient_gender)
      payload.patient_gender = caseData.value.patient_gender;
    if (caseData.value.patient_ethnicity)
      payload.patient_ethnicity = caseData.value.patient_ethnicity;
    if (caseData.value.patient_occupation)
      payload.patient_occupation = caseData.value.patient_occupation;
    if (caseData.value.medical_record_number)
      payload.medical_record_number = caseData.value.medical_record_number;

    // Format dates properly
    const admissionDate = formatDate(caseData.value.admission_date);
    if (admissionDate) payload.admission_date = admissionDate;

    const dischargeDate = formatDate(caseData.value.discharge_date);
    if (dischargeDate) payload.discharge_date = dischargeDate;

    if (caseData.value.chief_complaint_brief)
      payload.chief_complaint_brief = caseData.value.chief_complaint_brief;
    if (caseData.value.case_summary)
      payload.case_summary = caseData.value.case_summary;
    if (caseData.value.keywords) payload.keywords = caseData.value.keywords;
    if (caseData.value.learning_tags)
      payload.learning_tags = caseData.value.learning_tags;
    if (caseData.value.estimated_study_hours)
      payload.estimated_study_hours = caseData.value.estimated_study_hours;
    if (caseData.value.requires_follow_up !== undefined)
      payload.requires_follow_up = caseData.value.requires_follow_up;

    const followUpDate = formatDate(caseData.value.follow_up_date);
    if (followUpDate) payload.follow_up_date = followUpDate;

    // Add nested models only if they have data
    const cleanedClinicalHistory = cleanObject(caseData.value.clinical_history);
    if (cleanedClinicalHistory)
      payload.clinical_history = cleanedClinicalHistory;

    const cleanedPhysicalExam = cleanObject(
      caseData.value.physical_examination
    );
    if (cleanedPhysicalExam) {
      // Ensure consciousness_level is a valid choice (alert, drowsy, stupor, coma)
      if (
        cleanedPhysicalExam.consciousness_level &&
        !["alert", "drowsy", "stupor", "coma"].includes(
          cleanedPhysicalExam.consciousness_level
        )
      ) {
        cleanedPhysicalExam.consciousness_level = "alert"; // Default to alert
      }
      payload.physical_examination = cleanedPhysicalExam;
    }

    const cleanedInvestigations = cleanObject(
      caseData.value.detailed_investigations
    );
    if (cleanedInvestigations)
      payload.detailed_investigations = cleanedInvestigations;

    const cleanedDiagnosis = cleanObject(caseData.value.diagnosis_management);
    if (cleanedDiagnosis) payload.diagnosis_management = cleanedDiagnosis;

    const cleanedLearning = cleanObject(caseData.value.learning_outcomes);
    if (cleanedLearning) payload.learning_outcomes = cleanedLearning;

    console.log("=== CASE CREATION PAYLOAD ===");
    console.log("Full payload:", JSON.stringify(payload, null, 2));
    console.log("Is instructor template:", isInstructor.value);
    console.log("=== END PAYLOAD ===");

    // Determine API endpoint based on user role
    // Instructors create templates via /cases/instructor/ endpoint
    const apiEndpoint = isInstructor.value ? "/cases/instructor/" : "/cases/";

    // Check if there are attachments
    const hasAttachments =
      caseData.value.attachments && caseData.value.attachments.length > 0;

    let response;
    if (hasAttachments) {
      // Use FormData for multipart upload
      const formData = new FormData();
      formData.append("data", JSON.stringify(payload));

      caseData.value.attachments.forEach((file: File, index: number) => {
        formData.append(`attachment_${index}`, file);
      });

      response = await api.post(apiEndpoint, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
    } else {
      // Use regular JSON for cases without attachments
      response = await api.post(apiEndpoint, payload);
    }

    // For instructor templates, the backend auto-publishes to feed
    // Show appropriate success message
    if (isInstructor.value) {
      toast.success("Đã tạo và xuất bản hồ sơ mẫu thành công!");
    } else {
      toast.success(t("wizard.caseCreated"));
    }

    // Navigate to the new case
    setTimeout(() => {
      emit("complete", { caseId: response.data.id, caseData: response.data });
    }, 500);
  } catch (error: any) {
    console.error("Error creating case:", error);
    console.error("Error response:", error.response?.data);
    console.error("Error status:", error.response?.status);

    // Map backend field names to i18n translation keys
    const fieldToI18nKey: Record<string, string> = {
      title: "createCase.caseTitle",
      patient_name: "createCase.firstName",
      patient_age: "createCase.age",
      patient_gender: "createCase.gender",
      specialty: "createCase.specialty",
      repository: "common.repository",
      clinical_history: "createCase.clinicalPresentation",
      chief_complaint: "createCase.chief_complaint",
      history_present_illness: "createCase.historyOfPresentIllness",
      past_medical_history: "createCase.pastMedicalHistory",
      physical_examination: "createCase.physicalExamination",
      general_appearance: "createCase.generalAppearance",
      vital_signs: "createCase.vitalSigns",
      detailed_investigations: "createCase.diagnosticWorkup",
      diagnosis_management: "wizard.assessmentPlan",
      primary_diagnosis: "createCase.primaryDiagnosis",
      treatment_plan: "createCase.treatmentPlan",
      learning_outcomes: "createCase.learningOutcomes",
      complexity_level: "createCase.complexity",
    };

    // Map common DRF error messages to i18n keys (fallback to simple translation)
    const errorMessages: Record<string, string> = {
      "This field is required.": t(
        "common.fieldRequired",
        "This field is required"
      ),
      "This field may not be blank.": t(
        "common.fieldRequired",
        "This field is required"
      ),
      "This field may not be null.": t(
        "common.fieldRequired",
        "This field is required"
      ),
      "A valid integer is required.": t(
        "common.invalidNumber",
        "Please enter a valid number"
      ),
      "Enter a valid date.": t(
        "common.invalidDate",
        "Please enter a valid date"
      ),
    };

    // Helper to translate field name using i18n
    const translateField = (field: string): string => {
      const i18nKey = fieldToI18nKey[field];
      if (i18nKey) {
        return t(i18nKey, field.replace(/_/g, " "));
      }
      return field.replace(/_/g, " ");
    };

    // Helper to translate error message
    const translateError = (msg: string): string => {
      return errorMessages[msg] || msg;
    };

    // Helper to format nested errors
    const formatNestedErrors = (
      errors: any,
      parentField: string = ""
    ): string[] => {
      const messages: string[] = [];

      for (const [field, value] of Object.entries(errors)) {
        const fullField = parentField ? `${parentField}.${field}` : field;
        const fieldName = translateField(field);

        if (Array.isArray(value)) {
          // Simple array of error messages
          const errorMsg = translateError(value[0]);
          messages.push(`${fieldName}: ${errorMsg}`);
        } else if (typeof value === "object" && value !== null) {
          // Nested object - recurse
          const nestedMessages = formatNestedErrors(value, fullField);
          messages.push(...nestedMessages);
        } else if (typeof value === "string") {
          const errorMsg = translateError(value);
          messages.push(`${fieldName}: ${errorMsg}`);
        }
      }

      return messages;
    };

    // Display detailed error information
    let errorMessage = t("wizard.failedToCreate");

    if (error.response?.data) {
      // Log the full error object to see all validation errors
      console.error(
        "Full error object: ",
        JSON.stringify(error.response.data, null, 2)
      );

      // If there's a specific error message
      if (error.response.data.message) {
        errorMessage = error.response.data.message;
      } else if (error.response.data.detail) {
        errorMessage = error.response.data.detail;
      } else {
        // Format field-specific errors
        const errors = error.response.data;
        const formattedErrors = formatNestedErrors(errors);

        if (formattedErrors.length > 0) {
          // Show first error in toast, log all
          errorMessage = formattedErrors[0] || "";
          if (formattedErrors.length > 1) {
            console.error("All validation errors:", formattedErrors);
          }
        }
      }
    }

    toast.error(errorMessage);
  }
};

const updateCaseData = (newData: Partial<typeof caseData.value>) => {
  caseData.value = { ...caseData.value, ...newData };
};

const onValidationChanged = (isValid: boolean) => {
  stepValidations.value[currentStep.value] = isValid;
};

// Provide reactive data to child components
defineExpose({
  caseData,
  updateField,
  studentDepartment: props.studentDepartment,
});
</script>
