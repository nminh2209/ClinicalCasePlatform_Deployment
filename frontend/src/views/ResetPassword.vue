<template>
  <div class="reset-password-page">
    <div class="reset-password-container">
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

      <div class="reset-password-form-wrapper">
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
          <h2 class="form-title">Đặt lại mật khẩu</h2>
          <p class="form-subtitle">Nhập mật khẩu mới cho tài khoản của bạn</p>
        </div>

        <!-- Success Message — PrimeVue Message -->
        <Message
          v-if="successMessage"
          severity="success"
          :closable="false"
          class="feedback-message"
        >
          <div class="message-content">
            <p class="success-title">Đặt lại mật khẩu thành công!</p>
            <p class="success-text">
              Bạn có thể đăng nhập với mật khẩu mới. Đang chuyển đến trang đăng
              nhập...
            </p>
          </div>
        </Message>

        <!-- Reset Form -->
        <form
          v-if="!successMessage"
          @submit.prevent="handleSubmit"
          class="reset-password-form"
        >
          <!-- New Password -->
          <div class="form-group">
            <label for="new_password" class="form-label">Mật khẩu mới</label>
            <Password
              id="new_password"
              v-model="formData.new_password"
              placeholder="Nhập mật khẩu mới"
              toggle-mask
              fluid
              :feedback="false"
              required
            />
            <p class="form-hint">
              Tối thiểu 8 ký tự, bao gồm chữ hoa, chữ thường và số
            </p>
          </div>

          <!-- Confirm Password -->
          <div class="form-group">
            <label for="new_password_confirm" class="form-label"
              >Xác nhận mật khẩu</label
            >
            <Password
              id="new_password_confirm"
              v-model="formData.new_password_confirm"
              placeholder="Nhập lại mật khẩu mới"
              toggle-mask
              fluid
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
            :disabled="loading"
            :loading="loading"
            :label="loading ? 'Đang xử lý...' : 'Đặt lại mật khẩu'"
            :icon="loading ? '' : 'pi pi-check'"
            icon-pos="right"
          />
        </form>

        <!-- Back to Login -->
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
import { useRouter, useRoute } from "vue-router";
import api from "@/services/api";
import Button from "primevue/button";
import Divider from "primevue/divider";
import Message from "primevue/message";
import Password from "primevue/password";

const router = useRouter();
const route = useRoute();

const formData = ref({
  new_password: "",
  new_password_confirm: "",
});

const error = ref("");
const successMessage = ref(false);
const loading = ref(false);

const handleSubmit = async () => {
  loading.value = true;
  error.value = "";

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
    const uid = route.params.uid as string;
    const token = route.params.token as string;

    await api.post("/auth/password-reset-confirm/", {
      uid,
      token,
      new_password: formData.value.new_password,
      new_password_confirm: formData.value.new_password_confirm,
    });

    successMessage.value = true;

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
  background: var(--background);
  color: var(--foreground);
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

.reset-password-form-wrapper {
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

.reset-password-form {
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

/* PrimeVue Password — full-width + styled to match other inputs */
:deep(.p-password) {
  width: 100% !important;
}

:deep(.p-password .p-password-input) {
  width: 100% !important;
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
  box-shadow: 0 0 0 3px rgba(30, 58, 138, 0.1) !important;
}

:deep(.p-password-toggle) {
  color: var(--muted-foreground) !important;
  transition: color 0.2s ease !important;
}

:deep(.p-password-toggle:hover) {
  color: var(--primary) !important;
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
  .reset-password-form-wrapper {
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
