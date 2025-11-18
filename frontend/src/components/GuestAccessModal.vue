<template>
  <div v-if="open" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="$emit('update:open', false)">
    <div class="bg-white rounded-lg p-6 w-full max-w-md m-4" @click.stop>
      <div class="mb-4">
        <h2 class="text-xl font-bold">
          {{ currentLang === 'vi' ? 'Tạo liên kết khách mời' : 'Create Guest Access Link' }}
        </h2>
        <p class="text-gray-600">
          {{ currentLang === 'vi' ? 'Tạo liên kết truy cập cho người không có tài khoản' : 'Create access link for users without accounts' }}
        </p>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="space-y-4">
          <!-- Guest Name -->
          <div>
            <label class="block text-sm font-medium mb-1">
              {{ currentLang === 'vi' ? 'Tên khách mời' : 'Guest Name' }}
            </label>
            <input 
              v-model="form.guestName" 
              type="text"
              class="w-full border rounded-md p-2"
              :placeholder="currentLang === 'vi' ? 'Nhập tên khách mời' : 'Enter guest name'"
              required
            />
          </div>

          <!-- Guest Email -->
          <div>
            <label class="block text-sm font-medium mb-1">
              {{ currentLang === 'vi' ? 'Email khách mời' : 'Guest Email' }}
            </label>
            <input 
              v-model="form.guestEmail" 
              type="email"
              class="w-full border rounded-md p-2"
              :placeholder="currentLang === 'vi' ? 'Nhập email khách mời' : 'Enter guest email'"
              required
            />
          </div>

          <!-- Access Duration -->
          <div>
            <label class="block text-sm font-medium mb-1">
              {{ currentLang === 'vi' ? 'Thời gian truy cập' : 'Access Duration' }}
            </label>
            <select v-model="form.duration" class="w-full border rounded-md p-2">
              <option value="1">{{ currentLang === 'vi' ? '1 giờ' : '1 Hour' }}</option>
              <option value="6">{{ currentLang === 'vi' ? '6 giờ' : '6 Hours' }}</option>
              <option value="24">{{ currentLang === 'vi' ? '1 ngày' : '1 Day' }}</option>
              <option value="168">{{ currentLang === 'vi' ? '1 tuần' : '1 Week' }}</option>
              <option value="720">{{ currentLang === 'vi' ? '1 tháng' : '1 Month' }}</option>
              <option value="custom">{{ currentLang === 'vi' ? 'Tùy chỉnh' : 'Custom' }}</option>
            </select>
          </div>

          <!-- Custom Expiry Date -->
          <div v-if="form.duration === 'custom'">
            <label class="block text-sm font-medium mb-1">
              {{ currentLang === 'vi' ? 'Ngày hết hạn' : 'Expiry Date' }}
            </label>
            <input 
              type="datetime-local" 
              v-model="form.customExpiry"
              class="w-full border rounded-md p-2"
              :min="new Date().toISOString().slice(0, 16)"
            />
          </div>

          <!-- Access Limits -->
          <div>
            <label class="block text-sm font-medium mb-1">
              {{ currentLang === 'vi' ? 'Giới hạn truy cập (tuỳ chọn)' : 'Access Limit (Optional)' }}
            </label>
            <input 
              v-model.number="form.accessLimit" 
              type="number"
              class="w-full border rounded-md p-2"
              :placeholder="currentLang === 'vi' ? 'Số lần truy cập tối đa' : 'Maximum access count'"
              min="1"
            />
            <p class="text-xs text-gray-500 mt-1">
              {{ currentLang === 'vi' ? 'Để trống nếu không giới hạn' : 'Leave empty for unlimited access' }}
            </p>
          </div>

          <!-- Send Email Option -->
          <div class="flex items-center space-x-2">
            <input 
              type="checkbox" 
              v-model="form.sendEmail" 
              id="send-email"
              class="rounded"
            />
            <label for="send-email" class="text-sm">
              {{ currentLang === 'vi' ? 'Gửi email thông báo cho khách mời' : 'Send notification email to guest' }}
            </label>
          </div>

          <!-- Custom Message -->
          <div v-if="form.sendEmail">
            <label class="block text-sm font-medium mb-1">
              {{ currentLang === 'vi' ? 'Tin nhắn (tuỳ chọn)' : 'Message (Optional)' }}
            </label>
            <textarea 
              v-model="form.message"
              class="w-full border rounded-md p-2"
              :placeholder="currentLang === 'vi' ? 'Thêm tin nhắn trong email...' : 'Add message to email...'"
              rows="3"
            ></textarea>
          </div>
        </div>

        <div class="flex justify-end space-x-2 mt-6">
          <button 
            type="button" 
            class="px-4 py-2 border rounded-md hover:bg-gray-50"
            @click="$emit('update:open', false)"
          >
            {{ currentLang === 'vi' ? 'Huỷ' : 'Cancel' }}
          </button>
          <button 
            type="submit" 
            class="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 disabled:opacity-50"
            :disabled="!canSubmit || loading"
          >
            <span v-if="loading">⏳</span>
            {{ currentLang === 'vi' ? 'Tạo liên kết' : 'Create Link' }}
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
import type { GuestAccess } from '@/services/sharing'

interface Props {
  open: boolean
  caseId: number
}

interface Emits {
  (event: 'update:open', value: boolean): void
  (event: 'guest-created', guest: GuestAccess): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const { currentLang } = useLanguage()
const toast = useToast()

const loading = ref(false)

const form = ref({
  guestName: '',
  guestEmail: '',
  duration: '24', // hours
  customExpiry: '',
  accessLimit: null as number | null,
  sendEmail: true,
  message: ''
})

const canSubmit = computed(() => {
  return form.value.guestName && 
         form.value.guestEmail && 
         (form.value.duration !== 'custom' || form.value.customExpiry)
})

// Reset form when modal opens/closes
watch(() => props.open, (isOpen) => {
  if (!isOpen) {
    resetForm()
  }
})

const resetForm = () => {
  form.value = {
    guestName: '',
    guestEmail: '',
    duration: '24',
    customExpiry: '',
    accessLimit: null,
    sendEmail: true,
    message: ''
  }
}

const calculateExpiryDate = (): string => {
  if (form.value.duration === 'custom') {
    return form.value.customExpiry
  }
  
  const hours = parseInt(form.value.duration)
  const expiryDate = new Date()
  expiryDate.setHours(expiryDate.getHours() + hours)
  
  return expiryDate.toISOString()
}

const handleSubmit = async () => {
  if (!canSubmit.value) return

  loading.value = true
  try {
    const guestData: any = {
      case_id: props.caseId,
      guest_name: form.value.guestName,
      guest_email: form.value.guestEmail,
      expires_at: calculateExpiryDate(),
      access_limit: form.value.accessLimit || undefined,
      send_email: form.value.sendEmail,
      message: form.value.message || undefined
    }

    const guest = await sharingService.createGuestAccess(props.caseId, guestData)
    
    toast.toast.success(
      currentLang.value === 'vi' 
        ? 'Đã tạo liên kết khách mời thành công!' 
        : 'Guest access link created successfully!'
    )
    
    emit('guest-created', guest)
    emit('update:open', false)
  } catch (error) {
    console.error('Failed to create guest access:', error)
    toast.toast.error(
      currentLang.value === 'vi' 
        ? 'Không thể tạo liên kết khách mời' 
        : 'Failed to create guest access link'
    )
  } finally {
    loading.value = false
  }
}
</script>