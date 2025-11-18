<template>
  <div class="student-list">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <h1>Danh sách sinh viên</h1>
      </div>
    </div>

    <!-- Filter -->
    <div class="filters-section">
      <div class="search-and-filters">
        <!-- Combined search: dropdown (left) + input (right) -->
        <div class="combined-search">
          <select
            v-model="searchField"
            class="search-field-select"
            aria-label="Search field"
          >
            <option value="email">Email</option>
            <option value="student_id">Mã sinh viên</option>
          </select>

          <div class="search-container">
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              class="search-icon"
            >
              <circle cx="11" cy="11" r="8" />
              <path d="m21 21-4.35-4.35" />
            </svg>
            <input
              v-model="searchQuery"
              @input="handleSearch"
              type="text"
              :placeholder="`Tìm kiếm sinh viên theo ${placeholderText}`"
              class="search-input"
              aria-label="Search query"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Main -->
    <main class="cases-main">
      <div class="container">
        <div class="cases-grid">
          <div
            v-for="student in displayedStudents"
            :key="student.id"
            class="case-card"
          >
            <div class="case-header">
              <h3>{{ student.first_name }} {{ student.last_name }}</h3>
            </div>

            <div class="case-meta mt-6">
              <!-- <p><strong>Username:</strong> {{ student.username }}</p> -->
              <p><strong>Email:</strong> {{ student.email }}</p>
              <p><strong>Điện thoại:</strong> {{ student.phone }}</p>
              <p><strong>Mã sinh viên:</strong> {{ student.student_id }}</p>
              <p><strong>Năm học:</strong> {{ student.academic_year }}</p>
            </div>
          </div>
        </div>

        <div class="empty-state" v-if="displayedStudents.length === 0">
          <h3>Không có sinh viên phù hợp</h3>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { requireRoles } from '@/composables/useAuthorize'

// Component-level guard (instructors + admins)
requireRoles(['instructor','admin'])

const searchQuery = ref("");
const searchField = ref("email");

const students = ref([
  {
    id: 1,
    first_name: "Nguyễn",
    last_name: "Văn A",
    username: "nguyenvana",
    email: "nguyenvana@example.com",
    phone: "+84-912-345-001",
    student_id: "S2025001",
    academic_year: "2024/2025",
  },
  {
    id: 2,
    first_name: "Trần",
    last_name: "Thị B",
    username: "tranthib",
    email: "tranthib@example.com",
    phone: "+84-912-345-002",
    student_id: "S2025002",
    academic_year: "2024/2025",
  },
  {
    id: 3,
    first_name: "Lê",
    last_name: "Văn C",
    username: "levanc",
    email: "levanc@example.com",
    phone: "+84-912-345-003",
    student_id: "S2025003",
    academic_year: "2024/2025",
  },
  {
    id: 4,
    first_name: "Phạm",
    last_name: "Thị D",
    username: "phamthid",
    email: "phamthid@example.com",
    phone: "+84-912-345-004",
    student_id: "S2025004",
    academic_year: "2024/2025",
  },
  {
    id: 5,
    first_name: "Hoàng",
    last_name: "Văn E",
    username: "hoangvane",
    email: "hoangvane@example.com",
    phone: "+84-912-345-005",
    student_id: "S2025005",
    academic_year: "2024/2025",
  },
  {
    id: 6,
    first_name: "Đỗ",
    last_name: "Thị F",
    username: "dothif",
    email: "dothif@example.com",
    phone: "+84-912-345-006",
    student_id: "S2025006",
    academic_year: "2024/2025",
  },
]);

const placeholderText = computed(() => {
  switch (searchField.value) {
    case "email":
      return "email";
    case "student_id":
      return "mã sinh viên (VD: S1234567)";
    case "username":
      return "tên đăng nhập";
    case "name":
      return "họ và tên";
    default:
      return "từ khóa";
  }
});

const displayedStudents = computed(() => {
  const q = searchQuery.value.trim().toLowerCase();
  if (!q) return students.value;
  return students.value.filter((s) => {
    if (searchField.value === "email") {
      return (s.email || "").toLowerCase().includes(q);
    }
    if (searchField.value === "student_id") {
      return (s.student_id || "").toLowerCase().includes(q);
    }
    if (searchField.value === "username") {
      return (s.username || "").toLowerCase().includes(q);
    }
    if (searchField.value === "name") {
      const full = `${s.first_name} ${s.last_name}`.toLowerCase();
      return full.includes(q);
    }
    // fallback: search across common fields
    return (
      (s.email || "").toLowerCase().includes(q) ||
      (s.student_id || "").toLowerCase().includes(q) ||
      `${s.first_name} ${s.last_name}`.toLowerCase().includes(q) ||
      (s.username || "").toLowerCase().includes(q)
    );
  });
});

function handleSearch() {
  // computed displayedStudents will react — this function kept for possible debouncing
}
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

/* Replace filters-section styles to match Cases.vue filters look */

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

/* Combined search: dropdown (left) + input (right) */
.combined-search {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  width: 100%; /* Remove max-width to allow full expansion */
  padding: 0 1.5rem; /* Add padding to match filters-section */
}

.search-field-select {
  width: 180px; /* Fixed width instead of min-width */
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
  width: 100%; /* Ensure full width */
  min-width: unset; /* Remove min-width constraint */
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

/* Responsive adjustments */
@media (max-width: 768px) {
  .combined-search {
    padding: 0 1rem; /* Slightly smaller padding on mobile */
  }

  .search-field-select {
    width: 100%;
  }
}
</style>
