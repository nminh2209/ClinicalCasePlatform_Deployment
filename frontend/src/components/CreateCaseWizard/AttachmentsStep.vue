<template>
  <div class="space-y-6">
    <!-- File Upload Area -->
    <Card class="p-3 border-2 border-gray-200">
      <template #content>
        <div class="p-2">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            {{ t("createCase.uploadFiles") }}
          </h3>

          <div
            class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors cursor-pointer flex flex-col items-center gap-4"
            :class="{ 'border-blue-400 bg-blue-50': isDragOver }"
            @dragover.prevent="isDragOver = true"
            @dragleave.prevent="isDragOver = false"
            @drop.prevent="handleDrop"
            @click="fileInput?.click()"
          >
            <i
              class="pi pi-file-arrow-up text-gray-400"
              style="font-size: 3rem"
            />
            <div>
              <p class="text-lg font-medium text-gray-900">
                {{ t("createCase.dragDropFiles") }}
              </p>
              <p class="text-gray-500">{{ t("createCase.orClickToBrowse") }}</p>
            </div>
            <Button
              outlined
              severity="secondary"
              type="button"
              icon="pi pi-folder-open"
              :label="t('createCase.selectFiles')"
              @click.stop="fileInput?.click()"
              class="text-gray-500"
            />
            <input
              ref="fileInput"
              type="file"
              multiple
              accept="image/*,.pdf,.doc,.docx"
              class="hidden"
              @change="handleFileSelect"
            />
          </div>

          <div class="mt-4 text-sm text-gray-500">
            <p>
              {{ t("createCase.supportedFormats") }}: JPG, PNG, PDF, DOC, DOCX
            </p>
            <p>{{ t("createCase.maxFileSize") }}: 10MB/file</p>
          </div>
        </div>
      </template>
    </Card>

    <!-- OCR Processing Status -->
    <div
      v-if="isOcrProcessing"
      class="bg-blue-50 p-4 rounded-lg flex items-center gap-3"
    >
      <ProgressSpinner style="width: 24px; height: 24px" strokeWidth="4" />
      <div class="flex-1">
        <p class="text-sm font-medium text-blue-800">Đang xử lý OCR...</p>
        <p class="text-xs text-blue-600">
          Đang trích xuất văn bản và điền vào biểu mẫu...
        </p>
      </div>
    </div>

    <!-- Uploaded Files -->
    <Card v-if="localData.attachments && localData.attachments.length > 0">
      <template #content>
        <div class="p-2">
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
                <div class="flex items-center gap-4 flex-1">
                  <!-- Image preview or icon -->
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
                    <i class="pi pi-file-pdf text-blue-600 text-4xl" />
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

                <div class="flex items-center gap-2 ml-4">
                  <!-- OCR Button -->
                  <Button
                    outlined
                    severity="secondary"
                    size="small"
                    @click="runOCR(file)"
                    :disabled="isOcrProcessing"
                    :title="
                      isOcrProcessing
                        ? 'Đang xử lý OCR...'
                        : 'Trích xuất văn bản (OCR)'
                    "
                    :class="{
                      'opacity-50 cursor-not-allowed': isOcrProcessing,
                    }"
                  >
                    <template #default>
                      <span
                        v-if="!isOcrProcessing"
                        class="text-xs font-bold border border-gray-400 rounded px-1"
                        >OCR</span
                      >
                      <span v-else class="flex items-center gap-1">
                        <i class="pi pi-spin pi-spinner text-xs" />
                        <span class="text-xs">...</span>
                      </span>
                    </template>
                  </Button>

                  <!-- Preview Button -->
                  <Button
                    v-if="isImageFile(file)"
                    outlined
                    severity="secondary"
                    size="small"
                    icon="pi pi-eye"
                    @click="previewFile(file)"
                  />

                  <!-- Remove Button -->
                  <Button
                    outlined
                    severity="danger"
                    size="small"
                    icon="pi pi-trash"
                    @click="removeFile(Number(index))"
                  />
                </div>
              </div>

              <!-- Attachment Metadata -->
              <div class="border-t border-gray-200 pt-4 mt-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <!-- Attachment Type -->
                  <div class="flex flex-col gap-1">
                    <label class="text-sm font-medium text-gray-700">
                      {{ t("createCase.attachmentType") }}
                    </label>
                    <Select
                      v-model="file.attachment_type"
                      :options="attachmentTypeOptions"
                      option-label="name"
                      option-value="value"
                      :placeholder="t('createCase.selectType')"
                      class="w-full"
                    />
                  </div>

                  <!-- Title -->
                  <div class="flex flex-col gap-1">
                    <label class="text-sm font-medium text-gray-700">
                      {{ t("createCase.title") }}
                    </label>
                    <InputText
                      v-model="file.title"
                      :placeholder="t('createCase.enterTitle')"
                      class="w-full"
                    />
                  </div>

                  <!-- Description -->
                  <div class="flex flex-col gap-1 md:col-span-2">
                    <label class="text-sm font-medium text-gray-700">
                      {{ t("createCase.description") }}
                    </label>
                    <Textarea
                      v-model="file.description"
                      rows="2"
                      :placeholder="t('createCase.enterDescription')"
                      class="w-full"
                    />
                  </div>

                  <!-- Confidential -->
                  <div class="flex items-center gap-2 md:col-span-2">
                    <Checkbox
                      v-model="file.is_confidential"
                      binary
                      :input-id="`conf-${index}`"
                    />
                    <label
                      :for="`conf-${index}`"
                      class="flex items-center gap-1 text-sm text-gray-700 cursor-pointer"
                    >
                      {{ t("createCase.isConfidential") }}
                      <span class="text-xs text-gray-500"
                        >({{ t("createCase.confidentialDescription") }})</span
                      >
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </Card>

    <!-- File Preview Dialog -->
    <Dialog
      :visible="!!previewFileData"
      @update:visible="closePreview"
      modal
      :header="previewFileData?.name"
      :style="{ width: '90vw', maxWidth: '900px' }"
      :contentStyle="{ maxHeight: 'calc(90vh - 80px)', overflowY: 'auto' }"
    >
      <div class="p-2">
        <img
          v-if="previewFileData && isImageFile(previewFileData)"
          :src="previewFileData.url"
          :alt="previewFileData.name"
          class="max-w-full h-auto object-contain mx-auto"
        />
        <div
          v-else
          class="text-center text-gray-500 py-12 flex flex-col items-center gap-4"
        >
          <i class="pi pi-file text-gray-300" style="font-size: 4rem" />
          <p>{{ t("createCase.previewNotAvailable") }}</p>
        </div>
      </div>
    </Dialog>

    <!-- OCR Result Dialog -->
    <Dialog
      :visible="!!ocrResult"
      @update:visible="ocrResult = null"
      modal
      header="Kết quả OCR"
      :style="{ width: '90vw', maxWidth: '640px' }"
    >
      <div class="flex flex-col gap-4">
        <div
          class="bg-green-50 p-4 rounded-lg border border-green-200 flex items-start gap-3"
        >
          <i
            class="pi pi-check-circle text-green-600 text-xl mt-0.5 shrink-0"
          />
          <div>
            <h3 class="text-sm font-medium text-green-800">OCR thành công</h3>
            <p class="text-sm text-green-700 mt-1">
              Thông tin đã được trích xuất và tự động điền vào biểu mẫu.
            </p>
          </div>
        </div>

        <div
          class="bg-yellow-50 p-4 rounded-lg border border-yellow-200 flex items-start gap-3"
        >
          <i
            class="pi pi-exclamation-triangle text-yellow-600 text-xl mt-0.5 shrink-0"
          />
          <div>
            <h3 class="text-sm font-medium text-yellow-800">
              Lưu ý quan trọng
            </h3>
            <p class="text-sm text-yellow-700 mt-1">
              Thông tin tự động điền có thể không chính xác do sự khác biệt về
              định dạng tiêu đề giữa các bệnh viện. Vui lòng kiểm tra kỹ lại các
              trường dữ liệu.
            </p>
          </div>
        </div>
      </div>

      <template #footer>
        <Button
          label="Đóng"
          outlined
          severity="secondary"
          @click="ocrResult = null"
        />
      </template>
    </Dialog>

    <!-- Case Summary -->
    <Card class="p-3 border-2 border-gray-200">
      <template #content>
        <div class="p-2">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            {{ t("createCase.caseSummary") }}
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
            <div>
              <h4 class="font-medium text-gray-900 mb-2">
                {{ t("createCase.patientInfo") }}
              </h4>
              <dl class="space-y-1">
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
              <dl class="space-y-1">
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
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onUnmounted } from "vue";
import { useI18n } from "vue-i18n";
import Card from "primevue/card";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import InputText from "primevue/inputtext";
import Textarea from "primevue/textarea";
import Select from "primevue/select";
import Checkbox from "primevue/checkbox";
import ProgressSpinner from "primevue/progressspinner";
import { ocrService, type OCRResult } from "@/services/ocr";

const fileInput = ref<HTMLInputElement>();

const props = defineProps<{ caseData: any }>();
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

let currentAbortController: AbortController | null = null;

onUnmounted(() => {
  if (currentAbortController) {
    currentAbortController.abort();
    currentAbortController = null;
  }
});

const isOcrProcessing = computed(() => {
  if (ocrProcessing.value || localData.value?.ocrProcessing === true)
    return true;
  const tableJobStatus = localData.value?.ocrResult?.table_job_status;
  if (tableJobStatus === "queued" || tableJobStatus === "running") return true;
  return false;
});

const attachmentTypeOptions = [
  { name: t("createCase.xRay"), value: "x_ray" },
  { name: t("createCase.labReport"), value: "lab_report" },
  { name: t("createCase.ctScan"), value: "ct_scan" },
  { name: t("createCase.mriScan"), value: "mri_scan" },
  { name: t("createCase.ultrasoundType"), value: "ultrasound" },
  { name: t("createCase.injuryPhoto"), value: "injury_photo" },
  { name: t("createCase.surgicalPhoto"), value: "surgical_photo" },
  { name: t("createCase.pathologySlide"), value: "pathology_slide" },
  { name: t("createCase.prescriptionType"), value: "prescription" },
  { name: t("createCase.dischargeSummary"), value: "discharge_summary" },
  { name: t("createCase.vitalSignsType"), value: "vital_signs" },
  { name: t("createCase.ekgEcg"), value: "ekg_ecg" },
  { name: t("createCase.endoscopyType"), value: "endoscopy" },
  { name: t("createCase.biopsyReport"), value: "biopsy_report" },
  { name: t("createCase.medicalCertificate"), value: "medical_certificate" },
  { name: t("createCase.otherType"), value: "other" },
];

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
  addFiles(Array.from(event.dataTransfer.files) as File[]);
};

const handleFileSelect = (event: any) => {
  addFiles(Array.from(event.target.files) as File[]);
};

const addFiles = async (files: File[]) => {
  const validFiles = files.filter((file) => {
    if (file.size > 10 * 1024 * 1024) {
      alert(`${file.name} ${t("createCase.fileTooLarge")}`);
      return false;
    }
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

  const fileObjects = validFiles.map((file) => ({
    name: file.name,
    size: file.size,
    type: file.type,
    url: URL.createObjectURL(file),
    file,
    attachment_type: "",
    title: file.name.split(".")[0] || "",
    description: "",
    is_confidential: false,
  }));

  const currentAttachments = localData.value.attachments || [];
  localData.value = {
    ...localData.value,
    attachments: [...currentAttachments, ...fileObjects],
  };
};

const runOCR = async (fileObj: any) => {
  if (ocrProcessing.value) return;

  const fileToProcess = fileObj.file;
  if (!fileToProcess) {
    alert("Lỗi: Không tìm thấy tệp. Vui lòng tải lên lại.");
    return;
  }

  ocrResult.value = null;
  currentAbortController = new AbortController();
  const signal = currentAbortController.signal;

  try {
    ocrProcessing.value = true;
    const currentAttachments = localData.value.attachments || [];
    localData.value = {
      ...localData.value,
      attachments: currentAttachments,
      ocrProcessing: true,
    };

    const { ocr, autofill } = await ocrService.extractAndAutofill(
      fileToProcess,
      0.6,
      "full",
      signal,
    );
    ocrResult.value = ocr;

    emit("ocr-extracted", ocr);

    const ocrResultsMap = localData.value.ocrResultsMap || {};
    ocrResultsMap[fileToProcess.name] = ocr;

    const updateData: Record<string, any> = {
      ...localData.value,
      attachments: currentAttachments,
      ocrResult: ocr,
      ocrResultsMap,
      currentOcrFile: fileToProcess.name,
      ocrProcessing: false,
    };

    if (autofill.structured && Object.keys(autofill.structured).length > 0) {
      const mergeData = (target: any, source: any) => {
        for (const key in source) {
          if (
            typeof source[key] === "object" &&
            source[key] !== null &&
            !Array.isArray(source[key])
          ) {
            if (!target[key]) target[key] = {};
            mergeData(target[key], source[key]);
          } else if (
            source[key] &&
            typeof source[key] === "string" &&
            source[key].trim() !== ""
          ) {
            target[key] = source[key];
          }
        }
      };
      mergeData(updateData, autofill.structured);
    }

    localData.value = updateData;
  } catch (error: any) {
    if (
      error.message === "OCR request was cancelled" ||
      error.name === "AbortError" ||
      error.name === "CanceledError"
    ) {
      // Silently cancelled
    } else {
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
    currentAbortController = null;
  }
};

const isImageFile = (file: any) => file.type.startsWith("image/");
const previewFile = (file: any) => {
  previewFileData.value = file;
};
const closePreview = () => {
  previewFileData.value = null;
};

const removeFile = (index: number) => {
  const attachments = [...(localData.value.attachments || [])];
  const fileToRemove = attachments[index];
  if (fileToRemove?.url) URL.revokeObjectURL(fileToRemove.url);
  attachments.splice(index, 1);
  localData.value = { ...localData.value, attachments };
};

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
};
</script>
