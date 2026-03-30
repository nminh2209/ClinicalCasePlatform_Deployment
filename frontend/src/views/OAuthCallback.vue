<template>
  <div class="oauth-callback-page">
    <div class="callback-container">
      <!-- Loading State -->
      <template v-if="!error">
        <div class="loading-spinner">
          <ProgressSpinner
            style="width: 56px; height: 56px"
            strokeWidth="3"
            animationDuration=".8s"
            class="auth-spinner"
          />
        </div>
        <h2 class="loading-title">Đang xác thực...</h2>
        <p class="loading-text">Vui lòng đợi trong giây lát</p>
      </template>

      <!-- Error State -->
      <template v-else>
        <div class="error-icon-wrapper">
          <i class="pi pi-times-circle error-icon" />
        </div>

        <h2 class="error-title">Xác thực thất bại</h2>

        <!-- PrimeVue Message for error detail -->
        <Message severity="error" :closable="false" class="error-message-box">
          {{ error }}
        </Message>

        <Button
          label="Quay lại đăng nhập"
          icon="pi pi-arrow-left"
          class="back-btn"
          @click="$router.push('/login')"
        />
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import api from "@/services/api";
import Button from "primevue/button";
import Message from "primevue/message";
import ProgressSpinner from "primevue/progressspinner";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const error = ref("");

onMounted(async () => {
  try {
    const hash = window.location.hash.substring(1);
    const params = new URLSearchParams(hash);
    const accessToken = params.get("access_token");

    if (!accessToken) {
      error.value = "Không tìm thấy access token. Vui lòng thử lại.";
      return;
    }

    const provider = route.path.includes("google") ? "google" : "microsoft";
    const endpoint = `/auth/${provider}/`;

    const response = await api.post(endpoint, { access_token: accessToken });

    const { user, tokens } = response.data;
    authStore.user = user;
    authStore.token = tokens.access;

    localStorage.setItem("access_token", tokens.access);
    localStorage.setItem("refresh_token", tokens.refresh);
    localStorage.setItem("user", JSON.stringify(user));

    router.push("/home");
  } catch (err: any) {
    console.error("OAuth callback error: ", err);
    error.value =
      err.response?.data?.error || "Xác thực thất bại. Vui lòng thử lại sau.";
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
  background: var(--background);
}

.callback-container {
  text-align: center;
  background: var(--card);
  border-radius: 24px;
  padding: 3rem 2.5rem;
  box-shadow: 0 8px 24px var(--shadow-grey);
  border: 1px solid var(--border);
  max-width: 480px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

/* Loading */
.loading-spinner {
  display: flex;
  justify-content: center;
  margin-bottom: 0.5rem;
}

/* Override PrimeVue ProgressSpinner color to use --primary */
:deep(.auth-spinner .p-progressspinner-circle) {
  stroke: var(--primary) !important;
}

.loading-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--foreground);
  margin: 0;
}

.loading-text {
  font-size: 0.9375rem;
  color: var(--muted-foreground);
  margin: 0;
}

/* Error */
.error-icon-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 0.5rem;
}

.error-icon {
  font-size: 3rem;
  color: var(--destructive);
}

.error-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--foreground);
  margin: 0;
}

.error-message-box {
  width: 100%;
  border-radius: 12px !important;
  font-size: 0.9375rem !important;
  text-align: left;
}

/* Back button */
.back-btn {
  margin-top: 0.5rem;
  padding: 0.75rem 1.5rem !important;
  background: var(--primary) !important;
  color: var(--primary-foreground) !important;
  border: none !important;
  border-radius: 12px !important;
  font-weight: 600 !important;
  transition: all 0.3s ease !important;
  box-shadow: 0 4px 12px var(--shadow-blue) !important;
}

.back-btn:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 20px var(--shadow-blue-hover) !important;
  background: rgba(30, 58, 138, 0.9) !important;
}
</style>
