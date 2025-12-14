<template>
  <div class="space-y-6">
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-6">
          {{ t('createCase.vitalSigns') }}
        </h3>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <!-- Temperature -->
          <div class="space-y-2">
            <Label for="temperature">{{ t('createCase.temperature') }} {{ t('createCase.temperatureUnit') }}</Label>
            <Input id="temperature" type="number" step="0.1" v-model.number="localData.physical_examination.vital_signs_temp"
              placeholder="37.0" min="30" max="45" />
          </div>

          <!-- Heart Rate -->
          <div class="space-y-2">
            <Label for="heartRate">{{ t('createCase.heartRate') }} {{ t('createCase.heartRateUnit') }}</Label>
            <Input id="heartRate" type="number" v-model.number="localData.physical_examination.vital_signs_hr" placeholder="72" min="30"
              max="200" />
          </div>

          <!-- Blood Pressure -->
          <div class="space-y-2">
            <Label for="bloodPressure">{{ t('createCase.bloodPressure') }} {{ t('createCase.bloodPressureUnit') }}</Label>
            <div class="flex space-x-2">
              <Input id="bloodPressure" type="text" v-model="localData.physical_examination.vital_signs_bp" placeholder="120/80" />
            </div>
            <p class="text-xs text-gray-500">{{ t('createCase.bloodPressureFormat') }}</p>
          </div>

          <!-- Respiratory Rate -->
          <div class="space-y-2">
            <Label for="respiratoryRate">{{ t('createCase.respiratoryRate') }} {{ t('createCase.respiratoryRateUnit') }}</Label>
            <Input id="respiratoryRate" type="number" v-model.number="localData.physical_examination.vital_signs_rr" placeholder="16"
              min="8" max="60" />
          </div>

          <!-- Oxygen Saturation -->
          <div class="space-y-2">
            <Label for="oxygenSaturation">{{ t('createCase.oxygenSaturation') }} {{ t('createCase.oxygenSaturationUnit') }}</Label>
            <Input id="oxygenSaturation" type="number" v-model.number="localData.physical_examination.vital_signs_spo2" placeholder="98"
              min="70" max="100" />
          </div>

          <!-- Weight -->
          <div class="space-y-2">
            <Label for="weight">{{ t('createCase.weight') }} {{ t('createCase.weightUnit') }}</Label>
            <Input id="weight" type="number" step="0.1" v-model.number="localData.physical_examination.weight_kg" placeholder="70" min="10"
              max="300" />
          </div>

          <!-- Height -->
          <div class="space-y-2">
            <Label for="height">{{ t('createCase.height') }} {{ t('createCase.heightUnit') }}</Label>
            <Input id="height" type="number" step="0.1" v-model.number="localData.physical_examination.height_cm" placeholder="170" min="50"
              max="250" />
          </div>

          <!-- BMI -->
          <div class="space-y-2">
            <Label for="bmi">{{ t('createCase.bmi') }} {{ t('createCase.bmiUnit') }}</Label>
            <Input id="bmi" type="number" step="0.1" :value="calculatedBMI" readonly class="bg-gray-50"
              :placeholder="t('createCase.autoCalculated')" />
          </div>
        </div>

        <div class="mt-6 space-y-4">
          <div class="space-y-2">
            <Label for="generalAppearance">Ngoại hình chung (General Appearance)</Label>
            <Textarea id="generalAppearance" v-model="localData.physical_examination.general_appearance"
              placeholder="Mô tả ngoại hình và tình trạng chung của bệnh nhân..." rows="2" />
          </div>

          <div class="space-y-2">
            <Label for="vitalSignsNotes">{{ t('createCase.generalAppearanceNotes') }}</Label>
            <Textarea id="vitalSignsNotes" v-model="localData.physical_examination.vital_signs"
              :placeholder="t('createCase.generalAppearanceNotesPlaceholder')" rows="3" />
          </div>
        </div>
      </div>
    </Card>

    <Card v-if="calculatedBMI" class="bg-blue-50 border-blue-200">
      <div class="p-4">
        <div class="flex items-center space-x-2">
          <span class="text-sm font-medium text-blue-900">
            {{ t('createCase.bmiCategory') }}: {{ getTranslatedBMICategory() }}
          </span>
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

const { t } = useI18n()

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
  const weight = localData.value.physical_examination?.weight_kg
  const height = localData.value.physical_examination?.height_cm

  if (weight && height && height > 0) {
    // BMI = weight (kg) / (height (m))^2
    const heightInMeters = height / 100
    const bmi = weight / (heightInMeters * heightInMeters)
    const roundedBMI = Math.round(bmi * 10) / 10
    
    // Save BMI to the data model
    if (localData.value.physical_examination) {
      localData.value.physical_examination.bmi = roundedBMI
    }
    
    return roundedBMI
  }
  
  // Clear BMI if invalid
  if (localData.value.physical_examination) {
    localData.value.physical_examination.bmi = null
  }
  
  return null
})

const bmiCategory = computed(() => {
  const bmi = calculatedBMI.value
  if (!bmi) return ''

  if (bmi < 18.5) return 'underweight'
  if (bmi < 25) return 'normalWeight'
  if (bmi < 30) return 'overweight'
  return 'obese'
})

const getTranslatedBMICategory = (): string => {
  const category = bmiCategory.value
  if (!category) return ''
  return t(`createCase.${category}`)
}
</script>
