import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { authService } from "@/services/auth";

export const useAuthStore = defineStore("auth", () => {
  const user = ref(authService.getCurrentUser());
  const isAuthenticated = computed(() => !!user.value);
  const isStudent = computed(() => user.value?.role === "student");
  const isInstructor = computed(() => user.value?.role === "instructor");
  const isAdmin = computed(() => user.value?.role === "admin");
  const loading = ref(false);
  const error = ref(null);

  async function login(email: string, password: string) {
    loading.value = true;
    error.value = null;
    try {
      const response = await authService.login(email, password);
      user.value = response.user;
      return response;
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
      const response = await authService.register(userData);
      user.value = response.user;
      return response;
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
    } catch (err: any) {
      console.warn("Logout error:", err);
    } finally {
      loading.value = false;
    }
  }

  function clearError() {
    error.value = null;
  }

  function checkAuth() {
    // Check if user is already authenticated from localStorage
    const currentUser = authService.getCurrentUser();
    if (currentUser) {
      user.value = currentUser;
    }
  }

  return {
    user,
    isAuthenticated,
    isStudent,
    isInstructor,
    isAdmin,
    loading,
    error,
    login,
    register,
    logout,
    clearError,
    checkAuth,
  };
});
