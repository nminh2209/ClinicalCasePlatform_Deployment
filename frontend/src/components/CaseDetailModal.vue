<template>
  <Dialog
    v-model:visible="dialogVisible"
    :header="caseData?.title || 'Chi tiết bệnh án'"
    :style="{ width: '900px', maxWidth: '95vw' }"
    :maximizable="true"
    :modal="true"
    :draggable="false"
    content-style="padding: 0; display: flex; flex-direction: column; max-height: 80vh;"
    @hide="close"
  >
    <div v-if="loading" class="state-container">
      <ProgressSpinner style="width: 48px; height: 48px" />
      <span class="state-text">Đang tải...</span>
    </div>

    <div v-else-if="error" class="state-container">
      <span class="error-text">{{ error }}</span>
    </div>

    <div v-else-if="caseData" class="modal-body">
      <section class="info-section">
        <h3>Thông tin bệnh nhân</h3>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">Tên bệnh nhân:</span>
            <span class="value">{{ caseData.patient_name }}</span>
          </div>
          <div class="info-item">
            <span class="label">Tuổi:</span>
            <span class="value">{{ caseData.patient_age }}</span>
          </div>
          <div class="info-item">
            <span class="label">Giới tính:</span>
            <span class="value">{{
              formatGender(caseData.patient_gender)
            }}</span>
          </div>
          <div class="info-item">
            <span class="label">Mã hồ sơ:</span>
            <span class="value">{{ caseData.medical_record_number }}</span>
          </div>
          <div class="info-item">
            <span class="label">Ngày nhập viện:</span>
            <span class="value">{{ formatDate(caseData.admission_date) }}</span>
          </div>
          <div class="info-item">
            <span class="label">Ngày xuất viện:</span>
            <span class="value">{{ formatDate(caseData.discharge_date) }}</span>
          </div>
        </div>
      </section>

      <section class="info-section">
        <h3>Thông tin ca bệnh</h3>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">Chuyên khoa:</span>
            <span class="value">{{ caseData.specialty }}</span>
          </div>
          <div class="info-item">
            <span class="label">Sinh viên:</span>
            <span class="value">{{ caseData.student?.full_name }}</span>
          </div>
          <div class="info-item">
            <span class="label">Khoa:</span>
            <span class="value">{{ caseData.student?.department_name }}</span>
          </div>
          <div class="info-item">
            <span class="label">Người duyệt:</span>
            <span class="value">{{ caseData.published_by?.full_name }}</span>
          </div>
        </div>
      </section>

      <section class="info-section" v-if="caseData.case_summary">
        <h3>Tóm tắt ca bệnh</h3>
        <p class="text-content">{{ caseData.case_summary }}</p>
      </section>

      <section class="info-section" v-if="caseData.chief_complaint_brief">
        <h3>Lý do khám</h3>
        <p class="text-content">{{ caseData.chief_complaint_brief }}</p>
      </section>

      <section class="info-section" v-if="caseData.keywords">
        <h3>Từ khóa</h3>
        <p class="text-content">{{ caseData.keywords }}</p>
      </section>

      <section
        class="info-section"
        v-if="caseData.clinical_history?.chief_complaint"
      >
        <h3>Lý do khám</h3>
        <p class="text-content">
          {{ caseData.clinical_history.chief_complaint }}
        </p>
      </section>

      <section
        class="info-section"
        v-if="caseData.clinical_history?.present_illness"
      >
        <h3>Bệnh sử hiện tại</h3>
        <p class="text-content">
          {{ caseData.clinical_history.present_illness }}
        </p>
      </section>

      <section
        class="info-section"
        v-if="caseData.clinical_history?.past_medical"
      >
        <h3>Tiền sử bệnh</h3>
        <p class="text-content">{{ caseData.clinical_history.past_medical }}</p>
      </section>

      <section
        class="info-section"
        v-if="caseData.clinical_history?.family_history"
      >
        <h3>Tiền sử gia đình</h3>
        <p class="text-content">
          {{ caseData.clinical_history.family_history }}
        </p>
      </section>

      <section
        class="info-section"
        v-if="caseData.clinical_history?.social_history"
      >
        <h3>Tiền sử xã hội</h3>
        <p class="text-content">
          {{ caseData.clinical_history.social_history }}
        </p>
      </section>

      <section
        class="info-section"
        v-if="caseData.clinical_history?.review_of_systems"
      >
        <h3>Khám hệ thống</h3>
        <p class="text-content">
          {{ caseData.clinical_history.review_of_systems }}
        </p>
      </section>

      <section class="info-section" v-if="caseData.clinical_history?.allergies">
        <h3>Dị ứng</h3>
        <p class="text-content">{{ caseData.clinical_history.allergies }}</p>
      </section>

      <section
        class="info-section"
        v-if="caseData.clinical_history?.current_medications"
      >
        <h3>Thuốc hiện tại</h3>
        <p class="text-content">
          {{ caseData.clinical_history.current_medications }}
        </p>
      </section>

      <section
        class="info-section"
        v-if="caseData.physical_examination?.vital_signs"
      >
        <h3>Sinh hiệu</h3>
        <p class="text-content">
          {{ caseData.physical_examination.vital_signs }}
        </p>
      </section>

      <section
        class="info-section"
        v-if="caseData.physical_examination?.general_appearance"
      >
        <h3>Diện mạo chung</h3>
        <p class="text-content">
          {{ caseData.physical_examination.general_appearance }}
        </p>
      </section>

      <section
        class="info-section"
        v-if="caseData.physical_examination?.system_examination"
      >
        <h3>Khám hệ cơ quan</h3>
        <p class="text-content">
          {{ caseData.physical_examination.system_examination }}
        </p>
      </section>

      <section
        class="info-section"
        v-if="caseData.detailed_investigations?.lab_tests"
      >
        <h3>Kết quả xét nghiệm</h3>
        <p class="text-content">
          {{ caseData.detailed_investigations.lab_tests }}
        </p>
      </section>

      <section
        class="info-section"
        v-if="caseData.detailed_investigations?.imaging_studies"
      >
        <h3>Chẩn đoán hình ảnh</h3>
        <p class="text-content">
          {{ caseData.detailed_investigations.imaging_studies }}
        </p>
      </section>

      <section
        class="info-section"
        v-if="caseData.detailed_investigations?.special_tests"
      >
        <h3>Xét nghiệm đặc biệt</h3>
        <p class="text-content">
          {{ caseData.detailed_investigations.special_tests }}
        </p>
      </section>

      <section
        class="info-section"
        v-if="caseData.diagnosis_management?.primary_diagnosis"
      >
        <h3>Chẩn đoán chính</h3>
        <p class="text-content">
          {{ caseData.diagnosis_management.primary_diagnosis }}
        </p>
      </section>

      <section
        class="info-section"
        v-if="caseData.diagnosis_management?.differential_diagnosis"
      >
        <h3>Chẩn đoán phân biệt</h3>
        <p class="text-content">
          {{ caseData.diagnosis_management.differential_diagnosis }}
        </p>
      </section>

      <section
        class="info-section"
        v-if="caseData.diagnosis_management?.treatment_plan"
      >
        <h3>Kế hoạch điều trị</h3>
        <p class="text-content">
          {{ caseData.diagnosis_management.treatment_plan }}
        </p>
      </section>

      <section
        class="info-section"
        v-if="caseData.diagnosis_management?.clinical_progress"
      >
        <h3>Diễn biến lâm sàng</h3>
        <p class="text-content">
          {{ caseData.diagnosis_management.clinical_progress }}
        </p>
      </section>

      <section
        class="info-section"
        v-if="caseData.diagnosis_management?.discharge_summary"
      >
        <h3>Tóm tắt xuất viện</h3>
        <p class="text-content">
          {{ caseData.diagnosis_management.discharge_summary }}
        </p>
      </section>

      <section
        class="info-section"
        v-if="caseData.diagnosis_management?.follow_up_plan"
      >
        <h3>Kế hoạch theo dõi</h3>
        <p class="text-content">
          {{ caseData.diagnosis_management.follow_up_plan }}
        </p>
      </section>

      <section
        class="info-section"
        v-if="caseData.learning_outcomes?.learning_points"
      >
        <h3>Điểm học tập</h3>
        <p class="text-content">
          {{ caseData.learning_outcomes.learning_points }}
        </p>
      </section>

      <section
        class="info-section"
        v-if="caseData.learning_outcomes?.key_concepts"
      >
        <h3>Khái niệm chính</h3>
        <p class="text-content">
          {{ caseData.learning_outcomes.key_concepts }}
        </p>
      </section>

      <section
        class="info-section"
        v-if="caseData.learning_outcomes?.references"
      >
        <h3>Tài liệu tham khảo</h3>
        <p class="text-content">{{ caseData.learning_outcomes.references }}</p>
      </section>

      <section
        class="info-section student-notes-section"
        v-if="caseData.student_notes"
      >
        <h3 class="section-title">
          <i class="pi pi-pencil section-icon"></i> Ghi chú của sinh viên
        </h3>
        <div
          v-if="caseData.student_notes.clinical_assessment"
          class="note-subsection"
        >
          <h4>Đánh giá lâm sàng</h4>
          <p class="text-content">
            {{ caseData.student_notes.clinical_assessment }}
          </p>
        </div>
        <div
          v-if="caseData.student_notes.differential_diagnosis"
          class="note-subsection"
        >
          <h4>Chẩn đoán phân biệt</h4>
          <p class="text-content">
            {{ caseData.student_notes.differential_diagnosis }}
          </p>
        </div>
        <div
          v-if="caseData.student_notes.treatment_plan"
          class="note-subsection"
        >
          <h4>Kế hoạch điều trị</h4>
          <p class="text-content">
            {{ caseData.student_notes.treatment_plan }}
          </p>
        </div>
        <div
          v-if="caseData.student_notes.learning_reflections"
          class="note-subsection"
        >
          <h4>Suy ngẫm học tập</h4>
          <p class="text-content">
            {{ caseData.student_notes.learning_reflections }}
          </p>
        </div>
        <div
          v-if="caseData.student_notes.questions_for_instructor"
          class="note-subsection"
        >
          <h4>Câu hỏi cho giảng viên</h4>
          <p class="text-content">
            {{ caseData.student_notes.questions_for_instructor }}
          </p>
        </div>
        <div
          v-if="caseData.student_notes.challenges_faced"
          class="note-subsection"
        >
          <h4>Thử thách gặp phải</h4>
          <p class="text-content">
            {{ caseData.student_notes.challenges_faced }}
          </p>
        </div>
        <div
          v-if="caseData.student_notes.resources_used"
          class="note-subsection"
        >
          <h4>Tài liệu đã sử dụng</h4>
          <p class="text-content">
            {{ caseData.student_notes.resources_used }}
          </p>
        </div>
      </section>

      <section
        class="info-section"
        v-if="caseData.medical_attachments?.length > 0"
      >
        <h3>
          <i class="pi pi-paperclip section-icon"></i> Tệp đính kèm ({{
            caseData.medical_attachments.length
          }})
        </h3>
        <div class="attachments-list">
          <div
            v-for="attachment in caseData.medical_attachments"
            :key="attachment.id"
            class="attachment-item"
          >
            <div class="attachment-icon">
              <i
                v-if="attachment.file_type?.includes('pdf')"
                class="pi pi-file-pdf"
              ></i>
              <i
                v-else-if="attachment.file_type?.includes('image')"
                class="pi pi-image"
              ></i>
              <i v-else class="pi pi-file"></i>
            </div>
            <div class="attachment-info">
              <div class="attachment-title">{{ attachment.title }}</div>
              <div class="attachment-meta">
                <span class="attachment-type">{{
                  attachment.attachment_type_display ||
                  attachment.attachment_type
                }}</span>
                <span v-if="attachment.file_size" class="attachment-size">{{
                  formatFileSize(attachment.file_size)
                }}</span>
                <span
                  v-if="attachment.uploaded_by_name"
                  class="attachment-uploader"
                  >{{ attachment.uploaded_by_name }}</span
                >
              </div>
              <div v-if="attachment.description" class="attachment-description">
                {{ attachment.description }}
              </div>
            </div>
            <div class="attachment-actions">
              <Button
                as="a"
                :href="getFileUrl(attachment.file)"
                target="_blank"
                icon="pi pi-download"
                size="small"
                title="Tải xuống"
              />
            </div>
          </div>
        </div>
      </section>

      <section class="info-section">
        <h3>Bình luận ({{ comments.length }})</h3>
        <div class="comments-list">
          <div
            v-for="comment in comments"
            :key="comment.id"
            class="comment-item"
          >
            <div class="comment-header">
              <strong>{{ comment.author_name || "Ẩn danh" }}</strong>
              <span class="comment-time">{{
                formatCommentDate(comment.created_at)
              }}</span>
            </div>
            <p class="comment-content">{{ comment.content }}</p>
          </div>
          <div v-if="comments.length === 0" class="no-comments">
            Chưa có bình luận nào
          </div>
        </div>

        <div class="add-comment">
          <Textarea
            v-model="newComment"
            placeholder="Viết bình luận..."
            rows="3"
            class="w-full"
            auto-resize
          />
          <Button
            label="Gửi bình luận"
            icon="pi pi-send"
            :disabled="!newComment.trim()"
            @click="submitComment"
            class="align-self-end"
          />
        </div>
      </section>
    </div>

    <template #footer>
      <Button
        :label="exportingPDF ? 'Đang tạo PDF...' : 'Xuất PDF'"
        icon="pi pi-file-pdf"
        :loading="exportingPDF"
        :disabled="exportingPDF"
        @click="exportPDF"
      />
      <Button
        label="Đóng"
        icon="pi pi-times"
        severity="secondary"
        @click="close"
      />
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, watch, computed } from "vue";
import Dialog from "primevue/dialog";
import Button from "primevue/button";
import Textarea from "primevue/textarea";
import ProgressSpinner from "primevue/progressspinner";
import api from "@/services/api";
import { useToast } from "@/composables/useToast";

interface Props {
  caseId: number | null;
  isOpen: boolean;
}

const props = defineProps<Props>();
const emit = defineEmits(["close", "refresh"]);

const { toast } = useToast();

const caseData = ref<any>(null);
const comments = ref<any[]>([]);
const loading = ref(false);
const error = ref("");
const newComment = ref("");
const exportingPDF = ref(false);

const dialogVisible = computed({
  get: () => props.isOpen,
  set: (val) => {
    if (!val) emit("close");
  },
});

watch(
  () => props.isOpen,
  async (isOpen) => {
    if (isOpen && props.caseId) {
      caseData.value = null;
      comments.value = [];
      await loadCaseDetails();
      await loadComments();
    } else {
      resetModal();
    }
  },
);

watch(
  () => props.caseId,
  async (newCaseId, oldCaseId) => {
    if (props.isOpen && newCaseId && newCaseId !== oldCaseId) {
      caseData.value = null;
      comments.value = [];
      await loadCaseDetails();
      await loadComments();
    }
  },
);

const loadCaseDetails = async () => {
  loading.value = true;
  error.value = "";
  try {
    const response = await api.get(`/cases/${props.caseId}/`);
    caseData.value = response.data;
    console.log("📋 Case data loaded:", response.data);
    console.log(
      "📎 Attachments:",
      response.data.medical_attachments?.length || 0,
    );
    console.log("📝 Has clinical_history:", !!response.data.clinical_history);
    console.log(
      "🔬 Has physical_examination:",
      !!response.data.physical_examination,
    );
    console.log(
      "🧪 Has detailed_investigations:",
      !!response.data.detailed_investigations,
    );
    console.log(
      "💊 Has diagnosis_management:",
      !!response.data.diagnosis_management,
    );
    console.log("📚 Has learning_outcomes:", !!response.data.learning_outcomes);
  } catch (err: any) {
    error.value = "Không thể tải chi tiết bệnh án";
    console.error("Failed to load case details:", err);
  } finally {
    loading.value = false;
  }
};

const loadComments = async () => {
  if (!props.caseId) {
    console.warn("Cannot load comments: caseId is null");
    return;
  }
  try {
    const response = await api.get(
      `/comments/?case=${props.caseId}&is_reaction=false`,
    );
    const loadedComments = response.data.results || response.data;
    comments.value = Array.isArray(loadedComments) ? loadedComments : [];
  } catch {
    comments.value = [];
  }
};

const submitComment = async () => {
  if (!newComment.value.trim()) return;
  try {
    await api.post(`/comments/`, {
      case: props.caseId,
      content: newComment.value,
      is_reaction: false,
    });
    newComment.value = "";
    await loadComments();
    emit("refresh");
    toast.success("Đã gửi bình luận");
  } catch (err: any) {
    toast.error("Không thể gửi bình luận");
    console.error("Failed to submit comment:", err);
  }
};

const close = () => emit("close");

const resetModal = () => {
  caseData.value = null;
  comments.value = [];
  newComment.value = "";
  error.value = "";
};

const formatGender = (gender: string) => {
  const map: Record<string, string> = {
    male: "Nam",
    female: "Nữ",
    other: "Khác",
  };
  return map[gender] || gender;
};

const formatDate = (dateString: string) => {
  if (!dateString) return "N/A";
  return new Date(dateString).toLocaleDateString("vi-VN");
};

const formatCommentDate = (dateString: string) => {
  const date = new Date(dateString);
  const diff = Date.now() - date.getTime();
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const days = Math.floor(hours / 24);
  if (hours < 1) return "Vừa xong";
  if (hours < 24) return `${hours} giờ trước`;
  if (days < 7) return `${days} ngày trước`;
  return date.toLocaleDateString("vi-VN");
};

const formatFileSize = (bytes: number): string => {
  if (!bytes) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i];
};

const getFileUrl = (filePath: string): string => {
  if (filePath.startsWith("http")) return filePath;
  const baseUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
  return `${baseUrl}${filePath}`;
};

const exportPDF = async () => {
  if (!props.caseId) return;
  exportingPDF.value = true;
  try {
    const response = await api.get(`/cases/${props.caseId}/export_pdf/`, {
      responseType: "blob",
    });
    const blob = new Blob([response.data], { type: "application/pdf" });
    const url = window.URL.createObjectURL(blob);
    window.open(url, "_blank");
    setTimeout(() => window.URL.revokeObjectURL(url), 100);
    toast.success("Đã mở PDF trong tab mới!");
  } catch (err: any) {
    console.error("PDF export failed:", err);
    toast.error("Không thể tạo PDF. Vui lòng thử lại.");
  } finally {
    exportingPDF.value = false;
  }
};
</script>

<style scoped>
.state-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px;
  gap: 16px;
}

.state-text {
  font-size: 14px;
  color: #6b7280;
}

.error-text {
  font-size: 14px;
  color: #ef4444;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.info-section {
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.info-section:last-child {
  border-bottom: none;
}

.info-section h3 {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 16px 0;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.label {
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
}

.value {
  font-size: 14px;
  color: #111827;
}

.text-content {
  font-size: 14px;
  line-height: 1.6;
  color: #374151;
  white-space: pre-wrap;
  margin: 0;
}

/* Student Notes */
.student-notes-section {
  background: #f9fafb;
  border-radius: 8px;
  padding: 20px !important;
}

.student-notes-section .section-title {
  color: #1f2937;
  margin-bottom: 20px;
}

.note-subsection {
  margin-bottom: 16px;
  padding: 12px;
  background: white;
  border-radius: 6px;
  border-left: 3px solid #3b82f6;
}

.note-subsection:last-child {
  margin-bottom: 0;
}

.note-subsection h4 {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 8px 0;
}

/* Comments */
.comments-list {
  margin-bottom: 20px;
}

.comment-item {
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
  margin-bottom: 12px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.comment-header strong {
  font-size: 14px;
  color: #111827;
}

.comment-time {
  font-size: 12px;
  color: #6b7280;
}

.comment-content {
  font-size: 14px;
  color: #374151;
  margin: 0;
  white-space: pre-wrap;
}

.no-comments {
  text-align: center;
  padding: 20px;
  color: #9ca3af;
  font-size: 14px;
}

.add-comment {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Attachments */
.attachments-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.attachment-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  transition: all 0.2s;
}

.attachment-item:hover {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.attachment-icon {
  font-size: 20px;
  flex-shrink: 0;
  color: #6b7280;
  display: flex;
  align-items: center;
  padding-top: 2px;
}

.section-icon {
  font-size: 15px;
  vertical-align: middle;
  margin-right: 2px;
}

.attachment-info {
  flex: 1;
  min-width: 0;
}

.attachment-title {
  font-weight: 500;
  color: #111827;
  margin-bottom: 4px;
  word-break: break-word;
}

.attachment-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 4px;
}

.attachment-type {
  padding: 2px 8px;
  background: #dbeafe;
  color: #1e40af;
  border-radius: 4px;
  text-transform: capitalize;
}

.attachment-size,
.attachment-uploader {
  padding: 2px 8px;
  background: #f3f4f6;
  border-radius: 4px;
}

.attachment-description {
  font-size: 13px;
  color: #6b7280;
  margin-top: 4px;
  line-height: 1.4;
}

.attachment-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>
