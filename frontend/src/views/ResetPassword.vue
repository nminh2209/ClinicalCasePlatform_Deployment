<template>
  <div class="reset-password-page">
    <div class="reset-password-container">
      <!-- Top Navigation Bar -->
      <div class="top-nav-bar">
        <!-- Back to Login Button -->
        <router-link to="/login" class="back-button">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7" />
          </svg>
          <span>Quay lại đăng nhập</span>
        </router-link>

        <!-- Language Switcher -->
        <div class="language-switcher-inline">
          <LanguageSwitcher />
        </div>
      </div>

      <div class="reset-password-form-wrapper">
        <div class="form-header">
          <!-- Icon -->
          <div class="icon-wrapper">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
              <path d="M7 11V7a5 5 0 0 1 10 0v4" />
            </svg>
          </div>

          <h2 class="form-title">Đặt lại mật khẩu</h2>
          <p class="form-subtitle">Nhập mật khẩu mới cho tài khoản của bạn</p>
        </div>

        <!-- Success Message -->
        <div v-if="successMessage" class="success-message">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
            <polyline points="22 4 12 14.01 9 11.01" />
          </svg>
          <div>
            <p class="success-title">Đặt lại mật khẩu thành công!</p>
            <p class="success-text">
              Bạn có thể đăng nhập với mật khẩu mới. Đang chuyển đến trang đăng
              nhập...
            </p>
          </div>
        </div>

        <!-- Reset Form -->
        <form v-if="!successMessage" @submit.prevent="handleSubmit" class="reset-password-form">
          <!-- New Password -->
          <div class="form-group">
            <Label htmlFor="new_password" class="form-label">Mật khẩu mới</Label>
            <div class="password-input-wrapper">
              <Input id="new_password" v-model="formData.new_password" :type="showPassword ? 'text' : 'password'"
                placeholder="Nhập mật khẩu mới" class="form-input password-input" required />
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

          <!-- Confirm Password -->
          <div class="form-group">
            <Label htmlFor="new_password_confirm" class="form-label">Xác nhận mật khẩu</Label>
            <div class="password-input-wrapper">
              <Input id="new_password_confirm" v-model="formData.new_password_confirm"
                :type="showPasswordConfirm ? 'text' : 'password'" placeholder="Nhập lại mật khẩu mới"
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
              Đang xử lý...
            </span>
            <span v-else class="button-content">
              Đặt lại mật khẩu
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                <polyline points="22 4 12 14.01 9 11.01" />
              </svg>
            </span>
          </Button>
        </form>

        <!-- Back to Login Link -->
        <div class="footer-links">
          <router-link to="/login" class="link">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 12H5M12 19l-7-7 7-7" />
            </svg>
            Quay lại trang đăng nhập
          </router-link>
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
import { useRouter, useRoute } from "vue-router";
import api from "@/services/api";
import LanguageSwitcher from "@/components/LanguageSwitcher.vue";
import Button from "@/components/ui/Button.vue";
import Input from "@/components/ui/Input.vue";
import Label from "@/components/ui/Label.vue";
import Eye from "@/components/icons/Eye.vue";
import EyeOff from "@/components/icons/EyeOff.vue";

const router = useRouter();
const route = useRoute();

const formData = ref({
  new_password: "",
  new_password_confirm: "",
});

const error = ref("");
const successMessage = ref(false);
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

  // Client-side validation
  if (formData.value.new_password !== formData.value.new_password_confirm) {
    error.value = "Mật khẩu xác nhận không khớp";
    loading.value = false;
    return;
  }

  if (formData.value.new_password.length < 8) {
    error.value = "Mật khẩu phải có ít nhất 8 ký tự";
    loading.value = false;
    return;
  }

  try {
    // Get uid and token from URL params
    const uid = route.params.uid as string;
    const token = route.params.token as string;

    await api.post("/auth/password-reset-confirm/", {
      uid,
      token,
      new_password: formData.value.new_password,
      new_password_confirm: formData.value.new_password_confirm,
    });

    successMessage.value = true;

    // Redirect to login after 3 seconds
    setTimeout(() => {
      router.push("/login");
    }, 3000);
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
      error.value = "Đặt lại mật khẩu thất bại. Liên kết có thể đã hết hạn.";
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.reset-password-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
}

.reset-password-container {
  width: 100%;
  max-width: 480px;
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

.reset-password-form-wrapper {
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.form-header {
  text-align: center;
  margin-bottom: 2rem;
}

.icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #e0e7ff 0%, #ddd6fe 100%);
  border-radius: 50%;
  margin-bottom: 1.5rem;
  color: #6366f1;
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
  line-height: 1.6;
}

.reset-password-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
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
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem 1.25rem;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 8px;
  color: #16a34a;
  margin-bottom: 1.5rem;
}

.success-message svg {
  flex-shrink: 0;
  margin-top: 0.125rem;
}

.success-title {
  font-weight: 600;
  font-size: 0.9375rem;
  margin-bottom: 0.25rem;
}

.success-text {
  font-size: 0.875rem;
  color: #15803d;
  line-height: 1.5;
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

.link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #6366f1;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9375rem;
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
  .reset-password-form-wrapper {
    padding: 1.5rem;
  }

  .form-title {
    font-size: 1.5rem;
  }
}
</style>
