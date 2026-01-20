<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">Quản lý Người Dùng</h1>
        <p class="text-sm text-gray-500 mt-1">Tạo và quản lý tài khoản sinh viên, giảng viên, quản trị viên</p>
      </div>
      <button @click="openCreateModal"
        class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors flex items-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Tạo người dùng mới
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="bg-white rounded-lg border border-gray-200 p-6 shadow-sm text-center">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-blue-500"></div>
      <p class="text-gray-600 mt-2">Đang tải dữ liệu...</p>
    </div>

    <!-- Error State -->
    <div v-if="error && !loading" class="bg-red-50 rounded-lg border border-red-200 p-4 shadow-sm">
      <p class="text-red-700 font-medium">Lỗi:</p>
      <p class="text-red-600 text-sm mt-1">{{ error }}</p>
      <button @click="loadUsers()"
        class="mt-2 px-3 py-1 text-sm bg-red-600 hover:bg-red-700 text-white rounded transition-colors">
        Thử lại
      </button>
    </div>

    <!-- Search and Filter -->
    <div v-if="!loading" class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-xs font-medium text-gray-700 mb-2">Tìm kiếm</label>
          <input v-model="searchQuery" placeholder="Tên, email, ID..."
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm" />
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-700 mb-2">Vai trò</label>
          <select v-model="roleFilter"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm">
            <option value="">Tất cả vai trò</option>
            <option value="student">Sinh viên</option>
            <option value="instructor">Giảng viên</option>
            <option value="admin">Quản trị</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-700 mb-2">Trạng thái</label>
          <select v-model="statusFilter"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm">
            <option value="">Tất cả</option>
            <option value="active">Hoạt động</option>
            <option value="inactive">Không hoạt động</option>
          </select>
        </div>
        <div class="flex items-end">
          <button @click="resetFilters"
            class="w-full px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-md text-sm font-medium transition-colors">
            Xóa bộ lọc
          </button>
        </div>
      </div>
    </div>

    <!-- Users Table -->
    <div v-if="!loading" class="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
      <div class="p-4 border-b border-gray-200">
        <h3 class="font-semibold text-gray-800">Danh sách người dùng ({{ filteredUsers.length }})</h3>
      </div>

      <div class="overflow-x-auto">
        <table class="min-w-full text-sm">
          <thead>
            <tr class="bg-gray-50 border-b border-gray-200">
              <th class="px-6 py-3 text-left font-medium text-gray-700">Tên</th>
              <th class="px-6 py-3 text-left font-medium text-gray-700">Email</th>
              <th class="px-6 py-3 text-left font-medium text-gray-700">Vai trò</th>
              <th class="px-6 py-3 text-left font-medium text-gray-700">Khoa</th>
              <th class="px-6 py-3 text-left font-medium text-gray-700">Trạng thái</th>
              <th class="px-6 py-3 text-left font-medium text-gray-700">Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in filteredUsers" :key="user.id" class="border-b border-gray-100 hover:bg-gray-50">
              <td class="px-6 py-4">
                <div class="font-medium text-gray-900">{{ user.full_name || `${user.first_name} ${user.last_name}` }}
                </div>
                <div class="text-xs text-gray-500">{{ user.username }}</div>
              </td>
              <td class="px-6 py-4 text-gray-600">{{ user.email }}</td>
              <td class="px-6 py-4">
                <span :class="getRoleBadgeClass(user.role)" class="px-2 py-1 rounded-full text-xs font-medium">
                  {{ getRoleLabel(user.role) }}
                </span>
              </td>
              <td class="px-6 py-4 text-gray-600">{{ user.department_vietnamese_name || 'Chưa có' }}</td>
              <td class="px-6 py-4">
                <span :class="user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                  class="px-2 py-1 rounded-full text-xs font-medium">
                  {{ user.is_active ? 'Hoạt động' : 'Không hoạt động' }}
                </span>
              </td>
              <td class="px-6 py-4">
                <div class="flex gap-2">
                  <button @click="openEditModal(user)"
                    class="p-1 text-blue-600 hover:bg-blue-50 rounded transition-colors" title="Chỉnh sửa">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button @click="toggleUserStatus(user)"
                    :class="user.is_active ? 'text-orange-600 hover:bg-orange-50' : 'text-green-600 hover:bg-green-50'"
                    class="p-1 rounded transition-colors" :title="user.is_active ? 'Vô hiệu hóa' : 'Kích hoạt'">
                    <svg v-if="user.is_active" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                    </svg>
                    <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </button>
                  <button @click="confirmDelete(user)"
                    class="p-1 text-red-600 hover:bg-red-50 rounded transition-colors" title="Xóa">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200">
          <h2 class="text-xl font-bold text-gray-800">{{ isEditing ? 'Chỉnh sửa người dùng' : 'Tạo người dùng mới' }}
          </h2>
        </div>

        <form @submit.prevent="submitUser" class="p-6 space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Họ <span class="text-red-500">*</span></label>
              <input v-model="formData.first_name" required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Tên <span
                  class="text-red-500">*</span></label>
              <input v-model="formData.last_name" required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Username <span
                class="text-red-500">*</span></label>
            <input v-model="formData.username" required :disabled="isEditing"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100" />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email <span
                class="text-red-500">*</span></label>
            <input v-model="formData.email" type="email" required
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Mật khẩu {{ isEditing ? '(để trống nếu không đổi)' : '' }} <span v-if="!isEditing"
                class="text-red-500">*</span>
            </label>
            <input v-model="formData.password" type="password" :required="!isEditing"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Vai trò <span
                  class="text-red-500">*</span></label>
              <select v-model="formData.role" required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="">-- Chọn vai trò --</option>
                <option value="student">Sinh viên</option>
                <option value="instructor">Giảng viên</option>
                <option value="admin">Quản trị viên</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Khoa</label>
              <select v-model="formData.department"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option :value="null">-- Chưa chọn --</option>
                <option v-for="dept in departments" :key="dept?.id || 'empty'" :value="dept?.id">{{
                  dept?.vietnamese_name || dept?.name }}</option>
              </select>
            </div>
          </div>

          <div v-if="formData.role === 'student'">
            <label class="block text-sm font-medium text-gray-700 mb-1">Mã sinh viên</label>
            <input v-model="formData.student_id"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>

          <div v-if="formData.role === 'instructor' || formData.role === 'admin'">
            <label class="block text-sm font-medium text-gray-700 mb-1">Mã nhân viên</label>
            <input v-model="formData.employee_id"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>

          <div class="flex items-center gap-2">
            <input v-model="formData.is_active" type="checkbox" id="is_active"
              class="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500" />
            <label for="is_active" class="text-sm font-medium text-gray-700">Tài khoản hoạt động</label>
          </div>

          <div class="flex items-center gap-2">
            <input v-model="formData.is_staff" type="checkbox" id="is_staff"
              class="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500" />
            <label for="is_staff" class="text-sm font-medium text-gray-700">Quyền truy cập Django Admin</label>
          </div>

          <div class="flex justify-end gap-3 pt-4 border-t border-gray-200">
            <button type="button" @click="closeModal"
              class="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors">
              Hủy
            </button>
            <button type="submit" :disabled="submitting"
              class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors disabled:opacity-50">
              {{ submitting ? 'Đang lưu...' : (isEditing ? 'Cập nhật' : 'Tạo mới') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-xl w-full max-w-md p-6">
        <h3 class="text-lg font-bold text-gray-800 mb-2">Xác nhận xóa</h3>
        <p class="text-gray-600 mb-4">Bạn có chắc muốn xóa người dùng <strong>{{ userToDelete?.full_name }}</strong>?
        </p>
        <div class="flex justify-end gap-3">
          <button @click="showDeleteConfirm = false"
            class="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors">
            Hủy
          </button>
          <button @click="deleteUser"
            class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md transition-colors">
            Xóa
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'

interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  full_name: string
  role: string
  department: number | null
  department_name: string
  department_vietnamese_name: string
  student_id?: string
  employee_id?: string
  is_active: boolean
  is_staff: boolean
  created_at: string
}

interface Department {
  id: number
  name: string
  vietnamese_name: string
}

const users = ref<User[]>([])
const departments = ref<Department[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const searchQuery = ref('')
const roleFilter = ref('')
const statusFilter = ref('')
const showModal = ref(false)
const showDeleteConfirm = ref(false)
const isEditing = ref(false)
const submitting = ref(false)
const userToDelete = ref<User | null>(null)

const formData = ref({
  id: null as number | null,
  username: '',
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  role: '',
  department: null as number | null,
  student_id: '',
  employee_id: '',
  is_active: true,
  is_staff: false,
})

const filteredUsers = computed(() => {
  // Filter out null/undefined users first
  let filtered = users.value.filter(u => u && u.id)

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(u =>
      u.username?.toLowerCase().includes(query) ||
      u.email?.toLowerCase().includes(query) ||
      u.first_name?.toLowerCase().includes(query) ||
      u.last_name?.toLowerCase().includes(query) ||
      (u.student_id && u.student_id.toLowerCase().includes(query)) ||
      (u.employee_id && u.employee_id.toLowerCase().includes(query))
    )
  }

  if (roleFilter.value) {
    filtered = filtered.filter(u => u.role === roleFilter.value)
  }

  if (statusFilter.value) {
    filtered = filtered.filter(u =>
      statusFilter.value === 'active' ? u.is_active : !u.is_active
    )
  }

  return filtered
})

const loadUsers = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await api.get('/auth/admin/users/')
    // Handle paginated or direct array response, and filter out null users
    const data = response.data?.results || response.data || []
    users.value = Array.isArray(data) ? data.filter((u: any) => u && u.id) : []
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to load users'
    users.value = []
  } finally {
    loading.value = false
  }
}

const loadDepartments = async () => {
  try {
    const response = await api.get('/cases/departments/')
    // Handle both paginated and non-paginated responses
    const data = response.data?.results || response.data || []
    // Filter out any null/undefined departments
    departments.value = Array.isArray(data) ? data.filter((dept: any) => dept && dept.id) : []
  } catch (err) {
    console.error('Failed to load departments:', err)
    departments.value = []
  }
}

const openCreateModal = () => {
  isEditing.value = false
  formData.value = {
    id: null,
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    role: '',
    department: null,
    student_id: '',
    employee_id: '',
    is_active: true,
    is_staff: false,
  }
  showModal.value = true
}

const openEditModal = (user: User) => {
  isEditing.value = true
  formData.value = {
    id: user.id,
    username: user.username,
    email: user.email,
    password: '',
    first_name: user.first_name,
    last_name: user.last_name,
    role: user.role,
    department: user.department,
    student_id: user.student_id || '',
    employee_id: user.employee_id || '',
    is_active: user.is_active,
    is_staff: user.is_staff,
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const submitUser = async () => {
  submitting.value = true
  error.value = null

  try {
    const payload: any = {
      username: formData.value.username,
      email: formData.value.email,
      first_name: formData.value.first_name,
      last_name: formData.value.last_name,
      role: formData.value.role,
      department: formData.value.department,
      is_active: formData.value.is_active,
      is_staff: formData.value.is_staff,
    }

    if (formData.value.password) {
      payload.password = formData.value.password
    }

    if (formData.value.role === 'student' && formData.value.student_id) {
      payload.student_id = formData.value.student_id
    }

    if ((formData.value.role === 'instructor' || formData.value.role === 'admin') && formData.value.employee_id) {
      payload.employee_id = formData.value.employee_id
    }

    if (isEditing.value && formData.value.id) {
      await api.put(`/auth/admin/users/${formData.value.id}/`, payload)
    } else {
      await api.post('/auth/admin/users/', payload)
    }

    closeModal()
    await loadUsers()
  } catch (err: any) {
    error.value = err.response?.data?.detail || err.response?.data?.error || 'Failed to save user'
    alert(error.value)
  } finally {
    submitting.value = false
  }
}

const toggleUserStatus = async (user: User) => {
  try {
    const action = user.is_active ? 'deactivate' : 'activate'
    await api.post(`/auth/admin/users/${user.id}/${action}/`)
    await loadUsers()
  } catch (err: any) {
    alert(err.response?.data?.detail || 'Failed to update user status')
  }
}

const confirmDelete = (user: User) => {
  userToDelete.value = user
  showDeleteConfirm.value = true
}

const deleteUser = async () => {
  if (!userToDelete.value) return

  try {
    await api.delete(`/auth/admin/users/${userToDelete.value.id}/`)
    showDeleteConfirm.value = false
    userToDelete.value = null
    await loadUsers()
  } catch (err: any) {
    alert(err.response?.data?.detail || 'Failed to delete user')
  }
}

const resetFilters = () => {
  searchQuery.value = ''
  roleFilter.value = ''
  statusFilter.value = ''
}

const getRoleLabel = (role: string) => {
  const labels: Record<string, string> = {
    student: 'Sinh viên',
    instructor: 'Giảng viên',
    admin: 'Quản trị viên',
  }
  return labels[role] || role
}

const getRoleBadgeClass = (role: string) => {
  const classes: Record<string, string> = {
    student: 'bg-blue-100 text-blue-800',
    instructor: 'bg-purple-100 text-purple-800',
    admin: 'bg-red-100 text-red-800',
  }
  return classes[role] || 'bg-gray-100 text-gray-800'
}

onMounted(() => {
  loadUsers()
  loadDepartments()
})
</script>
