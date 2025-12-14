<template>
  <div class="login-page">
    <div class="login-container">
      <!-- Top Navigation Bar -->
      <div class="top-nav-bar">
        <!-- Back to Home Button -->
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
          <span>{{ t("login.goBack") }}</span>
        </router-link>

        <!-- Language Switcher -->
        <div class="language-switcher-inline">
          <LanguageSwitcher />
        </div>
      </div>

      <div class="login-form-wrapper">
        <div class="form-header">
          <h2 class="form-title">{{ t("login.title") }}</h2>
          <p class="form-subtitle">{{ t("login.subtitle") }}</p>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleSubmit" class="login-form">
          <div class="form-group">
            <Label htmlFor="email" class="form-label">{{
              t("login.username")
            }}</Label>
            <Input
              id="email"
              v-model="email"
              type="email"
              :placeholder="t('login.placeholder.username')"
              class="form-input"
              required
            />
          </div>

          <div class="form-group">
            <Label htmlFor="password" class="form-label">{{
              t("login.password")
            }}</Label>
            <div class="password-input-wrapper">
              <Input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                :placeholder="t('login.placeholder.password')"
                class="form-input password-input"
                required
              />
              <button
                type="button"
                @click="togglePasswordVisibility"
                class="password-toggle"
                :aria-label="showPassword ? 'Hide password' : 'Show password'"
              >
                <Eye v-if="!showPassword" />
                <EyeOff v-else />
              </button>
            </div>
          </div>

          <div v-if="error" class="error-message">
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
            {{ t("login.error.failedLogin") }}
          </div>

          <Button type="submit" class="submit-button" :disabled="loading">
            <span v-if="loading" class="loading-text">
              <svg
                class="spinner"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path d="M21 12a9 9 0 1 1-6.219-8.56" />
              </svg>
              Đang đăng nhập...
            </span>
            <span v-else class="button-content">
              {{ t("login.button") }}
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <line x1="5" y1="12" x2="19" y2="12" />
                <polyline points="12 5 19 12 12 19" />
              </svg>
            </span>
          </Button>
        </form>

        <div class="copyright">
          <p>{{ t("login.copyright") }}</p>
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
import { useLanguage } from "@/composables/useLanguage";
import LanguageSwitcher from "@/components/LanguageSwitcher.vue";
import Button from "@/components/ui/Button.vue";
import Input from "@/components/ui/Input.vue";
import Label from "@/components/ui/Label.vue";
import Eye from "@/components/icons/Eye.vue";
import EyeOff from "@/components/icons/EyeOff.vue";

const router = useRouter();
const authStore = useAuthStore();
const casesStore = useCasesStore();
const { t } = useLanguage();

const email = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);
const showPassword = ref(false);

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const handleSubmit = async () => {
  loading.value = true;
  error.value = "";

  try {
    await authStore.login(email.value, password.value);
    
    // Redirect to home to show role-based dashboard
    router.push("/home");
  } catch (err: any) {
    error.value =
      err.response?.data?.detail ||
      "Đăng nhập thất bại. Vui lòng kiểm tra thông tin đăng nhập.";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
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
  background: white;
  color: #374151;
  border-radius: 12px;
  font-weight: 500;
  font-size: 0.9375rem;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #e5e7eb;
}

.back-button:hover {
  background: #f9fafb;
  transform: translateX(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.back-button svg {
  transition: transform 0.3s ease;
}

.back-button:hover svg {
  transform: translateX(-2px);
}

.language-switcher-inline {
  display: flex;
  align-items: center;
}

.login-form-wrapper {
  background: white;
  border-radius: 24px;
  padding: 3rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  border: 1px solid #e5e7eb;
  position: relative;
}

.form-header {
  margin-bottom: 2.5rem;
  text-align: center;
}

.form-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.75rem;
  letter-spacing: -0.02em;
}

.form-subtitle {
  font-size: 1rem;
  color: #6b7280;
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
  color: #374151;
  margin-bottom: 0.25rem;
}

.form-input {
  height: 52px;
  border-radius: 12px;
  border: 2px solid #e5e7eb;
  padding: 0 1.25rem;
  font-size: 0.9375rem;
  transition: all 0.3s ease;
  background: #f9fafb;
}

.form-input:hover {
  border-color: #cbd5e1;
  background: white;
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
  transform: translateY(-1px);
}

.password-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.password-input {
  padding-right: 3.5rem;
  width: 100%;
}

.password-toggle {
  position: absolute;
  right: 1rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  transition: color 0.2s ease;
  border-radius: 8px;
}

.password-toggle:hover {
  color: #374151;
  background: #f3f4f6;
}

.password-toggle:focus {
  outline: none;
  color: #3b82f6;
}

.password-toggle svg {
  width: 20px;
  height: 20px;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  background: #fef2f2;
  border: 2px solid #fecaca;
  border-radius: 12px;
  color: #dc2626;
  font-size: 0.875rem;
  font-weight: 500;
  animation: shake 0.4s ease-in-out;
}

.error-message svg {
  flex-shrink: 0;
  color: #ef4444;
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

.form-footer {
  display: flex;
  justify-content: flex-end;
}

.forgot-link {
  font-size: 0.875rem;
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s;
  position: relative;
}

.forgot-link::after {
  content: "";
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: #3b82f6;
  transition: width 0.3s ease;
}

.forgot-link:hover {
  color: #1d4ed8;
}

.forgot-link:hover::after {
  width: 100%;
}

.submit-button {
  height: 52px;
  background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
  background: linear-gradient(135deg, #2563eb 0%, #1e3a8a 100%);
}

.submit-button:active:not(:disabled) {
  transform: translateY(0);
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.button-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

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

.copyright {
  margin-top: 2rem;
  text-align: center;
}

.copyright p {
  font-size: 0.875rem;
  color: #9ca3af;
}

/* Responsive Design */
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

  .language-switcher-inline {
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
