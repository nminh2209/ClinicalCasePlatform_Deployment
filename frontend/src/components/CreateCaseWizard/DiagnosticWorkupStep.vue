<template>
  <div class="space-y-6">
    <div class="text-center">
      <h2 class="text-2xl font-bold text-gray-900 mb-2">
        Diagnostic Investigations
      </h2>
      <p class="text-gray-600">
        Laboratory results, imaging studies, and other diagnostic tests
      </p>
    </div>

    <!-- Laboratory Tests -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          Laboratory Results
        </h3>

        <div class="space-y-4">
          <div class="space-y-2">
            <Label for="labResults">Complete Laboratory Results</Label>
            <Textarea id="labResults" v-model="localData.detailed_investigations.laboratory_results"
              placeholder="Enter all laboratory test results including CBC, CMP, liver function, coagulation studies..." rows="4" />
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div class="space-y-2">
              <Label for="hemoglobin">Hemoglobin (g/dL)</Label>
              <Input id="hemoglobin" type="number" step="0.1" v-model.number="localData.detailed_investigations.hemoglobin_level"
                placeholder="14.0" />
            </div>

            <div class="space-y-2">
              <Label for="wbc">White Blood Cell Count (10^9/L)</Label>
              <Input id="wbc" type="number" step="0.1" v-model.number="localData.detailed_investigations.white_cell_count"
                placeholder="7.5" />
            </div>

            <div class="space-y-2">
              <Label for="platelet">Platelet Count (10^9/L)</Label>
              <Input id="platelet" type="number" step="1" v-model.number="localData.detailed_investigations.platelet_count"
                placeholder="250" />
            </div>

            <div class="space-y-2">
              <Label for="sodium">Sodium (mmol/L)</Label>
              <Input id="sodium" type="number" step="0.1" v-model.number="localData.detailed_investigations.sodium_level"
                placeholder="140" />
            </div>

            <div class="space-y-2">
              <Label for="potassium">Potassium (mmol/L)</Label>
              <Input id="potassium" type="number" step="0.1" v-model.number="localData.detailed_investigations.potassium_level"
                placeholder="4.0" />
            </div>

            <div class="space-y-2">
              <Label for="creatinine">Creatinine (mg/dL)</Label>
              <Input id="creatinine" type="number" step="0.1" v-model.number="localData.detailed_investigations.creatinine_level"
                placeholder="1.0" />
            </div>

            <div class="space-y-2">
              <Label for="glucose">Glucose (mg/dL)</Label>
              <Input id="glucose" type="number" step="1" v-model.number="localData.detailed_investigations.glucose_level"
                placeholder="100" />
            </div>
          </div>
        </div>
      </div>
    </Card>

    <!-- Imaging Studies -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          Imaging Studies
        </h3>

        <div class="space-y-4">
          <div class="space-y-2">
            <Label for="imaging">Imaging Findings</Label>
            <Textarea id="imaging" v-model="localData.detailed_investigations.imaging_studies"
              placeholder="Describe all imaging findings: X-rays, CT scans, MRI, ultrasound, etc..." rows="4" />
          </div>
        </div>
      </div>
    </Card>

    <!-- Other Diagnostic Tests -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          Other Diagnostic Tests
        </h3>

        <div class="space-y-4">
          <div class="space-y-2">
            <Label for="pathology">Pathology Results</Label>
            <Textarea id="pathology" v-model="localData.detailed_investigations.pathology_results"
              placeholder="Biopsy results, histopathology findings..." rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="microbiology">Microbiology Results</Label>
            <Textarea id="microbiology" v-model="localData.detailed_investigations.microbiology_results"
              placeholder="Culture results, sensitivity testing..." rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="otherInvestigations">Additional Investigations</Label>
            <Textarea id="otherInvestigations" v-model="localData.detailed_investigations.other_investigations"
              placeholder="ECG findings, echocardiography, endoscopy, other special tests..." rows="3" />
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
