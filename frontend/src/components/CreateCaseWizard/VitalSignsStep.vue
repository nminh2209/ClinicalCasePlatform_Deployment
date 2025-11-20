<template>
  <div class="space-y-6">
    <div class="text-center">
      <h2 class="text-2xl font-bold text-gray-900 mb-2">
        Vital Signs & Physical Measurements
      </h2>
      <p class="text-gray-600">
        Record the patient's vital signs and basic physical measurements
      </p>
    </div>

    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-6">
          Vital Signs
        </h3>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <!-- Temperature -->
          <div class="space-y-2">
            <Label for="temperature">Temperature (°C)</Label>
            <Input id="temperature" type="number" step="0.1" v-model.number="localData.physical_examination.vital_signs_temp"
              placeholder="37.0" min="30" max="45" />
          </div>

          <!-- Heart Rate -->
          <div class="space-y-2">
            <Label for="heartRate">Heart Rate (bpm)</Label>
            <Input id="heartRate" type="number" v-model.number="localData.physical_examination.vital_signs_hr" placeholder="72" min="30"
              max="200" />
          </div>

          <!-- Blood Pressure -->
          <div class="space-y-2">
            <Label for="bloodPressure">Blood Pressure (mmHg)</Label>
            <div class="flex space-x-2">
              <Input type="number" v-model.number="localData.physical_examination.vital_signs_bp" placeholder="120/80" />
            </div>
            <p class="text-xs text-gray-500">Format: systolic/diastolic (e.g., 120/80)</p>
          </div>

          <!-- Respiratory Rate -->
          <div class="space-y-2">
            <Label for="respiratoryRate">Respiratory Rate (breaths/min)</Label>
            <Input id="respiratoryRate" type="number" v-model.number="localData.physical_examination.vital_signs_rr" placeholder="16"
              min="8" max="60" />
          </div>

          <!-- Oxygen Saturation -->
          <div class="space-y-2">
            <Label for="oxygenSaturation">Oxygen Saturation (%)</Label>
            <Input id="oxygenSaturation" type="number" v-model.number="localData.physical_examination.vital_signs_spo2" placeholder="98"
              min="70" max="100" />
          </div>

          <!-- Weight -->
          <div class="space-y-2">
            <Label for="weight">Weight (kg)</Label>
            <Input id="weight" type="number" step="0.1" v-model.number="localData.physical_examination.vital_signs_weight" placeholder="70" min="10"
              max="300" />
          </div>

          <!-- Height -->
          <div class="space-y-2">
            <Label for="height">Height (cm)</Label>
            <Input id="height" type="number" step="0.1" v-model.number="localData.physical_examination.vital_signs_height" placeholder="170" min="50"
              max="250" />
          </div>

          <!-- BMI -->
          <div class="space-y-2">
            <Label for="bmi">BMI (kg/m²)</Label>
            <Input id="bmi" type="number" step="0.1" :value="calculatedBMI" readonly class="bg-gray-50"
              placeholder="Auto-calculated" />
          </div>
        </div>

        <div class="mt-6">
          <div class="space-y-2">
            <Label for="vitalSignsNotes">General Appearance & Vital Signs Notes</Label>
            <Textarea id="vitalSignsNotes" v-model="localData.physical_examination.vital_signs"
              placeholder="Describe general appearance, vital signs stability, any abnormalities..." rows="3" />
          </div>
        </div>
      </div>
    </Card>

    <Card v-if="calculatedBMI" class="bg-blue-50 border-blue-200">
      <div class="p-4">
        <div class="flex items-center space-x-2">
          <span class="text-sm font-medium text-blue-900">
            BMI Category: {{ bmiCategory }}
          </span>
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

const calculatedBMI = computed(() => {
  const weight = localData.value.physical_examination?.vital_signs_weight
  const height = localData.value.physical_examination?.vital_signs_height

  if (weight && height && height > 0) {
    // BMI = weight (kg) / (height (m))^2
    const heightInMeters = height / 100
    const bmi = weight / (heightInMeters * heightInMeters)
    return Math.round(bmi * 10) / 10
  }
  return null
})

const bmiCategory = computed(() => {
  const bmi = calculatedBMI.value
  if (!bmi) return ''

  if (bmi < 18.5) return 'Underweight'
  if (bmi < 25) return 'Normal Weight'
  if (bmi < 30) return 'Overweight'
  return 'Obese'
})
</script>
