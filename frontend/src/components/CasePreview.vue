<template>
  <Dialog
    class="rounded p-3"
    :visible="true"
    @update:visible="$emit('close')"
    modal
    :closable="true"
    :style="{ width: '56rem', maxWidth: '95vw' }"
    :contentStyle="{ maxHeight: '80vh', overflowY: 'auto' }"
    :pt="{ header: { class: 'border-b pb-4' } }"
  >
    <template #header>
      <h2 class="text-2xl font-bold text-gray-800">Xem trước bệnh án</h2>
    </template>

    <div class="space-y-6 p-2">
      <div class="text-center border-b pb-4">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">
          {{ caseData.title }}
        </h1>
        <Tag
          :value="caseData.specialty"
          severity="secondary"
          class="text-lg px-4 py-2"
        />
      </div>

      <div
        class="bg-purple-50 p-4 rounded-lg border-l-4 border-purple-500 mb-4"
      >
        <h3
          class="text-lg font-semibold text-gray-800 mb-3 flex items-center gap-2"
        >
          <i class="pi pi-chart-bar text-purple-600" /> Thông tin ca bệnh
        </h3>
        <div class="grid grid-cols-2 gap-3 text-sm">
          <div>
            <span class="font-medium">Mức độ ưu tiên:</span>
            {{ formatPriority(caseData.priority_level) }}
          </div>
          <div>
            <span class="font-medium">Độ phức tạp:</span>
            {{ formatComplexity(caseData.complexity_level) }}
          </div>
          <div v-if="caseData.estimated_study_hours">
            <span class="font-medium">Giờ học ước tính:</span>
            {{ caseData.estimated_study_hours }} giờ
          </div>
          <div v-if="caseData.learning_tags">
            <span class="font-medium">Tags:</span>
            {{ caseData.learning_tags }}
          </div>
        </div>
        <div
          v-if="caseData.case_summary"
          class="mt-3 pt-3 border-t border-purple-200"
        >
          <span class="font-medium">Tóm tắt:</span>
          <p class="text-gray-700 mt-1">{{ caseData.case_summary }}</p>
        </div>
      </div>

      <div class="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
        <h3
          class="text-lg font-semibold text-gray-800 mb-3 flex items-center gap-2"
        >
          <i class="pi pi-user text-blue-600" /> Thông tin bệnh nhân
        </h3>
        <div class="grid grid-cols-2 gap-3 text-sm">
          <div>
            <span class="font-medium">Tuổi:</span>
            {{ caseData.patient_age || "Chưa nhập" }}
          </div>
          <div>
            <span class="font-medium">Giới tính:</span>
            {{ formatGender(caseData.patient_gender) }}
          </div>
          <div v-if="caseData.patient_ethnicity">
            <span class="font-medium">Dân tộc:</span>
            {{ caseData.patient_ethnicity }}
          </div>
          <div v-if="caseData.patient_occupation">
            <span class="font-medium">Nghề nghiệp:</span>
            {{ caseData.patient_occupation }}
          </div>
          <div v-if="caseData.admission_date">
            <span class="font-medium">Ngày nhập viện:</span>
            {{ caseData.admission_date }}
          </div>
          <div v-if="caseData.discharge_date">
            <span class="font-medium">Ngày xuất viện:</span>
            {{ caseData.discharge_date }}
          </div>
          <div>
            <span class="font-medium">Số hồ sơ:</span>
            {{ caseData.medical_record_number || "Chưa nhập" }}
          </div>
          <div v-if="caseData.chief_complaint_brief">
            <span class="font-medium">Lý do khám:</span>
            {{ caseData.chief_complaint_brief }}
          </div>
        </div>
      </div>

      <div>
        <h3
          class="text-xl font-bold text-gray-800 mb-3 border-b pb-2 flex items-center gap-2"
        >
          <i class="pi pi-clipboard text-gray-600" /> Tiền sử lâm sàng
        </h3>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Lý do khám chính
          </h4>
          <div class="text-gray-700 bg-gray-50 p-3 rounded-lg">
            {{ caseData.clinical_history?.chief_complaint || "Chưa nhập" }}
          </div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Bệnh sử hiện tại
          </h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{
              caseData.clinical_history?.history_present_illness || "Chưa nhập"
            }}
          </div>
        </div>

        <div
          v-if="
            caseData.clinical_history?.symptom_duration_days ||
            caseData.clinical_history?.symptom_onset ||
            caseData.clinical_history?.symptom_progression
          "
          class="mb-4"
        >
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Thông tin triệu chứng
          </h4>
          <div class="text-gray-700 bg-gray-50 p-3 rounded-lg">
            <div v-if="caseData.clinical_history?.symptom_duration_days">
              Thời gian:
              {{ caseData.clinical_history.symptom_duration_days }} ngày
            </div>
            <div v-if="caseData.clinical_history?.symptom_onset">
              Khởi phát:
              {{ formatSymptomOnset(caseData.clinical_history.symptom_onset) }}
            </div>
            <div v-if="caseData.clinical_history?.symptom_progression">
              Diễn biến:
              {{
                formatSymptomProgression(
                  caseData.clinical_history.symptom_progression,
                )
              }}
            </div>
          </div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Tiền sử bệnh tật
          </h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ caseData.clinical_history?.past_medical_history || "Chưa nhập" }}
          </div>
        </div>

        <div v-if="caseData.clinical_history?.family_history" class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Tiền sử gia đình
          </h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ caseData.clinical_history.family_history }}
          </div>
        </div>

        <div v-if="caseData.clinical_history?.social_history" class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Tiền sử xã hội
          </h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ caseData.clinical_history.social_history }}
          </div>
        </div>

        <div v-if="caseData.clinical_history?.allergies" class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Dị ứng</h4>
          <div
            class="text-gray-700 bg-red-50 p-3 rounded-lg whitespace-pre-line border-l-4 border-red-500"
          >
            {{ caseData.clinical_history.allergies }}
          </div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Thuốc đang sử dụng
          </h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ caseData.clinical_history?.medications || "Chưa nhập" }}
          </div>
        </div>

        <div v-if="caseData.clinical_history?.review_systems" class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Hỏi bệnh theo hệ thống
          </h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ caseData.clinical_history.review_systems }}
          </div>
        </div>
      </div>

      <div>
        <h3
          class="text-xl font-bold text-gray-800 mb-3 border-b pb-2 flex items-center gap-2"
        >
          <i class="pi pi-heart text-gray-600" /> Khám lâm sàng
        </h3>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Tình trạng chung
          </h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{
              caseData.physical_examination?.general_appearance || "Chưa nhập"
            }}
          </div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Dấu hiệu sinh tồn
          </h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ formatVitalSigns() }}
          </div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Tim mạch</h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ caseData.physical_examination?.cardiovascular || "Chưa nhập" }}
          </div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Hô hấp</h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ caseData.physical_examination?.respiratory || "Chưa nhập" }}
          </div>
        </div>

        <div v-if="caseData.physical_examination?.abdominal" class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Bụng</h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ caseData.physical_examination.abdominal }}
          </div>
        </div>

        <div v-if="caseData.physical_examination?.neurological" class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Thần kinh</h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ caseData.physical_examination.neurological }}
          </div>
        </div>

        <div v-if="caseData.physical_examination?.musculoskeletal" class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Cơ xương khớp
          </h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ caseData.physical_examination.musculoskeletal }}
          </div>
        </div>

        <div v-if="caseData.physical_examination?.skin" class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Da</h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ caseData.physical_examination.skin }}
          </div>
        </div>

        <div v-if="caseData.physical_examination?.head_neck" class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Đầu và cổ</h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ caseData.physical_examination.head_neck }}
          </div>
        </div>
      </div>

      <div>
        <h3
          class="text-xl font-bold text-gray-800 mb-3 border-b pb-2 flex items-center gap-2"
        >
          <i class="pi pi-search text-gray-600" /> Cận lâm sàng
        </h3>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Xét nghiệm</h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line font-mono text-sm"
          >
            {{
              caseData.detailed_investigations?.laboratory_results ||
              "Chưa nhập"
            }}
          </div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Chẩn đoán hình ảnh
          </h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{
              caseData.detailed_investigations?.imaging_studies || "Chưa nhập"
            }}
          </div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Điện tâm đồ</h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ caseData.detailed_investigations?.ecg_findings || "Chưa nhập" }}
          </div>
        </div>

        <div
          v-if="
            caseData.detailed_investigations?.other_procedures ||
            caseData.investigations?.other_procedures
          "
          class="mb-4"
        >
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Thủ thuật khác
          </h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{
              caseData.detailed_investigations?.other_procedures ||
              caseData.investigations?.other_procedures
            }}
          </div>
        </div>

        <div
          v-if="
            caseData.detailed_investigations?.pathology_results ||
            caseData.investigations?.pathology_results
          "
          class="mb-4"
        >
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Kết quả giải phẫu bệnh
          </h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{
              caseData.detailed_investigations?.pathology_results ||
              caseData.investigations?.pathology_results
            }}
          </div>
        </div>
      </div>

      <div>
        <h3
          class="text-xl font-bold text-gray-800 mb-3 border-b pb-2 flex items-center gap-2"
        >
          <i class="pi pi-file text-gray-600" /> Chẩn đoán và điều trị
        </h3>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Chẩn đoán chính
          </h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{
              caseData.diagnosis_management?.primary_diagnosis || "Chưa nhập"
            }}
          </div>
        </div>

        <div
          v-if="caseData.diagnosis_management?.differential_diagnosis"
          class="mb-4"
        >
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Chẩn đoán phân biệt
          </h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ caseData.diagnosis_management.differential_diagnosis }}
          </div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Kế hoạch điều trị
          </h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ caseData.diagnosis_management?.treatment_plan || "Chưa nhập" }}
          </div>
        </div>

        <div
          v-if="caseData.diagnosis_management?.procedures_performed"
          class="mb-4"
        >
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Thủ thuật đã thực hiện
          </h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ caseData.diagnosis_management.procedures_performed }}
          </div>
        </div>

        <div v-if="caseData.diagnosis_management?.prognosis" class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Tiên lượng</h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ caseData.diagnosis_management.prognosis }}
          </div>
        </div>

        <div v-if="caseData.diagnosis_management?.follow_up_plan" class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Kế hoạch theo dõi
          </h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ caseData.diagnosis_management.follow_up_plan }}
          </div>
        </div>
      </div>

      <div v-if="caseData.attachments && caseData.attachments.length > 0">
        <h3
          class="text-xl font-bold text-gray-800 mb-3 border-b pb-2 flex items-center gap-2"
        >
          <i class="pi pi-paperclip text-gray-600" /> Tệp đính kèm y tế ({{
            caseData.attachments.length
          }})
        </h3>
        <div class="space-y-4">
          <div
            v-for="(file, index) in caseData.attachments"
            :key="index"
            class="border border-gray-200 rounded-lg p-4"
          >
            <div class="mb-3">
              <p
                class="font-semibold text-gray-900 mb-2 text-lg truncate"
                :title="file.title || file.name"
              >
                {{ file.title || file.name }}
              </p>

              <div class="w-full mb-3">
                <div
                  v-if="file.type?.startsWith('image/')"
                  class="w-full h-48 rounded-lg overflow-hidden border border-gray-200"
                >
                  <img
                    :src="file.url"
                    :alt="file.title || file.name"
                    class="w-full h-full object-cover"
                  />
                </div>
                <div
                  v-else
                  class="w-full h-48 rounded-lg bg-blue-100 flex items-center justify-center"
                >
                  <i class="pi pi-file text-blue-600" style="font-size: 4rem" />
                </div>
              </div>
            </div>

            <div class="bg-gray-50 p-3 rounded-lg space-y-2">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm">
                <div v-if="file.attachment_type">
                  <span class="font-medium text-gray-700">Loại tài liệu:</span>
                  <span class="text-gray-600 ml-1">{{
                    getAttachmentTypeLabel(file.attachment_type)
                  }}</span>
                </div>
                <div>
                  <span class="font-medium text-gray-700">Kích thước:</span>
                  <span class="text-gray-600 ml-1">{{
                    formatFileSize(file.size)
                  }}</span>
                </div>
                <div v-if="file.department">
                  <span class="font-medium text-gray-700">Khoa:</span>
                  <span class="text-gray-600 ml-1">{{
                    getDepartmentLabel(file.department)
                  }}</span>
                </div>
                <div v-if="file.date_taken">
                  <span class="font-medium text-gray-700">Ngày thực hiện:</span>
                  <span class="text-gray-600 ml-1">{{ file.date_taken }}</span>
                </div>
              </div>

              <div
                v-if="file.description"
                class="pt-2 border-t border-gray-200"
              >
                <span class="font-medium text-gray-700 text-sm">Mô tả:</span>
                <p class="text-gray-600 text-sm mt-1">{{ file.description }}</p>
              </div>

              <div
                v-if="file.physician_notes"
                class="pt-2 border-t border-gray-200"
              >
                <span class="font-medium text-gray-700 text-sm"
                  >Ghi chú bác sĩ:</span
                >
                <p class="text-gray-600 text-sm mt-1">
                  {{ file.physician_notes }}
                </p>
              </div>

              <div
                v-if="file.is_confidential"
                class="pt-2 border-t border-gray-200"
              >
                <Tag severity="danger">
                  <i class="pi pi-lock mr-1" /> Tài liệu bảo mật
                </Tag>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="caseData.learning_outcomes" class="border-t pt-6">
        <h2
          class="text-xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white p-3 rounded-lg flex items-center gap-2"
        >
          <i class="pi pi-graduation-cap" /> Mục tiêu học tập
        </h2>

        <div class="mb-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-2">Mục tiêu</h3>
          <div
            class="text-gray-700 bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500 whitespace-pre-line"
          >
            {{
              caseData.learning_outcomes.learning_objectives ||
              "Chưa có nội dung"
            }}
          </div>
        </div>

        <div class="mb-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-2">
            Khái niệm chính
          </h3>
          <div
            class="text-gray-700 bg-yellow-50 p-4 rounded-lg border-l-4 border-yellow-500 whitespace-pre-line"
          >
            {{ caseData.learning_outcomes.key_concepts || "Chưa có nội dung" }}
          </div>
        </div>

        <div class="mb-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-2">
            Điểm lưu ý lâm sàng
          </h3>
          <div
            class="text-gray-700 bg-purple-50 p-4 rounded-lg border-l-4 border-purple-500 whitespace-pre-line"
          >
            {{
              caseData.learning_outcomes.clinical_pearls || "Chưa có nội dung"
            }}
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <div
        class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 w-full"
      >
        <Button
          severity="secondary"
          outlined
          @click="$emit('close')"
          class="w-full sm:w-auto"
        >
          <i class="pi pi-arrow-left mr-2" /> Quay lại chỉnh sửa
        </Button>
        <div class="flex flex-col sm:flex-row gap-3">
          <Button
            severity="secondary"
            outlined
            @click="handlePrint"
            class="w-full sm:w-auto"
          >
            <i class="pi pi-print mr-2" /> In bệnh án
          </Button>
          <Button
            v-if="showSubmitButton"
            severity="primary"
            @click="$emit('submit')"
            class="w-full sm:w-auto"
          >
            <i class="pi pi-send mr-2" /> Xác nhận nộp bài
          </Button>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { useChoices } from "@/composables/useChoices";
import Button from "primevue/button";
import Tag from "primevue/tag";
import Dialog from "primevue/dialog";

const { formatGender, formatPriority, formatComplexity } = useChoices();

const props = defineProps({
  caseData: {
    type: Object,
    required: true,
  },
  showSubmitButton: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["close", "submit"]);

const handlePrint = () => {
  window.print();
};

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
};

const getAttachmentTypeLabel = (type: string) => {
  const labels: Record<string, string> = {
    x_ray: "Chụp X-quang",
    lab_report: "Phiếu xét nghiệm",
    ct_scan: "Chụp CT",
    mri_scan: "Chụp MRI",
    ultrasound: "Siêu âm",
    ekg_ecg: "Điện tâm đồ",
    other: "Khác",
  };
  return labels[type] || type;
};

const getDepartmentLabel = (dept: string) => {
  const labels: Record<string, string> = {
    cardiology: "Tim mạch",
    neurology: "Thần kinh",
    radiology: "Chẩn đoán hình ảnh",
    pathology: "Giải phẫu bệnh",
    emergency: "Cấp cứu",
    internal_medicine: "Nội khoa",
  };
  return labels[dept] || dept;
};

const formatVitalSigns = () => {
  const pe = props.caseData?.physical_examination;
  if (!pe) return "Chưa nhập";

  const parts = [];
  if (pe.vital_signs_temp) parts.push(`Nhiệt độ: ${pe.vital_signs_temp}°C`);
  if (pe.vital_signs_hr) parts.push(`Nhịp tim: ${pe.vital_signs_hr} bpm`);
  if (pe.vital_signs_bp) parts.push(`Huyết áp: ${pe.vital_signs_bp} mmHg`);
  if (pe.vital_signs_rr) parts.push(`Nhịp thở: ${pe.vital_signs_rr} /phút`);
  if (pe.vital_signs_spo2) parts.push(`SpO2: ${pe.vital_signs_spo2}%`);
  if (pe.weight_kg) parts.push(`Cân nặng: ${pe.weight_kg} kg`);
  if (pe.height_cm) parts.push(`Chiều cao: ${pe.height_cm} cm`);

  return parts.length > 0 ? parts.join("\n") : "Chưa nhập";
};

const formatSymptomOnset = (onset: string) => {
  const map: Record<string, string> = {
    sudden: "Đột ngột",
    gradual: "Từ từ",
    chronic: "Mạn tính",
  };
  return map[onset] || onset;
};

const formatSymptomProgression = (progression: string) => {
  const map: Record<string, string> = {
    improving: "Cải thiện",
    worsening: "Xấu đi",
    stable: "Ổn định",
    fluctuating: "Biến đổi",
  };
  return map[progression] || progression;
};
</script>

<style scoped>
@media print {
  .p-dialog-mask {
    position: static !important;
    background: transparent !important;
  }

  .p-dialog {
    max-height: none !important;
    box-shadow: none !important;
  }

  .p-dialog-footer {
    display: none !important;
  }
}
</style>
