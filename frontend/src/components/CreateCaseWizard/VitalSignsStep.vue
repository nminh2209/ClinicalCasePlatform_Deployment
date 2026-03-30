<template>
  <div class="space-y-6">
    <Card class="p-3 border-2 border-gray-200">
      <template #content>
        <div class="p-2">
          <h3 class="text-lg font-semibold text-gray-900 mb-6">
            {{ t("createCase.vitalSigns") }}
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <!-- Temperature -->
            <div class="flex flex-col gap-1">
              <label for="temperature" class="field-label">
                {{ t("createCase.temperature") }}
                {{ t("createCase.temperatureUnit") }}
              </label>
              <InputNumber
                id="temperature"
                :step="0.1"
                v-model="localData.physical_examination.vital_signs_temp"
                placeholder="37.0"
                :min="30"
                :max="45"
              />
            </div>

            <!-- Heart Rate -->
            <div class="flex flex-col gap-1">
              <label for="heartRate" class="field-label">
                {{ t("createCase.heartRate") }}
                {{ t("createCase.heartRateUnit") }}
              </label>
              <InputNumber
                id="heartRate"
                v-model="localData.physical_examination.vital_signs_hr"
                placeholder="72"
                :min="30"
                :max="200"
              />
            </div>

            <!-- Blood Pressure -->
            <div class="flex flex-col gap-1">
              <label for="bloodPressure" class="field-label">
                {{ t("createCase.bloodPressure") }}
                {{ t("createCase.bloodPressureUnit") }}
              </label>
              <InputText
                id="bloodPressure"
                v-model="localData.physical_examination.vital_signs_bp"
                placeholder="120/80"
                class="w-full"
              />
              <small class="text-gray-500 text-xs">{{
                t("createCase.bloodPressureFormat")
              }}</small>
            </div>

            <!-- Respiratory Rate -->
            <div class="flex flex-col gap-1">
              <label for="respiratoryRate" class="field-label">
                {{ t("createCase.respiratoryRate") }}
                {{ t("createCase.respiratoryRateUnit") }}
              </label>
              <InputNumber
                id="respiratoryRate"
                v-model="localData.physical_examination.vital_signs_rr"
                placeholder="16"
                :min="8"
                :max="60"
              />
            </div>

            <!-- Oxygen Saturation -->
            <div class="flex flex-col gap-1">
              <label for="oxygenSaturation" class="field-label">
                {{ t("createCase.oxygenSaturation") }}
                {{ t("createCase.oxygenSaturationUnit") }}
              </label>
              <InputNumber
                id="oxygenSaturation"
                v-model="localData.physical_examination.vital_signs_spo2"
                placeholder="98"
                :min="70"
                :max="100"
              />
            </div>

            <!-- Weight -->
            <div class="flex flex-col gap-1">
              <label for="weight" class="field-label">
                {{ t("createCase.weight") }} {{ t("createCase.weightUnit") }}
              </label>
              <InputNumber
                id="weight"
                :step="0.1"
                v-model="localData.physical_examination.weight_kg"
                placeholder="70"
                :min="10"
                :max="300"
              />
            </div>

            <!-- Height -->
            <div class="flex flex-col gap-1">
              <label for="height" class="field-label">
                {{ t("createCase.height") }} {{ t("createCase.heightUnit") }}
              </label>
              <InputNumber
                id="height"
                :step="0.1"
                v-model="localData.physical_examination.height_cm"
                placeholder="170"
                :min="50"
                :max="250"
              />
            </div>

            <!-- BMI (auto-calculated, read-only) -->
            <div class="flex flex-col gap-1">
              <label for="bmi" class="field-label">
                {{ t("createCase.bmi") }} {{ t("createCase.bmiUnit") }}
              </label>
              <InputNumber
                id="bmi"
                :step="0.1"
                :model-value="calculatedBMI"
                :placeholder="t('createCase.autoCalculated')"
                readonly
                class="bg-gray-50"
              />
            </div>
          </div>

          <div class="mt-6 space-y-4">
            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="generalAppearance" class="field-label"
                  >Ngoại hình chung (General Appearance)</label
                >
                <VoiceToText
                  v-model="localData.physical_examination.general_appearance"
                  size="small"
                />
              </div>
              <Textarea
                id="generalAppearance"
                v-model="localData.physical_examination.general_appearance"
                placeholder="Mô tả ngoại hình và tình trạng chung của bệnh nhân..."
                rows="2"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="vitalSignsNotes" class="field-label">{{
                  t("createCase.generalAppearanceNotes")
                }}</label>
                <VoiceToText
                  v-model="localData.physical_examination.vital_signs"
                  size="small"
                />
              </div>
              <Textarea
                id="vitalSignsNotes"
                v-model="localData.physical_examination.vital_signs"
                :placeholder="t('createCase.generalAppearanceNotesPlaceholder')"
                rows="3"
                class="w-full"
              />
            </div>
          </div>
        </div>
      </template>
    </Card>

    <!-- BMI Category Banner -->
    <Card v-if="calculatedBMI" class="bg-blue-50 border-blue-200">
      <template #content>
        <div class="p-3 flex items-center gap-2">
          <i class="pi pi-info-circle text-blue-600" />
          <span class="text-sm font-medium text-blue-900">
            {{ t("createCase.bmiCategory") }}: {{ getTranslatedBMICategory() }}
          </span>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import Card from "primevue/card";
import InputNumber from "primevue/inputnumber";
import InputText from "primevue/inputtext";
import Textarea from "primevue/textarea";
import VoiceToText from "@/components/VoiceToText.vue";

const { t } = useI18n();

const props = defineProps<{ caseData: any }>();
const emit = defineEmits<{ "update:caseData": [any] }>();

const localData = computed({
  get: () => props.caseData,
  set: (value) => emit("update:caseData", value),
});

const calculatedBMI = computed(() => {
  const weight = localData.value.physical_examination?.weight_kg;
  const height = localData.value.physical_examination?.height_cm;

  if (weight && height && height > 0) {
    const heightInMeters = height / 100;
    const bmi = weight / (heightInMeters * heightInMeters);
    const roundedBMI = Math.round(bmi * 10) / 10;
    if (localData.value.physical_examination) {
      localData.value.physical_examination.bmi = roundedBMI;
    }
    return roundedBMI;
  }

  if (localData.value.physical_examination) {
    localData.value.physical_examination.bmi = null;
  }
  return null;
});

const bmiCategory = computed(() => {
  const bmi = calculatedBMI.value;
  if (!bmi) return "";
  if (bmi < 18.5) return "underweight";
  if (bmi < 25) return "normalWeight";
  if (bmi < 30) return "overweight";
  return "obese";
});

const getTranslatedBMICategory = (): string => {
  const category = bmiCategory.value;
  return category ? t(`createCase.${category}`) : "";
};
</script>

<style scoped>
.field-label {
  font-weight: 600;
  font-size: 0.875rem;
  color: #374151;
}
</style>
