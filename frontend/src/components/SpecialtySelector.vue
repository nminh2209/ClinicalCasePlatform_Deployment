<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'

interface Department {
  id: number
  name: string
  vietnamese_name: string
}

interface Specialty {
  id: number
  name: string
  english_name: string
  department: number
  department_name: string
  icon: string
  color: string
}

interface Props {
  modelValue?: number | null
  departmentId?: number | null
  label?: string
  required?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  label: 'Chuyên khoa',
  required: false
})

const emit = defineEmits<{
  'update:modelValue': [value: number | null]
  'update:departmentId': [value: number | null]
  'specialty-selected': [specialty: Specialty | null]
}>()

const departments = ref<Department[]>([])
const specialties = ref<Specialty[]>([])
const allSpecialties = ref<Specialty[]>([])
const selectedDepartment = ref<number | null>(props.departmentId || null)
const selectedSpecialty = ref<number | null>(props.modelValue || null)
const loading = ref(false)
const error = ref<string | null>(null)

// Load departments and specialties
onMounted(async () => {
  await loadDepartments()
  await loadSpecialties()
})

async function loadDepartments() {
  try {
    loading.value = true
    const response = await api.get('/api/cases/departments/')
    departments.value = response.data
  } catch (err) {
    error.value = 'Failed to load departments'
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function loadSpecialties() {
  try {
    loading.value = true
    const response = await api.get('/api/cases/specialties/')
    allSpecialties.value = response.data
    filterSpecialties()
  } catch (err) {
    error.value = 'Failed to load specialties'
    console.error(err)
  } finally {
    loading.value = false
  }
}

function filterSpecialties() {
  if (selectedDepartment.value) {
    specialties.value = allSpecialties.value.filter(
      s => s.department === selectedDepartment.value
    )
  } else {
    specialties.value = allSpecialties.value
  }
}

function onDepartmentChange() {
  selectedSpecialty.value = null
  filterSpecialties()
  emit('update:departmentId', selectedDepartment.value)
  emit('update:modelValue', null)
  emit('specialty-selected', null)
}

function onSpecialtyChange() {
  emit('update:modelValue', selectedSpecialty.value)
  const specialty = specialties.value.find(s => s.id === selectedSpecialty.value)
  emit('specialty-selected', specialty || null)
}

const selectedSpecialtyData = computed(() => {
  return specialties.value.find(s => s.id === selectedSpecialty.value)
})
</script>

<template>
  <div class="specialty-selector">
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div class="row">
      <!-- Department Selector -->
      <div class="col-md-6 mb-3">
        <label class="form-label">Khoa</label>
        <select v-model="selectedDepartment" class="form-select" @change="onDepartmentChange" :disabled="loading">
          <option :value="null">-- Tất cả khoa --</option>
          <option v-for="dept in departments" :key="dept.id" :value="dept.id">
            {{ dept.vietnamese_name || dept.name }}
          </option>
        </select>
      </div>

      <!-- Specialty Selector -->
      <div class="col-md-6 mb-3">
        <label class="form-label">
          {{ label }}
          <span v-if="required" class="text-danger">*</span>
        </label>
        <select v-model="selectedSpecialty" class="form-select" @change="onSpecialtyChange"
          :disabled="loading || specialties.length === 0" :required="required">
          <option :value="null">-- Chọn chuyên khoa --</option>
          <option v-for="specialty in specialties" :key="specialty.id" :value="specialty.id">
            <i v-if="specialty.icon" :class="`fas fa-${specialty.icon}`"></i>
            {{ specialty.name }}
          </option>
        </select>
      </div>
    </div>

    <!-- Selected Specialty Info -->
    <div v-if="selectedSpecialtyData" class="specialty-info p-3 rounded mb-3"
      :style="{ borderLeft: `4px solid ${selectedSpecialtyData.color || '#007bff'}` }">
      <div class="d-flex align-items-center">
        <i v-if="selectedSpecialtyData.icon" :class="`fas fa-${selectedSpecialtyData.icon} fa-2x me-3`"
          :style="{ color: selectedSpecialtyData.color || '#007bff' }">
        </i>
        <div>
          <h6 class="mb-1">{{ selectedSpecialtyData.name }}</h6>
          <small class="text-muted">
            {{ selectedSpecialtyData.department_name }} •
            {{ selectedSpecialtyData.english_name }}
          </small>
        </div>
      </div>
    </div>

    <div v-if="loading" class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.specialty-selector {
  margin-bottom: 1rem;
}

.specialty-info {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
}

.form-select:disabled {
  background-color: #e9ecef;
  cursor: not-allowed;
}
</style>
