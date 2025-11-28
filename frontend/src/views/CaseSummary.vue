<template>
  <div class="p-6 space-y-6 max-w-7xl mx-auto">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Bệnh án tổng hợp</h1>
        <p class="text-gray-600 mt-1">Tổng quan và phân tích các ca bệnh của bạn</p>
      </div>
      <Button variant="outline" @click="refreshData">
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        Làm mới
      </Button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <!-- Summary Content -->
    <div v-else-if="summary" class="space-y-6">
      <!-- Statistics Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <!-- Total Cases -->
        <Card>
          <CardContent class="p-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-600">Tổng số ca bệnh</p>
                <p class="text-3xl font-bold text-blue-600 mt-2">{{ summary.total_cases }}</p>
              </div>
              <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Completion Rate -->
        <Card>
          <CardContent class="p-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-600">Tỷ lệ hoàn thành</p>
                <p class="text-3xl font-bold text-green-600 mt-2">{{ summary.completion_stats.completion_rate }}%</p>
              </div>
              <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Study Hours -->
        <Card>
          <CardContent class="p-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-600">Tổng giờ học</p>
                <p class="text-3xl font-bold text-purple-600 mt-2">{{ summary.learning_metrics.total_study_hours }}</p>
              </div>
              <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- This Week -->
        <Card>
          <CardContent class="p-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-600">Ca bệnh tuần này</p>
                <p class="text-3xl font-bold text-orange-600 mt-2">{{ summary.learning_metrics.cases_created_this_week }}</p>
              </div>
              <div class="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- Charts Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Status Distribution -->
        <Card>
          <CardHeader>
            <CardTitle>Phân bố theo trạng thái</CardTitle>
          </CardHeader>
          <CardContent>
            <div class="space-y-3">
              <div v-for="(status, key) in summary.by_status" :key="key" class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <Badge :class="getStatusBadgeClass(key)">{{ status.label }}</Badge>
                  <span class="text-sm text-gray-600">{{ status.count }} ca</span>
                </div>
                <div class="flex items-center gap-2">
                  <div class="w-32 bg-gray-200 rounded-full h-2">
                    <div 
                      class="h-2 rounded-full transition-all"
                      :class="getStatusBarClass(key)"
                      :style="{ width: status.percentage + '%' }"
                    ></div>
                  </div>
                  <span class="text-sm font-medium text-gray-700 w-12 text-right">{{ status.percentage }}%</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Top Specialties -->
        <Card>
          <CardHeader>
            <CardTitle>Chuyên khoa hàng đầu</CardTitle>
          </CardHeader>
          <CardContent>
            <div class="space-y-3">
              <div v-for="(item, index) in summary.top_specialties" :key="index" class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <span class="w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs font-bold">
                    {{ index + 1 }}
                  </span>
                  <span class="text-sm font-medium text-gray-700">{{ item.specialty }}</span>
                </div>
                <Badge variant="secondary">{{ item.count }} ca</Badge>
              </div>
              <div v-if="summary.top_specialties.length === 0" class="text-center text-gray-500 py-4">
                Chưa có dữ liệu chuyên khoa
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Priority Distribution -->
        <Card>
          <CardHeader>
            <CardTitle>Phân bố mức độ ưu tiên</CardTitle>
          </CardHeader>
          <CardContent>
            <div class="space-y-3">
              <div v-for="(count, priority) in summary.by_priority" :key="priority" class="flex items-center justify-between">
                <Badge :class="getPriorityBadgeClass(priority)">
                  {{ getPriorityLabel(priority) }}
                </Badge>
                <span class="text-sm font-medium text-gray-700">{{ count }} ca</span>
              </div>
              <div v-if="Object.keys(summary.by_priority).length === 0" class="text-center text-gray-500 py-4">
                Chưa có dữ liệu mức độ ưu tiên
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Complexity Distribution -->
        <Card>
          <CardHeader>
            <CardTitle>Phân bố mức độ phức tạp</CardTitle>
          </CardHeader>
          <CardContent>
            <div class="space-y-3">
              <div v-for="(count, complexity) in summary.by_complexity" :key="complexity" class="flex items-center justify-between">
                <Badge :class="getComplexityBadgeClass(complexity)">
                  {{ getComplexityLabel(complexity) }}
                </Badge>
                <span class="text-sm font-medium text-gray-700">{{ count }} ca</span>
              </div>
              <div v-if="Object.keys(summary.by_complexity).length === 0" class="text-center text-gray-500 py-4">
                Chưa có dữ liệu mức độ phức tạp
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- Recent Cases -->
      <Card>
        <CardHeader>
          <CardTitle>Ca bệnh gần đây</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-3">
            <div 
              v-for="caseItem in summary.recent_cases" 
              :key="caseItem.id"
              class="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50 transition-colors cursor-pointer"
              @click="viewCase(caseItem.id)"
            >
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-1">
                  <h4 class="font-medium text-gray-900">{{ caseItem.title }}</h4>
                  <Badge variant="secondary" class="text-xs">{{ caseItem.specialty }}</Badge>
                  <Badge :class="getStatusBadgeClass(caseItem.case_status)" class="text-xs">
                    {{ getStatusLabel(caseItem.case_status) }}
                  </Badge>
                </div>
                <p class="text-sm text-gray-500">
                  Ngày tạo: {{ formatDate(caseItem.created_at) }}
                </p>
              </div>
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </div>
            <div v-if="summary.recent_cases.length === 0" class="text-center text-gray-500 py-8">
              Chưa có ca bệnh nào
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <p class="text-red-600 mb-4">{{ error }}</p>
      <Button @click="refreshData">Thử lại</Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { casesService } from '@/services/cases'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import Badge from '@/components/ui/Badge.vue'

const router = useRouter()

const loading = ref(true)
const error = ref('')
const summary = ref<any>(null)

const fetchSummary = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await casesService.getCaseSummary()
    summary.value = response
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Không thể tải dữ liệu tổng hợp'
    console.error('Error fetching case summary:', err)
  } finally {
    loading.value = false
  }
}

const refreshData = () => {
  fetchSummary()
}

const viewCase = (caseId: number) => {
  router.push(`/cases/${caseId}`)
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('vi-VN', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
}

const getStatusLabel = (status: string | number) => {
  const statusStr = String(status)
  const labels: Record<string, string> = {
    draft: 'Bản nháp',
    submitted: 'Đã nộp',
    reviewed: 'Đã xem xét',
    approved: 'Đã phê duyệt'
  }
  return labels[statusStr] || statusStr
}

const getStatusBadgeClass = (status: string | number) => {
  const statusStr = String(status)
  const classes: Record<string, string> = {
    draft: 'bg-gray-500 text-white',
    submitted: 'bg-yellow-500 text-white',
    reviewed: 'bg-blue-500 text-white',
    approved: 'bg-green-500 text-white'
  }
  return classes[statusStr] || 'bg-gray-500 text-white'
}

const getStatusBarClass = (status: string | number) => {
  const statusStr = String(status)
  const classes: Record<string, string> = {
    draft: 'bg-gray-500',
    submitted: 'bg-yellow-500',
    reviewed: 'bg-blue-500',
    approved: 'bg-green-500'
  }
  return classes[statusStr] || 'bg-gray-500'
}

const getPriorityLabel = (priority: string | number) => {
  const priorityStr = String(priority)
  const labels: Record<string, string> = {
    low: 'Thấp',
    medium: 'Trung bình',
    high: 'Cao',
    urgent: 'Khẩn cấp'
  }
  return labels[priorityStr] || priorityStr
}

const getPriorityBadgeClass = (priority: string | number) => {
  const priorityStr = String(priority)
  const classes: Record<string, string> = {
    low: 'bg-gray-500 text-white',
    medium: 'bg-blue-500 text-white',
    high: 'bg-orange-500 text-white',
    urgent: 'bg-red-500 text-white'
  }
  return classes[priorityStr] || 'bg-gray-500 text-white'
}

const getComplexityLabel = (complexity: string | number) => {
  const complexityStr = String(complexity)
  const labels: Record<string, string> = {
    basic: 'Cơ bản',
    intermediate: 'Trung cấp',
    advanced: 'Nâng cao',
    expert: 'Chuyên gia'
  }
  return labels[complexityStr] || complexityStr
}

const getComplexityBadgeClass = (complexity: string | number) => {
  const complexityStr = String(complexity)
  const classes: Record<string, string> = {
    basic: 'bg-green-500 text-white',
    intermediate: 'bg-blue-500 text-white',
    advanced: 'bg-orange-500 text-white',
    expert: 'bg-red-500 text-white'
  }
  return classes[complexityStr] || 'bg-gray-500 text-white'
}

onMounted(() => {
  fetchSummary()
})
</script>
