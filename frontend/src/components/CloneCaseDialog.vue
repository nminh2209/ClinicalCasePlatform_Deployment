<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="close">
    <div class="modal-dialog">
      <div class="modal-header">
        <h2>� Lưu vào bộ sưu tập</h2>
        <button type="button" @click="close" class="modal-close-btn">✕</button>
      </div>

      <div class="modal-body">
        <div v-if="originalCase" class="original-case-info">
          <div class="original-badge">📚 Hồ sơ mẫu của Giảng viên</div>
          <p><strong>Hồ sơ gốc:</strong> {{ originalCase.title }}</p>
          <p><strong>Chuyên khoa:</strong> {{ originalCase.specialty }}</p>
          <p v-if="getAuthorName(originalCase)">
            <strong>Tác giả:</strong> {{ getAuthorName(originalCase) }}
          </p>
        </div>

        <form @submit.prevent="submitClone" class="clone-form">
          <!-- Title -->
          <div class="form-group">
            <label for="title">Tiêu đề hồ sơ của bạn *</label>
            <input id="title" v-model="cloneData.title" type="text" class="form-input"
              placeholder="VD: Suy hô hấp cấp - Viêm phổi (Của tôi)" required />
            <small>Nhân bản sẽ tạo một bản sao hoàn toàn riêng của bạn</small>
          </div>

          <!-- Summary -->
          <div class="form-group">
            <label for="summary">Tóm tắt (tuỳ chọn)</label>
            <textarea id="summary" v-model="cloneData.summary" class="form-textarea" rows="3"
              placeholder="Bạn có thể thay đổi tóm tắt nếu muốn"></textarea>
          </div>

          <!-- What will be saved -->
          <div class="cloned-content-info">
            <h3>📋 Những gì sẽ được lưu vào bộ sưu tập:</h3>
            <ul>
              <li>✅ Toàn bộ nội dung hồ sơ mẫu (y nguyên)</li>
              <li>✅ Tất cả các phần y tế (lý do tới viện, tiền sử, khám lâm sàng, đánh giá, kế hoạch)</li>
              <li>✅ Tất cả các tệp đính kèm y tế</li>
              <li>✅ Tất cả các tham chiếu y tế</li>
              <li>ℹ️ <strong>Quyền tác giả vẫn thuộc về giảng viên</strong> đã tạo hồ sơ gốc</li>
              <li>ℹ️ Hồ sơ sẽ hiển thị trong mục "Hồ sơ đã lưu" của bạn</li>
            </ul>
          </div>

          <!-- Error Message -->
          <div v-if="errorMessage" class="alert alert-error">
            {{ errorMessage }}
          </div>

          <!-- Actions -->
          <div class="modal-actions">
            <button type="button" @click="close" class="btn btn-outline">
              Huỷ bỏ
            </button>
            <button type="submit" class="btn btn-primary" :disabled="!isValidClone || loading">
              {{ loading ? "Đang lưu..." : "📥 Lưu vào bộ sưu tập" }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { casesService } from "../services/cases";
import type { InstructorCase, CloneCaseRequest } from "../types/instructor";

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

const isValidClone = computed(() => {
  return cloneData.value.title?.trim() !== "";
});

watch(
  () => props.isOpen,
  async (newVal) => {
    if (newVal && props.caseId) {
      await loadCaseData();
      // Pre-fill title with "Copy of" prefix
      if (originalCase.value) {
        cloneData.value.title = `Copy of ${originalCase.value.title}`;
        cloneData.value.summary = originalCase.value.summary || "";
      }
    } else {
      resetForm();
    }
  }
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

// Helper to get author name from different possible sources
const getAuthorName = (caseData: any): string | null => {
  if (!caseData) return null;
  return caseData.student_name || 
         caseData.created_by_name || 
         (caseData.student?.first_name && caseData.student?.last_name 
           ? `${caseData.student.first_name} ${caseData.student.last_name}` 
           : null) ||
         (caseData.created_by?.first_name && caseData.created_by?.last_name 
           ? `${caseData.created_by.first_name} ${caseData.created_by.last_name}` 
           : null);
};

const submitClone = async () => {
  if (!isValidClone.value || loading.value || !props.caseId) return;

  errorMessage.value = "";
  loading.value = true;

  try {
    const submitData: CloneCaseRequest = {
      title: cloneData.value.title?.trim(),
    };

    // Include summary if provided and different from original
    if (cloneData.value.summary && cloneData.value.summary !== originalCase.value?.summary) {
      submitData.adjust_fields = {
        summary: cloneData.value.summary,
      };
    }

    const clonedCase = await casesService.cloneCase(props.caseId, submitData);

    // Call success callback
    if (props.onSuccess) {
      props.onSuccess(clonedCase);
    }

    // Close modal
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
  cloneData.value = {
    title: "",
    summary: "",
  };
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

defineExpose({
  close,
});
</script>

<style scoped lang="css">
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-dialog {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.3rem;
  color: #333;
}

.modal-close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 1.5rem;
}

.original-case-info {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.original-badge {
  display: inline-block;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.original-case-info p {
  margin: 0.5rem 0;
  color: #555;
}

.clone-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #333;
  font-size: 0.95rem;
}

.form-input,
.form-textarea {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-family: inherit;
  font-size: 0.95rem;
  transition: border-color 0.2s;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

small {
  color: #999;
  font-size: 0.85rem;
}

.cloned-content-info {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  border-left: 4px solid #667eea;
  padding: 1rem;
  border-radius: 6px;
  margin: 1rem 0;
}

.cloned-content-info h3 {
  margin: 0 0 0.75rem;
  font-size: 0.95rem;
  color: #333;
}

.cloned-content-info ul {
  margin: 0;
  padding-left: 1.25rem;
  list-style: none;
}

.cloned-content-info li {
  margin: 0.4rem 0;
  color: #555;
  font-size: 0.9rem;
}

.alert {
  padding: 1rem;
  border-radius: 6px;
  font-size: 0.9rem;
}

.alert-error {
  background: #fee;
  border: 1px solid #fcc;
  color: #c33;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #eee;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-outline {
  background: transparent;
  border: 2px solid #ddd;
  color: #333;
}

.btn-outline:hover:not(:disabled) {
  border-color: #667eea;
  color: #667eea;
}
</style>
