<template>
  <div class="space-y-6">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Mental Status / Consciousness -->
      <Card class="p-3 border-2 border-gray-200">
        <template #content>
          <div class="p-2">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">
              {{ t("createCase.mentalStatus") }}
            </h3>

            <div class="grid grid-cols-2 gap-2">
              <div
                v-for="status in consciousnessOptions"
                :key="status.value"
                class="flex items-center gap-2"
              >
                <RadioButton
                  :inputId="`consciousness-${status.value}`"
                  :value="status.value"
                  :modelValue="
                    localData.physical_examination.consciousness_level
                  "
                  @update:modelValue="setConsciousnessLevel"
                />
                <label
                  :for="`consciousness-${status.value}`"
                  class="text-sm cursor-pointer"
                >
                  {{ t(`createCase.${status.value}`) }}
                </label>
              </div>
            </div>
          </div>
        </template>
      </Card>

      <!-- Vital Signs Summary -->
      <Card class="p-3 border-2 border-gray-200">
        <template #content>
          <div class="p-2">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">
              {{ t("createCase.vitalSignsSummary") }}
            </h3>

            <div class="space-y-3 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-600"
                  >{{ t("createCase.temperature") }}:</span
                >
                <span class="font-medium"
                  >{{
                    localData.physical_examination?.vital_signs_temp ||
                    t("createCase.notRecorded")
                  }}
                  (°C)</span
                >
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600"
                  >{{ t("createCase.heartRate") }}:</span
                >
                <span class="font-medium"
                  >{{
                    localData.physical_examination?.vital_signs_hr ||
                    t("createCase.notRecorded")
                  }}
                  (bpm)</span
                >
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600"
                  >{{ t("createCase.bloodPressure") }}:</span
                >
                <span class="font-medium"
                  >{{
                    localData.physical_examination?.vital_signs_bp ||
                    t("createCase.notRecorded")
                  }}
                  (mmHg)</span
                >
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600"
                  >{{ t("createCase.respiratoryRate") }}:</span
                >
                <span class="font-medium"
                  >{{
                    localData.physical_examination?.vital_signs_rr ||
                    t("createCase.notRecorded")
                  }}
                  {{ t("createCase.respiratoryRateUnit") }}</span
                >
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600"
                  >{{ t("createCase.oxygenSaturation") }}:</span
                >
                <span class="font-medium"
                  >{{
                    localData.physical_examination?.vital_signs_spo2 ||
                    t("createCase.notRecorded")
                  }}
                  %</span
                >
              </div>
            </div>
          </div>
        </template>
      </Card>
    </div>

    <!-- Systems Review -->
    <Card class="p-3 border-2 border-gray-200">
      <template #content>
        <div class="p-2">
          <h3 class="text-lg font-semibold text-gray-900 mb-6">
            {{ t("createCase.physicalExaminationBySystem") }}
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="headNeck" class="field-label">{{
                  t("createCase.headAndNeck")
                }}</label>
                <VoiceToText
                  v-model="localData.physical_examination.head_neck"
                  size="small"
                />
              </div>
              <Textarea
                id="headNeck"
                v-model="localData.physical_examination.head_neck"
                :placeholder="t('createCase.heentPlaceholder')"
                rows="3"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="cardiovascular" class="field-label">{{
                  t("createCase.cardiovascular")
                }}</label>
                <VoiceToText
                  v-model="localData.physical_examination.cardiovascular"
                  size="small"
                />
              </div>
              <Textarea
                id="cardiovascular"
                v-model="localData.physical_examination.cardiovascular"
                :placeholder="t('createCase.cardiovascularPlaceholder')"
                rows="3"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="respiratory" class="field-label">{{
                  t("createCase.respiratory")
                }}</label>
                <VoiceToText
                  v-model="localData.physical_examination.respiratory"
                  size="small"
                />
              </div>
              <Textarea
                id="respiratory"
                v-model="localData.physical_examination.respiratory"
                :placeholder="t('createCase.respiratoryPlaceholder')"
                rows="3"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="abdominal" class="field-label">{{
                  t("createCase.abdominal")
                }}</label>
                <VoiceToText
                  v-model="localData.physical_examination.abdominal"
                  size="small"
                />
              </div>
              <Textarea
                id="abdominal"
                v-model="localData.physical_examination.abdominal"
                :placeholder="t('createCase.abdominalPlaceholder')"
                rows="3"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="neurological" class="field-label">{{
                  t("createCase.neurological")
                }}</label>
                <VoiceToText
                  v-model="localData.physical_examination.neurological"
                  size="small"
                />
              </div>
              <Textarea
                id="neurological"
                v-model="localData.physical_examination.neurological"
                :placeholder="t('createCase.neurologicalPlaceholder')"
                rows="3"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="musculoskeletal" class="field-label">{{
                  t("createCase.musculoskeletal")
                }}</label>
                <VoiceToText
                  v-model="localData.physical_examination.musculoskeletal"
                  size="small"
                />
              </div>
              <Textarea
                id="musculoskeletal"
                v-model="localData.physical_examination.musculoskeletal"
                :placeholder="t('createCase.musculoskeletalPlaceholder')"
                rows="3"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="skin" class="field-label">{{
                  t("createCase.skin")
                }}</label>
                <VoiceToText
                  v-model="localData.physical_examination.skin"
                  size="small"
                />
              </div>
              <Textarea
                id="skin"
                v-model="localData.physical_examination.skin"
                :placeholder="t('createCase.skinPlaceholder')"
                rows="3"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="other_systems" class="field-label"
                  >Ghi chú khám bổ sung</label
                >
                <VoiceToText
                  v-model="localData.physical_examination.other_systems"
                  size="small"
                />
              </div>
              <Textarea
                id="other_systems"
                v-model="localData.physical_examination.other_systems"
                placeholder="Các hệ thống khác hoặc ghi chú bổ sung..."
                rows="3"
                class="w-full"
              />
            </div>
          </div>
        </div>
      </template>
    </Card>

    <!-- Additional Exam Notes -->
    <Card class="p-3 border-2 border-gray-200">
      <template #content>
        <div class="p-2">
          <div class="flex items-center gap-2 mb-4">
            <h3 class="text-lg font-semibold text-gray-900">
              {{ t("createCase.additionalExaminationNotes") }}
            </h3>
            <VoiceToText
              v-model="localData.physical_examination.other_findings"
              size="small"
            />
          </div>
          <Textarea
            id="examNotes"
            fluid
            v-model="localData.physical_examination.other_findings"
            :placeholder="t('createCase.additionalFindingsPlaceholder')"
            rows="4"
            class="w-full"
          />
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
import RadioButton from "primevue/radiobutton";
import VoiceToText from "@/components/VoiceToText.vue";

const props = defineProps<{ caseData: any }>();
const { t } = useI18n();
const emit = defineEmits<{ "update:caseData": [any] }>();

const localData = computed({
  get: () => props.caseData,
  set: (value) => emit("update:caseData", value),
});

const setConsciousnessLevel = (value: string) => {
  emit("update:caseData", {
    ...props.caseData,
    physical_examination: {
      ...props.caseData.physical_examination,
      consciousness_level: value,
    },
  });
};

const consciousnessOptions = [
  { value: "alert", label: "Alert" },
  { value: "drowsy", label: "Drowsy" },
  { value: "stupor", label: "Stupor" },
  { value: "coma", label: "Coma" },
];
</script>

<style scoped>
.field-label {
  font-weight: 600;
  font-size: 0.875rem;
  color: #374151;
}
</style>
