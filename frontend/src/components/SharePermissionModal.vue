<template>
  <div v-if="open" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    @click="$emit('update:open', false)">
    <div class="bg-white rounded-lg p-6 w-full max-w-md m-4" @click.stop>
      <div class="mb-4">
        <h2 class="text-xl font-bold">
          {{ currentLang === 'vi' ? 'Cấp quyền truy cập' : 'Grant Access Permission' }}
        </h2>
        <p class="text-gray-600">
          {{ currentLang === 'vi' ?
            'Chia sẻ ca bệnh này với người dùng hoặc nhóm'
            : 'Share this case with users or groups' }}
        </p>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="space-y-4">
          <!-- Share Type -->
          <div>
            <label class="block text-sm font-medium mb-1">
              {{ currentLang === 'vi' ? 'Loại chia sẻ' : 'Share Type' }}
            </label>
            <select v-model="form.shareType" class="w-full border rounded-md p-2">
              <option value="individual">
                {{ currentLang === 'vi' ? 'Chia sẻ cá nhân' : 'Individual User' }}
              </option>
              <option value="department">
                {{ currentLang === 'vi' ? 'Chia sẻ khoa' : 'Department' }}
              </option>
              <option value="public">
                {{ currentLang === 'vi' ? 'Công khai' : 'Public Access' }}
              </option>
            </select>
          </div>

          <!-- User Selection -->
          <div v-if="form.shareType === 'individual'">
            <label class="block text-sm font-medium mb-1">
              {{ currentLang === 'vi' ? 'Người dùng' : 'User' }}
            </label>
            <div class="relative">
              <input v-model="form.searchQuery" type="text" class="w-full border rounded-md p-2"
                :placeholder="form.selectedUser ? form.selectedUser.full_name : (currentLang === 'vi' ? 'Tìm kiếm giảng viên...' : 'Search instructors...')"
                autocomplete="off" @focus="showSearchResults = true" @blur="hideSearchResults" />
              <!-- Search Results Dropdown -->
              <div v-if="showSearchResults && !form.selectedUser && searchResults.length > 0"
                class="absolute z-10 mt-1 w-full bg-white border rounded-md shadow-lg max-h-40 overflow-y-auto">
                <div v-for="user in searchResults" :key="user.id" @click="selectUser(user)"
                  class="p-3 hover:bg-gray-100 cursor-pointer border-b last:border-b-0">
                  <div class="font-medium">{{ user.full_name }}</div>
                  <div class="text-sm text-gray-500">{{ user.email }}</div>
                  <div class="text-xs text-gray-400">{{ user.department }}</div>
                </div>
              </div>
              <!-- No Results Message -->
              <div
                v-else-if="showSearchResults && !form.selectedUser && form.searchQuery.length >= 2 && searchResults.length === 0"
                class="absolute z-10 mt-1 w-full bg-white border rounded-md shadow-lg">
                <div class="p-3 text-gray-500 text-center">
                  {{ currentLang === 'vi' ? 'Không tìm thấy người dùng nào' : 'No users found' }}
                </div>
              </div>
            </div>
            <!-- Selected User Display -->
            <div v-if="form.selectedUser" class="mt-2 p-2 bg-blue-50 rounded-md flex items-center justify-between">
              <div class="text-sm">
                <span class="font-medium">{{ currentLang === 'vi' ? 'Đã chọn:' : 'Selected:' }}</span>
                {{ form.selectedUser.full_name }} ({{ form.selectedUser.email }})
              </div>
              <button type="button" @click="clearSelectedUser" class="text-red-500 hover:text-red-700 ml-2">
                ✕
              </button>
            </div>
          </div>

          <!-- Department Selection -->
          <div v-if="form.shareType === 'department'">
            <label class="block text-sm font-medium mb-1">
              {{ currentLang === 'vi' ? 'Chia sẻ với khôa' : 'Share with Department' }}
            </label>
            <div class="p-3 bg-blue-50 rounded-md border">
              <div class="flex items-center space-x-2">
                <BuildingIcon class="w-5 h-5 text-blue-500" />
                <div>
                  <div class="font-medium text-blue-800">
                    {{ userDepartment?.vietnamese_name || userDepartment?.name || 'Unknown Department' }}
                  </div>
                  <div class="text-sm text-blue-600">
                    {{ currentLang === 'vi' ?
                      'Tất cả sinh viên trong khoa này sẽ có thể xem ca bệnh'
                      : 'All students in this department will be able to view the case ' }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Permission Type -->
          <div>
            <label class="block text-sm font-medium mb-1">
              {{ currentLang === 'vi' ? 'Loại quyền' : 'Permission Type' }}
            </label>
            <select v-model="form.permissionType" class="w-full border rounded-md p-2">
              <option value="view">
                {{ currentLang === 'vi' ? 'Chỉ xem' : 'Read Only' }}
              </option>
              <option value="comment">
                {{ currentLang === 'vi' ? 'Xem và bình luận' : 'Read & Comment' }}
              </option>
              <option value="analyze">
                {{ currentLang === 'vi' ? 'Xem, bình luận và phân tích' : 'Read, Comment & Analyze' }}
              </option>
              <option value="edit">
                {{ currentLang === 'vi' ? 'Toàn quyền chỉnh sửa' : 'Full Edit Access' }}
              </option>
            </select>
          </div>

          <!-- Expiry Date -->
          <div>
            <label class="block text-sm font-medium mb-1">
              {{ currentLang === 'vi' ? 'Ngày hết hạn (tuỳ chọn)' : 'Expiry Date (Optional)' }}
            </label>
            <input type="datetime-local" v-model="form.expiresAt" class="w-full border rounded-md p-2"
              :min="new Date().toISOString().slice(0, 16)" />
          </div>

          <!-- Custom Message -->
          <div>
            <label class="block text-sm font-medium mb-1">
              {{ currentLang === 'vi' ? 'Tin nhắn (tuỳ chọn)' : 'Message (Optional)' }}
            </label>
            <textarea v-model="form.message" class="w-full border rounded-md p-2"
              :placeholder="currentLang === 'vi' ? 'Thêm tin nhắn cho người nhận...' : 'Add a message for the recipient...'"
              rows="3"></textarea>
          </div>
        </div>

        <div class="flex justify-end space-x-2 mt-6">
          <button type="button" class="px-4 py-2 border rounded-md hover:bg-gray-50"
            @click="$emit('update:open', false)">
            {{ currentLang === 'vi' ? 'Huỷ' : 'Cancel' }}
          </button>
          <button type="submit"
            class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:opacity-50"
            :disabled="!canSubmit || loading">
            <span v-if="loading">⏳</span>
            {{ currentLang === 'vi' ? 'Cấp quyền' : 'Grant Access' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useLanguage } from '@/composables/useLanguage'
import { useToast } from '@/composables/useToast'
import { sharingService } from '@/services/sharing'
import api from '@/services/api'
import type { SharePermission, CreatePermissionRequest } from '@/services/sharing'
import BuildingIcon from '@/components/icons/BuildingIcon.vue'

// Debounce utility
const debounce = <T extends (...args: any[]) => void>(func: T, delay: number): T => {
  let timeoutId: number
  return ((...args: any[]) => {
    window.clearTimeout(timeoutId)
    timeoutId = window.setTimeout(() => func(...args), delay)
  }) as T
}

type ShareType = 'individual' | 'department' | 'public'
type PermissionType = 'view' | 'comment' | 'analyze' | 'edit'

interface Props {
  open: boolean
  caseId: number
  shareType?: ShareType
}

interface User {
  id: number
  full_name: string
  email: string
  department: string
}

interface Department {
  id: number
  name: string
  vietnamese_name?: string
}

interface Emits {
  (event: 'update:open', value: boolean): void
  (event: 'permission-created', permission: SharePermission): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const { currentLang } = useLanguage()
const toast = useToast()

const loading = ref(false)
const searchResults = ref<User[]>([])
const departments = ref<Department[]>([])
const userDepartment = ref<Department | null>(null)
const searchTimeout = ref<number | null>(null)
const showSearchResults = ref(false)

// Helper to hide search results with delay
const hideSearchResults = () => {
  window.setTimeout(() => {
    showSearchResults.value = false
  }, 200)
}

const form = ref({
  shareType: 'individual' as 'individual' | 'department' | 'public',
  permissionType: 'view' as 'view' | 'comment' | 'analyze' | 'edit',
  searchQuery: '',
  selectedUser: null as User | null,
  departmentId: '',
  expiresAt: '',
  message: ''
})// Backend-compatible form data
const getPermissionData = (): CreatePermissionRequest => {
  const data: CreatePermissionRequest = {
    share_type: form.value.shareType,
    permission_type: form.value.permissionType,
  }

  // Add optional fields
  if (form.value.expiresAt) {
    data.expires_at = form.value.expiresAt
  }
  if (form.value.message) {
    data.notes = form.value.message
  }

  // Add type-specific fields
  if (form.value.shareType === 'individual' && form.value.selectedUser) {
    data.user = form.value.selectedUser.id
  } else if (form.value.shareType === 'department' && userDepartment.value) {
    data.target_department = userDepartment.value.id
  }
  // For 'public' type, no additional fields needed

  console.log('Permission data being sent:', data) // Debug log
  return data
}

const canSubmit = computed(() => {
  if (form.value.shareType === 'individual') {
    return form.value.selectedUser && form.value.permissionType
  } else if (form.value.shareType === 'department') {
    return userDepartment.value && form.value.permissionType
  } else if (form.value.shareType === 'public') {
    return form.value.permissionType
  }
  return false
})

// Reset form when modal opens/closes
watch(() => props.open, (isOpen) => {
  if (isOpen) {
    form.value.shareType = props.shareType || 'individual'
    loadDepartments()
    loadUserDepartment()
  } else {
    resetForm()
  }
})

// Watch search query with debouncing
watch(() => form.value.searchQuery, () => {
  if (form.value.shareType === 'individual') {
    debouncedSearchUsers()
  }
})

// Watch share type changes
watch(() => form.value.shareType, (newType) => {
  // Clear relevant form data when switching types
  if (newType !== 'individual') {
    clearSelectedUser()
  }
  if (newType !== 'department') {
    form.value.departmentId = ''
  }
})

const resetForm = () => {
  form.value = {
    shareType: 'individual',
    searchQuery: '',
    selectedUser: null,
    departmentId: '',
    permissionType: 'view',
    expiresAt: '',
    message: ''
  }
  searchResults.value = []
  showSearchResults.value = false
}

const loadDepartments = async () => {
  // Simple caching to avoid repeated API calls
  if (departments.value.length > 0) {
    return
  }

  try {
    const list = await sharingService.getDepartments({
      ordering: 'name',
      page_size: 100 // Get more departments at once
    })
    departments.value = list
  } catch (error) {
    console.error('Failed to load departments:', error)
    departments.value = []
    toast.toast.error(
      currentLang.value === 'vi'
        ? 'Không thể tải danh sách khoa'
        : 'Failed to load departments'
    )
  }
}

// Load departments on component mount for caching
onMounted(() => {
  loadDepartments()
})

const loadUserDepartment = async () => {
  try {
    // Get current user's profile to find their department
    const response = await api.get('/auth/profile/')
    const user = response.data

    console.log('User profile:', user) // Debug log

    if (user.department) {
      // Handle both ID reference and nested object
      if (typeof user.department === 'object') {
        userDepartment.value = user.department
      } else {
        // If department is just an ID, we need to get the full department data
        const departments = await sharingService.getDepartments()
        userDepartment.value = departments.find((dept: Department) => dept.id === user.department)
      }

      console.log('User department set:', userDepartment.value) // Debug log
    } else {
      console.warn('User has no department assigned')
      toast.toast.error(
        currentLang.value === 'vi'
          ? 'Bạn chưa được phân vào khôa nào'
          : 'You are not assigned to any department'
      )
    }
  } catch (error) {
    console.error('Failed to load user department:', error)
    toast.toast.error(
      currentLang.value === 'vi'
        ? 'Không thể tải thông tin khôa'
        : 'Failed to load department information'
    )
  }
}

const searchUsers = async () => {
  if (form.value.searchQuery.length < 2) {
    searchResults.value = []
    return
  }

  try {
    // Use the correct API endpoint for user search
    const response = await api.get('/auth/users/', {
      params: {
        search: form.value.searchQuery,
        role: 'instructor', // Only search for instructors for sharing
        page_size: 10 // Limit results for performance
      }
    })

    // Handle paginated response
    const users = Array.isArray(response.data) ? response.data : response.data.results || []
    searchResults.value = users.map((user: any) => ({
      id: user.id,
      full_name: user.first_name && user.last_name ? `${user.first_name} ${user.last_name}` : user.username,
      email: user.email,
      department: user.department?.name || 'Unknown Department'
    }))
  } catch (error) {
    console.error('Failed to search users:', error)
    searchResults.value = []
    toast.toast.error(
      currentLang.value === 'vi'
        ? 'Không thể tìm kiếm người dùng'
        : 'Failed to search users'
    )
  }
}

// Debounced search function
const debouncedSearchUsers = debounce(searchUsers, 300)

const selectUser = (user: User) => {
  form.value.selectedUser = user
  form.value.searchQuery = user.full_name
  searchResults.value = []
  showSearchResults.value = false
}

const clearSelectedUser = () => {
  form.value.selectedUser = null
  form.value.searchQuery = ''
  searchResults.value = []
  showSearchResults.value = false
}

const handleSubmit = async () => {
  if (!canSubmit.value) return

  loading.value = true
  try {
    const permissionData = getPermissionData()

    // For department sharing, we'll share with all students in that department
    // The backend should handle creating individual permissions for each student
    const permission = await sharingService.createPermission(props.caseId, permissionData)

    let successMessage = ''
    if (form.value.shareType === 'department') {
      const deptName = userDepartment.value ? (currentLang.value === 'vi' ? userDepartment.value.vietnamese_name || userDepartment.value.name : userDepartment.value.name) : 'department'
      successMessage = currentLang.value === 'vi'
        ? `Đã chia sẻ với tất cả sinh viên trong khôa ${deptName}!`
        : `Shared with all students in ${deptName} department!`
    } else if (form.value.shareType === 'public') {
      successMessage = currentLang.value === 'vi'
        ? 'Ca bệnh đã được công khai!'
        : 'Case has been made public!'
    } else {
      const userName = form.value.selectedUser?.full_name || 'user'
      successMessage = currentLang.value === 'vi'
        ? `Đã chia sẻ với ${userName}!`
        : `Shared with ${userName}!`
    }

    toast.toast.success(successMessage)

    emit('permission-created', permission)
    emit('update:open', false)
  } catch (error: any) {
    console.error('Failed to create permission:', error)
    console.error('Error response:', error.response?.data) // Additional debug info

    let errorMessage = ''
    if (error.response?.data?.error) {
      errorMessage = error.response.data.error
    } else if (error.response?.data?.detail) {
      errorMessage = error.response.data.detail
    } else if (error.response?.data?.message) {
      errorMessage = error.response.data.message
    } else {
      errorMessage = currentLang.value === 'vi'
        ? 'Không thể cấp quyền truy cập'
        : 'Failed to grant access permission'
    }

    toast.toast.error(errorMessage)
  } finally {
    loading.value = false
  }
}
</script>
