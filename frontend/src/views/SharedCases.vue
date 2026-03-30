<template>
  <div class="cases-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1>Ca bệnh được phê duyệt</h1>
        <p class="subtitle">
          Tất cả ca bệnh đã được phê duyệt từ sinh viên khác
        </p>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="filters-section">
      <div class="search-and-filters">
        <div class="search-container">
          <SearchAutocomplete
            v-model="searchQuery"
            placeholder="Tìm kiếm ca bệnh theo tên, chuyên khoa, bệnh nhân..."
            @update:modelValue="handleSearch"
          />
        </div>

        <div>
          <Select
            v-model="specialtyFilter"
            :options="specialties"
            optionLabel="name"
            optionValue="name"
            placeholder="Tất cả chuyên khoa"
            :disabled="choicesLoading"
            class="text-sm filter-options me-3"
            @change="applyFilters"
          />

          <Select
            v-model="dateSort"
            :options="[
              { label: 'Mới nhất', value: 'newest' },
              { label: 'Cũ nhất', value: 'oldest' },
            ]"
            optionLabel="label"
            optionValue="value"
            class="text-sm filter-options"
            @change="applyFilters"
          />
        </div>
      </div>
    </div>

    <!-- Stats Card -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon stat-success">
          <span class="pi-check-circle pi" style="font-size: 1.5rem"></span>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ cases.length }}</div>
          <div class="stat-label">Ca bệnh được phê duyệt</div>
        </div>
      </div>
    </div>

    <main class="cases-main">
      <div class="container">
        <div class="loading" v-if="loading">
          <p>Đang tải ca bệnh...</p>
        </div>

        <div class="error" v-if="error">
          <p>{{ error }}</p>
          <Button @click="loadCases" class="button font-bold">Thử lại</Button>
        </div>

        <div class="cases-grid" v-if="!loading && !error">
          <div
            v-if="filteredCases.length === 0"
            class="empty-state col-span-full"
          >
            <span
              class="pi-arrow-right-arrow-left pi"
              style="font-size: 2rem"
            ></span>
            <h3>Không tìm thấy ca bệnh được phê duyệt</h3>
            <p v-if="searchQuery || specialtyFilter">
              Thử điều chỉnh bộ lọc hoặc từ khóa tìm kiếm
            </p>
            <p v-else>Chưa có ca bệnh nào được phê duyệt</p>
          </div>

          <div v-for="case_ in filteredCases" :key="case_.id" class="case-card">
            <div class="case-header">
              <h3>{{ case_.title }}</h3>
              <Tag severity="success" value="Đã duyệt" class="approved-tag" />
            </div>

            <div class="case-meta">
              <p>
                <strong>Sinh viên:</strong> {{ case_.student_name || "N/A" }}
              </p>
              <p><strong>Bệnh nhân:</strong> {{ case_.patient_name }}</p>
              <p><strong>Tuổi:</strong> {{ case_.patient_age }}</p>
              <p><strong>Chuyên khoa:</strong> {{ case_.specialty }}</p>
              <p>
                <strong>Ngày tạo:</strong> {{ formatDate(case_.created_at) }}
              </p>
            </div>

            <div class="case-actions">
              <Button fluid @click="viewCase(case_)" class="button font-bold"
                >Xem chi tiết</Button
              >
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { requireRoles } from "@/composables/useAuthorize";
import { useChoices } from "@/composables/useChoices";
import { casesService } from "@/services/cases";
import InputText from "primevue/inputtext";
import Select from "primevue/select";
import Button from "primevue/button";
import Tag from "primevue/tag";
import SearchAutocomplete from "@/components/SearchAutocomplete.vue";

const router = useRouter();
const { specialties, loading: choicesLoading } = useChoices();

const searchQuery = ref("");
const specialtyFilter = ref("");
const dateSort = ref("newest");
const cases = ref<any[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

const filteredCases = computed(() => {
  let filtered = cases.value;

  // Filter by specialty
  if (specialtyFilter.value) {
    filtered = filtered.filter((c) => c.specialty === specialtyFilter.value);
  }

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(
      (c) =>
        c.title.toLowerCase().includes(query) ||
        c.specialty.toLowerCase().includes(query) ||
        c.patient_name.toLowerCase().includes(query) ||
        (c.keywords && c.keywords.toLowerCase().includes(query)) ||
        (c.student_name && c.student_name.toLowerCase().includes(query)),
    );
  }

  // Sort by date
  if (dateSort.value) {
    filtered = [...filtered].sort((a, b) => {
      const dateA = new Date(a.created_at).getTime();
      const dateB = new Date(b.created_at).getTime();

      if (dateSort.value === "newest") {
        return dateB - dateA;
      } else if (dateSort.value === "oldest") {
        return dateA - dateB;
      }
      return 0;
    });
  }

  return filtered;
});

async function loadCases() {
  loading.value = true;
  error.value = null;

  try {
    // Fetch only approved cases from all user
    const data = await casesService.getCases({ case_status: "approved" });

    // Check if data is an array or if it's paginated
    if (Array.isArray(data)) {
      cases.value = data;
    } else if (data && data.results) {
      // Handle paginated response
      cases.value = data.results;
    } else {
      cases.value = [];
    }
  } catch (err: any) {
    error.value = "Không thể tải ca bệnh. Vui lòng thử lại.";
  } finally {
    loading.value = false;
  }
}

function handleSearch() {
  // Search is reactive through computed property
}

function applyFilters() {
  // Filters are applied reactively through computed property
}

function viewCase(case_: any) {
  router.push(`/cases/${case_.id}`);
}

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString("vi-VN");
}

onMounted(() => {
  requireRoles(["student", "instructor"]);
  loadCases();
});
</script>

<style scoped>
/* Page Header */
.page-header {
  margin-bottom: 2rem;
  padding: 1.5rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.header-content {
  text-align: left;
}

.header-content h1 {
  margin: 0;
  color: #1f2937;
  font-size: 1.875rem;
  font-weight: 700;
}

.subtitle {
  margin: 0.5rem 0 0 0;
  color: #6b7280;
  font-size: 1rem;
}

/* Filters Section */
.filters-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 0.75rem;
  box-shadow:
    0 1px 3px 0 rgba(0, 0, 0, 0.1),
    0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.search-and-filters {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  align-items: center;
}

.search-container {
  position: relative;
  flex: 1;
  min-width: 300px;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #6b7280;
}

.search-input {
  padding-left: 3rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  transition: border-color 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.filter-options {
  border: 2px solid var(--border) !important;
  transition: all 0.3s ease !important;
}

.filter-options:focus {
  border-color: var(--primary) !important;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow:
    0 1px 3px 0 rgba(0, 0, 0, 0.1),
    0 1px 2px 0 rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.2s;
}

.stat-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-success {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  line-height: 1;
}

.stat-label {
  color: #6b7280;
  font-size: 0.875rem;
  font-weight: 500;
  margin-top: 0.25rem;
}

/* Cases Grid */
.loading,
.error {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
}

.cases-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.case-card {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow:
    0 1px 3px 0 rgba(0, 0, 0, 0.1),
    0 1px 2px 0 rgba(0, 0, 0, 0.06);
  transition: all 0.2s;
  border: 1px solid #f3f4f6;
}

.case-card:hover {
  box-shadow:
    0 10px 25px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border-color: #e5e7eb;
}

.case-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.case-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 1.125rem;
  line-height: 1.4;
  font-weight: 600;
  flex: 1;
  min-width: 0;
}

:deep(.approved-tag) {
  flex-shrink: 0;
  white-space: nowrap;
}

.case-meta {
  margin-bottom: 1rem;
}

.case-meta p {
  margin: 0.25rem 0;
  font-size: 0.875rem;
  color: #6b7280;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.case-meta strong {
  color: #374151;
}

.case-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #f3f4f6;
}

.button {
  background-color: var(--primary) !important;
  color: var(--primary-foreground) !important;
  border-color: var(--primary) !important;
  transition: 0.3s !important;
}

.button:hover {
  background-color: var(--primary-hover) !important;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.empty-state h3 {
  margin: 1rem 0 0.5rem 0;
  color: #374151;
  font-size: 1.25rem;
}

.empty-state p {
  margin: 0.5rem 0;
  color: #6b7280;
}
</style>
