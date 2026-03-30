<template>
  <div class="case-summary-page p-6 md:p-8 space-y-8 max-w-7xl mx-auto">
    <!-- ── Header ─────────────────────────────────────────── -->
    <div class="summary-header flex items-center justify-between gap-4">
      <div>
        <h1 class="text-xl font-bold text-gray-900">Bệnh án tổng hợp</h1>
        <p class="text-gray-600 mt-1">
          Tổng quan và phân tích các ca bệnh của bạn
        </p>
      </div>
      <Button
        outlined
        @click="refreshData"
        icon="pi pi-refresh"
        label="Làm mới"
        class="refresh-btn"
      />
    </div>

    <!-- ── Loading State ──────────────────────────────────── -->
    <div
      v-if="loading"
      class="flex items-center justify-center py-12 rounded-xl border border-gray-200 bg-white loading-container"
    >
      <ProgressSpinner
        style="width: 3rem; height: 3rem"
        strokeWidth="4"
        fill="transparent"
        animationDuration=".8s"
        aria-label="Đang tải dữ liệu"
      />
    </div>

    <!-- ── Summary Content ────────────────────────────────── -->
    <div v-else-if="summary" class="summary-content space-y-8">
      <!-- Statistics Cards -->
      <div
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 md:gap-6"
      >
        <Card
          v-for="card in summaryStatCards"
          :key="card.key"
          class="summary-card hover:drop-shadow-lg transition"
        >
          <template #content>
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-600">{{ card.label }}</p>
                <p :class="['text-3xl font-bold mt-2', card.valueClass]">
                  {{ card.value }}
                </p>
              </div>
              <div
                :class="[
                  'w-12 h-12 rounded-full flex items-center justify-center',
                  card.iconBgClass,
                ]"
              >
                <svg
                  :class="['w-6 h-6', card.iconClass]"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    :d="card.iconPath"
                  />
                </svg>
              </div>
            </div>
          </template>
        </Card>
      </div>

      <!-- Charts Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 md:gap-7">
        <!-- Status Distribution -->
        <Card class="summary-panel hover:drop-shadow-lg transition">
          <template #header>
            <p class="panel-heading">Phân bố theo trạng thái</p>
          </template>
          <template #content>
            <div class="space-y-3">
              <div
                v-for="(status, key) in summary.by_status"
                :key="key"
                class="flex items-center justify-between"
              >
                <div class="flex items-center gap-3">
                  <Tag
                    :class="getStatusBadgeClass(key)"
                    :value="status.label"
                  />
                  <span class="text-sm text-gray-600"
                    >{{ status.count }} ca</span
                  >
                </div>
                <div class="flex items-center gap-2">
                  <div class="w-32 bg-gray-200 rounded-full h-2">
                    <div
                      class="h-2 rounded-full transition-all"
                      :class="getStatusBarClass(key)"
                      :style="{ width: status.percentage + '%' }"
                    ></div>
                  </div>
                  <span
                    class="text-sm font-medium text-gray-700 w-12 text-right"
                    >{{ status.percentage }}%</span
                  >
                </div>
              </div>
            </div>
          </template>
        </Card>

        <!-- Top Specialties -->
        <Card class="summary-panel hover:drop-shadow-lg transition">
          <template #header>
            <p class="panel-heading">Chuyên khoa hàng đầu</p>
          </template>
          <template #content>
            <div class="space-y-3">
              <div
                v-for="(item, index) in summary.top_specialties"
                :key="index"
                class="flex items-center justify-between"
              >
                <div class="flex items-center gap-3">
                  <span
                    class="w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs font-bold"
                  >
                    {{ Number(index) + 1 }}
                  </span>
                  <span class="text-sm font-medium text-gray-700">{{
                    item.specialty
                  }}</span>
                </div>
                <Tag severity="secondary" :value="`${item.count} ca`" />
              </div>
              <div
                v-if="summary.top_specialties.length === 0"
                class="text-center text-gray-500 py-4"
              >
                Chưa có dữ liệu chuyên khoa
              </div>
            </div>
          </template>
        </Card>

        <!-- Priority / Complexity Distribution Panels -->
        <Card
          v-for="panel in distributionPanels"
          :key="panel.key"
          class="summary-panel hover:drop-shadow-lg transition"
        >
          <template #header>
            <p class="panel-heading">{{ panel.title }}</p>
          </template>
          <template #content>
            <div class="space-y-3">
              <div
                v-for="(count, itemKey) in panel.data"
                :key="String(itemKey)"
                class="flex items-center justify-between"
              >
                <Tag
                  :class="panel.badgeClass(itemKey)"
                  :value="panel.label(itemKey)"
                />
                <span class="text-sm font-medium text-gray-600"
                  >{{ count }} ca</span
                >
              </div>
              <div
                v-if="!panel.data || Object.keys(panel.data).length === 0"
                class="text-center text-gray-500 py-4"
              >
                {{ panel.emptyText }}
              </div>
            </div>
          </template>
        </Card>
      </div>

      <!-- Recent Cases -->
      <Card class="summary-panel hover:drop-shadow-lg transition">
        <template #header>
          <p class="panel-heading">Ca bệnh gần đây</p>
        </template>
        <template #content>
          <div class="space-y-3">
            <div
              v-for="caseItem in summary.recent_cases"
              :key="caseItem.id"
              class="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors cursor-pointer recent-case-row"
              @click="viewCase(caseItem.id)"
            >
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-1">
                  <h4 class="font-medium text-gray-900">
                    {{ caseItem.title }}
                  </h4>
                  <Tag
                    severity="secondary"
                    class="text-xs"
                    :value="caseItem.specialty"
                  />
                  <Tag
                    :class="getStatusBadgeClass(caseItem.case_status)"
                    class="text-xs"
                    :value="getStatusLabel(caseItem.case_status)"
                  />
                </div>
                <p class="text-sm text-gray-500">
                  Ngày tạo: {{ formatDate(caseItem.created_at) }}
                </p>
              </div>
              <i class="pi pi-chevron-right text-gray-400"></i>
            </div>
            <div
              v-if="summary.recent_cases.length === 0"
              class="text-center text-gray-500 py-8"
            >
              Chưa có ca bệnh nào
            </div>
          </div>
        </template>
      </Card>
    </div>

    <!-- ── Error State ────────────────────────────────────── -->
    <div v-else-if="error" class="text-center py-12">
      <p class="text-red-600 mb-4">{{ error }}</p>
      <Button @click="refreshData" label="Thử lại" icon="pi pi-refresh" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { casesService } from "@/services/cases";
import Button from "primevue/button";
import Card from "primevue/card";
import Tag from "primevue/tag";
import ProgressSpinner from "primevue/progressspinner";

const router = useRouter();

const loading = ref(true);
const error = ref("");
const summary = ref<any>(null);

// Helper functions for labels and styling
const getStatusLabel = (status: string | number) => {
  const statusStr = String(status);
  const labels: Record<string, string> = {
    draft: "Bản nháp",
    submitted: "Đã nộp",
    reviewed: "Đã xem xét",
    approved: "Đã phê duyệt",
  };
  return labels[statusStr] || statusStr;
};

const getStatusBadgeClass = (status: string | number) => {
  const statusStr = String(status);
  const classes: Record<string, string> = {
    draft: "bg-gray-500 text-white",
    submitted: "bg-yellow-500 text-white",
    reviewed: "bg-blue-500 text-white",
    approved: "bg-green-500 text-white",
  };
  return classes[statusStr] || "bg-gray-500 text-white";
};

const getStatusBarClass = (status: string | number) => {
  const statusStr = String(status);
  const classes: Record<string, string> = {
    draft: "bg-gray-500",
    submitted: "bg-yellow-500",
    reviewed: "bg-blue-500",
    approved: "bg-green-500",
  };
  return classes[statusStr] || "bg-gray-500";
};

const getPriorityLabel = (priority: string | number) => {
  const priorityStr = String(priority);
  const labels: Record<string, string> = {
    low: "Thấp",
    medium: "Trung bình",
    high: "Cao",
    urgent: "Khẩn cấp",
  };
  return labels[priorityStr] || priorityStr;
};

const getPriorityBadgeClass = (priority: string | number) => {
  const priorityStr = String(priority);
  const classes: Record<string, string> = {
    low: "bg-gray-500 text-white",
    medium: "bg-blue-500 text-white",
    high: "bg-orange-500 text-white",
    urgent: "bg-red-500 text-white",
  };
  return classes[priorityStr] || "bg-gray-500 text-white";
};

const getComplexityLabel = (complexity: string | number) => {
  const complexityStr = String(complexity);
  const labels: Record<string, string> = {
    basic: "Cơ bản",
    intermediate: "Trung cấp",
    advanced: "Nâng cao",
    expert: "Chuyên gia",
  };
  return labels[complexityStr] || complexityStr;
};

const getComplexityBadgeClass = (complexity: string | number) => {
  const complexityStr = String(complexity);
  const classes: Record<string, string> = {
    basic: "bg-green-500 text-white",
    intermediate: "bg-blue-500 text-white",
    advanced: "bg-orange-500 text-white",
    expert: "bg-red-500 text-white",
  };
  return classes[complexityStr] || "bg-gray-500 text-white";
};

const summaryStatCards = computed(() => {
  if (!summary.value) return [];

  return [
    {
      key: "total",
      label: "Tổng số ca bệnh",
      value: summary.value.total_cases,
      valueClass: "text-blue-600",
      iconBgClass: "bg-blue-100",
      iconClass: "text-blue-600",
      iconPath:
        "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z",
    },
    {
      key: "completion",
      label: "Tỷ lệ hoàn thành",
      value: `${summary.value.completion_stats.completion_rate}%`,
      valueClass: "text-green-600",
      iconBgClass: "bg-green-100",
      iconClass: "text-green-600",
      iconPath: "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z",
    },
    {
      key: "hours",
      label: "Tổng giờ học",
      value: summary.value.learning_metrics.total_study_hours,
      valueClass: "text-purple-600",
      iconBgClass: "bg-purple-100",
      iconClass: "text-purple-600",
      iconPath: "M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z",
    },
    {
      key: "weekly",
      label: "Ca bệnh tuần này",
      value: summary.value.learning_metrics.cases_created_this_week,
      valueClass: "text-orange-600",
      iconBgClass: "bg-orange-100",
      iconClass: "text-orange-600",
      iconPath: "M13 7h8m0 0v8m0-8l-8 8-4-4-6 6",
    },
  ];
});

const distributionPanels = computed(() => {
  if (!summary.value) return [];

  return [
    {
      key: "priority",
      title: "Phân bố mức độ ưu tiên",
      data: summary.value.by_priority,
      badgeClass: (key: string | number) => getPriorityBadgeClass(key),
      label: (key: string | number) => getPriorityLabel(key),
      emptyText: "Chưa có dữ liệu mức độ ưu tiên",
    },
    {
      key: "complexity",
      title: "Phân bố mức độ phức tạp",
      data: summary.value.by_complexity,
      badgeClass: (key: string | number) => getComplexityBadgeClass(key),
      label: (key: string | number) => getComplexityLabel(key),
      emptyText: "Chưa có dữ liệu mức độ phức tạp",
    },
  ];
});

const fetchSummary = async () => {
  loading.value = true;
  error.value = "";

  try {
    const response = await casesService.getCaseSummaryStatistics();

    const dailyTrends = response.trends?.last_30_days?.daily || [];
    const recentWeekCount = dailyTrends
      .slice(-7)
      .reduce((sum: number, day: any) => sum + (day.count || 0), 0);

    const statusObj: any = {};
    const totalCases = response.summary?.total_cases || 1;
    response.distributions?.by_status?.forEach((item: any) => {
      const percentage = Math.round((item.count / totalCases) * 100);
      statusObj[item.case_status] = {
        count: item.count,
        label: getStatusLabel(item.case_status),
        percentage: percentage,
      };
    });

    const priorityObj: any = {};
    response.distributions?.by_priority?.forEach((item: any) => {
      priorityObj[item.priority_level] = item.count;
    });

    const complexityObj: any = {};
    response.distributions?.by_complexity?.forEach((item: any) => {
      complexityObj[item.complexity_level] = item.count;
    });

    const topSpecialties = (response.distributions?.by_specialty || [])
      .sort((a: any, b: any) => b.count - a.count)
      .slice(0, 5)
      .map((item: any) => ({ specialty: item.specialty, count: item.count }));

    summary.value = {
      total_cases: response.summary?.total_cases || 0,
      completion_stats: {
        completion_rate: Math.round(
          ((response.distributions?.by_status?.find(
            (s: any) => s.case_status === "reviewed",
          )?.count || 0) /
            (response.summary?.total_cases || 1)) *
            100,
        ),
      },
      learning_metrics: {
        total_study_hours: Math.round(
          (response.summary?.total_cases || 0) * 2.5,
        ),
        cases_created_this_week: recentWeekCount,
      },
      by_status: statusObj,
      by_priority: priorityObj,
      by_complexity: complexityObj,
      top_specialties: topSpecialties,
      status_distribution: response.distributions?.by_status || [],
      specialty_distribution: response.distributions?.by_specialty || [],
      priority_distribution: response.distributions?.by_priority || [],
      complexity_distribution: response.distributions?.by_complexity || [],
      department_performance: response.distributions?.by_department || [],
      recent_cases: [],
    };
  } catch (err: any) {
    error.value =
      err.response?.data?.detail || "Không thể tải dữ liệu tổng hợp";
  } finally {
    loading.value = false;
  }
};

const refreshData = () => {
  fetchSummary();
};

const viewCase = (caseId: number) => {
  router.push(`/cases/${caseId}`);
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString("vi-VN", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

onMounted(() => {
  fetchSummary();
});
</script>

<style scoped>
.case-summary-page {
  background: var(--background);
}

.summary-header {
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border);
}

/* ── Loading container ─────────────────────────────────── */
.loading-container {
  background: var(--card);
  gap: 1rem;
}

/* ── Panel heading ─────────────────────────────────────── */
.panel-heading {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--foreground);
  margin: 0;
}

/* ── Card border-radius fix ────────────────────────────── */
/*
  Problem: PrimeVue Card generates a .p-card wrapper with border-radius
  AND the host element from Tailwind also carries a border-radius. When
  the host's border meets the inner card's background the "acute inner
  corner stacking" artefact appears — a visible gap or sharp angle where
  the backgrounds meet.

  Fix:
    1. Set overflow: hidden on .p-card so the background never bleeds.
    2. Unify the radius value on every layer (.p-card, .p-card-body) to 12px.
    3. Zero out padding on .p-card-body (padding moved to the individual
       #content / #header template slots).
*/
:deep(.summary-card.p-card),
:deep(.summary-panel.p-card) {
  border: none !important;
  border-radius: 12px !important;
  overflow: hidden !important;
  background: var(--card);
  box-shadow: 0 0 0 1px var(--border);
}

:deep(.summary-card.p-card .p-card-body),
:deep(.summary-panel.p-card .p-card-body) {
  padding: 0 !important;
  border-radius: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  overflow: hidden !important;
}

:deep(.summary-card.p-card .p-card-content) {
  padding: 1.25rem;
  flex: 1;
}

:deep(.summary-panel.p-card .p-card-header) {
  padding: 1.1rem 1.25rem 0.6rem !important;
  border: none !important;
  background: var(--card) !important;
  border-radius: 0 !important;
  flex-shrink: 0;
  box-shadow: inset 0 -1px 0 0 var(--border) !important;
}

:deep(.summary-panel.p-card .p-card-content) {
  padding: 0.9rem 1.25rem 1.25rem;
  flex: 1;
}

/* ── Refresh button ────────────────────────────────────── */
.refresh-btn {
  min-height: 2.5rem;
  white-space: nowrap;
}

:deep(.refresh-btn.p-button.p-button-outlined) {
  border-color: var(--border);
  color: var(--foreground);
  background: var(--card);
}

:deep(.refresh-btn.p-button.p-button-outlined:hover) {
  border-color: var(--foreground);
  background: var(--secondary);
}

:deep(.refresh-btn.p-button.p-button-outlined:active) {
  transform: translateY(1px);
}

/* ── Recent case rows ──────────────────────────────────── */
.recent-case-row {
  border: 1px solid var(--border);
  border-radius: 8px;
  transition: background 0.2s ease;
}

.recent-case-row:hover {
  background: var(--secondary) !important;
}
</style>
