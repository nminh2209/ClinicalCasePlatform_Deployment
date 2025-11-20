<template>
  <div class="case-sharing-panel p-6 bg-white rounded-lg shadow-lg">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-800">
        {{ currentLang === 'vi' ? 'Quản lý chia sẻ ca bệnh' : 'Case Sharing Management' }}
      </h2>
      <div class="flex space-x-2">
        <Button @click="refreshData" variant="outline" size="sm">
          🔄
          {{ currentLang === 'vi' ? 'Làm mới' : 'Refresh' }}
        </Button>
        <Button @click="showAuditLog = !showAuditLog" variant="outline" size="sm">
          📋
          {{ currentLang === 'vi' ? 'Nhật ký' : 'Audit Log' }}
        </Button>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="flex justify-between items-center mb-6">
      <div class="flex space-x-2">
        <Button @click="openShareModal('individual')" class="flex items-center space-x-2">
          <UserIcon class="w-4 h-4" />
          <span>{{ currentLang === 'vi' ? 'Chia sẻ ca bệnh' : 'Share Case' }}</span>
        </Button>
        
        <Button @click="openGuestModal" variant="outline" class="flex items-center space-x-2">
          <MailIcon class="w-4 h-4" />
          <span>{{ currentLang === 'vi' ? 'Truy cập khách' : 'Guest Access' }}</span>
        </Button>
      </div>
      
      <div class="text-sm text-gray-500">
        {{ permissions.length }} {{ currentLang === 'vi' ? 'quyền chia sẻ' : 'sharing permissions' }}
      </div>
    </div>

    <!-- Tabs for different views -->
    <Tabs v-model="activeTab" class="w-full">
      <TabsList class="grid w-full grid-cols-1">
        <TabsTrigger value="permissions">{{ currentLang === 'vi' ? 'Quyền chia sẻ' : 'Sharing Permissions' }}</TabsTrigger>
      </TabsList>

      <!-- Current Permissions Tab -->
      <TabsContent value="permissions" class="mt-6">
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
                {{ currentLang === 'vi' ? 'Chọn tất cả' : 'Select All' }} 
                ({{ selectedPermissions.length }}/{{ permissions.length }})
              </span>
            </div>
            <div class="space-x-2">
              <Button 
                @click="bulkRevokePermissions" 
                :disabled="selectedPermissions.length === 0"
                variant="destructive" 
                size="sm"
              >
                {{ currentLang === 'vi' ? 'Thu hồi đã chọn' : 'Revoke Selected' }}
              </Button>
            </div>
          </div>

          <!-- Permissions List -->
          <div class="border rounded-lg overflow-hidden">
            <table class="w-full">
              <thead class="bg-gray-50">
                <tr>
                  <th class="w-12 p-3"></th>
                  <th class="text-left p-3">{{ currentLang === 'vi' ? 'Người dùng/Nhóm' : 'User/Group' }}</th>
                  <th class="text-left p-3">{{ currentLang === 'vi' ? 'Loại quyền' : 'Permission Type' }}</th>
                  <th class="text-left p-3">{{ currentLang === 'vi' ? 'Hết hạn' : 'Expires' }}</th>
                  <th class="text-left p-3">{{ currentLang === 'vi' ? 'Trạng thái' : 'Status' }}</th>
                  <th class="text-right p-3">{{ currentLang === 'vi' ? 'Hành động' : 'Actions' }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="permission in permissions" :key="permission?.id || `perm-${Math.random()}`" class="border-t hover:bg-gray-50">
                  <td class="p-3">
                    <input 
                      type="checkbox" 
                      :value="permission?.id" 
                      v-model="selectedPermissions"
                      class="rounded"
                      :disabled="!permission?.id"
                    >
                  </td>
                  <td class="p-3">
                    <div class="flex items-center space-x-2">
                      <UserIcon v-if="permission?.share_type === 'individual'" class="w-4 h-4 text-blue-500" />
                      <BuildingIcon v-else-if="permission?.share_type === 'department'" class="w-4 h-4 text-green-500" />
                      <GlobeIcon v-else-if="permission?.share_type === 'public'" class="w-4 h-4 text-purple-500" />
                      <UsersIcon v-else-if="permission?.share_type === 'class_group'" class="w-4 h-4 text-orange-500" />
                      
                      <div>
                        <div class="font-medium">
                          {{ getPermissionDisplayName(permission) }}
                        </div>
                        <div class="text-sm text-gray-500">
                          {{ permission?.share_description || '' }}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="p-3">
                    <Badge :variant="getPermissionVariant(permission?.permission_type || 'view')">
                      {{ getPermissionTypeText(permission?.permission_type || 'view') }}
                    </Badge>
                  </td>
                  <td class="p-3">
                    <div class="text-sm">
                      {{ permission?.expires_at_display || (currentLang === 'vi' ? 'Không giới hạn' : 'No limit') }}
                    </div>
                    <div v-if="permission?.is_expired" class="text-xs text-red-500">
                      {{ currentLang === 'vi' ? 'Đã hết hạn' : 'Expired' }}
                    </div>
                  </td>
                  <td class="p-3">
                    <Badge :variant="(permission?.is_active && !permission?.is_expired) ? 'success' : 'secondary'">
                      {{ getStatusText(permission) }}
                    </Badge>
                  </td>
                  <td class="p-3 text-right">
                    <div class="flex justify-end space-x-2">
                      <Button @click="editPermission(permission)" size="sm" variant="outline" :disabled="!permission?.id">
                        ✏️
                      </Button>
                      <Button @click="deletePermission(permission?.id)" size="sm" variant="destructive" :disabled="!permission?.id">
                        🗑️
                      </Button>
                    </div>
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
      </TabsContent>

      <!-- Guest Access Tab -->
      <TabsContent value="guests" class="mt-6">
        <div class="space-y-4">
          <div class="flex justify-between items-center">
            <h3 class="text-lg font-semibold">
              {{ currentLang === 'vi' ? 'Truy cập khách mời' : 'Guest Access Links' }}
            </h3>
            <Button @click="openGuestModal">
              ➕
              {{ currentLang === 'vi' ? 'Tạo liên kết mới' : 'Create New Link' }}
            </Button>
          </div>

          <div class="grid gap-4">
            <div v-for="(guest, idx) in guestAccesses" :key="safeGuestKey(guest, idx)" class="border rounded-lg p-4">
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
      </TabsContent>

      <!-- My Shared Cases Tab -->
      <TabsContent value="my-shares" class="mt-6">
        <div class="space-y-4">
          <div class="flex justify-between items-center">
            <h3 class="text-lg font-semibold">
              {{ currentLang === 'vi' ? 'Các ca bệnh tôi đã chia sẻ' : 'Cases I Have Shared' }}
            </h3>
            <div class="text-sm text-gray-500">
              {{ mySharedCases.length }} {{ currentLang === 'vi' ? 'ca bệnh' : 'cases' }}
            </div>
          </div>

          <div v-if="loadingSharedCases" class="text-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
            <p class="mt-2 text-gray-500">{{ currentLang === 'vi' ? 'Đang tải...' : 'Loading...' }}</p>
          </div>

          <div v-else-if="mySharedCases.length === 0" class="text-center py-12 text-gray-500">
            📤
            <h3 class="text-lg font-medium mb-2">
              {{ currentLang === 'vi' ? 'Chưa chia sẻ ca bệnh nào' : 'No shared cases yet' }}
            </h3>
            <p class="mb-4">
              {{ currentLang === 'vi' ? 'Bắt đầu chia sẻ ca bệnh của bạn với đồng nghiệp' : 'Start sharing your cases with colleagues' }}
            </p>
          </div>

          <div v-else class="grid gap-4">
            <div v-for="sharedCase in mySharedCases" :key="sharedCase.case_id" class="border rounded-lg p-4">
              <div class="flex justify-between items-start">
                <div class="flex-1">
                  <h4 class="font-medium">{{ sharedCase.case_title }}</h4>
                  <p class="text-sm text-gray-600 mt-1">{{ sharedCase.case_description || 'No description' }}</p>
                  
                  <!-- Permission Summary -->
                  <div class="flex items-center space-x-4 mt-3 text-sm">
                    <span class="flex items-center">
                      👥
                      {{ sharedCase.permission_count }} {{ currentLang === 'vi' ? 'quyền truy cập' : 'permissions' }}
                    </span>
                    <span class="flex items-center">
                      🕒
                      {{ formatDate(sharedCase.last_shared) }}
                    </span>
                  </div>

                  <!-- Permission Details -->
                  <div class="mt-3 space-y-2">
                    <div v-for="perm in sharedCase.recent_permissions" :key="perm.id" class="flex items-center justify-between text-sm bg-gray-50 p-2 rounded">
                      <div class="flex items-center space-x-2">
                        <UserIcon v-if="perm.share_type === 'individual'" class="w-4 h-4 text-blue-500" />
                        <BuildingIcon v-else-if="perm.share_type === 'department'" class="w-4 h-4 text-green-500" />
                        <GlobeIcon v-else-if="perm.share_type === 'public'" class="w-4 h-4 text-purple-500" />
                        
                        <span class="font-medium">{{ getPermissionDisplayName(perm) }}</span>
                        <Badge size="sm" :variant="getPermissionVariant(perm.permission_type)">
                          {{ getPermissionTypeText(perm.permission_type) }}
                        </Badge>
                      </div>
                      
                      <Button 
                        @click="revokeSharedPermission(sharedCase.case_id, perm.id)" 
                        size="sm" 
                        variant="destructive"
                        :disabled="perm.revoking"
                      >
                        {{ perm.revoking ? '⏳' : '🗑️' }}
                      </Button>
                    </div>
                  </div>
                </div>

                <div class="ml-4">
                  <Button 
                    @click="viewCaseDetails(sharedCase.case_id)" 
                    size="sm" 
                    variant="outline"
                  >
                    {{ currentLang === 'vi' ? 'Xem chi tiết' : 'View Details' }}
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </TabsContent>

      <!-- Analytics Tab -->
      <TabsContent value="analytics" class="mt-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="bg-blue-50 p-4 rounded-lg">
            <h4 class="font-medium text-blue-800 mb-2">
              {{ currentLang === 'vi' ? 'Tổng quyền truy cập' : 'Total Permissions' }}
            </h4>
            <p class="text-2xl font-bold text-blue-600">{{ analytics.total_permissions || 0 }}</p>
          </div>
          
          <div class="bg-green-50 p-4 rounded-lg">
            <h4 class="font-medium text-green-800 mb-2">
              {{ currentLang === 'vi' ? 'Khách mời hoạt động' : 'Active Guests' }}
            </h4>
            <p class="text-2xl font-bold text-green-600">{{ analytics.active_guests || 0 }}</p>
          </div>
          
          <div class="bg-purple-50 p-4 rounded-lg">
            <h4 class="font-medium text-purple-800 mb-2">
              {{ currentLang === 'vi' ? 'Lượt truy cập trong tuần' : 'Weekly Access Count' }}
            </h4>
            <p class="text-2xl font-bold text-purple-600">{{ analytics.weekly_access || 0 }}</p>
          </div>
        </div>

        <!-- Audit Log -->
        <div v-if="showAuditLog" class="mt-6">
          <h4 class="font-medium mb-4">
            {{ currentLang === 'vi' ? 'Nhật ký hoạt động' : 'Activity Log' }}
          </h4>
          <div class="border rounded-lg max-h-64 overflow-y-auto">
            <div v-for="log in auditLogs" :key="log.id" class="border-b last:border-b-0 p-3">
              <div class="flex justify-between items-start">
                <div>
                  <p class="text-sm font-medium">{{ log.description }}</p>
                  <p class="text-xs text-gray-500">
                    {{ log.actor_user }} - {{ formatDate(log.created_at) }}
                  </p>
                </div>
                <Badge :variant="getActionVariant(log.action)">
                  {{ log.action }}
                </Badge>
              </div>
            </div>
          </div>
        </div>
      </TabsContent>
    </Tabs>

    <!-- Share Permission Modal -->
    <SharePermissionModal
      :open="showShareModal"
      @update:open="(value: boolean) => showShareModal = value"
      :case-id="caseId"
      :share-type="shareType"
      @permission-created="onPermissionCreated"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useLanguage } from '@/composables/useLanguage'
import { useToast } from '@/composables/useToast'
import sharingService from '@/services/sharing'
import Button from '@/components/ui/Button.vue'
import Badge from '@/components/ui/Badge.vue'
import Tabs from '@/components/ui/Tabs.vue'
import TabsList from '@/components/ui/TabsList.vue'
import TabsTrigger from '@/components/ui/TabsTrigger.vue'
import TabsContent from '@/components/ui/TabsContent.vue'
import SharePermissionModal from './SharePermissionModal.vue'

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
  guest_email: string
  guest_name?: string
  permission_type: 'view' | 'comment'
  expires_at_display?: string
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
const activeTab = ref('permissions')
const permissions = ref<Permission[]>([])
const selectedPermissions = ref<number[]>([])
const selectAll = ref(false)
const showAuditLog = ref(false)
const guestAccesses = ref<GuestAccess[]>([])
const mySharedCases = ref<any[]>([])
const loadingSharedCases = ref(false)
const analytics = ref({
  total_permissions: 0,
  active_guests: 0,
  weekly_access: 0
})
const auditLogs = ref<any[]>([])

// Modal states
const showShareModal = ref(false)
const showGuestModal = ref(false)
const editingPermission = ref<Permission | null>(null)
const editingGuest = ref<GuestAccess | null>(null)
type PanelShareType = 'individual' | 'department' | 'public'
const shareType = ref<PanelShareType>('individual')

// Methods
const refreshData = async () => {
  try {
    await loadPermissions()
    toast.success(currentLang.value === 'vi' ? 'Đã làm mới dữ liệu' : 'Data refreshed')
  } catch (error) {
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
    // Defensive: ensure array elements are non-null objects with id
    guestAccesses.value = (Array.isArray(data) ? data : []).filter(g => !!g)
  } catch (error) {
    console.error('Error loading guest accesses:', error)
  }
}

// Key helper to avoid runtime error if backend returns null elements
const safeGuestKey = (guest: GuestAccess | null | undefined, idx: number) => {
  if (guest && typeof guest.id === 'number') return guest.id
  return `guest-${idx}`
}

const loadMySharedCases = async () => {
  loadingSharedCases.value = true
  try {
    const data = await sharingService.getMySharedCases()
    mySharedCases.value = (Array.isArray(data) ? data : []).map(item => ({
      case_id: item.case_id || item.id,
      case_title: item.case_title || item.title || 'Untitled Case',
      case_description: item.case_description || item.description,
      permission_count: item.permission_count || 0,
      last_shared: item.last_shared || item.created_at,
      recent_permissions: (item.recent_permissions || []).map((p: any) => ({
        ...p,
        revoking: false
      }))
    }))
  } catch (error) {
    console.error('Error loading shared cases:', error)
    mySharedCases.value = []
    toast.error(currentLang.value === 'vi' ? 'Lỗi khi tải ca bệnh đã chia sẻ' : 'Error loading shared cases')
  } finally {
    loadingSharedCases.value = false
  }
}

const loadAnalytics = async () => {
  analytics.value = {
    total_permissions: permissions.value.length,
    active_guests: guestAccesses.value.filter((g: any) => !g.is_expired).length,
    weekly_access: permissions.value.reduce((sum, p) => sum + (p.access_count || 0), 0)
  }
}

const loadAuditLog = async () => {
  try {
    const data = await sharingService.getPermissionAuditLog(props.caseId)
    auditLogs.value = data
  } catch (error) {
    console.error('Error loading audit log:', error)
  }
}

// UI Helper methods
const getPermissionDisplayName = (permission: Permission | null | undefined) => {
  if (!permission) return 'Unknown'
  
  switch (permission.share_type) {
    case 'individual':
      return permission.user_name || permission.user_email || 'Unknown User'
    case 'department':
      return permission.department_name || 'Unknown Department'
    case 'class_group':
      return permission.class_group || 'Unknown Group'
    case 'public':
      return currentLang.value === 'vi' ? 'Công khai' : 'Public'
    default:
      return 'Unknown'
  }
}

const getPermissionVariant = (type: string) => {
  switch (type) {
    case 'view': return 'secondary'
    case 'comment': return 'default'
    case 'analyze': return 'outline'
    case 'edit': return 'destructive'
    default: return 'secondary'
  }
}

const getPermissionTypeText = (type: string) => {
  const texts: Record<string, string> = {
    view: currentLang.value === 'vi' ? 'Xem' : 'View',
    comment: currentLang.value === 'vi' ? 'Bình luận' : 'Comment',
    analyze: currentLang.value === 'vi' ? 'Phân tích' : 'Analyze',
    edit: currentLang.value === 'vi' ? 'Chỉnh sửa' : 'Edit'
  }
  return texts[type] || type
}

const getStatusText = (permission: Permission | null | undefined) => {
  if (!permission) return 'Unknown'
  
  if (permission.is_expired) {
    return currentLang.value === 'vi' ? 'Hết hạn' : 'Expired'
  }
  if (permission.is_active) {
    return currentLang.value === 'vi' ? 'Hoạt động' : 'Active'
  }
  return currentLang.value === 'vi' ? 'Không hoạt động' : 'Inactive'
}

const getActionVariant = (action: string) => {
  switch (action.toLowerCase()) {
    case 'granted': return 'success'
    case 'revoked': return 'destructive'
    case 'modified': return 'default'
    default: return 'secondary'
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}

// Modal management
const openShareModal = (type: string) => {
  if (['individual','department','public'].includes(type)) {
    shareType.value = type as PanelShareType
  } else {
    console.warn('Invalid share type:', type)
    shareType.value = 'individual'
  }
  editingPermission.value = null
  showShareModal.value = true
}

const closeShareModal = () => {
  showShareModal.value = false
  editingPermission.value = null
}

const openGuestModal = () => {
  editingGuest.value = null
  showGuestModal.value = true
}

const closeGuestModal = () => {
  showGuestModal.value = false
  editingGuest.value = null
}

// Success handlers
const onPermissionCreated = () => {
  loadPermissions()
  toast.success(currentLang.value === 'vi' ? 'Quyền đã được tạo' : 'Permission created successfully')
}

const onGuestCreated = () => {
  loadGuestAccesses()
  toast.success(currentLang.value === 'vi' ? 'Truy cập khách đã được tạo' : 'Guest access created successfully')
}

// Selection management
const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedPermissions.value = permissions.value.map(p => p.id)
  } else {
    selectedPermissions.value = []
  }
}

// Bulk operations
const bulkRevokePermissions = async () => {
  if (selectedPermissions.value.length === 0) return
  
  try {
    await sharingService.bulkRevokePermissions(props.caseId, selectedPermissions.value)
    selectedPermissions.value = []
    selectAll.value = false
    loadPermissions()
    toast.success(currentLang.value === 'vi' ? 'Đã thu hồi quyền đã chọn' : 'Selected permissions revoked')
  } catch (error) {
    toast.error(currentLang.value === 'vi' ? 'Lỗi khi thu hồi quyền' : 'Error revoking permissions')
  }
}

// Individual operations
const editPermission = (permission: Permission) => {
  editingPermission.value = permission
  // Map any unsupported types (e.g., class_group) to a safe fallback for modal
  shareType.value = (['individual','department','public'].includes(permission.share_type)
    ? permission.share_type
    : 'individual') as PanelShareType
  showShareModal.value = true
}

const deletePermission = async (permissionId: number) => {
  if (!confirm(currentLang.value === 'vi' ? 'Bạn có chắc muốn xóa quyền này?' : 'Are you sure you want to delete this permission?')) {
    return
  }
  
  try {
    await sharingService.deletePermission(props.caseId, permissionId)
    loadPermissions()
    toast.success(currentLang.value === 'vi' ? 'Quyền đã được xóa' : 'Permission deleted')
  } catch (error) {
    toast.error(currentLang.value === 'vi' ? 'Lỗi khi xóa quyền' : 'Error deleting permission')
  }
}

const copyGuestLink = (guest: GuestAccess) => {
  const url = `${window.location.origin}/guest-access/${guest.access_token}`
  navigator.clipboard.writeText(url)
  toast.success(currentLang.value === 'vi' ? 'Liên kết đã được sao chép' : 'Link copied to clipboard')
}

const extendGuestAccess = async (guest: GuestAccess) => {
  try {
    await sharingService.extendGuestAccess(props.caseId, guest.id, 72) // Extend by 72 hours
    loadGuestAccesses()
    toast.success(currentLang.value === 'vi' ? 'Đã gia hạn truy cập' : 'Guest access extended')
  } catch (error) {
    toast.error(currentLang.value === 'vi' ? 'Lỗi khi gia hạn' : 'Error extending access')
  }
}

const deleteGuestAccess = async (guestId: number) => {
  if (!confirm(currentLang.value === 'vi' ? 'Bạn có chắc muốn xóa truy cập khách này?' : 'Are you sure you want to delete this guest access?')) {
    return
  }
  
  try {
    await sharingService.deleteGuestAccess(props.caseId, guestId)
    loadGuestAccesses()
    toast.success(currentLang.value === 'vi' ? 'Truy cập khách đã được xóa' : 'Guest access deleted')
  } catch (error) {
    toast.error(currentLang.value === 'vi' ? 'Lỗi khi xóa truy cập khách' : 'Error deleting guest access')
  }
}

const revokeSharedPermission = async (caseId: number, permissionId: number) => {
  if (!confirm(currentLang.value === 'vi' ? 'Bạn có chắc muốn thu hồi quyền này?' : 'Are you sure you want to revoke this permission?')) {
    return
  }

  // Find and mark permission as revoking
  const sharedCase = mySharedCases.value.find(c => c.case_id === caseId)
  if (sharedCase) {
    const permission = sharedCase.recent_permissions.find((p: any) => p.id === permissionId)
    if (permission) {
      permission.revoking = true
    }
  }

  try {
    await sharingService.deletePermission(caseId, permissionId)
    
    // Remove the permission from the list
    if (sharedCase) {
      sharedCase.recent_permissions = sharedCase.recent_permissions.filter((p: any) => p.id !== permissionId)
      sharedCase.permission_count = Math.max(0, sharedCase.permission_count - 1)
      
      // Remove case if no permissions left
      if (sharedCase.permission_count === 0) {
        mySharedCases.value = mySharedCases.value.filter(c => c.case_id !== caseId)
      }
    }

    toast.success(currentLang.value === 'vi' ? 'Đã thu hồi quyền' : 'Permission revoked')
  } catch (error) {
    // Revert revoking state on error
    if (sharedCase) {
      const permission = sharedCase.recent_permissions.find((p: any) => p.id === permissionId)
      if (permission) {
        permission.revoking = false
      }
    }
    toast.error(currentLang.value === 'vi' ? 'Lỗi khi thu hồi quyền' : 'Error revoking permission')
  }
}

const viewCaseDetails = (caseId: number) => {
  // Navigate to case details - implement based on your routing
  window.open(`/cases/${caseId}`, '_blank')
}

// Lifecycle
onMounted(() => {
  refreshData()
})

// Watch for tab changes to load appropriate data
watch(() => activeTab.value, (newTab) => {
  if (newTab === 'my-shares' && mySharedCases.value.length === 0) {
    loadMySharedCases()
  }
  if (newTab === 'analytics' && showAuditLog.value) {
    loadAuditLog()
  }
})

watch(() => showAuditLog.value, (show) => {
  if (show) {
    loadAuditLog()
  }
})

// Watch selected permissions for select all state
watch(() => selectedPermissions.value, (selected) => {
  selectAll.value = selected.length === permissions.value.length && permissions.value.length > 0
}, { deep: true })
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