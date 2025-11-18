<template>
  <div class="case-sharing-panel bg-white rounded-lg shadow p-6">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-bold">
        {{ currentLang === 'vi' ? 'Quản lý chia sẻ ca bệnh' : 'Case Sharing Management' }}
      </h2>
      <div class="flex space-x-2">
        <Button @click="openShareModal('individual')" variant="default">
          ➕
          {{ currentLang === 'vi' ? 'Chia sẻ cá nhân' : 'Share with Individual' }}
        </Button>
        <Button @click="openShareModal('department')" variant="outline">
          🏢
          {{ currentLang === 'vi' ? 'Chia sẻ khoa' : 'Share with Department' }}
        </Button>
        <Button @click="openGuestModal" variant="outline">
          🔗
          {{ currentLang === 'vi' ? 'Chia sẻ khách' : 'Guest Access' }}
        </Button>
        <Button @click="openShareModal('public')" variant="outline">
          🌍
          {{ currentLang === 'vi' ? 'Công khai' : 'Make Public' }}
        </Button>
      </div>
    </div>

    <!-- Stats -->
    <div class="flex items-center space-x-4 mb-6 text-sm text-gray-600">
      <div class="flex items-center">
        📊
        {{ permissions.length }} {{ currentLang === 'vi' ? 'quyền chia sẻ' : 'sharing permissions' }}
      </div>
      <div class="flex items-center">
        🔗
        {{ guestAccesses.length }} {{ currentLang === 'vi' ? 'liên kết khách' : 'guest links' }}
      </div>
    </div>

    <!-- Current Permissions -->
    <div class="space-y-4">
      <!-- Bulk Actions -->
      <div class="flex justify-between items-center">
        <div class="flex items-center space-x-2">
          <input 
            type="checkbox" 
            v-model="selectAll" 
            @change="toggleSelectAll"
            class="rounded"
          >
          <span class="text-sm text-gray-600">
            {{ currentLang === 'vi' ? 'Chọn tất cả' : 'Select all' }}
          </span>
        </div>
        <div class="flex space-x-2">
          <Button 
            @click="bulkRevoke" 
            variant="destructive"
            :disabled="selectedPermissions.length === 0"
          >
            {{ currentLang === 'vi' ? 'Xóa các mục đã chọn' : 'Delete selected' }}
          </Button>
          <Button @click="() => refreshData(true)" size="sm" variant="outline">
            🔄
            {{ currentLang === 'vi' ? 'Làm mới' : 'Refresh' }}
          </Button>
        </div>
      </div>

      <!-- Permissions Table -->
      <div class="overflow-x-auto">
        <table class="w-full border-collapse border border-gray-200">
          <thead>
            <tr class="bg-gray-50">
              <th class="border border-gray-200 p-3 text-left">
                <input 
                  type="checkbox" 
                  v-model="selectAll" 
                  @change="toggleSelectAll"
                  class="rounded"
                >
              </th>
              <th class="border border-gray-200 p-3 text-left">
                {{ currentLang === 'vi' ? 'Được chia sẻ với' : 'Shared with' }}
              </th>
              <th class="border border-gray-200 p-3 text-left">
                {{ currentLang === 'vi' ? 'Loại quyền' : 'Permission Type' }}
              </th>
              <th class="border border-gray-200 p-3 text-left">
                {{ currentLang === 'vi' ? 'Hết hạn' : 'Expires' }}
              </th>
              <th class="border border-gray-200 p-3 text-left">
                {{ currentLang === 'vi' ? 'Trạng thái' : 'Status' }}
              </th>
              <th class="border border-gray-200 p-3 text-center">
                {{ currentLang === 'vi' ? 'Thao tác' : 'Actions' }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="permission in permissions" :key="permission.id">
              <td class="border border-gray-200 p-3">
                <input 
                  type="checkbox" 
                  :value="permission.id" 
                  v-model="selectedPermissions"
                  class="rounded"
                >
              </td>
              <td class="border border-gray-200 p-3">
                <div class="flex items-center space-x-2">
                  <UserIcon v-if="permission.share_type === 'individual'" class="w-4 h-4 text-blue-500" />
                  <BuildingIcon v-else-if="permission.share_type === 'department'" class="w-4 h-4 text-green-500" />
                  <GlobeIcon v-else-if="permission.share_type === 'public'" class="w-4 h-4 text-purple-500" />
                  
                  <div>
                    <div class="font-medium">{{ getPermissionDisplayName(permission) }}</div>
                    <div class="text-xs text-gray-500">{{ permission.share_description }}</div>
                  </div>
                </div>
              </td>
              <td class="border border-gray-200 p-3">
                <Badge :variant="getPermissionVariant(permission.permission_type)">
                  {{ getPermissionTypeText(permission.permission_type) }}
                </Badge>
              </td>
              <td class="border border-gray-200 p-3">
                <span class="text-sm" :class="permission.is_expired ? 'text-red-600' : 'text-gray-600'">
                  {{ permission.expires_at_display || (currentLang === 'vi' ? 'Không giới hạn' : 'No limit') }}
                </span>
              </td>
              <td class="border border-gray-200 p-3">
                <Badge :variant="permission.is_expired ? 'secondary' : 'success'">
                  {{ permission.is_expired ? (currentLang === 'vi' ? 'Hết hạn' : 'Expired') : (currentLang === 'vi' ? 'Hoạt động' : 'Active') }}
                </Badge>
              </td>
              <td class="border border-gray-200 p-3 text-center">
                <Button @click="revokePermission(permission.id)" size="sm" variant="destructive">
                  🗑️
                </Button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Empty state -->
      <div v-if="permissions.length === 0" class="text-center py-12 text-gray-500">
        🔒
        <h3 class="text-lg font-medium mb-2">
          {{ currentLang === 'vi' ? 'Chưa có quyền chia sẻ nào' : 'No sharing permissions yet' }}
        </h3>
        <p class="mb-4">
          {{ currentLang === 'vi' ? 'Bắt đầu chia sẻ ca bệnh này với đồng nghiệp của bạn' : 'Start sharing this case with your colleagues' }}
        </p>
        <Button @click="openShareModal('individual')">
          {{ currentLang === 'vi' ? 'Chia sẻ ngay' : 'Share Now' }}
        </Button>
      </div>
    </div>

    <!-- Guest Access Section -->
    <div v-if="guestAccesses.length > 0" class="mt-8">
      <h3 class="text-lg font-semibold mb-4">
        {{ currentLang === 'vi' ? 'Liên kết khách mời' : 'Guest Access Links' }}
      </h3>
      <div class="space-y-3">
        <div v-for="guest in guestAccesses" :key="guest.id" class="border rounded-lg p-4">
          <div class="flex justify-between items-start">
            <div>
              <h4 class="font-medium">{{ guest.guest_name || guest.guest_email }}</h4>
              <p class="text-sm text-gray-600">{{ guest.guest_email }}</p>
              <div class="flex items-center space-x-4 mt-2 text-sm">
                <span class="flex items-center">
                  🕒
                  {{ guest.expires_at_display }}
                </span>
                <span class="flex items-center">
                  👁️
                  {{ guest.access_count || 0 }} {{ currentLang === 'vi' ? 'lần truy cập' : 'accesses' }}
                </span>
                <Badge :variant="guest.is_expired ? 'secondary' : 'success'">
                  {{ guest.is_expired ? (currentLang === 'vi' ? 'Hết hạn' : 'Expired') : (currentLang === 'vi' ? 'Hoạt động' : 'Active') }}
                </Badge>
              </div>
            </div>
            <div class="flex space-x-2">
              <Button @click="copyGuestLink(guest)" size="sm" variant="outline">
                📋
                {{ currentLang === 'vi' ? 'Sao chép' : 'Copy' }}
              </Button>
              <Button @click="extendGuestAccess(guest)" size="sm" variant="outline" v-if="!guest.is_expired">
                🕒
                {{ currentLang === 'vi' ? 'Gia hạn' : 'Extend' }}
              </Button>
              <Button @click="deleteGuestAccess(guest.id)" size="sm" variant="destructive">
                🗑️
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Share Permission Modal -->
    <SharePermissionModal
      :open="showShareModal"
      @update:open="(value: boolean) => showShareModal = value"
      :case-id="caseId"
      :share-type="shareType"
      @permission-created="onPermissionCreated"
    />

    <!-- Guest Access Modal -->
    <GuestAccessModal
      :open="showGuestModal"
      @update:open="(value: boolean) => showGuestModal = value"
      :case-id="caseId"
      @guest-created="onGuestCreated"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted } from 'vue'
import { useLanguage } from '@/composables/useLanguage'
import { useToast } from '@/composables/useToast'
import sharingService from '@/services/sharing'
import Button from '@/components/ui/Button.vue'
import Badge from '@/components/ui/Badge.vue'
import SharePermissionModal from './SharePermissionModal.vue'
import GuestAccessModal from './GuestAccessModal.vue'

// Icons
import UserIcon from '@/components/icons/User.vue'
import BuildingIcon from '@/components/icons/BuildingIcon.vue'
import GlobeIcon from '@/components/icons/GlobeIcon.vue'

interface Permission {
  id: number
  case: number
  user?: number
  user_name?: string
  user_email?: string
  share_type: 'individual' | 'department' | 'class_group' | 'public'
  target_department?: number
  department_name?: string
  class_group?: string
  permission_type: 'view' | 'comment' | 'analyze' | 'edit'
  expires_at_display?: string
  is_active: boolean
  is_expired: boolean
  access_count?: number
  share_description?: string
}

interface GuestAccess {
  id: number
  case: number
  guest_email: string
  guest_name?: string
  permission_type: 'view' | 'comment'
  expires_at_display: string
  is_expired: boolean
  access_count: number
  access_token: string
}

const props = defineProps<{
  caseId: number
}>()

const { currentLang } = useLanguage()
const { toast } = useToast()

// State
const permissions = ref<Permission[]>([])
const guestAccesses = ref<GuestAccess[]>([])
const selectedPermissions = ref<number[]>([])
const selectAll = ref(false)

// Modal states
const showShareModal = ref(false)
const showGuestModal = ref(false)
type PanelShareType = 'individual' | 'department' | 'public'
const shareType = ref<PanelShareType>('individual')

// Cache for maintaining state per case
const dataCache = ref<Map<number, { permissions: Permission[], guests: GuestAccess[], timestamp: number }>>(new Map())
const CACHE_DURATION = 10 * 60 * 1000 // 10 minutes - longer persistence

// Methods
const refreshData = async (forceRefresh = false) => {
  try {
    const cacheKey = props.caseId
    const cachedData = dataCache.value.get(cacheKey)
    
    // Check cache first unless force refresh
    if (!forceRefresh && cachedData && Date.now() - cachedData.timestamp < CACHE_DURATION) {
      permissions.value = [...cachedData.permissions] // Clone to avoid reference issues
      guestAccesses.value = [...cachedData.guests]
      console.log('Using cached data for case', cacheKey, { permissions: permissions.value.length, guests: guestAccesses.value.length })
      return
    }
    
    console.log('Loading fresh data for case', cacheKey)
    await Promise.all([
      loadPermissions(),
      loadGuestAccesses()
    ])
    
    // Update cache with fresh data
    dataCache.value.set(cacheKey, {
      permissions: [...permissions.value],
      guests: [...guestAccesses.value],
      timestamp: Date.now()
    })
    
    if (forceRefresh) {
      toast.success(currentLang.value === 'vi' ? 'Đã làm mới dữ liệu' : 'Data refreshed')
    }
  } catch (error) {
    console.error('Error in refreshData:', error)
    toast.error(currentLang.value === 'vi' ? 'Lỗi khi tải dữ liệu' : 'Error loading data')
  }
}

const loadPermissions = async () => {
  try {
    const data = await sharingService.getCasePermissions(props.caseId)
    // Ensure we have valid permission objects with required properties
    permissions.value = (Array.isArray(data) ? data : []).filter(p => 
      p && typeof p === 'object' && typeof p.id === 'number'
    ).map(p => ({
      ...p,
      // Ensure all required properties exist with fallbacks
      share_type: p.share_type || 'individual',
      permission_type: p.permission_type || 'view',
      is_active: p.is_active !== undefined ? p.is_active : true,
      is_expired: p.is_expired !== undefined ? p.is_expired : false,
      user_name: p.user_name || '',
      user_email: p.user_email || '',
      department_name: p.department_name || '',
      class_group: p.class_group || '',
      share_description: p.share_description || ''
    }))
  } catch (error) {
    console.error('Error loading permissions:', error)
    permissions.value = []
    toast.error(currentLang.value === 'vi' ? 'Lỗi khi tải quyền truy cập' : 'Error loading permissions')
  }
}

const loadGuestAccesses = async () => {
  try {
    const data = await sharingService.getGuestAccesses(props.caseId)
    guestAccesses.value = Array.isArray(data) ? data : []
  } catch (error) {
    console.error('Error loading guest accesses:', error)
    guestAccesses.value = []
  }
}

const openShareModal = (type: PanelShareType) => {
  shareType.value = type
  showShareModal.value = true
}

const openGuestModal = () => {
  showGuestModal.value = true
}

const onGuestCreated = (guest: any) => {
  // Adapt the guest from modal to local GuestAccess interface
  const fullGuest: GuestAccess = {
    ...guest,
    expires_at_display: guest.expires_at_display || '',
    is_expired: false,
    access_count: 0,
    access_token: guest.access_token || ''
  }
  guestAccesses.value.unshift(fullGuest)
  // Update cache immediately
  const cacheKey = props.caseId
  const cachedData = dataCache.value.get(cacheKey)
  if (cachedData) {
    cachedData.guests = [...guestAccesses.value]
    cachedData.timestamp = Date.now()
  } else {
    dataCache.value.set(cacheKey, {
      permissions: [...permissions.value],
      guests: [...guestAccesses.value],
      timestamp: Date.now()
    })
  }
  console.log('Guest created and cache updated', { guestId: guest.id, cacheKey })
}

const copyGuestLink = (guest: GuestAccess) => {
  const link = `${window.location.origin}/guest-access/${guest.access_token}`
  navigator.clipboard.writeText(link)
  toast.success(currentLang.value === 'vi' ? 'Đã sao chép liên kết' : 'Link copied to clipboard')
}

const extendGuestAccess = async (guest: GuestAccess) => {
  try {
    await sharingService.extendGuestAccess(props.caseId, guest.id, 24)
    await loadGuestAccesses()
    // Update cache
    const cacheKey = props.caseId
    const cachedData = dataCache.value.get(cacheKey)
    if (cachedData) {
      cachedData.guests = [...guestAccesses.value]
      cachedData.timestamp = Date.now()
    }
    console.log('Guest access extended and cache updated', { guestId: guest.id, cacheKey })
    toast.success(currentLang.value === 'vi' ? 'Đã gia hạn 24 giờ' : 'Extended by 24 hours')
  } catch (error) {
    console.error('Error extending guest access:', error)
    toast.error(currentLang.value === 'vi' ? 'Lỗi khi gia hạn' : 'Error extending access')
  }
}

const deleteGuestAccess = async (guestId: number) => {
  if (!confirm(currentLang.value === 'vi' ? 'Bạn có chắc muốn xóa truy cập khách này?' : 'Are you sure you want to delete this guest access?')) {
    return
  }
  
  try {
    await sharingService.deleteGuestAccess(props.caseId, guestId)
    guestAccesses.value = guestAccesses.value.filter(g => g.id !== guestId)
    // Update cache
    const cacheKey = props.caseId
    const cachedData = dataCache.value.get(cacheKey)
    if (cachedData) {
      cachedData.guests = [...guestAccesses.value]
      cachedData.timestamp = Date.now()
    }
    console.log('Guest access deleted and cache updated', { guestId, cacheKey })
    toast.success(currentLang.value === 'vi' ? 'Đã xóa liên kết khách mời' : 'Guest access deleted')
  } catch (error) {
    console.error('Error deleting guest access:', error)
    toast.error(currentLang.value === 'vi' ? 'Lỗi khi xóa liên kết khách mời' : 'Error deleting guest access')
  }
}

const onPermissionCreated = (permission: any) => {
  // Adapt SharePermission to local Permission interface by adding required fields
  const fullPermission: Permission = {
    ...permission,
    is_active: true,
    is_expired: false
  }
  permissions.value.unshift(fullPermission)
  // Update cache immediately
  const cacheKey = props.caseId
  const cachedData = dataCache.value.get(cacheKey)
  if (cachedData) {
    cachedData.permissions = [...permissions.value]
    cachedData.timestamp = Date.now() // Refresh timestamp
  } else {
    // Create new cache entry if it doesn't exist
    dataCache.value.set(cacheKey, {
      permissions: [...permissions.value],
      guests: [...guestAccesses.value],
      timestamp: Date.now()
    })
  }
  console.log('Permission created and cache updated', { permissionId: permission.id, cacheKey })
}

const revokePermission = async (permissionId: number) => {
  if (!confirm(currentLang.value === 'vi' ? 'Bạn có chắc muốn xóa quyền này?' : 'Are you sure you want to delete this permission?')) {
    return
  }

  try {
    await sharingService.deletePermission(props.caseId, permissionId)
    permissions.value = permissions.value.filter(p => p.id !== permissionId)
    // Update cache
    const cacheKey = props.caseId
    const cachedData = dataCache.value.get(cacheKey)
    if (cachedData) {
      cachedData.permissions = [...permissions.value]
      cachedData.timestamp = Date.now()
    }
    console.log('Permission deleted and cache updated', { permissionId, cacheKey })
    toast.success(currentLang.value === 'vi' ? 'Quyền đã được xóa' : 'Permission deleted')
  } catch (error) {
    toast.error(currentLang.value === 'vi' ? 'Lỗi khi xóa quyền' : 'Error deleting permission')
  }
}

const bulkRevoke = async () => {
  if (selectedPermissions.value.length === 0) return

  if (!confirm(currentLang.value === 'vi' ? `Bạn có chắc muốn xóa ${selectedPermissions.value.length} quyền đã chọn?` : `Are you sure you want to delete ${selectedPermissions.value.length} selected permissions?`)) {
    return
  }

  try {
    for (const permissionId of selectedPermissions.value) {
      await sharingService.deletePermission(props.caseId, permissionId)
    }
    permissions.value = permissions.value.filter(p => !selectedPermissions.value.includes(p.id))
    selectedPermissions.value = []
    selectAll.value = false
    // Update cache
    const cacheKey = props.caseId
    const cachedData = dataCache.value.get(cacheKey)
    if (cachedData) {
      cachedData.permissions = [...permissions.value]
      cachedData.timestamp = Date.now()
    }
    console.log('Bulk permissions deleted and cache updated', { cacheKey })
    toast.success(currentLang.value === 'vi' ? 'Đã xóa các quyền đã chọn' : 'Deleted selected permissions')
  } catch (error) {
    toast.error(currentLang.value === 'vi' ? 'Lỗi khi xóa quyền' : 'Error deleting permissions')
    loadPermissions() // Reload to get current state
  }
}

const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedPermissions.value = permissions.value.map(p => p.id)
  } else {
    selectedPermissions.value = []
  }
}

const getPermissionDisplayName = (permission: Permission): string => {
  if (permission.share_type === 'individual') {
    return permission.user_name || permission.user_email || 'Unknown User'
  } else if (permission.share_type === 'department') {
    return permission.department_name || 'Unknown Department'
  } else if (permission.share_type === 'class_group') {
    return permission.class_group || 'Unknown Group'
  } else if (permission.share_type === 'public') {
    return currentLang.value === 'vi' ? 'Công khai' : 'Public Access'
  }
  return 'Unknown'
}

const getPermissionTypeText = (type: string): string => {
  const types = {
    'view': currentLang.value === 'vi' ? 'Xem' : 'View',
    'comment': currentLang.value === 'vi' ? 'Bình luận' : 'Comment',
    'analyze': currentLang.value === 'vi' ? 'Phân tích' : 'Analyze',
    'edit': currentLang.value === 'vi' ? 'Chỉnh sửa' : 'Edit'
  }
  return types[type as keyof typeof types] || type
}

const getPermissionVariant = (type: string) => {
  switch (type) {
    case 'view': return 'default'
    case 'comment': return 'secondary'
    case 'analyze': return 'outline'
    case 'edit': return 'destructive'
    default: return 'default'
  }
}

// Watch for select all changes
watch(() => selectedPermissions.value, (selected) => {
  selectAll.value = selected.length === permissions.value.length && permissions.value.length > 0
}, { deep: true })

// Load data on mount
onMounted(() => {
  console.log('Component mounted for case', props.caseId)
  refreshData(false) // Use cache if available
})

// Watch for case changes and reload
watch(() => props.caseId, (newCaseId) => {
  console.log('Case changed from', 'previous', 'to', newCaseId)
  refreshData(false) // Use cache for new case if available
})

// Optional: Clean up old cache entries periodically
onUnmounted(() => {
  // Don't clean up cache on unmount - we want persistence
  // But you could add cleanup of very old entries here if needed
  console.log('Component unmounted, keeping cache for case', props.caseId)
})
</script>

<style scoped>
.case-sharing-panel {
  max-width: 1200px;
  margin: 0 auto;
}

table {
  table-layout: fixed;
}

table th:first-child,
table td:first-child {
  width: 50px;
}

table th:last-child,
table td:last-child {
  width: 120px;
}
</style>