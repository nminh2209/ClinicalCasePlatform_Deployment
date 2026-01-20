<template>
  <div class="oauth-callback-page">
    <div class="callback-container">
      <div class="loading-spinner">
        <svg class="spinner" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor"
          stroke-width="2">
          <path d="M21 12a9 9 0 1 1-6.219-8.56" />
        </svg>
      </div>

      <h2 v-if="!error" class="loading-title">Đang xác thực...</h2>
      <p v-if="!error" class="loading-text">Vui lòng đợi trong giây lát</p>

      <div v-if="error" class="error-container">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
        <h2 class="error-title">Xác thực thất bại</h2>
        <p class="error-text">{{ error }}</p>
        <router-link to="/login" class="back-button">
          Quay lại đăng nhập
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import api from "@/services/api";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const error = ref("");

onMounted(async () => {
  try {
    // Extract access token from URL hash
    const hash = window.location.hash.substring(1);
    const params = new URLSearchParams(hash);
    const accessToken = params.get("access_token");

    if (!accessToken) {
      error.value = "Không tìm thấy access token. Vui lòng thử lại.";
      return;
    }

    // Determine provider from route path
    const provider = route.path.includes("google") ? "google" : "microsoft";
    const endpoint = `/auth/${provider}/`;

    // Exchange token with backend
    const response = await api.post(endpoint, { access_token: accessToken });

    // Update Pinia store
    const { user, tokens } = response.data;
    authStore.user = user;
    authStore.token = tokens.access;

    // Persist and save auth data
    localStorage.setItem("access_token", tokens.access);
    localStorage.setItem("refresh_token", tokens.refresh);
    localStorage.setItem("user", JSON.stringify(user));

    // Redirect to home
    router.push("/home");
  } catch (err: any) {
    console.error("OAuth callback error: ", err);
    error.value =
      err.response?.data?.error ||
      "Xác thực thất bại. Vui lòng thử lại sau.";
  }
});
</script>

<style scoped>
.oauth-callback-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
}

.callback-container {
  text-align: center;
  background: white;
  border-radius: 16px;
  padding: 3rem 2.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  max-width: 480px;
  width: 100%;
}

.loading-spinner {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.spinner {
  color: #6366f1;
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

.loading-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.loading-text {
  font-size: 0.9375rem;
  color: #64748b;
}

.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.error-container svg {
  color: #dc2626;
}

.error-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
}

.error-text {
  font-size: 0.9375rem;
  color: #64748b;
  line-height: 1.6;
}

.back-button {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.2s;
  display: inline-block;
}

.back-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
}
</style>
