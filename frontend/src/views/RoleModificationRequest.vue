<template>
  <div class="page-wrapper">
    <div class="page-header">
      <h1 class="page-title">Yêu cầu thay đổi vai trò</h1>
      <p class="page-subtitle">
        Điền đầy đủ thông tin để gửi yêu cầu trở thành Giảng viên đến quản trị
        viên hệ thống.
      </p>
    </div>

    <!-- Already-submitted banner -->
    <Message
      v-if="existingPending"
      severity="warn"
      :closable="false"
      class="mb-4"
    >
      Bạn đang có một yêu cầu <strong>đang chờ xét duyệt</strong>. Vui lòng đợi
      quản trị viên xử lý trước khi gửi yêu cầu mới.
    </Message>

    <!-- Past request history -->
    <div v-if="pastRequests.length > 0" class="history-card">
      <h2 class="section-title">Lịch sử yêu cầu</h2>
      <div v-for="req in pastRequests" :key="req.id" class="history-item">
        <div class="history-header">
          <span class="history-date">{{ formatDate(req.created_at) }}</span>
          <span :class="['status-badge', `status-${req.status}`]">
            {{ statusLabel(req.status) }}
          </span>
        </div>
        <p
          v-if="req.status === 'rejected' && req.rejection_reason"
          class="rejection-note"
        >
          <strong>Lý do từ chối:</strong> {{ req.rejection_reason }}
        </p>
      </div>
    </div>

    <!-- Request form -->
    <div v-if="!existingPending" class="form-card">
      <h2 class="section-title">Thông tin xác minh</h2>
      <p class="section-hint">
        Tất cả các trường có dấu <span class="required-star">*</span> đều bắt
        buộc. Thông tin này được sử dụng để xác minh danh tính và tư cách của
        bạn.
      </p>

      <form @submit.prevent="handleSubmit" novalidate>
        <!-- Full name -->
        <div class="form-group">
          <label class="form-label"
            >Họ và tên đầy đủ <span class="required-star">*</span></label
          >
          <InputText
            v-model="form.full_name"
            placeholder="Nguyễn Văn A"
            class="form-input"
            :class="{ 'input-error': errors.full_name }"
          />
          <p v-if="errors.full_name" class="field-error">
            {{ errors.full_name }}
          </p>
        </div>

        <!-- Email -->
        <div class="form-group">
          <label class="form-label"
            >Email <span class="required-star">*</span></label
          >
          <InputText
            v-model="form.email"
            type="email"
            placeholder="giang.vien@university.edu.vn"
            class="form-input"
            :class="{ 'input-error': errors.email }"
          />
          <p v-if="errors.email" class="field-error">{{ errors.email }}</p>
        </div>

        <!-- Student ID -->
        <div class="form-group">
          <label class="form-label"
            >Mã số sinh viên <span class="required-star">*</span></label
          >
          <InputText
            v-model="form.student_id"
            placeholder="SV2024001"
            class="form-input"
            :class="{ 'input-error': errors.student_id }"
          />
          <p v-if="errors.student_id" class="field-error">
            {{ errors.student_id }}
          </p>
        </div>

        <!-- Department -->
        <div class="form-group">
          <label class="form-label"
            >Khoa / Bộ môn <span class="required-star">*</span></label
          >
          <Select
            v-model="form.department"
            :options="departmentOptions"
            optionLabel="label"
            optionValue="value"
            placeholder="Chọn khoa / bộ môn"
            class="form-input"
            :loading="deptLoading"
            :class="{ 'input-error': errors.department }"
          />
          <p v-if="errors.department" class="field-error">
            {{ errors.department }}
          </p>
        </div>

        <!-- Specialty -->
        <div class="form-group">
          <label class="form-label"
            >Chuyên ngành / Lĩnh vực <span class="required-star">*</span></label
          >
          <InputText
            v-model="form.specialty"
            placeholder="VD: Nội khoa, Ngoại khoa, Nhi khoa…"
            class="form-input"
            :class="{ 'input-error': errors.specialty }"
          />
          <p v-if="errors.specialty" class="field-error">
            {{ errors.specialty }}
          </p>
        </div>

        <!-- Employee ID (optional) -->
        <div class="form-group">
          <label class="form-label"
            >Mã nhân viên / Mã giảng viên (nếu có)</label
          >
          <InputText
            v-model="form.employee_id"
            placeholder="GV2024001"
            class="form-input"
          />
        </div>

        <!-- Institution (optional) -->
        <div class="form-group">
          <label class="form-label">Đơn vị công tác / Bệnh viện (nếu có)</label>
          <InputText
            v-model="form.institution"
            placeholder="Bệnh viện Chợ Rẫy"
            class="form-input"
          />
        </div>

        <!-- Reason -->
        <div class="form-group">
          <label class="form-label">
            Lý do yêu cầu thay đổi vai trò <span class="required-star">*</span>
          </label>
          <Textarea
            v-model="form.reason"
            placeholder="Mô tả lý do bạn cần trở thành Giảng viên, kinh nghiệm giảng dạy, vị trí công tác…"
            rows="5"
            class="form-input"
            :class="{ 'input-error': errors.reason }"
            style="resize: vertical"
          />
          <p v-if="errors.reason" class="field-error">{{ errors.reason }}</p>
        </div>

        <!-- Server error -->
        <Message
          v-if="serverError"
          severity="error"
          :closable="false"
          class="mb-3"
        >
          {{ serverError }}
        </Message>

        <Button
          type="submit"
          label="Gửi yêu cầu"
          icon="pi pi-send"
          icon-pos="right"
          class="submit-btn"
          :loading="submitting"
          :disabled="submitting"
        />
      </form>
    </div>

    <!-- Success dialog -->
    <Dialog
      v-model:visible="showSuccess"
      header="Gửi yêu cầu thành công"
      :modal="true"
      :closable="false"
      style="max-width: 420px; width: 95vw"
    >
      <div class="success-dialog-body">
        <i class="pi pi-check-circle success-icon" />
        <p>
          Yêu cầu của bạn đã được gửi đến quản trị viên. Bạn sẽ nhận được thông
          báo qua
          <strong>Trung tâm thông báo</strong> khi yêu cầu được xử lý.
        </p>
      </div>
      <template #footer>
        <Button label="Đóng" @click="showSuccess = false" />
      </template>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import api from "@/services/api";
import { useAuthStore } from "@/stores/auth";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import InputText from "primevue/inputtext";
import Message from "primevue/message";
import Select from "primevue/select";
import Textarea from "primevue/textarea";

const authStore = useAuthStore();

const form = ref({
  full_name: "",
  email: "",
  student_id: "",
  department: null as number | null,
  specialty: "",
  employee_id: "",
  institution: "",
  reason: "",
});

const errors = ref<Record<string, string>>({});
const serverError = ref("");
const submitting = ref(false);
const showSuccess = ref(false);
const existingPending = ref(false);
const pastRequests = ref<any[]>([]);
const departmentOptions = ref<{ label: string; value: number }[]>([]);
const deptLoading = ref(false);

const prefillUserData = () => {
  const user = authStore.user;
  if (user) {
    form.value.full_name =
      user.full_name || `${user.last_name} ${user.first_name}`.trim();
    form.value.email = user.email || "";
    form.value.student_id = user.student_id || "";
    if (user.department) {
      form.value.department = user.department;
    }
  }
};

const loadDepartments = async () => {
  deptLoading.value = true;
  try {
    const response = await api.get("/cases/departments/");
    const data = response.data?.results || response.data || [];
    departmentOptions.value = (Array.isArray(data) ? data : [])
      .filter((d: any) => d && d.id)
      .map((d: any) => ({ label: d.vietnamese_name || d.name, value: d.id }));
  } catch {
    departmentOptions.value = [];
  } finally {
    deptLoading.value = false;
  }
};

const loadMyRequests = async () => {
  try {
    const response = await api.get("/auth/role-requests/my/");
    const all: any[] = response.data?.results || response.data || [];
    pastRequests.value = all;
    existingPending.value = all.some((r: any) => r.status === "pending");
  } catch {
    pastRequests.value = [];
  }
};

const validate = (): boolean => {
  const e: Record<string, string> = {};
  if (!form.value.full_name.trim())
    e.full_name = "Vui lòng nhập họ và tên đầy đủ.";
  if (!form.value.email.trim()) {
    e.email = "Vui lòng nhập email.";
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
    e.email = "Địa chỉ email không hợp lệ.";
  }
  if (!form.value.student_id.trim())
    e.student_id = "Vui lòng nhập mã số sinh viên.";
  if (!form.value.department) e.department = "Vui lòng chọn khoa / bộ môn.";
  if (!form.value.specialty.trim())
    e.specialty = "Vui lòng nhập chuyên ngành / lĩnh vực.";
  if (!form.value.reason.trim() || form.value.reason.trim().length < 30) {
    e.reason = "Vui lòng mô tả lý do (ít nhất 30 ký tự).";
  }
  errors.value = e;
  return Object.keys(e).length === 0;
};

const handleSubmit = async () => {
  serverError.value = "";
  if (!validate()) return;

  submitting.value = true;
  try {
    await api.post("/auth/role-requests/", {
      full_name: form.value.full_name.trim(),
      email: form.value.email.trim(),
      student_id: form.value.student_id.trim(),
      department: form.value.department,
      specialty: form.value.specialty.trim(),
      employee_id: form.value.employee_id.trim(),
      institution: form.value.institution.trim(),
      reason: form.value.reason.trim(),
    });

    showSuccess.value = true;
    existingPending.value = true;
  } catch (err: any) {
    const data = err.response?.data;
    if (data && typeof data === "object") {
      const first = Object.values(data)[0];
      serverError.value = Array.isArray(first)
        ? String(first[0])
        : String(first);
    } else {
      serverError.value = "Gửi yêu cầu thất bại. Vui lòng thử lại.";
    }
  } finally {
    submitting.value = false;
  }
};

const statusLabel = (s: string) => {
  return (
    { pending: "Đang chờ", approved: "Đã chấp thuận", rejected: "Đã từ chối" }[
      s
    ] ?? s
  );
};

const formatDate = (iso: string) => {
  return new Date(iso).toLocaleDateString("vi-VN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
};

onMounted(async () => {
  prefillUserData();
  await Promise.all([loadDepartments(), loadMyRequests()]);
});
</script>

<style scoped>
.page-wrapper {
  max-width: 720px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

.page-header {
  margin-bottom: 1.5rem;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--foreground);
  margin-bottom: 0.5rem;
}

.page-subtitle {
  font-size: 0.9375rem;
  color: var(--muted-foreground);
}

.history-card,
.form-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--foreground);
  margin-bottom: 0.5rem;
}

.section-hint {
  font-size: 0.875rem;
  color: var(--muted-foreground);
  margin-bottom: 1.5rem;
}

.history-item {
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border);
}

.history-item:last-child {
  border-bottom: none;
}

.history-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.25rem;
}

.history-date {
  font-size: 0.875rem;
  color: var(--muted-foreground);
}

.status-badge {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 2px 10px;
  border-radius: 999px;
}

.status-pending {
  background: #fef9c3;
  color: #854d0e;
}

.status-approved {
  background: #dcfce7;
  color: #166534;
}

.status-rejected {
  background: #fee2e2;
  color: #991b1b;
}

.rejection-note {
  font-size: 0.875rem;
  color: #7f1d1d;
  margin-top: 0.25rem;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--foreground);
}

.required-star {
  color: #ef4444;
  margin-left: 2px;
}

.form-input {
  width: 100%;
}

:deep(.form-input.p-inputtext),
:deep(.form-input .p-inputtext),
:deep(.form-input.p-select),
:deep(.form-input textarea) {
  border-radius: 10px !important;
  border: 2px solid var(--border) !important;
  background: var(--input-background) !important;
  color: var(--foreground) !important;
  font-size: 0.9375rem !important;
  transition: border-color 0.2s !important;
}

:deep(.form-input.p-inputtext:focus),
:deep(.form-input .p-inputtext:focus),
:deep(.form-input textarea:focus) {
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 3px var(--shadow-blue) !important;
}

:deep(.input-error.p-inputtext),
:deep(.input-error .p-inputtext),
:deep(.input-error.p-select),
:deep(.input-error textarea) {
  border-color: #ef4444 !important;
}

.field-error {
  font-size: 0.8125rem;
  color: #ef4444;
}

.submit-btn {
  align-self: flex-start;
  padding: 0.75rem 2rem !important;
  font-weight: 600 !important;
  border-radius: 10px !important;
}

.success-dialog-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 1rem 0;
  text-align: center;
}

.success-icon {
  font-size: 3rem;
  color: #16a34a;
}

.mb-3 {
  margin-bottom: 0.75rem;
}

.mb-4 {
  margin-bottom: 1rem;
}
</style>
