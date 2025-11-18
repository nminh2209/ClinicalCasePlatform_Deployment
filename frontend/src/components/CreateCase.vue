<template>
  <div class="create-case">
    <header class="create-header">
      <div class="container">
        <div class="header-content">
          <h1>Tạo hồ sơ bệnh án mới</h1>
          <div class="header-actions">
            <button @click="saveDraft" class="btn btn-outline" :disabled="saving">
              {{ saving ? 'Đang lưu...' : 'Lưu bản nháp' }}
            </button>
            <button @click="submitCase" class="btn btn-primary" :disabled="!isValid || saving">
              Nộp hồ sơ
            </button>
          </div>
        </div>
      </div>
    </header>

    <main class="create-main">
      <div class="container">
        <form @submit.prevent="submitCase" class="case-form">

          <!-- Basic Information -->
          <section class="form-section">
            <h2>🏥 Thông tin cơ bản</h2>
            <div class="form-grid">
              <div class="form-group">
                <label for="title">Tiêu đề hồ sơ *</label>
                <input id="title" v-model="caseData.title" type="text" class="form-input"
                  placeholder="VD: Suy hô hấp cấp - Viêm phổi - HSTC" required />
              </div>

              <div class="form-group">
                <label for="specialty">Chuyên khoa *</label>
                <select id="specialty" v-model="caseData.specialty" class="form-select" required>
                  <option value="">Chọn chuyên khoa</option>
                  <option value="Hồi sức tích cực">Hồi sức tích cực</option>
                  <option value="Tim mạch">Tim mạch</option>
                  <option value="Nội khoa">Nội khoa</option>
                  <option value="Phẫu thuật">Phẫu thuật</option>
                  <option value="Hô hấp">Hô hấp</option>
                  <option value="Tiêu hóa">Tiêu hóa</option>
                  <option value="Thần kinh">Thần kinh</option>
                  <option value="Sản phụ khoa">Sản phụ khoa</option>
                  <option value="Nhi khoa">Nhi khoa</option>
                  <option value="Khác">Khác</option>
                </select>
              </div>
            </div>
          </section>

          <!-- Patient Information -->
          <section class="form-section">
            <h2>👤 Thông tin bệnh nhân</h2>
            <div class="form-grid">
              <div class="form-group">
                <label for="patient_name">Tên bệnh nhân (ẩn danh) *</label>
                <input id="patient_name" v-model="caseData.patient_name" type="text" class="form-input"
                  placeholder="VD: NGUYỄN HỒNG ĐIỆP (ẩn danh)" required />
              </div>

              <div class="form-group">
                <label for="patient_age">Tuổi *</label>
                <input id="patient_age" v-model.number="caseData.patient_age" type="number" class="form-input" min="0"
                  max="120" required />
              </div>

              <div class="form-group">
                <label for="patient_gender">Giới tính *</label>
                <select id="patient_gender" v-model="caseData.patient_gender" class="form-select" required>
                  <option value="">Chọn giới tính</option>
                  <option value="male">Nam</option>
                  <option value="female">Nữ</option>
                  <option value="other">Khác</option>
                </select>
              </div>

              <div class="form-group">
                <label for="medical_record_number">Số hồ sơ bệnh án</label>
                <input id="medical_record_number" v-model="caseData.medical_record_number" type="text"
                  class="form-input" placeholder="VD: HST001" />
              </div>
            </div>
          </section>

          <!-- Clinical History -->
          <section class="form-section clinical-section">
            <h2>📋 Tiền sử lâm sàng</h2>

            <div class="form-group">
              <label for="chief_complaint">Lý do khám chính *</label>
              <textarea id="chief_complaint" v-model="caseData.clinical_history.chief_complaint" class="form-textarea"
                rows="2" placeholder="VD: Khó thở" required></textarea>
            </div>

            <div class="form-group">
              <label for="history_present_illness">Bệnh sử hiện tại *</label>
              <textarea id="history_present_illness" v-model="caseData.clinical_history.history_present_illness"
                class="form-textarea" rows="6" placeholder="Mô tả chi tiết quá trình khởi phát và diễn biến bệnh..."
                required></textarea>
            </div>

            <div class="form-group">
              <label for="past_medical_history">Tiền sử bệnh tật</label>
              <textarea id="past_medical_history" v-model="caseData.clinical_history.past_medical_history"
                class="form-textarea" rows="3" placeholder="Các bệnh đã mắc trước đây..."></textarea>
            </div>

            <div class="form-group">
              <label for="family_history">Tiền sử gia đình</label>
              <textarea id="family_history" v-model="caseData.clinical_history.family_history" class="form-textarea"
                rows="2" placeholder="Bệnh di truyền, bệnh gia đình..."></textarea>
            </div>

            <div class="form-group">
              <label for="medications">Thuốc đang sử dụng</label>
              <textarea id="medications" v-model="caseData.clinical_history.medications" class="form-textarea" rows="2"
                placeholder="Các thuốc đang dùng..."></textarea>
            </div>

            <div class="form-group">
              <label for="allergies">Dị ứng</label>
              <textarea id="allergies" v-model="caseData.clinical_history.allergies" class="form-textarea" rows="2"
                placeholder="Dị ứng thuốc, thực phẩm..."></textarea>
            </div>
          </section>

          <!-- Physical Examination -->
          <section class="form-section clinical-section">
            <h2>🩺 Khám lâm sàng</h2>

            <div class="form-group">
              <label for="general_appearance">Tình trạng chung *</label>
              <textarea id="general_appearance" v-model="caseData.physical_examination.general_appearance"
                class="form-textarea" rows="3" placeholder="Tình trạng ý thức, thể trạng chung..." required></textarea>
            </div>

            <div class="form-group">
              <label for="vital_signs">Sinh hiệu *</label>
              <textarea id="vital_signs" v-model="caseData.physical_examination.vital_signs" class="form-textarea"
                rows="3" placeholder="Nhiệt độ, mạch, huyết áp, nhịp thở, SpO2..." required></textarea>
            </div>

            <div class="form-group">
              <label for="cardiovascular">Tim mạch</label>
              <textarea id="cardiovascular" v-model="caseData.physical_examination.cardiovascular" class="form-textarea"
                rows="4" placeholder="Khám tim: nhịp tim, tiếng tim, thổi..."></textarea>
            </div>

            <div class="form-group">
              <label for="respiratory">Hô hấp</label>
              <textarea id="respiratory" v-model="caseData.physical_examination.respiratory" class="form-textarea"
                rows="4" placeholder="Khám phổi: nhịp thở, ran, thở máy..."></textarea>
            </div>

            <div class="form-group">
              <label for="abdominal">Bụng</label>
              <textarea id="abdominal" v-model="caseData.physical_examination.abdominal" class="form-textarea" rows="3"
                placeholder="Khám bụng: mềm, chướng, gan lách..."></textarea>
            </div>

            <div class="form-group">
              <label for="neurological">Thần kinh</label>
              <textarea id="neurological" v-model="caseData.physical_examination.neurological" class="form-textarea"
                rows="3" placeholder="Khám thần kinh: ý thức, phản xạ, vận động..."></textarea>
            </div>
          </section>

          <!-- Investigations -->
          <section class="form-section clinical-section">
            <h2>🧪 Cận lâm sàng</h2>

            <div class="form-group">
              <label for="laboratory_results">Xét nghiệm</label>
              <textarea id="laboratory_results" v-model="caseData.investigations.laboratory_results"
                class="form-textarea" rows="4" placeholder="Khí máu, bilan nhiễm trùng, sinh hóa..."></textarea>
            </div>

            <div class="form-group">
              <label for="imaging_studies">Chẩn đoán hình ảnh</label>
              <textarea id="imaging_studies" v-model="caseData.investigations.imaging_studies" class="form-textarea"
                rows="4" placeholder="X-quang, CT, siêu âm, MRI..."></textarea>
            </div>

            <div class="form-group">
              <label for="ecg_findings">Điện tâm đồ</label>
              <textarea id="ecg_findings" v-model="caseData.investigations.ecg_findings" class="form-textarea" rows="3"
                placeholder="Kết quả điện tâm đồ..."></textarea>
            </div>

            <div class="form-group">
              <label for="biochemistry">Sinh hóa</label>
              <textarea id="biochemistry" v-model="caseData.investigations.biochemistry" class="form-textarea" rows="3"
                placeholder="NT-proBNP, enzim gan, creatinin..."></textarea>
            </div>

            <div class="form-group">
              <label for="hematology">Huyết học</label>
              <textarea id="hematology" v-model="caseData.investigations.hematology" class="form-textarea" rows="3"
                placeholder="Công thức máu, đông cầm máu..."></textarea>
            </div>
          </section>

          <!-- Diagnosis and Management -->
          <section class="form-section clinical-section">
            <h2>💊 Chẩn đoán và điều trị</h2>

            <div class="form-group">
              <label for="primary_diagnosis">Chẩn đoán chính *</label>
              <textarea id="primary_diagnosis" v-model="caseData.diagnosis_management.primary_diagnosis"
                class="form-textarea" rows="3" placeholder="VD: Suy hô hấp cấp mức độ nặng - Viêm phổi nặng..."
                required></textarea>
            </div>

            <div class="form-group">
              <label for="differential_diagnosis">Chẩn đoán phân biệt</label>
              <textarea id="differential_diagnosis" v-model="caseData.diagnosis_management.differential_diagnosis"
                class="form-textarea" rows="3" placeholder="Các chẩn đoán cần loại trừ..."></textarea>
            </div>

            <div class="form-group">
              <label for="treatment_plan">Kế hoạch điều trị *</label>
              <textarea id="treatment_plan" v-model="caseData.diagnosis_management.treatment_plan" class="form-textarea"
                rows="5" placeholder="Hỗ trợ hô hấp, kháng sinh, điều trị nguyên nhân..." required></textarea>
            </div>

            <div class="form-group">
              <label for="medications_prescribed">Thuốc kê đơn</label>
              <textarea id="medications_prescribed" v-model="caseData.diagnosis_management.medications_prescribed"
                class="form-textarea" rows="3" placeholder="Danh sách thuốc được kê..."></textarea>
            </div>

            <div class="form-group">
              <label for="procedures_performed">Thủ thuật thực hiện</label>
              <textarea id="procedures_performed" v-model="caseData.diagnosis_management.procedures_performed"
                class="form-textarea" rows="3" placeholder="Các thủ thuật đã thực hiện..."></textarea>
            </div>

            <div class="form-group">
              <label for="prognosis">Tiên lượng</label>
              <textarea id="prognosis" v-model="caseData.diagnosis_management.prognosis" class="form-textarea" rows="2"
                placeholder="Tiên lượng bệnh..."></textarea>
            </div>
          </section>

          <!-- Learning Outcomes -->
          <section class="form-section clinical-section">
            <h2>🎯 Mục tiêu học tập</h2>

            <div class="form-group">
              <label for="learning_objectives">Mục tiêu học tập *</label>
              <textarea id="learning_objectives" v-model="caseData.learning_outcomes.learning_objectives"
                class="form-textarea" rows="4" placeholder="Những mục tiêu học tập chính từ ca bệnh này..."
                required></textarea>
            </div>

            <div class="form-group">
              <label for="key_concepts">Khái niệm chính</label>
              <textarea id="key_concepts" v-model="caseData.learning_outcomes.key_concepts" class="form-textarea"
                rows="3" placeholder="Các khái niệm y học quan trọng..."></textarea>
            </div>

            <div class="form-group">
              <label for="clinical_pearls">Điểm lâm sàng quan trọng</label>
              <textarea id="clinical_pearls" v-model="caseData.learning_outcomes.clinical_pearls" class="form-textarea"
                rows="3" placeholder="Những điểm lâm sàng đáng chú ý..."></textarea>
            </div>

            <div class="form-group">
              <label for="discussion_points">Điểm thảo luận</label>
              <textarea id="discussion_points" v-model="caseData.learning_outcomes.discussion_points"
                class="form-textarea" rows="3" placeholder="Các câu hỏi thảo luận..."></textarea>
            </div>

            <div class="form-group">
              <label for="references">Tài liệu tham khảo</label>
              <textarea id="references" v-model="caseData.learning_outcomes.references" class="form-textarea" rows="3"
                placeholder="Tài liệu tham khảo liên quan..."></textarea>
            </div>
          </section>

          <!-- Medical Attachments -->
          <section class="form-section clinical-section">
            <h2>📁 Tài liệu đính kèm y tế</h2>

            <!-- Upload Area -->
            <div class="upload-area" :class="{ 'dragover': isDragOver }" @dragover.prevent="handleDragOver"
              @dragleave.prevent="handleDragLeave" @drop.prevent="handleDrop">

              <div class="upload-content">
                <div class="upload-icon">
                  <i class="fas fa-cloud-upload-alt"></i>
                </div>
                <h3>Thêm tài liệu y tế</h3>
                <p>Kéo thả tệp vào đây hoặc click để chọn</p>
                <input ref="fileInput" type="file" multiple accept=".jpg,.jpeg,.png,.pdf,.doc,.docx,.dcm,.zip,.rar"
                  @change="handleFileSelect" class="file-input">
                <button type="button" @click="openFileDialog" class="btn btn-outline">
                  <i class="fas fa-plus"></i> Chọn tệp
                </button>
              </div>

              <div class="file-types">
                <small>Hỗ trợ: JPG, PNG, PDF, DOC, DOCX, DICOM, ZIP, RAR (Max: 50MB mỗi tệp)</small>
              </div>
            </div>

            <!-- Selected Files List -->
            <div v-if="attachments.length > 0" class="attachments-list">
              <h4>Tệp đã chọn ({{ attachments.length }})</h4>

              <div class="attachment-item" v-for="(attachment, index) in attachments" :key="index">
                <div class="attachment-preview">
                  <div class="attachment-icon">
                    <i :class="getFileIcon(attachment.file)"></i>
                  </div>

                  <div class="attachment-info">
                    <div class="file-name">{{ attachment.file.name }}</div>
                    <div class="file-size">{{ formatFileSize(attachment.file.size) }}</div>
                  </div>
                </div>

                <div class="attachment-metadata">
                  <!-- Attachment Type -->
                  <div class="metadata-field">
                    <label>Loại tài liệu:</label>
                    <select v-model="attachment.attachment_type" required>
                      <option value="">-- Chọn loại --</option>
                      <option value="x_ray">📷 Ảnh chụp X-quang</option>
                      <option value="lab_report">🧪 Phiếu xét nghiệm</option>
                      <option value="ct_scan">🔬 Chụp CT/Scanner</option>
                      <option value="mri_scan">🧠 Chụp MRI</option>
                      <option value="ultrasound">📡 Siêu âm</option>
                      <option value="injury_photo">📸 Ảnh chụp chấn thương</option>
                      <option value="surgical_photo">⚕️ Ảnh phẫu thuật</option>
                      <option value="pathology_slide">🔬 Tiêu bản bệnh học</option>
                      <option value="prescription">💊 Đơn thuốc</option>
                      <option value="discharge_summary">📋 Tóm tắt xuất viện</option>
                      <option value="vital_signs">💓 Dấu hiệu sinh tồn</option>
                      <option value="ekg_ecg">❤️ Điện tâm đồ</option>
                      <option value="endoscopy">🔍 Nội soi</option>
                      <option value="biopsy_report">🧬 Kết quả sinh thiết</option>
                      <option value="medical_certificate">📜 Giấy chứng nhận y tế</option>
                      <option value="other">📄 Khác</option>
                    </select>
                  </div>

                  <!-- Title -->
                  <div class="metadata-field">
                    <label>Tiêu đề:</label>
                    <input v-model="attachment.title" type="text" placeholder="Nhập tiêu đề mô tả..." required>
                  </div>

                  <!-- Description -->
                  <div class="metadata-field">
                    <label>Mô tả:</label>
                    <textarea v-model="attachment.description" rows="2"
                      placeholder="Mô tả chi tiết về tài liệu..."></textarea>
                  </div>

                  <!-- Date Taken -->
                  <div class="metadata-field">
                    <label>Ngày thực hiện:</label>
                    <input v-model="attachment.date_taken" type="date">
                  </div>

                  <!-- Physician Notes -->
                  <div class="metadata-field">
                    <label>Ghi chú bác sĩ:</label>
                    <textarea v-model="attachment.physician_notes" rows="2"
                      placeholder="Ghi chú của bác sĩ về tài liệu..."></textarea>
                  </div>

                  <!-- Confidential -->
                  <div class="metadata-field checkbox-field">
                    <label class="checkbox-label">
                      <input type="checkbox" v-model="attachment.is_confidential">
                      <i class="fas fa-lock"></i> Tài liệu bảo mật (chỉ giảng viên xem được)
                    </label>
                  </div>
                </div>

                <!-- Remove Button -->
                <button type="button" @click="removeAttachment(index)" class="remove-btn">
                  <i class="fas fa-times"></i>
                </button>
              </div>
            </div>
          </section>

          <!-- Keywords and Tags -->
          <section class="form-section">
            <h2>🏷️ Từ khóa và phân loại</h2>
            <div class="form-group">
              <label for="keywords">Từ khóa</label>
              <input id="keywords" v-model="caseData.keywords" type="text" class="form-input"
                placeholder="VD: suy hô hấp, viêm phổi, thở máy, HSTC" />
              <small class="form-help">Phân cách bằng dấu phẩy để dễ tìm kiếm</small>
            </div>
          </section>

        </form>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
// import Badge from '@/components/ui/Badge.vue';
// import Button from '@/components/ui/Button.vue';
// import Card from '@/components/ui/Card.vue';
// import CardHeader from '@/components/ui/CardHeader.vue';
// import CardTitle from '@/components/ui/CardTitle.vue';
// import CardDescription from '@/components/ui/CardDescription.vue';
// import CardContent from '@/components/ui/CardContent.vue';
// import Input from '@/components/ui/Input.vue';
// import Tabs from '@/components/ui/Tabs.vue';
// import TabsList from '@/components/ui/TabsList.vue';
// import TabsTrigger from '@/components/ui/TabsTrigger.vue';
// import TabsContent from '@/components/ui/TabsContent.vue';
// import Textarea from '@/components/ui/Textarea.vue';
// import Toast from '@/components/ui/Toast.vue';
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCasesStore } from '@/stores/cases'
import { casesService } from '@/services/cases'

const router = useRouter()
const authStore = useAuthStore()
const casesStore = useCasesStore()

const saving = ref(false)

// Medical attachments data
const attachments = ref<Array<{
  file: File,
  attachment_type: string,
  title: string,
  description?: string,
  date_taken?: string,
  physician_notes?: string,
  is_confidential: boolean
}>>([])
const isDragOver = ref(false)
const fileInput = ref(<HTMLInputElement | null>(null))

type CaseData = {
  title: string
  specialty: string
  patient_name: string
  patient_age: number | string | null
  patient_gender: string
  medical_record_number: string
  keywords: string
  template: any
  repository: number | null
  clinical_history: Record<string, any>
  physical_examination: Record<string, any>
  investigations: Record<string, any>
  diagnosis_management: Record<string, any>
  learning_outcomes: Record<string, any>
}

const caseData = ref<CaseData>({
  title: '',
  specialty: '',
  patient_name: '',
  patient_age: '',
  patient_gender: '',
  medical_record_number: '',
  keywords: '',
  template: null,
  repository: null,
  // Detailed medical sections
  clinical_history: {
    chief_complaint: '',
    history_present_illness: '',
    past_medical_history: '',
    family_history: '',
    social_history: '',
    allergies: '',
    medications: '',
    review_systems: ''
  },
  physical_examination: {
    general_appearance: '',
    vital_signs: '',
    head_neck: '',
    cardiovascular: '',
    respiratory: '',
    abdominal: '',
    neurological: '',
    musculoskeletal: '',
    skin: '',
    other_findings: ''
  },
  investigations: {
    laboratory_results: '',
    imaging_studies: '',
    ecg_findings: '',
    special_tests: '',
    biochemistry: '',
    hematology: '',
    microbiology: ''
  },
  diagnosis_management: {
    primary_diagnosis: '',
    differential_diagnosis: '',
    treatment_plan: '',
    medications_prescribed: '',
    procedures_performed: '',
    follow_up_plan: '',
    prognosis: '',
    complications: ''
  },
  learning_outcomes: {
    learning_objectives: '',
    key_concepts: '',
    clinical_pearls: '',
    references: '',
    discussion_points: '',
    assessment_criteria: ''
  }
})

const repositories = ref<Array<{ id: number, name: string }>>([])
const templates = ref([])

const isValid = computed(() => {
  return caseData.value.title &&
    caseData.value.specialty &&
    caseData.value.patient_name &&
    caseData.value.patient_age &&
    caseData.value.patient_gender &&
    caseData.value.clinical_history.chief_complaint &&
    caseData.value.clinical_history.history_present_illness &&
    caseData.value.physical_examination.general_appearance &&
    caseData.value.physical_examination.vital_signs &&
    caseData.value.diagnosis_management.primary_diagnosis &&
    caseData.value.diagnosis_management.treatment_plan &&
    caseData.value.learning_outcomes.learning_objectives &&
    caseData.value.repository
})

async function saveDraft() {
  if (!caseData.value.title || !caseData.value.repository) {
    alert('Vui lòng nhập tiêu đề hồ sơ và chọn kho lưu trữ')
    return
  }

  saving.value = true
  try {
    const payload = prepareCasePayload('draft')
    const createdCase = await casesStore.createCase(payload)

    // Upload attachments if any
    if (attachments.value.length > 0) {
      await uploadAttachments(createdCase.id)
    }

    alert('Đã lưu bản nháp thành công!')
    router.push('/cases')
  } catch (error: any) {
    console.error('Error saving draft:', error)
    alert('Có lỗi xảy ra khi lưu bản nháp: ' + (error.response?.data?.detail || error.message))
  } finally {
    saving.value = false
  }
}

async function submitCase() {
  if (!isValid.value) {
    alert('Vui lòng điền đầy đủ thông tin bắt buộc')
    return
  }

  // Validate attachments metadata
  for (let i = 0; i < attachments.value.length; i++) {
    const attachment = attachments.value[i]
    if (!attachment?.attachment_type || !attachment.title) {
      alert(`Vui lòng điền đầy đủ thông tin cho tệp "${attachment?.file.name}" (loại tài liệu và tiêu đề)`)
      return
    }
  }

  saving.value = true
  try {
    const payload = prepareCasePayload('submitted')
    const createdCase = await casesStore.createCase(payload)

    // Upload attachments if any
    if (attachments.value.length > 0) {
      await uploadAttachments(createdCase.id)
    }

    alert('Đã nộp hồ sơ bệnh án thành công!')
    router.push('/cases')
  } catch (error: any) {
    console.error('Error submitting case:', error)
    alert('Có lỗi xảy ra khi nộp hồ sơ: ' + (error.response?.data?.detail || error.message))
  } finally {
    saving.value = false
  }
}

async function uploadAttachments(caseId: string) {
  const uploadPromises = attachments.value.map(async (attachment) => {
    try {
      const formData = new FormData()
      formData.append('file', attachment.file)
      formData.append('attachment_type', attachment.attachment_type)
      formData.append('title', attachment.title)
      formData.append('description', attachment.description || '')
      formData.append('physician_notes', attachment.physician_notes || '')
      formData.append('is_confidential', `${attachment.is_confidential}`)

      if (attachment.date_taken) {
        formData.append('date_taken', attachment.date_taken)
      }

      await casesService.uploadAttachment(caseId, formData)
    } catch (error: any) {
      console.error(`Error uploading ${attachment.file.name}:`, error)
      throw new Error(`Lỗi khi tải lên tệp "${attachment.file.name}": ${error.response?.data?.message || error.message}`)
    }
  })

  await Promise.all(uploadPromises)
}

function prepareCasePayload(status: string) {
  // Create the main case object with detailed sections
  const payload = {
    title: caseData.value.title,
    specialty: caseData.value.specialty,
    patient_name: caseData.value.patient_name,
    patient_age: caseData.value.patient_age,
    patient_gender: caseData.value.patient_gender,
    medical_record_number: caseData.value.medical_record_number,
    keywords: caseData.value.keywords,
    template: caseData.value.template,
    repository: caseData.value.repository,
    case_status: status,
    // Include detailed medical sections
    clinical_history: caseData.value.clinical_history,
    physical_examination: caseData.value.physical_examination,
    detailed_investigations: caseData.value.investigations,
    diagnosis_management: caseData.value.diagnosis_management,
    learning_outcomes: caseData.value.learning_outcomes
  }

  return payload
}

async function loadRepositories() {
  try {
    // For now, create a default repository automatically
    // In a real app, you'd fetch from API
    repositories.value = [
      { id: 1, name: 'Kho hồ sơ bệnh án chính' }
    ]
    // Auto-select the first repository
    if (repositories.value.length > 0) {
      caseData.value.repository = repositories.value[0]?.id ?? null
    }
  } catch (error: any) {
    console.error('Error loading repositories:', error)
  }
}

// File handling methods
function openFileDialog() {
  fileInput.value?.click()
}

function handleFileSelect(event: Event) {
  const files = Array.from((event.target as HTMLInputElement).files || [])
  addFiles(files);
  // Reset input value so same file can be selected again
  (event.target as HTMLInputElement).value = ''
}

function handleDragOver(event: DragEvent) {
  event.preventDefault()
  isDragOver.value = true
}

function handleDragLeave(event: DragEvent) {
  event.preventDefault()
  isDragOver.value = false
}

function handleDrop(event: DragEvent) {
  event.preventDefault()
  isDragOver.value = false

  const files = Array.from(event.dataTransfer?.files || [])
  addFiles(files)
}

function addFiles(files: File[]) {
  const maxSize = 50 * 1024 * 1024 // 50MB
  const allowedTypes = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx', '.dcm', '.zip', '.rar']

  files.forEach(file => {
    // Validate file size
    if (file.size > maxSize) {
      alert(`Tệp "${file.name}" quá lớn! Vui lòng chọn tệp nhỏ hơn 50MB.`)
      return
    }

    // Validate file type
    const name = file.name || ''
    const parts = name.split('.')
    const ext = parts.length > 1 ? parts[parts.length - 1]?.toLowerCase() : ''
    const extension = ext ? '.' + ext : ''
    if (!extension || !allowedTypes.includes(extension)) {
      alert(`Tệp "${file.name}" không được hỗ trợ! Vui lòng chọn tệp có định dạng: ${allowedTypes.join(', ')}`)
      return
    }

    // Create attachment object
    const baseName = name.includes('.') ? name.substring(0, name.lastIndexOf('.')) : name
    const attachment = {
      file: file,
      attachment_type: '',
      title: baseName, // Auto-fill title from filename
      description: '',
      date_taken: '',
      physician_notes: '',
      is_confidential: false
    }

    attachments.value.push(attachment)
  })
}

function removeAttachment(index: number) {
  attachments.value.splice(index, 1)
}

function getFileIcon(file: File) {
  const extension = ((file.name || '').split('.').pop() || '').toLowerCase()
  const iconMap: { [key: string]: string } = {
    'jpg': 'fas fa-image',
    'jpeg': 'fas fa-image',
    'png': 'fas fa-image',
    'pdf': 'fas fa-file-pdf',
    'doc': 'fas fa-file-word',
    'docx': 'fas fa-file-word',
    'dcm': 'fas fa-x-ray',
    'zip': 'fas fa-file-archive',
    'rar': 'fas fa-file-archive'
  }
  return iconMap[extension] || 'fas fa-file'
}

function formatFileSize(bytes: number) {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

onMounted(async () => {
  // Check if user is authenticated
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }

  // Load repositories and templates
  await loadRepositories()
})
</script>

<style scoped>
.create-case {
  min-height: 100vh;
  background: #f8f9fa;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 2rem;
}

.create-header {
  background: white;
  border-bottom: 1px solid #e1e5e9;
  padding: 2rem 0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h1 {
  margin: 0;
  color: #333;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.create-main {
  padding: 2rem 0;
}

.case-form {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-section {
  margin-bottom: 3rem;
}

.form-section h2 {
  margin: 0 0 1.5rem 0;
  color: #333;
  font-size: 1.25rem;
  border-bottom: 2px solid #667eea;
  padding-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Enhanced styling for clinical sections */
.clinical-section {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.clinical-section h2 {
  background: white;
  padding: 1rem;
  margin: -2rem -2rem 1.5rem -2rem;
  border-radius: 12px 12px 0 0;
  border-bottom: 2px solid #667eea;
  font-weight: 600;
}

/* Color coding for different clinical sections */
.clinical-section:nth-of-type(3) {
  border-left: 4px solid #10b981;
  /* Green - Clinical History */
}

.clinical-section:nth-of-type(4) {
  border-left: 4px solid #f59e0b;
  /* Amber - Physical Examination */
}

.clinical-section:nth-of-type(5) {
  border-left: 4px solid #8b5cf6;
  /* Purple - Investigations */
}

.clinical-section:nth-of-type(6) {
  border-left: 4px solid #ef4444;
  /* Red - Diagnosis & Management */
}

.clinical-section:nth-of-type(7) {
  border-left: 4px solid #06b6d4;
  /* Cyan - Learning Outcomes */
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #374151;
}

.form-input,
.form-select,
.form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.form-help {
  display: block;
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #5a67d8;
}

.btn-outline {
  background: transparent;
  color: #667eea;
  border: 1px solid #667eea;
}

.btn-outline:hover:not(:disabled) {
  background: #667eea;
  color: white;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .case-form {
    padding: 1rem;
  }
}

/* Medical Attachments Upload Styles */
.upload-area {
  border: 2px dashed #cbd5e1;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  background: #f8fafc;
  transition: all 0.3s ease;
  cursor: pointer;
  margin-bottom: 2rem;
}

.upload-area:hover,
.upload-area.dragover {
  border-color: #16a34a;
  background: #f0fdf4;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.upload-icon {
  font-size: 3rem;
  color: #9ca3af;
}

.upload-area:hover .upload-icon,
.upload-area.dragover .upload-icon {
  color: #16a34a;
}

.upload-content h3 {
  margin: 0;
  color: #374151;
  font-size: 1.125rem;
}

.upload-content p {
  margin: 0;
  color: #6b7280;
}

.file-input {
  display: none;
}

.file-types {
  margin-top: 1rem;
  color: #6b7280;
}

.attachments-list {
  margin-top: 2rem;
}

.attachments-list h4 {
  margin: 0 0 1rem 0;
  color: #374151;
  font-size: 1.1rem;
}

.attachment-item {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  position: relative;
  transition: box-shadow 0.2s ease;
}

.attachment-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.attachment-preview {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f3f4f6;
}

.attachment-icon {
  width: 48px;
  height: 48px;
  background: #f3f4f6;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: #6b7280;
}

.attachment-info {
  flex: 1;
}

.file-name {
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.25rem;
}

.file-size {
  font-size: 0.875rem;
  color: #6b7280;
}

.attachment-metadata {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.metadata-field {
  display: flex;
  flex-direction: column;
}

.metadata-field label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
}

.metadata-field input,
.metadata-field select,
.metadata-field textarea {
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
  transition: border-color 0.2s ease;
}

.metadata-field input:focus,
.metadata-field select:focus,
.metadata-field textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.checkbox-field {
  flex-direction: row;
  align-items: center;
  gap: 0.5rem;
  grid-column: span 2;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #374151;
  cursor: pointer;
  margin: 0;
}

.checkbox-label input[type="checkbox"] {
  margin: 0;
  width: 1rem;
  height: 1rem;
}

.remove-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.remove-btn:hover {
  background: #dc2626;
}

/* Responsive attachments */
@media (max-width: 768px) {
  .attachment-metadata {
    grid-template-columns: 1fr;
  }

  .checkbox-field {
    grid-column: span 1;
  }

  .upload-content {
    padding: 1rem;
  }
}
</style>
