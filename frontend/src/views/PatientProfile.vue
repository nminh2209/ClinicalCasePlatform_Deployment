<template>
  <div class="patient-profile-page space-y-6">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <ProgressSpinner
        style="width: 3rem; height: 3rem"
        strokeWidth="4"
        fill="transparent"
        animationDuration=".8s"
        aria-label="Đang tải hồ sơ bệnh nhân"
      />
    </div>

    <!-- Error State -->
    <div v-if="error && !loading" class="max-w-4xl mx-auto">
      <div class="bg-red-50 p-4 rounded-lg border border-red-200 mb-6">
        <p class="text-red-800 font-medium">{{ error }}</p>
        <Button
          label="Thử lại"
          severity="danger"
          outlined
          @click="loadPatientCase"
          class="mt-3"
        />
      </div>
    </div>

    <!-- Content -->
    <div v-else-if="caseData" class="max-w-4xl mx-auto">
      <!-- Header -->
      <div
        class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between mb-6"
      >
        <div class="flex items-center gap-3 sm:gap-4">
          <Button
            icon="pi pi-arrow-left"
            outlined
            rounded
            @click="router.push('/patients')"
            aria-label="Quay lại danh sách hồ sơ"
          />
          <div>
            <h1 class="text-2xl font-bold text-gray-800">
              Hồ sơ Y Tế Bệnh Nhân
            </h1>
          </div>
        </div>
        <div class="flex gap-2 justify-start sm:justify-end">
          <Button
            icon="pi pi-print"
            label="In Tóm Tắt"
            outlined
            @click="handlePrint"
          />
        </div>
      </div>

      <!-- Title and Specialty -->
      <div class="text-center border-b pb-4 mb-6">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">
          {{ caseData.title }}
        </h1>
        <Badge severity="secondary" class="text-lg px-4 py-2">{{
          caseData.specialty
        }}</Badge>
      </div>

      <!-- Patient Info Card -->
      <div class="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500 mb-6">
        <h3 class="text-lg font-semibold text-gray-800 mb-3">
          Thông Tin Bệnh Nhân
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
          <div>
            <span class="font-medium">Tên:</span>
            {{ caseData.patient_name || "Chưa nhập" }}
          </div>
          <div>
            <span class="font-medium">Tuổi:</span>
            {{ caseData.patient_age || "Chưa nhập" }}
          </div>
          <div>
            <span class="font-medium">Giới tính:</span>
            {{ formatGender(caseData.patient_gender) }}
          </div>
          <div>
            <span class="font-medium">Mã Hồ sơ Y Tế:</span>
            {{ caseData.medical_record_number || "Chưa nhập" }}
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
            {{ formatDate(caseData.admission_date) }}
          </div>
          <div v-if="caseData.discharge_date">
            <span class="font-medium">Ngày xuất viện:</span>
            {{ formatDate(caseData.discharge_date) }}
          </div>
          <div>
            <span class="font-medium">Trạng thái:</span>
            <span :class="getStatusClass(caseData.case_status)" class="ml-2">
              {{ formatStatus(caseData.case_status) }}
            </span>
          </div>
        </div>
      </div>

      <!-- Clinical History -->
      <div class="mb-6">
        <h3 class="text-xl font-bold text-gray-800 mb-3 border-b pb-2">
          Tiền Sử Bệnh Lý
        </h3>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Triệu chứng chính
          </h4>
          <p class="text-gray-700 bg-gray-50 p-3 rounded-lg">
            {{ caseData.clinical_history?.chief_complaint || "Chưa nhập" }}
          </p>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Tiền sử bệnh hiện tại
          </h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{
              caseData.clinical_history?.history_present_illness || "Chưa nhập"
            }}
          </div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Tiền sử bệnh quá khứ
          </h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ caseData.clinical_history?.past_medical_history || "Chưa nhập" }}
          </div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Thuốc hiện tại
          </h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ caseData.clinical_history?.medications || "Chưa nhập" }}
          </div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Dị ứng</h4>
          <p class="text-gray-700 bg-gray-50 p-3 rounded-lg">
            {{ caseData.clinical_history?.allergies || "Chưa nhập" }}
          </p>
        </div>
      </div>

      <!-- Physical Examination -->
      <div class="mb-6">
        <h3 class="text-xl font-bold text-gray-800 mb-3 border-b pb-2">
          Khám Lâm Sàng
        </h3>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Tổng Quan</h4>
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
            {{ caseData.physical_examination?.vital_signs || "Chưa nhập" }}
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
      </div>

      <!-- Investigations -->
      <div class="mb-6">
        <h3 class="text-xl font-bold text-gray-800 mb-3 border-b pb-2">
          Xét Nghiệm & Điều Tra
        </h3>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Kết Quả Xét Nghiệm
          </h4>
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
          <h4 class="text-md font-semibold text-gray-800 mb-2">Hình Ảnh</h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{
              caseData.detailed_investigations?.imaging_studies || "Chưa nhập"
            }}
          </div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">Điện Tâm Đồ</h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ caseData.detailed_investigations?.ecg_findings || "Chưa nhập" }}
          </div>
        </div>
      </div>

      <!-- Diagnosis & Management -->
      <div class="mb-6">
        <h3 class="text-xl font-bold text-gray-800 mb-3 border-b pb-2">
          Chẩn Đoán & Quản Lý
        </h3>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Chẩn Đoán Chính
          </h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{
              caseData.diagnosis_management?.primary_diagnosis || "Chưa nhập"
            }}
          </div>
        </div>

        <div class="mb-4">
          <h4 class="text-md font-semibold text-gray-800 mb-2">
            Kế Hoạch Điều Trị
          </h4>
          <div
            class="text-gray-700 bg-gray-50 p-3 rounded-lg whitespace-pre-line"
          >
            {{ caseData.diagnosis_management?.treatment_plan || "Chưa nhập" }}
          </div>
        </div>
      </div>

      <!-- Medical Attachments -->
      <div
        v-if="
          caseData.medical_attachments &&
          caseData.medical_attachments.length > 0
        "
        class="mb-6"
      >
        <h3 class="text-xl font-bold text-gray-800 mb-3 border-b pb-2">
          Tệp Đính Kèm Y Tế ({{ caseData.medical_attachments.length }})
        </h3>
        <div class="space-y-4">
          <div
            v-for="attachment in caseData.medical_attachments"
            :key="attachment.id"
            class="border border-gray-200 rounded-lg p-4"
          >
            <div class="mb-3">
              <p class="font-semibold text-gray-900 mb-2 text-lg">
                {{ attachment.title }}
              </p>
            </div>
            <div class="bg-gray-50 p-3 rounded-lg space-y-2">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm">
                <div v-if="attachment.attachment_type">
                  <span class="font-medium text-gray-700">Loại:</span>
                  <span class="text-gray-600 ml-1">{{
                    attachment.attachment_type_display
                  }}</span>
                </div>
                <div v-if="attachment.date_taken">
                  <span class="font-medium text-gray-700"
                    >Ngày Chụp/Ngày Tải Lên:</span
                  >
                  <span class="text-gray-600 ml-1">{{
                    formatDate(attachment.date_taken)
                  }}</span>
                </div>
              </div>
              <div
                v-if="attachment.description"
                class="pt-2 border-t border-gray-200"
              >
                <span class="font-medium text-gray-700 text-sm">Mô Tả:</span>
                <p class="text-gray-600 text-sm mt-1">
                  {{ attachment.description }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Learning Outcomes -->
      <div v-if="caseData.learning_outcomes" class="border-t pt-6">
        <h2
          class="!text-white text-xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 p-3 rounded-lg"
        >
          Kết Quả Học Tập
        </h2>

        <!-- Learning Objectives -->
        <div class="mb-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-2">
            Mục Tiêu Học Tập
          </h3>
          <div
            class="text-gray-700 bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500 whitespace-pre-line"
          >
            {{
              caseData.learning_outcomes.learning_objectives || "Chưa xác định"
            }}
          </div>
        </div>

        <!-- Key Concepts -->
        <div class="mb-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-2">
            Khái Niệm Chính
          </h3>
          <div
            class="text-gray-700 bg-yellow-50 p-4 rounded-lg border-l-4 border-yellow-500 whitespace-pre-line"
          >
            {{ caseData.learning_outcomes.key_concepts || "Chưa xác định" }}
          </div>
        </div>

        <!-- Clinical Pearls -->
        <div class="mb-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-2">Mẹo Lâm Sàng</h3>
          <div
            class="text-gray-700 bg-purple-50 p-4 rounded-lg border-l-4 border-purple-500 whitespace-pre-line"
          >
            {{ caseData.learning_outcomes.clinical_pearls || "Chưa xác định" }}
          </div>
        </div>

        <!-- References -->
        <div v-if="caseData.learning_outcomes.references" class="mb-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-2">
            Tài Liệu Tham Khảo
          </h3>
          <div
            class="text-gray-700 bg-green-50 p-4 rounded-lg border-l-4 border-green-500 whitespace-pre-line"
          >
            {{ caseData.learning_outcomes.references }}
          </div>
        </div>
      </div>
    </div>

    <!-- Error State -->
    <div v-else class="text-center py-12">
      <p class="text-gray-500">Không tìm thấy hồ sơ bệnh nhân</p>
      <Button outlined @click="router.push('/patients')" class="mt-4">
        Quay lại Hồ sơ Bệnh nhân
      </Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import Button from "primevue/button";
import Badge from "primevue/badge";
import ProgressSpinner from "primevue/progressspinner";
import { requireRoles } from "@/composables/useAuthorize";
import { casesService } from "@/services/cases";

const router = useRouter();
const route = useRoute();
requireRoles(["student", "instructor"]);

const loading = ref(false);
const caseData = ref<any>(null);
const error = ref<string | null>(null);

// Get case ID from route params
const caseId = route.params.id as string;

async function loadPatientCase() {
  if (!caseId) return;

  loading.value = true;
  error.value = null;
  try {
    caseData.value = await casesService.getCase(caseId);
  } catch (err) {
    // Log to backend error tracking
    logErrorToBackend(err, { caseId });

    // Show user-friendly message based on error type
    if (err instanceof Response && err.status === 404) {
      error.value = "Không tìm thấy hồ sơ bệnh nhân";
    } else if (err instanceof Response && err.status === 403) {
      error.value = "Bạn không có quyền truy cập hồ sơ này";
    } else if (err instanceof TypeError) {
      error.value = "Lỗi kết nối. Vui lòng kiểm tra kết nối mạng";
    } else {
      error.value = "Lỗi tải hồ sơ. Vui lòng thử lại";
    }
  } finally {
    loading.value = false;
  }
}

// Backend error logging function
async function logErrorToBackend(err: any, context: Record<string, any>) {
  try {
    // Only send non-sensitive info to your backend
    await fetch("/api/logs/errors", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: err?.message || "Unknown error",
        context,
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent,
      }),
    });
  } catch {
    // Silently fail
  }
}

onMounted(() => {
  loadPatientCase();
});

function formatDate(dateStr: string | null) {
  if (!dateStr) return "N/A";
  return new Date(dateStr).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

function formatGender(gender: string) {
  const genderMap: Record<string, string> = {
    male: "Nam",
    female: "Nữ",
    other: "Khác",
    not_specified: "Chưa xác định",
  };
  return genderMap[gender] || gender;
}

function formatStatus(status: string) {
  const statusMap: Record<string, string> = {
    draft: "Bản nháp",
    submitted: "Đã nộp",
    reviewed: "Đã xem xét",
    approved: "Đã phê duyệt",
  };
  return statusMap[status] || status;
}

function getStatusClass(status: string) {
  const classMap: Record<string, string> = {
    draft:
      "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800",
    submitted:
      "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800",
    reviewed:
      "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800",
    approved:
      "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800",
  };
  return (
    classMap[status] ||
    "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600"
  );
}

const handlePrint = () => {
  window.print();
};
</script>

<style scoped>
/* Patient Profile Page - CSS Variable Overrides */
.patient-profile-page {
  background: var(--background);
  min-height: 100vh;
  padding: 1.5rem;
}

/* Headers */
h1,
h2,
h3,
h4 {
  color: var(--foreground);
}

/* Text colors for Tailwind overrides */
:deep(.text-gray-800) {
  color: var(--foreground) !important;
}

:deep(.text-gray-700) {
  color: var(--foreground) !important;
}

:deep(.text-gray-600) {
  color: var(--muted-foreground) !important;
}

:deep(.text-gray-500) {
  color: var(--muted-foreground) !important;
}

/* Card backgrounds */
:deep(.bg-gray-50) {
  background: var(--secondary) !important;
}

:deep(.bg-blue-50) {
  background: var(--accent) !important;
}

/* Primary accent card */
:deep(.border-blue-500) {
  border-color: var(--primary) !important;
}

:deep(.border-blue-600) {
  border-color: var(--primary) !important;
}

/* Border colors */
:deep(.border-gray-200) {
  border-color: var(--border) !important;
}

/* Spinners */
:deep(.border-blue-600) {
  border-color: var(--primary) !important;
}

/* Status badges - using semantic colors for accessibility */
:deep(.bg-green-100) {
  background: rgba(16, 185, 129, 0.1) !important;
}

:deep(.text-green-800) {
  color: rgb(6, 95, 70) !important;
}

:deep(.bg-yellow-100) {
  background: rgba(245, 158, 11, 0.1) !important;
}

:deep(.text-yellow-800) {
  color: rgb(146, 64, 14) !important;
}

:deep(.bg-blue-100) {
  background: var(--accent) !important;
}

:deep(.text-blue-800) {
  color: var(--primary) !important;
}

/* Learning outcomes gradient header */
:deep(.from-blue-600) {
  --tw-gradient-from: var(--primary) !important;
}

:deep(.to-purple-600) {
  --tw-gradient-to: var(--chart-2) !important;
}

/* Print styles */
@media print {
  .patient-profile-page {
    background: white;
    padding: 0;
  }
}

@media (max-width: 640px) {
  .patient-profile-page {
    padding: 1rem;
  }
}
</style>
