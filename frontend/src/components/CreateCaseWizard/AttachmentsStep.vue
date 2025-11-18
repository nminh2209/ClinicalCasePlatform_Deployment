<template>
  <div class="space-y-6">
    <div class="text-center">
      <h2 class="text-2xl font-bold text-gray-900 mb-2">
        {{ $t('createCase.attachments') }}
      </h2>
      <p class="text-gray-600">
        {{ $t('createCase.attachmentsDescription') }}
      </p>
    </div>

    <!-- File Upload Area -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ $t('createCase.uploadFiles') }}
        </h3>

        <div
          class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors"
          :class="{ 'border-blue-400 bg-blue-50': isDragOver }" @dragover.prevent="isDragOver = true"
          @dragleave.prevent="isDragOver = false" @drop.prevent="handleDrop">
          <div class="space-y-4">
            <UploadIcon class="w-12 h-12 text-gray-400 mx-auto" />
            <div>
              <p class="text-lg font-medium text-gray-900">
                {{ $t('createCase.dragDropFiles') }}
              </p>
              <p class="text-gray-500">
                {{ $t('createCase.orClickToBrowse') }}
              </p>
            </div>
            <Button variant="outline" @click="fileInput?.click()">
              {{ $t('createCase.selectFiles') }}
            </Button>
            <input ref="fileInput" type="file" multiple accept="image/*,.pdf,.doc,.docx" class="hidden"
              @change="handleFileSelect" />
          </div>
        </div>

        <div class="mt-4 text-sm text-gray-500">
          <p>{{ $t('createCase.supportedFormats') }}: JPG, PNG, PDF, DOC, DOCX</p>
          <p>{{ $t('createCase.maxFileSize') }}: 10MB {{ $t('createCase.perFile') }}</p>
        </div>
      </div>
    </Card>

    <!-- Uploaded Files -->
    <Card v-if="attachments.length > 0">
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ $t('createCase.uploadedFiles') }}
        </h3>

        <div class="space-y-6">
          <div v-for="(file, index) in attachments" :key="index"
            class="border border-gray-200 rounded-lg p-4">
            <div class="flex items-start justify-between mb-4">
              <div class="flex items-center space-x-4 flex-1">
                <!-- Image Preview or Icon -->
                <div v-if="isImageFile(file)" class="w-24 h-24 rounded-lg overflow-hidden flex-shrink-0 border border-gray-200">
                  <img :src="file.url" :alt="file.name" class="w-full h-full object-cover" />
                </div>
                <div v-else class="w-24 h-24 rounded-lg bg-blue-100 flex items-center justify-center flex-shrink-0">
                  <DocumentIcon class="w-12 h-12 text-blue-600" />
                </div>
                
                <div class="flex-1 min-w-0">
                  <p class="font-medium text-gray-900 truncate">{{ file.name }}</p>
                  <p class="text-sm text-gray-500">
                    {{ formatFileSize(file.size) }} • {{ file.type || 'Unknown type' }}
                  </p>
                </div>
              </div>

              <div class="flex items-center space-x-2 ml-4">
                <Button variant="outline" size="sm" @click="previewFile(file)" v-if="isImageFile(file)">
                  <EyeIcon class="w-4 h-4" />
                </Button>
                <Button variant="outline" size="sm" @click="removeFile(index)" class="text-red-600 hover:text-red-700">
                  <TrashIcon class="w-4 h-4" />
                </Button>
              </div>
            </div>

            <!-- Attachment Metadata Form -->
            <div class="border-t border-gray-200 pt-4 mt-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <!-- Attachment Type -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    {{ $t('createCase.attachmentType') }}
                  </label>
                  <select v-model="file.attachment_type" 
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option value="">{{ $t('createCase.selectType') }}</option>
                    <option value="x_ray">📷 {{ $t('createCase.xRay') }}</option>
                    <option value="lab_report">🧪 {{ $t('createCase.labReport') }}</option>
                    <option value="ct_scan">🔬 {{ $t('createCase.ctScan') }}</option>
                    <option value="mri_scan">🧠 {{ $t('createCase.mriScan') }}</option>
                    <option value="ultrasound">📡 {{ $t('createCase.ultrasoundType') }}</option>
                    <option value="injury_photo">📸 {{ $t('createCase.injuryPhoto') }}</option>
                    <option value="surgical_photo">⚕️ {{ $t('createCase.surgicalPhoto') }}</option>
                    <option value="pathology_slide">🔬 {{ $t('createCase.pathologySlide') }}</option>
                    <option value="prescription">💊 {{ $t('createCase.prescriptionType') }}</option>
                    <option value="discharge_summary">📋 {{ $t('createCase.dischargeSummary') }}</option>
                    <option value="vital_signs">💓 {{ $t('createCase.vitalSignsType') }}</option>
                    <option value="ekg_ecg">❤️ {{ $t('createCase.ekgEcg') }}</option>
                    <option value="endoscopy">🔍 {{ $t('createCase.endoscopyType') }}</option>
                    <option value="biopsy_report">🧬 {{ $t('createCase.biopsyReport') }}</option>
                    <option value="medical_certificate">📜 {{ $t('createCase.medicalCertificate') }}</option>
                    <option value="other">📄 {{ $t('createCase.otherType') }}</option>
                  </select>
                </div>

                <!-- Title -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    {{ $t('createCase.title') }}
                  </label>
                  <input v-model="file.title" type="text" 
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    :placeholder="$t('createCase.enterTitle')" />
                </div>

                <!-- Department -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    {{ $t('createCase.department') }}
                  </label>
                  <select v-model="file.department" 
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option value="">{{ $t('createCase.selectDepartment') }}</option>
                    <option value="cardiology">{{ $t('createCase.cardiology') }}</option>
                    <option value="neurology">{{ $t('createCase.neurology') }}</option>
                    <option value="orthopedics">{{ $t('createCase.orthopedics') }}</option>
                    <option value="pediatrics">{{ $t('createCase.pediatrics') }}</option>
                    <option value="radiology">{{ $t('createCase.radiology') }}</option>
                    <option value="pathology">{{ $t('createCase.pathology') }}</option>
                    <option value="emergency">{{ $t('createCase.emergency') }}</option>
                    <option value="surgery">{{ $t('createCase.surgery') }}</option>
                    <option value="internal_medicine">{{ $t('createCase.internalMedicine') }}</option>
                    <option value="other">{{ $t('createCase.otherType') }}</option>
                  </select>
                </div>

                <!-- Date Taken -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    {{ $t('createCase.dateTaken') }}
                  </label>
                  <input v-model="file.date_taken" type="date" 
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>

                <!-- Description (Full Width) -->
                <div class="md:col-span-2">
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    {{ $t('createCase.description') }}
                  </label>
                  <textarea v-model="file.description" rows="2"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    :placeholder="$t('createCase.enterDescription')"></textarea>
                </div>

                <!-- Physician Notes (Full Width) -->
                <div class="md:col-span-2">
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    {{ $t('createCase.physicianNotes') }}
                  </label>
                  <textarea v-model="file.physician_notes" rows="2"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    :placeholder="$t('createCase.enterPhysicianNotes')"></textarea>
                </div>

                <!-- Is Confidential -->
                <div class="md:col-span-2">
                  <label class="flex items-center space-x-2 cursor-pointer">
                    <input v-model="file.is_confidential" type="checkbox" 
                      class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500" />
                    <span class="text-sm font-medium text-gray-700">
                      {{ $t('createCase.isConfidential') }}
                    </span>
                    <span class="text-xs text-gray-500">
                      ({{ $t('createCase.confidentialDescription') }})
                    </span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Card>

    <!-- File Preview Modal -->
    <div v-if="previewFileData" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click="closePreview">
      <div class="bg-white rounded-lg max-w-4xl max-h-4xl w-full mx-4 overflow-hidden">
        <div class="flex items-center justify-between p-4 border-b">
          <h3 class="text-lg font-semibold">{{ previewFileData.name }}</h3>
          <Button variant="outline" @click="closePreview">
            <XIcon class="w-4 h-4" />
          </Button>
        </div>
        <div class="p-4">
          <img v-if="isImageFile(previewFileData)" :src="previewFileData.url" :alt="previewFileData.name"
            class="max-w-full max-h-96 object-contain" />
          <div v-else class="text-center text-gray-500">
            <DocumentIcon class="w-16 h-16 mx-auto mb-4" />
            <p>{{ $t('createCase.previewNotAvailable') }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Case Summary -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ $t('createCase.caseSummary') }}
        </h3>

        <div class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 class="font-medium text-gray-900 mb-2">{{ $t('createCase.patientInfo') }}</h4>
              <dl class="space-y-1 text-sm">
                <div class="flex justify-between">
                  <dt class="text-gray-600">{{ $t('createCase.name') }}:</dt>
                  <dd class="font-medium">{{ caseData.patient?.firstName }} {{ caseData.patient?.lastName }}</dd>
                </div>
                <div class="flex justify-between">
                  <dt class="text-gray-600">{{ $t('createCase.age') }}:</dt>
                  <dd class="font-medium">{{ caseData.patient?.age }}</dd>
                </div>
                <div class="flex justify-between">
                  <dt class="text-gray-600">{{ $t('createCase.gender') }}:</dt>
                  <dd class="font-medium">{{ caseData.patient?.gender }}</dd>
                </div>
              </dl>
            </div>

            <div>
              <h4 class="font-medium text-gray-900 mb-2">{{ $t('createCase.caseDetails') }}</h4>
              <dl class="space-y-1 text-sm">
                <div class="flex justify-between">
                  <dt class="text-gray-600">{{ $t('createCase.template') }}:</dt>
                  <dd class="font-medium">{{ caseData.template?.name }}</dd>
                </div>
                <div class="flex justify-between">
                  <dt class="text-gray-600">{{ $t('createCase.attachments') }}:</dt>
                  <dd class="font-medium">{{ attachments.length }}</dd>
                </div>
                <div class="flex justify-between">
                  <dt class="text-gray-600">{{ $t('createCase.learningObjectives') }}:</dt>
                  <dd class="font-medium">{{ caseData.assessment?.learningObjectives?.length || 0 }}</dd>
                </div>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import { UploadIcon, FileIcon, DocumentIcon, EyeIcon, TrashIcon, XIcon } from '@/components/icons'

const { t } = useI18n()
const fileInput = ref<HTMLInputElement>()

const props = defineProps({
  caseData: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:caseData'])

const attachments = computed({
  get: () => props.caseData.attachments || [],
  set: (value) => emit('update:caseData', {
    ...props.caseData,
    attachments: value
  })
})

const isDragOver = ref(false)
interface FileWithURL extends File {
  url?: string;
}

const previewFileData = ref<FileWithURL | null>(null)

const handleDrop = (event: any) => {
  isDragOver.value = false
  const files: File[] = Array.from(event.dataTransfer.files)
  addFiles(files)
}

const handleFileSelect = (event: any) => {
  const files: File[] = Array.from(event.target.files)
  addFiles(files)
}

const addFiles = (files: File[]) => {
  const validFiles = files.filter(file => {
    // Check file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      alert(t('createCase.fileTooLarge', { fileName: file.name }))
      return false
    }

    // Check file type
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    if (!allowedTypes.includes(file.type)) {
      alert(t('createCase.unsupportedFileType', { fileName: file.name }))
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
}

const removeFile = (index: number) => {
  const fileToRemove = attachments.value[index]
  if (fileToRemove.url) {
    URL.revokeObjectURL(fileToRemove.url)
  }
  attachments.value.splice(index, 1)
}

const isImageFile = (file: File) => {
  return file.type?.startsWith('image/')
}

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const previewFile = (file: File) => {
  previewFileData.value = file
}

const closePreview = () => {
  previewFileData.value = null
}
</script>
