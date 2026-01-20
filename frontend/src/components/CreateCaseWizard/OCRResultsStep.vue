<template>
  <div class="space-y-6">
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">📄 Kết quả OCR</h3>

        <!-- File Tabs (when multiple files have OCR results) -->
        <div
          v-if="ocrFileNames.length > 1"
          class="flex gap-2 flex-wrap border-b pb-3 mb-4"
        >
          <button
            v-for="fileName in ocrFileNames"
            :key="fileName"
            @click="selectOcrFile(fileName)"
            :class="[
              'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors truncate max-w-[200px]',
              selectedOcrFile === fileName
                ? 'bg-blue-500 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
            ]"
            :title="fileName"
          >
            📄 {{ fileName }}
          </button>
        </div>

        <!-- No OCR Results Yet -->
        <div v-if="!hasOCRResults" class="text-center py-12">
          <FileSearch class="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h4 class="text-lg font-medium text-gray-600 mb-2">
            Chưa có kết quả OCR
          </h4>
          <p class="text-gray-500 max-w-md mx-auto">
            Tải lên tệp PDF hoặc hình ảnh ở bước "Tệp Đính Kèm" và nhấn nút OCR
            để trích xuất văn bản, bảng và hình ảnh.
          </p>
          <Button variant="outline" class="mt-4" @click="goToAttachmentsStep">
            ← Quay lại Tệp Đính Kèm
          </Button>
        </div>

        <!-- OCR Results Available -->
        <div v-else class="space-y-6">
          <!-- Plain Text Section -->
          <div v-if="ocrData?.text" class="border rounded-lg p-4">
            <h4 class="font-medium text-gray-900 mb-3 flex items-center gap-2">
              <FileText class="w-5 h-5 text-blue-600" />
              Văn bản đã trích xuất
            </h4>
            <div class="bg-gray-50 rounded p-4 max-h-48 overflow-y-auto">
              <pre
                class="whitespace-pre-wrap text-sm text-gray-700 font-mono"
                >{{ ocrData.text }}</pre
              >
            </div>
          </div>

          <!-- Tables/Images Loading State -->
          <div
            v-if="tableJobLoading"
            class="border rounded-lg p-6 bg-blue-50 border-blue-200"
          >
            <div class="flex items-center gap-4">
              <div
                class="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full"
              ></div>
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
          </div>

          <!-- Tables/Images Error State -->
          <div
            v-if="tableJobError"
            class="border rounded-lg p-6 bg-red-50 border-red-200"
          >
            <div class="flex items-start gap-4">
              <span class="text-2xl">⚠️</span>
              <div>
                <h4 class="font-medium text-red-800">
                  Trích xuất bảng/hình ảnh thất bại
                </h4>
                <p class="text-sm text-red-600 mt-1">
                  {{ tableJobError }}
                </p>
                <Button
                  variant="outline"
                  size="sm"
                  class="mt-3"
                  @click="retryTableImageExtraction"
                >
                  🔄 Thử lại
                </Button>
              </div>
            </div>
          </div>

          <!-- Page Tabs (when multi-page results) -->
          <div
            v-if="!tableJobLoading && uniquePages.length > 1"
            class="flex gap-2 flex-wrap border-b pb-3"
          >
            <button
              @click="selectedPage = null"
              :class="[
                'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                selectedPage === null
                  ? 'bg-purple-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
              ]"
            >
              Tất cả ({{ tables.length + images.length }})
            </button>
            <button
              v-for="page in uniquePages"
              :key="page"
              @click="selectedPage = page"
              :class="[
                'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                selectedPage === page
                  ? 'bg-purple-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
              ]"
            >
              Trang {{ page }} ({{ getPageItemCount(page) }})
            </button>
          </div>

          <!-- Tables Section -->
          <div
            v-if="!tableJobLoading && filteredTables.length > 0"
            class="border rounded-lg p-4"
          >
            <h4 class="font-medium text-gray-900 mb-3 flex items-center gap-2">
              <TableIcon class="w-5 h-5 text-green-600" />
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
                    variant="outline"
                    size="sm"
                    @click="copyTableAsMarkdown(table)"
                  >
                    📋 Sao chép Markdown
                  </Button>
                </div>
                <div
                  v-if="table.html"
                  v-html="table.html"
                  class="overflow-x-auto table-content"
                ></div>
                <div v-else class="text-sm text-gray-500">
                  Không thể hiển thị bảng
                </div>
              </div>
            </div>
          </div>

          <!-- Images Section -->
          <div
            v-if="!tableJobLoading && filteredImages.length > 0"
            class="border rounded-lg p-4"
          >
            <h4 class="font-medium text-gray-900 mb-3 flex items-center gap-2">
              <ImageIcon class="w-5 h-5 text-purple-600" />
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

          <!-- No Tables/Images Message (only show after loading completes) -->
          <div
            v-if="
              !tableJobLoading &&
              tables.length === 0 &&
              images.length === 0 &&
              !tableJobId &&
              !tableJobSkipped
            "
            class="bg-yellow-50 p-4 rounded-lg border border-yellow-200"
          >
            <div class="flex items-start gap-3">
              <span class="text-xl">ℹ️</span>
              <div>
                <h4 class="font-medium text-yellow-800">Chỉ có văn bản</h4>
                <p class="text-sm text-yellow-700 mt-1">
                  Tài liệu này không chứa bảng hoặc hình ảnh đã được nhận dạng.
                  Văn bản đã được tự động điền vào biểu mẫu.
                </p>
              </div>
            </div>
          </div>

          <!-- Table Extraction Skipped (no tables/images detected) -->
          <div
            v-if="tableJobSkipped"
            class="bg-blue-50 p-4 rounded-lg border border-blue-200"
          >
            <div class="flex items-start gap-3">
              <span class="text-xl">📝</span>
              <div>
                <h4 class="font-medium text-blue-800">Chỉ có văn bản</h4>
                <p class="text-sm text-blue-700 mt-1">
                  Không phát hiện bảng hoặc hình ảnh trong tài liệu.
                  Văn bản đã được tự động điền vào biểu mẫu.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Card>

    <!-- Image Preview Modal -->
    <div
      v-if="previewingImage"
      class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50"
      @click="previewingImage = null"
    >
      <div class="max-w-4xl max-h-[90vh] p-4" @click.stop>
        <img
          :src="previewingImage.url"
          :alt="previewingImage.caption"
          class="max-w-full max-h-full object-contain rounded-lg"
        />
        <p class="text-white text-center mt-2">
          {{ previewingImage.caption || "Hình ảnh" }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from "vue";
import Card from "@/components/ui/Card.vue";
import Button from "@/components/ui/Button.vue";
import { FileSearch, FileText } from "@/components/icons";
import { ocrService, type TableResult, type ImageResult } from "@/services/ocr";

// Table and Image icons (inline)
const TableIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M3 15h18"/><path d="M9 3v18"/></svg>`,
};

const ImageIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/></svg>`,
};

const props = defineProps<{
  caseData: any;
}>();

const emit = defineEmits<{
  "update:caseData": [any];
}>();

const previewingImage = ref<any>(null);
const tableJobLoading = ref(false);
const tables = ref<TableResult[]>([]);
const images = ref<ImageResult[]>([]);
const pollAttempts = ref(0);
const tableJobError = ref<string | null>(null);
const selectedPage = ref<number | null>(null); // null = show all pages
const selectedOcrFile = ref<string | null>(null); // Selected file for OCR display

// Polling cancellation tracking
let currentPollingJobId: string | null = null;
let pollAbortController: AbortController | null = null;

// Cleanup on unmount
onUnmounted(() => {
  if (pollAbortController) {
    console.log("🛑 Canceling table/image polling on unmount");
    pollAbortController.abort();
    pollAbortController = null;
  }
  currentPollingJobId = null;
});

// File selection from ocrResultsMap
const ocrResultsMap = computed(() => props.caseData?.ocrResultsMap || {});
const ocrFileNames = computed(() => Object.keys(ocrResultsMap.value));

// Initialize selectedOcrFile from caseData or default to first file
watch(ocrFileNames, (names) => {
  if (names.length > 0 && !selectedOcrFile.value) {
    selectedOcrFile.value = props.caseData?.currentOcrFile || names[0];
  }
}, { immediate: true });

const selectOcrFile = (fileName: string) => {
  selectedOcrFile.value = fileName;
  // Reset page filter when switching files
  selectedPage.value = null;
  // Load tables/images for the selected file
  const fileResult = ocrResultsMap.value[fileName];
  if (fileResult?.tables) tables.value = fileResult.tables;
  if (fileResult?.images) images.value = fileResult.images;
  // Re-poll if job is pending
  if (fileResult?.table_job_id && tables.value.length === 0 && images.value.length === 0) {
    pollTableImageJob(fileResult.table_job_id);
  }
};

// OCR data from selected file (or current file for backward compat)
const ocrData = computed(() => {
  if (selectedOcrFile.value && ocrResultsMap.value[selectedOcrFile.value]) {
    return ocrResultsMap.value[selectedOcrFile.value];
  }
  return props.caseData?.ocrResult || null;
});
const tableJobId = computed(() => ocrData.value?.table_job_id || null);
const tableJobSkipped = computed(() => ocrData.value?.table_job_status === "skipped");
const tableJobSkipReason = computed(() => ocrData.value?.table_job_reason || "");
const hasOCRResults = computed(
  () =>
    !!ocrData.value?.text || tables.value.length > 0 || images.value.length > 0 || ocrFileNames.value.length > 0
);

// Unique page numbers from tables + images
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

// Filtered tables based on selected page
const filteredTables = computed(() => {
  if (selectedPage.value === null) return tables.value;
  return tables.value.filter(t => t.page === selectedPage.value);
});

// Filtered images based on selected page
const filteredImages = computed(() => {
  if (selectedPage.value === null) return images.value;
  return images.value.filter(i => i.page === selectedPage.value);
});

// Helper to count items per page
const getPageItemCount = (page: number): number => {
  const tableCount = tables.value.filter(t => t.page === page).length;
  const imageCount = images.value.filter(i => i.page === page).length;
  return tableCount + imageCount;
};

// Start polling when table_job_id is present
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
  { immediate: true }
);

// Also check on mount
onMounted(() => {
  console.log("🔄 OCRResultsStep mounted");
  console.log("📊 ocrData:", ocrData.value);
  console.log("📊 tableJobId:", tableJobId.value);

  // Load any cached tables/images from caseData
  if (ocrData.value?.tables) {
    tables.value = ocrData.value.tables;
    console.log("📊 Loaded cached tables:", tables.value.length);
  }
  if (ocrData.value?.images) {
    images.value = ocrData.value.images;
    console.log("📊 Loaded cached images:", images.value.length);
  }

  // Explicitly start polling if job_id exists and no results yet
  if (
    tableJobId.value &&
    tables.value.length === 0 &&
    images.value.length === 0 &&
    !tableJobLoading.value &&
    !tableJobError.value
  ) {
    console.log("🚀 Starting polling on mount for job:", tableJobId.value);
    pollTableImageJob(tableJobId.value);
  }
});

const pollTableImageJob = async (jobId: string) => {
  // Cancel any existing polling for a different job
  if (currentPollingJobId && currentPollingJobId !== jobId) {
    console.log(`🛑 Canceling previous poll for job ${currentPollingJobId}`);
    if (pollAbortController) {
      pollAbortController.abort();
    }
  }

  // If already polling this exact job, skip
  if (currentPollingJobId === jobId && tableJobLoading.value) {
    console.log(`⏭️ Already polling job ${jobId}, skipping duplicate call`);
    return;
  }

  // Set up new polling
  currentPollingJobId = jobId;
  pollAbortController = new AbortController();
  const signal = pollAbortController.signal;

  tableJobLoading.value = true;
  tableJobError.value = null;
  pollAttempts.value = 0;

  try {
    console.log(`🔄 Starting poll for table/image job: ${jobId}`);

    // Custom polling with attempt tracking and cancellation
    const result = await new Promise<any>((resolve, reject) => {
      const startTime = Date.now();
      const timeoutMs = 300000; // 5 minutes
      const intervalMs = 3000; // 3 seconds

      const checkStatus = async () => {
        // Check if aborted
        if (signal.aborted) {
          reject(new Error("Polling was cancelled"));
          return;
        }

        // Check if job ID changed (new OCR started)
        if (currentPollingJobId !== jobId) {
          console.log(`⚠️ Job ID changed from ${jobId} to ${currentPollingJobId}, stopping old poll`);
          reject(new Error("Polling was cancelled - new job started"));
          return;
        }

        pollAttempts.value++;
        console.log(`📊 Poll attempt ${pollAttempts.value} for job ${jobId}`);

        try {
          if (Date.now() - startTime > timeoutMs) {
            reject(new Error("Quá thời gian chờ (5 phút). Vui lòng thử lại."));
            return;
          }

          const response = await fetch(`/api/ocr/jobs/${jobId}/`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
            signal, // Pass abort signal to fetch
          });
          const data = await response.json();

          console.log(`📊 Job status:`, data.status);

          if (data.status === "done" || data.status === "SUCCESS") {
            resolve(data);
          } else if (data.status === "failed" || data.status === "FAILURE") {
            reject(new Error(data.error || "Trích xuất thất bại"));
          } else {
            // Still running/queued, wait and retry
            setTimeout(checkStatus, intervalMs);
          }
        } catch (error: any) {
          // Handle abort gracefully
          if (error.name === "AbortError") {
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

    // Update caseData with results AND mark job as done
    const newData = { ...props.caseData };
    if (newData.ocrResult) {
      newData.ocrResult.tables = result.tables;
      newData.ocrResult.images = result.images;
      newData.ocrResult.table_job_status = "done"; // Unlock OCR button in AttachmentsStep
    }
    emit("update:caseData", newData);

    console.log(
      `✅ Job complete: ${result.tables.length} tables, ${result.images.length} images`
    );
  } catch (error: any) {
    // Handle cancellation gracefully (don't show error)
    if (error.message?.includes("cancelled") || error.name === "AbortError") {
      console.log(`🛑 Polling for job ${jobId} was cancelled`);
    } else {
      console.error("Table/image extraction failed:", error);
      tableJobError.value = error.message || "Lỗi không xác định";
    }
  } finally {
    // Only clear loading if this was the current job
    if (currentPollingJobId === jobId) {
      tableJobLoading.value = false;
      pollAbortController = null;
    }
  }
};

const retryTableImageExtraction = async () => {
  tableJobError.value = null;
  if (tableJobId.value) {
    await pollTableImageJob(tableJobId.value);
  }
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
  } catch (error) {
    console.error("Failed to copy:", error);
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
