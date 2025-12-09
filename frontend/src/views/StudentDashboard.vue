<!-- STUDENT DASHBOARD -->
<template>
  <div class="p-6 space-y-6">
    <!-- Page Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-3 mb-2">
          <h1 class="text-gray-800 text-2xl font-bold">Trang Sinh viên</h1>
          <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200">
            <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path d="M12 14l9-5-9-5-9 5 9 5z"></path>
              <path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222"></path>
            </svg>
            {{ studentProfile.department }}
          </span>
        </div>
        <p class="text-gray-600">
          Chào mừng trở lại, {{ studentProfile.name }}! Tiếp tục hành trình học tập y khoa của bạn.
        </p>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- Case Summary Card (New) -->
      <div 
        @click="router.push('/case-summary')"
        class="bg-gradient-to-br from-indigo-50 to-purple-50 border border-indigo-200 rounded-xl shadow-sm hover:shadow-lg transition-all cursor-pointer transform hover:scale-105"
      >
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <p class="text-sm font-semibold text-indigo-700">Bệnh án tổng hợp</p>
              <p class="text-lg font-bold text-indigo-900 mt-2">Xem thống kê</p>
              <p class="text-xs text-indigo-600 mt-1">Phân tích và báo cáo</p>
            </div>
            <div class="p-3 bg-indigo-100 rounded-lg">
              <svg class="h-6 w-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Assigned Cases Card -->
      <div class="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow">
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-500">Bệnh án được giao</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.assignedCases }}</p>
              <p class="text-xs text-gray-500 mt-1">Bài tập đang thực hiện</p>
            </div>
            <div class="p-3 bg-blue-50 rounded-lg">
              <svg class="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Completed Notes Card -->
      <div class="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow">
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-500">Ghi chú hoàn thành</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.completedNotes }}</p>
              <p class="text-xs text-gray-500 mt-1">Ghi chú đã nộp</p>
            </div>
            <div class="p-3 bg-green-50 rounded-lg">
              <svg class="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Draft Cases Card -->
      <div class="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow">
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-500">Bản nháp</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.draftCases }}</p>
              <p class="text-xs text-gray-500 mt-1">Chưa hoàn thành</p>
            </div>
            <div class="p-3 bg-yellow-50 rounded-lg">
              <svg class="h-6 w-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Average Grade Card -->
      <div class="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow">
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-500">Điểm trung bình</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.averageGrade }}%</p>
              <p class="text-xs text-gray-500 mt-1">Kết quả tổng thể</p>
            </div>
            <div class="p-3 bg-purple-50 rounded-lg">
              <svg class="h-6 w-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
              </svg>
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
            <button 
              @click="activeTab = 'cases'"
              :class="[
                'px-4 py-2 text-sm font-medium rounded-md transition-colors',
                activeTab === 'cases' 
                  ? 'bg-white text-gray-900 shadow-sm' 
                  : 'text-gray-600 hover:text-gray-900'
              ]"
            >
              Bệnh án của tôi
            </button>
            <button 
              @click="activeTab = 'progress'"
              :class="[
                'px-4 py-2 text-sm font-medium rounded-md transition-colors inline-flex items-center gap-2',
                activeTab === 'progress' 
                  ? 'bg-white text-gray-900 shadow-sm' 
                  : 'text-gray-600 hover:text-gray-900'
              ]"
            >
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
              </svg>
              Phân tích tiến độ
            </button>
          </div>
        </div>
      </div>

      <!-- Cases Tab Content -->
      <div v-show="activeTab === 'cases'" class="p-6">
        <div class="mb-4">
          <h2 class="text-lg font-semibold text-gray-900">Bệnh án bệnh nhân</h2>
          <p class="text-sm text-gray-500 mt-1">Tiếp tục làm việc với các bệnh án được giao</p>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="space-y-3">
          <div v-for="i in 3" :key="i" class="p-4 border border-gray-200 rounded-lg animate-pulse">
            <div class="h-4 bg-gray-200 rounded w-3/4 mb-3"></div>
            <div class="h-3 bg-gray-200 rounded w-1/2 mb-2"></div>
            <div class="h-3 bg-gray-200 rounded w-1/3"></div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="recentCases.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">Chưa có bệnh án</h3>
          <p class="mt-1 text-sm text-gray-500">Bạn chưa được phân công bệnh án nào.</p>
        </div>

        <!-- Cases List -->
        <div v-else class="space-y-3">
          <div 
            v-for="case_ in recentCases" 
            :key="case_.id" 
            @click="router.push(`/cases/${case_.id}`)"
            class="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer transition-all hover:shadow-sm"
          >
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
              <div class="flex-1">
                <div class="flex items-start gap-3 mb-2">
                  <div class="flex-1">
                    <h3 class="font-semibold text-gray-900 mb-2">{{ case_.title }}</h3>
                    <div class="flex flex-wrap items-center gap-2">
                      <span class="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium bg-blue-50 text-blue-700">
                        {{ case_.specialty }}
                      </span>
                      <span 
                        :class="[
                          'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                          case_.status === 'in-progress' ? 'bg-yellow-100 text-yellow-800' :
                          case_.status === 'submitted' ? 'bg-blue-100 text-blue-800' :
                          case_.status === 'graded' ? 'bg-green-100 text-green-800' :
                          'bg-gray-100 text-gray-800'
                        ]"
                      >
                        {{ getStatusLabel(case_.status) }}
                      </span>
                    </div>
                  </div>
                </div>
                <p class="text-sm text-gray-600">Giảng viên: {{ case_.teacher }}</p>
              </div>
              <div class="text-right">
                <div v-if="case_.grade !== null && case_.grade !== undefined" class="text-2xl font-bold text-green-600">
                  {{ case_.grade }}%
                </div>
                <div v-else-if="case_.status === 'submitted' || case_.case_status === 'submitted'" class="text-sm font-medium text-blue-600">
                  Đang chấm
                </div>
                <div v-else class="text-2xl font-bold text-gray-400">
                  --/--
                </div>
                
                <!-- Date display based on status -->
                <div class="text-xs text-gray-500 mt-1 space-y-0.5">
                  <!-- For graded/submitted cases: show created (due) and submitted -->
                  <div v-if="case_.status === 'graded' || case_.status === 'submitted'">
                    <div v-if="case_.createdAt">Tạo: {{ formatDate(case_.createdAt) }}</div>
                    <div v-if="case_.submittedAt">Nộp: {{ formatDate(case_.submittedAt) }}</div>
                  </div>
                  
                  <!-- For draft/in-progress cases: show created (due) and updated -->
                  <div v-else>
                    <div v-if="case_.createdAt">Tạo: {{ formatDate(case_.createdAt) }}</div>
                    <div v-if="case_.updatedAt">Cập nhật: {{ formatDate(case_.updatedAt) }}</div>
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
import { BookOpen, FileText, Award, Clock, GraduationCap, TrendingUp } from "lucide-vue-next";
import { useRouter } from "vue-router";

import Card from "@/components/ui/Card.vue";
import CardHeader from "@/components/ui/CardHeader.vue";
import CardContent from "@/components/ui/CardContent.vue";
import CardTitle from "@/components/ui/CardTitle.vue";
import CardDescription from "@/components/ui/CardDescription.vue";
import Badge from "@/components/ui/Badge.vue";
import Button from "@/components/ui/Button.vue";
import Tabs from "@/components/ui/Tabs.vue";
import TabsList from "@/components/ui/TabsList.vue";
import TabsTrigger from "@/components/ui/TabsTrigger.vue";
import TabsContent from "@/components/ui/TabsContent.vue";
import ProgressAnalytics from "@/components/ProgressAnalytics.vue";
import { useAuthStore } from "@/stores/auth";
import { casesService } from "@/services/cases";
import { gradesService } from "@/services/grades";

const router = useRouter();
const emit = defineEmits(['navigate']);
const authStore = useAuthStore();
const activeTab = ref('cases');
const loading = ref(true);
const casesData = ref<any[]>([]);
const gradesData = ref<any[]>([]);

const studentProfile = computed(() => ({
  name: authStore.user?.first_name || "Student",
  department: authStore.user?.department_vietnamese_name || authStore.user?.department_name || "Chưa phân khoa",
  studentId: authStore.user?.student_id || "N/A",
  year: "3rd Year",
}));

// Computed stats from real data
const stats = computed(() => {
  const assignedCases = casesData.value.length;
  
  // Count cases that are submitted, approved, or graded
  const completedNotes = casesData.value.filter((c: any) => 
    c.case_status === 'submitted' || c.case_status === 'approved' || c.case_status === 'reviewed'
  ).length;
  
  const draftCases = casesData.value.filter((c: any) => c.case_status === 'draft').length;
  
  // Calculate average grade from grades data
  const gradedCases = gradesData.value.filter((g: any) => g.is_final && g.score !== null);
  const averageGrade = gradedCases.length > 0
    ? Math.round(gradedCases.reduce((sum: number, g: any) => sum + (g.score || 0), 0) / gradedCases.length)
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
      title: case_.title || `${case_.patient_name || 'Unnamed Patient'} - ${case_.specialty || 'General'}`,
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
    casesData.value = Array.isArray(casesResponse) ? casesResponse : (casesResponse?.results || []);
    gradesData.value = Array.isArray(gradesResponse) ? gradesResponse : (gradesResponse?.results || []);
    
    // Debug logging
    // console.log('=== STUDENT DASHBOARD DEBUG ===');
    // console.log('Cases loaded:', casesData.value.length);
    // console.log('Cases data:', casesData.value);
    // console.log('Grades loaded:', gradesData.value.length);
    // console.log('Grades data:', gradesData.value);
    // console.log('Grade to Case mapping:');
    // casesData.value.forEach((c: any) => {
    //   const grade = gradesData.value.find((g: any) => g.case === c.id);
    //   console.log(`  Case ${c.id}: Grade =`, grade);
    // });
    // console.log('===============================');
  } catch (error) {
    console.error("Error loading dashboard data:", error);
    casesData.value = [];
    gradesData.value = [];
  } finally {
    loading.value = false;
  }
}

function mapCaseStatus(status: string): string {
  // Map backend status to frontend status
  switch (status) {
    case 'draft':
      return 'in-progress';
    case 'submitted':
      return 'submitted';
    case 'approved':
      return 'submitted';
    case 'graded':
      return 'graded';
    case 'reviewed':
      return 'graded';
    default:
      return 'not-started';
  }
}

function formatDate(dateStr: string | null) {
  if (!dateStr) return "N/A";
  return new Date(dateStr).toLocaleDateString("vi-VN");
}

function getStatusLabel(status: string) {
  switch (status) {
    case "in-progress": return "Đang thực hiện";
    case "submitted": return "Chờ chấm điểm";
    case "graded": return "Đã chấm điểm";
    case "not-started": return "Chưa bắt đầu";
    default: return "";
  }
}

// Load data on mount
onMounted(() => {
  loadDashboardData();
});
</script>