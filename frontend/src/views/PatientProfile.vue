<template>
  <div class="p-6 space-y-6">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <!-- Content -->
    <div v-else-if="caseData" class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center gap-4">
          <Button variant="outline" size="icon" @click="router.push('/patients')">
            <ArrowLeft class="w-5 h-5" />
          </Button>
          <div>
            <h1 class="text-2xl font-bold text-gray-800">Patient Medical Record</h1>
          </div>
        </div>
        <div class="flex gap-2">
          <Button variant="outline" @click="handlePrint">
            <Printer class="w-4 h-4 mr-2" />
            Print Summary
          </Button>
        </div>
      </div>

      <!-- Title and Specialty -->
      <div class="text-center border-b pb-4 mb-6">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">{{ caseData.title }}</h1>
        <Badge variant="secondary" class="text-lg px-4 py-2">{{ caseData.specialty }}</Badge>
      </div>

      <!-- Patient Info Card -->
      <div class="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500 mb-6">
        <h3 class="text-lg font-semibold text-gray-800 mb-3">👤 Patient Information</h3>
        <div class="grid grid-cols-2 gap-3 text-sm">
          <div><span class="font-medium">Name:</span> {{ caseData.patient_name || 'Not entered' }}</div>
          <div><span class="font-medium">Age:</span> {{ caseData.patient_age || 'Not entered' }}</div>
          <div><span class="font-medium">Gender:</span> {{ formatGender(caseData.patient_gender) }}</div>
          <div><span class="font-medium">MRN:</span> {{ caseData.medical_record_number || 'Not entered' }}</div>
          <div v-if="caseData.patient_ethnicity"><span class="font-medium">Ethnicity:</span> {{ caseData.patient_ethnicity }}</div>
          <div v-if="caseData.patient_occupation"><span class="font-medium">Occupation:</span> {{ caseData.patient_occupation }}</div>
          <div v-if="caseData.admission_date"><span class="font-medium">Admission:</span> {{ formatDate(caseData.admission_date) }}</div>
          <div v-if="caseData.discharge_date"><span class="font-medium">Discharge:</span> {{ formatDate(caseData.discharge_date) }}</div>
          <div>
            <span class="font-medium">Status:</span> 
            <span :class="getStatusClass(caseData.case_status)" class="ml-2">
              {{ formatStatus(caseData.case_status) }}
            </span>
          </div>
        </div>
      </div>

      <!-- Clinical History -->
      <div class="mb-6">
        <h3 class="text-xl font-bold text-gray-800 mb-3 border-b pb-2">📋 Clinical History</h3>
        
        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Chief Complaint</h4>
          <p class="text-gray-700 bg-gray-50 p-3 rounded-lg">{{ caseData.clinical_history?.chief_complaint || 'Not entered' }}</p>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">History of Present Illness</h4>
          <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line">{{ caseData.clinical_history?.history_present_illness || 'Not entered' }}</div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Past Medical History</h4>
          <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line">{{ caseData.clinical_history?.past_medical_history || 'Not entered' }}</div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Current Medications</h4>
          <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line">{{ caseData.clinical_history?.medications || 'Not entered' }}</div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Allergies</h4>
          <p class="text-gray-700 bg-gray-50 p-3 rounded-lg">{{ caseData.clinical_history?.allergies || 'Not entered' }}</p>
        </div>
      </div>

      <!-- Physical Examination -->
      <div class="mb-6">
        <h3 class="text-xl font-bold text-gray-800 mb-3 border-b pb-2">🩺 Physical Examination</h3>
        
        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">General Appearance</h4>
          <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line">{{ caseData.physical_examination?.general_appearance || 'Not entered' }}</div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Vital Signs</h4>
          <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line">{{ caseData.physical_examination?.vital_signs || 'Not entered' }}</div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Cardiovascular</h4>
          <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line">{{ caseData.physical_examination?.cardiovascular || 'Not entered' }}</div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Respiratory</h4>
          <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line">{{ caseData.physical_examination?.respiratory || 'Not entered' }}</div>
        </div>
      </div>

      <!-- Investigations -->
      <div class="mb-6">
        <h3 class="text-xl font-bold text-gray-800 mb-3 border-b pb-2">🧪 Laboratory & Investigations</h3>
        
        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Laboratory Results</h4>
          <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line font-mono text-sm">{{ caseData.detailed_investigations?.laboratory_results || 'Not entered' }}</div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Imaging Studies</h4>
          <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line">{{ caseData.detailed_investigations?.imaging_studies || 'Not entered' }}</div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">ECG Findings</h4>
          <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line">{{ caseData.detailed_investigations?.ecg_findings || 'Not entered' }}</div>
        </div>
      </div>

      <!-- Diagnosis & Management -->
      <div class="mb-6">
        <h3 class="text-xl font-bold text-gray-800 mb-3 border-b pb-2">💊 Diagnosis & Management</h3>
        
        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Primary Diagnosis</h4>
          <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line">{{ caseData.diagnosis_management?.primary_diagnosis || 'Not entered' }}</div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Treatment Plan (from form)</h4>
          <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line">{{ caseData.diagnosis_management?.treatment_plan || 'Not entered' }}</div>
        </div>
      </div>

      <!-- Medical Attachments -->
      <div v-if="caseData.medical_attachments && caseData.medical_attachments.length > 0" class="mb-6">
        <h3 class="text-xl font-bold text-gray-800 mb-3 border-b pb-2">📎 Medical Attachments ({{ caseData.medical_attachments.length }})</h3>
        <div class="space-y-4">
          <div v-for="attachment in caseData.medical_attachments" :key="attachment.id"
            class="border border-gray-200 rounded-lg p-4">
            <div class="mb-3">
              <p class="font-semibold text-gray-900 mb-2 text-lg">{{ attachment.title }}</p>
            </div>
            <div class="bg-gray-50 p-3 rounded-lg space-y-2">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm">
                <div v-if="attachment.attachment_type">
                  <span class="font-medium text-gray-700">Type:</span>
                  <span class="text-gray-600 ml-1">{{ attachment.attachment_type_display }}</span>
                </div>
                <div v-if="attachment.date_taken">
                  <span class="font-medium text-gray-700">Date Taken:</span>
                  <span class="text-gray-600 ml-1">{{ formatDate(attachment.date_taken) }}</span>
                </div>
              </div>
              <div v-if="attachment.description" class="pt-2 border-t border-gray-200">
                <span class="font-medium text-gray-700 text-sm">Description:</span>
                <p class="text-gray-600 text-sm mt-1">{{ attachment.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Learning Outcomes -->
      <div v-if="caseData.learning_outcomes" class="border-t pt-6">
        <h2 class="text-xl font-bold text-gray-800 mb-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white p-3 rounded-lg">🎓 Learning Outcomes</h2>

        <!-- Learning Objectives -->
        <div class="mb-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-2">Learning Objectives</h3>
          <div class="text-gray-700 bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500 whitespace-pre-line">
            {{ caseData.learning_outcomes.learning_objectives || 'Not specified' }}
          </div>
        </div>

        <!-- Key Concepts -->
        <div class="mb-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-2">Key Concepts</h3>
          <div class="text-gray-700 bg-yellow-50 p-4 rounded-lg border-l-4 border-yellow-500 whitespace-pre-line">
            {{ caseData.learning_outcomes.key_concepts || 'Not specified' }}
          </div>
        </div>

        <!-- Clinical Pearls -->
        <div class="mb-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-2">Clinical Pearls</h3>
          <div class="text-gray-700 bg-purple-50 p-4 rounded-lg border-l-4 border-purple-500 whitespace-pre-line">
            {{ caseData.learning_outcomes.clinical_pearls || 'Not specified' }}
          </div>
        </div>

        <!-- References -->
        <div v-if="caseData.learning_outcomes.references" class="mb-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-2">References</h3>
          <div class="text-gray-700 bg-green-50 p-4 rounded-lg border-l-4 border-green-500 whitespace-pre-line">
            {{ caseData.learning_outcomes.references }}
          </div>
        </div>
      </div>
    </div>

    <!-- Error State -->
    <div v-else class="text-center py-12">
      <p class="text-gray-500">Patient case not found</p>
      <Button variant="outline" @click="router.push('/patients')" class="mt-4">
        Back to Patient Records
      </Button>
    </div>
  </div>

</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Button from '@/components/ui/Button.vue'
import Badge from '@/components/ui/Badge.vue'
import { ArrowLeft, Printer } from '@/components/icons'
import { requireRoles } from '@/composables/useAuthorize'
import { casesService } from '@/services/cases'

const router = useRouter()
const route = useRoute()
requireRoles(['student','instructor'])

const activeTab = ref('overview')
const loading = ref(false)
const caseData = ref<any>(null)

// Get case ID from route params
const caseId = route.params.id as string

async function loadPatientCase() {
  if (!caseId) return
  
  loading.value = true
  try {
    caseData.value = await casesService.getCase(caseId)
  } catch (error) {
    console.error('Failed to load patient case:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadPatientCase()
})

function formatDate(dateStr: string | null) {
  if (!dateStr) return 'N/A'
  return new Date(dateStr).toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
}

function formatGender(gender: string) {
  const genderMap: Record<string, string> = {
    'male': 'Male',
    'female': 'Female',
    'other': 'Other',
    'not_specified': 'Not Specified'
  }
  return genderMap[gender] || gender
}

function formatStatus(status: string) {
  const statusMap: Record<string, string> = {
    'draft': 'Draft',
    'submitted': 'Submitted',
    'reviewed': 'Reviewed',
    'approved': 'Approved'
  }
  return statusMap[status] || status
}

function getStatusClass(status: string) {
  const classMap: Record<string, string> = {
    'draft': 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800',
    'submitted': 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800',
    'reviewed': 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800',
    'approved': 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800'
  }
  return classMap[status] || 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600'
}

const handleSave = () => {
  alert("This is a read-only view. Use the case editor to make changes.")
}

const handlePrint = () => {
  window.print()
}
</script>
