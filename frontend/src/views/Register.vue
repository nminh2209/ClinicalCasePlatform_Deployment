<template>
  <div class="register-page">
    <div class="register-container">
      <!-- Top Navigation Bar -->
      <div class="top-nav-bar">
        <!-- Back to Home Button -->
        <router-link to="/" class="back-button">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7" />
          </svg>
          <span>Về trang chủ</span>
        </router-link>

        <!-- Language Switcher -->
        <div class="language-switcher-inline">
          <LanguageSwitcher />
        </div>
      </div>

      <div class="register-form-wrapper">
        <div class="form-header">
          <h2 class="form-title">Đăng ký tài khoản</h2>
          <p class="form-subtitle">Tạo tài khoản mới để truy cập hệ thống</p>
        </div>

        <!-- Success Message -->
        <div v-if="successMessage" class="success-message">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
            <polyline points="22 4 12 14.01 9 11.01" />
          </svg>
          {{ successMessage }}
        </div>

        <!-- Registration Form -->
        <form @submit.prevent="handleSubmit" class="register-form">
          <!-- Email -->
          <div class="form-group">
            <Label htmlFor="email" class="form-label">Email</Label>
            <Input id="email" v-model="formData.email" type="email" placeholder="your.email@university.edu"
              class="form-input" required />
          </div>

          <!-- Username -->
          <div class="form-group">
            <Label htmlFor="username" class="form-label">Tên đăng nhập</Label>
            <Input id="username" v-model="formData.username" type="text" placeholder="username" class="form-input"
              required />
          </div>

          <!-- Name Fields (Side by Side) -->
          <div class="form-row">
            <div class="form-group">
              <Label htmlFor="first_name" class="form-label">Tên</Label>
              <Input id="first_name" v-model="formData.first_name" type="text" placeholder="Nguyễn" class="form-input"
                required />
            </div>

            <div class="form-group">
              <Label htmlFor="last_name" class="form-label">Họ</Label>
              <Input id="last_name" v-model="formData.last_name" type="text" placeholder="Văn A" class="form-input"
                required />
            </div>
          </div>

          <!-- Role Selection -->
          <div class="form-group">
            <Label htmlFor="role" class="form-label">Vai trò</Label>
            <select id="role" v-model="formData.role" class="form-select" required>
              <option value="">Chọn vai trò</option>
              <option value="student">Sinh viên</option>
              <option value="instructor">Giảng viên</option>
            </select>
          </div>

          <!-- Student ID (conditional) -->
          <div v-if="formData.role === 'student'" class="form-group">
            <Label htmlFor="student_id" class="form-label">Mã sinh viên</Label>
            <Input id="student_id" v-model="formData.student_id" type="text" placeholder="SV2024001"
              class="form-input" />
          </div>

          <!-- Employee ID (conditional) -->
          <div v-if="formData.role === 'instructor'" class="form-group">
            <Label htmlFor="employee_id" class="form-label">Mã giảng viên</Label>
            <Input id="employee_id" v-model="formData.employee_id" type="text" placeholder="GV2024001"
              class="form-input" />
          </div>

          <!-- Password -->
          <div class="form-group">
            <Label htmlFor="password" class="form-label">Mật khẩu</Label>
            <div class="password-input-wrapper">
              <Input id="password" v-model="formData.password" :type="showPassword ? 'text' : 'password'"
                placeholder="Nhập mật khẩu" class="form-input password-input" required />
              <button type="button" @click="togglePasswordVisibility" class="password-toggle"
                :aria-label="showPassword ? 'Hide password' : 'Show password'">
                <Eye v-if="!showPassword" />
                <EyeOff v-else />
              </button>
            </div>
            <p class="form-hint">
              Tối thiểu 8 ký tự, bao gồm chữ hoa, chữ thường và số
            </p>
          </div>

          <!-- Password Confirmation -->
          <div class="form-group">
            <Label htmlFor="password_confirm" class="form-label">Xác nhận mật khẩu</Label>
            <div class="password-input-wrapper">
              <Input id="password_confirm" v-model="formData.password_confirm"
                :type="showPasswordConfirm ? 'text' : 'password'" placeholder="Nhập lại mật khẩu"
                class="form-input password-input" required />
              <button type="button" @click="togglePasswordConfirmVisibility" class="password-toggle" :aria-label="showPasswordConfirm ? 'Hide password' : 'Show password'
                ">
                <Eye v-if="!showPasswordConfirm" />
                <EyeOff v-else />
              </button>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="error-message">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
            {{ error }}
          </div>

          <!-- Submit Button -->
          <Button type="submit" class="submit-button" :disabled="loading">
            <span v-if="loading" class="loading-text">
              <svg class="spinner" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                stroke-width="2">
                <path d="M21 12a9 9 0 1 1-6.219-8.56" />
              </svg>
              Đang tạo tài khoản...
            </span>
            <span v-else class="button-content">
              Đăng ký
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                <polyline points="22 4 12 14.01 9 11.01" />
              </svg>
            </span>
          </Button>
        </form>

        <!-- Login Link -->
        <div class="footer-links">
          <p>
            Đã có tài khoản?
            <router-link to="/login" class="link">Đăng nhập</router-link>
          </p>
        </div>

        <div class="copyright">
          <p>&copy; 2026 Clinical Case Platform</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "@/services/api";
import LanguageSwitcher from "@/components/LanguageSwitcher.vue";
import Button from "@/components/ui/Button.vue";
import Input from "@/components/ui/Input.vue";
import Label from "@/components/ui/Label.vue";
import Eye from "@/components/icons/Eye.vue";
import EyeOff from "@/components/icons/EyeOff.vue";

const router = useRouter();

const formData = ref({
  email: "",
  username: "",
  first_name: "",
  last_name: "",
  role: "",
  student_id: "",
  employee_id: "",
  password: "",
  password_confirm: "",
});

const error = ref("");
const successMessage = ref("");
const loading = ref(false);
const showPassword = ref(false);
const showPasswordConfirm = ref(false);

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const togglePasswordConfirmVisibility = () => {
  showPasswordConfirm.value = !showPasswordConfirm.value;
};

const handleSubmit = async () => {
  loading.value = true;
  error.value = "";
  successMessage.value = "";

  // Client-side validation
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
    // Prepare data
    const payload: any = {
      email: formData.value.email,
      username: formData.value.username,
      first_name: formData.value.first_name,
      last_name: formData.value.last_name,
      role: formData.value.role,
      password: formData.value.password,
      password_confirm: formData.value.password_confirm,
    };

    // Add role-specific fields
    if (formData.value.role === "student" && formData.value.student_id) {
      payload.student_id = formData.value.student_id;
    }
    if (formData.value.role === "instructor" && formData.value.employee_id) {
      payload.employee_id = formData.value.employee_id;
    }

    await api.post("/auth/register/", payload);

    successMessage.value =
      "Đăng ký thành công! Đang chuyển đến trang đăng nhập...";

    // Redirect to login after 2 seconds
    setTimeout(() => {
      router.push("/login");
    }, 2000);
  } catch (err: any) {
    if (err.response?.data) {
      // Handle specific field errors
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
  background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
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
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: white;
  border-radius: 8px;
  color: #64748b;
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.back-button:hover {
  background: #f8fafc;
  color: #475569;
  transform: translateX(-2px);
}

.register-form-wrapper {
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.form-header {
  text-align: center;
  margin-bottom: 2rem;
}

.form-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.form-subtitle {
  font-size: 0.9375rem;
  color: #64748b;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
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
  color: #334155;
}

.form-input {
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.9375rem;
  transition: all 0.2s;
  width: 100%;
}

.form-input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.form-select {
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.9375rem;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.form-select:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.form-hint {
  font-size: 0.8125rem;
  color: #64748b;
  margin-top: 0.25rem;
}

.password-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.password-input {
  width: 100%;
  padding-right: 3rem;
}

.password-toggle {
  position: absolute;
  right: 1rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  color: #94a3b8;
  transition: color 0.2s;
}

.password-toggle:hover {
  color: #64748b;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  color: #dc2626;
  font-size: 0.875rem;
}

.success-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 8px;
  color: #16a34a;
  font-size: 0.875rem;
  margin-bottom: 1.5rem;
}

.submit-button {
  width: 100%;
  padding: 0.875rem 1.5rem;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.button-content,
.loading-text {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

.footer-links {
  text-align: center;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.footer-links p {
  font-size: 0.9375rem;
  color: #64748b;
}

.link {
  color: #6366f1;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
}

.link:hover {
  color: #4f46e5;
  text-decoration: underline;
}

.copyright {
  text-align: center;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.copyright p {
  font-size: 0.8125rem;
  color: #94a3b8;
}

@media (max-width: 640px) {
  .register-form-wrapper {
    padding: 1.5rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .form-title {
    font-size: 1.5rem;
  }
}
</style>
