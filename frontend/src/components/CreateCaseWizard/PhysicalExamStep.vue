<template>
  <div class="space-y-6">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- General Appearance -->
      <Card>
        <div class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            {{ t('createCase.mentalStatus') }}
          </h3>

          <div class="space-y-2">
            <div class="grid grid-cols-2 gap-2">
              <label v-for="status in consciousnessOptions" :key="status.value" class="flex items-center">
                <input type="radio" :value="status.value" v-model="localData.physical_examination.consciousness_level"
                  class="text-blue-600 focus:ring-blue-500" />
                <span class="ml-2 text-sm"> {{ t(`createCase.${status.value}`) }}</span>
              </label>
            </div>
          </div>
        </div>
      </Card>

      <!-- Vital Signs Summary -->
      <Card>
        <div class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            {{ t('createCase.vitalSignsSummary') }}
          </h3>

          <div class="space-y-3">
            <div class="flex justify-between">
              <span class="text-gray-600">{{ t('createCase.temperature') }}:</span>
              <span class="font-medium">{{ localData.physical_examination?.vital_signs_temp || t('createCase.notRecorded') }} (°C)</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">{{ t('createCase.heartRate') }}:</span>
              <span class="font-medium">{{ localData.physical_examination?.vital_signs_hr || t('createCase.notRecorded') }} (bpm)</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">{{ t('createCase.bloodPressure') }}:</span>
              <span class="font-medium">{{ localData.physical_examination?.vital_signs_bp || t('createCase.notRecorded') }} (mmHg)</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">{{ t('createCase.respiratoryRate') }}:</span>
              <span class="font-medium">{{ localData.physical_examination?.vital_signs_rr || t('createCase.notRecorded') }} {{ t('createCase.respiratoryRateUnit') }} </span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">{{ t('createCase.oxygenSaturation') }}:</span>
              <span class="font-medium">{{ localData.physical_examination?.vital_signs_spo2 || t('createCase.notRecorded') }} %</span>
            </div>
          </div>
        </div>
      </Card>
    </div>

    <!-- Systems Review -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-6">
          {{ t('createCase.physicalExaminationBySystem') }}
        </h3>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2">
            <Label for="headNeck">{{ t('createCase.headAndNeck') }}</Label>
            <Textarea id="headNeck" v-model="localData.physical_examination.head_neck" 
              :placeholder="t('createCase.heentPlaceholder')" rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="cardiovascular">{{ t('createCase.cardiovascular') }}</Label>
            <Textarea id="cardiovascular" v-model="localData.physical_examination.cardiovascular" 
              :placeholder="t('createCase.cardiovascularPlaceholder')" rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="respiratory">{{ t('createCase.respiratory') }}</Label>
            <Textarea id="respiratory" v-model="localData.physical_examination.respiratory" 
              :placeholder="t('createCase.respiratoryPlaceholder')" rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="abdominal">{{ t('createCase.abdominal') }}</Label>
            <Textarea id="abdominal" v-model="localData.physical_examination.abdominal" 
              :placeholder="t('createCase.abdominalPlaceholder')" rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="neurological">{{ t('createCase.neurological') }}</Label>
            <Textarea id="neurological" v-model="localData.physical_examination.neurological" 
              :placeholder="t('createCase.neurologicalPlaceholder')" rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="musculoskeletal">{{ t('createCase.musculoskeletal') }}</Label>
            <Textarea id="musculoskeletal" v-model="localData.physical_examination.musculoskeletal" 
              :placeholder="t('createCase.musculoskeletalPlaceholder')" rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="skin">{{ t('createCase.skin') }}</Label>
            <Textarea id="skin" v-model="localData.physical_examination.skin" 
              :placeholder="t('createCase.skinPlaceholder')" rows="3" />
          </div>
        </div>
      </div>
    </Card>

    <!-- Additional Physical Exam Notes -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ t('createCase.additionalExaminationNotes') }}
        </h3>

        <div class="space-y-2">
          <Textarea id="examNotes" v-model="localData.physical_examination.other_findings" 
            :placeholder="t('createCase.additionalFindingsPlaceholder')" rows="4" />
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import Card from '@/components/ui/Card.vue'
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

const consciousnessOptions = [
  { value: 'alert', label: 'Alert' },
  { value: 'confused', label: 'Confused' },
  { value: 'lethargic', label: 'Lethargic' },
  { value: 'obtunded', label: 'Obtunded' },
  { value: 'stuporous', label: 'Stuporous' },
  { value: 'comatose', label: 'Comatose' }
]
</script>
