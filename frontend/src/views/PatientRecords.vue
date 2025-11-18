<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">Patient Records</h1>
        <p class="text-sm text-gray-500">View and manage all patient medical records</p>
      </div>
    </div>

    <!-- Search and Filters -->
    <Card>
      <CardContent class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="md:col-span-2 relative">
            <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <Input v-model="searchQuery" type="text" placeholder="Search by patient name, MRN, specialty..."
              class="pl-10" />
          </div>
          <select v-model="specialtyFilter"
            class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="all">All Specialties</option>
            <option v-for="spec in availableSpecialties" :key="spec" :value="spec">{{ spec }}</option>
          </select>
        </div>
      </CardContent>
    </Card>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <!-- Patients Table -->
    <Card v-else class="bg-white">
      <CardHeader>
        <CardTitle>Patient Records ({{ filteredPatients.length }})</CardTitle>
      </CardHeader>
      <CardContent>
        <div v-if="filteredPatients.length === 0" class="text-center py-12">
          <p class="text-gray-500">No patient records found</p>
        </div>
        <div v-else class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b">
                <th class="text-left p-3 font-medium text-gray-700">MRN</th>
                <th class="text-left p-3 font-medium text-gray-700">Patient Name</th>
                <th class="text-left p-3 font-medium text-gray-700">Age</th>
                <th class="text-left p-3 font-medium text-gray-700">Gender</th>
                <th class="text-left p-3 font-medium text-gray-700">Specialty</th>
                <th class="text-left p-3 font-medium text-gray-700">Admission Date</th>
                <th class="text-left p-3 font-medium text-gray-700">Status</th>
                <th class="text-left p-3 font-medium text-gray-700">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="patient in filteredPatients" :key="patient.id"
                class="border-b hover:bg-gray-50 transition-colors">
                <td class="p-3 font-mono text-sm">{{ patient.medical_record_number || 'N/A' }}</td>
                <td class="p-3 font-medium">{{ patient.patient_name || 'N/A' }}</td>
                <td class="p-3">{{ patient.patient_age || 'N/A' }}</td>
                <td class="p-3 capitalize">{{ formatGender(patient.patient_gender) }}</td>
                <td class="p-3">{{ patient.specialty || 'N/A' }}</td>
                <td class="p-3">{{ formatDate(patient.admission_date) }}</td>
                <td class="p-3">
                  <span :class="getStatusClass(patient.case_status)">
                    {{ formatStatus(patient.case_status) }}
                  </span>
                </td>
                <td class="p-3">
                  <Button variant="ghost" size="sm" @click="handleViewPatient(patient.id)"
                    class="text-blue-600 hover:text-blue-700">
                    <Eye class="w-4 h-4 mr-1" />
                    View
                  </Button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { requireRoles } from '@/composables/useAuthorize'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import Badge from '@/components/ui/Badge.vue'
import { Eye } from '@/components/icons'
import { Search } from 'lucide-vue-next'
import { casesService } from '@/services/cases'

const router = useRouter()
requireRoles(['student','instructor'])

const searchQuery = ref('')
const specialtyFilter = ref('all')
const loading = ref(false)
const cases = ref<any[]>([])

const availableSpecialties = computed(() => {
  const specs = new Set(cases.value.map(c => c.specialty).filter(Boolean))
  return Array.from(specs).sort()
})

const filteredPatients = computed(() => {
  return cases.value.filter((patient) => {
    const matchesSearch =
      patient.patient_name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      patient.medical_record_number?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      patient.specialty?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      patient.title?.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesSpecialty = specialtyFilter.value === 'all' || patient.specialty === specialtyFilter.value
    return matchesSearch && matchesSpecialty
  })
})

async function loadPatientRecords() {
  loading.value = true
  try {
    const response = await casesService.getCases()
    cases.value = response.results || response
  } catch (error) {
    console.error('Failed to load patient records:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadPatientRecords()
})

function formatDate(dateStr: string | null) {
  if (!dateStr) return 'N/A'
  return new Date(dateStr).toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
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

function getStatusVariant(status: string) {
  return status === 'approved' ? 'default' : 'secondary'
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

const handleViewPatient = (caseId: string) => {
  router.push(`/patients/${caseId}`)
}
</script>
