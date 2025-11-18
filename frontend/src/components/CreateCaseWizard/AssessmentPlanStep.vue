<template>
  <div class="space-y-6">
    <div class="text-center">
      <h2 class="text-2xl font-bold text-gray-900 mb-2">
        {{ $t('createCase.assessmentAndPlan') }}
      </h2>
      <p class="text-gray-600">
        {{ $t('createCase.assessmentPlanDescription') }}
      </p>
    </div>

    <!-- Assessment/Diagnosis -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ $t('createCase.assessment') }}
        </h3>

        <div class="space-y-4">
          <div class="space-y-2">
            <Label for="primaryDiagnosis">{{ $t('createCase.primaryDiagnosis') }} *</Label>
            <Textarea id="primaryDiagnosis" v-model="assessment.primaryDiagnosis"
              :placeholder="$t('createCase.primaryDiagnosisPlaceholder')" :error="errors.primaryDiagnosis" rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="differentialDiagnosis">{{ $t('createCase.differentialDiagnosis') }}</Label>
            <Textarea id="differentialDiagnosis" v-model="assessment.differentialDiagnosis"
              :placeholder="$t('createCase.differentialDiagnosisPlaceholder')" rows="4" />
          </div>

          <div class="space-y-2">
            <Label for="clinicalReasoning">{{ $t('createCase.clinicalReasoning') }}</Label>
            <Textarea id="clinicalReasoning" v-model="assessment.clinicalReasoning"
              :placeholder="$t('createCase.clinicalReasoningPlaceholder')" rows="4" />
          </div>
        </div>
      </div>
    </Card>

    <!-- Treatment Plan -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ $t('createCase.treatmentPlan') }}
        </h3>

        <div class="space-y-6">
          <!-- Medications -->
          <div class="space-y-4">
            <h4 class="font-medium text-gray-900">{{ $t('createCase.medications') }}</h4>

            <div v-for="(medication, index) in assessment.medications" :key="index"
              class="border border-gray-200 rounded-lg p-4">
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="space-y-2">
                  <Label :for="`med-name-${index}`">{{ $t('createCase.medicationName') }}</Label>
                  <Input :id="`med-name-${index}`" v-model="medication.name"
                    :placeholder="$t('createCase.medicationNamePlaceholder')" />
                </div>

                <div class="space-y-2">
                  <Label :for="`med-dose-${index}`">{{ $t('createCase.dosage') }}</Label>
                  <Input :id="`med-dose-${index}`" v-model="medication.dosage" :placeholder="'500 mg'" />
                </div>

                <div class="space-y-2">
                  <Label :for="`med-route-${index}`">{{ $t('createCase.route') }}</Label>
                  <select :id="`med-route-${index}`" v-model="medication.route"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                    <option value="">{{ $t('createCase.selectRoute') }}</option>
                    <option value="oral">Oral</option>
                    <option value="iv">IV</option>
                    <option value="im">IM</option>
                    <option value="subcutaneous">Subcutaneous</option>
                    <option value="topical">Topical</option>
                    <option value="inhaled">Inhaled</option>
                  </select>
                </div>

                <div class="space-y-2">
                  <Label :for="`med-frequency-${index}`">{{ $t('createCase.frequency') }}</Label>
                  <Input :id="`med-frequency-${index}`" v-model="medication.frequency" :placeholder="'twice daily'" />
                </div>
              </div>

              <div class="mt-4 flex justify-end">
                <Button variant="outline" size="sm" @click="removeMedication(index)"
                  class="text-red-600 hover:text-red-700">
                  {{ $t('createCase.removeMedication') }}
                </Button>
              </div>
            </div>

            <Button variant="outline" @click="addMedication" class="w-full">
              <PlusIcon class="w-4 h-4 mr-2" />
              {{ $t('createCase.addMedication') }}
            </Button>
          </div>

          <!-- Procedures/Interventions -->
          <div class="space-y-4">
            <h4 class="font-medium text-gray-900">{{ $t('createCase.proceduresInterventions') }}</h4>

            <div class="space-y-2">
              <Textarea id="procedures" v-model="assessment.procedures"
                :placeholder="$t('createCase.proceduresPlaceholder')" rows="4" />
            </div>
          </div>

          <!-- Follow-up -->
          <div class="space-y-4">
            <h4 class="font-medium text-gray-900">{{ $t('createCase.followUp') }}</h4>

            <div class="space-y-2">
              <Textarea id="followUp" v-model="assessment.followUp" :placeholder="$t('createCase.followUpPlaceholder')"
                rows="3" />
            </div>
          </div>
        </div>
      </div>
    </Card>

    <!-- Learning Objectives -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ $t('createCase.learningObjectives') }}
        </h3>

        <div class="space-y-4">
          <div v-for="(objective, index) in assessment.learningObjectives" :key="index"
            class="flex items-center space-x-4">
            <span
              class="flex-shrink-0 w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-sm font-medium">
              {{ index + 1 }}
            </span>
            <Input v-model="objective.text" :placeholder="$t('createCase.learningObjectivePlaceholder')"
              class="flex-1" />
            <Button variant="outline" size="sm" @click="removeLearningObjective(index)"
              class="text-red-600 hover:text-red-700">
              <XIcon class="w-4 h-4" />
            </Button>
          </div>

          <Button variant="outline" @click="addLearningObjective" class="w-full">
            <PlusIcon class="w-4 h-4 mr-2" />
            {{ $t('createCase.addLearningObjective') }}
          </Button>
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import Card from '@/components/ui/Card.vue'
import Input from '@/components/ui/Input.vue'
import Label from '@/components/ui/Label.vue'
import Textarea from '@/components/ui/Textarea.vue'
import Button from '@/components/ui/Button.vue'
import { PlusIcon, XIcon } from '@/components/icons'

const { t } = useI18n()

const props = defineProps({
  caseData: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:caseData', 'validation-changed'])

const assessment = computed({
  get: () => props.caseData.assessment || {
    medications: [],
    learningObjectives: []
  },
  set: (value) => emit('update:caseData', {
    ...props.caseData,
    assessment: value
  })
})

const errors = ref({
  primaryDiagnosis: ''
})

const validateStep = () => {
  errors.value = {
    primaryDiagnosis: ''
  }

  if (!assessment.value.primaryDiagnosis?.trim()) {
    errors.value.primaryDiagnosis = t('createCase.primaryDiagnosisRequired')
  }

  return Object.keys(errors.value).length === 0
}

const addMedication = () => {
  assessment.value.medications.push({
    name: '',
    dosage: '',
    route: '',
    frequency: ''
  })
}

const removeMedication = (index: number) => {
  assessment.value.medications.splice(index, 1)
}

const addLearningObjective = () => {
  assessment.value.learningObjectives.push({
    text: ''
  })
}

const removeLearningObjective = (index: number) => {
  assessment.value.learningObjectives.splice(index, 1)
}

// Watch for changes and emit validation status
watch([assessment], () => {
  emit('validation-changed', validateStep())
}, { deep: true })

// Expose validation function
defineExpose({
  validateStep
})
</script>
