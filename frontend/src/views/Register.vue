<template>
  <div class="register-page">
    <div class="register-container">
      <!-- Top Navigation Bar -->
      <div class="top-nav-bar">
        <router-link to="/" class="back-button">
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M19 12H5M12 19l-7-7 7-7" />
          </svg>
          <span>Quay lại Trang chủ</span>
        </router-link>
      </div>

      <div class="register-form-wrapper">
        <div class="form-header">
          <h2 class="form-title">Đăng ký tài khoản</h2>
          <p class="form-subtitle">Tạo tài khoản mới để truy cập hệ thống</p>
        </div>

        <!-- Success Message — PrimeVue Message -->
        <Message
          v-if="successMessage"
          severity="success"
          :closable="false"
          class="feedback-message"
        >
          {{ successMessage }}
        </Message>

        <!-- Registration Form -->
        <form @submit.prevent="handleSubmit" class="register-form">
          <!-- Email -->
          <div class="form-group">
            <label for="email" class="form-label">Email</label>
            <InputText
              id="email"
              v-model="formData.email"
              type="email"
              placeholder="your.email@university.edu"
              class="form-input"
              required
            />
          </div>

          <!-- Username -->
          <div class="form-group">
            <label for="username" class="form-label">Tên đăng nhập</label>
            <InputText
              id="username"
              v-model="formData.username"
              type="text"
              placeholder="username"
              class="form-input"
              required
            />
          </div>

          <!-- Name Fields -->
          <div class="form-row">
            <div class="form-group">
              <label for="first_name" class="form-label">Tên</label>
              <InputText
                id="first_name"
                v-model="formData.first_name"
                type="text"
                placeholder="Nguyễn"
                class="form-input"
                required
              />
            </div>

            <div class="form-group">
              <label for="last_name" class="form-label">Họ</label>
              <InputText
                id="last_name"
                v-model="formData.last_name"
                type="text"
                placeholder="Văn A"
                class="form-input"
                required
              />
            </div>
          </div>

          <!-- Role Selection -->
          <div class="form-group">
            <label for="role" class="form-label">Vai trò</label>
            <Select
              id="role"
              v-model="formData.role"
              :options="roleOptions"
              optionLabel="label"
              optionValue="value"
              placeholder="Chọn vai trò"
              class="form-input"
              required
            />
          </div>

          <!-- Department Selection -->
          <div class="form-group">
            <label for="department" class="form-label">Khoa / Bộ môn</label>
            <Select
              id="department"
              v-model="formData.department"
              :options="departmentOptions"
              optionLabel="label"
              optionValue="value"
              placeholder="Chọn khoa (có thể bỏ qua)"
              class="form-input"
              :loading="departmentsLoading"
              showClear
            />
          </div>

          <!-- Student ID (conditional) -->
          <div v-if="formData.role === 'student'" class="form-group">
            <label for="student_id" class="form-label">Mã sinh viên</label>
            <InputText
              id="student_id"
              v-model="formData.student_id"
              type="text"
              placeholder="SV2024001"
              class="form-input"
            />
          </div>

          <!-- Employee ID (conditional) -->
          <div v-if="formData.role === 'instructor'" class="form-group">
            <label for="employee_id" class="form-label">Mã giảng viên</label>
            <InputText
              id="employee_id"
              v-model="formData.employee_id"
              type="text"
              placeholder="GV2024001"
              class="form-input"
            />
          </div>

          <!-- Password -->
          <div class="form-group">
            <label for="password" class="form-label">Mật khẩu</label>
            <Password
              id="password"
              v-model="formData.password"
              placeholder="Nhập mật khẩu"
              toggleMask
              showClear
              fluid
              :feedback="false"
              required
            />
            <p class="form-hint">
              Tối thiểu 8 ký tự, bao gồm chữ hoa, chữ thường và số
            </p>
          </div>

          <!-- Password Confirmation -->
          <div class="form-group">
            <label for="password_confirm" class="form-label"
              >Xác nhận mật khẩu</label
            >
            <Password
              id="password_confirm"
              fluid
              v-model="formData.password_confirm"
              placeholder="Nhập lại mật khẩu"
              toggleMask
              showClear
              :feedback="false"
              required
            />
          </div>

          <!-- Error Message — PrimeVue Message -->
          <Message
            v-if="error"
            severity="error"
            :closable="false"
            class="feedback-message"
          >
            {{ error }}
          </Message>

          <!-- Submit Button -->
          <Button
            type="submit"
            class="submit-button"
            :disabled="
              loading ||
              !formData.role ||
              !formData.email ||
              !formData.username ||
              !formData.first_name ||
              !formData.last_name ||
              !formData.password ||
              !formData.password_confirm
            "
            :loading="loading"
            :label="loading ? 'Đang tạo tài khoản...' : 'Đăng ký'"
            :icon="loading ? '' : 'pi pi-check'"
            icon-pos="right"
          />
        </form>

        <!-- Login Link -->
        <Divider class="footer-divider" />
        <div class="footer-links">
          <p>
            Đã có tài khoản?
            <router-link to="/login" class="link"
              >Quay lại trang đăng nhập</router-link
            >
          </p>
        </div>

        <Divider class="footer-divider" />
        <div class="copyright">
          <p>Bản quyền thuộc về © 2025-2026 MedCase Team.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "@/services/api";
import Button from "primevue/button";
import Divider from "primevue/divider";
import InputText from "primevue/inputtext";
import Message from "primevue/message";
import Password from "primevue/password";
import Select from "primevue/select";

const router = useRouter();

const formData = ref({
  email: "",
  username: "",
  first_name: "",
  last_name: "",
  role: "",
  department: null as number | null,
  student_id: "",
  employee_id: "",
  password: "",
  password_confirm: "",
});

const error = ref("");
const successMessage = ref("");
const loading = ref(false);
const departmentsLoading = ref(false);
const departmentOptions = ref<{ label: string; value: number }[]>([]);

const roleOptions = [
  { label: "Sinh viên", value: "student" },
  { label: "Giảng viên", value: "instructor" },
];

const loadDepartments = async () => {
  departmentsLoading.value = true;
  try {
    const response = await api.get("/cases/departments/");
    const data = response.data?.results || response.data || [];
    departmentOptions.value = (Array.isArray(data) ? data : [])
      .filter((d: any) => d && d.id)
      .map((d: any) => ({
        label: d.vietnamese_name || d.name,
        value: d.id,
      }));
  } catch {
    departmentOptions.value = [];
  } finally {
    departmentsLoading.value = false;
  }
};

onMounted(loadDepartments);

const handleSubmit = async () => {
  loading.value = true;
  error.value = "";
  successMessage.value = "";

  if (formData.value.password !== formData.value.password_confirm) {
    error.value = "Mật khẩu xác nhận không khớp";
    loading.value = false;
    return;
  }

  if (formData.value.password.length < 8) {
    error.value = "Mật khẩu phải có ít nhất 8 ký tự";
    loading.value = false;
    return;
  }

  try {
    const payload: any = {
      email: formData.value.email,
      username: formData.value.username,
      first_name: formData.value.first_name,
      last_name: formData.value.last_name,
      role: formData.value.role,
      password: formData.value.password,
      password_confirm: formData.value.password_confirm,
    };

    if (formData.value.role === "student" && formData.value.student_id) {
      payload.student_id = formData.value.student_id;
    }
    if (formData.value.role === "instructor" && formData.value.employee_id) {
      payload.employee_id = formData.value.employee_id;
    }
    if (formData.value.department) {
      payload.department = formData.value.department;
    }

    await api.post("/auth/register/", payload);

    successMessage.value =
      "Đăng ký thành công! Đang chuyển đến trang đăng nhập...";

    setTimeout(() => {
      router.push("/login");
    }, 2000);
  } catch (err: any) {
    if (err.response?.data) {
      const errors = err.response.data;
      if (typeof errors === "object") {
        const firstError = Object.values(errors)[0];
        error.value = Array.isArray(firstError)
          ? firstError[0]
          : String(firstError);
      } else {
        error.value = String(errors);
      }
    } else {
      error.value = "Đăng ký thất bại. Vui lòng thử lại sau.";
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
  background: var(--background);
  color: var(--foreground);
}

.register-container {
  width: 100%;
  max-width: 580px;
  position: relative;
}

.top-nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: var(--card);
  color: var(--muted-foreground);
  border-radius: 12px;
  font-weight: 500;
  font-size: 0.9375rem;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px var(--shadow-grey);
  border: 1px solid var(--border);
}

.back-button:hover {
  background: var(--secondary);
  transform: translateX(-4px);
  box-shadow: 0 4px 12px var(--shadow-grey);
  color: var(--foreground);
}

.back-button svg {
  transition: transform 0.3s ease;
}

.back-button:hover svg {
  transform: translateX(-2px);
}

.register-form-wrapper {
  background: var(--card);
  border-radius: 24px;
  padding: 3rem;
  box-shadow: 0 8px 24px var(--shadow-grey);
  border: 1px solid var(--border);
  position: relative;
}

.form-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.form-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--foreground);
  margin-bottom: 0.75rem;
  letter-spacing: -0.02em;
}

.form-subtitle {
  font-size: 1rem;
  color: var(--muted-foreground);
  line-height: 1.5;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--foreground);
  margin-bottom: 0.25rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem !important;
  font-size: 0.9375rem !important;
  border-radius: 12px !important;
  border: 2px solid var(--border) !important;
  background: var(--input-background) !important;
  color: var(--foreground) !important;
  transition: all 0.3s ease !important;
}

.form-input:hover {
  border-color: var(--primary) !important;
  background: var(--card) !important;
}

.form-input:focus {
  outline: none !important;
  border-color: var(--primary) !important;
  background: var(--card) !important;
  box-shadow: 0 0 0 3px var(--shadow-blue) !important;
}

/* PrimeVue Password */
:deep(.p-password .p-password-input) {
  padding: 0.75rem 1rem !important;
  font-size: 0.9375rem !important;
  border-radius: 12px !important;
  border: 2px solid var(--border) !important;
  background: var(--input-background) !important;
  color: var(--foreground) !important;
  transition: all 0.3s ease !important;
}

:deep(.p-password .p-password-input:hover) {
  border-color: var(--primary) !important;
  background: var(--card) !important;
}

:deep(.p-password .p-password-input:focus) {
  outline: none !important;
  border-color: var(--primary) !important;
  background: var(--card) !important;
  box-shadow: 0 0 0 3px var(--shadow-blue) !important;
}

:deep(.p-password-meter) {
  display: none !important;
}

:deep(.p-password .p-password-toggle) {
  color: var(--muted-foreground) !important;
}

:deep(.p-password .p-password-toggle:hover) {
  color: var(--primary) !important;
}

/* PrimeVue Dropdown trigger icon */
:deep(.p-dropdown .p-dropdown-trigger) {
  color: var(--muted-foreground) !important;
}

.form-hint {
  font-size: 0.8125rem;
  color: var(--muted-foreground);
  margin-top: 0.25rem;
}

/* PrimeVue Message — unified feedback banners */
.feedback-message {
  border-radius: 12px !important;
  font-size: 0.875rem !important;
  font-weight: 500 !important;
}

.submit-button {
  width: 100%;
  height: 52px !important;
  background: var(--primary) !important;
  color: var(--primary-foreground) !important;
  border: 1px solid var(--primary) !important;
  border-radius: 12px !important;
  font-weight: 600 !important;
  font-size: 1rem !important;
  cursor: pointer !important;
  transition: all 0.3s ease !important;
  box-shadow: 0 4px 12px rgba(30, 58, 138, 0.3) !important;
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 20px rgba(30, 58, 138, 0.4) !important;
  background: rgba(30, 58, 138, 0.9) !important;
}

.submit-button:active:not(:disabled) {
  transform: translateY(0) !important;
}

.submit-button:disabled {
  opacity: 0.6 !important;
  cursor: not-allowed !important;
  transform: none !important;
}

/* Divider */
.footer-divider {
  margin: 1.5rem 0 !important;
}

:deep(.footer-divider .p-divider-content) {
  background: var(--card) !important;
}

.footer-links {
  text-align: center;
}

.footer-links p {
  font-size: 0.9375rem;
  color: var(--muted-foreground);
  margin: 0;
}

.link {
  color: var(--primary);
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
}

.link:hover {
  text-decoration: underline;
}

.copyright {
  text-align: center;
}

.copyright p {
  font-size: 0.875rem;
  color: var(--muted-foreground);
  margin: 0;
}

@media (max-width: 640px) {
  .register-form-wrapper {
    padding: 2.5rem 1.5rem;
    border-radius: 20px;
  }
  .form-row {
    grid-template-columns: 1fr;
  }
  .form-title {
    font-size: 1.625rem;
  }
  .form-subtitle {
    font-size: 0.9375rem;
  }
}
</style>
