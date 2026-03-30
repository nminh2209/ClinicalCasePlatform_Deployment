<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <h3 class="text-lg font-semibold text-gray-900">Dữ liệu OCR</h3>
      <span class="text-sm text-gray-500">
        {{ pages.length }} trang • {{ totalTableCells }} ô bảng
      </span>
    </div>

    <!-- Page Tabs -->
    <div v-if="pages.length > 1" class="flex gap-2 flex-wrap">
      <Button
        v-for="page in pages"
        :key="page.page"
        :label="`Trang ${page.page}`"
        size="small"
        :severity="currentPageNum === page.page ? undefined : 'secondary'"
        :outlined="currentPageNum !== page.page"
        @click="currentPageNum = page.page"
      />
    </div>

    <!-- Tables Section -->
    <Card v-if="currentPage?.tables && currentPage.tables.length > 0">
      <template #content>
        <div class="p-2">
          <div class="flex items-center justify-between mb-3">
            <h4 class="font-medium text-gray-900 flex items-center gap-2">
              <i class="pi pi-table" /> Bảng dữ liệu
            </h4>
            <Button
              icon="pi pi-clipboard"
              label="Copy"
              outlined
              severity="secondary"
              size="small"
              @click="copyTables"
            />
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
                v-html="renderMarkdown(table.content as string)"
              />
              <div v-else class="p-3 bg-gray-50 text-sm">
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
      </template>
    </Card>

    <!-- No Tables Message -->
    <div
      v-else-if="!currentPage?.tables?.length"
      class="text-center py-8 text-gray-500 flex flex-col items-center gap-2"
    >
      <i class="pi pi-table text-3xl text-gray-300" />
      <p>Không tìm thấy bảng dữ liệu trong trang này</p>
    </div>

    <!-- Original Image Section -->
    <Card>
      <template #content>
        <div class="p-2">
          <h4 class="font-medium text-gray-900 flex items-center gap-2 mb-3">
            <i class="pi pi-image" /> Hình ảnh gốc
          </h4>

          <div
            v-if="currentPageImage"
            class="border rounded-lg overflow-hidden"
          >
            <img
              :src="currentPageImage"
              alt="Original document"
              class="w-full h-auto"
            />
          </div>
          <div
            v-else
            class="text-center py-8 text-gray-400 flex flex-col items-center gap-2"
          >
            <i class="pi pi-image text-3xl" />
            <p class="text-sm">Tải lên tệp để xem hình ảnh gốc</p>
          </div>
        </div>
      </template>
    </Card>

    <!-- Plain Text (collapsed by default) -->
    <Card>
      <template #content>
        <div class="p-2">
          <button
            @click="showPlainText = !showPlainText"
            class="flex items-center justify-between w-full text-left"
          >
            <h4 class="font-medium text-gray-900 flex items-center gap-2">
              <i class="pi pi-file" /> Văn bản thuần (đã auto-fill)
            </h4>
            <i
              :class="
                showPlainText ? 'pi pi-chevron-down' : 'pi pi-chevron-right'
              "
              class="text-gray-400"
            />
          </button>

          <div v-if="showPlainText" class="mt-3">
            <pre
              class="bg-gray-50 p-3 rounded-lg text-sm whitespace-pre-wrap font-mono overflow-x-auto max-h-64"
              >{{ currentPage?.plain_text || "Không có văn bản" }}</pre
            >
            <div class="mt-2">
              <Button
                icon="pi pi-clipboard"
                label="Copy văn bản"
                outlined
                severity="secondary"
                size="small"
                @click="copyPlainText"
              />
            </div>
          </div>
        </div>
      </template>
    </Card>

    <!-- Confidence Score -->
    <div class="text-center text-sm text-gray-500">
      Độ tin cậy: {{ Math.round((currentPage?.confidence || 0) * 100) }}%
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import Card from "primevue/card";
import Button from "primevue/button";

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
    pages.value.find((p) => p.page === currentPageNum.value) || pages.value[0],
);

const currentPageImage = computed(() => {
  if (!props.uploadedFiles?.length) return null;
  const imageFile = props.uploadedFiles.find((f) =>
    f.type?.startsWith("image/"),
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
        const matches = (table.content as string).match(/\|/g);
        count += matches ? Math.floor(matches.length / 2) : 0;
      }
    }
  }
  return count;
});

const renderMarkdown = (markdown: string) => {
  const lines = markdown.trim().split("\n");
  let html = '<table class="min-w-full divide-y divide-gray-200">';
  lines.forEach((line, idx) => {
    if (line.includes("|---")) return;
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
