<template>
  <div class="student-list">
    <!-- Header & Filters -->
    <div class="page-header">
      <div class="header-content">
        <h1>Danh sách sinh viên</h1>
      </div>
    </div>

    <div class="filters-section">
      <div class="search-and-filters">
        <div class="combined-search">
          <select v-model="searchField" class="search-field-select">
            <option value="email">Email</option>
            <option value="student_id">Mã sinh viên</option>
          </select>

          <div class="search-container">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              class="search-icon">
              <circle cx="11" cy="11" r="8" />
              <path d="m21 21-4.35-4.35" />
            </svg>
            <input v-model="searchQuery" @input="searchStudents" type="text" :placeholder="`Tìm kiếm theo ${searchField === 'email' ? 'email' : 'mã sinh viên'
              }`" class="search-input" />
          </div>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <main class="cases-main">
      <div class="container">
        <!-- Loading -->
        <div v-if="loading" class="text-center py-8">
          <p>Đang tải danh sách sinh viên...</p>
        </div>

        <!-- Students grid -->
        <div v-else class="cases-grid">
          <div v-for="student in students" :key="student.id" class="case-card">
            <div class="case-header">
              <h3>{{ student.first_name }} {{ student.last_name }}</h3>
            </div>
            <div class="case-meta mt-6">
              <p><strong>Email:</strong> {{ student.email }}</p>
              <p>
                <strong>Mã sinh viên:</strong>
                {{ student.student_id }}
              </p>
            </div>
          </div>
        </div>

        <!-- Empty state -->
        <div v-if="!loading && students.length === 0" class="empty-state text-center">
          <h3>Không có sinh viên phù hợp</h3>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="currentPageNumber > 1 || nextPageUrl" class="pagination-container">
        <div class="pagination">
          <button @click="goToPrevious" :disabled="!previousPageUrl" class="page-btn">
            Trước
          </button>

          <button v-for="page in maxVisiblePage" :key="page" @click="goToPage(page)"
            :class="{ active: page === currentPageNumber }" class="page-btn page-number">
            {{ page }}
          </button>

          <button @click="goToNext" :disabled="!nextPageUrl" class="page-btn">
            Sau
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import { requireRoles } from "@/composables/useAuthorize";
import axios from "@/services/api";

requireRoles(["instructor", "admin"]);

const searchQuery = ref("");
const searchField = ref("email");

const currentPageUsers = ref<any[]>([]);
const nextPageUrl = ref<string | null>(null);
const previousPageUrl = ref<string | null>(null);
const currentPageNumber = ref(1);

const loading = ref(true);

// Fetch page
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

    // Extract current page number from URL
    const urlObj = new URL(url, window.location.origin);
    const page = urlObj.searchParams.get("page");
    currentPageNumber.value = page ? parseInt(page) : 1;
  } catch (err: any) {
    console.error(err);
    currentPageUsers.value = [];
  } finally {
    loading.value = false;
  }
}

onMounted(() => fetchPage());

// Navigation
function goToNext() {
  if (nextPageUrl.value) fetchPage(nextPageUrl.value);
}

function goToPrevious() {
  if (previousPageUrl.value) fetchPage(previousPageUrl.value);
}

function goToPage(page: number) {
  if (page === currentPageNumber.value) return;
  fetchPage(`/auth/users/?page=${page}`);
}

// Search (reset to page 1)
function searchStudents() {
  fetchPage("/auth/users/");
}

// Show pages 1 to currentPageNumber (and +1 if next exists)
const maxVisiblePage = computed(() => {
  return nextPageUrl.value
    ? currentPageNumber.value + 1
    : currentPageNumber.value;
});

// Only show accounts with role === "student" + search
const students = computed(() => {
  let list = currentPageUsers.value.filter((u: any) => u.role === "student");

  if (!searchQuery.value.trim()) return list;

  const q = searchQuery.value.trim().toLowerCase();
  return list.filter((s: any) => {
    const name = `${s.first_name || ""} ${s.last_name || ""}`.toLowerCase();
    const email = (s.email || "").toLowerCase();
    const studentId = (s.student_id || "").toLowerCase();

    if (searchField.value === "email") return email.includes(q);
    if (searchField.value === "student_id") return studentId.includes(q);

    return name.includes(q) || email.includes(q) || studentId.includes(q);
  });
});
</script>

<style scoped>
.page-header {
  margin-bottom: 2rem;
  padding: 1.5rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h1 {
  margin: 0;
  color: #1f2937;
  font-size: 1.875rem;
  font-weight: 700;
}

.filters-section {
  margin-bottom: 2rem;
  padding: 1.5rem 0;
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
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

.search-field-select {
  width: 180px;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  background: white;
  color: #374151;
  font-size: 0.95rem;
}

.search-field-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.search-container {
  position: relative;
  flex: 1;
  width: 100%;
  min-width: unset;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #6b7280;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.95rem;
  transition: border-color 0.2s;
  background: white;
  color: #374151;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.08);
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
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  transition: all 0.2s;
  border: 1px solid #f3f4f6;
}

.case-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border-color: #e5e7eb;
}

.case-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 1.125rem;
  line-height: 1.4;
  font-weight: 600;
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
  width: 120px;
  display: inline-block;
}

.pagination-container {
  display: flex;
  justify-content: center;
  padding: 2rem 0 1rem;
}

.pagination {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
}

.page-btn {
  min-width: 44px;
  height: 44px;
  padding: 0 0.75rem;
  border: 1px solid #d1d5db;
  background: white;
  color: #374151;
  border-radius: 0.5rem;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  background: #f3f4f6;
  border-color: #9ca3af;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #f9fafb;
}

.page-btn.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
  font-weight: 600;
}

.page-number {
  width: 44px;
}

@media (max-width: 768px) {
  .combined-search {
    padding: 0 1rem;
  }

  .search-field-select {
    width: 100%;
  }
}
</style>
