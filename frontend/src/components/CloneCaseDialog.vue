<template>
  <Dialog
    :visible="isOpen"
    @update:visible="close"
    modal
    :closable="true"
    :style="{ width: '32rem', maxWidth: '95vw' }"
    :contentStyle="{ overflowY: 'auto' }"
  >
    <template #header>
      <div class="flex items-center gap-2">
        <i class="pi pi-bookmark text-purple-600 text-xl" />
        <span class="text-xl font-bold text-gray-800">Lưu vào bộ sưu tập</span>
      </div>
    </template>

    <div class="flex flex-col gap-4">
      <div v-if="originalCase" class="bg-gray-50 p-4 rounded-lg">
        <div class="original-badge mb-3">
          <i class="pi pi-book me-2" />Hồ sơ mẫu của Giảng viên
        </div>
        <p class="text-sm text-gray-600 mb-1">
          <strong>Hồ sơ gốc:</strong> {{ originalCase.title }}
        </p>
        <p class="text-sm text-gray-600 mb-1">
          <strong>Chuyên khoa:</strong> {{ originalCase.specialty }}
        </p>
        <p v-if="getAuthorName(originalCase)" class="text-sm text-gray-600">
          <strong>Tác giả:</strong> {{ getAuthorName(originalCase) }}
        </p>
      </div>

      <div class="flex flex-col gap-1">
        <label for="clone-title" class="font-semibold text-gray-800 text-sm">
          Tiêu đề hồ sơ của bạn <span class="text-red-500">*</span>
        </label>
        <InputText
          id="clone-title"
          v-model="cloneData.title"
          placeholder="VD: Suy hô hấp cấp - Viêm phổi (Của tôi)"
          class="w-full"
        />
        <small class="text-gray-400"
          >Nhân bản sẽ tạo một bản sao hoàn toàn riêng của bạn</small
        >
      </div>

      <div class="flex flex-col gap-1">
        <label for="clone-summary" class="font-semibold text-gray-800 text-sm">
          Tóm tắt <span class="text-gray-400 font-normal">(tuỳ chọn)</span>
        </label>
        <Textarea
          id="clone-summary"
          v-model="cloneData.summary"
          rows="3"
          placeholder="Bạn có thể thay đổi tóm tắt nếu muốn"
          class="w-full"
        />
      </div>

      <div class="cloned-content-info">
        <h3
          class="text-sm font-semibold text-gray-800 mb-2 flex items-center gap-2"
        >
          <i class="pi pi-list text-purple-600" />
          Những gì sẽ được lưu vào bộ sưu tập:
        </h3>
        <ul class="flex flex-col gap-1">
          <li class="flex items-start gap-2 text-sm text-gray-600">
            <i class="pi pi-check-circle text-green-500 mt-0.5 shrink-0" />
            Toàn bộ nội dung hồ sơ mẫu (y nguyên)
          </li>
          <li class="flex items-start gap-2 text-sm text-gray-600">
            <i class="pi pi-check-circle text-green-500 mt-0.5 shrink-0" />
            Tất cả các phần y tế (lý do tới viện, tiền sử, khám lâm sàng, đánh
            giá, kế hoạch)
          </li>
          <li class="flex items-start gap-2 text-sm text-gray-600">
            <i class="pi pi-check-circle text-green-500 mt-0.5 shrink-0" />
            Tất cả các tệp đính kèm y tế
          </li>
          <li class="flex items-start gap-2 text-sm text-gray-600">
            <i class="pi pi-check-circle text-green-500 mt-0.5 shrink-0" />
            Tất cả các tham chiếu y tế
          </li>
          <li class="flex items-start gap-2 text-sm text-gray-600">
            <i class="pi pi-info-circle text-blue-500 mt-0.5 shrink-0" />
            <span
              ><strong>Quyền tác giả vẫn thuộc về giảng viên</strong> đã tạo hồ
              sơ gốc</span
            >
          </li>
          <li class="flex items-start gap-2 text-sm text-gray-600">
            <i class="pi pi-info-circle text-blue-500 mt-0.5 shrink-0" />
            Hồ sơ sẽ hiển thị trong mục "Hồ sơ đã lưu" của bạn
          </li>
        </ul>
      </div>

      <Message v-if="errorMessage" severity="error" :closable="false">
        {{ errorMessage }}
      </Message>
    </div>

    <template #footer>
      <div class="flex justify-end gap-3 w-full">
        <Button
          label="Huỷ bỏ"
          icon="pi pi-times"
          severity="secondary"
          outlined
          @click="close"
        />
        <Button
          icon="pi pi-download"
          :label="loading ? 'Đang lưu...' : 'Lưu vào bộ sưu tập'"
          :disabled="!isValidClone || loading"
          :loading="loading"
          @click="submitClone"
        />
      </div>
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { casesService } from "../services/cases";
import type { InstructorCase, CloneCaseRequest } from "../types/instructor";
import Dialog from "primevue/dialog";
import Button from "primevue/button";
import InputText from "primevue/inputtext";
import Textarea from "primevue/textarea";
import Message from "primevue/message";

interface Props {
  isOpen: boolean;
  caseId?: string | number;
  onClose?: () => void;
  onSuccess?: (clonedCase: any) => void;
}

const props = withDefaults(defineProps<Props>(), {
  isOpen: false,
});

const cloneData = ref<CloneCaseRequest & { summary?: string }>({
  title: "",
  summary: "",
});

const originalCase = ref<InstructorCase | null>(null);
const loading = ref(false);
const errorMessage = ref("");

const isValidClone = computed(() => cloneData.value.title?.trim() !== "");

watch(
  () => props.isOpen,
  async (newVal) => {
    if (newVal && props.caseId) {
      await loadCaseData();
      if (originalCase.value) {
        cloneData.value.title = `Copy of ${originalCase.value.title}`;
        cloneData.value.summary = originalCase.value.summary || "";
      }
    } else {
      resetForm();
    }
  },
);

const loadCaseData = async () => {
  try {
    if (!props.caseId) return;
    const caseData = await casesService.getCase(String(props.caseId));
    originalCase.value = caseData;
  } catch (error) {
    console.error("Error loading case data:", error);
    errorMessage.value = "Failed to load case information.";
  }
};

const getAuthorName = (caseData: any): string | null => {
  if (!caseData) return null;
  return (
    caseData.student_name ||
    caseData.created_by_name ||
    (caseData.student?.first_name && caseData.student?.last_name
      ? `${caseData.student.first_name} ${caseData.student.last_name}`
      : null) ||
    (caseData.created_by?.first_name && caseData.created_by?.last_name
      ? `${caseData.created_by.first_name} ${caseData.created_by.last_name}`
      : null)
  );
};

const submitClone = async () => {
  if (!isValidClone.value || loading.value || !props.caseId) return;

  errorMessage.value = "";
  loading.value = true;

  try {
    const submitData: CloneCaseRequest = {
      title: cloneData.value.title?.trim(),
    };

    if (
      cloneData.value.summary &&
      cloneData.value.summary !== originalCase.value?.summary
    ) {
      submitData.adjust_fields = {
        summary: cloneData.value.summary,
      };
    }

    const clonedCase = await casesService.cloneCase(props.caseId, submitData);

    if (props.onSuccess) {
      props.onSuccess(clonedCase);
    }

    close();
  } catch (error: any) {
    console.error("Error cloning case:", error);
    errorMessage.value =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      "Failed to clone case. Please try again.";
  } finally {
    loading.value = false;
  }
};

const resetForm = () => {
  cloneData.value = { title: "", summary: "" };
  originalCase.value = null;
  errorMessage.value = "";
  loading.value = false;
};

const close = () => {
  resetForm();
  if (props.onClose) {
    props.onClose();
  }
};

defineExpose({ close });
</script>

<style scoped>
.original-badge {
  display: inline-flex;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.cloned-content-info {
  background: linear-gradient(
    135deg,
    rgba(102, 126, 234, 0.08) 0%,
    rgba(118, 75, 162, 0.08) 100%
  );
  border-left: 4px solid #667eea;
  padding: 1rem;
  border-radius: 6px;
}
</style>
