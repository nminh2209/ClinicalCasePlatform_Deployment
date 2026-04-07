<template>
  <header class="top-header">
    <div class="header-left flex items-center gap-4">
      <div class="md:hidden">
        <Button
          text
          rounded
          aria-label="Toggle menu"
          icon="pi pi-bars"
          @click="$emit('menu-click')"
          class="p-2"
        />
      </div>
    </div>

    <div class="header-right">
      <NotificationCenter :user-role="user?.role" />

      <RouterLink to="/profile" class="user-profile" title="Hồ sơ cá nhân">
        <Avatar
          :image="user?.avatar || undefined"
          :label="!user?.avatar ? userInitials : undefined"
          shape="circle"
          class="user-avatar"
        />
        <div class="user-info">
          <span class="user-name"
            >{{ user?.first_name }} {{ user?.last_name }}</span
          >
          <span class="user-role">{{ formatRole(user?.role) }}</span>
        </div>
      </RouterLink>
    </div>
  </header>
</template>

<script setup>
import { computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import Button from "primevue/button";
import Avatar from "primevue/avatar";
import NotificationCenter from "./NotificationCenter.vue";

defineEmits(["menu-click"]);

const authStore = useAuthStore();

const user = computed(() => authStore.user);

const userInitials = computed(() => {
  const first = user.value?.first_name?.[0] ?? "";
  const last = user.value?.last_name?.[0] ?? "";
  return (first + last).toUpperCase() || "?";
});

const formatRole = (role) => {
  const roleMap = {
    student: "Sinh viên Y khoa",
    instructor: "Giảng viên Lâm sàng",
    admin: "Quản trị viên",
  };
  return roleMap[role] || role;
};
</script>

<style scoped>
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
  max-width: 400px;
  width: 100%;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.75rem !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 8px !important;
  font-size: 0.875rem !important;
  background: #f8fafc !important;
}

.search-input:focus {
  border-color: #3b82f6 !important;
  background: white !important;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
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
  width: 40px !important;
  height: 40px !important;
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

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.page-content {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
}

@media (max-width: 768px) {
  .top-header {
    padding: 0 1rem;
    gap: 0.5rem;
  }

  .page-content {
    padding: 1rem;
  }

  .search-container {
    max-width: none;
    width: 100%;
  }

  .header-right {
    gap: 0.5rem;
  }

  .user-info {
    display: none;
  }

  .user-avatar {
    width: 32px !important;
    height: 32px !important;
  }
}
</style>
