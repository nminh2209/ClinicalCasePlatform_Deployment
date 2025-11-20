<template>
  <div class="space-y-6">
    <div class="text-center">
      <h2 class="text-2xl font-bold text-gray-900 mb-2">
        {{ $t('createCase.physicalExamination') }}
      </h2>
      <p class="text-gray-600">
        {{ $t('createCase.physicalExamDescription') }}
      </p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- General Appearance -->
      <Card>
        <div class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            {{ $t('createCase.generalAppearance') }}
          </h3>

          <div class="space-y-4">
            <div class="space-y-2">
              <Label for="generalAppearance">{{ $t('createCase.appearance') }}</Label>
              <Textarea id="generalAppearance" v-model="physicalExam.generalAppearance"
                :placeholder="$t('createCase.generalAppearancePlaceholder')" rows="3" />
            </div>

            <div class="space-y-2">
              <Label>{{ $t('createCase.mentalStatus') }}</Label>
              <div class="grid grid-cols-2 gap-2">
                <label v-for="status in mentalStatusOptions" :key="status.value" class="flex items-center">
                  <input type="radio" :value="status.value" v-model="physicalExam.mentalStatus"
                    class="text-blue-600 focus:ring-blue-500" />
                  <span class="ml-2 text-sm">{{ status.label }}</span>
                </label>
              </div>
            </div>
          </div>
        </div>
      </Card>

      <!-- Vital Signs Summary -->
      <Card>
        <div class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            {{ $t('createCase.vitalSignsSummary') }}
          </h3>

          <div class="space-y-3">
            <div class="flex justify-between">
              <span class="text-gray-600">{{ $t('createCase.temperature') }}:</span>
              <span class="font-medium">{{ caseData.vitalSigns?.temperature || 'Not recorded' }}°F</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">{{ $t('createCase.heartRate') }}:</span>
              <span class="font-medium">{{ caseData.vitalSigns?.heartRate || 'Not recorded' }} bpm</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">{{ $t('createCase.bloodPressure') }}:</span>
              <span class="font-medium">
                {{ caseData.vitalSigns?.bloodPressureSystolic || '?' }}/{{ caseData.vitalSigns?.bloodPressureDiastolic
                  || '?' }}
              </span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">{{ $t('createCase.respiratoryRate') }}:</span>
              <span class="font-medium">{{ caseData.vitalSigns?.respiratoryRate || 'Not recorded' }}/min</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">{{ $t('createCase.oxygenSaturation') }}:</span>
              <span class="font-medium">{{ caseData.vitalSigns?.oxygenSaturation || 'Not recorded' }}%</span>
            </div>
          </div>
        </div>
      </Card>
    </div>

    <!-- Systems Review -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-6">
          {{ $t('createCase.systemsReview') }}
        </h3>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="system in bodySystems" :key="system.key" class="space-y-2">
            <Label :for="system.key">{{ system.label }}</Label>
            <Textarea :id="system.key" v-model="physicalExam[system.key]" :placeholder="system.placeholder" rows="2" />
          </div>
        </div>
      </div>
    </Card>

    <!-- Physical Exam Notes -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ $t('createCase.physicalExamNotes') }}
        </h3>

        <div class="space-y-2">
          <Textarea id="examNotes" v-model="physicalExam.notes" :placeholder="$t('createCase.examNotesPlaceholder')"
            rows="4" />
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import Card from '@/components/ui/Card.vue'
import Label from '@/components/ui/Label.vue'
import Textarea from '@/components/ui/Textarea.vue'

const { t } = useI18n()

const props = defineProps({
  caseData: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:caseData'])

const physicalExam = computed({
  get: () => props.caseData.physicalExam || {},
  set: (value) => emit('update:caseData', {
    ...props.caseData,
    physicalExam: value
  })
})

const mentalStatusOptions = [
  { value: 'alert', label: t('createCase.alert') },
  { value: 'confused', label: t('createCase.confused') },
  { value: 'lethargic', label: t('createCase.lethargic') },
  { value: 'unresponsive', label: t('createCase.unresponsive') }
]

const bodySystems = [
  {
    key: 'heent',
    label: t('createCase.heent'),
    placeholder: t('createCase.heentPlaceholder')
  },
  {
    key: 'cardiovascular',
    label: t('createCase.cardiovascular'),
    placeholder: t('createCase.cardiovascularPlaceholder')
  },
  {
    key: 'respiratory',
    label: t('createCase.respiratory'),
    placeholder: t('createCase.respiratoryPlaceholder')
  },
  {
    key: 'gastrointestinal',
    label: t('createCase.gastrointestinal'),
    placeholder: t('createCase.gastrointestinalPlaceholder')
  },
  {
    key: 'genitourinary',
    label: t('createCase.genitourinary'),
    placeholder: t('createCase.genitourinaryPlaceholder')
  },
  {
    key: 'musculoskeletal',
    label: t('createCase.musculoskeletal'),
    placeholder: t('createCase.musculoskeletalPlaceholder')
  },
  {
    key: 'neurological',
    label: t('createCase.neurological'),
    placeholder: t('createCase.neurologicalPlaceholder')
  },
  {
    key: 'skin',
    label: t('createCase.skin'),
    placeholder: t('createCase.skinPlaceholder')
  },
  {
    key: 'psychiatric',
    label: t('createCase.psychiatric'),
    placeholder: t('createCase.psychiatricPlaceholder')
  }
]
</script>
