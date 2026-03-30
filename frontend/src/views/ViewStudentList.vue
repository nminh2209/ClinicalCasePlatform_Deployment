<template>
  <div class="student-list">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <h1>Danh sách sinh viên</h1>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-section">
      <div class="search-and-filters">
        <div class="combined-search">
          <Select
            v-model="searchField"
            :options="searchFieldOptions"
            optionLabel="label"
            optionValue="value"
            class="search-field-select"
          />

          <div class="search-container">
            <IconField>
              <InputIcon class="pi pi-search search-icon" />
              <InputText
                v-model="searchQuery"
                @input="searchStudents"
                :placeholder="`Tìm kiếm theo ${searchField === 'email' ? 'email' : 'mã sinh viên'}`"
                class="search-input"
              />
            </IconField>
          </div>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <main class="cases-main">
      <div class="container">
        <!-- DataTable — replaces the custom .cases-grid card layout -->
        <DataTable
          :value="students"
          :loading="loading"
          class="student-table"
          stripedRows
          responsiveLayout="scroll"
          :rowHover="true"
          tableStyle="min-width: 40rem"
        >
          <!-- Loading slot -->
          <template #loading>
            <div class="table-loading">
              <ProgressSpinner
                style="width: 50px; height: 50px"
                strokeWidth="4"
              />
              <p>Đang tải danh sách sinh viên...</p>
            </div>
          </template>

          <!-- Empty slot -->
          <template #empty>
            <div class="empty-state text-center">
              <i class="pi pi-users empty-icon" />
              <h3>Không có sinh viên phù hợp</h3>
            </div>
          </template>

          <!-- Name column -->
          <Column field="full_name" header="Họ và tên" style="min-width: 200px">
            <template #body="{ data }">
              <div class="student-name-cell">
                <Avatar
                  icon="pi pi-user"
                  shape="circle"
                  class="student-avatar"
                />
                <span class="student-name"
                  >{{ data.first_name }} {{ data.last_name }}</span
                >
              </div>
            </template>
          </Column>

          <!-- Email column -->
          <Column field="email" header="Email" style="min-width: 220px">
            <template #body="{ data }">
              <span class="student-email">{{ data.email }}</span>
            </template>
          </Column>

          <!-- Student ID column -->
          <Column
            field="student_id"
            header="Mã sinh viên"
            style="min-width: 160px"
          >
            <template #body="{ data }">
              <Tag
                :value="data.student_id || '—'"
                severity="secondary"
                class="student-id-tag"
              />
            </template>
          </Column>
        </DataTable>
      </div>

      <!-- Paginator — replaces manual prev/next/page-number Button set -->
      <div
        v-if="currentPageNumber > 1 || nextPageUrl"
        class="pagination-container"
      >
        <Paginator
          :first="(currentPageNumber - 1) * pageSize"
          :rows="pageSize"
          :totalRecords="totalRecords"
          class="student-paginator"
          @page="onPageChange"
        />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { requireRoles } from "@/composables/useAuthorize";
import axios from "@/services/api";
import Avatar from "primevue/avatar";
import Button from "primevue/button";
import Column from "primevue/column";
import DataTable from "primevue/datatable";
import IconField from "primevue/iconfield";
import InputIcon from "primevue/inputicon";
import InputText from "primevue/inputtext";
import Paginator from "primevue/paginator";
import ProgressSpinner from "primevue/progressspinner";
import Select from "primevue/select";
import Tag from "primevue/tag";

requireRoles(["instructor", "admin"]);

const searchQuery = ref("");
const searchField = ref("email");
const searchFieldOptions = [
  { label: "Email", value: "email" },
  { label: "Mã sinh viên", value: "student_id" },
];

const currentPageUsers = ref<any[]>([]);
const nextPageUrl = ref<string | null>(null);
const previousPageUrl = ref<string | null>(null);
const currentPageNumber = ref(1);
const pageSize = ref(10);
const totalRecords = ref(0);

const loading = ref(true);

async function fetchPage(url: string = "/auth/users/") {
  try {
    loading.value = true;

    const response = await axios.get(url, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
    });

    const data = response.data;

    currentPageUsers.value = data.results || [];
    nextPageUrl.value = data.next;
    previousPageUrl.value = data.previous;
    totalRecords.value = data.count || currentPageUsers.value.length;

    const urlObj = new URL(url, window.location.origin);
    const page = urlObj.searchParams.get("page");
    currentPageNumber.value = page ? parseInt(page) : 1;
  } catch (err: any) {
    currentPageUsers.value = [];
  } finally {
    loading.value = false;
  }
}

onMounted(() => fetchPage());

// Paginator event handler
function onPageChange(event: { page: number; rows: number }) {
  pageSize.value = event.rows;
  const page = event.page + 1;
  fetchPage(`/auth/users/?page=${page}`);
}

function searchStudents() {
  fetchPage("/auth/users/");
}

const students = computed(() => {
  let list = currentPageUsers.value.filter((u: any) => u.role === "student");

  if (!searchQuery.value.trim()) return list;

  const q = searchQuery.value.trim().toLowerCase();
  return list.filter((s: any) => {
    const email = (s.email || "").toLowerCase();
    const studentId = (s.student_id || "").toLowerCase();

    if (searchField.value === "email") return email.includes(q);
    if (searchField.value === "student_id") return studentId.includes(q);

    const name = `${s.first_name || ""} ${s.last_name || ""}`.toLowerCase();
    return name.includes(q) || email.includes(q) || studentId.includes(q);
  });
});
</script>

<style scoped>
.page-header {
  margin-bottom: 2rem;
  padding: 1.5rem 0;
  border-bottom: 1px solid var(--border);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h1 {
  margin: 0;
  color: var(--foreground);
  font-size: 1.875rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.filters-section {
  margin-bottom: 2rem;
  padding: 1.5rem 0;
  background: var(--card);
  border-radius: 16px;
  box-shadow: 0 2px 4px var(--shadow-grey);
  border: 1px solid var(--border);
}

.search-and-filters {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
}

.combined-search {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  width: 100%;
  padding: 0 1.5rem;
}

:deep(.search-field-select.p-select) {
  width: 180px;
  min-height: 2.75rem;
  padding: 0 0.75rem;
  border: 1px solid var(--border);
  border-radius: 10px;
  background: var(--card);
  color: var(--foreground);
  font-size: 0.95rem;
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

:deep(.search-field-select.p-select:hover) {
  border-color: var(--foreground);
}

:deep(.search-field-select.p-select.p-focus) {
  border-color: var(--primary);
  box-shadow: 0 0 0 2px var(--shadow-blue-hover);
}

:deep(.search-field-select .p-select-label) {
  display: flex;
  align-items: center;
  font-size: 0.95rem;
}

:deep(.p-select-overlay .p-select-option) {
  min-height: 2.5rem;
  display: flex;
  align-items: center;
  font-size: 0.95rem;
}

.search-container {
  position: relative;
  flex: 1;
  width: 100%;
}

:deep(.search-container .p-iconfield) {
  width: 100%;
}

.search-icon {
  color: var(--muted-foreground);
}

.search-input {
  width: 100%;
  min-height: 2.75rem;
  padding: 0.75rem 1rem 0.75rem 2.4rem;
  border: 1px solid var(--border);
  border-radius: 10px;
  font-size: 0.95rem;
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
  background: var(--card);
  color: var(--foreground);
}

.search-input:focus {
  outline: none;
  border-color: var(--foreground);
  box-shadow: 0 0 0 2px var(--border);
}

/* DataTable — card-like feel with clean rounded wrapper */
.container {
  background: var(--card);
  border-radius: 16px;
  border: 1px solid var(--border);
  overflow: hidden;
  box-shadow: 0 2px 4px var(--shadow-grey);
}

:deep(.student-table) {
  background: transparent !important;
}

:deep(.student-table .p-datatable-thead > tr > th) {
  background: var(--secondary) !important;
  color: var(--foreground) !important;
  font-weight: 600;
  font-size: 0.875rem;
  border-bottom: 2px solid var(--border) !important;
  padding: 1rem 1.25rem !important;
}

:deep(.student-table .p-datatable-tbody > tr) {
  background: var(--card) !important;
  transition: background 0.15s ease;
}

:deep(.student-table .p-datatable-tbody > tr:hover) {
  background: var(--secondary) !important;
}

:deep(.student-table .p-datatable-tbody > tr > td) {
  padding: 1rem 1.25rem !important;
  border-bottom: 1px solid var(--border) !important;
  color: var(--foreground) !important;
}

:deep(.student-table .p-datatable-striped tbody > tr:nth-child(even)) {
  background: rgba(0, 0, 0, 0.01) !important;
}

/* Loading / empty states */
.table-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 3rem;
  gap: 1rem;
  color: var(--muted-foreground);
}

.empty-state {
  padding: 3rem;
  color: var(--muted-foreground);
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.4;
}

/* Student name cell — avatar + name inline */
.student-name-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.student-avatar {
  width: 36px !important;
  height: 36px !important;
  background: var(--accent) !important;
  color: var(--primary) !important;
  font-size: 1rem !important;
  flex-shrink: 0;
}

.student-name {
  font-weight: 600;
  color: var(--foreground);
}

.student-email {
  color: var(--muted-foreground);
  font-size: 0.9rem;
}

.student-id-tag {
  font-family: monospace;
  font-size: 0.85rem !important;
}

/* Paginator */
.pagination-container {
  display: flex;
  justify-content: center;
  padding: 1.5rem 0;
}

:deep(.student-paginator) {
  background: transparent !important;
  border: none !important;
}

:deep(.student-paginator .p-paginator-page.p-highlight) {
  background: var(--primary) !important;
  color: var(--primary-foreground) !important;
  border-color: var(--primary) !important;
  border-radius: 8px !important;
}

:deep(.student-paginator .p-paginator-page),
:deep(.student-paginator .p-paginator-prev),
:deep(.student-paginator .p-paginator-next),
:deep(.student-paginator .p-paginator-first),
:deep(.student-paginator .p-paginator-last) {
  border-radius: 8px !important;
  color: var(--foreground) !important;
  min-width: 2.5rem !important;
  height: 2.5rem !important;
}

:deep(.student-paginator .p-paginator-page:hover),
:deep(.student-paginator .p-paginator-prev:hover),
:deep(.student-paginator .p-paginator-next:hover) {
  background: var(--secondary) !important;
  border-color: var(--primary) !important;
}

@media (max-width: 768px) {
  .combined-search {
    padding: 0 1rem;
    flex-direction: column;
  }
  :deep(.search-field-select.p-select) {
    width: 100%;
  }
}
</style>
