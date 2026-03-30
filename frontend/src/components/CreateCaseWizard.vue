<template>
  <div class="fixed inset-0 bg-black/50 z-50 overflow-y-auto">
    <div class="min-h-screen p-4 md:p-6 flex items-center justify-center">
      <div class="max-w-4xl w-full">
        <!-- Instructor Template Banner -->
        <div
          v-if="isInstructor"
          class="bg-amber-50 border border-amber-200 border-b-0 px-6 py-3 rounded-t-xl flex items-center gap-2 text-amber-800"
        >
          <i class="pi pi-star-fill text-amber-500" />
          <span class="font-medium">Đang tạo Hồ sơ mẫu (Template)</span>
          <span class="text-sm text-amber-600">
            - Hồ sơ sẽ được phê duyệt tự động và công khai cho sinh viên
          </span>
        </div>

        <Card
          :pt="{
            root: {
              class: isInstructor ? 'rounded-t-none rounded-b-none' : '',
            },
          }"
        >
          <template #header>
            <div class="px-6 pt-5 pb-4 border-b border-gray-200 rounded">
              <!-- Title row -->
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center gap-3">
                  <div
                    :class="[
                      'w-10 h-10 rounded-lg flex items-center justify-center shrink-0',
                      isInstructor ? 'bg-amber-100' : 'bg-blue-100',
                    ]"
                  >
                    <i
                      :class="[
                        steps[currentStep]?.icon,
                        'text-lg',
                        isInstructor ? 'text-amber-600' : 'text-blue-600',
                      ]"
                    />
                  </div>
                  <div>
                    <div
                      class="font-bold text-gray-800 text-base leading-tight"
                    >
                      {{ steps[currentStep]?.title }}
                    </div>
                    <div class="text-sm text-gray-500">
                      {{ t("wizard.step") }} {{ currentStep + 1 }}/{{
                        steps.length
                      }}
                    </div>
                  </div>
                </div>
                <Button
                  icon="pi pi-times"
                  text
                  rounded
                  severity="secondary"
                  @click="$emit('close')"
                />
              </div>

              <!-- Step navigation -->
              <div class="flex gap-2">
                <button
                  v-for="(step, index) in steps"
                  :key="step.id"
                  type="button"
                  @click="handleStepClick(index)"
                  :title="step.title"
                  :class="[
                    'h-10 flex-1 rounded-lg transition-all flex items-center justify-center gap-1.5 text-xs font-medium',
                    currentStep === index
                      ? isInstructor
                        ? 'bg-amber-500 text-white shadow-md'
                        : 'bg-blue-500 text-white shadow-md'
                      : currentStep > index
                        ? 'bg-green-500 text-white hover:bg-green-600'
                        : 'bg-gray-200 text-gray-600 hover:bg-gray-300',
                  ]"
                >
                  <i :class="[step.icon, 'text-sm']" />
                  <span class="hidden md:inline">{{ index + 1 }}</span>
                </button>
              </div>
            </div>
          </template>

          <template #content>
            <div class="p-6">
              <!-- Step content -->
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

              <!-- Navigation buttons -->
              <div
                class="flex items-center justify-between mt-6 pt-6 border-t border-gray-200"
              >
                <Button
                  v-if="!isInstructor"
                  icon="pi pi-save"
                  :label="t('wizard.saveDraft')"
                  outlined
                  severity="secondary"
                  @click="handleSaveDraft"
                />
                <div v-else />

                <div class="flex gap-2">
                  <Button
                    v-if="currentStep > 0"
                    icon="pi pi-arrow-left"
                    :label="t('wizard.back')"
                    outlined
                    severity="secondary"
                    @click="handleBack"
                  />

                  <Button
                    v-if="currentStep < steps.length - 1"
                    icon-pos="right"
                    icon="pi pi-arrow-right"
                    :label="t('wizard.next')"
                    :disabled="stepValidations[currentStep] === false"
                    @click="handleNext"
                  />

                  <Button
                    v-else
                    icon="pi pi-check-circle"
                    :label="
                      isInstructor ? 'Tạo hồ sơ mẫu' : t('wizard.createCase')
                    "
                    :disabled="stepValidations[currentStep] === false"
                    :class="
                      isInstructor
                        ? 'bg-amber-600 hover:bg-amber-700 border-amber-600'
                        : 'bg-green-600 hover:bg-green-700 border-green-600'
                    "
                    @click="handleComplete"
                  />
                </div>
              </div>
            </div>
          </template>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineAsyncComponent } from "vue";
import { useI18n } from "vue-i18n";
import { useToast } from "@/composables/useToast";
import Card from "primevue/card";
import Button from "primevue/button";
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

const isInstructor = computed(() => authStore.user?.role === "instructor");

const currentStep = ref(0);
const selectedTemplate = ref(null);
const currentStepRef = ref(null);
const stepValidations = ref<Record<number, boolean>>({});

const caseData = ref<Record<string, any>>({
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

  learning_outcomes: {
    learning_objectives: "",
    key_concepts: "",
    clinical_pearls: "",
    references: "",
    discussion_points: "",
    assessment_criteria: "",
  },

  attachments: [],
});

const steps = computed(() => [
  {
    id: 0,
    title: t("wizard.attachmentsStep"),
    icon: "pi pi-paperclip",
    description: t("wizard.attachmentsDesc"),
  },
  {
    id: 1,
    title: t("wizard.basicInfo"),
    icon: "pi pi-user",
    description: t("wizard.basicInfoDesc"),
  },
  {
    id: 2,
    title: t("wizard.vitalSigns"),
    icon: "pi pi-heart",
    description: t("wizard.vitalSignsDesc"),
  },
  {
    id: 3,
    title: t("wizard.physicalExam"),
    icon: "pi pi-search-plus",
    description: t("wizard.physicalExamDesc"),
  },
  {
    id: 4,
    title: t("wizard.diagnosticWorkup"),
    icon: "pi pi-check-circle",
    description: t("wizard.diagnosticWorkupDesc"),
  },
  {
    id: 5,
    title: t("wizard.assessmentPlan"),
    icon: "pi pi-file-edit",
    description: t("wizard.assessmentPlanDesc"),
  },
  {
    id: 6,
    title: "OCR",
    icon: "pi pi-file",
    description: "Xem bảng và hình ảnh đã trích xuất",
  },
]);

// Lazy load step components
const AttachmentsStep = defineAsyncComponent(
  () => import("./CreateCaseWizard/AttachmentsStep.vue"),
);
const BasicInfoStep = defineAsyncComponent(
  () => import("./CreateCaseWizard/BasicInfoStep.vue"),
);
const VitalSignsStep = defineAsyncComponent(
  () => import("./CreateCaseWizard/VitalSignsStep.vue"),
);
const PhysicalExamStep = defineAsyncComponent(
  () => import("./CreateCaseWizard/PhysicalExamStep.vue"),
);
const DiagnosticWorkupStep = defineAsyncComponent(
  () => import("./CreateCaseWizard/DiagnosticWorkupStep.vue"),
);
const AssessmentPlanStep = defineAsyncComponent(
  () => import("./CreateCaseWizard/AssessmentPlanStep.vue"),
);
const OCRResultsStep = defineAsyncComponent(
  () => import("./CreateCaseWizard/OCRResultsStep.vue"),
);

const currentStepComponent = computed(() => {
  switch (currentStep.value) {
    case 0:
      return AttachmentsStep;
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
      return OCRResultsStep;
    default:
      return null;
  }
});

const updateField = (field: keyof typeof caseData.value, value: any) => {
  caseData.value[field] = value;
};

const handleNext = () => {
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
  currentStep.value = stepIndex;
};

onMounted(async () => {
  if (props.caseId) {
    try {
      const existingCase = await casesService.getCase(props.caseId);
      console.log("Loading existing case:", existingCase);

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

      if (existingCase.template) selectedTemplate.value = existingCase.template;

      if (existingCase.clinical_history)
        Object.assign(
          caseData.value.clinical_history,
          existingCase.clinical_history,
        );
      if (existingCase.physical_examination)
        Object.assign(
          caseData.value.physical_examination,
          existingCase.physical_examination,
        );
      if (existingCase.detailed_investigations)
        Object.assign(
          caseData.value.detailed_investigations,
          existingCase.detailed_investigations,
        );
      if (existingCase.diagnosis_management)
        Object.assign(
          caseData.value.diagnosis_management,
          existingCase.diagnosis_management,
        );
      if (existingCase.learning_outcomes)
        Object.assign(
          caseData.value.learning_outcomes,
          existingCase.learning_outcomes,
        );

      console.log("Case data loaded successfully");
    } catch (error) {
      console.error("Error loading case:", error);
      toast.error("Không thể tải dữ liệu ca bệnh");
    }
  }
});

const handleSaveDraft = async () => {
  try {
    const payload = {
      title: caseData.value.title,
      patient_name: caseData.value.patient_name || caseData.value.title,
      ...(caseData.value.repository
        ? { repository: caseData.value.repository }
        : {}),
      specialty: caseData.value.specialty,
      complexity_level: caseData.value.complexity_level,
      patient_age: caseData.value.patient_age,
      patient_gender: caseData.value.patient_gender || "not_specified",
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
      case_status: "draft",
      clinical_history: caseData.value.clinical_history,
      physical_examination: caseData.value.physical_examination,
      detailed_investigations: caseData.value.detailed_investigations,
      diagnosis_management: caseData.value.diagnosis_management,
      learning_outcomes: caseData.value.learning_outcomes,
    };

    let response;

    if (props.caseId) {
      response = await api.put(`/cases/${props.caseId}/`, payload);
      toast.success("Đã cập nhật nháp!");
    } else {
      const hasAttachments =
        caseData.value.attachments && caseData.value.attachments.length > 0;

      if (hasAttachments) {
        const formData = new FormData();
        formData.append("data", JSON.stringify(payload));
        caseData.value.attachments.forEach((file: File, index: number) => {
          formData.append(`attachment_${index}`, file);
        });
        response = await api.post("/cases/", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
      } else {
        response = await api.post("/cases/", payload);
      }
      toast.success(t("wizard.caseSavedDraft"));
    }

    setTimeout(() => {
      emit("complete", {
        caseId: response.data.id || props.caseId,
        caseData: response.data,
      });
    }, 500);
  } catch (error: any) {
    console.error("Error saving draft:", error);
    toast.error(
      error.response?.data?.message ||
        error.response?.data?.detail ||
        t("wizard.failedToDraft"),
    );
  }
};

const handleComplete = async () => {
  const isValid = stepValidations.value[currentStep.value] !== false;
  if (!isValid) {
    toast.error(t("wizard.completeRequired"));
    return;
  }

  try {
    const cleanObject = (obj: any) => {
      if (!obj || typeof obj !== "object") return undefined;
      const cleaned: any = {};
      let hasNonEmptyValue = false;
      for (const [key, value] of Object.entries(obj)) {
        if (value === undefined || value === null || value === "") continue;
        if (typeof value === "number" && isNaN(value)) continue;
        cleaned[key] = value;
        hasNonEmptyValue = true;
      }
      return hasNonEmptyValue ? cleaned : undefined;
    };

    const formatDate = (dateValue: any) => {
      if (!dateValue || dateValue === "") return null;
      if (
        typeof dateValue === "string" &&
        /^\d{4}-\d{2}-\d{2}$/.test(dateValue)
      )
        return dateValue;
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

    if (caseData.value.template) {
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

    const cleanedClinicalHistory = cleanObject(caseData.value.clinical_history);
    if (cleanedClinicalHistory)
      payload.clinical_history = cleanedClinicalHistory;

    const cleanedPhysicalExam = cleanObject(
      caseData.value.physical_examination,
    );
    if (cleanedPhysicalExam) {
      if (
        cleanedPhysicalExam.consciousness_level &&
        !["alert", "drowsy", "stupor", "coma"].includes(
          cleanedPhysicalExam.consciousness_level,
        )
      ) {
        cleanedPhysicalExam.consciousness_level = "alert";
      }
      payload.physical_examination = cleanedPhysicalExam;
    }

    const cleanedInvestigations = cleanObject(
      caseData.value.detailed_investigations,
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

    const apiEndpoint = isInstructor.value ? "/cases/instructor/" : "/cases/";
    const hasAttachments =
      caseData.value.attachments && caseData.value.attachments.length > 0;

    let response;
    if (hasAttachments) {
      const formData = new FormData();
      formData.append("data", JSON.stringify(payload));
      caseData.value.attachments.forEach((file: File, index: number) => {
        formData.append(`attachment_${index}`, file);
      });
      response = await api.post(apiEndpoint, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
    } else {
      response = await api.post(apiEndpoint, payload);
    }

    if (isInstructor.value) {
      toast.success("Đã tạo và xuất bản hồ sơ mẫu thành công!");
    } else {
      toast.success(t("wizard.caseCreated"));
    }

    setTimeout(() => {
      emit("complete", { caseId: response.data.id, caseData: response.data });
    }, 500);
  } catch (error: any) {
    console.error("Error creating case:", error);
    console.error("Error response:", error.response?.data);
    console.error("Error status:", error.response?.status);

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

    const errorMessages: Record<string, string> = {
      "This field is required.": t(
        "common.fieldRequired",
        "This field is required",
      ),
      "This field may not be blank.": t(
        "common.fieldRequired",
        "This field is required",
      ),
      "This field may not be null.": t(
        "common.fieldRequired",
        "This field is required",
      ),
      "A valid integer is required.": t(
        "common.invalidNumber",
        "Please enter a valid number",
      ),
      "Enter a valid date.": t(
        "common.invalidDate",
        "Please enter a valid date",
      ),
    };

    const translateField = (field: string): string => {
      const i18nKey = fieldToI18nKey[field];
      return i18nKey
        ? t(i18nKey, field.replace(/_/g, " "))
        : field.replace(/_/g, " ");
    };

    const translateError = (msg: string): string => errorMessages[msg] || msg;

    const formatNestedErrors = (
      errors: any,
      parentField: string = "",
    ): string[] => {
      const messages: string[] = [];
      for (const [field, value] of Object.entries(errors)) {
        const fullField = parentField ? `${parentField}.${field}` : field;
        const fieldName = translateField(field);
        if (Array.isArray(value)) {
          messages.push(`${fieldName}: ${translateError(value[0])}`);
        } else if (typeof value === "object" && value !== null) {
          messages.push(...formatNestedErrors(value, fullField));
        } else if (typeof value === "string") {
          messages.push(`${fieldName}: ${translateError(value)}`);
        }
      }
      return messages;
    };

    let errorMessage = t("wizard.failedToCreate");

    if (error.response?.data) {
      console.error(
        "Full error object: ",
        JSON.stringify(error.response.data, null, 2),
      );
      if (error.response.data.message) {
        errorMessage = error.response.data.message;
      } else if (error.response.data.detail) {
        errorMessage = error.response.data.detail;
      } else {
        const formattedErrors = formatNestedErrors(error.response.data);
        if (formattedErrors.length > 0) {
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

defineExpose({
  caseData,
  updateField,
  studentDepartment: props.studentDepartment,
});
</script>
