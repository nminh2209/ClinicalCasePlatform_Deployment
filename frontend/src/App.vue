<template>
  <div id="app">
    <!-- Show layout with sidebar/topbar only for authenticated routes -->
    <Layout v-if="showLayout">
      <router-view />
    </Layout>

    <!-- Show without layout for login/landing pages -->
    <router-view v-else />
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRoute } from "vue-router";
import Layout from "@/components/Layout.vue";

const authStore = useAuthStore();
const route = useRoute();

// Pages that should NOT show the layout (sidebar/topbar)
const noLayoutPages = [
  "/",
  "/login",
  "/register",
  "/forgot-password",
];

// Show layout for all authenticated pages, hide for login/landing/auth pages
const showLayout = computed(() => {
  // Check exact path match
  if (noLayoutPages.includes(route.path)) {
    return false;
  }

  // Check path prefix for dynamic routes (password reset, OAuth callbacks)
  if (route.path.startsWith("/reset-password/") || route.path.startsWith("/auth/")) {
    return false;
  }

  return true;
});

onMounted(() => {
  // Check for existing authentication on app load
  authStore.checkAuth();
});
</script>

<style>
/* Global styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family:
    -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "Ubuntu",
    "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f8fafc;
  color: #1f2937;
  line-height: 1.6;
}

#app {
  min-height: 100vh;
}

/* Medical Theme Color Variables */
:root {
  --primary-blue: #1e40af;
  --primary-blue-light: #3b82f6;
  --primary-blue-dark: #1e3a8a;
  --success-green: #10b981;
  --warning-orange: #f59e0b;
  --danger-red: #ef4444;
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;
}

/* Scrollbar Styling */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Focus States */
*:focus {
  outline: 2px solid var(--primary-blue-light);
  outline-offset: 2px;
}

/* Selection */
::selection {
  background: var(--primary-blue-light);
  color: white;
}

/* Utility Classes */
.text-primary {
  color: var(--primary-blue);
}

.text-grey {
  color: var(--gray-50);
}

.text-success {
  color: var(--success-green);
}

.text-warning {
  color: var(--warning-orange);
}

.text-danger {
  color: var(--danger-red);
}

.bg-primary {
  background-color: var(--primary-blue);
}

.bg-success {
  background-color: var(--success-green);
}

.bg-warning {
  background-color: var(--warning-orange);
}

.bg-danger {
  background-color: var(--danger-red);
}

/* Medical Icons Enhancement */
.medical-icon {
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
}

/* Card Shadows */
.card-shadow {
  box-shadow:
    0 1px 3px 0 rgba(0, 0, 0, 0.1),
    0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.card-shadow-md {
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.card-shadow-lg {
  box-shadow:
    0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* Animation Classes */
.fade-in {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.slide-in-right {
  animation: slideInRight 0.3s ease-in-out;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }

  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Loading States */
.loading {
  opacity: 0.6;
  pointer-events: none;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #e5e7eb;
  border-top: 2px solid var(--primary-blue);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

/* Medical Color Scheme */
.medical-card {
  background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
  border: 1px solid #e2e8f0;
}

.medical-header {
  background: linear-gradient(135deg,
      var(--primary-blue) 0%,
      var(--primary-blue-dark) 100%);
}

/* Responsive Typography */
@media (max-width: 768px) {
  body {
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  body {
    font-size: 13px;
  }
}
</style>
