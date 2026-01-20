<template>
  <div class="space-y-6">
    <!-- File Upload Area -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ t("createCase.uploadFiles") }}
        </h3>

        <div
          class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors cursor-pointer"
          :class="{ 'border-blue-400 bg-blue-50': isDragOver }"
          @dragover.prevent="isDragOver = true"
          @dragleave.prevent="isDragOver = false"
          @drop.prevent="handleDrop"
          @click="fileInput?.click()"
        >
          <div class="space-y-4">
            <UploadIcon class="w-12 h-12 text-gray-400 mx-auto" />
            <div>
              <p class="text-lg font-medium text-gray-900">
                {{ t("createCase.dragDropFiles") }}
              </p>
              <p class="text-gray-500">
                {{ t("createCase.orClickToBrowse") }}
              </p>
            </div>
            <Button variant="outline" type="button">
              {{ t("createCase.selectFiles") }}
            </Button>
            <input
              ref="fileInput"
              type="file"
              multiple
              accept="image/*,.pdf,.doc,.docx"
              class="hidden"
              @change="handleFileSelect"
            />
          </div>
        </div>

        <div class="mt-4 text-sm text-gray-500">
          <p>
            {{ t("createCase.supportedFormats") }}: JPG, PNG, PDF, DOC, DOCX
          </p>
          <p>{{ t("createCase.maxFileSize") }}: 10MB/file</p>
        </div>
      </div>
    </Card>

    <!-- OCR Processing Status -->
    <div
      v-if="isOcrProcessing"
      class="bg-blue-50 p-4 rounded-lg flex items-center gap-3"
    >
      <div
        class="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"
      ></div>
      <div class="flex-1">
        <p class="text-sm font-medium text-blue-800">Đang xử lý OCR...</p>
        <p class="text-xs text-blue-600">
          Đang trích xuất văn bản và điền vào biểu mẫu...
        </p>
      </div>
    </div>

    <!-- Uploaded Files -->
    <Card v-if="localData.attachments && localData.attachments.length > 0">
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ t("createCase.uploadedFiles") }} ({{
            localData.attachments.length
          }})
        </h3>

        <div class="space-y-6">
          <div
            v-for="(file, index) in localData.attachments"
            :key="index"
            class="border border-gray-200 rounded-lg p-4"
          >
            <div class="flex items-start justify-between mb-4">
              <div class="flex items-center space-x-4 flex-1">
                <!-- Image Preview or Icon -->
                <div
                  v-if="isImageFile(file)"
                  class="w-24 h-24 rounded-lg overflow-hidden shrink-0 border border-gray-200"
                >
                  <img
                    :src="file.url"
                    :alt="file.name"
                    class="w-full h-full object-cover"
                  />
                </div>
                <div
                  v-else
                  class="w-24 h-24 rounded-lg bg-blue-100 flex items-center justify-center shrink-0"
                >
                  <DocumentIcon class="w-12 h-12 text-blue-600" />
                </div>

                <div class="flex-1 min-w-0">
                  <p class="font-medium text-gray-900 truncate">
                    {{ file.name }}
                  </p>
                  <p class="text-sm text-gray-500">
                    {{ formatFileSize(file.size) }} •
                    {{ file.type || "Unknown type" }}
                  </p>
                </div>
              </div>

              <div class="flex items-center space-x-2 ml-4">
                <Button
                  variant="outline"
                  size="sm"
                  @click="runOCR(file)"
                  :disabled="isOcrProcessing"
                  :title="isOcrProcessing ? 'Đang xử lý OCR...' : 'Trích xuất văn bản (OCR)'"
                  :class="{ 'opacity-50 cursor-not-allowed': isOcrProcessing }"
                >
                  <span v-if="!isOcrProcessing"
                    class="text-xs font-bold border border-gray-400 rounded px-1"
                    >OCR</span
                  >
                  <span v-else class="flex items-center gap-1">
                    <span class="animate-spin h-3 w-3 border-2 border-gray-400 border-t-transparent rounded-full"></span>
                    <span class="text-xs">...</span>
                  </span>
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  @click="previewFile(file)"
                  v-if="isImageFile(file)"
                >
                  <EyeIcon class="w-4 h-4" />
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  @click="removeFile(Number(index))"
                  class="text-red-600 hover:text-red-700"
                >
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
                    {{ t("createCase.attachmentType") }}
                  </label>
                  <select
                    v-model="file.attachment_type"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">{{ t("createCase.selectType") }}</option>
                    <option value="x_ray">📷 {{ t("createCase.xRay") }}</option>
                    <option value="lab_report">
                      🧪 {{ t("createCase.labReport") }}
                    </option>
                    <option value="ct_scan">
                      🔬 {{ t("createCase.ctScan") }}
                    </option>
                    <option value="mri_scan">
                      🧠 {{ t("createCase.mriScan") }}
                    </option>
                    <option value="ultrasound">
                      📡 {{ t("createCase.ultrasoundType") }}
                    </option>
                    <option value="injury_photo">
                      📸 {{ t("createCase.injuryPhoto") }}
                    </option>
                    <option value="surgical_photo">
                      ⚕️ {{ t("createCase.surgicalPhoto") }}
                    </option>
                    <option value="pathology_slide">
                      🔬 {{ t("createCase.pathologySlide") }}
                    </option>
                    <option value="prescription">
                      💊 {{ t("createCase.prescriptionType") }}
                    </option>
                    <option value="discharge_summary">
                      📋 {{ t("createCase.dischargeSummary") }}
                    </option>
                    <option value="vital_signs">
                      💓 {{ t("createCase.vitalSignsType") }}
                    </option>
                    <option value="ekg_ecg">
                      ❤️ {{ t("createCase.ekgEcg") }}
                    </option>
                    <option value="endoscopy">
                      🔍 {{ t("createCase.endoscopyType") }}
                    </option>
                    <option value="biopsy_report">
                      🧬 {{ t("createCase.biopsyReport") }}
                    </option>
                    <option value="medical_certificate">
                      📜 {{ t("createCase.medicalCertificate") }}
                    </option>
                    <option value="other">
                      📄 {{ t("createCase.otherType") }}
                    </option>
                  </select>
                </div>

                <!-- Title -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    {{ t("createCase.title") }}
                  </label>
                  <input
                    v-model="file.title"
                    type="text"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    :placeholder="t('createCase.enterTitle')"
                  />
                </div>

                <!-- Description (Full Width) -->
                <div class="md:col-span-2">
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    {{ t("createCase.description") }}
                  </label>
                  <textarea
                    v-model="file.description"
                    rows="2"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    :placeholder="t('createCase.enterDescription')"
                  ></textarea>
                </div>

                <!-- Is Confidential -->
                <div class="md:col-span-2">
                  <label class="flex items-center space-x-2 cursor-pointer">
                    <input
                      v-model="file.is_confidential"
                      type="checkbox"
                      class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                    />
                    <span class="text-sm font-medium text-gray-700">
                      {{ t("createCase.isConfidential") }}
                    </span>
                    <span class="text-xs text-gray-500">
                      ({{ t("createCase.confidentialDescription") }})
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
    <div
      v-if="previewFileData"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click="closePreview"
    >
      <div
        class="bg-white rounded-lg max-w-4xl max-h-[90vh] w-full mx-4 overflow-hidden"
        @click.stop
      >
        <div class="flex items-center justify-between p-4 border-b">
          <h3 class="text-lg font-semibold">{{ previewFileData.name }}</h3>
          <Button variant="outline" @click="closePreview">
            <XIcon class="w-4 h-4" />
          </Button>
        </div>
        <div class="p-4 overflow-auto max-h-[calc(90vh-80px)]">
          <img
            v-if="isImageFile(previewFileData)"
            :src="previewFileData.url"
            :alt="previewFileData.name"
            class="max-w-full h-auto object-contain mx-auto"
          />
          <div v-else class="text-center text-gray-500 py-12">
            <DocumentIcon class="w-16 h-16 mx-auto mb-4" />
            <p>{{ t("createCase.previewNotAvailable") }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- OCR Result Modal -->
    <div
      v-if="ocrResult"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click="ocrResult = null"
    >
      <div
        class="bg-white rounded-lg max-w-2xl w-full mx-4 max-h-[80vh] flex flex-col"
        @click.stop
      >
        <div class="p-4 border-b flex justify-between items-center">
          <h3 class="font-semibold text-lg">Kết quả OCR</h3>
          <button
            @click="ocrResult = null"
            class="text-gray-500 hover:text-gray-700"
          >
            &times;
          </button>
        </div>
        <div class="p-4 overflow-y-auto flex-1">
          <div class="bg-green-50 p-4 rounded-lg border border-green-200 mb-4">
            <div class="flex items-start">
              <div class="flex-shrink-0">
                <span class="text-xl">✅</span>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-green-800">
                  OCR thành công
                </h3>
                <div class="mt-2 text-sm text-green-700">
                  <p>
                    Thông tin đã được trích xuất và tự động điền vào biểu mẫu.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
            <div class="flex items-start">
              <div class="flex-shrink-0">
                <span class="text-xl">⚠️</span>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-yellow-800">
                  Lưu ý quan trọng
                </h3>
                <div class="mt-2 text-sm text-yellow-700">
                  <p>
                    Thông tin tự động điền có thể không chính xác do sự khác
                    biệt về định dạng tiêu đề giữa các bệnh viện. Vui lòng kiểm
                    tra kỹ lại các trường dữ liệu.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="p-4 border-t flex justify-end gap-2">
          <Button variant="outline" @click="ocrResult = null">Đóng</Button>
        </div>
      </div>
    </div>

    <!-- Case Summary -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ t("createCase.caseSummary") }}
        </h3>

        <div class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 class="font-medium text-gray-900 mb-2">
                {{ t("createCase.patientInfo") }}
              </h4>
              <dl class="space-y-1 text-sm">
                <div class="flex justify-between">
                  <dt class="text-gray-600">{{ t("createCase.age") }}:</dt>
                  <dd class="font-medium">
                    {{ localData.patient_age || t("createCase.notSpecified") }}
                  </dd>
                </div>
                <div class="flex justify-between">
                  <dt class="text-gray-600">{{ t("createCase.gender") }}:</dt>
                  <dd class="font-medium">
                    {{
                      localData.patient_gender || t("createCase.notSpecified")
                    }}
                  </dd>
                </div>
                <div class="flex justify-between">
                  <dt class="text-gray-600">{{ t("createCase.mrn") }}:</dt>
                  <dd class="font-medium">
                    {{
                      localData.medical_record_number ||
                      t("createCase.notAssigned")
                    }}
                  </dd>
                </div>
              </dl>
            </div>

            <div>
              <h4 class="font-medium text-gray-900 mb-2">
                {{ t("createCase.caseDetails") }}
              </h4>
              <dl class="space-y-1 text-sm">
                <div class="flex justify-between">
                  <dt class="text-gray-600">{{ t("createCase.title") }}:</dt>
                  <dd class="font-medium">
                    {{ localData.title || t("createCase.untitledCase") }}
                  </dd>
                </div>
                <div class="flex justify-between">
                  <dt class="text-gray-600">
                    {{ t("createCase.specialty") }}:
                  </dt>
                  <dd class="font-medium">
                    {{ localData.specialty || t("createCase.notSpecified") }}
                  </dd>
                </div>
                <div class="flex justify-between">
                  <dt class="text-gray-600">
                    {{ t("createCase.attachments") }}:
                  </dt>
                  <dd class="font-medium">
                    {{ localData.attachments?.length || 0 }}
                  </dd>
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
import { ref, computed, nextTick, onUnmounted } from "vue";
import { useI18n } from "vue-i18n";
import Card from "@/components/ui/Card.vue";
import Button from "@/components/ui/Button.vue";
import {
  UploadIcon,
  DocumentIcon,
  EyeIcon,
  TrashIcon,
  XIcon,
} from "@/components/icons";
import { ocrService, type OCRResult } from "@/services/ocr";

const fileInput = ref<HTMLInputElement>();

const props = defineProps<{
  caseData: any;
}>();

const { t } = useI18n();

const emit = defineEmits<{
  "update:caseData": [any];
  "ocr-extracted": [any];
}>();

const localData = computed({
  get: () => props.caseData,
  set: (value) => emit("update:caseData", value),
});

const isDragOver = ref(false);
const ocrProcessing = ref(false);
const ocrResult = ref<OCRResult | null>(null);

// AbortController for canceling ongoing fetch requests on unmount
let currentAbortController: AbortController | null = null;

// Cleanup on component unmount (e.g., page refresh)
onUnmounted(() => {
  if (currentAbortController) {
    console.log("🛑 Canceling ongoing OCR request on unmount");
    currentAbortController.abort();
    currentAbortController = null;
  }
});

// Computed: Check if OCR is processing (from local ref OR persisted state)
// Also considers if table/image extraction (Celery) is still running
const isOcrProcessing = computed(() => {
  // Text extraction in progress
  if (ocrProcessing.value || localData.value?.ocrProcessing === true) {
    return true;
  }
  
  // Check if Celery table/image extraction is pending
  const tableJobStatus = localData.value?.ocrResult?.table_job_status;
  if (tableJobStatus === 'queued' || tableJobStatus === 'running') {
    return true;
  }
  
  return false;
});

interface FileWithURL extends File {
  url?: string;
  attachment_type?: string;
  title?: string;
  description?: string;
  is_confidential?: boolean;
  file?: File;
}

const previewFileData = ref<FileWithURL | null>(null);

const handleDrop = (event: any) => {
  isDragOver.value = false;
  const files: File[] = Array.from(event.dataTransfer.files);
  addFiles(files);
};

const handleFileSelect = (event: any) => {
  const files: File[] = Array.from(event.target.files);
  addFiles(files);
};

const addFiles = async (files: File[]) => {
  const validFiles = files.filter((file) => {
    // Check file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      alert(`${file.name} ${t("createCase.fileTooLarge")}`);
      return false;
    }

    // Check file type
    const allowedTypes = [
      "image/jpeg",
      "image/png",
      "image/gif",
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];
    if (!allowedTypes.includes(file.type)) {
      alert(`${file.name} ${t("createCase.unsupportedFileType")}`);
      return false;
    }

    return true;
  });

  // Create file objects with URLs for preview and metadata fields
  const fileObjects = validFiles.map((file) => ({
    name: file.name,
    size: file.size,
    type: file.type,
    url: URL.createObjectURL(file),
    file: file,
    attachment_type: "",
    title: file.name.split(".")[0] || "",
    description: "",
    is_confidential: false,
  }));

  // Update attachments array
  const currentAttachments = localData.value.attachments || [];
  const newAttachments = [...currentAttachments, ...fileObjects];
  
  localData.value = {
    ...localData.value,
    attachments: newAttachments,
  };

  // NOTE: Auto-OCR removed. Users can click the OCR button manually for each file.
  // This prevents race conditions with multiple file uploads and gives users more control.
};

const runOCR = async (fileObj: any) => {
  // Guard: prevent duplicate OCR calls
  if (ocrProcessing.value) {
    console.warn("⚠️ OCR already in progress, ignoring duplicate call");
    return;
  }

  const fileToProcess = fileObj.file;
  if (!fileToProcess) {
    console.warn("⚠️ No file to process - File object may have been lost");
    alert("Lỗi: Không tìm thấy tệp. Vui lòng tải lên lại.");
    return;
  }

  // Clear previous result to prevent showing stale modal
  ocrResult.value = null;

  // Create AbortController for this request (cancel on unmount)
  currentAbortController = new AbortController();
  const signal = currentAbortController.signal;

  try {
    ocrProcessing.value = true;
    console.log(`🔄 Starting OCR for: ${fileToProcess.name}`);

    // IMPORTANT: Don't use JSON.parse(JSON.stringify()) - it destroys File objects!
    // Instead, spread current data and preserve attachments array with File references
    const currentAttachments = localData.value.attachments || [];
    
    // Update processing state while preserving attachments
    localData.value = {
      ...localData.value,
      attachments: currentAttachments, // Keep original array with File objects
      ocrProcessing: true,
    };

    // Use mode='full' to enable async table/image extraction
    // Pass AbortController signal for cancellation support
    const { ocr, autofill } = await ocrService.extractAndAutofill(
      fileToProcess,
      0.6, // confidence threshold
      "full", // Enable table/image extraction
      signal // Pass AbortController signal
    );
    ocrResult.value = ocr;

    // Log table job status
    if (ocr.table_job_id) {
      console.log(
        `📊 Table/image extraction queued: job_id=${ocr.table_job_id}`
      );
    }

    // Emit OCR results to parent for OCR panel display
    emit("ocr-extracted", ocr);

    // Store OCR result in map keyed by filename (preserves previous results)
    const ocrResultsMap = localData.value.ocrResultsMap || {};
    ocrResultsMap[fileToProcess.name] = ocr;

    // Build update data while preserving attachments
    const updateData: Record<string, any> = {
      ...localData.value,
      attachments: currentAttachments, // Keep original array with File objects  
      ocrResult: ocr, // Keep current file result for backward compatibility
      ocrResultsMap, // Store all results by filename
      currentOcrFile: fileToProcess.name, // Track which file's result is current
      ocrProcessing: false,
    };

    // Apply auto-fill from SBERT semantic matching
    if (autofill.structured && Object.keys(autofill.structured).length > 0) {
      console.log(
        `✅ Auto-fill: ${autofill.metadata.fields_matched} fields matched in ${autofill.metadata.elapsed_ms}ms`
      );

      // Recursive merge function
      const mergeData = (target: any, source: any) => {
        for (const key in source) {
          if (
            typeof source[key] === "object" &&
            source[key] !== null &&
            !Array.isArray(source[key])
          ) {
            if (!target[key]) target[key] = {};
            mergeData(target[key], source[key]);
          } else {
            // Only update if source has value
            if (
              source[key] &&
              typeof source[key] === "string" &&
              source[key].trim() !== ""
            ) {
              target[key] = source[key];
            }
          }
        }
      };

      mergeData(updateData, autofill.structured);
    }

    localData.value = updateData;
  } catch (error: any) {
    // Handle cancellation gracefully (no alert for user-initiated cancels like page refresh)
    if (error.message === "OCR request was cancelled" || 
        error.name === "AbortError" || 
        error.name === "CanceledError") {
      console.log("🛑 OCR request was cancelled");
    } else {
      console.error("OCR Failed:", error);
      // Clear processing state on error while preserving attachments
      const currentAttachmentsOnError = localData.value.attachments || [];
      localData.value = {
        ...localData.value,
        attachments: currentAttachmentsOnError,
        ocrProcessing: false,
      };
      alert(`Lỗi OCR: ${error.message || "Không thể xử lý tệp"}`);
    }
  } finally {
    ocrProcessing.value = false;
    currentAbortController = null; // Clear controller reference
  }
};

const isImageFile = (file: any) => {
  return file.type.startsWith("image/");
};

const previewFile = (file: any) => {
  previewFileData.value = file;
};

const closePreview = () => {
  previewFileData.value = null;
};

const removeFile = (index: number) => {
  const attachments = [...(localData.value.attachments || [])];
  const fileToRemove = attachments[index];
  if (fileToRemove?.url) {
    URL.revokeObjectURL(fileToRemove.url);
  }
  attachments.splice(index, 1);
  localData.value = {
    ...localData.value,
    attachments,
  };
};

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
};
</script>
