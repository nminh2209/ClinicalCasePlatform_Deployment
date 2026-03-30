<template>
  <div class="space-y-6">
    <Card class="p-3 border-2 border-gray-200">
      <template #content>
        <div class="p-2">
          <h3 class="text-lg font-semibold text-gray-900 mb-6">
            {{ t("createCase.caseInformation") }}
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="flex flex-col gap-1 md:col-span-2">
              <label for="title" class="field-label"
                >{{ t("createCase.caseTitle") }} *</label
              >
              <div class="flex gap-2 items-start">
                <InputText
                  id="title"
                  v-model="localData.title"
                  :placeholder="t('createCase.enterCaseTitle')"
                  :invalid="!!getTranslatedError('title')"
                  class="flex-1"
                />
                <VoiceToText v-model="localData.title" />
              </div>
              <small v-if="getTranslatedError('title')" class="text-red-600">
                {{ getTranslatedError("title") }}
              </small>
            </div>

            <input type="hidden" v-model="localData.patient_name" />

            <div class="flex flex-col gap-1">
              <label for="specialty" class="field-label"
                >{{ t("createCase.specialty") }} *</label
              >
              <Select
                id="specialty"
                v-model="localData.specialty"
                :options="specialties.filter(Boolean)"
                optionLabel="name"
                optionValue="name"
                :placeholder="
                  choicesLoading
                    ? 'Đang tải...'
                    : t('createCase.selectSpecialty')
                "
                :disabled="choicesLoading"
                :invalid="!!getTranslatedError('specialty')"
                class="w-full"
              />
              <small
                v-if="getTranslatedError('specialty')"
                class="text-red-600"
              >
                {{ getTranslatedError("specialty") }}
              </small>
            </div>

            <div class="flex flex-col gap-1">
              <label for="complexity" class="field-label">{{
                t("createCase.complexity")
              }}</label>
              <Select
                id="complexity"
                v-model="localData.complexity_level"
                :options="complexities"
                option-label="name"
                option-value="key"
                :placeholder="
                  choicesLoading ? 'Đang tải...' : 'Chọn độ phức tạp'
                "
                :disabled="choicesLoading"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <label for="priority" class="field-label">Mức độ ưu tiên</label>
              <Select
                id="priority"
                v-model="localData.priority_level"
                :options="priorities"
                option-label="name"
                option-value="key"
                :placeholder="
                  choicesLoading ? 'Đang tải...' : 'Chọn mức độ ưu tiên'
                "
                :disabled="choicesLoading"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-2">
              <label for="keywords" class="field-label"
                >Từ khóa (Keywords)</label
              >
              <InputText
                id="keywords"
                fluid
                v-model="localData.keywords"
                placeholder="Ví dụ: acute, myocardial, infarction"
              />
              <Message size="small" severity="secondary" variant="simple">
                Từ khóa tìm kiếm, phân cách bằng dấu phẩy
              </Message>
            </div>
          </div>
        </div>
      </template>
    </Card>

    <Card class="p-3 border-2 border-gray-200">
      <template #content>
        <div class="p-2">
          <h3 class="text-lg font-semibold text-gray-900 mb-6">
            {{ t("createCase.patientDemographics") }}
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="flex flex-col gap-1">
              <label for="age" class="field-label"
                >{{ t("createCase.age") }} *</label
              >
              <InputNumber
                id="age"
                showButtons
                v-model="localData.patient_age"
                :placeholder="t('createCase.patientAge')"
                :invalid="!!getTranslatedError('patient_age')"
                :min="0"
                :max="150"
              />
              <small
                v-if="getTranslatedError('patient_age')"
                class="text-red-600"
              >
                {{ getTranslatedError("patient_age") }}
              </small>
            </div>

            <div class="flex flex-col gap-1">
              <label for="gender" class="field-label"
                >{{ t("createCase.gender") }} *</label
              >
              <Select
                id="gender"
                v-model="localData.patient_gender"
                :options="genderOptions"
                optionLabel="label"
                optionValue="value"
                :placeholder="t('createCase.selectGender')"
                :invalid="!!getTranslatedError('patient_gender')"
                class="w-full"
              />
              <small
                v-if="getTranslatedError('patient_gender')"
                class="text-red-600"
              >
                {{ getTranslatedError("patient_gender") }}
              </small>
            </div>

            <div class="flex flex-col gap-1">
              <label for="mrn" class="field-label">{{
                t("createCase.medicalRecordNumber")
              }}</label>
              <InputText
                id="mrn"
                v-model="localData.medical_record_number"
                :placeholder="t('createCase.enterMRN')"
              />
            </div>

            <div class="flex flex-col gap-1">
              <label for="ethnicity" class="field-label">{{
                t("createCase.ethnicity")
              }}</label>
              <InputText
                id="ethnicity"
                v-model="localData.patient_ethnicity"
                :placeholder="t('createCase.enterEthnicity')"
              />
            </div>

            <div class="flex flex-col gap-1">
              <label for="occupation" class="field-label">{{
                t("createCase.occupation")
              }}</label>
              <InputText
                id="occupation"
                v-model="localData.patient_occupation"
                :placeholder="t('createCase.enterOccupation')"
              />
            </div>

            <div class="flex flex-col gap-1">
              <label for="admission" class="field-label">{{
                t("createCase.admissionDate")
              }}</label>
              <InputText
                id="admission"
                type="date"
                v-model="localData.admission_date"
                class="w-full"
              />
            </div>
          </div>
        </div>
      </template>
    </Card>

    <Card class="p-3 border-2 border-gray-200">
      <template #content>
        <div class="p-2">
          <h3 class="text-lg font-semibold text-gray-900 mb-6">
            {{ t("createCase.clinicalPresentation") }}
          </h3>

          <div class="space-y-6">
            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="chief_complaint" class="field-label"
                  >{{ t("createCase.chief_complaint") }} *</label
                >
                <VoiceToText
                  v-model="localData.clinical_history.chief_complaint"
                  size="small"
                />
              </div>
              <Textarea
                id="chief_complaint"
                v-model="localData.clinical_history.chief_complaint"
                :placeholder="t('createCase.describe_chief_complaint')"
                :invalid="!!getTranslatedError('chief_complaint')"
                rows="3"
                class="w-full"
              />
              <small
                v-if="getTranslatedError('chief_complaint')"
                class="text-red-600"
              >
                {{ getTranslatedError("chief_complaint") }}
              </small>
            </div>

            <div class="flex flex-col gap-1">
              <label for="chief_complaintBrief" class="field-label">{{
                t("createCase.briefChiefComplaint")
              }}</label>
              <InputText
                id="chief_complaintBrief"
                v-model="localData.chief_complaint_brief"
                :placeholder="t('createCase.enterBriefComplaint')"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="historyPresent" class="field-label">{{
                  t("createCase.historyOfPresentIllness")
                }}</label>
                <VoiceToText
                  v-model="localData.clinical_history.history_present_illness"
                  size="small"
                />
              </div>
              <Textarea
                id="historyPresent"
                v-model="localData.clinical_history.history_present_illness"
                :placeholder="t('createCase.detailedHistory')"
                rows="6"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="pastMedical" class="field-label">{{
                  t("createCase.pastMedicalHistory")
                }}</label>
                <VoiceToText
                  v-model="localData.clinical_history.past_medical_history"
                  size="small"
                />
              </div>
              <Textarea
                id="pastMedical"
                v-model="localData.clinical_history.past_medical_history"
                :placeholder="t('createCase.describePMH')"
                rows="4"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="medications" class="field-label">{{
                  t("createCase.currentMedications")
                }}</label>
                <VoiceToText
                  v-model="localData.clinical_history.medications"
                  size="small"
                />
              </div>
              <Textarea
                id="medications"
                v-model="localData.clinical_history.medications"
                :placeholder="t('createCase.listMedications')"
                rows="3"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="allergies" class="field-label">{{
                  t("createCase.allergies")
                }}</label>
                <VoiceToText
                  v-model="localData.clinical_history.allergies"
                  size="small"
                />
              </div>
              <Textarea
                id="allergies"
                v-model="localData.clinical_history.allergies"
                :placeholder="t('createCase.enterAllergies')"
                rows="2"
                class="w-full"
              />
            </div>

            <!-- Symptom Details -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="flex flex-col gap-1">
                <label for="symptom_duration" class="field-label"
                  >Thời gian có triệu chứng (ngày)</label
                >
                <InputNumber
                  id="symptom_duration"
                  v-model="localData.clinical_history.symptom_duration_days"
                  placeholder="Ví dụ: 7"
                  :min="0"
                />
              </div>

              <div class="flex flex-col gap-1">
                <label for="symptom_onset" class="field-label"
                  >Khởi phát triệu chứng</label
                >
                <Select
                  id="symptom_onset"
                  v-model="localData.clinical_history.symptom_onset"
                  :options="symptomOnsetOptions"
                  optionLabel="label"
                  optionValue="value"
                  placeholder="Chọn"
                  class="w-full"
                />
              </div>

              <div class="flex flex-col gap-1">
                <label for="symptom_progression" class="field-label"
                  >Diễn biến triệu chứng</label
                >
                <Select
                  id="symptom_progression"
                  v-model="localData.clinical_history.symptom_progression"
                  :options="symptomProgressionOptions"
                  optionLabel="label"
                  optionValue="value"
                  placeholder="Chọn"
                  class="w-full"
                />
              </div>
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="family_history" class="field-label"
                  >Tiền sử gia đình</label
                >
                <VoiceToText
                  v-model="localData.clinical_history.family_history"
                  size="small"
                />
              </div>
              <Textarea
                id="family_history"
                v-model="localData.clinical_history.family_history"
                :placeholder="t('createCase.describeFamilyHistory')"
                rows="3"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="social_history" class="field-label"
                  >Tiền sử xã hội</label
                >
                <VoiceToText
                  v-model="localData.clinical_history.social_history"
                  size="small"
                />
              </div>
              <Textarea
                id="social_history"
                v-model="localData.clinical_history.social_history"
                :placeholder="t('createCase.describeSocialHistory')"
                rows="3"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="review_systems" class="field-label"
                  >Hỏi bệnh theo hệ thống</label
                >
                <VoiceToText
                  v-model="localData.clinical_history.review_systems"
                  size="small"
                />
              </div>
              <Textarea
                id="review_systems"
                v-model="localData.clinical_history.review_systems"
                :placeholder="t('createCase.describeSystemsReview')"
                rows="4"
                class="w-full"
              />
            </div>
          </div>
        </div>
      </template>
    </Card>

    <!-- Case Summary & Learning Info -->
    <Card class="p-3 border-2 border-gray-200">
      <template #content>
        <div class="p-2">
          <h3 class="text-lg font-semibold text-gray-900 mb-6">
            Tóm tắt và Thông tin Học tập
          </h3>

          <div class="space-y-6">
            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="case_summary" class="field-label"
                  >Tóm tắt ca bệnh</label
                >
                <VoiceToText v-model="localData.case_summary" size="small" />
              </div>
              <Textarea
                id="case_summary"
                v-model="localData.case_summary"
                placeholder="Tóm tắt ngắn gọn về ca bệnh này..."
                rows="4"
                class="w-full"
              />
              <Message size="small" severity="secondary" variant="simple">
                Tóm tắt chung về ca bệnh để sinh viên dễ hiểu
              </Message>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="flex flex-col gap-1">
                <label for="learning_tags" class="field-label"
                  >Tags học tập</label
                >
                <InputText
                  id="learning_tags"
                  v-model="localData.learning_tags"
                  placeholder="Ví dụ: Tim mạch, Cấp cứu, Nội khoa"
                />
                <Message size="small" severity="secondary" variant="simple">
                  Các từ khóa giúp tìm kiếm, cách nhau bởi dấu phẩy
                </Message>
              </div>

              <div class="flex flex-col gap-1">
                <label for="estimated_hours" class="field-label"
                  >Số giờ học ước tính</label
                >
                <InputNumber
                  id="estimated_hours"
                  showButtons
                  v-model="localData.estimated_study_hours"
                  placeholder="Ví dụ: 2"
                  :min="0"
                  :step="0.5"
                />
                <Message size="small" severity="secondary" variant="simple">
                  Thời gian học tập dự kiến (giờ)
                </Message>
              </div>
            </div>
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { useChoices } from "@/composables/useChoices";
import Card from "primevue/card";
import InputText from "primevue/inputtext";
import InputNumber from "primevue/inputnumber";
import Textarea from "primevue/textarea";
import Select from "primevue/select";
import Message from "primevue/message";
import VoiceToText from "@/components/VoiceToText.vue";

const { t } = useI18n();
const {
  specialties,
  priorities,
  complexities,
  loading: choicesLoading,
  fetchChoices,
  refresh,
} = useChoices();

const props = defineProps<{ caseData: any }>();
const emit = defineEmits<{
  "update:caseData": [any];
  "validation-changed": [boolean];
}>();

const localData = computed({
  get: () => props.caseData,
  set: (value) => emit("update:caseData", value),
});

const genderOptions = computed(() => [
  { label: t("createCase.male"), value: "male" },
  { label: t("createCase.female"), value: "female" },
  { label: t("createCase.other"), value: "other" },
]);

const symptomOnsetOptions = [
  { label: "Đột ngột", value: "sudden" },
  { label: "Từ từ", value: "gradual" },
  { label: "Mạn tính", value: "chronic" },
];

const symptomProgressionOptions = [
  { label: "Cải thiện", value: "improving" },
  { label: "Xấu đi", value: "worsening" },
  { label: "Ổn định", value: "stable" },
  { label: "Biến đổi", value: "fluctuating" },
];

const errors = ref<Record<string, string>>({});

const getTranslatedError = (field: string): string | undefined => {
  if (!errors.value[field]) return undefined;
  const errorKeyMap: Record<string, string> = {
    title: "createCase.caseTitleRequired",
    patient_name: "createCase.patientNameRequired",
    specialty: "createCase.specialtyRequired",
    patient_age: "createCase.validAgeRequired",
    patient_gender: "createCase.genderRequired",
    chief_complaint: "createCase.chief_complaintRequired",
  };
  const keyForError = errorKeyMap[field];
  return keyForError ? t(keyForError) : errors.value[field];
};

const validateStep = () => {
  errors.value = {};
  if (!localData.value.title?.trim())
    errors.value.title = "Case title is required";
  if (!localData.value.patient_name?.trim()) {
    localData.value.patient_name = `Patient - ${localData.value.title?.substring(0, 20) || "Anonymous"}`;
  }
  if (!localData.value.specialty?.trim())
    errors.value.specialty = "Specialty is required";
  if (
    !localData.value.patient_age ||
    localData.value.patient_age < 0 ||
    localData.value.patient_age > 150
  ) {
    errors.value.patient_age = "Valid age is required";
  }
  if (!localData.value.patient_gender)
    errors.value.patient_gender = "Gender is required";
  if (!localData.value.clinical_history?.chief_complaint?.trim()) {
    errors.value.chief_complaint = "Chief complaint is required";
  }
  return Object.keys(errors.value).length === 0;
};

watch(
  localData,
  () => {
    emit("validation-changed", validateStep());
  },
  { deep: true },
);

onMounted(() => {
  fetchChoices();
});

defineExpose({
  validateStep,
});
</script>

<style scoped>
.field-label {
  font-weight: 600;
  font-size: 0.875rem;
  color: #374151;
}
</style>
