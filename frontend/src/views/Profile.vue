<template>
  <div class="profile-page">
    <!-- Page Header -->
    <div class="page-header">
      <h1 class="page-title">Hồ sơ cá nhân</h1>
      <p class="page-subtitle">Quản lý thông tin tài khoản và mật khẩu</p>
    </div>

    <div class="profile-grid">
      <!-- ── Left column: avatar + read-only summary ── -->
      <div class="profile-sidebar">
        <div class="avatar-card">
          <div class="avatar-wrapper">
            <Avatar
              :label="userInitials"
              shape="circle"
              size="xlarge"
              class="profile-avatar"
            />
          </div>
          <h2 class="sidebar-name">
            {{ user?.first_name }} {{ user?.last_name }}
          </h2>
          <span class="role-badge" :class="roleBadgeClass">{{
            roleLabel
          }}</span>
          <p class="sidebar-email">{{ user?.email }}</p>
          <div v-if="departmentLabel" class="sidebar-dept">
            <i class="pi pi-building" />
            {{ departmentLabel }}
          </div>
        </div>
      </div>

      <!-- ── Right column: edit forms ── -->
      <div class="profile-forms">
        <!-- Personal Info -->
        <div class="form-card">
          <h3 class="card-title">
            <i class="pi pi-user" />
            Thông tin cá nhân
          </h3>

          <form @submit.prevent="saveProfile" class="form-body">
            <div class="form-row">
              <div class="form-group">
                <label class="form-label"
                  >Họ <span class="required">*</span></label
                >
                <InputText
                  v-model="profileForm.first_name"
                  class="form-input"
                  required
                />
              </div>
              <div class="form-group">
                <label class="form-label"
                  >Tên <span class="required">*</span></label
                >
                <InputText
                  v-model="profileForm.last_name"
                  class="form-input"
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <label class="form-label"
                >Tên đăng nhập <span class="required">*</span></label
              >
              <InputText
                v-model="profileForm.username"
                class="form-input"
                required
              />
            </div>

            <div class="form-group">
              <label class="form-label">Email</label>
              <InputText :value="user?.email" class="form-input" disabled />
              <p class="form-hint">Email không thể thay đổi</p>
            </div>

            <div class="form-group">
              <label class="form-label">Số điện thoại</label>
              <InputText
                v-model="profileForm.phone_number"
                class="form-input"
                placeholder="VD: 0912345678"
              />
            </div>

            <div class="form-group">
              <label class="form-label">Khoa / Bộ môn</label>
              <Select
                v-model="profileForm.department"
                :options="departmentOptions"
                optionLabel="label"
                optionValue="value"
                placeholder="Chọn khoa"
                class="form-input"
                showClear
              />
            </div>

            <div v-if="user?.role === 'instructor'" class="form-group">
              <label class="form-label">Chuyên ngành</label>
              <InputText
                v-model="profileForm.specialization"
                class="form-input"
                placeholder="VD: Nội tim mạch"
              />
            </div>

            <div v-if="user?.role === 'student'" class="form-group">
              <label class="form-label">Mã sinh viên</label>
              <InputText
                v-model="profileForm.student_id"
                class="form-input"
                placeholder="SV2024001"
              />
            </div>

            <div
              v-if="user?.role === 'instructor' || user?.role === 'admin'"
              class="form-group"
            >
              <label class="form-label">Mã nhân viên</label>
              <InputText
                v-model="profileForm.employee_id"
                class="form-input"
                placeholder="GV2024001"
              />
            </div>

            <div v-if="user?.role === 'student'" class="form-group">
              <label class="form-label">Năm học</label>
              <InputText
                v-model="profileForm.academic_year"
                class="form-input"
                placeholder="VD: 2024-2025"
              />
            </div>

            <div class="form-group">
              <label class="form-label">Giới thiệu bản thân</label>
              <Textarea
                v-model="profileForm.bio"
                rows="3"
                class="form-input"
                placeholder="Mô tả ngắn về bản thân..."
                autoResize
              />
            </div>

            <div class="form-group">
              <label class="form-label">Ngôn ngữ hiển thị</label>
              <Select
                v-model="profileForm.language_preference"
                :options="languageOptions"
                optionLabel="label"
                optionValue="value"
                class="form-input"
              />
            </div>

            <!-- Inline feedback — replaces .alert divs with PrimeVue Message -->
            <!-- globals.css does not define .p-message colours, so we force
                 them to match the design system via scoped :deep overrides. -->
            <Message
              v-if="profileSuccess"
              severity="success"
              :closable="false"
              class="feedback-msg"
            >
              {{ profileSuccess }}
            </Message>
            <Message
              v-if="profileError"
              severity="error"
              :closable="false"
              class="feedback-msg"
            >
              {{ profileError }}
            </Message>

            <div class="form-actions">
              <Button
                type="submit"
                label="Lưu thông tin"
                icon="pi pi-save"
                :loading="savingProfile"
              />
            </div>
          </form>
        </div>

        <!-- Change Password -->
        <div class="form-card">
          <h3 class="card-title">
            <i class="pi pi-lock" />
            Đổi mật khẩu
          </h3>

          <form @submit.prevent="submitChangePassword" class="form-body">
            <div class="form-group">
              <label class="form-label"
                >Mật khẩu hiện tại <span class="required">*</span></label
              >
              <Password
                v-model="passwordForm.current_password"
                :feedback="false"
                toggleMask
                fluid
                required
                placeholder="Nhập mật khẩu hiện tại"
              />
            </div>

            <div class="form-group">
              <label class="form-label"
                >Mật khẩu mới <span class="required">*</span></label
              >
              <Password
                v-model="passwordForm.new_password"
                toggleMask
                fluid
                required
                placeholder="Tối thiểu 8 ký tự"
              />
            </div>

            <div class="form-group">
              <label class="form-label"
                >Xác nhận mật khẩu mới <span class="required">*</span></label
              >
              <Password
                v-model="passwordForm.new_password_confirm"
                :feedback="false"
                toggleMask
                fluid
                required
                placeholder="Nhập lại mật khẩu mới"
              />
            </div>

            <!-- Password feedback Messages -->
            <Message
              v-if="passwordSuccess"
              severity="success"
              :closable="false"
              class="feedback-msg"
            >
              {{ passwordSuccess }}
            </Message>
            <Message
              v-if="passwordError"
              severity="error"
              :closable="false"
              class="feedback-msg"
            >
              {{ passwordError }}
            </Message>

            <div class="form-actions">
              <Button
                type="submit"
                label="Đổi mật khẩu"
                icon="pi pi-key"
                severity="warning"
                :loading="savingPassword"
              />
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import api from "@/services/api";
import Avatar from "primevue/avatar";
import Button from "primevue/button";
import InputText from "primevue/inputtext";
import Password from "primevue/password";
import Select from "primevue/select";
import Textarea from "primevue/textarea";
import Message from "primevue/message";

const authStore = useAuthStore();
const user = computed(() => authStore.user);

const profileForm = ref({
  first_name: "",
  last_name: "",
  username: "",
  phone_number: "",
  department: null as number | null,
  specialization: "",
  student_id: "",
  employee_id: "",
  academic_year: "",
  bio: "",
  language_preference: "vi",
});

const savingProfile = ref(false);
const profileSuccess = ref("");
const profileError = ref("");

const passwordForm = ref({
  current_password: "",
  new_password: "",
  new_password_confirm: "",
});

const savingPassword = ref(false);
const passwordSuccess = ref("");
const passwordError = ref("");

const departmentOptions = ref<{ label: string; value: number }[]>([]);

const languageOptions = [
  { label: "Tiếng Việt", value: "vi" },
  { label: "English", value: "en" },
];

const userInitials = computed(() => {
  const f = user.value?.first_name?.[0] ?? "";
  const l = user.value?.last_name?.[0] ?? "";
  return (f + l).toUpperCase() || "U";
});

const roleLabel = computed(() => {
  const map: Record<string, string> = {
    student: "Sinh viên",
    instructor: "Giảng viên",
    admin: "Quản trị viên",
  };
  return map[user.value?.role ?? ""] ?? "";
});

const roleBadgeClass = computed(() => {
  const map: Record<string, string> = {
    student: "badge-student",
    instructor: "badge-instructor",
    admin: "badge-admin",
  };
  return map[user.value?.role ?? ""] ?? "";
});

const departmentLabel = computed(() => {
  const id = user.value?.department;
  if (!id) return "";
  const found = departmentOptions.value.find((d) => d.value === id);
  return (
    found?.label ??
    user.value?.department_vietnamese_name ??
    user.value?.department_name ??
    ""
  );
});

function populateForm() {
  const u = user.value;
  if (!u) return;
  profileForm.value = {
    first_name: u.first_name ?? "",
    last_name: u.last_name ?? "",
    username: u.username ?? "",
    phone_number: u.phone_number ?? "",
    department: u.department ?? null,
    specialization: u.specialization ?? "",
    student_id: u.student_id ?? "",
    employee_id: u.employee_id ?? "",
    academic_year: u.academic_year ?? "",
    bio: u.bio ?? "",
    language_preference: u.language_preference ?? "vi",
  };
}

async function loadDepartments() {
  try {
    const res = await api.get("/cases/departments/");
    const data = res.data?.results || res.data || [];
    departmentOptions.value = (Array.isArray(data) ? data : [])
      .filter((d: any) => d?.id)
      .map((d: any) => ({ label: d.vietnamese_name || d.name, value: d.id }));
  } catch {
    departmentOptions.value = [];
  }
}

async function saveProfile() {
  savingProfile.value = true;
  profileSuccess.value = "";
  profileError.value = "";
  try {
    await authStore.updateProfile({ ...profileForm.value });
    profileSuccess.value = "Thông tin đã được cập nhật thành công";
  } catch (err: any) {
    const data = err.response?.data;
    profileError.value =
      data && typeof data === "object"
        ? Object.values(data).flat().join(" ")
        : "Cập nhật thất bại. Vui lòng thử lại.";
  } finally {
    savingProfile.value = false;
  }
}

async function submitChangePassword() {
  passwordSuccess.value = "";
  passwordError.value = "";

  if (
    passwordForm.value.new_password !== passwordForm.value.new_password_confirm
  ) {
    passwordError.value = "Mật khẩu mới không khớp";
    return;
  }
  if (passwordForm.value.new_password.length < 8) {
    passwordError.value = "Mật khẩu mới phải có ít nhất 8 ký tự";
    return;
  }

  savingPassword.value = true;
  try {
    await authStore.changePassword({ ...passwordForm.value });
    passwordSuccess.value = "Mật khẩu đã được thay đổi thành công";
    passwordForm.value = {
      current_password: "",
      new_password: "",
      new_password_confirm: "",
    };
  } catch (err: any) {
    const data = err.response?.data;
    passwordError.value =
      data && typeof data === "object"
        ? Object.values(data).flat().join(" ")
        : "Đổi mật khẩu thất bại. Vui lòng kiểm tra lại.";
  } finally {
    savingPassword.value = false;
  }
}

onMounted(async () => {
  await Promise.all([loadDepartments(), authStore.refreshUser()]);
  populateForm();
});
</script>

<style scoped>
.profile-page {
  padding: 1.5rem;
  max-width: 1100px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 1.5rem;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--foreground);
}

.page-subtitle {
  color: var(--muted-foreground);
  margin-top: 0.25rem;
}

.profile-grid {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 1.5rem;
  align-items: start;
}

@media (max-width: 768px) {
  .profile-grid {
    grid-template-columns: 1fr;
  }
}

.avatar-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  padding: 1.5rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.avatar-wrapper {
  margin-bottom: 0.5rem;
}

/* Override PrimeVue Avatar default colours to use the primary blue.
   globals.css does not define .p-avatar, so we add it here. */
:deep(.profile-avatar.p-avatar) {
  width: 80px;
  height: 80px;
  font-size: 1.75rem;
  font-weight: 700;
  background: var(--primary);
  color: var(--primary-foreground);
}

.sidebar-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--foreground);
}

.sidebar-email {
  font-size: 0.875rem;
  color: var(--muted-foreground);
  word-break: break-all;
}

.sidebar-dept {
  font-size: 0.875rem;
  color: var(--foreground);
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.role-badge {
  display: inline-block;
  padding: 0.2rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.badge-student {
  background: #dbeafe;
  color: #1d4ed8;
}
.badge-instructor {
  background: #dcfce7;
  color: #15803d;
}
.badge-admin {
  background: #fef3c7;
  color: #92400e;
}

.profile-forms {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  padding: 1.5rem;
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--foreground);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border);
}

.card-title i {
  color: var(--primary);
}

.form-body {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 480px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--foreground);
}

.required {
  color: var(--destructive);
  margin-left: 2px;
}

.form-input {
  width: 100%;
}

.form-hint {
  font-size: 0.75rem;
  color: var(--muted-foreground);
  margin-top: 0.2rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 0.5rem;
}

/* Message feedback — ensure colours match globals.css design tokens.
   PrimeVue Message uses its own colour system, so we pin it here. */
.feedback-msg {
  width: 100%;
}

:deep(.feedback-msg.p-message-success) {
  background-color: #f0fdf4 !important;
  color: #15803d !important;
  border: 1px solid #bbf7d0 !important;
}

:deep(.feedback-msg.p-message-error) {
  background-color: #fef2f2 !important;
  color: #b91c1c !important;
  border: 1px solid #fecaca !important;
}
</style>
