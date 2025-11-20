<template>
  <div class="space-y-6">
    <div class="text-center">
      <h2 class="text-2xl font-bold text-gray-900 mb-2">
        Medical Attachments
      </h2>
      <p class="text-gray-600">
        Upload X-rays, lab reports, and other medical images or documents
      </p>
    </div>

    <!-- File Upload Area -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          Upload Files
        </h3>

        <div
          class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors cursor-pointer"
          :class="{ 'border-blue-400 bg-blue-50': isDragOver }" @dragover.prevent="isDragOver = true"
          @dragleave.prevent="isDragOver = false" @drop.prevent="handleDrop" @click="fileInput?.click()">
          <div class="space-y-4">
            <UploadIcon class="w-12 h-12 text-gray-400 mx-auto" />
            <div>
              <p class="text-lg font-medium text-gray-900">
                Drag and drop files here
              </p>
              <p class="text-gray-500">
                or click to browse
              </p>
            </div>
            <Button variant="outline" type="button">
              Select Files
            </Button>
            <input ref="fileInput" type="file" multiple accept="image/*,.pdf,.doc,.docx" class="hidden"
              @change="handleFileSelect" />
          </div>
        </div>

        <div class="mt-4 text-sm text-gray-500">
          <p>Supported formats: JPG, PNG, PDF, DOC, DOCX</p>
          <p>Maximum file size: 10MB per file</p>
        </div>
      </div>
    </Card>

    <!-- Uploaded Files -->
    <Card v-if="localData.attachments && localData.attachments.length > 0">
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          Uploaded Files ({{ localData.attachments.length }})
        </h3>

        <div class="space-y-6">
          <div v-for="(file, index) in localData.attachments" :key="index"
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
                    Attachment Type
                  </label>
                  <select v-model="file.attachment_type" 
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option value="">Select type...</option>
                    <option value="x_ray">📷 X-Ray</option>
                    <option value="lab_report">🧪 Lab Report</option>
                    <option value="ct_scan">🔬 CT Scan</option>
                    <option value="mri_scan">🧠 MRI Scan</option>
                    <option value="ultrasound">📡 Ultrasound</option>
                    <option value="injury_photo">📸 Injury Photo</option>
                    <option value="surgical_photo">⚕️ Surgical Photo</option>
                    <option value="pathology_slide">🔬 Pathology Slide</option>
                    <option value="prescription">💊 Prescription</option>
                    <option value="discharge_summary">📋 Discharge Summary</option>
                    <option value="vital_signs">💓 Vital Signs Chart</option>
                    <option value="ekg_ecg">❤️ EKG/ECG</option>
                    <option value="endoscopy">🔍 Endoscopy</option>
                    <option value="biopsy_report">🧬 Biopsy Report</option>
                    <option value="medical_certificate">📜 Medical Certificate</option>
                    <option value="other">📄 Other</option>
                  </select>
                </div>

                <!-- Title -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Title
                  </label>
                  <input v-model="file.title" type="text" 
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Enter title..." />
                </div>

                <!-- Description (Full Width) -->
                <div class="md:col-span-2">
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Description
                  </label>
                  <textarea v-model="file.description" rows="2"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Describe the attachment..."></textarea>
                </div>

                <!-- Is Confidential -->
                <div class="md:col-span-2">
                  <label class="flex items-center space-x-2 cursor-pointer">
                    <input v-model="file.is_confidential" type="checkbox" 
                      class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500" />
                    <span class="text-sm font-medium text-gray-700">
                      Mark as confidential
                    </span>
                    <span class="text-xs text-gray-500">
                      (restricted access to authorized users only)
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
      <div class="bg-white rounded-lg max-w-4xl max-h-[90vh] w-full mx-4 overflow-hidden" @click.stop>
        <div class="flex items-center justify-between p-4 border-b">
          <h3 class="text-lg font-semibold">{{ previewFileData.name }}</h3>
          <Button variant="outline" @click="closePreview">
            <XIcon class="w-4 h-4" />
          </Button>
        </div>
        <div class="p-4 overflow-auto max-h-[calc(90vh-80px)]">
          <img v-if="isImageFile(previewFileData)" :src="previewFileData.url" :alt="previewFileData.name"
            class="max-w-full h-auto object-contain mx-auto" />
          <div v-else class="text-center text-gray-500 py-12">
            <DocumentIcon class="w-16 h-16 mx-auto mb-4" />
            <p>Preview not available for this file type</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Case Summary -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          Case Summary
        </h3>

        <div class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 class="font-medium text-gray-900 mb-2">Patient Information</h4>
              <dl class="space-y-1 text-sm">
                <div class="flex justify-between">
                  <dt class="text-gray-600">Age:</dt>
                  <dd class="font-medium">{{ localData.patient_age || 'Not specified' }} years</dd>
                </div>
                <div class="flex justify-between">
                  <dt class="text-gray-600">Gender:</dt>
                  <dd class="font-medium">{{ localData.patient_gender || 'Not specified' }}</dd>
                </div>
                <div class="flex justify-between">
                  <dt class="text-gray-600">MRN:</dt>
                  <dd class="font-medium">{{ localData.medical_record_number || 'Not assigned' }}</dd>
                </div>
              </dl>
            </div>

            <div>
              <h4 class="font-medium text-gray-900 mb-2">Case Details</h4>
              <dl class="space-y-1 text-sm">
                <div class="flex justify-between">
                  <dt class="text-gray-600">Title:</dt>
                  <dd class="font-medium">{{ localData.title || 'Untitled Case' }}</dd>
                </div>
                <div class="flex justify-between">
                  <dt class="text-gray-600">Specialty:</dt>
                  <dd class="font-medium">{{ localData.specialty || 'Not specified' }}</dd>
                </div>
                <div class="flex justify-between">
                  <dt class="text-gray-600">Attachments:</dt>
                  <dd class="font-medium">{{ localData.attachments?.length || 0 }}</dd>
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
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import { UploadIcon, DocumentIcon, EyeIcon, TrashIcon, XIcon } from '@/components/icons'

const fileInput = ref<HTMLInputElement>()

const props = defineProps<{
  caseData: any
}>()

const emit = defineEmits<{
  'update:caseData': [any]
}>()

const localData = computed({
  get: () => props.caseData,
  set: (value) => emit('update:caseData', value)
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
      alert(`File "${file.name}" is too large. Maximum size is 10MB.`)
      return false
    }

    // Check file type
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    if (!allowedTypes.includes(file.type)) {
      alert(`File "${file.name}" has unsupported format. Please upload JPG, PNG, PDF, DOC, or DOCX files.`)
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
    description: '',
    is_confidential: false
  }))

  // Update attachments array
  const currentAttachments = localData.value.attachments || []
  localData.value = {
    ...localData.value,
    attachments: [...currentAttachments, ...fileObjects]
  }
}

const removeFile = (index: number) => {
  const attachments = localData.value.attachments || []
  const fileToRemove = attachments[index]
  if (fileToRemove.url) {
    URL.revokeObjectURL(fileToRemove.url)
  }
  const updatedAttachments = [...attachments]
  updatedAttachments.splice(index, 1)
  localData.value = {
    ...localData.value,
    attachments: updatedAttachments
  }
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
