<template>
  <div class="app-layout">
    <Sidebar />

    <!-- Main Content -->
    <div class="main-content">
      <!-- Top Header -->
      <Topbar />

      <!-- Page Content -->
      <main class="page-content">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import Sidebar from "./Sidebar.vue";
import Topbar from "./Topbar.vue";
import { ref, computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const router = useRouter();
const searchQuery = ref("");

const user = computed(() => authStore.user);

const formatRole = (role: string) => {
  const roleMap: Record<string, string> = {
    STUDENT: "Sinh viên Y khoa",
    INSTRUCTOR: "Giảng viên Lâm sàng",
    ADMIN: "Quản trị viên",
  };
  return roleMap[role] || role;
};

const logout = () => {
  authStore.logout();
  router.push("/login");
};
</script>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  background-color: #f8fafc;
}

/* Sidebar Styles */
.sidebar {
  width: 280px;
  background: linear-gradient(180deg, #1e40af 0%, #1e3a8a 100%);
  color: white;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-icon {
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-text {
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.2s;
  border: none;
  background: none;
  width: 100%;
  cursor: pointer;
  font-size: 0.875rem;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-item.active {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border-right: 3px solid #60a5fa;
}

.sidebar-footer {
  padding: 1rem 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.logout-btn {
  color: rgba(255, 255, 255, 0.7);
}

.logout-btn:hover {
  color: #fca5a5;
  background: rgba(239, 68, 68, 0.1);
}

/* Main Content Styles */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.top-header {
  height: 80px;
  background: white;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.header-left {
  flex: 1;
}

.search-container {
  position: relative;
  max-width: 400px;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #64748b;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.875rem;
  background: #f8fafc;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.notification-btn {
  position: relative;
  padding: 0.5rem;
  border: none;
  background: #f8fafc;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.notification-btn:hover {
  background: #e2e8f0;
}

.notification-badge {
  position: absolute;
  top: 0;
  right: 0;
  background: #ef4444;
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.user-profile:hover {
  background: #f8fafc;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #e2e8f0;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 600;
  color: #1f2937;
  font-size: 0.875rem;
}

.user-role {
  font-size: 0.75rem;
  color: #6b7280;
}

.page-content {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .sidebar {
    width: 240px;
  }

  .top-header {
    padding: 0 1rem;
  }

  .page-content {
    padding: 1rem;
  }

  .search-container {
    max-width: 200px;
  }

  .user-info {
    display: none;
  }
}
</style>
