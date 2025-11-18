<template>
  <div v-if="isOpen" class="modal-overlay" @click="close">
    <div class="modal-container" @click.stop>
      <div class="modal-header">
        <h2>{{ caseData?.title || 'Chi tiết bệnh án' }}</h2>
        <button @click="close" class="close-btn">×</button>
      </div>

      <div v-if="loading" class="modal-body">
        <div class="loading">Đang tải...</div>
      </div>

      <div v-else-if="error" class="modal-body">
        <div class="error">{{ error }}</div>
      </div>

      <div v-else-if="caseData" class="modal-body">
        <!-- Patient Info -->
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
              <span class="value">{{ formatGender(caseData.patient_gender) }}</span>
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

        <!-- Case Info -->
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

        <!-- Case Summary (if available) -->
        <section class="info-section" v-if="caseData.case_summary">
          <h3>Tóm tắt ca bệnh</h3>
          <p class="text-content">{{ caseData.case_summary }}</p>
        </section>

        <!-- Chief Complaint Brief (direct field) -->
        <section class="info-section" v-if="caseData.chief_complaint_brief">
          <h3>Lý do khám</h3>
          <p class="text-content">{{ caseData.chief_complaint_brief }}</p>
        </section>

        <!-- Keywords (if available) -->
        <section class="info-section" v-if="caseData.keywords">
          <h3>Từ khóa</h3>
          <p class="text-content">{{ caseData.keywords }}</p>
        </section>

        <!-- Chief Complaint -->
        <section class="info-section" v-if="caseData.clinical_history?.chief_complaint">
          <h3>Lý do khám</h3>
          <p class="text-content">{{ caseData.clinical_history.chief_complaint }}</p>
        </section>

        <!-- Present Illness -->
        <section class="info-section" v-if="caseData.clinical_history?.present_illness">
          <h3>Bệnh sử hiện tại</h3>
          <p class="text-content">{{ caseData.clinical_history.present_illness }}</p>
        </section>

        <!-- Past Medical History -->
        <section class="info-section" v-if="caseData.clinical_history?.past_medical">
          <h3>Tiền sử bệnh</h3>
          <p class="text-content">{{ caseData.clinical_history.past_medical }}</p>
        </section>

        <!-- Family History -->
        <section class="info-section" v-if="caseData.clinical_history?.family_history">
          <h3>Tiền sử gia đình</h3>
          <p class="text-content">{{ caseData.clinical_history.family_history }}</p>
        </section>

        <!-- Social History -->
        <section class="info-section" v-if="caseData.clinical_history?.social_history">
          <h3>Tiền sử xã hội</h3>
          <p class="text-content">{{ caseData.clinical_history.social_history }}</p>
        </section>

        <!-- Review of Systems -->
        <section class="info-section" v-if="caseData.clinical_history?.review_of_systems">
          <h3>Khám hệ thống</h3>
          <p class="text-content">{{ caseData.clinical_history.review_of_systems }}</p>
        </section>

        <!-- Allergies -->
        <section class="info-section" v-if="caseData.clinical_history?.allergies">
          <h3>Dị ứng</h3>
          <p class="text-content">{{ caseData.clinical_history.allergies }}</p>
        </section>

        <!-- Current Medications -->
        <section class="info-section" v-if="caseData.clinical_history?.current_medications">
          <h3>Thuốc hiện tại</h3>
          <p class="text-content">{{ caseData.clinical_history.current_medications }}</p>
        </section>

        <!-- Vital Signs -->
        <section class="info-section" v-if="caseData.physical_examination?.vital_signs">
          <h3>Sinh hiệu</h3>
          <p class="text-content">{{ caseData.physical_examination.vital_signs }}</p>
        </section>

        <!-- General Appearance -->
        <section class="info-section" v-if="caseData.physical_examination?.general_appearance">
          <h3>Diện mạo chung</h3>
          <p class="text-content">{{ caseData.physical_examination.general_appearance }}</p>
        </section>

        <!-- System Examination -->
        <section class="info-section" v-if="caseData.physical_examination?.system_examination">
          <h3>Khám hệ cơ quan</h3>
          <p class="text-content">{{ caseData.physical_examination.system_examination }}</p>
        </section>

        <!-- Lab Results -->
        <section class="info-section" v-if="caseData.detailed_investigations?.lab_tests">
          <h3>Kết quả xét nghiệm</h3>
          <p class="text-content">{{ caseData.detailed_investigations.lab_tests }}</p>
        </section>

        <!-- Imaging Results -->
        <section class="info-section" v-if="caseData.detailed_investigations?.imaging_studies">
          <h3>Chẩn đoán hình ảnh</h3>
          <p class="text-content">{{ caseData.detailed_investigations.imaging_studies }}</p>
        </section>

        <!-- Special Tests -->
        <section class="info-section" v-if="caseData.detailed_investigations?.special_tests">
          <h3>Xét nghiệm đặc biệt</h3>
          <p class="text-content">{{ caseData.detailed_investigations.special_tests }}</p>
        </section>

        <!-- Diagnosis -->
        <section class="info-section" v-if="caseData.diagnosis_management?.primary_diagnosis">
          <h3>Chẩn đoán chính</h3>
          <p class="text-content">{{ caseData.diagnosis_management.primary_diagnosis }}</p>
        </section>

        <!-- Differential Diagnosis -->
        <section class="info-section" v-if="caseData.diagnosis_management?.differential_diagnosis">
          <h3>Chẩn đoán phân biệt</h3>
          <p class="text-content">{{ caseData.diagnosis_management.differential_diagnosis }}</p>
        </section>

        <!-- Treatment Plan -->
        <section class="info-section" v-if="caseData.diagnosis_management?.treatment_plan">
          <h3>Kế hoạch điều trị</h3>
          <p class="text-content">{{ caseData.diagnosis_management.treatment_plan }}</p>
        </section>

        <!-- Clinical Progress -->
        <section class="info-section" v-if="caseData.diagnosis_management?.clinical_progress">
          <h3>Diễn biến lâm sàng</h3>
          <p class="text-content">{{ caseData.diagnosis_management.clinical_progress }}</p>
        </section>

        <!-- Discharge Summary -->
        <section class="info-section" v-if="caseData.diagnosis_management?.discharge_summary">
          <h3>Tóm tắt xuất viện</h3>
          <p class="text-content">{{ caseData.diagnosis_management.discharge_summary }}</p>
        </section>

        <!-- Follow-up Plan -->
        <section class="info-section" v-if="caseData.diagnosis_management?.follow_up_plan">
          <h3>Kế hoạch theo dõi</h3>
          <p class="text-content">{{ caseData.diagnosis_management.follow_up_plan }}</p>
        </section>

        <!-- Learning Points -->
        <section class="info-section" v-if="caseData.learning_outcomes?.learning_points">
          <h3>Điểm học tập</h3>
          <p class="text-content">{{ caseData.learning_outcomes.learning_points }}</p>
        </section>

        <!-- Key Concepts -->
        <section class="info-section" v-if="caseData.learning_outcomes?.key_concepts">
          <h3>Khái niệm chính</h3>
          <p class="text-content">{{ caseData.learning_outcomes.key_concepts }}</p>
        </section>

        <!-- References -->
        <section class="info-section" v-if="caseData.learning_outcomes?.references">
          <h3>Tài liệu tham khảo</h3>
          <p class="text-content">{{ caseData.learning_outcomes.references }}</p>
        </section>

        <!-- Student Notes Section -->
        <section class="info-section student-notes-section" v-if="caseData.student_notes">
          <h3 class="section-title">📝 Ghi chú của sinh viên</h3>
          
          <!-- Clinical Assessment -->
          <div v-if="caseData.student_notes.clinical_assessment" class="note-subsection">
            <h4>Đánh giá lâm sàng</h4>
            <p class="text-content">{{ caseData.student_notes.clinical_assessment }}</p>
          </div>

          <!-- Differential Diagnosis -->
          <div v-if="caseData.student_notes.differential_diagnosis" class="note-subsection">
            <h4>Chẩn đoán phân biệt</h4>
            <p class="text-content">{{ caseData.student_notes.differential_diagnosis }}</p>
          </div>

          <!-- Treatment Plan -->
          <div v-if="caseData.student_notes.treatment_plan" class="note-subsection">
            <h4>Kế hoạch điều trị</h4>
            <p class="text-content">{{ caseData.student_notes.treatment_plan }}</p>
          </div>

          <!-- Learning Reflections -->
          <div v-if="caseData.student_notes.learning_reflections" class="note-subsection">
            <h4>Suy ngẫm học tập</h4>
            <p class="text-content">{{ caseData.student_notes.learning_reflections }}</p>
          </div>

          <!-- Questions for Instructor -->
          <div v-if="caseData.student_notes.questions_for_instructor" class="note-subsection">
            <h4>Câu hỏi cho giảng viên</h4>
            <p class="text-content">{{ caseData.student_notes.questions_for_instructor }}</p>
          </div>

          <!-- Challenges Faced -->
          <div v-if="caseData.student_notes.challenges_faced" class="note-subsection">
            <h4>Thử thách gặp phải</h4>
            <p class="text-content">{{ caseData.student_notes.challenges_faced }}</p>
          </div>

          <!-- Resources Used -->
          <div v-if="caseData.student_notes.resources_used" class="note-subsection">
            <h4>Tài liệu đã sử dụng</h4>
            <p class="text-content">{{ caseData.student_notes.resources_used }}</p>
          </div>
        </section>

        <!-- Comments Section -->
        <section class="info-section">
          <h3>Bình luận ({{ comments.length }})</h3>
          <div class="comments-list">
            <div v-for="comment in comments" :key="comment.id" class="comment-item">
              <div class="comment-header">
                <strong>{{ comment.author_name || 'Ẩn danh' }}</strong>
                <span class="comment-time">{{ formatCommentDate(comment.created_at) }}</span>
              </div>
              <p class="comment-content">{{ comment.content }}</p>
            </div>
            <div v-if="comments.length === 0" class="no-comments">
              Chưa có bình luận nào
            </div>
          </div>

          <!-- Add Comment Form -->
          <div class="add-comment">
            <textarea 
              v-model="newComment" 
              placeholder="Viết bình luận..."
              rows="3"
              class="comment-input"
            ></textarea>
            <button @click="submitComment" :disabled="!newComment.trim()" class="submit-btn">
              Gửi bình luận
            </button>
          </div>
        </section>
      </div>

      <div class="modal-footer">
        <button @click="close" class="btn-secondary">Đóng</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import api from '@/services/api';
import { useToast } from '@/composables/useToast';

interface Props {
  caseId: number | null;
  isOpen: boolean;
}

const props = defineProps<Props>();
const emit = defineEmits(['close', 'refresh']);

const { toast } = useToast();

const caseData = ref<any>(null);
const comments = ref<any[]>([]);
const loading = ref(false);
const error = ref('');
const newComment = ref('');

watch(() => props.isOpen, async (isOpen) => {
  if (isOpen && props.caseId) {
    // Clear old data first
    caseData.value = null;
    comments.value = [];
    await loadCaseDetails();
    await loadComments();
  } else {
    resetModal();
  }
});

// Watch for case ID changes while modal is open
watch(() => props.caseId, async (newCaseId, oldCaseId) => {
  if (props.isOpen && newCaseId && newCaseId !== oldCaseId) {
    // Clear old data first
    caseData.value = null;
    comments.value = [];
    await loadCaseDetails();
    await loadComments();
  }
});

const loadCaseDetails = async () => {
  loading.value = true;
  error.value = '';
  try {
    // Use the public feed endpoint which includes all necessary fields
    const response = await api.get(`/cases/public-feed/${props.caseId}/`);
    caseData.value = response.data;
    console.log('📋 Case data loaded:', response.data);
    console.log('📝 Has clinical_history:', !!response.data.clinical_history);
    console.log('🔬 Has physical_examination:', !!response.data.physical_examination);
    console.log('🧪 Has detailed_investigations:', !!response.data.detailed_investigations);
    console.log('💊 Has diagnosis_management:', !!response.data.diagnosis_management);
    console.log('📚 Has learning_outcomes:', !!response.data.learning_outcomes);
  } catch (err: any) {
    error.value = 'Không thể tải chi tiết bệnh án';
    console.error('Failed to load case details:', err);
  } finally {
    loading.value = false;
  }
};

const loadComments = async () => {
  if (!props.caseId) {
    console.warn('Cannot load comments: caseId is null');
    return;
  }
  
  try {
    console.log(`💬 Loading comments for case ${props.caseId}...`);
    // Filter comments by case_id and exclude reactions
    const response = await api.get(`/comments/?case=${props.caseId}&is_reaction=false`);
    const loadedComments = response.data.results || response.data;
    
    // Extra safety: filter by case ID on frontend too
    const filteredComments = Array.isArray(loadedComments) 
      ? loadedComments.filter(c => c.case === props.caseId)
      : [];
    
    comments.value = filteredComments;
    console.log(`✅ Loaded ${filteredComments.length} comments for case ${props.caseId}`);
  } catch (err: any) {
    console.error('Failed to load comments:', err);
    comments.value = [];
  }
};

const submitComment = async () => {
  if (!newComment.value.trim()) return;

  try {
    await api.post(`/comments/`, {
      case: props.caseId,
      content: newComment.value,
      is_reaction: false
    });
    newComment.value = '';
    await loadComments();
    emit('refresh');
    toast.success('Đã gửi bình luận');
  } catch (err: any) {
    toast.error('Không thể gửi bình luận');
    console.error('Failed to submit comment:', err);
  }
};

const close = () => {
  emit('close');
};

const resetModal = () => {
  caseData.value = null;
  comments.value = [];
  newComment.value = '';
  error.value = '';
};

const formatGender = (gender: string) => {
  const map: Record<string, string> = {
    male: 'Nam',
    female: 'Nữ',
    other: 'Khác'
  };
  return map[gender] || gender;
};

const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('vi-VN');
};

const formatCommentDate = (dateString: string) => {
  const date = new Date(dateString);
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const days = Math.floor(hours / 24);

  if (hours < 1) return 'Vừa xong';
  if (hours < 24) return `${hours} giờ trước`;
  if (days < 7) return `${days} ngày trước`;

  return date.toLocaleDateString('vi-VN');
};
</script>

<style scoped>
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
  padding: 20px;
}

.modal-container {
  background: white;
  border-radius: 12px;
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #111827;
}

.close-btn {
  background: none;
  border: none;
  font-size: 32px;
  color: #6b7280;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #f3f4f6;
  color: #111827;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.loading,
.error {
  text-align: center;
  padding: 40px;
  color: #6b7280;
}

.error {
  color: #ef4444;
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

.note-subsection .text-content {
  margin: 0;
}

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

.comment-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
}

.comment-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.submit-btn {
  align-self: flex-end;
  padding: 10px 20px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background: #2563eb;
}

.submit-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn-secondary {
  padding: 10px 20px;
  background: #f3f4f6;
  color: #374151;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

@media (max-width: 768px) {
  .modal-overlay {
    padding: 0;
  }

  .modal-container {
    max-height: 100vh;
    border-radius: 0;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>
