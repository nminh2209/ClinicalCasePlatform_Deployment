<template>
  <div class="space-y-6">
    <div class="text-center">
      <h2 class="text-2xl font-bold text-gray-900 mb-2">
        {{ $t('createCase.basicInformation') }}
      </h2>
      <p class="text-gray-600">
        {{ $t('createCase.basicInfoDescription') }}
      </p>
    </div>

    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-6">
          {{ $t('createCase.patientDemographics') }}
        </h3>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2">
            <Label for="firstName">{{ $t('createCase.firstName') }} *</Label>
            <Input id="firstName" v-model="patientData.firstName" :placeholder="$t('createCase.enterFirstName')"
              :error="errors.firstName" />
          </div>

          <div class="space-y-2">
            <Label for="lastName">{{ $t('createCase.lastName') }} *</Label>
            <Input id="lastName" v-model="patientData.lastName" :placeholder="$t('createCase.enterLastName')"
              :error="errors.lastName" />
          </div>

          <div class="space-y-2">
            <Label for="age">{{ $t('createCase.age') }} *</Label>
            <Input id="age" type="number" v-model.number="patientData.age" :placeholder="$t('createCase.enterAge')"
              :error="errors.age" min="0" max="150" />
          </div>

          <div class="space-y-2">
            <Label for="gender">{{ $t('createCase.gender') }} *</Label>
            <select id="gender" v-model="patientData.gender"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.gender }">
              <option value="">{{ $t('createCase.selectGender') }}</option>
              <option value="male">{{ $t('createCase.male') }}</option>
              <option value="female">{{ $t('createCase.female') }}</option>
              <option value="other">{{ $t('createCase.other') }}</option>
            </select>
            <p v-if="errors.gender" class="text-sm text-red-600">{{ errors.gender }}</p>
          </div>

          <div class="space-y-2">
            <Label for="mrn">{{ $t('createCase.medicalRecordNumber') }}</Label>
            <Input id="mrn" v-model="patientData.mrn" :placeholder="$t('createCase.enterMRN')" />
          </div>

          <div class="space-y-2">
            <Label for="dateOfBirth">{{ $t('createCase.dateOfBirth') }}</Label>
            <Input id="dateOfBirth" type="date" v-model="patientData.dateOfBirth" />
          </div>
        </div>
      </div>
    </Card>

    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-6">
          {{ $t('createCase.clinicalPresentation') }}
        </h3>

        <div class="space-y-6">
          <div class="space-y-2">
            <Label for="chiefComplaint">{{ $t('createCase.chiefComplaint') }} *</Label>
            <Textarea id="chiefComplaint" v-model="caseData.chiefComplaint"
              :placeholder="$t('createCase.describeChiefComplaint')" :error="errors.chiefComplaint" rows="4" />
          </div>

          <div class="space-y-2">
            <Label for="historyOfPresentIllness">{{ $t('createCase.historyOfPresentIllness') }}</Label>
            <Textarea id="historyOfPresentIllness" v-model="caseData.historyOfPresentIllness"
              :placeholder="$t('createCase.describeHPI')" rows="6" />
          </div>

          <div class="space-y-2">
            <Label for="pastMedicalHistory">{{ $t('createCase.pastMedicalHistory') }}</Label>
            <Textarea id="pastMedicalHistory" v-model="caseData.pastMedicalHistory"
              :placeholder="$t('createCase.describePMH')" rows="4" />
          </div>
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

const { t } = useI18n()

interface Patient {
  firstName?: string
  lastName?: string
  age?: number
  gender?: string
  mrn?: string
  dateOfBirth?: string
}

interface CaseData {
  patient?: Patient
  chiefComplaint?: string
  historyOfPresentIllness?: string
  pastMedicalHistory?: string
}

const props = defineProps<{
  caseData: CaseData
}>()

interface Errors {
  firstName?: string
  lastName?: string
  age?: string
  gender?: string
  chiefComplaint?: string
}

const emit = defineEmits<{
  'update:caseData': [CaseData]
  'validation-changed': [boolean]
}>()

const patientData = computed({
  get: () => props.caseData.patient || {},
  set: (value) => emit('update:caseData', {
    ...props.caseData,
    patient: value
  })
})

const errors = ref<Errors>({})

const validateStep = () => {
  errors.value = {}

  if (!patientData.value.firstName?.trim()) {
    errors.value.firstName = t('createCase.firstNameRequired')
  }

  if (!patientData.value.lastName?.trim()) {
    errors.value.lastName = t('createCase.lastNameRequired')
  }

  if (!patientData.value.age || patientData.value.age < 0 || patientData.value.age > 150) {
    errors.value.age = t('createCase.validAgeRequired')
  }

  if (!patientData.value.gender) {
    errors.value.gender = t('createCase.genderRequired')
  }

  if (!props.caseData.chiefComplaint?.trim()) {
    errors.value.chiefComplaint = t('createCase.chiefComplaintRequired')
  }

  return Object.keys(errors.value).length === 0
}

// Watch for changes and emit validation status
watch([patientData, () => props.caseData.chiefComplaint], () => {
  emit('validation-changed', validateStep())
}, { deep: true })

// Expose validation function
defineExpose({
  validateStep
})
</script>
