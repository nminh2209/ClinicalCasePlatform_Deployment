<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white border-b border-gray-200 py-6 px-8">
      <div class="max-w-4xl mx-auto flex items-center justify-between gap-4">
        <h1 class="text-2xl font-bold text-gray-800 m-0">
          Tạo hồ sơ bệnh án mới
        </h1>
        <div class="flex gap-3">
          <Button
            icon="pi pi-save"
            label="Lưu bản nháp"
            outlined
            :disabled="saving"
            :loading="saving"
            @click="saveDraft"
          />
          <Button
            icon="pi pi-send"
            label="Nộp hồ sơ"
            :disabled="!isValid || saving"
            :loading="saving"
            @click="submitCase"
          />
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="py-8 px-8">
      <div class="max-w-4xl mx-auto">
        <div class="bg-white rounded-xl shadow-sm p-8 flex flex-col gap-10">
          <!-- Basic Information -->
          <section class="form-section">
            <h2 class="section-heading">
              <i class="pi pi-building" />
              Thông tin cơ bản
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="flex flex-col gap-1">
                <label for="title" class="field-label"
                  >Tiêu đề hồ sơ <span class="text-red-500">*</span></label
                >
                <InputText
                  id="title"
                  v-model="caseData.title"
                  placeholder="VD: Suy hô hấp cấp - Viêm phổi - HSTC"
                  class="w-full"
                />
              </div>

              <div class="flex flex-col gap-1">
                <label for="specialty" class="field-label"
                  >Chuyên khoa <span class="text-red-500">*</span></label
                >
                <Select
                  id="specialty"
                  v-model="caseData.specialty"
                  :options="specialties"
                  option-label="name"
                  option-value="name"
                  :placeholder="
                    choicesLoading ? 'Đang tải...' : 'Chọn chuyên khoa'
                  "
                  :disabled="choicesLoading"
                  class="w-full"
                />
              </div>
            </div>
          </section>

          <!-- Patient Information -->
          <section class="form-section">
            <h2 class="section-heading">
              <i class="pi pi-user" />
              Thông tin bệnh nhân
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="flex flex-col gap-1">
                <label for="patient_name" class="field-label"
                  >Tên bệnh nhân (ẩn danh)
                  <span class="text-red-500">*</span></label
                >
                <InputText
                  id="patient_name"
                  v-model="caseData.patient_name"
                  placeholder="VD: NGUYỄN HỒNG ĐIỆP (ẩn danh)"
                  class="w-full"
                />
              </div>

              <div class="flex flex-col gap-1">
                <label for="patient_age" class="field-label"
                  >Tuổi <span class="text-red-500">*</span></label
                >
                <InputNumber
                  id="patient_age"
                  v-model="caseData.patient_age"
                  :min="0"
                  :max="120"
                  fluid
                  class="w-full"
                />
              </div>

              <div class="flex flex-col gap-1">
                <label for="patient_gender" class="field-label"
                  >Giới tính <span class="text-red-500">*</span></label
                >
                <Select
                  id="patient_gender"
                  v-model="caseData.patient_gender"
                  :options="genders"
                  option-label="label"
                  option-value="key"
                  :placeholder="
                    choicesLoading ? 'Đang tải...' : 'Chọn giới tính'
                  "
                  :disabled="choicesLoading"
                  class="w-full"
                />
              </div>

              <div class="flex flex-col gap-1">
                <label for="medical_record_number" class="field-label"
                  >Số hồ sơ bệnh án</label
                >
                <InputText
                  id="medical_record_number"
                  v-model="caseData.medical_record_number"
                  placeholder="VD: HST001"
                  class="w-full"
                />
              </div>
            </div>
          </section>

          <!-- Clinical History -->
          <section class="form-section clinical-section clinical-green">
            <h2 class="section-heading">
              <i class="pi pi-clipboard" />
              Tiền sử lâm sàng
            </h2>

            <div class="flex flex-col gap-1 mb-5">
              <label for="chief_complaint" class="field-label"
                >Lý do khám chính <span class="text-red-500">*</span></label
              >
              <Textarea
                id="chief_complaint"
                v-model="caseData.clinical_history.chief_complaint"
                rows="2"
                placeholder="VD: Khó thở"
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1 mb-5">
              <label for="history_present_illness" class="field-label"
                >Bệnh sử hiện tại <span class="text-red-500">*</span></label
              >
              <Textarea
                id="history_present_illness"
                v-model="caseData.clinical_history.history_present_illness"
                rows="6"
                placeholder="Mô tả chi tiết quá trình khởi phát và diễn biến bệnh..."
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1 mb-5">
              <label for="past_medical_history" class="field-label"
                >Tiền sử bệnh tật</label
              >
              <Textarea
                id="past_medical_history"
                v-model="caseData.clinical_history.past_medical_history"
                rows="3"
                placeholder="Các bệnh đã mắc trước đây..."
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1 mb-5">
              <label for="family_history" class="field-label"
                >Tiền sử gia đình</label
              >
              <Textarea
                id="family_history"
                v-model="caseData.clinical_history.family_history"
                rows="2"
                placeholder="Bệnh di truyền, bệnh gia đình..."
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1 mb-5">
              <label for="medications" class="field-label"
                >Thuốc đang sử dụng</label
              >
              <Textarea
                id="medications"
                v-model="caseData.clinical_history.medications"
                rows="2"
                placeholder="Các thuốc đang dùng..."
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <label for="allergies" class="field-label">Dị ứng</label>
              <Textarea
                id="allergies"
                v-model="caseData.clinical_history.allergies"
                rows="2"
                placeholder="Dị ứng thuốc, thực phẩm..."
                class="w-full"
              />
            </div>
          </section>

          <!-- Physical Examination -->
          <section class="form-section clinical-section clinical-amber">
            <h2 class="section-heading">
              <i class="pi pi-heart" />
              Khám lâm sàng
            </h2>

            <div class="flex flex-col gap-1 mb-5">
              <label for="general_appearance" class="field-label"
                >Tình trạng chung <span class="text-red-500">*</span></label
              >
              <Textarea
                id="general_appearance"
                v-model="caseData.physical_examination.general_appearance"
                rows="3"
                placeholder="Tình trạng ý thức, thể trạng chung..."
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1 mb-5">
              <label for="vital_signs" class="field-label"
                >Sinh hiệu <span class="text-red-500">*</span></label
              >
              <Textarea
                id="vital_signs"
                v-model="caseData.physical_examination.vital_signs"
                rows="3"
                placeholder="Nhiệt độ, mạch, huyết áp, nhịp thở, SpO2..."
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1 mb-5">
              <label for="cardiovascular" class="field-label">Tim mạch</label>
              <Textarea
                id="cardiovascular"
                v-model="caseData.physical_examination.cardiovascular"
                rows="4"
                placeholder="Khám tim: nhịp tim, tiếng tim, thổi..."
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1 mb-5">
              <label for="respiratory" class="field-label">Hô hấp</label>
              <Textarea
                id="respiratory"
                v-model="caseData.physical_examination.respiratory"
                rows="4"
                placeholder="Khám phổi: nhịp thở, ran, thở máy..."
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1 mb-5">
              <label for="abdominal" class="field-label">Bụng</label>
              <Textarea
                id="abdominal"
                v-model="caseData.physical_examination.abdominal"
                rows="3"
                placeholder="Khám bụng: mềm, chướng, gan lách..."
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <label for="neurological" class="field-label">Thần kinh</label>
              <Textarea
                id="neurological"
                v-model="caseData.physical_examination.neurological"
                rows="3"
                placeholder="Khám thần kinh: ý thức, phản xạ, vận động..."
                class="w-full"
              />
            </div>
          </section>

          <!-- Investigations -->
          <section class="form-section clinical-section clinical-purple">
            <h2 class="section-heading">
              <i class="pi pi-search" />
              Cận lâm sàng
            </h2>

            <div class="flex flex-col gap-1 mb-5">
              <label for="laboratory_results" class="field-label"
                >Xét nghiệm</label
              >
              <Textarea
                id="laboratory_results"
                v-model="caseData.investigations.laboratory_results"
                rows="4"
                placeholder="Khí máu, bilan nhiễm trùng, sinh hóa..."
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1 mb-5">
              <label for="imaging_studies" class="field-label"
                >Chẩn đoán hình ảnh</label
              >
              <Textarea
                id="imaging_studies"
                v-model="caseData.investigations.imaging_studies"
                rows="4"
                placeholder="X-quang, CT, siêu âm, MRI..."
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1 mb-5">
              <label for="ecg_findings" class="field-label">Điện tâm đồ</label>
              <Textarea
                id="ecg_findings"
                v-model="caseData.investigations.ecg_findings"
                rows="3"
                placeholder="Kết quả điện tâm đồ..."
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1 mb-5">
              <label for="biochemistry" class="field-label">Sinh hóa</label>
              <Textarea
                id="biochemistry"
                v-model="caseData.investigations.biochemistry"
                rows="3"
                placeholder="NT-proBNP, enzim gan, creatinin..."
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <label for="hematology" class="field-label">Huyết học</label>
              <Textarea
                id="hematology"
                v-model="caseData.investigations.hematology"
                rows="3"
                placeholder="Công thức máu, đông cầm máu..."
                class="w-full"
              />
            </div>
          </section>

          <!-- Diagnosis and Management -->
          <section class="form-section clinical-section clinical-red">
            <h2 class="section-heading">
              <i class="pi pi-tablet" />
              Chẩn đoán và điều trị
            </h2>

            <div class="flex flex-col gap-1 mb-5">
              <label for="primary_diagnosis" class="field-label"
                >Chẩn đoán chính <span class="text-red-500">*</span></label
              >
              <Textarea
                id="primary_diagnosis"
                v-model="caseData.diagnosis_management.primary_diagnosis"
                rows="3"
                placeholder="VD: Suy hô hấp cấp mức độ nặng - Viêm phổi nặng..."
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1 mb-5">
              <label for="differential_diagnosis" class="field-label"
                >Chẩn đoán phân biệt</label
              >
              <Textarea
                id="differential_diagnosis"
                v-model="caseData.diagnosis_management.differential_diagnosis"
                rows="3"
                placeholder="Các chẩn đoán cần loại trừ..."
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1 mb-5">
              <label for="treatment_plan" class="field-label"
                >Kế hoạch điều trị <span class="text-red-500">*</span></label
              >
              <Textarea
                id="treatment_plan"
                v-model="caseData.diagnosis_management.treatment_plan"
                rows="5"
                placeholder="Hỗ trợ hô hấp, kháng sinh, điều trị nguyên nhân..."
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1 mb-5">
              <label for="medications_prescribed" class="field-label"
                >Thuốc kê đơn</label
              >
              <Textarea
                id="medications_prescribed"
                v-model="caseData.diagnosis_management.medications_prescribed"
                rows="3"
                placeholder="Danh sách thuốc được kê..."
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1 mb-5">
              <label for="procedures_performed" class="field-label"
                >Thủ thuật thực hiện</label
              >
              <Textarea
                id="procedures_performed"
                v-model="caseData.diagnosis_management.procedures_performed"
                rows="3"
                placeholder="Các thủ thuật đã thực hiện..."
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <label for="prognosis" class="field-label">Tiên lượng</label>
              <Textarea
                id="prognosis"
                v-model="caseData.diagnosis_management.prognosis"
                rows="2"
                placeholder="Tiên lượng bệnh..."
                class="w-full"
              />
            </div>
          </section>

          <!-- Learning Outcomes -->
          <section class="form-section clinical-section clinical-cyan">
            <h2 class="section-heading">
              <i class="pi pi-graduation-cap" />
              Mục tiêu học tập
            </h2>

            <div class="flex flex-col gap-1 mb-5">
              <label for="learning_objectives" class="field-label"
                >Mục tiêu học tập <span class="text-red-500">*</span></label
              >
              <Textarea
                id="learning_objectives"
                v-model="caseData.learning_outcomes.learning_objectives"
                rows="4"
                placeholder="Những mục tiêu học tập chính từ ca bệnh này..."
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1 mb-5">
              <label for="key_concepts" class="field-label"
                >Khái niệm chính</label
              >
              <Textarea
                id="key_concepts"
                v-model="caseData.learning_outcomes.key_concepts"
                rows="3"
                placeholder="Các khái niệm y học quan trọng..."
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1 mb-5">
              <label for="clinical_pearls" class="field-label"
                >Điểm lâm sàng quan trọng</label
              >
              <Textarea
                id="clinical_pearls"
                v-model="caseData.learning_outcomes.clinical_pearls"
                rows="3"
                placeholder="Những điểm lâm sàng đáng chú ý..."
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1 mb-5">
              <label for="discussion_points" class="field-label"
                >Điểm thảo luận</label
              >
              <Textarea
                id="discussion_points"
                v-model="caseData.learning_outcomes.discussion_points"
                rows="3"
                placeholder="Các câu hỏi thảo luận..."
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1">
              <label for="references" class="field-label"
                >Tài liệu tham khảo</label
              >
              <Textarea
                id="references"
                v-model="caseData.learning_outcomes.references"
                rows="3"
                placeholder="Tài liệu tham khảo liên quan..."
                class="w-full"
              />
            </div>
          </section>

          <!-- Medical Attachments -->
          <section class="form-section">
            <h2 class="section-heading">
              <i class="pi pi-folder-open" />
              Tài liệu đính kèm y tế
            </h2>

            <!-- Upload Area -->
            <div
              class="upload-area"
              :class="{ 'upload-area--dragover': isDragOver }"
              @dragover.prevent="handleDragOver"
              @dragleave.prevent="handleDragLeave"
              @drop.prevent="handleDrop"
              @click="openFileDialog"
            >
              <i class="pi pi-cloud-upload upload-icon" />
              <h3 class="text-base font-semibold text-gray-700 m-0">
                Thêm tài liệu y tế
              </h3>
              <p class="text-sm text-gray-500 m-0">
                Kéo thả tệp vào đây hoặc click để chọn
              </p>
              <Button
                type="button"
                icon="pi pi-plus"
                label="Chọn tệp"
                outlined
                size="small"
                @click.stop="openFileDialog"
              />
              <small class="text-gray-400 mt-1"
                >Hỗ trợ: JPG, PNG, PDF, DOC, DOCX, DICOM, ZIP, RAR (Max: 50MB
                mỗi tệp)</small
              >
              <input
                ref="fileInput"
                type="file"
                multiple
                accept=".jpg,.jpeg,.png,.pdf,.doc,.docx,.dcm,.zip,.rar"
                @change="handleFileSelect"
                class="hidden"
              />
            </div>

            <!-- Attachments List -->
            <div v-if="attachments.length > 0" class="mt-6 flex flex-col gap-4">
              <h4 class="font-semibold text-gray-700 m-0">
                Tệp đã chọn ({{ attachments.length }})
              </h4>

              <div
                v-for="(attachment, index) in attachments"
                :key="index"
                class="relative border border-gray-200 rounded-lg p-5 bg-white hover:shadow-md transition-shadow"
              >
                <!-- Remove button -->
                <Button
                  type="button"
                  icon="pi pi-times"
                  severity="danger"
                  rounded
                  text
                  size="small"
                  class="!absolute top-3 right-3"
                  @click="removeAttachment(index)"
                />

                <!-- File preview row -->
                <div
                  class="flex items-center gap-3 mb-4 pb-4 border-b border-gray-100"
                >
                  <div
                    class="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center shrink-0"
                  >
                    <i
                      :class="getFileIcon(attachment.file)"
                      class="text-gray-500 text-xl"
                    />
                  </div>
                  <div>
                    <div class="font-semibold text-gray-800 text-sm">
                      {{ attachment.file.name }}
                    </div>
                    <div class="text-xs text-gray-500">
                      {{ formatFileSize(attachment.file.size) }}
                    </div>
                  </div>
                </div>

                <!-- Metadata grid -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <!-- Attachment Type -->
                  <div class="flex flex-col gap-1">
                    <label class="text-xs font-semibold text-gray-700"
                      >Loại tài liệu</label
                    >
                    <Select
                      v-model="attachment.attachment_type"
                      :options="attachmentTypeOptions"
                      option-label="name"
                      option-value="value"
                      placeholder="-- Chọn loại --"
                      class="w-full text-sm"
                    />
                  </div>

                  <!-- Title -->
                  <div class="flex flex-col gap-1">
                    <label class="text-xs font-semibold text-gray-700"
                      >Tiêu đề</label
                    >
                    <InputText
                      v-model="attachment.title"
                      placeholder="Nhập tiêu đề mô tả..."
                      class="w-full text-sm"
                    />
                  </div>

                  <!-- Description -->
                  <div class="flex flex-col gap-1">
                    <label class="text-xs font-semibold text-gray-700"
                      >Mô tả</label
                    >
                    <Textarea
                      v-model="attachment.description"
                      rows="2"
                      placeholder="Mô tả chi tiết về tài liệu..."
                      class="w-full text-sm"
                    />
                  </div>

                  <!-- Date Taken -->
                  <div class="flex flex-col gap-1">
                    <label class="text-xs font-semibold text-gray-700"
                      >Ngày thực hiện</label
                    >
                    <InputText
                      v-model="attachment.date_taken"
                      type="date"
                      class="w-full text-sm"
                    />
                  </div>

                  <!-- Physician Notes -->
                  <div class="flex flex-col gap-1 md:col-span-2">
                    <label class="text-xs font-semibold text-gray-700"
                      >Ghi chú bác sĩ</label
                    >
                    <Textarea
                      v-model="attachment.physician_notes"
                      rows="2"
                      placeholder="Ghi chú của bác sĩ về tài liệu..."
                      class="w-full text-sm"
                    />
                  </div>

                  <!-- Confidential -->
                  <div class="flex items-center gap-2 md:col-span-2">
                    <Checkbox
                      v-model="attachment.is_confidential"
                      binary
                      input-id="`conf-${index}`"
                    />
                    <label
                      :for="`conf-${index}`"
                      class="flex items-center gap-1 text-sm text-gray-700 cursor-pointer"
                    >
                      <i class="pi pi-lock text-gray-500" />
                      Tài liệu bảo mật (chỉ giảng viên xem được)
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- Keywords -->
          <section class="form-section">
            <h2 class="section-heading">
              <i class="pi pi-tag" />
              Từ khóa và phân loại
            </h2>
            <div class="flex flex-col gap-1">
              <label for="keywords" class="field-label">Từ khóa</label>
              <InputText
                id="keywords"
                v-model="caseData.keywords"
                placeholder="VD: suy hô hấp, viêm phổi, thở máy, HSTC"
                class="w-full"
              />
              <small class="text-gray-400"
                >Phân cách bằng dấu phẩy để dễ tìm kiếm</small
              >
            </div>
          </section>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useCasesStore } from "@/stores/cases";
import { casesService } from "@/services/cases";
import { useChoices } from "@/composables/useChoices";
import Button from "primevue/button";
import InputText from "primevue/inputtext";
import InputNumber from "primevue/inputnumber";
import Textarea from "primevue/textarea";
import Select from "primevue/select";
import Checkbox from "primevue/checkbox";

const router = useRouter();
const authStore = useAuthStore();
const casesStore = useCasesStore();
const { specialties, genders, loading: choicesLoading } = useChoices();

const saving = ref(false);

const attachmentTypeOptions = [
  { name: "Ảnh chụp X-quang", value: "x_ray" },
  { name: "Phiếu xét nghiệm", value: "lab_report" },
  { name: "Chụp CT/Scanner", value: "ct_scan" },
  { name: "Chụp MRI", value: "mri_scan" },
  { name: "Siêu âm", value: "ultrasound" },
  { name: "Ảnh chụp chấn thương", value: "injury_photo" },
  { name: "Ảnh phẫu thuật", value: "surgical_photo" },
  { name: "Tiêu bản bệnh học", value: "pathology_slide" },
  { name: "Đơn thuốc", value: "prescription" },
  { name: "Tóm tắt xuất viện", value: "discharge_summary" },
  { name: "Dấu hiệu sinh tồn", value: "vital_signs" },
  { name: "Điện tâm đồ", value: "ekg_ecg" },
  { name: "Nội soi", value: "endoscopy" },
  { name: "Kết quả sinh thiết", value: "biopsy_report" },
  { name: "Giấy chứng nhận y tế", value: "medical_certificate" },
  { name: "Khác", value: "other" },
];

const attachments = ref<
  Array<{
    file: File;
    attachment_type: string;
    title: string;
    description?: string;
    date_taken?: string;
    physician_notes?: string;
    is_confidential: boolean;
  }>
>([]);

const isDragOver = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);

type CaseData = {
  title: string;
  specialty: string;
  patient_name: string;
  patient_age: number | null;
  patient_gender: string;
  medical_record_number: string;
  keywords: string;
  template: any;
  repository: number | null;
  clinical_history: Record<string, any>;
  physical_examination: Record<string, any>;
  investigations: Record<string, any>;
  diagnosis_management: Record<string, any>;
  learning_outcomes: Record<string, any>;
};

const caseData = ref<CaseData>({
  title: "",
  specialty: "",
  patient_name: "",
  patient_age: null,
  patient_gender: "",
  medical_record_number: "",
  keywords: "",
  template: null,
  repository: null,
  clinical_history: {
    chief_complaint: "",
    history_present_illness: "",
    past_medical_history: "",
    family_history: "",
    social_history: "",
    allergies: "",
    medications: "",
    review_systems: "",
  },
  physical_examination: {
    general_appearance: "",
    vital_signs: "",
    head_neck: "",
    cardiovascular: "",
    respiratory: "",
    abdominal: "",
    neurological: "",
    musculoskeletal: "",
    skin: "",
    other_findings: "",
  },
  investigations: {
    laboratory_results: "",
    imaging_studies: "",
    ecg_findings: "",
    special_tests: "",
    biochemistry: "",
    hematology: "",
    microbiology: "",
  },
  diagnosis_management: {
    primary_diagnosis: "",
    differential_diagnosis: "",
    treatment_plan: "",
    medications_prescribed: "",
    procedures_performed: "",
    follow_up_plan: "",
    prognosis: "",
    complications: "",
  },
  learning_outcomes: {
    learning_objectives: "",
    key_concepts: "",
    clinical_pearls: "",
    references: "",
    discussion_points: "",
    assessment_criteria: "",
  },
});

const repositories = ref<Array<{ id: number; name: string }>>([]);

const isValid = computed(
  () =>
    caseData.value.title &&
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
    caseData.value.repository,
);

async function saveDraft() {
  if (!caseData.value.title || !caseData.value.repository) {
    alert("Vui lòng nhập tiêu đề hồ sơ và chọn kho lưu trữ");
    return;
  }
  saving.value = true;
  try {
    const payload = prepareCasePayload("draft");
    const createdCase = await casesStore.createCase(payload);
    if (attachments.value.length > 0) await uploadAttachments(createdCase.id);
    alert("Đã lưu bản nháp thành công!");
    router.push("/cases");
  } catch (error: any) {
    console.error("Error saving draft:", error);
    alert(
      "Có lỗi xảy ra khi lưu bản nháp: " +
        (error.response?.data?.detail || error.message),
    );
  } finally {
    saving.value = false;
  }
}

async function submitCase() {
  if (!isValid.value) {
    alert("Vui lòng điền đầy đủ thông tin bắt buộc");
    return;
  }
  for (let i = 0; i < attachments.value.length; i++) {
    const attachment = attachments.value[i];
    if (!attachment?.attachment_type || !attachment.title) {
      alert(
        `Vui lòng điền đầy đủ thông tin cho tệp "${attachment?.file.name}" (loại tài liệu và tiêu đề)`,
      );
      return;
    }
  }
  saving.value = true;
  try {
    const payload = prepareCasePayload("submitted");
    const createdCase = await casesStore.createCase(payload);
    if (attachments.value.length > 0) await uploadAttachments(createdCase.id);
    alert("Đã nộp hồ sơ bệnh án thành công!");
    router.push("/cases");
  } catch (error: any) {
    console.error("Error submitting case:", error);
    alert(
      "Có lỗi xảy ra khi nộp hồ sơ: " +
        (error.response?.data?.detail || error.message),
    );
  } finally {
    saving.value = false;
  }
}

async function uploadAttachments(caseId: string) {
  const uploadPromises = attachments.value.map(async (attachment) => {
    try {
      const formData = new FormData();
      formData.append("file", attachment.file);
      formData.append("attachment_type", attachment.attachment_type);
      formData.append("title", attachment.title);
      formData.append("description", attachment.description || "");
      formData.append("physician_notes", attachment.physician_notes || "");
      formData.append("is_confidential", `${attachment.is_confidential}`);
      if (attachment.date_taken)
        formData.append("date_taken", attachment.date_taken);
      await casesService.uploadAttachment(caseId, formData);
    } catch (error: any) {
      console.error(`Error uploading ${attachment.file.name}:`, error);
      throw new Error(
        `Lỗi khi tải lên tệp "${attachment.file.name}": ${error.response?.data?.message || error.message}`,
      );
    }
  });
  await Promise.all(uploadPromises);
}

function prepareCasePayload(status: string) {
  return {
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
    clinical_history: caseData.value.clinical_history,
    physical_examination: caseData.value.physical_examination,
    detailed_investigations: caseData.value.investigations,
    diagnosis_management: caseData.value.diagnosis_management,
    learning_outcomes: caseData.value.learning_outcomes,
  };
}

async function loadRepositories() {
  try {
    repositories.value = [{ id: 1, name: "Kho hồ sơ bệnh án chính" }];
    if (repositories.value.length > 0) {
      caseData.value.repository = repositories.value[0]?.id ?? null;
    }
  } catch (error: any) {
    console.error("Error loading repositories:", error);
  }
}

function openFileDialog() {
  fileInput.value?.click();
}

function handleFileSelect(event: Event) {
  const files = Array.from((event.target as HTMLInputElement).files || []);
  addFiles(files);
  (event.target as HTMLInputElement).value = "";
}

function handleDragOver(event: DragEvent) {
  event.preventDefault();
  isDragOver.value = true;
}

function handleDragLeave(event: DragEvent) {
  event.preventDefault();
  isDragOver.value = false;
}

function handleDrop(event: DragEvent) {
  event.preventDefault();
  isDragOver.value = false;
  addFiles(Array.from(event.dataTransfer?.files || []));
}

function addFiles(files: File[]) {
  const maxSize = 50 * 1024 * 1024;
  const allowedTypes = [
    ".jpg",
    ".jpeg",
    ".png",
    ".pdf",
    ".doc",
    ".docx",
    ".dcm",
    ".zip",
    ".rar",
  ];

  files.forEach((file) => {
    if (file.size > maxSize) {
      alert(`Tệp "${file.name}" quá lớn! Vui lòng chọn tệp nhỏ hơn 50MB.`);
      return;
    }
    const name = file.name || "";
    const parts = name.split(".");
    const ext = parts.length > 1 ? parts[parts.length - 1]?.toLowerCase() : "";
    const extension = ext ? "." + ext : "";
    if (!extension || !allowedTypes.includes(extension)) {
      alert(
        `Tệp "${file.name}" không được hỗ trợ! Vui lòng chọn tệp có định dạng: ${allowedTypes.join(", ")}`,
      );
      return;
    }
    const baseName = name.includes(".")
      ? name.substring(0, name.lastIndexOf("."))
      : name;
    attachments.value.push({
      file,
      attachment_type: "",
      title: baseName,
      description: "",
      date_taken: "",
      physician_notes: "",
      is_confidential: false,
    });
  });
}

function removeAttachment(index: number) {
  attachments.value.splice(index, 1);
}

function getFileIcon(file: File): string {
  const extension = ((file.name || "").split(".").pop() || "").toLowerCase();
  const iconMap: Record<string, string> = {
    jpg: "pi pi-image",
    jpeg: "pi pi-image",
    png: "pi pi-image",
    pdf: "pi pi-file-pdf",
    doc: "pi pi-file-word",
    docx: "pi pi-file-word",
    dcm: "pi pi-desktop",
    zip: "pi pi-inbox",
    rar: "pi pi-inbox",
  };
  return iconMap[extension] || "pi pi-file";
}

function formatFileSize(bytes: number): string {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push("/login");
    return;
  }
  await loadRepositories();
});
</script>

<style scoped>
.section-heading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.15rem;
  font-weight: 700;
  color: #333;
  border-bottom: 2px solid #667eea;
  padding-bottom: 0.5rem;
  margin: 0 0 1.5rem 0;
}

.field-label {
  font-weight: 600;
  font-size: 0.9rem;
  color: #374151;
}

.form-section {
  padding-bottom: 1rem;
}

/* Clinical section card style */
.clinical-section {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
}

.clinical-section .section-heading {
  background: white;
  padding: 1rem;
  margin: -1.5rem -1.5rem 1.5rem -1.5rem;
  border-radius: 12px 12px 0 0;
  border-bottom: 2px solid #667eea;
}

.clinical-green {
  border-left: 4px solid #10b981;
}
.clinical-amber {
  border-left: 4px solid #f59e0b;
}
.clinical-purple {
  border-left: 4px solid #8b5cf6;
}
.clinical-red {
  border-left: 4px solid #ef4444;
}
.clinical-cyan {
  border-left: 4px solid #06b6d4;
}

/* Upload area */
.upload-area {
  border: 2px dashed #cbd5e1;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  background: #f8fafc;
  transition: all 0.3s ease;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.upload-area:hover,
.upload-area--dragover {
  border-color: #16a34a;
  background: #f0fdf4;
}

.upload-icon {
  font-size: 3rem;
  color: #9ca3af;
}

.upload-area:hover .upload-icon,
.upload-area--dragover .upload-icon {
  color: #16a34a;
}
</style>
