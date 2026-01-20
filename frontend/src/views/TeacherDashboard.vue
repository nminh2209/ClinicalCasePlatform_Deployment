<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-gray-800 mb-2 text-2xl font-bold">Bảng giảng viên</h1>
        <p class="text-gray-600">
          {{ userDepartmentVietnamese || "Tất cả khoa" }} — Quản lý bài nộp và tiến độ sinh viên
        </p>
      </div>
      <button @click="emit('navigate', 'students')"
        class="inline-flex items-center justify-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium shadow-sm">
        <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z">
          </path>
        </svg>
        Quản lý sinh viên
      </button>
    </div>

    <!-- Statistic Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- Case Summary Card (New) -->
      <div @click="router.push('/case-summary')"
        class="bg-gradient-to-br from-indigo-50 to-purple-50 border border-indigo-200 rounded-xl shadow-sm hover:shadow-lg transition-all cursor-pointer transform hover:scale-105">
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <p class="text-sm font-semibold text-indigo-700">Bệnh án tổng hợp</p>
              <p class="text-lg font-bold text-indigo-900 mt-2">Xem thống kê</p>
              <p class="text-xs text-indigo-600 mt-1">Phân tích và báo cáo</p>
            </div>
            <div class="p-3 bg-indigo-100 rounded-lg">
              <svg class="h-6 w-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z">
                </path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Total Students Card -->
      <div class="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow">
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-500">Tổng sinh viên</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.totalStudents }}</p>
              <p class="text-xs text-gray-500 mt-1">
                {{ userDepartmentVietnamese ? `Trong ${userDepartmentVietnamese}` : "Tất cả khoa" }}
              </p>
            </div>
            <div class="p-3 bg-blue-50 rounded-lg">
              <svg class="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M12 14l9-5-9-5-9 5 9 5z"></path>
                <path
                  d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z">
                </path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222">
                </path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Pending Review Card -->
      <div class="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow">
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-500">Chờ chấm điểm</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.pendingReview }}</p>
              <p class="text-xs text-gray-500 mt-1">Đang chờ nhận xét</p>
            </div>
            <div class="p-3 bg-yellow-50 rounded-lg">
              <svg class="h-6 w-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Graded This Week Card -->
      <div class="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow">
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-500">Đã chấm tuần này</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.gradedThisWeek }}</p>
              <p class="text-xs text-gray-500 mt-1">Bài được chấm</p>
            </div>
            <div class="p-3 bg-green-50 rounded-lg">
              <svg class="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Active Cases Card -->
      <div class="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow">
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-500">Ca bệnh hoạt động</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.activeCases }}</p>
              <p class="text-xs text-gray-500 mt-1">Đang được thực hiện</p>
            </div>
            <div class="p-3 bg-purple-50 rounded-lg">
              <svg class="h-6 w-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253">
                </path>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pending Submissions -->
    <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
      <div class="p-6 border-b border-gray-200">
        <h2 class="text-lg font-semibold text-gray-900">Bài chờ chấm</h2>
        <p class="text-sm text-gray-500 mt-1">Bệnh án sinh viên đang chờ bạn đánh giá</p>
      </div>
      <div class="p-6">
        <div v-if="pendingSubmissions.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z">
            </path>
          </svg>
          <p class="mt-2 text-sm text-gray-500">Không có bài nộp nào đang chờ chấm điểm</p>
        </div>
        <div v-else class="space-y-3">
          <div v-for="submission in pendingSubmissions" :key="submission.id" @click="viewCase(submission.id)"
            class="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer transition-all hover:shadow-sm">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-2">
                  <h3 class="font-semibold text-gray-900">{{ submission.studentName }}</h3>
                  <span
                    class="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium bg-gray-100 text-gray-800">
                    {{ submission.studentId }}
                  </span>
                </div>
                <p class="text-sm text-gray-600 mb-2">{{ submission.caseTitle }}</p>
                <div class="flex items-center gap-1 text-xs text-gray-500">
                  <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  <span>Nộp ngày: {{ formatDate(submission.submittedDate) }}</span>
                </div>
              </div>
              <div class="flex items-center gap-2">
                <span v-if="submission.daysWaiting > 2"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                  Khẩn
                </span>
                <span v-else-if="submission.daysWaiting <= 2 && submission.daysWaiting > 0"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                  {{ submission.daysWaiting }} ngày trước
                </span>
                <span v-else
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  Mới
                </span>
                <button
                  class="px-4 py-2 text-sm font-medium bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                  Chấm điểm
                </button>
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
        <p class="text-sm text-gray-500 mt-1">Kết quả và phản hồi mới nhất của bạn</p>
      </div>
      <div class="p-6">
        <div v-if="recentlyGraded.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4">
            </path>
          </svg>
          <p class="mt-2 text-sm text-gray-500">Chưa có bài nào được chấm điểm</p>
        </div>
        <div v-else class="space-y-3">
          <div v-for="submission in recentlyGraded" :key="submission.id" @click="viewCase(submission.id)"
            class="p-4 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-all hover:shadow-sm">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-2">
                  <h3 class="font-semibold text-gray-900">{{ submission.studentName }}</h3>
                  <span
                    class="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium bg-gray-100 text-gray-800">
                    {{ submission.studentId }}
                  </span>
                </div>
                <p class="text-sm text-gray-600 mb-2">{{ submission.caseTitle }}</p>
                <div class="flex items-center gap-1 text-xs text-gray-500">
                  <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  <span>Ngày chấm: {{ formatDate(submission.gradedDate) }}</span>
                </div>
              </div>
              <div class="flex items-center gap-3">
                <div class="text-right">
                  <span :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                    submission.visibility === 'public'
                      ? 'bg-green-100 text-green-800'
                      : 'bg-gray-100 text-gray-800'
                  ]">
                    {{ submission.visibility === 'public' ? 'Công khai' : 'Riêng tư' }}
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
import { Users, FileCheck, BookOpen, GraduationCap } from "lucide-vue-next";
import { useCasesStore } from "@/stores/cases";
import { useAuthStore } from "@/stores/auth";

// UI Components
import Card from "@/components/ui/Card.vue";
import CardHeader from "@/components/ui/CardHeader.vue";
import CardContent from "@/components/ui/CardContent.vue";
import CardTitle from "@/components/ui/CardTitle.vue";
import CardDescription from "@/components/ui/CardDescription.vue";
import Badge from "@/components/ui/Badge.vue";
import Button from "@/components/ui/Button.vue";

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
  () => authStore.user?.department_vietnamese_name || userDepartment.value
);

// Filter cases by instructor's department
const departmentCases = computed(() => {
  if (!userDepartment.value) {
    return allCases.value;
  }
  return allCases.value.filter(
    (c) =>
      c.student_department === userDepartment.value ||
      c.student_department_vietnamese === userDepartmentVietnamese.value
  );
});

// Filter cases that are submitted (waiting for review) and not yet graded
const pendingSubmissions = computed(() => {
  return departmentCases.value
    .filter((c) => c.case_status === "submitted" && c.case_status !== "reviewed" && c.case_status !== "approved")
    .map((c) => {
      const submittedDate = new Date(c.submitted_at || c.updated_at);
      const daysWaiting = Math.floor(
        (new Date().getTime() - submittedDate.getTime()) / (1000 * 60 * 60 * 24)
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
        new Date(b.gradedDate).getTime() - new Date(a.gradedDate).getTime()
    )
    .slice(0, 5);
});

// Calculate stats
const stats = computed(() => {
  const submitted = departmentCases.value.filter(
    (c) => c.case_status === "submitted"
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
    departmentCases.value.map((c) => c.created_by_id).filter(Boolean)
  );

  return {
    totalStudents: uniqueStudents.size,
    pendingReview: submitted,
    gradedThisWeek: gradedThisWeek,
    activeCases: departmentCases.value.filter(
      (c) => c.case_status === "draft" || c.case_status === "submitted"
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
