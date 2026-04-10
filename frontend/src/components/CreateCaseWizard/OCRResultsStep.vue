<template>
  <div class="space-y-6">
    <Card class="p-3 border-2 border-gray-200">
      <template #content>
        <div class="p-2">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Kết quả OCR</h3>

          <!-- File Tabs (multiple files) -->
          <div
            v-if="ocrFileNames.length > 1"
            class="flex gap-2 flex-wrap border-b pb-3 mb-4"
          >
            <Button
              v-for="fileName in ocrFileNames"
              :key="fileName"
              :label="fileName"
              size="small"
              :severity="selectedOcrFile === fileName ? undefined : 'secondary'"
              :outlined="selectedOcrFile !== fileName"
              icon="pi pi-file"
              class="max-w-[200px] truncate"
              :title="fileName"
              @click="selectOcrFile(fileName)"
            />
          </div>

          <!-- No OCR Results -->
          <div
            v-if="!hasOCRResults"
            class="text-center py-12 flex flex-col items-center gap-4"
          >
            <i
              class="pi pi-file-import text-gray-300"
              style="font-size: 3rem"
            />
            <h4 class="text-lg font-medium text-gray-600">
              Chưa có kết quả OCR
            </h4>
            <p class="text-gray-500 max-w-md">
              Tải lên tệp PDF hoặc hình ảnh ở bước "Tệp Đính Kèm" và nhấn nút
              OCR để trích xuất văn bản, bảng và hình ảnh.
            </p>
            <Button
              icon="pi pi-arrow-left"
              label="Quay lại Tệp Đính Kèm"
              outlined
              severity="secondary"
              @click="goToAttachmentsStep"
            />
          </div>

          <!-- OCR Results -->
          <div v-else class="space-y-6">
            <!-- Plain Text -->
            <div v-if="ocrData?.text" class="border rounded-lg p-4">
              <h4
                class="font-medium text-gray-900 mb-3 flex items-center gap-2"
              >
                <i class="pi pi-file-edit text-blue-600" />
                Văn bản đã trích xuất
              </h4>
              <div class="bg-gray-50 rounded p-4 max-h-48 overflow-y-auto">
                <pre
                  class="whitespace-pre-wrap text-sm text-gray-700 font-mono"
                  >{{ ocrData.text }}</pre
                >
              </div>
            </div>

            <!-- Tables/Images Loading -->
            <div
              v-if="tableJobLoading"
              class="border rounded-lg p-6 bg-blue-50 border-blue-200 flex items-center gap-4"
            >
              <ProgressSpinner
                style="width: 36px; height: 36px"
                strokeWidth="4"
              />
              <div>
                <h4 class="font-medium text-blue-800">
                  Đang xử lý bảng và hình ảnh...
                </h4>
                <p class="text-sm text-blue-600 mt-1">
                  Quá trình này có thể mất vài phút.
                  <span v-if="pollAttempts > 0"
                    >(Đang kiểm tra... lần {{ pollAttempts }})</span
                  >
                </p>
                <p
                  v-if="tableJobId"
                  class="text-xs text-blue-500 mt-2 font-mono"
                >
                  Job ID: {{ tableJobId }}
                </p>
              </div>
            </div>

            <!-- Tables/Images Error -->
            <div
              v-if="tableJobError"
              class="border rounded-lg p-6 bg-red-50 border-red-200 flex items-start gap-4"
            >
              <i
                class="pi pi-exclamation-triangle text-red-500 text-2xl mt-0.5 shrink-0"
              />
              <div>
                <h4 class="font-medium text-red-800">
                  Trích xuất bảng/hình ảnh thất bại
                </h4>
                <p class="text-sm text-red-600 mt-1">{{ tableJobError }}</p>
                <Button
                  icon="pi pi-refresh"
                  label="Thử lại"
                  outlined
                  severity="danger"
                  size="small"
                  class="mt-3"
                  @click="retryTableImageExtraction"
                />
              </div>
            </div>

            <!-- Page Tabs (multi-page) -->
            <div
              v-if="!tableJobLoading && uniquePages.length > 1"
              class="flex gap-2 flex-wrap border-b pb-3"
            >
              <Button
                :label="`Tất cả (${tables.length + images.length})`"
                size="small"
                :severity="selectedPage === null ? undefined : 'secondary'"
                :outlined="selectedPage !== null"
                @click="selectedPage = null"
              />
              <Button
                v-for="page in uniquePages"
                :key="page"
                :label="`Trang ${page} (${getPageItemCount(page)})`"
                size="small"
                :severity="selectedPage === page ? undefined : 'secondary'"
                :outlined="selectedPage !== page"
                @click="selectedPage = page"
              />
            </div>

            <!-- Tables -->
            <div
              v-if="!tableJobLoading && filteredTables.length > 0"
              class="border rounded-lg p-4"
            >
              <h4
                class="font-medium text-gray-900 mb-3 flex items-center gap-2"
              >
                <i class="pi pi-table text-green-600" />
                Bảng ({{ filteredTables.length }})
              </h4>
              <div class="space-y-4">
                <div
                  v-for="(table, index) in filteredTables"
                  :key="index"
                  class="bg-gray-50 rounded p-4"
                >
                  <div class="flex justify-between items-center mb-2">
                    <span class="text-sm font-medium"
                      >Bảng {{ index + 1 }} (Trang {{ table.page }})</span
                    >
                    <Button
                      icon="pi pi-clipboard"
                      label="Sao chép Markdown"
                      outlined
                      severity="secondary"
                      size="small"
                      @click="copyTableAsMarkdown(table)"
                    />
                  </div>
                  <div
                    v-if="table.html"
                    v-html="table.html"
                    class="overflow-x-auto table-content"
                  />
                  <div v-else class="text-sm text-gray-500">
                    Không thể hiển thị bảng
                  </div>
                </div>
              </div>
            </div>

            <!-- Images -->
            <div
              v-if="!tableJobLoading && filteredImages.length > 0"
              class="border rounded-lg p-4"
            >
              <h4
                class="font-medium text-gray-900 mb-3 flex items-center gap-2"
              >
                <i class="pi pi-images text-purple-600" />
                Hình ảnh ({{ filteredImages.length }})
              </h4>
              <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
                <div
                  v-for="(image, index) in filteredImages"
                  :key="index"
                  class="border rounded-lg overflow-hidden cursor-pointer hover:shadow-md transition-shadow"
                  @click="previewImage(image)"
                >
                  <img
                    v-if="image.url"
                    :src="image.url"
                    :alt="`Hình ${index + 1}`"
                    class="w-full h-32 object-cover"
                  />
                  <div class="p-2 text-xs text-gray-500 truncate">
                    {{ image.caption || `Hình ${index + 1}` }}
                  </div>
                </div>
              </div>
            </div>

            <!-- Only Text (no tables/images) -->
            <div
              v-if="
                !tableJobLoading &&
                tables.length === 0 &&
                images.length === 0 &&
                !tableJobId &&
                !tableJobSkipped
              "
              class="bg-yellow-50 p-4 rounded-lg border border-yellow-200 flex items-start gap-3"
            >
              <i
                class="pi pi-info-circle text-yellow-600 text-xl mt-0.5 shrink-0"
              />
              <div>
                <h4 class="font-medium text-yellow-800">Chỉ có văn bản</h4>
                <p class="text-sm text-yellow-700 mt-1">
                  Tài liệu này không chứa bảng hoặc hình ảnh đã được nhận dạng.
                  Văn bản đã được tự động điền vào biểu mẫu.
                </p>
              </div>
            </div>

            <!-- Table Extraction Skipped -->
            <div
              v-if="tableJobSkipped"
              class="bg-blue-50 p-4 rounded-lg border border-blue-200 flex items-start gap-3"
            >
              <i
                class="pi pi-file-edit text-blue-600 text-xl mt-0.5 shrink-0"
              />
              <div>
                <h4 class="font-medium text-blue-800">Chỉ có văn bản</h4>
                <p class="text-sm text-blue-700 mt-1">
                  Không phát hiện bảng hoặc hình ảnh trong tài liệu. Văn bản đã
                  được tự động điền vào biểu mẫu.
                </p>
              </div>
            </div>
          </div>
        </div>
      </template>
    </Card>

    <!-- Image Preview Dialog -->
    <Dialog
      :visible="!!previewingImage"
      @update:visible="previewingImage = null"
      modal
      :header="previewingImage?.caption || 'Hình ảnh'"
      :style="{ width: '90vw', maxWidth: '900px' }"
    >
      <div class="flex justify-center">
        <img
          v-if="previewingImage"
          :src="previewingImage.url"
          :alt="previewingImage.caption"
          class="max-w-full max-h-[75vh] object-contain rounded-lg"
        />
      </div>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from "vue";
import Card from "primevue/card";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import ProgressSpinner from "primevue/progressspinner";
import { ocrService, type TableResult, type ImageResult } from "@/services/ocr";
import api from "@/services/api";

const props = defineProps<{ caseData: any }>();
const emit = defineEmits<{ "update:caseData": [any] }>();

const previewingImage = ref<any>(null);
const tableJobLoading = ref(false);
const tables = ref<TableResult[]>([]);
const images = ref<ImageResult[]>([]);
const pollAttempts = ref(0);
const tableJobError = ref<string | null>(null);
const selectedPage = ref<number | null>(null);
const selectedOcrFile = ref<string | null>(null);

let currentPollingJobId: string | null = null;
let pollAbortController: AbortController | null = null;

onUnmounted(() => {
  if (pollAbortController) {
    pollAbortController.abort();
    pollAbortController = null;
  }
  currentPollingJobId = null;
});

const ocrResultsMap = computed(() => props.caseData?.ocrResultsMap || {});
const ocrFileNames = computed(() => Object.keys(ocrResultsMap.value));

watch(
  ocrFileNames,
  (names) => {
    if (names.length > 0 && !selectedOcrFile.value) {
      selectedOcrFile.value = props.caseData?.currentOcrFile || names[0];
    }
  },
  { immediate: true },
);

const selectOcrFile = (fileName: string) => {
  selectedOcrFile.value = fileName;
  selectedPage.value = null;
  const fileResult = ocrResultsMap.value[fileName];
  if (fileResult?.tables) tables.value = fileResult.tables;
  if (fileResult?.images) images.value = fileResult.images;
  if (
    fileResult?.table_job_id &&
    tables.value.length === 0 &&
    images.value.length === 0
  ) {
    pollTableImageJob(fileResult.table_job_id);
  }
};

const ocrData = computed(() => {
  if (selectedOcrFile.value && ocrResultsMap.value[selectedOcrFile.value]) {
    return ocrResultsMap.value[selectedOcrFile.value];
  }
  return props.caseData?.ocrResult || null;
});

const tableJobId = computed(() => ocrData.value?.table_job_id || null);
const tableJobSkipped = computed(
  () => ocrData.value?.table_job_status === "skipped",
);
const tableJobSkipReason = computed(
  () => ocrData.value?.table_job_reason || "",
);
const hasOCRResults = computed(
  () =>
    !!ocrData.value?.text ||
    tables.value.length > 0 ||
    images.value.length > 0 ||
    ocrFileNames.value.length > 0,
);

const uniquePages = computed(() => {
  const pageSet = new Set<number>();
  for (const t of tables.value) {
    if (t.page) pageSet.add(t.page);
  }
  for (const i of images.value) {
    if (i.page) pageSet.add(i.page);
  }
  return Array.from(pageSet).sort((a, b) => a - b);
});

const filteredTables = computed(() => {
  if (selectedPage.value === null) return tables.value;
  return tables.value.filter((t) => t.page === selectedPage.value);
});

const filteredImages = computed(() => {
  if (selectedPage.value === null) return images.value;
  return images.value.filter((i) => i.page === selectedPage.value);
});

const getPageItemCount = (page: number): number =>
  tables.value.filter((t) => t.page === page).length +
  images.value.filter((i) => i.page === page).length;

watch(
  tableJobId,
  async (jobId) => {
    if (
      jobId &&
      tables.value.length === 0 &&
      images.value.length === 0 &&
      !tableJobError.value
    ) {
      await pollTableImageJob(jobId);
    }
  },
  { immediate: true },
);

onMounted(() => {
  if (ocrData.value?.tables) tables.value = ocrData.value.tables;
  if (ocrData.value?.images) images.value = ocrData.value.images;
  if (
    tableJobId.value &&
    tables.value.length === 0 &&
    images.value.length === 0 &&
    !tableJobLoading.value &&
    !tableJobError.value
  ) {
    pollTableImageJob(tableJobId.value);
  }
});

const pollTableImageJob = async (jobId: string) => {
  if (currentPollingJobId && currentPollingJobId !== jobId) {
    if (pollAbortController) pollAbortController.abort();
  }
  if (currentPollingJobId === jobId && tableJobLoading.value) return;

  currentPollingJobId = jobId;
  pollAbortController = new AbortController();
  const signal = pollAbortController.signal;

  tableJobLoading.value = true;
  tableJobError.value = null;
  pollAttempts.value = 0;

  try {
    const result = await new Promise<any>((resolve, reject) => {
      const startTime = Date.now();
      const timeoutMs = 300000;
      const intervalMs = 3000;

      const checkStatus = async () => {
        if (signal.aborted) {
          reject(new Error("Polling was cancelled"));
          return;
        }
        if (currentPollingJobId !== jobId) {
          reject(new Error("Polling was cancelled - new job started"));
          return;
        }

        pollAttempts.value++;

        try {
          if (Date.now() - startTime > timeoutMs) {
            reject(new Error("Quá thời gian chờ (5 phút). Vui lòng thử lại."));
            return;
          }

          const response = await api.get(`/ocr/jobs/${jobId}/`, { signal });
          const data = response.data;

          if (data.status === "done" || data.status === "SUCCESS") {
            resolve(data);
          } else if (data.status === "failed" || data.status === "FAILURE") {
            reject(new Error(data.error || "Trích xuất thất bại"));
          } else {
            setTimeout(checkStatus, intervalMs);
          }
        } catch (error: any) {
          if (error.name === "AbortError" || error.name === "CanceledError") {
            reject(new Error("Polling was cancelled"));
          } else {
            reject(error);
          }
        }
      };

      checkStatus();
    });

    tables.value = result.tables || [];
    images.value = result.images || [];

    const newData = { ...props.caseData };
    if (newData.ocrResult) {
      newData.ocrResult.tables = result.tables;
      newData.ocrResult.images = result.images;
      newData.ocrResult.table_job_status = "done";
    }
    emit("update:caseData", newData);
  } catch (error: any) {
    if (!error.message?.includes("cancelled") && error.name !== "AbortError") {
      tableJobError.value = error.message || "Lỗi không xác định";
    }
  } finally {
    if (currentPollingJobId === jobId) {
      tableJobLoading.value = false;
      pollAbortController = null;
    }
  }
};

const retryTableImageExtraction = async () => {
  tableJobError.value = null;
  if (tableJobId.value) await pollTableImageJob(tableJobId.value);
};

const goToAttachmentsStep = () => {
  // Parent wizard handles step navigation
};

const previewImage = (image: any) => {
  previewingImage.value = image;
};

const copyTableAsMarkdown = async (table: any) => {
  try {
    const markdown = table.markdown || convertHtmlToMarkdown(table.html);
    await navigator.clipboard.writeText(markdown);
    alert("Đã sao chép bảng dưới dạng Markdown!");
  } catch {
    alert("Không thể sao chép. Vui lòng thử lại.");
  }
};

const convertHtmlToMarkdown = (html: string): string => {
  if (!html) return "";
  const temp = document.createElement("div");
  temp.innerHTML = html;
  const rows = temp.querySelectorAll("tr");
  let markdown = "";
  rows.forEach((row, idx) => {
    const cells = row.querySelectorAll("td, th");
    const rowText = Array.from(cells)
      .map((c) => c.textContent?.trim() || "")
      .join(" | ");
    markdown += `| ${rowText} |\n`;
    if (idx === 0) {
      markdown += `|${Array.from(cells)
        .map(() => "---")
        .join("|")}|\n`;
    }
  });
  return markdown;
};
</script>

<style scoped>
.table-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
}
.table-content :deep(th),
.table-content :deep(td) {
  border: 1px solid #e5e7eb;
  padding: 8px;
  text-align: left;
}
.table-content :deep(th) {
  background-color: #f9fafb;
  font-weight: 600;
}
</style>
