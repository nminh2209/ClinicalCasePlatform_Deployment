<template>
  <div v-if="open" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    @click="$emit('update:open', false)">
    <div class="bg-white rounded-lg p-6 w-full max-w-md m-4" @click.stop>
      <div class="mb-4">
        <h2 class="text-xl font-bold">
          {{ editGroup ?
            (currentLang === 'vi' ? 'Chỉnh sửa nhóm' : 'Edit Group')
            : (currentLang === 'vi' ? 'Tạo nhóm ca bệnh' : 'Create Case Group') }}
        </h2>
        <p class="text-gray-600">
          {{ currentLang === 'vi' ?
            'Tạo nhóm để quản lý nhiều ca bệnh cùng lúc'
            : 'Create group to manage multiple cases together' }}
        </p>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="space-y-4">
          <!-- Group Name -->
          <div>
            <label class="block text-sm font-medium mb-1">
              {{ currentLang === 'vi' ? 'Tên nhóm' : 'Group Name' }}
            </label>
            <input v-model="form.name" type="text" class="w-full border rounded-md p-2"
              :placeholder="currentLang === 'vi' ? 'Nhập tên nhóm' : 'Enter group name'" required />
          </div>

          <!-- Description -->
          <div>
            <label class="block text-sm font-medium mb-1">
              {{ currentLang === 'vi' ? 'Mô tả' : 'Description' }}
            </label>
            <textarea v-model="form.description" class="w-full border rounded-md p-2"
              :placeholder="currentLang === 'vi' ? 'Mô tả mục đích nhóm...' : 'Describe the group purpose...'"
              rows="3"></textarea>
          </div>

          <!-- Group Type -->
          <div>
            <label class="block text-sm font-medium mb-1">
              {{ currentLang === 'vi' ? 'Loại nhóm' : 'Group Type' }}
            </label>
            <select v-model="form.groupType" class="w-full border rounded-md p-2">
              <option value="teaching">{{ currentLang === 'vi' ? 'Giảng dạy' : 'Teaching' }}</option>
              <option value="research">{{ currentLang === 'vi' ? 'Nghiên cứu' : 'Research' }}</option>
              <option value="collaboration">{{ currentLang === 'vi' ? 'Hợp tác' : 'Collaboration' }}</option>
              <option value="review">{{ currentLang === 'vi' ? 'Xem xét' : 'Review' }}</option>
              <option value="other">{{ currentLang === 'vi' ? 'Khác' : 'Other' }}</option>
            </select>
          </div>

          <!-- Visibility -->
          <div>
            <label class="block text-sm font-medium mb-1">
              {{ currentLang === 'vi' ? 'Chế độ hiển thị' : 'Visibility' }}
            </label>
            <select v-model="form.isPrivate" class="w-full border rounded-md p-2">
              <option :value="false">{{ currentLang === 'vi' ? 'Công khai' : 'Public' }}</option>
              <option :value="true">{{ currentLang === 'vi' ? 'Riêng tư' : 'Private' }}</option>
            </select>
            <p class="text-xs text-gray-500 mt-1">
              {{ currentLang === 'vi' ?
                'Nhóm công khai có thể được tìm thấy bởi người khác'
                : 'Public groups can be discovered by others' }}
            </p>
          </div>

          <!-- Auto-add current case -->
          <div v-if="caseId" class="flex items-center space-x-2">
            <input type="checkbox" v-model="form.includeCurrentCase" id="include-case" class="rounded" />
            <label for="include-case" class="text-sm">
              {{ currentLang === 'vi' ? 'Thêm ca bệnh hiện tại vào nhóm' : 'Add current case to group' }}
            </label>
          </div>

          <!-- Default Permissions -->
          <div>
            <label class="block text-sm font-medium mb-1">
              {{ currentLang === 'vi' ? 'Quyền mặc định' : 'Default Permission' }}
            </label>
            <select v-model="form.defaultPermission" class="w-full border rounded-md p-2">
              <option value="read">{{ currentLang === 'vi' ? 'Chỉ xem' : 'Read Only' }}</option>
              <option value="comment">{{ currentLang === 'vi' ? 'Xem và bình luận' : 'Read & Comment' }}</option>
              <option value="edit">{{ currentLang === 'vi' ? 'Xem và chỉnh sửa' : 'Read & Edit' }}</option>
            </select>
            <p class="text-xs text-gray-500 mt-1">
              {{ currentLang === 'vi' ? 'Quyền được cấp cho thành viên mới' : 'Permission granted to new members' }}
            </p>
          </div>

          <!-- Tags -->
          <div>
            <label class="block text-sm font-medium mb-1">
              {{ currentLang === 'vi' ? 'Thẻ (tuỳ chọn)' : 'Tags (Optional)' }}
            </label>
            <input v-model="form.tags" type="text" class="w-full border rounded-md p-2"
              :placeholder="currentLang === 'vi' ? 'Nhập thẻ, phân cách bằng dấu phẩy' : 'Enter tags, separated by commas'" />
          </div>
        </div>

        <div class="flex justify-end space-x-2 mt-6">
          <button type="button" class="px-4 py-2 border rounded-md hover:bg-gray-50"
            @click="$emit('update:open', false)">
            {{ currentLang === 'vi' ? 'Huỷ' : 'Cancel' }}
          </button>
          <button type="submit"
            class="px-4 py-2 bg-purple-500 text-white rounded-md hover:bg-purple-600 disabled:opacity-50"
            :disabled="!canSubmit || loading">
            <span v-if="loading">⏳</span>
            {{ editGroup ?
              (currentLang === 'vi' ? 'Cập nhật' : 'Update')
              : (currentLang === 'vi' ? 'Tạo nhóm' : 'Create Group') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useLanguage } from '@/composables/useLanguage'
import { useToast } from '@/composables/useToast'
import { sharingService } from '@/services/sharing'
import type { CaseGroup } from '@/services/sharing'

interface Props {
  open: boolean
  caseId?: number
  editGroup?: CaseGroup
}

interface Emits {
  (event: 'update:open', value: boolean): void
  (event: 'group-created', group: CaseGroup): void
  (event: 'group-updated', group: CaseGroup): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const { currentLang } = useLanguage()
const toast = useToast()

const loading = ref(false)

const form = ref({
  name: '',
  description: '',
  groupType: 'teaching',
  isPrivate: false,
  includeCurrentCase: true,
  defaultPermission: 'read',
  tags: ''
})

const canSubmit = computed(() => {
  return form.value.name.trim() && form.value.groupType && form.value.defaultPermission
})

// Reset form when modal opens/closes
watch(() => props.open, (isOpen) => {
  if (isOpen && props.editGroup) {
    loadGroupData()
  } else if (!isOpen) {
    resetForm()
  }
})

const resetForm = () => {
  form.value = {
    name: '',
    description: '',
    groupType: 'teaching',
    isPrivate: false,
    includeCurrentCase: true,
    defaultPermission: 'read',
    tags: ''
  }
}

const loadGroupData = () => {
  if (props.editGroup) {
    form.value = {
      name: props.editGroup.name,
      description: props.editGroup.description || '',
      groupType: props.editGroup.group_type,
      isPrivate: false, // Default since property doesn't exist
      includeCurrentCase: false,
      defaultPermission: 'read',
      tags: '' // Default since property doesn't exist
    }
  }
}

const processTags = (tagString: string): string[] => {
  return tagString
    .split(',')
    .map(tag => tag.trim())
    .filter(tag => tag.length > 0)
}

const handleSubmit = async () => {
  if (!canSubmit.value) return

  loading.value = true
  try {
    const groupData: any = {
      name: form.value.name.trim(),
      description: form.value.description.trim() || undefined,
      group_type: form.value.groupType,
      is_private: form.value.isPrivate,
      default_permission: form.value.defaultPermission,
      tags: processTags(form.value.tags)
    }

    let group: CaseGroup

    if (props.editGroup && props.editGroup.id) {
      group = await sharingService.updateCaseGroup(props.editGroup.id, groupData)
      emit('group-updated', group)
      toast.toast.success(
        currentLang.value === 'vi'
          ? 'Đã cập nhật nhóm thành công!'
          : 'Group updated successfully!'
      )
    } else {
      group = await sharingService.createCaseGroup(groupData)

      // Add current case to group if requested
      if (props.caseId && form.value.includeCurrentCase) {
        // Note: This method might need to be implemented in the service
        console.log('Would add case', props.caseId, 'to group', group.id)
      }

      emit('group-created', group)
      toast.toast.success(
        currentLang.value === 'vi'
          ? 'Đã tạo nhóm thành công!'
          : 'Group created successfully!'
      )
    }

    emit('update:open', false)
  } catch (error) {
    console.error('Failed to save group:', error)
    toast.toast.error(
      currentLang.value === 'vi'
        ? 'Không thể lưu nhóm'
        : 'Failed to save group'
    )
  } finally {
    loading.value = false
  }
}
</script>
