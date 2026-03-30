<template>
  <div class="page-container">
    <!-- Header -->
    <div class="page-header">
      <h1 class="page-title">Hồ sơ Bệnh nhân</h1>
      <p class="page-subtitle">
        Xem và quản lý tất cả hồ sơ bệnh nhân bạn đã tạo.
      </p>
    </div>

    <!-- Search and Filters -->
    <Card class="search-card">
      <template #content>
        <div class="search-content">
          <div class="search-grid">
            <div class="search-field">
              <IconField>
                <InputIcon class="pi pi-search" />
                <InputText
                  v-model="searchQuery"
                  class="w-full"
                  type="text"
                  placeholder="Tìm kiếm theo tên bệnh nhân, MRN, chuyên khoa..."
                />
              </IconField>
            </div>
            <Select
              v-model="specialtyFilter"
              :options="specialtyOptions"
              optionLabel="label"
              optionValue="value"
              class="w-full specialty-select"
              placeholder="Tất cả chuyên khoa"
            />
          </div>
        </div>
      </template>
    </Card>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <ProgressSpinner
        style="width: 2.5rem; height: 2.5rem"
        strokeWidth="4"
        fill="transparent"
        animationDuration=".8s"
        aria-label="Đang tải hồ sơ bệnh nhân"
      />
    </div>

    <!-- Patients Table -->
    <Card v-else class="table-card">
      <template #title>
        Hồ sơ Bệnh nhân ({{ filteredPatients.length }})
      </template>
      <template #content>
        <div v-if="filteredPatients.length === 0" class="empty-state">
          <p class="empty-text">Không tìm thấy hồ sơ bệnh nhân nào</p>
        </div>
        <div v-else class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b">
                <th class="text-left p-3 font-medium text-gray-700">
                  Mã Hồ sơ Y Tế
                </th>
                <th class="text-left p-3 font-medium text-gray-700">
                  Tên bệnh nhân
                </th>
                <th class="text-left p-3 font-medium text-gray-700">Tuổi</th>
                <th class="text-left p-3 font-medium text-gray-700">
                  Giới tính
                </th>
                <th class="text-left p-3 font-medium text-gray-700">
                  Chuyên khoa
                </th>
                <th class="text-left p-3 font-medium text-gray-700">
                  Ngày nhập viện
                </th>
                <th class="text-left p-3 font-medium text-gray-700">
                  Trạng thái
                </th>
                <th class="text-left p-3 font-medium text-gray-700">
                  Hành động
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="patient in filteredPatients"
                :key="patient.id"
                class="border-b hover:bg-gray-50 transition-colors"
              >
                <td class="p-3 font-mono text-sm">
                  {{ patient.medical_record_number || "N/A" }}
                </td>
                <td class="p-3 font-medium">
                  {{ patient.patient_name || "N/A" }}
                </td>
                <td class="p-3">{{ patient.patient_age || "N/A" }}</td>
                <td class="p-3 capitalize">
                  {{ formatGender(patient.patient_gender) }}
                </td>
                <td class="p-3">{{ patient.specialty || "N/A" }}</td>
                <td class="p-3">{{ formatDate(patient.admission_date) }}</td>
                <td class="p-3">
                  <span :class="getStatusClass(patient.case_status)">
                    {{ formatStatus(patient.case_status) }}
                  </span>
                </td>
                <td class="p-3">
                  <Button
                    text
                    size="small"
                    icon="pi pi-eye"
                    label="Xem Chi Tiết"
                    @click="handleViewPatient(patient.id)"
                    class="text-blue-600 hover:text-blue-700"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { requireRoles } from "@/composables/useAuthorize";
import Button from "primevue/button";
import InputText from "primevue/inputtext";
import Select from "primevue/select";
import IconField from "primevue/iconfield";
import InputIcon from "primevue/inputicon";
import Card from "primevue/card";
import ProgressSpinner from "primevue/progressspinner";
import { casesService } from "@/services/cases";

const router = useRouter();
requireRoles(["student", "instructor"]);

const searchQuery = ref("");
const specialtyFilter = ref("all");
const loading = ref(false);
const cases = ref<any[]>([]);

const availableSpecialties = computed(() => {
  const specs = new Set(cases.value.map((c) => c.specialty).filter(Boolean));
  return Array.from(specs).sort();
});

const specialtyOptions = computed(() => [
  { label: "Tất cả chuyên khoa", value: "all" },
  ...availableSpecialties.value.map((spec) => ({ label: spec, value: spec })),
]);

const filteredPatients = computed(() => {
  return cases.value.filter((patient) => {
    const matchesSearch =
      patient.patient_name
        ?.toLowerCase()
        .includes(searchQuery.value.toLowerCase()) ||
      patient.medical_record_number
        ?.toLowerCase()
        .includes(searchQuery.value.toLowerCase()) ||
      patient.specialty
        ?.toLowerCase()
        .includes(searchQuery.value.toLowerCase()) ||
      patient.title?.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesSpecialty =
      specialtyFilter.value === "all" ||
      patient.specialty === specialtyFilter.value;
    return matchesSearch && matchesSpecialty;
  });
});

async function loadPatientRecords() {
  loading.value = true;
  try {
    const response = await casesService.getCases();
    cases.value = response.results || response;
  } catch (error) {
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  loadPatientRecords();
});

function formatDate(dateStr: string | null) {
  if (!dateStr) return "N/A";
  return new Date(dateStr).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

function formatGender(gender: string) {
  const genderMap: Record<string, string> = {
    male: "Nam",
    female: "Nữ",
    other: "Khác",
    not_specified: "Chưa xác định",
  };
  return genderMap[gender] || gender;
}

function formatStatus(status: string) {
  const statusMap: Record<string, string> = {
    draft: "Bản nháp",
    submitted: "Đã nộp",
    reviewed: "Đã xem xét",
    approved: "Đã phê duyệt",
  };
  return statusMap[status] || status;
}

function getStatusClass(status: string) {
  const classMap: Record<string, string> = {
    draft:
      "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800",
    submitted:
      "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800",
    reviewed:
      "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800",
    approved:
      "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800",
  };
  return (
    classMap[status] ||
    "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600"
  );
}

const handleViewPatient = (caseId: string) => {
  router.push(`/patients/${caseId}`);
};
</script>

<style scoped>
/* Patient Records Page */
.page-container {
  padding: 1.5rem;
  background: var(--background);
  min-height: 100vh;
}

/* Header */
.page-header {
  margin-bottom: 1rem;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--foreground);
  margin: 0 0 0.25rem 0;
}

.page-subtitle {
  font-size: 0.875rem;
  color: var(--muted-foreground);
  margin: 0;
}

/* Search Card */
.search-card {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
}

.search-content {
  padding: 1rem 1.25rem 1.25rem;
}

.search-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.75rem;
  align-items: center;
}

.search-field {
  min-width: 0;
}

@media (min-width: 768px) {
  .search-grid {
    grid-template-columns: minmax(0, 2fr) minmax(0, 1fr);
  }
}

/* Loading State */
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 3rem 0;
}

/* Table Card */
.table-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  margin-top: 0.5rem;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 2.5rem 0;
}

.empty-text {
  color: var(--muted-foreground);
  margin: 0;
}

/* Table Styling */
:deep(table) {
  width: 100%;
}

:deep(th) {
  color: var(--foreground);
  font-weight: 500;
  padding: 0.75rem;
  text-align: left;
  font-size: 0.875rem;
}

:deep(td) {
  padding: 0.75rem;
  font-size: 0.875rem;
  color: var(--foreground);
}

:deep(tr) {
  border-bottom: 1px solid var(--border);
}

:deep(tbody tr:hover) {
  background: var(--secondary);
}

:deep(tbody tr:last-child) {
  border-bottom: none;
}

/* PrimeVue Select */
:deep(.p-select) {
  background: var(--card) !important;
  color: var(--foreground) !important;
  border-color: var(--border) !important;
  min-height: 2.75rem;
}

:deep(.p-select.p-focus) {
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 2px var(--shadow-blue-hover) !important;
}

:deep(.p-select-label) {
  display: flex;
  align-items: center;
}

:deep(.p-iconfield) {
  width: 100%;
}

:deep(.p-inputicon) {
  color: var(--muted-foreground) !important;
}

:deep(.p-inputtext) {
  width: 100%;
  min-height: 2.75rem;
}

/* Search icon */
:deep(.text-gray-400) {
  color: var(--muted-foreground) !important;
}

/* Status badges - semantic colors */
:deep(.bg-gray-100) {
  background: var(--secondary) !important;
}

:deep(.text-gray-800) {
  color: var(--foreground) !important;
}

:deep(.bg-blue-100) {
  background: rgba(30, 58, 138, 0.1) !important;
}

:deep(.text-blue-800) {
  color: var(--primary) !important;
}

:deep(.bg-yellow-100) {
  background: rgba(245, 158, 11, 0.1) !important;
}

:deep(.text-yellow-800) {
  color: rgb(146, 64, 14) !important;
}

:deep(.bg-green-100) {
  background: rgba(16, 185, 129, 0.1) !important;
}

:deep(.text-green-800) {
  color: rgb(6, 95, 70) !important;
}

/* View button */
:deep(.text-blue-600) {
  color: var(--primary) !important;
}

:deep(.hover\:text-blue-700:hover) {
  color: var(--primary-hover) !important;
}
</style>
