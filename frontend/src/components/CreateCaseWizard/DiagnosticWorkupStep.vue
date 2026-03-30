<template>
  <div class="space-y-6">
    <!-- Laboratory Tests -->
    <Card class="p-3 border-2 border-gray-200">
      <template #content>
        <div class="p-2">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            {{ t("createCase.laboratoryResults") }}
          </h3>

          <div class="space-y-4">
            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="labResults" class="field-label">{{
                  t("createCase.completeLaboratoryResults")
                }}</label>
                <VoiceToText
                  v-model="localData.detailed_investigations.laboratory_results"
                  size="small"
                />
              </div>
              <Textarea
                id="labResults"
                v-model="localData.detailed_investigations.laboratory_results"
                :placeholder="t('createCase.completeLabPlaceholder')"
                rows="4"
                class="w-full"
              />
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div class="flex flex-col gap-1">
                <label for="hemoglobin" class="field-label"
                  >{{ t("createCase.hemoglobin") }}
                  {{ t("createCase.hemoglobinUnit") }}</label
                >
                <InputNumber
                  id="hemoglobin"
                  :step="0.1"
                  v-model="localData.detailed_investigations.hemoglobin_level"
                  placeholder="14.0"
                />
              </div>

              <div class="flex flex-col gap-1">
                <label for="wbc" class="field-label"
                  >{{ t("createCase.whiteBloodCellCount") }}
                  {{ t("createCase.wbcUnit") }}</label
                >
                <InputNumber
                  id="wbc"
                  :step="0.1"
                  v-model="localData.detailed_investigations.white_cell_count"
                  placeholder="7.5"
                />
              </div>

              <div class="flex flex-col gap-1">
                <label for="platelet" class="field-label"
                  >{{ t("createCase.plateletCount") }}
                  {{ t("createCase.plateletUnit") }}</label
                >
                <InputNumber
                  id="platelet"
                  :step="1"
                  v-model="localData.detailed_investigations.platelet_count"
                  placeholder="250"
                />
              </div>

              <div class="flex flex-col gap-1">
                <label for="sodium" class="field-label"
                  >{{ t("createCase.sodium") }}
                  {{ t("createCase.sodiumUnit") }}</label
                >
                <InputNumber
                  id="sodium"
                  :step="0.1"
                  v-model="localData.detailed_investigations.sodium_level"
                  placeholder="140"
                />
              </div>

              <div class="flex flex-col gap-1">
                <label for="potassium" class="field-label"
                  >{{ t("createCase.potassium") }}
                  {{ t("createCase.potassiumUnit") }}</label
                >
                <InputNumber
                  id="potassium"
                  :step="0.1"
                  v-model="localData.detailed_investigations.potassium_level"
                  placeholder="4.0"
                />
              </div>

              <div class="flex flex-col gap-1">
                <label for="creatinine" class="field-label"
                  >{{ t("createCase.creatinine") }}
                  {{ t("createCase.creatinineUnit") }}</label
                >
                <InputNumber
                  id="creatinine"
                  :step="0.1"
                  v-model="localData.detailed_investigations.creatinine_level"
                  placeholder="1.0"
                />
              </div>

              <div class="flex flex-col gap-1">
                <label for="glucose" class="field-label"
                  >{{ t("createCase.glucose") }}
                  {{ t("createCase.glucoseUnit") }}</label
                >
                <InputNumber
                  id="glucose"
                  :step="1"
                  v-model="localData.detailed_investigations.glucose_level"
                  placeholder="100"
                />
              </div>
            </div>
          </div>
        </div>
      </template>
    </Card>

    <!-- Imaging Studies -->
    <Card class="p-3 border-2 border-gray-200">
      <template #content>
        <div class="p-2">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            {{ t("createCase.imagingStudies") }}
          </h3>

          <div class="space-y-4">
            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="imaging" class="field-label">{{
                  t("createCase.imagingFindings")
                }}</label>
                <VoiceToText
                  v-model="localData.detailed_investigations.imaging_studies"
                  size="small"
                />
              </div>
              <Textarea
                id="imaging"
                v-model="localData.detailed_investigations.imaging_studies"
                :placeholder="t('createCase.imagingFindingsPlaceholder')"
                rows="4"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="ecg_findings" class="field-label"
                  >Điện tâm đồ (ECG)</label
                >
                <VoiceToText
                  v-model="localData.detailed_investigations.ecg_findings"
                  size="small"
                />
              </div>
              <Textarea
                id="ecg_findings"
                v-model="localData.detailed_investigations.ecg_findings"
                placeholder="Nhập kết quả điện tâm đồ..."
                rows="3"
                class="w-full"
              />
            </div>
          </div>
        </div>
      </template>
    </Card>

    <!-- Other Diagnostic Tests -->
    <Card class="p-3 border-2 border-gray-200">
      <template #content>
        <div class="p-2">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            {{ t("createCase.otherDiagnosticTests") }}
          </h3>

          <div class="space-y-4">
            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="pathology" class="field-label">{{
                  t("createCase.pathologyResults")
                }}</label>
                <VoiceToText
                  v-model="localData.detailed_investigations.pathology_results"
                  size="small"
                />
              </div>
              <Textarea
                id="pathology"
                v-model="localData.detailed_investigations.pathology_results"
                :placeholder="t('createCase.pathologyPlaceholder')"
                rows="3"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="microbiology" class="field-label">{{
                  t("createCase.microbiologyResults")
                }}</label>
                <VoiceToText
                  v-model="
                    localData.detailed_investigations.microbiology_results
                  "
                  size="small"
                />
              </div>
              <Textarea
                id="microbiology"
                v-model="localData.detailed_investigations.microbiology_results"
                :placeholder="t('createCase.microbiologyPlaceholder')"
                rows="3"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="otherInvestigations" class="field-label">{{
                  t("createCase.additionalInvestigations")
                }}</label>
                <VoiceToText
                  v-model="
                    localData.detailed_investigations.other_investigations
                  "
                  size="small"
                />
              </div>
              <Textarea
                id="otherInvestigations"
                v-model="localData.detailed_investigations.other_investigations"
                :placeholder="
                  t('createCase.additionalInvestigationsPlaceholder')
                "
                rows="3"
                class="w-full"
              />
            </div>
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import Card from "primevue/card";
import Textarea from "primevue/textarea";
import InputNumber from "primevue/inputnumber";
import VoiceToText from "@/components/VoiceToText.vue";

const props = defineProps<{ caseData: any }>();
const { t } = useI18n();
const emit = defineEmits<{ "update:caseData": [any] }>();

const localData = computed({
  get: () => props.caseData,
  set: (value) => emit("update:caseData", value),
});
</script>

<style scoped>
.field-label {
  font-weight: 600;
  font-size: 0.875rem;
  color: #374151;
}
</style>
