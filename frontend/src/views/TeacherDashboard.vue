<template>
  <div class="teacher-dashboard p-6 space-y-6">
    <!-- Header -->
    <div
      class="flex flex-col md:flex-row md:items-center justify-between gap-4"
    >
      <div>
        <h1 class="text-gray-800 mb-2 text-2xl font-bold">Bảng giảng viên</h1>
        <p class="text-gray-600">
          {{ userDepartmentVietnamese || "Tất cả khoa" }} — Quản lý bài nộp và
          tiến độ sinh viên
        </p>
      </div>
      <Button
        icon="pi pi-users"
        label="Quản lý sinh viên"
        @click="emit('navigate', 'students')"
      />
    </div>

    <!-- Case Summary Section -->
    <div class="case-summary-row">
      <p class="case-summary-label">Truy cập nhanh</p>
      <div
        @click="router.push('/case-summary')"
        class="case-summary-card bg-gradient-to-br from-indigo-50 to-purple-50 border border-indigo-200 rounded-xl shadow-sm hover:shadow-lg transition-all cursor-pointer transform hover:scale-[1.01]"
      >
        <div class="p-4">
          <div class="flex items-start justify-between gap-4">
            <div class="flex-1">
              <p class="text-sm font-semibold text-indigo-700">
                Bệnh án tổng hợp
              </p>
              <p class="text-lg font-bold text-indigo-900 mt-2">Xem thống kê</p>
              <p class="text-xs text-indigo-600 mt-1">Phân tích và báo cáo</p>
            </div>
            <div class="p-3 bg-indigo-100 rounded-lg">
              <i class="pi pi-chart-bar h-6 w-6 text-indigo-600 stat-glyph" aria-hidden="true"></i>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Statistic Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">

      <!-- Total Students Card -->
      <div
        class="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow"
      >
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-500">Tổng sinh viên</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">
                {{ stats.totalStudents }}
              </p>
              <p class="text-xs text-gray-500 mt-1">
                {{
                  userDepartmentVietnamese
                    ? `Trong ${userDepartmentVietnamese}`
                    : "Tất cả khoa"
                }}
              </p>
            </div>
            <div class="p-3 bg-blue-50 rounded-lg">
              <i class="pi pi-graduation-cap h-6 w-6 text-blue-600 stat-glyph" aria-hidden="true"></i>
            </div>
          </div>
        </div>
      </div>

      <!-- Pending Review Card -->
      <div
        class="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow"
      >
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-500">Chờ chấm điểm</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">
                {{ stats.pendingReview }}
              </p>
              <p class="text-xs text-gray-500 mt-1">Đang chờ nhận xét</p>
            </div>
            <div class="p-3 bg-yellow-50 rounded-lg">
              <i class="pi pi-clock h-6 w-6 text-yellow-600 stat-glyph" aria-hidden="true"></i>
            </div>
          </div>
        </div>
      </div>

      <!-- Graded This Week Card -->
      <div
        class="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow"
      >
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-500">Đã chấm tuần này</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">
                {{ stats.gradedThisWeek }}
              </p>
              <p class="text-xs text-gray-500 mt-1">Bài được chấm</p>
            </div>
            <div class="p-3 bg-green-50 rounded-lg">
              <i class="pi pi-check-circle h-6 w-6 text-green-600 stat-glyph" aria-hidden="true"></i>
            </div>
          </div>
        </div>
      </div>

      <!-- Active Cases Card -->
      <div
        class="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow"
      >
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-500">Ca bệnh hoạt động</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">
                {{ stats.activeCases }}
              </p>
              <p class="text-xs text-gray-500 mt-1">Đang được thực hiện</p>
            </div>
            <div class="p-3 bg-purple-50 rounded-lg">
              <i class="pi pi-book h-6 w-6 text-purple-600 stat-glyph" aria-hidden="true"></i>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pending Submissions -->
    <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
      <div class="p-6 border-b border-gray-200">
        <h2 class="text-lg font-semibold text-gray-900">Bài chờ chấm</h2>
        <p class="text-sm text-gray-500 mt-1">
          Bệnh án sinh viên đang chờ bạn đánh giá
        </p>
      </div>
      <div class="p-6">
        <div v-if="pendingSubmissions.length === 0" class="text-center py-12">
          <i class="pi pi-inbox mx-auto text-3xl text-gray-400" aria-hidden="true"></i>
          <p class="mt-2 text-sm text-gray-500">
            Không có bài nộp nào đang chờ chấm điểm
          </p>
        </div>
        <div v-else class="space-y-3">
          <div
            v-for="submission in pendingSubmissions"
            :key="submission.id"
            @click="viewCase(submission.id)"
            class="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer transition-all hover:shadow-sm"
          >
            <div
              class="flex flex-col md:flex-row md:items-center justify-between gap-3"
            >
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-2">
                  <h3 class="font-semibold text-gray-900">
                    {{ submission.studentName }}
                  </h3>
                  <span
                    class="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium bg-gray-100 text-gray-800"
                  >
                    {{ submission.studentId }}
                  </span>
                </div>
                <p class="text-sm text-gray-600 mb-2">
                  {{ submission.caseTitle }}
                </p>
                <div class="flex items-center gap-1 text-xs text-gray-500">
                  <i class="pi pi-calendar h-3.5 w-3.5" aria-hidden="true"></i>
                  <span
                    >Nộp ngày: {{ formatDate(submission.submittedDate) }}</span
                  >
                </div>
              </div>
              <div class="flex items-center gap-2">
                <span
                  v-if="submission.daysWaiting > 2"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800"
                >
                  Khẩn
                </span>
                <span
                  v-else-if="
                    submission.daysWaiting <= 2 && submission.daysWaiting > 0
                  "
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800"
                >
                  {{ submission.daysWaiting }} ngày trước
                </span>
                <span
                  v-else
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                >
                  Mới
                </span>
                <Button
                  label="Chấm điểm"
                  size="small"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recently Graded -->
    <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
      <div class="p-6 border-b border-gray-200">
        <h2 class="text-lg font-semibold text-gray-900">Đã chấm gần đây</h2>
        <p class="text-sm text-gray-500 mt-1">
          Kết quả và phản hồi mới nhất của bạn
        </p>
      </div>
      <div class="p-6">
        <div v-if="recentlyGraded.length === 0" class="text-center py-12">
          <i class="pi pi-clipboard mx-auto text-3xl text-gray-400" aria-hidden="true"></i>
          <p class="mt-2 text-sm text-gray-500">
            Chưa có bài nào được chấm điểm
          </p>
        </div>
        <div v-else class="space-y-3">
          <div
            v-for="submission in recentlyGraded"
            :key="submission.id"
            @click="viewCase(submission.id)"
            class="p-4 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-all hover:shadow-sm"
          >
            <div
              class="flex flex-col md:flex-row md:items-center justify-between gap-3"
            >
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-2">
                  <h3 class="font-semibold text-gray-900">
                    {{ submission.studentName }}
                  </h3>
                  <span
                    class="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium bg-gray-100 text-gray-800"
                  >
                    {{ submission.studentId }}
                  </span>
                </div>
                <p class="text-sm text-gray-600 mb-2">
                  {{ submission.caseTitle }}
                </p>
                <div class="flex items-center gap-1 text-xs text-gray-500">
                  <i class="pi pi-calendar h-3.5 w-3.5" aria-hidden="true"></i>
                  <span
                    >Ngày chấm: {{ formatDate(submission.gradedDate) }}</span
                  >
                </div>
              </div>
              <div class="flex items-center gap-3">
                <div class="text-right">
                  <span
                    :class="[
                      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                      submission.visibility === 'public'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-gray-100 text-gray-800',
                    ]"
                  >
                    {{
                      submission.visibility === "public"
                        ? "Công khai"
                        : "Riêng tư"
                    }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import Button from "primevue/button";
import { useCasesStore } from "@/stores/cases";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const casesStore = useCasesStore();
const authStore = useAuthStore();

const emit = defineEmits(["navigate"]);

// Fetch cases on mount
onMounted(async () => {
  await casesStore.fetchCases();
});

// Get all cases from store
const allCases = computed(() => casesStore.cases || []);

// Get current instructor's department
const userDepartment = computed(() => authStore.user?.department_name || "");
const userDepartmentVietnamese = computed(
  () => authStore.user?.department_vietnamese_name || userDepartment.value,
);

// Filter cases by instructor's department
const departmentCases = computed(() => {
  if (!userDepartment.value) {
    return allCases.value;
  }
  return allCases.value.filter(
    (c) =>
      c.student_department === userDepartment.value ||
      c.student_department_vietnamese === userDepartmentVietnamese.value,
  );
});

// Filter cases that are submitted (waiting for review) and not yet graded
const pendingSubmissions = computed(() => {
  return departmentCases.value
    .filter(
      (c) =>
        c.case_status === "submitted" &&
        c.case_status !== "reviewed" &&
        c.case_status !== "approved",
    )
    .map((c) => {
      const submittedDate = new Date(c.submitted_at || c.updated_at);
      const daysWaiting = Math.floor(
        (new Date().getTime() - submittedDate.getTime()) /
          (1000 * 60 * 60 * 24),
      );

      return {
        id: c.id,
        studentName: c.created_by_name || "Unknown Student",
        studentId: c.created_by_id || "",
        caseTitle: c.title,
        submittedDate: c.submitted_at || c.updated_at,
        daysWaiting: daysWaiting,
      };
    })
    .sort((a, b) => b.daysWaiting - a.daysWaiting);
});

// Filter cases that are reviewed/approved
const recentlyGraded = computed(() => {
  return departmentCases.value
    .filter((c) => c.case_status === "reviewed" || c.case_status === "approved")
    .map((c) => ({
      id: c.id,
      studentName: c.created_by_name || "Unknown Student",
      studentId: c.created_by_id || "",
      caseTitle: c.title,
      grade: c.grade || 0,
      gradedDate: c.reviewed_at || c.updated_at,
      visibility: c.is_public ? "public" : "private",
    }))
    .sort(
      (a, b) =>
        new Date(b.gradedDate).getTime() - new Date(a.gradedDate).getTime(),
    )
    .slice(0, 5);
});

// Calculate stats
const stats = computed(() => {
  const submitted = departmentCases.value.filter(
    (c) => c.case_status === "submitted",
  ).length;

  const oneWeekAgo = new Date();
  oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
  const gradedThisWeek = departmentCases.value.filter((c) => {
    const reviewDate = new Date(c.reviewed_at || c.updated_at);
    return (
      (c.case_status === "reviewed" || c.case_status === "approved") &&
      reviewDate >= oneWeekAgo
    );
  }).length;

  const uniqueStudents = new Set(
    departmentCases.value.map((c) => c.created_by_id).filter(Boolean),
  );

  return {
    totalStudents: uniqueStudents.size,
    pendingReview: submitted,
    gradedThisWeek: gradedThisWeek,
    activeCases: departmentCases.value.filter(
      (c) => c.case_status === "draft" || c.case_status === "submitted",
    ).length,
  };
});

function formatDate(dateStr: any) {
  return new Date(dateStr).toLocaleDateString("vi-VN");
}

function viewCase(caseId: any) {
  router.push(`/cases/${caseId}`);
}
</script>

<style scoped>
/* Teacher Dashboard - CSS Variable Overrides */
.teacher-dashboard {
  background: var(--background);
  min-height: 100vh;
}

.case-summary-row {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.case-summary-label {
  margin: 0;
  font-size: 0.8rem;
  color: var(--muted-foreground);
  font-weight: 600;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

.case-summary-card {
  width: 100%;
  max-width: 8960px;
}

/* Headers */
h1, h2, h3, h4 {
  color: var(--foreground);
}

/* Text colors */
:deep(.text-gray-800) {
  color: var(--foreground) !important;
}

:deep(.text-gray-700) {
  color: var(--foreground) !important;
}

:deep(.text-gray-600) {
  color: var(--muted-foreground) !important;
}

:deep(.text-gray-500) {
  color: var(--muted-foreground) !important;
}

/* Card backgrounds */
:deep(.bg-white) {
  background: var(--card) !important;
}

:deep(.bg-gray-50) {
  background: var(--secondary) !important;
}

/* Border colors */
:deep(.border-gray-200) {
  border-color: var(--border) !important;
}

.stat-glyph {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

:deep(.stat-glyph::before) {
  line-height: 1;
}

/* Primary buttons and accents */
:deep(.bg-blue-600) {
  background: var(--primary) !important;
}

:deep(.bg-blue-700) {
  background: var(--primary-hover) !important;
}

:deep(.hover\:bg-blue-700:hover) {
  background: var(--primary-hover) !important;
}

/* Primary text */
:deep(.text-blue-700),
:deep(.text-blue-600) {
  color: var(--primary) !important;
}

/* Indigo accent */
:deep(.bg-indigo-50) {
  background: var(--accent) !important;
}

:deep(.text-indigo-700),
:deep(.text-indigo-600) {
  color: var(--primary) !important;
}

:deep(.border-indigo-200) {
  border-color: var(--shadow-blue) !important;
}

/* Success (green) - semantic */
:deep(.bg-green-50) {
  background: rgba(16, 185, 129, 0.1) !important;
}

:deep(.bg-green-100) {
  background: rgba(16, 185, 129, 0.15) !important;
}

:deep(.text-green-700),
:deep(.text-green-600),
:deep(.text-green-800) {
  color: rgb(4, 120, 87) !important;
}

/* Warning (yellow) - semantic */
:deep(.bg-yellow-50) {
  background: rgba(245, 158, 11, 0.1) !important;
}

:deep(.bg-yellow-100) {
  background: rgba(245, 158, 11, 0.15) !important;
}

:deep(.text-yellow-700),
:deep(.text-yellow-600),
:deep(.text-yellow-800) {
  color: rgb(180, 83, 9) !important;
}

/* Purple accent */
:deep(.bg-purple-50) {
  background: rgba(139, 92, 246, 0.1) !important;
}

:deep(.text-purple-700),
:deep(.text-purple-600) {
  color: rgb(109, 40, 217) !important;
}

/* Destructive (red) - semantic */
:deep(.bg-red-50) {
  background: rgba(220, 38, 38, 0.1) !important;
}

:deep(.bg-red-100) {
  background: rgba(220, 38, 38, 0.15) !important;
}

:deep(.text-red-700),
:deep(.text-red-800) {
  color: var(--destructive) !important;
}

/* Hover states */
:deep(.hover\:bg-gray-50:hover) {
  background: var(--secondary) !important;
}
</style>
