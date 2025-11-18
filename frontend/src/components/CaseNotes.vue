<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <Button variant="ghost" size="icon" @click="$emit('navigate', 'dashboard')">
          <ArrowLeft class="h-5 w-5" />
        </Button>
        <div>
          <h1 class="text-2xl font-bold text-gray-800 mb-1">{{ caseData.title }}</h1>
          <div class="flex items-center gap-2">
            <Badge variant="secondary">{{ caseData.specialty }}</Badge>
            <Badge class="bg-yellow-500 text-white">Đang thực hiện</Badge>
          </div>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <Button variant="outline" @click="handleSave" :disabled="!hasUnsavedChanges">
          <Save class="h-4 w-4 mr-2" />
          Lưu nháp
        </Button>
        <Button @click="handleSubmit" class="bg-blue-600 hover:bg-blue-700 text-grey">
          <Send class="h-4 w-4 mr-2" />
          Nộp để xem xét
        </Button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Case Information (Editable) -->
      <div class="space-y-6">
        <!-- Basic Information -->
        <Card>
          <CardHeader>
            <CardTitle>🏥 Thông tin cơ bản</CardTitle>
          </CardHeader>
          <CardContent class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm text-gray-500">Tiêu đề</label>
                <Input v-model="caseData.title" placeholder="Nhập tiêu đề hồ sơ..." />
              </div>
              <div>
                <label class="text-sm text-gray-500">Chuyên khoa</label>
                <select v-model="caseData.specialty" class="w-full p-2 border rounded-md">
                  <option value="">Chọn chuyên khoa</option>
                  <option value="Hồi sức tích cực">Hồi sức tích cực</option>
                  <option value="Tim mạch">Tim mạch</option>
                  <option value="Nội khoa">Nội khoa</option>
                  <option value="Phẫu thuật">Phẫu thuật</option>
                  <option value="Hô hấp">Hô hấp</option>
                  <option value="Tiêu hóa">Tiêu hóa</option>
                  <option value="Thần kinh">Thần kinh</option>
                  <option value="Sản phụ khoa">Sản phụ khoa</option>
                  <option value="Nhi khoa">Nhi khoa</option>
                  <option value="Khác">Khác</option>
                </select>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Patient Information -->
        <Card>
          <CardHeader>
            <CardTitle>👤 Thông tin bệnh nhân</CardTitle>
          </CardHeader>
          <CardContent class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm text-gray-500">Tên bệnh nhân</label>
                <Input v-model="caseData.patient_name" placeholder="Nhập tên bệnh nhân..." />
              </div>
              <div>
                <label class="text-sm text-gray-500">Tuổi</label>
                <Input v-model.number="caseData.patient_age" type="number" placeholder="Tuổi..." />
              </div>
              <div>
                <label class="text-sm text-gray-500">Giới tính</label>
                <select v-model="caseData.patient_gender" class="w-full p-2 border rounded-md">
                  <option value="">Chọn giới tính</option>
                  <option value="male">Nam</option>
                  <option value="female">Nữ</option>
                  <option value="other">Khác</option>
                </select>
              </div>
              <div>
                <label class="text-sm text-gray-500">Số hồ sơ bệnh án</label>
                <Input v-model="caseData.medical_record_number" placeholder="Số hồ sơ..." />
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Clinical History -->
        <Card>
          <CardHeader>
            <CardTitle>📋 Tiền sử lâm sàng</CardTitle>
          </CardHeader>
          <CardContent class="space-y-4">
            <div>
              <label class="text-sm text-gray-500">Lý do khám chính</label>
              <Textarea v-model="caseData.clinical_history.chief_complaint" placeholder="Lý do khám chính..." />
            </div>
            <div>
              <label class="text-sm text-gray-500">Bệnh sử hiện tại</label>
              <Textarea v-model="caseData.clinical_history.history_present_illness" placeholder="Bệnh sử hiện tại..." />
            </div>
            <div>
              <label class="text-sm text-gray-500">Tiền sử bệnh tật</label>
              <Textarea v-model="caseData.clinical_history.past_medical_history" placeholder="Tiền sử bệnh tật..." />
            </div>
            <div>
              <label class="text-sm text-gray-500">Thuốc đang sử dụng</label>
              <Textarea v-model="caseData.clinical_history.medications" placeholder="Thuốc đang dùng..." />
            </div>
          </CardContent>
        </Card>

        <!-- Physical Examination -->
        <Card>
          <CardHeader>
            <CardTitle>🩺 Khám lâm sàng</CardTitle>
          </CardHeader>
          <CardContent class="space-y-4">
            <div>
              <label class="text-sm text-gray-500">Tình trạng chung</label>
              <Textarea v-model="caseData.physical_examination.general_appearance" placeholder="Tình trạng chung..." />
            </div>
            <div>
              <label class="text-sm text-gray-500">Sinh hiệu</label>
              <Textarea v-model="caseData.physical_examination.vital_signs" placeholder="Sinh hiệu..." />
            </div>
            <div>
              <label class="text-sm text-gray-500">Tim mạch</label>
              <Textarea v-model="caseData.physical_examination.cardiovascular" placeholder="Khám tim mạch..." />
            </div>
            <div>
              <label class="text-sm text-gray-500">Hô hấp</label>
              <Textarea v-model="caseData.physical_examination.respiratory" placeholder="Khám hô hấp..." />
            </div>
          </CardContent>
        </Card>

        <!-- Investigations -->
        <Card>
          <CardHeader>
            <CardTitle>🧪 Cận lâm sàng</CardTitle>
          </CardHeader>
          <CardContent class="space-y-4">
            <div>
              <label class="text-sm text-gray-500">Xét nghiệm</label>
              <Textarea v-model="caseData.investigations.laboratory_results" placeholder="Kết quả xét nghiệm..." />
            </div>
            <div>
              <label class="text-sm text-gray-500">Chẩn đoán hình ảnh</label>
              <Textarea v-model="caseData.investigations.imaging_studies" placeholder="Kết quả chẩn đoán hình ảnh..." />
            </div>
            <div>
              <label class="text-sm text-gray-500">Điện tâm đồ</label>
              <Textarea v-model="caseData.investigations.ecg_findings" placeholder="Kết quả điện tâm đồ..." />
            </div>
          </CardContent>
        </Card>

        <!-- Diagnosis and Management -->
        <Card>
          <CardHeader>
            <CardTitle>💊 Chẩn đoán và điều trị</CardTitle>
          </CardHeader>
          <CardContent class="space-y-4">
            <div>
              <label class="text-sm text-gray-500">Chẩn đoán chính</label>
              <Textarea v-model="caseData.diagnosis_management.primary_diagnosis" placeholder="Chẩn đoán chính..." />
            </div>
            <div>
              <label class="text-sm text-gray-500">Kế hoạch điều trị</label>
              <Textarea v-model="caseData.diagnosis_management.treatment_plan" placeholder="Kế hoạch điều trị..." />
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- Student Notes Section -->
      <div class="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Ghi chú lâm sàng của bạn</CardTitle>
            <CardDescription>
              Hoàn thành đánh giá và kế hoạch cho ca bệnh này
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs v-model="activeTab" default-value="assessment" class="w-full">
              <TabsList class="grid w-full grid-cols-2 sm:grid-cols-4">
                <TabsTrigger value="assessment">Đánh giá</TabsTrigger>
                <TabsTrigger value="differential">Chẩn đoán</TabsTrigger>
                <TabsTrigger value="plan">Kế hoạch</TabsTrigger>
                <TabsTrigger value="learning">Học tập</TabsTrigger>
              </TabsList>

              <TabsContent value="assessment" class="space-y-4">
                <div class="space-y-2">
                  <label class="text-sm font-medium text-gray-800">Đánh giá lâm sàng</label>
                  <p class="text-sm text-gray-500">
                    Đưa ra đánh giá lâm sàng của bạn về bệnh nhân này dựa trên tiền sử, khám lâm sàng và các kết quả
                    chẩn đoán.
                  </p>
                  <Textarea rows="10" v-model="notes.clinical_assessment" placeholder="Viết đánh giá lâm sàng của bạn ở đây..."
                    class="min-h-[400px]" @input="handleNoteChange" />
                </div>
              </TabsContent>

              <TabsContent value="differential" class="space-y-4">
                <div class="space-y-2">
                  <label class="text-sm font-medium text-gray-800">Chẩn đoán phân biệt</label>
                  <p class="text-sm text-gray-500">
                    Liệt kê và giải thích các chẩn đoán phân biệt theo thứ tự khả năng.
                  </p>
                  <Textarea rows="10" v-model="notes.differential_diagnosis"
                    placeholder="1. Chẩn đoán có khả năng nhất và lý do&#10;2. Chẩn đoán phân biệt thứ hai và tại sao...&#10;3. Những cân nhắc khác..."
                    class="min-h-[400px]" @input="handleNoteChange" />
                </div>
              </TabsContent>

              <TabsContent value="plan" class="space-y-4">
                <div class="space-y-2">
                  <label class="text-sm font-medium text-gray-800">Kế hoạch điều trị</label>
                  <p class="text-sm text-gray-500">
                    Phác thảo kế hoạch quản lý ngay lập tức và dài hạn cho bệnh nhân này.
                  </p>
                  <Textarea rows="10" v-model="notes.treatment_plan"
                    placeholder="Xử trí ngay:&#10;- &#10;&#10;Xét nghiệm thêm:&#10;- &#10;&#10;Quản lý dài hạn:&#10;- "
                    class="min-h-[400px]" @input="handleNoteChange" />
                </div>
              </TabsContent>

              <TabsContent value="learning" class="space-y-4">
                <div class="space-y-2">
                  <label class="text-sm font-medium text-gray-800">Điểm học tập</label>
                  <p class="text-sm text-gray-500">
                    Suy ngẫm về những gì bạn đã học được từ ca bệnh này và bất kỳ câu hỏi nào bạn có.
                  </p>
                  <Textarea rows="10" v-model="notes.learning_reflections"
                    placeholder="Điểm học tập chính:&#10;- &#10;&#10;Câu hỏi cho giảng viên:&#10;- &#10;&#10;Lĩnh vực cần nghiên cứu thêm:&#10;- "
                    class="min-h-[400px]" @input="handleNoteChange" />
                </div>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>📎 Tệp đính kèm y tế</CardTitle>
          </CardHeader>
          <CardContent>
            <!-- File Upload Area -->
            <div
              class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors mb-4 cursor-pointer"
              :class="{ 'border-blue-400 bg-blue-50': isDragOver }" @dragover.prevent="isDragOver = true"
              @dragleave.prevent="isDragOver = false" @drop.prevent="handleDrop" @click="fileInput?.click()">
              <div class="space-y-3">
                <svg class="w-12 h-12 text-gray-400 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <div>
                  <p class="text-md font-medium text-gray-900">Kéo thả file vào đây</p>
                  <p class="text-sm text-gray-500">hoặc nhấp để chọn file</p>
                </div>
                <input ref="fileInput" type="file" multiple accept="image/*,.pdf,.doc,.docx" class="hidden"
                  @change="handleFileSelect" />
              </div>
            </div>

            <div class="text-xs text-gray-500 mb-4">
              <p>Định dạng hỗ trợ: JPG, PNG, PDF, DOC, DOCX</p>
              <p>Kích thước tối đa: 10MB mỗi file</p>
            </div>

            <!-- Uploaded Files -->
            <div v-if="attachments.length > 0" class="space-y-4 mt-6">
              <h4 class="font-semibold text-gray-900">File đã tải lên ({{ attachments.length }})</h4>

              <div v-for="(file, index) in attachments" :key="index" class="border border-gray-200 rounded-lg p-4">
                <div class="flex items-start justify-between mb-4">
                  <div class="flex flex-col space-y-2 flex-1 min-w-0">
                    <!-- Title and size placed above preview -->
                    <div class="flex items-start justify-between gap-2">
                      <div class="min-w-0 flex-1">
                        <p class="font-medium text-gray-900 truncate" :title="file.title || file.name">
                          {{ file.title || file.name }}
                        </p>
                        <p class="text-xs text-gray-500">
                          {{ formatFileSize(file.size) }}
                        </p>
                      </div>
                      
                      <Button variant="outline" size="sm" @click="removeFile(index)"
                        class="text-red-600 hover:text-red-700 flex-shrink-0">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </Button>
                    </div>

                    <!-- Image Preview or Icon - takes full width -->
                    <div class="w-full">
                      <div v-if="isImageFile(file)"
                        class="w-full h-64 rounded-lg overflow-hidden border border-gray-200">
                        <img :src="file.url" :alt="file.name" class="w-full h-full object-cover" />
                      </div>

                      <div v-else
                        class="w-full h-64 rounded-lg bg-blue-100 flex items-center justify-center">
                        <svg class="w-24 h-24 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Attachment Metadata Form -->
                <div class="border-t border-gray-200 pt-4 mt-4">
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <!-- Attachment Type -->
                    <div>
                      <label class="block text-xs font-medium text-gray-700 mb-1">Loại tài liệu</label>
                      <select v-model="file.attachment_type"
                        class="w-full px-2 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option value="">Chọn loại</option>
                        <option value="x_ray">📷 Chụp X-quang</option>
                        <option value="lab_report">🧪 Phiếu xét nghiệm</option>
                        <option value="ct_scan">🔬 Chụp CT</option>
                        <option value="mri_scan">🧠 Chụp MRI</option>
                        <option value="ultrasound">📡 Siêu âm</option>
                        <option value="ekg_ecg">❤️ Điện tâm đồ</option>
                        <option value="other">📄 Khác</option>
                      </select>
                    </div>

                    <!-- Title -->
                    <div>
                      <label class="block text-xs font-medium text-gray-700 mb-1">Tiêu đề</label>
                      <input v-model="file.title" type="text"
                        class="w-full px-2 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Nhập tiêu đề..." />
                    </div>

                    <!-- Department -->
                    <div>
                      <label class="block text-xs font-medium text-gray-700 mb-1">Khoa</label>
                      <select v-model="file.department"
                        class="w-full px-2 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option value="">Chọn khoa</option>
                        <option value="cardiology">Tim mạch</option>
                        <option value="neurology">Thần kinh</option>
                        <option value="radiology">Chẩn đoán hình ảnh</option>
                        <option value="pathology">Giải phẫu bệnh</option>
                        <option value="emergency">Cấp cứu</option>
                        <option value="internal_medicine">Nội khoa</option>
                      </select>
                    </div>

                    <!-- Date Taken -->
                    <div>
                      <label class="block text-xs font-medium text-gray-700 mb-1">Ngày thực hiện</label>
                      <input v-model="file.date_taken" type="date"
                        class="w-full px-2 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
                    </div>

                    <!-- Description (Full Width) -->
                    <div class="md:col-span-2">
                      <label class="block text-xs font-medium text-gray-700 mb-1">Mô tả</label>
                      <textarea v-model="file.description" rows="2"
                        class="w-full px-2 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Nhập mô tả chi tiết..."></textarea>
                    </div>

                    <!-- Physician Notes (Full Width) -->
                    <div class="md:col-span-2">
                      <label class="block text-xs font-medium text-gray-700 mb-1">Ghi chú bác sĩ</label>
                      <textarea v-model="file.physician_notes" rows="2"
                        class="w-full px-2 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Ghi chú của bác sĩ..."></textarea>
                    </div>

                    <!-- Is Confidential -->
                    <div class="md:col-span-2">
                      <label class="flex items-center space-x-2 cursor-pointer">
                        <input v-model="file.is_confidential" type="checkbox"
                          class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500" />
                        <span class="text-xs font-medium text-gray-700">Tài liệu bảo mật</span>
                        <span class="text-xs text-gray-500">(Chỉ giảng viên xem được)</span>
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Preview Button -->
        <Button variant="outline" class="w-full" @click="showPreview = true">
          <Eye class="h-4 w-4 mr-2" />
          Xem trước bệnh án trước khi nộp
        </Button>
      </div>
    </div>

    <!-- Preview Dialog -->
    <CasePreview v-if="showPreview" :case-data="previewData" @close="showPreview = false" @submit="handleSubmit"
      :show-submit-button="true" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useToast } from '@/composables/useToast'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import Textarea from '@/components/ui/Textarea.vue'
import Input from '@/components/ui/Input.vue'
import Badge from '@/components/ui/Badge.vue'
import Tabs from '@/components/ui/Tabs.vue'
import TabsContent from '@/components/ui/TabsContent.vue'
import TabsList from '@/components/ui/TabsList.vue'
import TabsTrigger from '@/components/ui/TabsTrigger.vue'
import CasePreview from '@/components/CasePreview.vue'
import { ArrowLeft, Save, Send, Eye } from '@/components/icons'
import { casesService } from '@/services/cases'

const props = defineProps({
  caseId: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['navigate'])

const notes = ref({
  clinical_assessment: '',
  differential_diagnosis: '',
  treatment_plan: '',
  learning_reflections: '',
  questions_for_instructor: '',
  challenges_faced: '',
  resources_used: '',
  final_diagnosis: '',
  plan: '',
  learning: ''
})

const hasUnsavedChanges = ref(false)
const showPreview = ref(false)
const activeTab = ref('assessment')
const { toast } = useToast()

// File upload state
const fileInput = ref<HTMLInputElement>()
const isDragOver = ref(false)
const attachments = ref<any[]>([])

const handleDrop = (event: DragEvent) => {
  isDragOver.value = false
  const files = Array.from(event.dataTransfer?.files || [])
  addFiles(files)
}

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  const files = Array.from(target.files || [])
  addFiles(files)
}

const addFiles = (files: File[]) => {
  const validFiles = files.filter(file => {
    // Check file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      toast.error(`File ${file.name} quá lớn. Kích thước tối đa là 10MB.`)
      return false
    }

    // Check file type
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    if (!allowedTypes.includes(file.type)) {
      toast.error(`File ${file.name} không được hỗ trợ.`)
      return false
    }

    return true
  })

  // Create file objects with URLs for preview and metadata fields
  const fileObjects = validFiles.map(file => ({
    name: file.name,
    size: file.size,
    type: file.type,
    url: URL.createObjectURL(file),
    file: file,
    attachment_type: '',
    title: file.name.split('.')[0] || '',
    department: '',
    description: '',
    date_taken: '',
    physician_notes: '',
    is_confidential: false
  }))

  attachments.value = [...attachments.value, ...fileObjects]
  hasUnsavedChanges.value = true
}

const removeFile = (index: number) => {
  const fileToRemove = attachments.value[index]
  if (fileToRemove.url) {
    URL.revokeObjectURL(fileToRemove.url)
  }
  attachments.value.splice(index, 1)
  hasUnsavedChanges.value = true
}

const isImageFile = (file: any) => {
  return file.type?.startsWith('image/')
}

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// Case data using the same structure as CreateCase.vue
const caseData = ref({
  title: '',
  specialty: '',
  patient_name: '',
  patient_age: '',
  patient_gender: '',
  medical_record_number: '',
  keywords: '',
  template: null,
  repository: null,
  // Detailed medical sections
  clinical_history: {
    chief_complaint: '',
    history_present_illness: '',
    past_medical_history: '',
    family_history: '',
    social_history: '',
    allergies: '',
    medications: '',
    review_systems: ''
  },
  physical_examination: {
    general_appearance: '',
    vital_signs: '',
    head_neck: '',
    cardiovascular: '',
    respiratory: '',
    abdominal: '',
    neurological: '',
    musculoskeletal: '',
    skin: '',
    other_findings: ''
  },
  investigations: {
    laboratory_results: '',
    imaging_studies: '',
    ecg_findings: '',
    special_tests: '',
    biochemistry: '',
    hematology: '',
    microbiology: ''
  },
  diagnosis_management: {
    primary_diagnosis: '',
    differential_diagnosis: '',
    treatment_plan: '',
    medications_prescribed: '',
    procedures_performed: '',
    follow_up_plan: '',
    prognosis: '',
    complications: ''
  },
  learning_outcomes: {
    learning_objectives: '',
    key_concepts: '',
    clinical_pearls: '',
    references: '',
    discussion_points: '',
    assessment_criteria: ''
  }
})

const handleNoteChange = () => {
  hasUnsavedChanges.value = true
}

const handleSave = async () => {
  try {
    console.log('Starting save...', caseData.value)
    
    // 1. Update main case data with properly formatted nested objects
    const caseUpdateData: any = {
      title: caseData.value.title,
      specialty: caseData.value.specialty,
      patient_name: caseData.value.patient_name,
      patient_age: caseData.value.patient_age,
      patient_gender: caseData.value.patient_gender,
      medical_record_number: caseData.value.medical_record_number,
      // Keep status as draft when saving
      case_status: 'draft',
      // Include nested medical data - backend expects these exact field names
      clinical_history: {
        chief_complaint: caseData.value.clinical_history?.chief_complaint || '',
        history_present_illness: caseData.value.clinical_history?.history_present_illness || '',
        past_medical_history: caseData.value.clinical_history?.past_medical_history || '',
        family_history: caseData.value.clinical_history?.family_history || '',
        social_history: caseData.value.clinical_history?.social_history || '',
        allergies: caseData.value.clinical_history?.allergies || '',
        medications: caseData.value.clinical_history?.medications || '',
        review_systems: caseData.value.clinical_history?.review_systems || ''
      },
      physical_examination: {
        general_appearance: caseData.value.physical_examination?.general_appearance || '',
        vital_signs: caseData.value.physical_examination?.vital_signs || '',
        head_neck: caseData.value.physical_examination?.head_neck || '',
        cardiovascular: caseData.value.physical_examination?.cardiovascular || '',
        respiratory: caseData.value.physical_examination?.respiratory || '',
        abdominal: caseData.value.physical_examination?.abdominal || '',
        neurological: caseData.value.physical_examination?.neurological || '',
        musculoskeletal: caseData.value.physical_examination?.musculoskeletal || '',
        skin: caseData.value.physical_examination?.skin || '',
        other_systems: caseData.value.physical_examination?.other_findings || ''
      },
      detailed_investigations: {
        laboratory_results: caseData.value.investigations?.laboratory_results || '',
        imaging_studies: caseData.value.investigations?.imaging_studies || '',
        ecg_findings: caseData.value.investigations?.ecg_findings || '',
        special_tests: caseData.value.investigations?.special_tests || '',
        biochemistry: caseData.value.investigations?.biochemistry || '',
        hematology: caseData.value.investigations?.hematology || '',
        microbiology: caseData.value.investigations?.microbiology || ''
      },
      diagnosis_management: {
        primary_diagnosis: caseData.value.diagnosis_management?.primary_diagnosis || '',
        differential_diagnosis: caseData.value.diagnosis_management?.differential_diagnosis || '',
        treatment_plan: caseData.value.diagnosis_management?.treatment_plan || '',
        medications_prescribed: caseData.value.diagnosis_management?.medications_prescribed || '',
        procedures_performed: caseData.value.diagnosis_management?.procedures_performed || '',
        follow_up_plan: caseData.value.diagnosis_management?.follow_up_plan || '',
        prognosis: caseData.value.diagnosis_management?.prognosis || '',
        complications: caseData.value.diagnosis_management?.complications || ''
      }
    }
    
    // Only include repository and template if they exist and are valid IDs
    if (caseData.value.repository) {
      caseUpdateData.repository = caseData.value.repository
    }
    if (caseData.value.template) {
      caseUpdateData.template = caseData.value.template
    }

    console.log('Sending case update:', caseUpdateData)
    await casesService.updateCase(props.caseId, caseUpdateData)

    // 2. Save/Update student notes (case and student are set by backend)
    const notesData = {
      clinical_assessment: notes.value.clinical_assessment,
      differential_diagnosis: notes.value.differential_diagnosis,
      treatment_plan: notes.value.treatment_plan,
      learning_reflections: notes.value.learning_reflections,
      questions_for_instructor: notes.value.questions_for_instructor || '',
      challenges_faced: notes.value.challenges_faced || '',
      resources_used: notes.value.resources_used || ''
    }

    // Check if notes already exist
    const existingNotes = await casesService.getStudentNotes(props.caseId)
    if (existingNotes && existingNotes.id) {
      await casesService.updateStudentNotes(existingNotes.id, notesData)
    } else {
      await casesService.saveStudentNotes(props.caseId, notesData)
    }

    // 3. Upload new attachments
    for (const attachment of attachments.value) {
      // Only upload if this is a new file (has the 'file' property)
      if (attachment.file && !attachment.id) {
        const formData = new FormData()
        formData.append('file', attachment.file)
        formData.append('title', attachment.title || attachment.name)
        formData.append('attachment_type', attachment.attachment_type || 'other')
        if (attachment.description) formData.append('description', attachment.description)
        if (attachment.department) formData.append('department', attachment.department)
        if (attachment.date_taken) formData.append('date_taken', attachment.date_taken)
        if (attachment.physician_notes) formData.append('physician_notes', attachment.physician_notes)
        formData.append('is_confidential', attachment.is_confidential ? 'true' : 'false')

        await casesService.uploadAttachment(props.caseId, formData)
      }
    }

    toast.success('Đã lưu nháp thành công!')
    hasUnsavedChanges.value = false
  } catch (error: any) {
    console.error('Error saving case:', error)
    console.error('Error response:', error.response?.data)
    
    // Show specific error messages
    if (error.response?.data) {
      const errors = error.response.data
      if (typeof errors === 'object') {
        const errorMessages = Object.entries(errors).map(([field, msgs]) => {
          const messages = Array.isArray(msgs) ? msgs : [msgs]
          return `${field}: ${messages.join(', ')}`
        }).join('\n')
        toast.error(`Lỗi: ${errorMessages}`)
      } else {
        toast.error(error.response?.data?.message || error.response?.data || 'Không thể lưu nháp. Vui lòng thử lại.')
      }
    } else {
      toast.error('Không thể lưu nháp. Vui lòng thử lại.')
    }
  }
}

const handleSubmit = async () => {
  try {
    console.log('Starting submit...')
    
    // First save all data
    await handleSave()

    // Then submit the case (this will change status to 'submitted')
    console.log('Submitting case...')
    await casesService.submitCase(props.caseId)

    toast.success('Ca bệnh đã được nộp để xem xét!')
    setTimeout(() => emit('navigate', 'dashboard'), 1500)
  } catch (error: any) {
    console.error('Error submitting case:', error)
    console.error('Error response:', error.response?.data)
    
    // Show specific error messages
    if (error.response?.data) {
      const errorData = error.response.data
      if (errorData.error) {
        toast.error(errorData.error)
      } else if (typeof errorData === 'object') {
        const errorMessages = Object.entries(errorData).map(([field, msgs]) => {
          const messages = Array.isArray(msgs) ? msgs : [msgs]
          return `${field}: ${messages.join(', ')}`
        }).join('\n')
        toast.error(`Lỗi: ${errorMessages}`)
      } else {
        toast.error(errorData || 'Không thể nộp ca bệnh. Vui lòng thử lại.')
      }
    } else {
      toast.error('Không thể nộp ca bệnh. Vui lòng thử lại.')
    }
  }
}

const previewData = computed(() => ({
  // Basic Information
  title: caseData.value?.title || 'Chưa có tiêu đề',
  specialty: caseData.value?.specialty || 'Chưa chọn chuyên khoa',

  // Patient Information
  patientName: caseData.value?.patient_name || 'Chưa nhập',
  patientAge: caseData.value?.patient_age || 'Chưa nhập',
  patientGender: caseData.value?.patient_gender === 'male' ? 'Nam' : caseData.value?.patient_gender === 'female' ? 'Nữ' : caseData.value?.patient_gender || 'Chưa nhập',
  medicalRecordNumber: caseData.value?.medical_record_number || 'Chưa nhập',

  // Clinical History
  chiefComplaint: caseData.value?.clinical_history?.chief_complaint || 'Chưa nhập',
  historyOfPresentIllness: caseData.value?.clinical_history?.history_present_illness || 'Chưa nhập',
  pastMedicalHistory: caseData.value?.clinical_history?.past_medical_history || 'Chưa nhập',
  medications: caseData.value?.clinical_history?.medications || 'Chưa nhập',

  // Physical Examination
  generalAppearance: caseData.value?.physical_examination?.general_appearance || 'Chưa nhập',
  vitalSigns: caseData.value?.physical_examination?.vital_signs || 'Chưa nhập',
  cardiovascular: caseData.value?.physical_examination?.cardiovascular || 'Chưa nhập',
  respiratory: caseData.value?.physical_examination?.respiratory || 'Chưa nhập',

  // Investigations
  labsAndImaging: caseData.value?.investigations?.laboratory_results || 'Chưa nhập',
  imagingStudies: caseData.value?.investigations?.imaging_studies || 'Chưa nhập',
  ecgFindings: caseData.value?.investigations?.ecg_findings || 'Chưa nhập',

  // Diagnosis and Management (from form)
  primaryDiagnosis: caseData.value?.diagnosis_management?.primary_diagnosis || 'Chưa nhập',
  treatmentPlanForm: caseData.value?.diagnosis_management?.treatment_plan || 'Chưa nhập',

  // Student Notes
  differentialDiagnosis: notes.value?.differential_diagnosis || 'Chưa nhập',
  finalDiagnosis: notes.value?.clinical_assessment || 'Chưa nhập',
  treatmentPlan: notes.value?.treatment_plan || 'Chưa nhập',
  notes: notes.value?.learning_reflections || 'Chưa nhập',

  // Attachments
  attachments: attachments.value || []
}))

onMounted(async () => {
  try {
    // Load case data from API
    const caseDetails = await casesService.getCase(props.caseId)
    console.log('Loaded case details:', caseDetails)
    
    // Ensure all nested objects are initialized
    caseData.value = {
      ...caseDetails,
      clinical_history: caseDetails.clinical_history || {
        chief_complaint: '',
        history_present_illness: '',
        past_medical_history: '',
        family_history: '',
        social_history: '',
        allergies: '',
        medications: '',
        review_systems: ''
      },
      physical_examination: caseDetails.physical_examination || {
        general_appearance: '',
        vital_signs: '',
        head_neck: '',
        cardiovascular: '',
        respiratory: '',
        abdominal: '',
        neurological: '',
        musculoskeletal: '',
        skin: '',
        other_findings: ''
      },
      investigations: caseDetails.investigations_detail || {
        laboratory_results: '',
        imaging_studies: '',
        ecg_findings: '',
        special_tests: '',
        biochemistry: '',
        hematology: '',
        microbiology: ''
      },
      diagnosis_management: caseDetails.diagnosis_management || {
        primary_diagnosis: '',
        differential_diagnosis: '',
        treatment_plan: '',
        medications_prescribed: '',
        procedures_performed: '',
        follow_up_plan: '',
        prognosis: '',
        complications: ''
      }
    }

    // Load existing attachments
    if (caseDetails.medical_attachments && caseDetails.medical_attachments.length > 0) {
      attachments.value = caseDetails.medical_attachments.map((att: any) => ({
        ...att,
        url: att.file,
        type: att.file_type,
        size: att.file_size || 0
      }))
    }

    // Load existing student notes if any
    const existingNotes = await casesService.getStudentNotes(props.caseId)
    if (existingNotes) {
      notes.value = {
        clinical_assessment: existingNotes.clinical_assessment || '',
        differential_diagnosis: existingNotes.differential_diagnosis || '',
        treatment_plan: existingNotes.treatment_plan || '',
        learning_reflections: existingNotes.learning_reflections || '',
        questions_for_instructor: existingNotes.questions_for_instructor || '',
        challenges_faced: existingNotes.challenges_faced || '',
        resources_used: existingNotes.resources_used || '',
        final_diagnosis: existingNotes.clinical_assessment || '',
        plan: existingNotes.treatment_plan || '',
        learning: existingNotes.learning_reflections || ''
      }
    }
  } catch (error) {
    console.error('Error loading case data:', error)
    toast.error('Không thể tải dữ liệu ca bệnh')
  }
})
</script>
