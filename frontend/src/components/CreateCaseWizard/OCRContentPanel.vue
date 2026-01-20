<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <h3 class="text-lg font-semibold text-gray-900 flex items-center gap-2">
        📋 Dữ liệu OCR
      </h3>
      <span class="text-sm text-gray-500">
        {{ pages.length }} trang • {{ totalTableCells }} ô bảng
      </span>
    </div>

    <!-- Page Tabs -->
    <div v-if="pages.length > 1" class="flex gap-2 flex-wrap">
      <button
        v-for="page in pages"
        :key="page.page"
        @click="currentPageNum = page.page"
        :class="[
          'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
          currentPageNum === page.page
            ? 'bg-purple-500 text-white'
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
        ]"
      >
        Trang {{ page.page }}
      </button>
    </div>

    <!-- Tables Section -->
    <Card v-if="currentPage?.tables?.length > 0">
      <div class="p-4">
        <div class="flex items-center justify-between mb-3">
          <h4 class="font-medium text-gray-900 flex items-center gap-2">
            📊 Bảng dữ liệu
          </h4>
          <Button variant="outline" size="sm" @click="copyTables">
            📋 Copy
          </Button>
        </div>

        <div class="space-y-4">
          <div
            v-for="(table, idx) in currentPage.tables"
            :key="idx"
            class="border rounded-lg overflow-x-auto"
          >
            <div
              v-if="table.type === 'markdown'"
              class="prose prose-sm max-w-none p-3"
              v-html="renderMarkdown(table.content)"
            />
            <div v-else class="p-3 bg-gray-50 text-sm">
              <!-- Fallback for cell list -->
              <div class="flex flex-wrap gap-1">
                <span
                  v-for="(cell, cidx) in table.content"
                  :key="cidx"
                  class="px-2 py-0.5 bg-white border rounded text-xs"
                >
                  {{ cell }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Card>

    <!-- No Tables Message -->
    <div
      v-else-if="!currentPage?.tables?.length"
      class="text-center py-8 text-gray-500"
    >
      <span class="text-3xl mb-2 block">📊</span>
      <p>Không tìm thấy bảng dữ liệu trong trang này</p>
    </div>

    <!-- Original Image Section -->
    <Card>
      <div class="p-4">
        <div class="flex items-center justify-between mb-3">
          <h4 class="font-medium text-gray-900 flex items-center gap-2">
            🖼️ Hình ảnh gốc
          </h4>
        </div>

        <div v-if="currentPageImage" class="border rounded-lg overflow-hidden">
          <img
            :src="currentPageImage"
            alt="Original document"
            class="w-full h-auto"
          />
        </div>
        <div v-else class="text-center py-8 text-gray-400">
          <span class="text-3xl mb-2 block">🖼️</span>
          <p class="text-sm">Tải lên tệp để xem hình ảnh gốc</p>
        </div>
      </div>
    </Card>

    <!-- Plain Text Preview (collapsed by default) -->
    <Card>
      <div class="p-4">
        <button
          @click="showPlainText = !showPlainText"
          class="flex items-center justify-between w-full text-left"
        >
          <h4 class="font-medium text-gray-900 flex items-center gap-2">
            📄 Văn bản thuần (đã auto-fill)
          </h4>
          <span class="text-gray-400">{{ showPlainText ? "▼" : "▶" }}</span>
        </button>

        <div v-if="showPlainText" class="mt-3">
          <pre
            class="bg-gray-50 p-3 rounded-lg text-sm whitespace-pre-wrap font-mono overflow-x-auto max-h-64"
            >{{ currentPage?.plain_text || "Không có văn bản" }}</pre
          >
          <div class="mt-2 flex gap-2">
            <Button variant="outline" size="sm" @click="copyPlainText">
              📋 Copy văn bản
            </Button>
          </div>
        </div>
      </div>
    </Card>

    <!-- Confidence Score -->
    <div class="text-center text-sm text-gray-500">
      Độ tin cậy: {{ Math.round((currentPage?.confidence || 0) * 100) }}%
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import Card from "@/components/ui/Card.vue";
import Button from "@/components/ui/Button.vue";

interface TableData {
  type: "markdown" | "cells";
  content: string | string[];
}

interface PageResult {
  page: number;
  text?: string;
  plain_text?: string;
  tables?: TableData[];
  images?: any[];
  confidence?: number;
}

interface OCRResult {
  text?: string;
  pages?: PageResult[];
  structured?: any;
  metadata?: any;
}

const props = defineProps<{
  ocrResults: OCRResult | null;
  uploadedFiles?: any[];
}>();

const currentPageNum = ref(1);
const showPlainText = ref(false);

const pages = computed(() => props.ocrResults?.pages || []);

const currentPage = computed(
  () =>
    pages.value.find((p) => p.page === currentPageNum.value) || pages.value[0]
);

const currentPageImage = computed(() => {
  if (!props.uploadedFiles?.length) return null;
  // For multi-page PDFs, we'd need pdf.js to render specific pages
  // For now, show the first uploaded image
  const imageFile = props.uploadedFiles.find((f) =>
    f.type?.startsWith("image/")
  );
  return imageFile?.url || null;
});

const totalTableCells = computed(() => {
  let count = 0;
  for (const page of pages.value) {
    for (const table of page.tables || []) {
      if (table.type === "cells" && Array.isArray(table.content)) {
        count += table.content.length;
      } else if (table.type === "markdown") {
        // Count cells from markdown (rough estimate)
        const matches = (table.content as string).match(/\|/g);
        count += matches ? Math.floor(matches.length / 2) : 0;
      }
    }
  }
  return count;
});

const renderMarkdown = (markdown: string) => {
  // Simple markdown table to HTML conversion
  const lines = markdown.trim().split("\n");
  let html = '<table class="min-w-full divide-y divide-gray-200">';

  lines.forEach((line, idx) => {
    if (line.includes("|---")) return; // Skip separator row

    const cells = line.split("|").filter((c) => c.trim());
    const tag = idx === 0 ? "th" : "td";
    const rowClass =
      idx === 0 ? "bg-gray-100" : idx % 2 === 0 ? "bg-white" : "bg-gray-50";

    html += `<tr class="${rowClass}">`;
    cells.forEach((cell) => {
      const cellClass =
        tag === "th"
          ? "px-2 py-1 text-left text-xs font-medium text-gray-700 uppercase"
          : "px-2 py-1 text-sm text-gray-900";
      html += `<${tag} class="${cellClass}">${cell.trim()}</${tag}>`;
    });
    html += "</tr>";
  });

  html += "</table>";
  return html;
};

const copyTables = async () => {
  const tables = currentPage.value?.tables || [];
  let text = "";
  for (const table of tables) {
    if (table.type === "markdown") {
      text += table.content + "\n\n";
    } else if (Array.isArray(table.content)) {
      text += table.content.join("\t") + "\n";
    }
  }
  await navigator.clipboard.writeText(text);
  alert("Đã copy bảng vào clipboard!");
};

const copyPlainText = async () => {
  const text = currentPage.value?.plain_text || "";
  await navigator.clipboard.writeText(text);
  alert("Đã copy văn bản vào clipboard!");
};
</script>
