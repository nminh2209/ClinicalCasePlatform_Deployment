<template>
  <div class="cases-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1>Ca bệnh được phê duyệt</h1>
        <p class="subtitle">Tất cả ca bệnh đã được phê duyệt từ sinh viên khác</p>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="filters-section">
      <div class="search-and-filters">
        <div class="search-container">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            class="search-icon">
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.35-4.35" />
          </svg>
          <input v-model="searchQuery" @input="handleSearch" type="text"
            placeholder="Tìm kiếm ca bệnh theo tên, chuyên khoa, bệnh nhân..." class="search-input" />
        </div>

        <div class="filter-options">
          <select v-model="specialtyFilter" @change="applyFilters" class="filter-select">
            <option value="">Tất cả chuyên khoa</option>
            <option value="Tim mạch">Tim mạch</option>
            <option value="Nội khoa">Nội khoa</option>
            <option value="Phẫu thuật">Phẫu thuật</option>
            <option value="Hô hấp">Hô hấp</option>
            <option value="Tiêu hóa">Tiêu hóa</option>
            <option value="Thần kinh">Thần kinh</option>
            <option value="Sản phụ khoa">Sản phụ khoa</option>
            <option value="Nhi khoa">Nhi khoa</option>
          </select>

          <select v-model="dateSort" class="filter-select">
            <option selected value="newest">Mới nhất</option>
            <option value="oldest">Cũ nhất</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Stats Card -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon stat-success">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
            <polyline points="22,4 12,14.01 9,11.01" />
          </svg>
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
          <button @click="loadCases" class="btn btn-primary">Thử lại</button>
        </div>

        <div class="cases-grid" v-if="!loading && !error">
          <div v-if="filteredCases.length === 0" class="empty-state">
            <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
            </svg>
            <h3>Không tìm thấy ca bệnh được phê duyệt</h3>
            <p v-if="searchQuery || specialtyFilter">Thử điều chỉnh bộ lọc hoặc từ khóa tìm kiếm</p>
            <p v-else>Chưa có ca bệnh nào được phê duyệt</p>
          </div>

          <div v-for="case_ in filteredCases" :key="case_.id" class="case-card">
            <div class="case-header">
              <h3>{{ case_.title }}</h3>
              <span class="status-badge approved">
                Đã phê duyệt
              </span>
            </div>

            <div class="case-meta">
              <p><strong>Sinh viên:</strong> {{ case_.student_name || 'N/A' }}</p>
              <p><strong>Bệnh nhân:</strong> {{ case_.patient_name }}</p>
              <p><strong>Tuổi:</strong> {{ case_.patient_age }}</p>
              <p><strong>Chuyên khoa:</strong> {{ case_.specialty }}</p>
              <p><strong>Ngày tạo:</strong> {{ formatDate(case_.created_at) }}</p>
            </div>

            <div class="case-actions">
              <button @click="viewCase(case_)" class="btn btn-primary btn-sm">
                Xem chi tiết
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { requireRoles } from '@/composables/useAuthorize'
import { casesService } from '@/services/cases'

const router = useRouter()

const searchQuery = ref('')
const specialtyFilter = ref('')
const dateSort = ref('newest')
const cases = ref<any[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

const filteredCases = computed(() => {
  let filtered = cases.value

  // Filter by specialty
  if (specialtyFilter.value) {
    filtered = filtered.filter(c => c.specialty === specialtyFilter.value)
  }

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(c =>
      c.title.toLowerCase().includes(query) ||
      c.specialty.toLowerCase().includes(query) ||
      c.patient_name.toLowerCase().includes(query) ||
      (c.keywords && c.keywords.toLowerCase().includes(query)) ||
      (c.student_name && c.student_name.toLowerCase().includes(query))
    )
  }

  // Sort by date
  if (dateSort.value) {
    filtered = [...filtered].sort((a, b) => {
      const dateA = new Date(a.created_at).getTime()
      const dateB = new Date(b.created_at).getTime()
      
      if (dateSort.value === 'newest') {
        return dateB - dateA
      } else if (dateSort.value === 'oldest') {
        return dateA - dateB
      }
      return 0
    })
  }

  return filtered
})

async function loadCases() {
  loading.value = true
  error.value = null
  
  try {
    // Fetch only approved cases from all users
    console.log('Fetching approved cases...')
    const data = await casesService.getCases({ case_status: 'approved' })
    console.log('Received data:', data)
    console.log('Number of cases:', Array.isArray(data) ? data.length : 'Not an array')
    
    // Check if data is an array or if it's paginated
    if (Array.isArray(data)) {
      cases.value = data
    } else if (data && data.results) {
      // Handle paginated response
      cases.value = data.results
    } else {
      console.warn('Unexpected data format:', data)
      cases.value = []
    }
  } catch (err: any) {
    console.error('Failed to load approved cases:', err)
    console.error('Error response:', err.response?.data)
    error.value = 'Không thể tải ca bệnh. Vui lòng thử lại.'
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  // Search is reactive through computed property
}

function applyFilters() {
  // Filters are applied reactively through computed property
}

function viewCase(case_: any) {
  router.push(`/cases/${case_.id}`)
}

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString('vi-VN')
}

onMounted(() => {
  requireRoles(['student', 'instructor'])
  loadCases()
})
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
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
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
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  transition: border-color 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.filter-options {
  display: flex;
  gap: 1rem;
}

.filter-select {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  background: white;
  min-width: 180px;
  font-size: 0.875rem;
}

.filter-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
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
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
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
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  transition: all 0.2s;
  border: 1px solid #f3f4f6;
}

.case-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border-color: #e5e7eb;
}

.case-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.case-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 1.125rem;
  line-height: 1.4;
  font-weight: 600;
}

.status-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.status-badge.approved {
  background: #dcfce7;
  color: #14532d;
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

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.2s;
  text-decoration: none;
  border: 1px solid transparent;
  cursor: pointer;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  flex: 1;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
  transform: translateY(-1px);
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
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

.w-16 {
  width: 4rem;
}

.h-16 {
  height: 4rem;
}

.text-gray-400 {
  color: #9ca3af;
}

.mx-auto {
  margin-left: auto;
  margin-right: auto;
}

.mb-4 {
  margin-bottom: 1rem;
}
</style>
