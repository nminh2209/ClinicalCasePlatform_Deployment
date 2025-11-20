<template>
  <div class="space-y-6">
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-6">{{ t('createCase.caseInformation') }}</h3>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2 md:col-span-2">
            <Label for="title">{{ t('createCase.caseTitle') }} *</Label>
            <Input id="title" v-model="localData.title" :placeholder="t('createCase.enterCaseTitle')"
              :error="getTranslatedError('title')" />
          </div>

          <div class="space-y-2 md:col-span-2">
            <Label for="patientName">{{ t('createCase.patientName') }} *</Label>
            <Input id="patientName" v-model="localData.patient_name" :placeholder="t('createCase.patientName') + ' ' + t('createCase.canBeAnonymized')"
              :error="getTranslatedError('patientName')" />
          </div>

          <div class="space-y-2">
            <Label for="specialty">{{ t('createCase.specialty') }} *</Label>
            <Input id="specialty" v-model="localData.specialty" :placeholder="t('createCase.specialtyExample')"
              :error="getTranslatedError('specialty')" />
          </div>

          <div class="space-y-2">
            <Label for="complexity">{{ t('createCase.complexity') }}</Label>
            <select id="complexity" v-model="localData.complexity_level"
              class="w-full px-3 py-2 border border-gray-300 rounded-md">
              <option value="basic">{{ t('createCase.complexityBasic') }}</option>
              <option value="intermediate">{{ t('createCase.complexityIntermediate') }}</option>
              <option value="advanced">{{ t('createCase.complexityAdvanced') }}</option>
              <option value="expert">{{ t('createCase.complexityExpert') }}</option>
            </select>
          </div>
        </div>
      </div>
    </Card>

    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-6">{{ t('createCase.patientDemographics') }}</h3>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2">
            <Label for="age">{{ t('createCase.age') }} *</Label>
            <Input id="age" type="number" v-model.number="localData.patient_age" :placeholder="t('createCase.patientAge')"
              :error="getTranslatedError('patient_age')" min="0" max="150" />
          </div>

          <div class="space-y-2">
            <Label for="gender">{{ t('createCase.gender') }} *</Label>
            <select id="gender" v-model="localData.patient_gender"
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
              :class="{ 'border-red-500': getTranslatedError('patient_gender') }">
              <option value="">{{ t('createCase.selectGender') }}</option>
              <option value="male">{{ t('createCase.male') }}</option>
              <option value="female">{{ t('createCase.female') }}</option>
              <option value="other">{{ t('createCase.other') }}</option>
            </select>
            <p v-if="getTranslatedError('patient_gender')" class="text-sm text-red-600">{{ getTranslatedError('patient_gender') }}</p>
          </div>

          <div class="space-y-2">
            <Label for="mrn">{{ t('createCase.medicalRecordNumber') }}</Label>
            <Input id="mrn" v-model="localData.medical_record_number" :placeholder="t('createCase.enterMRN')" />
          </div>

          <div class="space-y-2">
            <Label for="ethnicity">{{ t('createCase.ethnicity') }}</Label>
            <Input id="ethnicity" v-model="localData.patient_ethnicity" :placeholder="t('createCase.enterEthnicity')" />
          </div>

          <div class="space-y-2">
            <Label for="occupation">{{ t('createCase.occupation') }}</Label>
            <Input id="occupation" v-model="localData.patient_occupation" :placeholder="t('createCase.enterOccupation')" />
          </div>

          <div class="space-y-2">
            <Label for="admission">{{ t('createCase.admissionDate') }}</Label>
            <Input id="admission" type="date" v-model="localData.admission_date" />
          </div>
        </div>
      </div>
    </Card>

    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-6">{{ t('createCase.clinicalPresentation') }}</h3>

        <div class="space-y-6">
          <div class="space-y-2">
            <Label for="chief_complaint">{{ t('createCase.chief_complaint') }} *</Label>
            <Textarea id="chief_complaint" v-model="localData.clinical_history.chief_complaint"
              :placeholder="t('createCase.describe_chief_complaint')" :error="getTranslatedError('chief_complaint')" rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="chief_complaintBrief">{{ t('createCase.briefChiefComplaint') }}</Label>
            <Input id="chief_complaintBrief" v-model="localData.chief_complaint_brief"
              :placeholder="t('createCase.enterBriefComplaint')" />
          </div>

          <div class="space-y-2">
            <Label for="historyPresent">{{ t('createCase.historyOfPresentIllness') }}</Label>
            <Textarea id="historyPresent" v-model="localData.clinical_history.history_present_illness"
              :placeholder="t('createCase.detailedHistory')" rows="6" />
          </div>

          <div class="space-y-2">
            <Label for="pastMedical">{{ t('createCase.pastMedicalHistory') }}</Label>
            <Textarea id="pastMedical" v-model="localData.clinical_history.past_medical_history"
              :placeholder="t('createCase.describePMH')" rows="4" />
          </div>

          <div class="space-y-2">
            <Label for="medications">{{ t('createCase.currentMedications') }}</Label>
            <Textarea id="medications" v-model="localData.clinical_history.medications"
              :placeholder="t('createCase.listMedications')" rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="allergies">{{ t('createCase.allergies') }}</Label>
            <Textarea id="allergies" v-model="localData.clinical_history.allergies"
              :placeholder="t('createCase.enterAllergies')" rows="2" />
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

const props = defineProps<{
  caseData: any
}>()

const emit = defineEmits<{
  'update:caseData': [any]
  'validation-changed': [boolean]
}>()

const localData = computed({
  get: () => props.caseData,
  set: (value) => emit('update:caseData', value)
})

const errors = ref<Record<string, string>>({})

const getTranslatedError = (field: string): string | undefined => {
  if (!errors.value[field]) return undefined
  
  // Map field names to i18n keys for error messages
  const errorKeyMap: Record<string, string> = {
    title: 'createCase.caseTitleRequired',
    patient_name: 'createCase.patientNameRequired',
    specialty: 'createCase.specialtyRequired',
    patient_age: 'createCase.validAgeRequired',
    patient_gender: 'createCase.genderRequired',
    chief_complaint: 'createCase.chief_complaintRequired',
  }
  
  const keyForError = errorKeyMap[field]
  if (keyForError) {
    return t(keyForError)
  }
  return errors.value[field]
}

const validateStep = () => {
  errors.value = {}

  if (!localData.value.title?.trim()) {
    errors.value.title = 'Case title is required'
  }

  if (!localData.value.patient_name?.trim()) {
    errors.value.patient_name = 'Patient name is required'
  }

  if (!localData.value.specialty?.trim()) {
    errors.value.specialty = 'Specialty is required'
  }

  if (!localData.value.patient_age || localData.value.patient_age < 0 || localData.value.patient_age > 150) {
    errors.value.patient_age = 'Valid age is required'
  }

  if (!localData.value.patient_gender) {
    errors.value.patient_gender = 'Gender is required'
  }

  if (!localData.value.clinical_history?.chief_complaint?.trim()) {
    errors.value.chief_complaint = 'Chief complaint is required'
  }

  return Object.keys(errors.value).length === 0
}

watch(localData, () => {
  emit('validation-changed', validateStep())
}, { deep: true })

defineExpose({
  validateStep
})
</script>
