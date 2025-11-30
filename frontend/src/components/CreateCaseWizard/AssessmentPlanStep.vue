<template>
  <div class="space-y-6">
    <!-- Diagnosis -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ t('createCase.diagnosis') }}
        </h3>

        <div class="space-y-4">
          <div class="space-y-2">
            <Label for="primaryDiagnosis">{{ t('createCase.primaryDiagnosis') }} *</Label>
            <Textarea id="primaryDiagnosis" v-model="localData.diagnosis_management.primary_diagnosis"
              :placeholder="t('createCase.primaryDiagnosisPlaceholder')" rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="differentialDiagnosis">{{ t('createCase.differentialDiagnosis') }}</Label>
            <Textarea id="differentialDiagnosis" v-model="localData.diagnosis_management.differential_diagnosis"
              :placeholder="t('createCase.differentialDiagnosisPlaceholder')" rows="4" />
          </div>

          <div class="space-y-2">
            <Label for="icdCode">{{ t('createCase.icdCode') }}</Label>
            <Input id="icdCode" v-model="localData.diagnosis_management.icd10_codes"
              :placeholder="t('createCase.icdCodePlaceholder')" />
          </div>
        </div>
      </div>
    </Card>

    <!-- Treatment/Management Plan -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ t('createCase.managementPlan') }}
        </h3>

        <div class="space-y-4">
          <div class="space-y-2">
            <Label for="treatmentPlan">{{ t('createCase.treatmentPlan') }}</Label>
            <Textarea id="treatmentPlan" v-model="localData.diagnosis_management.treatment_plan"
              :placeholder="t('createCase.treatmentPlanPlaceholder')" rows="4" />
          </div>

          <div class="space-y-2">
            <Label for="medications">{{ t('createCase.medicationsPrescribed') }}</Label>
            <Textarea id="medications" v-model="localData.diagnosis_management.medications_prescribed"
              :placeholder="t('createCase.medicationsPrescribedPlaceholder')" rows="4" />
          </div>

          <div class="space-y-2">
            <Label for="procedures">{{ t('createCase.proceduresInterventions') }}</Label>
            <Textarea id="procedures" v-model="localData.diagnosis_management.procedures_performed"
              :placeholder="t('createCase.proceduresPlaceholder')" rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="followUp">{{ t('createCase.followUp') }}</Label>
            <Textarea id="followUp" v-model="localData.diagnosis_management.follow_up_plan"
              :placeholder="t('createCase.followUpPlaceholder')" rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="prognosis">{{ t('createCase.prognosis') }}</Label>
            <Textarea id="prognosis" v-model="localData.diagnosis_management.prognosis"
              :placeholder="t('createCase.prognosisPlaceholder')" rows="2" />
          </div>
        </div>
      </div>
    </Card>

    <!-- Learning Outcomes -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ t('createCase.educationalObjectives') }}
        </h3>

        <div class="space-y-4">
          <div class="space-y-2">
            <Label for="learningObjectives">{{ t('createCase.learningObjectives') }}</Label>
            <Textarea id="learningObjectives" v-model="localData.learning_outcomes.learning_objectives"
              :placeholder="t('createCase.learningObjectivesPlaceholder')" rows="4" />
          </div>

          <div class="space-y-2">
            <Label for="keyConcepts">{{ t('createCase.keyConcepts') }}</Label>
            <Textarea id="keyConcepts" v-model="localData.learning_outcomes.key_concepts"
              :placeholder="t('createCase.keyConceptsPlaceholder')" rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="clinicalPearls">{{ t('createCase.clinicalPearls') }}</Label>
            <Textarea id="clinicalPearls" v-model="localData.learning_outcomes.clinical_pearls"
              :placeholder="t('createCase.clinicalPearlsPlaceholder')" rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="references">{{ t('createCase.references') }}</Label>
            <Textarea id="references" v-model="localData.learning_outcomes.references"
              :placeholder="t('createCase.referencesPlaceholder')" rows="3" />
          </div>
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import Card from '@/components/ui/Card.vue'
import Input from '@/components/ui/Input.vue'
import Label from '@/components/ui/Label.vue'
import Textarea from '@/components/ui/Textarea.vue'

const props = defineProps<{
  caseData: any
}>()

const { t } = useI18n()

const emit = defineEmits<{
  'update:caseData': [any]
}>()

const localData = computed({
  get: () => props.caseData,
  set: (value) => emit('update:caseData', value)
})
</script>
