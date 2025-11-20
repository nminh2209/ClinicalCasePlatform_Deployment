<template>
  <div class="space-y-6">
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-6">Case Information</h3>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2 md:col-span-2">
            <Label for="title">Case Title *</Label>
            <Input id="title" v-model="localData.title" placeholder="Enter case title"
              :error="errors.title" />
          </div>

          <div class="space-y-2 md:col-span-2">
            <Label for="patientName">Patient Name *</Label>
            <Input id="patientName" v-model="localData.patient_name" placeholder="Enter patient name (can be anonymized)"
              :error="errors.patient_name" />
          </div>

          <div class="space-y-2">
            <Label for="specialty">Specialty *</Label>
            <Input id="specialty" v-model="localData.specialty" placeholder="e.g., Cardiology, Neurology"
              :error="errors.specialty" />
          </div>

          <div class="space-y-2">
            <Label for="complexity">Complexity Level</Label>
            <select id="complexity" v-model="localData.complexity_level"
              class="w-full px-3 py-2 border border-gray-300 rounded-md">
              <option value="basic">Basic</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
              <option value="expert">Expert</option>
            </select>
          </div>
        </div>
      </div>
    </Card>

    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-6">Patient Demographics</h3>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2">
            <Label for="age">Age *</Label>
            <Input id="age" type="number" v-model.number="localData.patient_age" placeholder="Patient age"
              :error="errors.patient_age" min="0" max="150" />
          </div>

          <div class="space-y-2">
            <Label for="gender">Gender *</Label>
            <select id="gender" v-model="localData.patient_gender"
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
              :class="{ 'border-red-500': errors.patient_gender }">
              <option value="">Select gender</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
            <p v-if="errors.patient_gender" class="text-sm text-red-600">{{ errors.patient_gender }}</p>
          </div>

          <div class="space-y-2">
            <Label for="mrn">Medical Record Number</Label>
            <Input id="mrn" v-model="localData.medical_record_number" placeholder="MRN (anonymized)" />
          </div>

          <div class="space-y-2">
            <Label for="ethnicity">Ethnicity</Label>
            <Input id="ethnicity" v-model="localData.patient_ethnicity" placeholder="Patient ethnicity" />
          </div>

          <div class="space-y-2">
            <Label for="occupation">Occupation</Label>
            <Input id="occupation" v-model="localData.patient_occupation" placeholder="Patient occupation" />
          </div>

          <div class="space-y-2">
            <Label for="admission">Admission Date</Label>
            <Input id="admission" type="date" v-model="localData.admission_date" />
          </div>
        </div>
      </div>
    </Card>

    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-6">Clinical Presentation</h3>

        <div class="space-y-6">
          <div class="space-y-2">
            <Label for="chief_complaint">Chief Complaint *</Label>
            <Textarea id="chief_complaint" v-model="localData.clinical_history.chief_complaint"
              placeholder="Main reason for patient presentation" :error="errors.chief_complaint" rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="chief_complaintBrief">Brief Chief Complaint</Label>
            <Input id="chief_complaintBrief" v-model="localData.chief_complaint_brief"
              placeholder="One-line summary" />
          </div>

          <div class="space-y-2">
            <Label for="historyPresent">History of Present Illness</Label>
            <Textarea id="historyPresent" v-model="localData.clinical_history.history_present_illness"
              placeholder="Detailed history of current illness" rows="6" />
          </div>

          <div class="space-y-2">
            <Label for="pastMedical">Past Medical History</Label>
            <Textarea id="pastMedical" v-model="localData.clinical_history.past_medical_history"
              placeholder="Previous medical conditions" rows="4" />
          </div>

          <div class="space-y-2">
            <Label for="medications">Current Medications</Label>
            <Textarea id="medications" v-model="localData.clinical_history.medications"
              placeholder="List current medications" rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="allergies">Allergies</Label>
            <Textarea id="allergies" v-model="localData.clinical_history.allergies"
              placeholder="Known allergies" rows="2" />
          </div>
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import Card from '@/components/ui/Card.vue'
import Input from '@/components/ui/Input.vue'
import Label from '@/components/ui/Label.vue'
import Textarea from '@/components/ui/Textarea.vue'

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
