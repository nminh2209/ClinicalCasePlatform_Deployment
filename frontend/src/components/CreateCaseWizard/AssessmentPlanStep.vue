<template>
  <div class="space-y-6">
    <!-- Diagnosis -->
    <Card class="p-3 border-2 border-gray-200">
      <template #content>
        <div class="p-2">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            {{ t("createCase.diagnosis") }}
          </h3>

          <div class="space-y-4">
            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="primaryDiagnosis" class="field-label">
                  {{ t("createCase.primaryDiagnosis") }} *
                </label>
                <VoiceToText
                  v-model="localData.diagnosis_management.primary_diagnosis"
                  size="small"
                />
              </div>
              <Textarea
                id="primaryDiagnosis"
                v-model="localData.diagnosis_management.primary_diagnosis"
                :placeholder="t('createCase.primaryDiagnosisPlaceholder')"
                rows="3"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="differentialDiagnosis" class="field-label">
                  {{ t("createCase.differentialDiagnosis") }}
                </label>
                <VoiceToText
                  v-model="
                    localData.diagnosis_management.differential_diagnosis
                  "
                  size="small"
                />
              </div>
              <Textarea
                id="differentialDiagnosis"
                v-model="localData.diagnosis_management.differential_diagnosis"
                :placeholder="t('createCase.differentialDiagnosisPlaceholder')"
                rows="4"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <label for="icdCode" class="field-label">
                {{ t("createCase.icdCode") }}
              </label>
              <InputText
                id="icdCode"
                v-model="localData.diagnosis_management.icd10_codes"
                :placeholder="t('createCase.icdCodePlaceholder')"
                class="w-full"
              />
            </div>
          </div>
        </div>
      </template>
    </Card>

    <!-- Treatment / Management Plan -->
    <Card class="p-3 border-2 border-gray-200">
      <template #content>
        <div class="p-2">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            {{ t("createCase.managementPlan") }}
          </h3>

          <div class="space-y-4">
            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="treatmentPlan" class="field-label">{{
                  t("createCase.treatmentPlan")
                }}</label>
                <VoiceToText
                  v-model="localData.diagnosis_management.treatment_plan"
                  size="small"
                />
              </div>
              <Textarea
                id="treatmentPlan"
                v-model="localData.diagnosis_management.treatment_plan"
                :placeholder="t('createCase.treatmentPlanPlaceholder')"
                rows="4"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="medications" class="field-label">{{
                  t("createCase.medicationsPrescribed")
                }}</label>
                <VoiceToText
                  v-model="
                    localData.diagnosis_management.medications_prescribed
                  "
                  size="small"
                />
              </div>
              <Textarea
                id="medications"
                v-model="localData.diagnosis_management.medications_prescribed"
                :placeholder="t('createCase.medicationsPrescribedPlaceholder')"
                rows="4"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="procedures" class="field-label">{{
                  t("createCase.proceduresInterventions")
                }}</label>
                <VoiceToText
                  v-model="localData.diagnosis_management.procedures_performed"
                  size="small"
                />
              </div>
              <Textarea
                id="procedures"
                v-model="localData.diagnosis_management.procedures_performed"
                :placeholder="t('createCase.proceduresPlaceholder')"
                rows="3"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="followUp" class="field-label">{{
                  t("createCase.followUp")
                }}</label>
                <VoiceToText
                  v-model="localData.diagnosis_management.follow_up_plan"
                  size="small"
                />
              </div>
              <Textarea
                id="followUp"
                v-model="localData.diagnosis_management.follow_up_plan"
                :placeholder="t('createCase.followUpPlaceholder')"
                rows="3"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="prognosis" class="field-label">{{
                  t("createCase.prognosis")
                }}</label>
                <VoiceToText
                  v-model="localData.diagnosis_management.prognosis"
                  size="small"
                />
              </div>
              <Textarea
                id="prognosis"
                v-model="localData.diagnosis_management.prognosis"
                :placeholder="t('createCase.prognosisPlaceholder')"
                rows="2"
                class="w-full"
              />
            </div>
          </div>
        </div>
      </template>
    </Card>

    <!-- Learning Outcomes -->
    <Card class="p-3 border-2 border-gray-200">
      <template #content>
        <div class="p-2">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            {{ t("createCase.educationalObjectives") }}
          </h3>

          <div class="space-y-4">
            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="learningObjectives" class="field-label">{{
                  t("createCase.learningObjectives")
                }}</label>
                <VoiceToText
                  v-model="localData.learning_outcomes.learning_objectives"
                  size="small"
                />
              </div>
              <Textarea
                id="learningObjectives"
                v-model="localData.learning_outcomes.learning_objectives"
                :placeholder="t('createCase.learningObjectivesPlaceholder')"
                rows="4"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="keyConcepts" class="field-label">{{
                  t("createCase.keyConcepts")
                }}</label>
                <VoiceToText
                  v-model="localData.learning_outcomes.key_concepts"
                  size="small"
                />
              </div>
              <Textarea
                id="keyConcepts"
                v-model="localData.learning_outcomes.key_concepts"
                :placeholder="t('createCase.keyConceptsPlaceholder')"
                rows="3"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="clinicalPearls" class="field-label">{{
                  t("createCase.clinicalPearls")
                }}</label>
                <VoiceToText
                  v-model="localData.learning_outcomes.clinical_pearls"
                  size="small"
                />
              </div>
              <Textarea
                id="clinicalPearls"
                v-model="localData.learning_outcomes.clinical_pearls"
                :placeholder="t('createCase.clinicalPearlsPlaceholder')"
                rows="3"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="references" class="field-label">{{
                  t("createCase.references")
                }}</label>
                <VoiceToText
                  v-model="localData.learning_outcomes.references"
                  size="small"
                />
              </div>
              <Textarea
                id="references"
                v-model="localData.learning_outcomes.references"
                :placeholder="t('createCase.referencesPlaceholder')"
                rows="3"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="discussion_points" class="field-label"
                  >Điểm thảo luận</label
                >
                <VoiceToText
                  v-model="localData.learning_outcomes.discussion_points"
                  size="small"
                />
              </div>
              <Textarea
                id="discussion_points"
                v-model="localData.learning_outcomes.discussion_points"
                placeholder="Các điểm quan trọng để thảo luận với sinh viên..."
                rows="3"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <label for="assessment_criteria" class="field-label"
                  >Tiêu chí đánh giá</label
                >
                <VoiceToText
                  v-model="localData.learning_outcomes.assessment_criteria"
                  size="small"
                />
              </div>
              <Textarea
                id="assessment_criteria"
                v-model="localData.learning_outcomes.assessment_criteria"
                placeholder="Các tiêu chí để đánh giá hiểu biết của sinh viên..."
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
import InputText from "primevue/inputtext";
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
