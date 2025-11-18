<template>
  <div class="space-y-6">
    <div class="text-center">
      <h2 class="text-2xl font-bold text-gray-900 mb-2">
        {{ $t('createCase.vitalSigns') }}
      </h2>
      <p class="text-gray-600">
        {{ $t('createCase.vitalSignsDescription') }}
      </p>
    </div>

    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-6">
          {{ $t('createCase.recordVitalSigns') }}
        </h3>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div class="space-y-2">
            <Label for="temperature">{{ $t('createCase.temperature') }} (°F)</Label>
            <Input id="temperature" type="number" step="0.1" v-model.number="vitalSigns.temperature"
              :placeholder="'98.6'" min="90" max="110" />
          </div>

          <div class="space-y-2">
            <Label for="heartRate">{{ $t('createCase.heartRate') }} (bpm)</Label>
            <Input id="heartRate" type="number" v-model.number="vitalSigns.heartRate" :placeholder="'72'" min="30"
              max="200" />
          </div>

          <div class="space-y-2">
            <Label for="bloodPressureSystolic">{{ $t('createCase.bloodPressure') }}</Label>
            <div class="flex space-x-2">
              <Input type="number" v-model.number="vitalSigns.bloodPressureSystolic" :placeholder="'120'" min="70"
                max="250" class="flex-1" />
              <span class="flex items-center text-gray-500">/</span>
              <Input type="number" v-model.number="vitalSigns.bloodPressureDiastolic" :placeholder="'80'" min="40"
                max="150" class="flex-1" />
            </div>
          </div>

          <div class="space-y-2">
            <Label for="respiratoryRate">{{ $t('createCase.respiratoryRate') }} (breaths/min)</Label>
            <Input id="respiratoryRate" type="number" v-model.number="vitalSigns.respiratoryRate" :placeholder="'16'"
              min="8" max="60" />
          </div>

          <div class="space-y-2">
            <Label for="oxygenSaturation">{{ $t('createCase.oxygenSaturation') }} (%)</Label>
            <Input id="oxygenSaturation" type="number" v-model.number="vitalSigns.oxygenSaturation" :placeholder="'98'"
              min="70" max="100" />
          </div>

          <div class="space-y-2">
            <Label for="weight">{{ $t('createCase.weight') }} (lbs)</Label>
            <Input id="weight" type="number" step="0.1" v-model.number="vitalSigns.weight" :placeholder="'150'" min="50"
              max="500" />
          </div>

          <div class="space-y-2">
            <Label for="height">{{ $t('createCase.height') }} (inches)</Label>
            <Input id="height" type="number" step="0.1" v-model.number="vitalSigns.height" :placeholder="'68'" min="36"
              max="84" />
          </div>

          <div class="space-y-2">
            <Label for="bmi">{{ $t('createCase.bmi') }}</Label>
            <Input id="bmi" type="number" step="0.1" :value="calculatedBMI" readonly class="bg-gray-50"
              :placeholder="'Auto-calculated'" />
          </div>

          <div class="space-y-2">
            <Label for="painScale">{{ $t('createCase.painScale') }} (0-10)</Label>
            <Input id="painScale" type="number" v-model.number="vitalSigns.painScale" :placeholder="'0'" min="0"
              max="10" />
          </div>
        </div>

        <div class="mt-6">
          <div class="space-y-2">
            <Label for="vitalSignsNotes">{{ $t('createCase.additionalNotes') }}</Label>
            <Textarea id="vitalSignsNotes" v-model="vitalSigns.notes"
              :placeholder="$t('createCase.vitalSignsNotesPlaceholder')" rows="3" />
          </div>
        </div>
      </div>
    </Card>

    <Card v-if="calculatedBMI" class="bg-blue-50 border-blue-200">
      <div class="p-4">
        <div class="flex items-center space-x-2">
          <InfoIcon class="w-5 h-5 text-blue-600" />
          <span class="text-sm font-medium text-blue-900">
            BMI Category: {{ bmiCategory }}
          </span>
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
import { InfoIcon } from '@/components/icons'

const { t } = useI18n()

const props = defineProps({
  caseData: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:caseData'])

const vitalSigns = computed({
  get: () => props.caseData.vitalSigns || {},
  set: (value) => emit('update:caseData', {
    ...props.caseData,
    vitalSigns: value
  })
})

const calculatedBMI = computed(() => {
  const weight = vitalSigns.value.weight
  const height = vitalSigns.value.height

  if (weight && height && height > 0) {
    // BMI = (weight in lbs * 703) / (height in inches)^2
    const bmi = (weight * 703) / (height * height)
    return Math.round(bmi * 10) / 10
  }
  return null
})

const bmiCategory = computed(() => {
  const bmi = calculatedBMI.value
  if (!bmi) return ''

  if (bmi < 18.5) return t('createCase.underweight')
  if (bmi < 25) return t('createCase.normalWeight')
  if (bmi < 30) return t('createCase.overweight')
  return t('createCase.obese')
})

// Update BMI in vital signs when calculated
watch(calculatedBMI, (newBMI) => {
  if (newBMI && vitalSigns.value) {
    vitalSigns.value.bmi = newBMI
  }
})
</script>
