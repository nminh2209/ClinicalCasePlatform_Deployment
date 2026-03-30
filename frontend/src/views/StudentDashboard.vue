<!-- STUDENT DASHBOARD -->
<template>
  <div class="student-dashboard p-6 space-y-6">
    <!-- Page Header -->
    <div
      class="flex flex-col md:flex-row md:items-center justify-between gap-4"
    >
      <div>
        <div class="flex items-center gap-3 mb-2">
          <h1 class="text-gray-800 text-2xl font-bold">Trang Sinh viên</h1>
          <span
            class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200"
          >
            <i class="pi pi-graduation-cap text-[10px]" aria-hidden="true"></i>
            {{ studentProfile.department }}
          </span>
        </div>
        <p class="text-gray-600">
          Chào mừng trở lại, {{ studentProfile.name }}! Tiếp tục hành trình học
          tập y khoa của bạn.
        </p>
      </div>
    </div>
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
              <i
                class="pi pi-chart-bar h-6 w-6 text-indigo-600 stat-glyph"
                aria-hidden="true"
              ></i>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- Assigned Cases Card -->
      <div
        class="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow"
      >
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-500">Bệnh án được giao</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">
                {{ stats.assignedCases }}
              </p>
              <p class="text-xs text-gray-500 mt-1">Bài tập đang thực hiện</p>
            </div>
            <div class="p-3 bg-blue-50 rounded-lg">
              <i
                class="pi pi-book h-6 w-6 text-blue-600"
                aria-hidden="true"
              ></i>
            </div>
          </div>
        </div>
      </div>

      <!-- Completed Notes Card -->
      <div
        class="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow"
      >
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-500">
                Ghi chú hoàn thành
              </p>
              <p class="text-3xl font-bold text-gray-900 mt-2">
                {{ stats.completedNotes }}
              </p>
              <p class="text-xs text-gray-500 mt-1">Ghi chú đã nộp</p>
            </div>
            <div class="p-3 bg-green-50 rounded-lg">
              <i
                class="pi pi-file h-6 w-6 text-green-600"
                aria-hidden="true"
              ></i>
            </div>
          </div>
        </div>
      </div>

      <!-- Draft Cases Card -->
      <div
        class="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow"
      >
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-500">Bản nháp</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">
                {{ stats.draftCases }}
              </p>
              <p class="text-xs text-gray-500 mt-1">Chưa hoàn thành</p>
            </div>
            <div class="p-3 bg-yellow-50 rounded-lg">
              <i
                class="pi pi-pencil h-6 w-6 text-yellow-600"
                aria-hidden="true"
              ></i>
            </div>
          </div>
        </div>
      </div>

      <!-- Average Grade Card -->
      <div
        class="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow"
      >
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-500">Điểm trung bình</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">
                {{ stats.averageGrade }}%
              </p>
              <p class="text-xs text-gray-500 mt-1">Kết quả tổng thể</p>
            </div>
            <div class="p-3 bg-purple-50 rounded-lg">
              <i
                class="pi pi-star-fill h-6 w-6 text-purple-600"
                aria-hidden="true"
              ></i>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabs Section -->
    <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
      <!-- Tab Headers -->
      <div class="border-b border-gray-200">
        <div class="flex justify-center p-2">
          <div class="inline-flex gap-2 p-1 bg-gray-100 rounded-lg">
            <Button
              @click="activeTab = 'cases'"
              text
              size="small"
              :class="[
                'px-4 py-2 text-sm font-medium rounded-md transition-colors',
                activeTab === 'cases'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900',
              ]"
              label="Bệnh án của tôi"
            />
            <Button
              @click="activeTab = 'progress'"
              text
              size="small"
              icon="pi pi-chart-line"
              label="Phân tích tiến độ"
              :class="[
                'px-4 py-2 text-sm font-medium rounded-md transition-colors inline-flex items-center gap-2',
                activeTab === 'progress'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900',
              ]"
            >
            </Button>
          </div>
        </div>
      </div>

      <!-- Cases Tab Content -->
      <div v-show="activeTab === 'cases'" class="p-6">
        <div class="mb-4">
          <h2 class="text-lg font-semibold text-gray-900">Bệnh án bệnh nhân</h2>
          <p class="text-sm text-gray-500 mt-1">
            Tiếp tục làm việc với các bệnh án được giao
          </p>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="space-y-3">
          <div
            v-for="i in 3"
            :key="i"
            class="p-4 border border-gray-200 rounded-lg animate-pulse"
          >
            <div class="h-4 bg-gray-200 rounded w-3/4 mb-3"></div>
            <div class="h-3 bg-gray-200 rounded w-1/2 mb-2"></div>
            <div class="h-3 bg-gray-200 rounded w-1/3"></div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="recentCases.length === 0" class="text-center py-12">
          <i
            class="pi pi-inbox mx-auto text-3xl text-gray-400"
            aria-hidden="true"
          ></i>
          <h3 class="mt-2 text-sm font-medium text-gray-900">
            Chưa có bệnh án
          </h3>
          <p class="mt-1 text-sm text-gray-500">
            Bạn chưa được phân công bệnh án nào.
          </p>
        </div>

        <!-- Cases List -->
        <div v-else class="space-y-3">
          <div
            v-for="case_ in recentCases"
            :key="case_.id"
            @click="router.push(`/cases/${case_.id}`)"
            class="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer transition-all hover:shadow-sm"
          >
            <div
              class="flex flex-col md:flex-row md:items-center justify-between gap-3"
            >
              <div class="flex-1">
                <div class="flex items-start gap-3 mb-2">
                  <div class="flex-1">
                    <h3 class="font-semibold text-gray-900 mb-2">
                      {{ case_.title }}
                    </h3>
                    <div class="flex flex-wrap items-center gap-2">
                      <span
                        class="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium bg-blue-50 text-blue-700"
                      >
                        {{ case_.specialty }}
                      </span>
                      <span
                        :class="[
                          'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                          case_.status === 'in-progress'
                            ? 'bg-yellow-100 text-yellow-800'
                            : case_.status === 'submitted'
                              ? 'bg-blue-100 text-blue-800'
                              : case_.status === 'graded'
                                ? 'bg-green-100 text-green-800'
                                : 'bg-gray-100 text-gray-800',
                        ]"
                      >
                        {{ getStatusLabel(case_.status) }}
                      </span>
                    </div>
                  </div>
                </div>
                <p class="text-sm text-gray-600">
                  Giảng viên: {{ case_.teacher }}
                </p>
              </div>
              <div class="text-right">
                <div
                  v-if="case_.grade !== null && case_.grade !== undefined"
                  class="text-2xl font-bold text-green-600"
                >
                  {{ case_.grade }}%
                </div>
                <div
                  v-else-if="
                    case_.status === 'submitted' ||
                    case_.case_status === 'submitted'
                  "
                  class="text-sm font-medium text-blue-600"
                >
                  Đang chấm
                </div>
                <div v-else class="text-2xl font-bold text-gray-400">--/--</div>

                <!-- Date display based on status -->
                <div class="text-xs text-gray-500 mt-1 space-y-0.5">
                  <!-- For graded/submitted cases: show created (due) and submitted -->
                  <div
                    v-if="
                      case_.status === 'graded' || case_.status === 'submitted'
                    "
                  >
                    <div v-if="case_.createdAt">
                      Tạo: {{ formatDate(case_.createdAt) }}
                    </div>
                    <div v-if="case_.submittedAt">
                      Nộp: {{ formatDate(case_.submittedAt) }}
                    </div>
                  </div>

                  <!-- For draft/in-progress cases: show created (due) and updated -->
                  <div v-else>
                    <div v-if="case_.createdAt">
                      Tạo: {{ formatDate(case_.createdAt) }}
                    </div>
                    <div v-if="case_.updatedAt">
                      Cập nhật: {{ formatDate(case_.updatedAt) }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Progress Tab Content -->
      <div v-show="activeTab === 'progress'" class="p-6">
        <ProgressAnalytics :studentName="studentProfile.name" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import Button from "primevue/button";
import ProgressAnalytics from "@/components/ProgressAnalytics.vue";
import { useAuthStore } from "@/stores/auth";
import { casesService } from "@/services/cases";
import { gradesService } from "@/services/grades";

const router = useRouter();
const emit = defineEmits(["navigate"]);
const authStore = useAuthStore();
const activeTab = ref("cases");
const loading = ref(true);
const casesData = ref<any[]>([]);
const gradesData = ref<any[]>([]);

const studentProfile = computed(() => ({
  name: authStore.user?.first_name || "Student",
  department:
    authStore.user?.department_vietnamese_name ||
    authStore.user?.department_name ||
    "Chưa phân khoa",
  studentId: authStore.user?.student_id || "N/A",
  year: "3rd Year",
}));

// Computed stats from real data
const stats = computed(() => {
  const assignedCases = casesData.value.length;

  // Count cases that are submitted, approved, or graded
  const completedNotes = casesData.value.filter(
    (c: any) =>
      c.case_status === "submitted" ||
      c.case_status === "approved" ||
      c.case_status === "reviewed",
  ).length;

  const draftCases = casesData.value.filter(
    (c: any) => c.case_status === "draft",
  ).length;

  // Calculate average grade from grades data
  const gradedCases = gradesData.value.filter(
    (g: any) => g.is_final && g.score !== null,
  );
  const averageGrade =
    gradedCases.length > 0
      ? Math.round(
          gradedCases.reduce((sum: number, g: any) => sum + (g.score || 0), 0) /
            gradedCases.length,
        )
      : 0;

  return {
    assignedCases,
    completedNotes,
    draftCases,
    averageGrade,
  };
});

// Map case data with grades
const recentCases = computed(() => {
  return casesData.value.map((case_: any) => {
    const grade = gradesData.value.find((g: any) => g.case === case_.id);

    return {
      id: case_.id.toString(),
      title:
        case_.title ||
        `${case_.patient_name || "Unnamed Patient"} - ${case_.specialty || "General"}`,
      specialty: case_.specialty || "General",
      status: mapCaseStatus(case_.case_status),
      createdAt: case_.created_at,
      updatedAt: case_.updated_at,
      submittedAt: case_.submitted_at,
      reviewedAt: case_.reviewed_at,
      teacher: case_.instructor_name || "Chưa phân công",
      grade: grade?.is_final ? Math.round(grade.score || 0) : null,
      case_status: case_.case_status,
    };
  });
});

// Load data from API
async function loadDashboardData() {
  loading.value = true;
  try {
    // Fetch cases and grades in parallel
    const [casesResponse, gradesResponse] = await Promise.all([
      casesService.getCases(),
      gradesService.getStudentGrades().catch(() => []), // Gracefully handle if grades API fails
    ]);

    // Handle both array and paginated response formats
    casesData.value = Array.isArray(casesResponse)
      ? casesResponse
      : casesResponse?.results || [];
    gradesData.value = Array.isArray(gradesResponse)
      ? gradesResponse
      : gradesResponse?.results || [];
  } catch (error) {
    casesData.value = [];
    gradesData.value = [];
  } finally {
    loading.value = false;
  }
}

function mapCaseStatus(status: string): string {
  // Map backend status to frontend status
  switch (status) {
    case "draft":
      return "in-progress";
    case "submitted":
      return "submitted";
    case "approved":
      return "submitted";
    case "graded":
      return "graded";
    case "reviewed":
      return "graded";
    default:
      return "not-started";
  }
}

function formatDate(dateStr: string | null) {
  if (!dateStr) return "N/A";
  return new Date(dateStr).toLocaleDateString("vi-VN");
}

function getStatusLabel(status: string) {
  switch (status) {
    case "in-progress":
      return "Đang thực hiện";
    case "submitted":
      return "Chờ chấm điểm";
    case "graded":
      return "Đã chấm điểm";
    case "not-started":
      return "Chưa bắt đầu";
    default:
      return "";
  }
}

// Load data on mount
onMounted(() => {
  loadDashboardData();
});
</script>

<style scoped>
/* Student Dashboard - CSS Variable Overrides */
.student-dashboard {
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

.stat-glyph {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

:deep(.stat-glyph::before) {
  line-height: 1;
}

/* Headers */
h1,
h2,
h3,
h4 {
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

/* Primary accent colors */
:deep(.bg-blue-50) {
  background: var(--accent) !important;
}

:deep(.text-blue-700),
:deep(.text-blue-600) {
  color: var(--primary) !important;
}

:deep(.border-blue-200) {
  border-color: var(--shadow-blue) !important;
}

:deep(.bg-blue-600) {
  background: var(--primary) !important;
}

/* Indigo accent (secondary primary) */
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

/* Success (green) - keeping semantic colors */
:deep(.bg-green-50) {
  background: rgba(16, 185, 129, 0.1) !important;
}

:deep(.text-green-700),
:deep(.text-green-600) {
  color: rgb(4, 120, 87) !important;
}

/* Warning (yellow) - keeping semantic */
:deep(.bg-yellow-50) {
  background: rgba(245, 158, 11, 0.1) !important;
}

:deep(.text-yellow-700),
:deep(.text-yellow-600) {
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

/* Tab styling */
:deep(.border-blue-500) {
  border-color: var(--primary) !important;
}

/* Hover states */
:deep(.hover\:bg-gray-50:hover) {
  background: var(--secondary) !important;
}
</style>
