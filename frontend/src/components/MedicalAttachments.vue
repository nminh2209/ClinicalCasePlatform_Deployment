<template>
  <div class="space-y-4">
    <!-- Upload Area -->
    <div
      class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors"
      :class="{ 'border-blue-400 bg-blue-50': isDragOver }" @dragover.prevent="isDragOver = true"
      @dragleave="isDragOver = false" @drop.prevent="handleDrop">
      <Upload class="h-8 w-8 text-gray-400 mx-auto mb-2" />
      <p class="text-sm text-gray-600 mb-2">
        Kéo thả tệp vào đây hoặc
        <button class="text-blue-600 hover:text-blue-700 underline" @click="fileInput?.click()">
          chọn tệp
        </button>
      </p>
      <p class="text-xs text-gray-500">
        Hỗ trợ: PDF, JPG, PNG, DICOM (tối đa 10MB)
      </p>
      <input ref="fileInput" type="file" multiple accept=".pdf,.jpg,.jpeg,.png,.dcm" class="hidden"
        @change="handleFileSelect" />
    </div>

    <!-- OCR Processing Status -->
    <div v-if="ocrProcessing" class="bg-blue-50 p-4 rounded-lg flex items-center gap-3">
      <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
      <div class="flex-1">
        <p class="text-sm font-medium text-blue-800">Đang xử lý OCR...</p>
        <p class="text-xs text-blue-600">Đang trích xuất văn bản từ tài liệu của bạn</p>
      </div>
    </div>

    <!-- Attachments List -->
    <div v-if="loading" class="text-center py-8">
      <p class="text-gray-500">Đang tải tệp đính kèm...</p>
    </div>

    <div v-else-if="attachments.length > 0" class="space-y-3">
      <h4 class="font-medium text-gray-800">Tệp đính kèm ({{ attachments.length }})</h4>
      <div class="space-y-2">
        <div v-for="attachment in attachments" :key="attachment.id"
          class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div class="flex items-center gap-3">
            <FileText class="h-5 w-5 text-blue-600" />
            <div>
              <p class="font-medium text-gray-800">{{ attachment.name }}</p>
              <p class="text-xs text-gray-500">
                {{ attachment.type }} • {{ formatFileSize(attachment.size) }}
                <span v-if="attachment.uploadedAt"> • {{ formatDate(attachment.uploadedAt) }}</span>
                <span v-if="attachment.is_confidential" class="text-red-600"> • 🔒 Bảo mật</span>
              </p>
              <p v-if="attachment.description" class="text-xs text-gray-600 mt-1">{{ attachment.description }}</p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <Button variant="ghost" size="sm" @click="runOCR(attachment)" title="Trích xuất văn bản (OCR)">
              <span class="text-xs font-bold border border-gray-400 rounded px-1">OCR</span>
            </Button>
            <Button variant="ghost" size="sm" @click="downloadFile(attachment)">
              <Download class="h-4 w-4" />
            </Button>
            <Button v-if="canEdit" variant="ghost" size="sm" @click="removeFile(attachment.id)"
              class="text-red-600 hover:text-red-700">
              <X class="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- OCR Result Modal -->
    <div v-if="ocrResult" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="ocrResult = null">
      <div class="bg-white rounded-lg max-w-2xl w-full mx-4 max-h-[80vh] flex flex-col" @click.stop>
        <div class="p-4 border-b flex justify-between items-center">
          <h3 class="font-semibold text-lg">Kết quả OCR</h3>
          <button @click="ocrResult = null" class="text-gray-500 hover:text-gray-700">&times;</button>
        </div>
        <div class="p-4 overflow-y-auto flex-1">
          <div class="bg-gray-50 p-3 rounded border text-sm whitespace-pre-wrap font-mono">{{ ocrResult.text }}</div>
          
          <div v-if="ocrResult.pages && ocrResult.pages.length > 0" class="mt-4">
            <h4 class="font-medium mb-2">Chi tiết theo trang</h4>
            <div v-for="page in ocrResult.pages" :key="page.page" class="mb-2 text-xs text-gray-600">
              <p>Trang {{ page.page }} (Độ tin cậy: {{ (page.confidence * 100).toFixed(1) }}%)</p>
              <p v-if="page.warnings.length" class="text-orange-600">⚠️ {{ page.warnings.join(', ') }}</p>
            </div>
          </div>
        </div>
        <div class="p-4 border-t flex justify-end gap-2">
          <Button variant="outline" @click="ocrResult = null">Đóng</Button>
          <Button @click="copyOCRText">Sao chép văn bản</Button>
        </div>
      </div>
    </div>

    <!-- No attachments message -->
    <div v-else class="text-center py-8">
      <FileText class="h-12 w-12 text-gray-300 mx-auto mb-3" />
      <p class="text-gray-500">Chưa có tệp đính kèm nào</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Button from '@/components/ui/Button.vue'
import { Upload, FileText, Download, X } from '@/components/icons'
import api from '@/services/api'
import { ocrService, type OCRResult } from '@/services/ocr'

const props = defineProps({
  caseId: String,
  canEdit: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['attachmentsChanged'])
const fileInput = ref()
const isDragOver = ref(false)
const attachments = ref<Array<{
  id: number,
  name: string,
  size: number,
  type: string,
  url?: string,
  uploadedAt?: string,
  description?: string,
  is_confidential: boolean,
  file?: File // Keep reference if just uploaded
}>>([])
const loading = ref(false)
const ocrProcessing = ref(false)
const ocrResult = ref<OCRResult | null>(null)

// Fetch attachments from backend
onMounted(async () => {
  if (!props.caseId) return

  loading.value = true
  try {
    const response = await api.get(`/api/cases/${props.caseId}/attachments/`)
    attachments.value = response.data.map((att: any) => ({
      id: att.id,
      name: att.title || 'Untitled',
      type: att.attachment_type_display || att.attachment_type,
      size: att.file_size || 0,
      uploadedAt: att.uploaded_at,
      url: att.file,
      description: att.description,
      isConfidential: att.is_confidential
    }))
  } catch (error) {
    console.error('Failed to load attachments:', error)
  } finally {
    loading.value = false
  }
})

const handleDrop = (event: DragEvent) => {
  isDragOver.value = false
  const files = event.dataTransfer?.files
  if (files) {
    handleFiles(Array.from(files))
  }
}

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  const files = target.files
  if (files) {
    handleFiles(Array.from(files))
  }
}

const handleFiles = async (files: File[]) => {
  if (!props.canEdit) {
    alert('Bạn không có quyền tải lên tệp')
    return
  }

  for (const file of files) {
    // Validate file size (10MB limit for OCR, 50MB general)
    if (file.size > 50 * 1024 * 1024) {
      alert(`Tệp ${file.name} quá lớn. Kích thước tối đa là 50MB.`)
      continue
    }

    // Validate file type
    const allowedTypes = ['.pdf', '.jpg', '.jpeg', '.png', '.dcm', '.doc', '.docx', '.zip', '.rar']
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase()
    if (!allowedTypes.includes(fileExtension)) {
      alert(`Định dạng tệp ${file.name} không được hỗ trợ.`)
      continue
    }

    // Upload to server
    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('title', file.name)
      formData.append('attachment_type', 'other') // Can be enhanced to detect type

      const response = await api.post(`/api/cases/${props.caseId}/attachments/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      // Add uploaded file to list
      const newAttachment = {
        id: response.data.id,
        name: response.data.title,
        type: response.data.attachment_type_display,
        size: response.data.file_size,
        uploadedAt: response.data.uploaded_at,
        url: response.data.file,
        description: response.data.description,
        is_confidential: response.data.is_confidential,
        file: file // Store file object for immediate OCR if needed
      }
      attachments.value.push(newAttachment)

      // Ask user if they want to run OCR immediately
      if (['.pdf', '.jpg', '.jpeg', '.png'].includes(fileExtension) && confirm(`Bạn có muốn trích xuất văn bản (OCR) từ ${file.name} không?`)) {
        runOCR(newAttachment)
      }

      alert(`Đã tải lên tệp ${file.name}`)
    } catch (error) {
      console.error('Upload failed:', error)
      alert(`Lỗi khi tải lên ${file.name}. Vui lòng thử lại.`)
    }
  }

  emit('attachmentsChanged', attachments.value)
}

const runOCR = async (attachment: any) => {
  if (ocrProcessing.value) return
  
  let fileToProcess = attachment.file
  
  // If we don't have the File object (loaded from server), we need to fetch it
  if (!fileToProcess && attachment.url) {
    try {
      ocrProcessing.value = true
      const response = await fetch(attachment.url)
      const blob = await response.blob()
      fileToProcess = new File([blob], attachment.name, { type: blob.type })
    } catch (e) {
      console.error("Failed to fetch file for OCR", e)
      alert("Không thể tải tệp để xử lý OCR")
      ocrProcessing.value = false
      return
    }
  }

  if (!fileToProcess) {
    alert("Không tìm thấy dữ liệu tệp")
    return
  }

  try {
    ocrProcessing.value = true
    const result = await ocrService.extractText(fileToProcess)
    ocrResult.value = result
  } catch (error: any) {
    console.error("OCR Failed:", error)
    alert(`Lỗi OCR: ${error.message || 'Không thể xử lý tệp'}`)
  } finally {
    ocrProcessing.value = false
  }
}

const copyOCRText = () => {
  if (ocrResult.value?.text) {
    navigator.clipboard.writeText(ocrResult.value.text)
    alert("Đã sao chép văn bản vào clipboard")
  }
}

const removeFile = async (id: number) => {
  const attachment = attachments.value.find(att => att.id === id)
  if (!attachment) return

  if (!confirm(`Xác nhận xóa tệp "${attachment.name}"?`)) return

  try {
    await api.delete(`/api/cases/attachments/${id}/`)

    const index = attachments.value.findIndex(att => att.id === id)
    if (index > -1) {
      attachments.value.splice(index, 1)
    }

    alert(`Đã xóa tệp ${attachment.name}`)
    emit('attachmentsChanged', attachments.value)
  } catch (error) {
    console.error('Delete failed:', error)
    alert('Lỗi khi xóa tệp. Vui lòng thử lại.')
  }
}

const downloadFile = (attachment: any) => {
  if (attachment.url) {
    window.open(attachment.url, '_blank')
  } else {
    alert('Không tìm thấy đường dẫn tệp')
  }
}

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('vi-VN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>
