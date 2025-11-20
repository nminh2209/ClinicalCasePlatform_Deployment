<template>
  <div class="space-y-6">
    <div class="text-center">
      <h2 class="text-2xl font-bold text-gray-900 mb-2">
        Diagnosis, Management & Learning Outcomes
      </h2>
      <p class="text-gray-600">
        Clinical diagnosis, treatment plan, and educational objectives
      </p>
    </div>

    <!-- Diagnosis -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          Diagnosis
        </h3>

        <div class="space-y-4">
          <div class="space-y-2">
            <Label for="primaryDiagnosis">Primary Diagnosis *</Label>
            <Textarea id="primaryDiagnosis" v-model="localData.diagnosis_management.primary_diagnosis"
              placeholder="Enter the primary diagnosis with supporting evidence..." rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="differentialDiagnosis">Differential Diagnosis</Label>
            <Textarea id="differentialDiagnosis" v-model="localData.diagnosis_management.differential_diagnosis"
              placeholder="List alternative diagnoses and reasoning for ruling them in or out..." rows="4" />
          </div>

          <div class="space-y-2">
            <Label for="icdCode">ICD-10 Code</Label>
            <Input id="icdCode" v-model="localData.diagnosis_management.icd_code"
              placeholder="e.g., J18.9 (Pneumonia, unspecified)" />
          </div>
        </div>
      </div>
    </Card>

    <!-- Treatment/Management Plan -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          Management Plan
        </h3>

        <div class="space-y-4">
          <div class="space-y-2">
            <Label for="treatmentPlan">Treatment Plan</Label>
            <Textarea id="treatmentPlan" v-model="localData.diagnosis_management.treatment_plan"
              placeholder="Detailed treatment approach including immediate interventions, ongoing management..." rows="4" />
          </div>

          <div class="space-y-2">
            <Label for="medications">Medications Prescribed</Label>
            <Textarea id="medications" v-model="localData.diagnosis_management.medications_prescribed"
              placeholder="List all medications with dosage, route, frequency, and duration..." rows="4" />
          </div>

          <div class="space-y-2">
            <Label for="procedures">Procedures/Interventions</Label>
            <Textarea id="procedures" v-model="localData.diagnosis_management.procedures_interventions"
              placeholder="Any procedures performed or planned..." rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="followUp">Follow-up Recommendations</Label>
            <Textarea id="followUp" v-model="localData.diagnosis_management.follow_up_recommendations"
              placeholder="Follow-up schedule, monitoring parameters, patient education..." rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="prognosis">Prognosis</Label>
            <Textarea id="prognosis" v-model="localData.diagnosis_management.prognosis"
              placeholder="Expected outcomes, potential complications..." rows="2" />
          </div>
        </div>
      </div>
    </Card>

    <!-- Learning Outcomes -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          Educational Objectives
        </h3>

        <div class="space-y-4">
          <div class="space-y-2">
            <Label for="learningObjectives">Learning Objectives</Label>
            <Textarea id="learningObjectives" v-model="localData.learning_outcomes.learning_objectives"
              placeholder="What should students learn from this case? List specific objectives..." rows="4" />
          </div>

          <div class="space-y-2">
            <Label for="keyConcepts">Key Concepts</Label>
            <Textarea id="keyConcepts" v-model="localData.learning_outcomes.key_concepts"
              placeholder="Important medical concepts illustrated by this case..." rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="clinicalPearls">Clinical Pearls</Label>
            <Textarea id="clinicalPearls" v-model="localData.learning_outcomes.clinical_pearls"
              placeholder="Important clinical insights, tips, or teaching points..." rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="references">References</Label>
            <Textarea id="references" v-model="localData.learning_outcomes.references"
              placeholder="Relevant literature, guidelines, or resources..." rows="3" />
          </div>
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Card from '@/components/ui/Card.vue'
import Input from '@/components/ui/Input.vue'
import Label from '@/components/ui/Label.vue'
import Textarea from '@/components/ui/Textarea.vue'

const props = defineProps<{
  caseData: any
}>()

const emit = defineEmits<{
  'update:caseData': [any]
}>()

const localData = computed({
  get: () => props.caseData,
  set: (value) => emit('update:caseData', value)
})
</script>
