// stores/auth.ts

import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { authService } from "@/services/auth";
import { useCasesStore } from "@/stores/cases";

export const useAuthStore = defineStore("auth", () => {
  const user = ref<any | null>(authService.getCurrentUser());
  const token = ref<string | null>(authService.getAccessToken());

  const loading = ref(false);
  const error = ref<string | null>(null);

  const isAuthenticated = computed(() => !!token.value && !!user.value);
  const isStudent = computed(() => user.value?.role === "student");
  const isInstructor = computed(() => user.value?.role === "instructor");
  const isAdmin = computed(() => user.value?.role === "admin");

  async function login(email: string, password: string) {
    loading.value = true;
    error.value = null;
    try {
      const { user: u, tokens } = await authService.login(email, password);
      user.value = u;
      token.value = tokens.access;
      return { user: u, tokens };
    } catch (err: any) {
      error.value = err.response?.data?.message || "Login failed";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function register(userData: any) {
    loading.value = true;
    error.value = null;
    try {
      const { user: u, tokens } = await authService.register(userData);
      user.value = u;
      token.value = tokens.access;
      return { user: u, tokens };
    } catch (err: any) {
      error.value = err.response?.data?.message || "Registration failed";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function logout() {
    loading.value = true;
    try {
      await authService.logout();
      user.value = null;
      token.value = null;

      // Clear cases store to prevent showing previous user's cases
      const casesStore = useCasesStore();
      casesStore.$reset();
    } catch (err: any) {
      console.warn("Logout error: ", err)
    } finally {
      loading.value = false;
    }
  }

  function clearError() {
    error.value = null;
  }

  function checkAuth() {
    // Check if user is already logged in with proper token from local storage
    user.value = authService.getCurrentUser();
    token.value = authService.getAccessToken();
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    isStudent,
    isInstructor,
    isAdmin,
    login,
    register,
    logout,
    clearError,
    checkAuth,
  };
});

