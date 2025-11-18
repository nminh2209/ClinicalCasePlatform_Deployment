<template>
  <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
    @click.self="$emit('close')">
    <div class="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
      <div class="p-6 space-y-6">
        <!-- Header -->
        <div class="flex items-center justify-between border-b pb-4">
          <h2 class="text-2xl font-bold text-gray-800">Xem trước bệnh án</h2>
          <Button variant="ghost" size="icon" @click="$emit('close')">
            <X class="h-5 w-5" />
          </Button>
        </div>

        <!-- Case Preview Content -->
        <div class="space-y-6">
          <!-- Title and Specialty -->
          <div class="text-center border-b pb-4">
            <h1 class="text-3xl font-bold text-gray-800 mb-2">{{ caseData.title }}</h1>
            <Badge variant="secondary" class="text-lg px-4 py-2">{{ caseData.specialty }}</Badge>
          </div>

          <!-- Patient Information -->
          <div class="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
            <h3 class="text-lg font-semibold text-gray-800 mb-3">👤 Thông tin bệnh nhân</h3>
            <div class="grid grid-cols-2 gap-3 text-sm">
              <div><span class="font-medium">Tên:</span> {{ caseData.patientName || 'Chưa nhập' }}</div>
              <div><span class="font-medium">Tuổi:</span> {{ caseData.patientAge || 'Chưa nhập' }}</div>
              <div><span class="font-medium">Giới tính:</span> {{ caseData.patientGender || 'Chưa nhập' }}</div>
              <div><span class="font-medium">Số hồ sơ:</span> {{ caseData.medicalRecordNumber || 'Chưa nhập' }}</div>
            </div>
          </div>

          <!-- Clinical History -->
          <div>
            <h3 class="text-xl font-bold text-gray-800 mb-3 border-b pb-2">📋 Tiền sử lâm sàng</h3>
            
            <div class="mb-4">
              <h4 class="text-md font-semibold text-gray-800 mb-2">Lý do khám chính</h4>
              <p class="text-gray-700 bg-gray-50 p-3 rounded-lg">{{ caseData.chiefComplaint || 'Chưa nhập' }}</p>
            </div>

            <div class="mb-4">
              <h4 class="text-md font-semibold text-gray-800 mb-2">Bệnh sử hiện tại</h4>
              <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line">{{ caseData.historyOfPresentIllness || 'Chưa nhập' }}</div>
            </div>

            <div class="mb-4">
              <h4 class="text-md font-semibold text-gray-800 mb-2">Tiền sử bệnh tật</h4>
              <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line">{{ caseData.pastMedicalHistory || 'Chưa nhập' }}</div>
            </div>

            <div class="mb-4">
              <h4 class="text-md font-semibold text-gray-800 mb-2">Thuốc đang sử dụng</h4>
              <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line">{{ caseData.medications || 'Chưa nhập' }}</div>
            </div>
          </div>

          <!-- Physical Examination -->
          <div>
            <h3 class="text-xl font-bold text-gray-800 mb-3 border-b pb-2">🩺 Khám lâm sàng</h3>
            
            <div class="mb-4">
              <h4 class="text-md font-semibold text-gray-800 mb-2">Tình trạng chung</h4>
              <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line">{{ caseData.generalAppearance || 'Chưa nhập' }}</div>
            </div>

            <div class="mb-4">
              <h4 class="text-md font-semibold text-gray-800 mb-2">Dấu hiệu sinh tồn</h4>
              <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line">{{ caseData.vitalSigns || 'Chưa nhập' }}</div>
            </div>

            <div class="mb-4">
              <h4 class="text-md font-semibold text-gray-800 mb-2">Tim mạch</h4>
              <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line">{{ caseData.cardiovascular || 'Chưa nhập' }}</div>
            </div>

            <div class="mb-4">
              <h4 class="text-md font-semibold text-gray-800 mb-2">Hô hấp</h4>
              <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line">{{ caseData.respiratory || 'Chưa nhập' }}</div>
            </div>
          </div>

          <!-- Investigations -->
          <div>
            <h3 class="text-xl font-bold text-gray-800 mb-3 border-b pb-2">🧪 Cận lâm sàng</h3>
            
            <div class="mb-4">
              <h4 class="text-md font-semibold text-gray-800 mb-2">Xét nghiệm</h4>
              <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line font-mono text-sm">{{ caseData.labsAndImaging || 'Chưa nhập' }}</div>
            </div>

            <div class="mb-4">
              <h4 class="text-md font-semibold text-gray-800 mb-2">Chẩn đoán hình ảnh</h4>
              <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line">{{ caseData.imagingStudies || 'Chưa nhập' }}</div>
            </div>

            <div class="mb-4">
              <h4 class="text-md font-semibold text-gray-800 mb-2">Điện tâm đồ</h4>
              <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line">{{ caseData.ecgFindings || 'Chưa nhập' }}</div>
            </div>
          </div>

          <!-- Diagnosis and Management -->
          <div>
            <h3 class="text-xl font-bold text-gray-800 mb-3 border-b pb-2">💊 Chẩn đoán và điều trị</h3>
            
            <div class="mb-4">
              <h4 class="text-md font-semibold text-gray-800 mb-2">Chẩn đoán chính</h4>
              <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line">{{ caseData.primaryDiagnosis || 'Chưa nhập' }}</div>
            </div>

            <div class="mb-4">
              <h4 class="text-md font-semibold text-gray-800 mb-2">Kế hoạch điều trị (từ form)</h4>
              <div class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line">{{ caseData.treatmentPlanForm || 'Chưa nhập' }}</div>
            </div>
          </div>

          <!-- Medical Attachments -->
          <div v-if="caseData.attachments && caseData.attachments.length > 0">
            <h3 class="text-xl font-bold text-gray-800 mb-3 border-b pb-2">📎 Tệp đính kèm y tế ({{ caseData.attachments.length }})</h3>
            <div class="space-y-4">
              <div v-for="(file, index) in caseData.attachments" :key="index" class="border border-gray-200 rounded-lg p-4">
                <!-- File Header with Title and Preview -->
                <div class="mb-3">
                  <p class="font-semibold text-gray-900 mb-2 text-lg truncate" :title="file.title || file.name">{{ file.title || file.name }}</p>
                  
                  <!-- Image Preview or Icon -->
                  <div class="w-full mb-3">
                    <div v-if="file.type?.startsWith('image/')" class="w-full h-48 rounded-lg overflow-hidden border border-gray-200">
                      <img :src="file.url" :alt="file.title || file.name" class="w-full h-full object-cover" />
                    </div>
                    <div v-else class="w-full h-48 rounded-lg bg-blue-100 flex items-center justify-center">
                      <svg class="w-20 h-20 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </div>
                  </div>
                </div>

                <!-- File Metadata -->
                <div class="bg-gray-50 p-3 rounded-lg space-y-2">
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm">
                    <div v-if="file.attachment_type">
                      <span class="font-medium text-gray-700">Loại tài liệu:</span>
                      <span class="text-gray-600 ml-1">{{ getAttachmentTypeLabel(file.attachment_type) }}</span>
                    </div>
                    <div>
                      <span class="font-medium text-gray-700">Kích thước:</span>
                      <span class="text-gray-600 ml-1">{{ formatFileSize(file.size) }}</span>
                    </div>
                    <div v-if="file.department">
                      <span class="font-medium text-gray-700">Khoa:</span>
                      <span class="text-gray-600 ml-1">{{ getDepartmentLabel(file.department) }}</span>
                    </div>
                    <div v-if="file.date_taken">
                      <span class="font-medium text-gray-700">Ngày thực hiện:</span>
                      <span class="text-gray-600 ml-1">{{ file.date_taken }}</span>
                    </div>
                  </div>
                  
                  <div v-if="file.description" class="pt-2 border-t border-gray-200">
                    <span class="font-medium text-gray-700 text-sm">Mô tả:</span>
                    <p class="text-gray-600 text-sm mt-1">{{ file.description }}</p>
                  </div>
                  
                  <div v-if="file.physician_notes" class="pt-2 border-t border-gray-200">
                    <span class="font-medium text-gray-700 text-sm">Ghi chú bác sĩ:</span>
                    <p class="text-gray-600 text-sm mt-1">{{ file.physician_notes }}</p>
                  </div>
                  
                  <div v-if="file.is_confidential" class="pt-2 border-t border-gray-200">
                    <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                      🔒 Tài liệu bảo mật
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Student Responses -->
          <div class="border-t pt-6">
            <h2 class="text-xl font-bold text-gray-800 mb-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white p-3 rounded-lg">📝 Phản hồi của sinh viên</h2>

            <!-- Clinical Assessment -->
            <div class="mb-6">
              <h3 class="text-lg font-semibold text-gray-800 mb-2">Đánh giá lâm sàng</h3>
              <div class="text-gray-700 bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500 whitespace-pre-line">
                {{ caseData.finalDiagnosis || 'Chưa có nội dung' }}
              </div>
            </div>

            <!-- Differential Diagnosis -->
            <div class="mb-6">
              <h3 class="text-lg font-semibold text-gray-800 mb-2">Chẩn đoán phân biệt</h3>
              <div class="text-gray-700 bg-yellow-50 p-4 rounded-lg border-l-4 border-yellow-500 whitespace-pre-line">
                {{ caseData.differentialDiagnosis || 'Chưa có nội dung' }}
              </div>
            </div>

            <!-- Treatment Plan -->
            <div class="mb-6">
              <h3 class="text-lg font-semibold text-gray-800 mb-2">Kế hoạch điều trị</h3>
              <div class="text-gray-700 bg-green-50 p-4 rounded-lg border-l-4 border-green-500 whitespace-pre-line">
                {{ caseData.treatmentPlan || 'Chưa có nội dung' }}
              </div>
            </div>

            <!-- Learning Points -->
            <div class="mb-6">
              <h3 class="text-lg font-semibold text-gray-800 mb-2">Điểm học tập</h3>
              <div class="text-gray-700 bg-purple-50 p-4 rounded-lg border-l-4 border-purple-500 whitespace-pre-line">
                {{ caseData.notes || 'Chưa có nội dung' }}
              </div>
            </div>
          </div>
        </div>

        <!-- Footer Actions -->
        <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 border-t pt-4">
          <Button variant="outline" @click="$emit('close')" class="w-full sm:w-auto">
            <ArrowLeft class="h-4 w-4 mr-2" />
            Quay lại chỉnh sửa
          </Button>
          <div class="flex flex-col sm:flex-row gap-3">
            <Button variant="outline" @click="handlePrint" class="w-full sm:w-auto">
              <Printer class="h-4 w-4 mr-2" />
              In bệnh án
            </Button>
            <Button v-if="showSubmitButton" @click="$emit('submit')" class="bg-blue-600 hover:bg-blue-700 text-grey w-full sm:w-auto">
              <Send class="h-4 w-4 mr-2" />
              Xác nhận nộp bài
            </Button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Button from '@/components/ui/Button.vue'
import Badge from '@/components/ui/Badge.vue'
import X from '@/components/icons/X.vue'
import ArrowLeft from '@/components/icons/ArrowLeft.vue'
import Printer from '@/components/icons/Printer.vue'
import Send from '@/components/icons/Send.vue'

const props = defineProps({
  caseData: {
    type: Object,
    required: true
  },
  showSubmitButton: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'submit'])

const isOpen = computed(() => true)

const handlePrint = () => {
  window.print()
}

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const getAttachmentTypeLabel = (type: string) => {
  const labels: Record<string, string> = {
    'x_ray': '📷 Chụp X-quang',
    'lab_report': '🧪 Phiếu xét nghiệm',
    'ct_scan': '🔬 Chụp CT',
    'mri_scan': '🧠 Chụp MRI',
    'ultrasound': '📡 Siêu âm',
    'ekg_ecg': '❤️ Điện tâm đồ',
    'other': '📄 Khác'
  }
  return labels[type] || type
}

const getDepartmentLabel = (dept: string) => {
  const labels: Record<string, string> = {
    'cardiology': 'Tim mạch',
    'neurology': 'Thần kinh',
    'radiology': 'Chẩn đoán hình ảnh',
    'pathology': 'Giải phẫu bệnh',
    'emergency': 'Cấp cứu',
    'internal_medicine': 'Nội khoa'
  }
  return labels[dept] || dept
}
</script>

<style scoped>
@media print {
  .fixed {
    position: static !important;
  }

  .bg-black {
    background: transparent !important;
  }

  .max-h-90vh {
    max-height: none !important;
  }

  .overflow-y-auto {
    overflow: visible !important;
  }

  button {
    display: none !important;
  }
}
</style>
