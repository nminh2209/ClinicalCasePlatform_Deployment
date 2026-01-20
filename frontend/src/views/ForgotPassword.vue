<template>
  <div class="forgot-password-page">
    <div class="forgot-password-container">
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

      <div class="forgot-password-form-wrapper">
        <div class="form-header">
          <!-- Icon -->
          <div class="icon-wrapper">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
              <path d="M7 11V7a5 5 0 0 1 10 0v4" />
            </svg>
          </div>

          <h2 class="form-title">Quên mật khẩu?</h2>
          <p class="form-subtitle">
            Nhập email của bạn và chúng tôi sẽ gửi hướng dẫn đặt lại mật khẩu
          </p>
        </div>

        <!-- Success Message -->
        <div v-if="successMessage" class="success-message">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
            <polyline points="22 4 12 14.01 9 11.01" />
          </svg>
          <div>
            <p class="success-title">Email đã được gửi!</p>
            <p class="success-text">
              Vui lòng kiểm tra hộp thư của bạn và làm theo hướng dẫn để đặt
              lại mật khẩu.
            </p>
          </div>
        </div>

        <!-- Reset Form -->
        <form v-if="!successMessage" @submit.prevent="handleSubmit" class="forgot-password-form">
          <div class="form-group">
            <Label htmlFor="email" class="form-label">Email</Label>
            <Input id="email" v-model="email" type="email" placeholder="your.email@university.edu" class="form-input"
              required />
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
              Đang gửi...
            </span>
            <span v-else class="button-content">
              Gửi hướng dẫn đặt lại mật khẩu
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="5" y1="12" x2="19" y2="12" />
                <polyline points="12 5 19 12 12 19" />
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
import api from "@/services/api";
import LanguageSwitcher from "@/components/LanguageSwitcher.vue";
import Button from "@/components/ui/Button.vue";
import Input from "@/components/ui/Input.vue";
import Label from "@/components/ui/Label.vue";

const email = ref("");
const error = ref("");
const successMessage = ref(false);
const loading = ref(false);

const handleSubmit = async () => {
  loading.value = true;
  error.value = "";

  try {
    await api.post("/auth/password-reset/", { email: email.value });
    successMessage.value = true;
  } catch (err: any) {
    if (err.response?.data?.detail) {
      error.value = err.response.data.detail;
    } else if (err.response?.data?.email) {
      error.value = Array.isArray(err.response.data.email)
        ? err.response.data.email[0]
        : err.response.data.email;
    } else {
      error.value =
        "Không thể gửi email đặt lại mật khẩu. Vui lòng thử lại sau.";
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.forgot-password-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
}

.forgot-password-container {
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

.forgot-password-form-wrapper {
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

.forgot-password-form {
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
}

.form-input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
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
  .forgot-password-form-wrapper {
    padding: 1.5rem;
  }

  .form-title {
    font-size: 1.5rem;
  }
}
</style>
