<template>
  <div class="login-page">
    <div class="login-container">
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
          <span>Quay lại Trang Chủ</span>
        </router-link>
      </div>

      <div class="login-form-wrapper">
        <div class="form-header">
          <h2 class="form-title">Đăng Nhập</h2>
          <p class="form-subtitle">
            Vui lòng đăng nhập để tiếp tục sử dụng hệ thống!
          </p>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleSubmit" class="login-form">
          <div class="form-group">
            <label for="email" class="form-label">Tên đăng nhập</label>
            <InputText
              id="email"
              v-model="email"
              :invalid="!email"
              type="email"
              placeholder="Nhập tên người dùng của bạn..."
              class="form-input"
              required
            />
          </div>

          <div class="form-group">
            <label for="password" class="form-label">Mật khẩu</label>
            <Password
              id="password"
              v-model="password"
              :invalid="!password"
              placeholder="Nhập mật khẩu của bạn..."
              toggleMask
              showClear
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

          <Button
            type="submit"
            class="submit-button"
            :disabled="loading || !email || !password"
            :loading="loading"
            :label="loading ? 'Đang đăng nhập...' : 'Đăng Nhập'"
            :icon="loading ? '' : 'pi pi-arrow-right'"
            icon-pos="right"
          />
        </form>

        <!-- Forgot Password Link -->
        <div class="forgot-password-link">
          <router-link to="/forgot-password" class="link"
            >Quên mật khẩu?</router-link
          >
        </div>

        <!-- Divider — PrimeVue Divider -->
        <Divider align="center" class="auth-divider">
          <span class="divider-label">Hoặc</span>
        </Divider>

        <!-- Social Login Buttons — PrimeVue Button with custom slots -->
        <div class="social-login">
          <Button
            text
            class="social-button google-btn"
            :disabled="loading"
            @click="handleGoogleLogin"
          >
            <template #default>
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                class="social-icon"
              >
                <path
                  fill="#4285F4"
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                />
                <path
                  fill="#34A853"
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                />
                <path
                  fill="#FBBC05"
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                />
                <path
                  fill="#EA4335"
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                />
              </svg>
              <span>Đăng nhập với Google</span>
            </template>
          </Button>

          <Button
            text
            class="social-button microsoft-btn"
            :disabled="loading"
            @click="handleMicrosoftLogin"
          >
            <template #default>
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                class="social-icon"
              >
                <path fill="#f25022" d="M1 1h10v10H1z" />
                <path fill="#00a4ef" d="M13 1h10v10H13z" />
                <path fill="#7fba00" d="M1 13h10v10H1z" />
                <path fill="#ffb900" d="M13 13h10v10H13z" />
              </svg>
              <span>Đăng nhập với Microsoft</span>
            </template>
          </Button>
        </div>

        <!-- Register Link -->
        <div class="footer-links">
          <p>
            Chưa có tài khoản?
            <router-link to="/register" class="link">Đăng ký ngay</router-link>
          </p>
        </div>

        <div class="copyright">
          <p>Bản quyền thuộc về © 2025-2026 MedCase Team.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useCasesStore } from "@/stores/cases";
import Button from "primevue/button";
import Divider from "primevue/divider";
import InputText from "primevue/inputtext";
import Message from "primevue/message";
import Password from "primevue/password";

const router = useRouter();
const authStore = useAuthStore();
const casesStore = useCasesStore();

const email = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);

const handleSubmit = async () => {
  loading.value = true;
  error.value = "";

  try {
    await authStore.login(email.value, password.value);
    router.push("/home");
  } catch (err: any) {
    error.value =
      err.response?.data?.detail ||
      "Đăng nhập thất bại. Vui lòng kiểm tra thông tin đăng nhập.";
  } finally {
    loading.value = false;
  }
};

const handleGoogleLogin = () => {
  const clientId =
    import.meta.env.VITE_GOOGLE_CLIENT_ID || "YOUR_GOOGLE_CLIENT_ID";
  const redirectUri = `${window.location.origin}/auth/google/callback`;
  const scope = "openid email profile";
  const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=token&scope=${scope}`;
  window.location.href = authUrl;
};

const handleMicrosoftLogin = () => {
  const clientId =
    import.meta.env.VITE_MICROSOFT_CLIENT_ID || "YOUR_MICROSOFT_CLIENT_ID";
  const redirectUri = `${window.location.origin}/auth/microsoft/callback`;
  const scope = "openid email profile";
  const authUrl = `https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=token&scope=${scope}`;
  window.location.href = authUrl;
};
</script>

<style scoped>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
  background: var(--background);
  color: var(--foreground);
}

.login-container {
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

.login-form-wrapper {
  background: var(--card);
  border-radius: 24px;
  padding: 3rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  border: 1px solid var(--border);
  position: relative;
}

.form-header {
  margin-bottom: 2.5rem;
  text-align: center;
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

.login-form {
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
  box-shadow: 0 0 0 3px rgba(30, 58, 138, 0.1) !important;
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

/* Error message */
.feedback-message {
  border-radius: 12px !important;
  font-size: 0.875rem !important;
  font-weight: 500 !important;
  animation: shake 0.4s ease-in-out;
}

@keyframes shake {
  0%,
  100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-8px);
  }
  75% {
    transform: translateX(8px);
  }
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

.forgot-password-link {
  text-align: right;
  margin-top: 0.75rem;
}

/* PrimeVue Divider — replaces the custom .divider with ::before/::after pseudo-borders */
.auth-divider {
  margin: 1.5rem 0 !important;
}

:deep(.auth-divider .p-divider-content) {
  background: var(--card) !important;
  padding: 0 1rem;
}

.divider-label {
  font-size: 0.875rem;
  color: var(--muted-foreground);
}

/* Social login buttons — PrimeVue Button with overridden globals.css defaults */
.social-login {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.social-button {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 0.75rem !important;
  width: 100%;
}

:deep(.social-button.p-button) {
  background: white !important;
  color: var(--foreground) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  padding: 0.875rem 1.5rem !important;
  font-size: 0.9375rem !important;
  font-weight: 600 !important;
  cursor: pointer !important;
  transition: all 0.2s !important;
  box-shadow: none !important;
}

:deep(.social-button.p-button:hover) {
  background: #f5f5f5 !important;
  border-color: var(--primary) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 12px rgba(30, 58, 138, 0.15) !important;
}

:deep(.social-button.p-button:focus),
:deep(.social-button.p-button.p-focus) {
  background: #f5f5f5 !important;
  box-shadow: 0 4px 12px rgba(30, 58, 138, 0.15) !important;
  outline: none !important;
}

:deep(.social-button.p-button:disabled),
:deep(.social-button.p-button:disabled:hover) {
  opacity: 0.5 !important;
  cursor: not-allowed !important;
  background: white !important;
}

:deep(.social-button .p-button-content) {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 0.75rem !important;
}

/* Ensure icons inside social buttons inherit correct color */
:deep(.social-button .p-button-label) {
  display: none !important; /* we use custom slot content */
}

.social-icon {
  flex-shrink: 0;
}

.footer-links {
  text-align: center;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
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
  margin-top: 2rem;
  text-align: center;
}

.copyright p {
  font-size: 0.875rem;
  color: var(--muted-foreground);
  margin: 0;
}

@media (max-width: 640px) {
  .login-page {
    padding: 1rem;
  }
  .top-nav-bar {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
  }
  .back-button {
    font-size: 0.875rem;
    padding: 0.625rem 1rem;
    justify-content: center;
  }
  .login-form-wrapper {
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
