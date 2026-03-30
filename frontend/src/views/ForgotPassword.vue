<template>
  <div class="forgot-password-page">
    <div class="forgot-password-container">
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

      <div class="forgot-password-form-wrapper">
        <div class="form-header">
          <div class="icon-wrapper">
            <svg
              width="48"
              height="48"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
              <path d="M7 11V7a5 5 0 0 1 10 0v4" />
            </svg>
          </div>
          <h2 class="form-title">Quên mật khẩu?</h2>
          <p class="form-subtitle">
            Nhập email của bạn và chúng tôi sẽ gửi hướng dẫn đặt lại mật khẩu
          </p>
        </div>

        <!-- Success Message — PrimeVue Message component -->
        <Message
          v-if="successMessage"
          severity="success"
          :closable="false"
          class="feedback-message"
        >
          <div class="message-content">
            <p class="success-title">Email đã được gửi!</p>
            <p class="success-text">
              Vui lòng kiểm tra hộp thư của bạn và làm theo hướng dẫn để đặt lại
              mật khẩu.
            </p>
          </div>
        </Message>

        <!-- Reset Form -->
        <form
          v-if="!successMessage"
          @submit.prevent="handleSubmit"
          class="forgot-password-form"
        >
          <div class="form-group">
            <label for="email" class="form-label">Email</label>
            <InputText
              id="email"
              v-model="email"
              type="email"
              placeholder="your.email@university.edu"
              class="form-input"
              required
            />
          </div>

          <!-- Error Message — PrimeVue Message component -->
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
            :disabled="loading"
            :loading="loading"
            :label="loading ? 'Đang gửi...' : 'Gửi hướng dẫn đặt lại mật khẩu'"
            :icon="loading ? '' : 'pi pi-arrow-right'"
            icon-pos="right"
          />
        </form>

        <!-- Back to Login Link -->
        <Divider class="footer-divider" />
        <div class="footer-links">
          <router-link to="/login" class="link">
            <i class="pi pi-arrow-left" style="font-size: 0.875rem" />
            Quay lại trang đăng nhập
          </router-link>
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
import { ref } from "vue";
import api from "@/services/api";
import Button from "primevue/button";
import Divider from "primevue/divider";
import InputText from "primevue/inputtext";
import Message from "primevue/message";

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
  background: var(--background);
  color: var(--foreground);
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
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid var(--border);
}

.back-button:hover {
  background: var(--secondary);
  transform: translateX(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  color: var(--foreground);
}

.back-button svg {
  transition: transform 0.3s ease;
}

.back-button:hover svg {
  transform: translateX(-2px);
}

.forgot-password-form-wrapper {
  background: var(--card);
  border-radius: 24px;
  padding: 3rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  border: 1px solid var(--border);
  position: relative;
}

.form-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  background: linear-gradient(
    135deg,
    var(--accent) 0%,
    rgba(59, 130, 246, 0.1) 100%
  );
  border-radius: 50%;
  margin-bottom: 1.5rem;
  color: var(--primary);
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

.forgot-password-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
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
  box-shadow: 0 0 0 3px rgba(30, 58, 138, 0.1) !important;
}

/* PrimeVue Message overrides — match the original error/success banner look */
.feedback-message {
  border-radius: 12px !important;
  font-size: 0.875rem !important;
  font-weight: 500 !important;
}

.message-content .success-title {
  font-weight: 600;
  font-size: 0.9375rem;
  margin-bottom: 0.25rem;
}

.message-content .success-text {
  font-size: 0.875rem;
  line-height: 1.5;
  margin: 0;
}

/* Submit button */
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

/* Divider overrides */
.footer-divider {
  margin: 1.5rem 0 !important;
}

:deep(.footer-divider .p-divider-content) {
  background: var(--card) !important;
}

.footer-links {
  text-align: center;
}

.link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--primary);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9375rem;
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
  .forgot-password-form-wrapper {
    padding: 2.5rem 1.5rem;
    border-radius: 20px;
  }

  .form-title {
    font-size: 1.625rem;
  }

  .form-subtitle {
    font-size: 0.9375rem;
  }
}
</style>
