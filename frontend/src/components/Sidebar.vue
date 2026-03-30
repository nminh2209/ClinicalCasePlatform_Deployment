<template>
  <div class="md:hidden">
    <Button
      @click="toggleMobile"
      class="hamburger-btn"
      text
      rounded
      aria-label="Toggle menu"
      icon="pi pi-bars"
    />
  </div>

  <div
    v-if="isMobileOpen"
    @click="closeMobile"
    class="mobile-overlay md:hidden"
  />

  <aside
    class="sidebar"
    :class="{
      collapsed: isCollapsed && !isMobileOpen,
      'mobile-open': isMobileOpen,
    }"
  >
    <Button
      @click="toggleCollapse"
      class="toggle-btn-center hidden md:flex"
      :title="isCollapsed ? 'Expand' : 'Collapse'"
      :icon="isCollapsed ? 'pi pi-chevron-right' : 'pi pi-chevron-left'"
      text
      rounded
      severity="secondary"
    />

    <div class="sidebar-header">
      <div class="logo">
        <div class="logo-icon">
          <i class="pi pi-heart-fill" style="font-size: 1.25rem" />
        </div>
        <span class="logo-text" v-show="!isCollapsed || isMobileOpen">
          Hồ sơ Bệnh án
        </span>
      </div>
    </div>

    <nav class="sidebar-nav">
      <router-link
        to="/home"
        class="nav-item"
        :class="{ active: $route.path === '/home' }"
        @click="closeMobileOnNavigate"
      >
        <i class="pi pi-home" />
        <span v-show="!isCollapsed || isMobileOpen">Trang chính</span>
      </router-link>

      <template v-if="role === 'student'">
        <router-link
          to="/cases"
          class="nav-item"
          :class="{ active: $route.path.includes('/cases') }"
          @click="closeMobileOnNavigate"
        >
          <i class="pi pi-file" />
          <span v-show="!isCollapsed || isMobileOpen">Hồ sơ Bệnh án</span>
        </router-link>

        <router-link
          to="/patients"
          class="nav-item"
          :class="{ active: $route.path.includes('/patients') }"
          @click="closeMobileOnNavigate"
        >
          <i class="pi pi-user" />
          <span v-show="!isCollapsed || isMobileOpen">Bệnh nhân</span>
        </router-link>

        <router-link
          to="/public-feed"
          class="nav-item"
          :class="{ active: $route.path.includes('/public-feed') }"
          @click="closeMobileOnNavigate"
        >
          <i class="pi pi-globe" />
          <span v-show="!isCollapsed || isMobileOpen">Bệnh Án Công Khai</span>
        </router-link>

        <router-link
          to="/shared-cases"
          class="nav-item"
          :class="{ active: $route.path.includes('/shared-cases') }"
          @click="closeMobileOnNavigate"
        >
          <i class="pi pi-arrow-right-arrow-left" />
          <span v-show="!isCollapsed || isMobileOpen">Ca bệnh chia sẻ</span>
        </router-link>
      </template>

      <template v-else-if="role === 'instructor'">
        <router-link
          to="/cases"
          class="nav-item"
          :class="{ active: $route.path.includes('/cases') }"
          @click="closeMobileOnNavigate"
        >
          <i class="pi pi-file-edit" />
          <span v-show="!isCollapsed || isMobileOpen">Chấm điểm Bệnh án</span>
        </router-link>

        <router-link
          to="/students"
          class="nav-item"
          :class="{ active: $route.path.includes('/students') }"
          @click="closeMobileOnNavigate"
        >
          <i class="pi pi-user" />
          <span v-show="!isCollapsed || isMobileOpen">Sinh viên</span>
        </router-link>

        <router-link
          to="/public-feed"
          class="nav-item"
          :class="{ active: $route.path.includes('/public-feed') }"
          @click="closeMobileOnNavigate"
        >
          <i class="pi pi-globe" />
          <span v-show="!isCollapsed || isMobileOpen">Bệnh Án Công Khai</span>
        </router-link>

        <router-link
          to="/shared-cases"
          class="nav-item"
          :class="{ active: $route.path.includes('/shared-cases') }"
          @click="closeMobileOnNavigate"
        >
          <i class="pi pi-arrow-right-arrow-left" />
          <span v-show="!isCollapsed || isMobileOpen">Ca bệnh chia sẻ</span>
        </router-link>
      </template>

      <template v-else-if="role === 'admin'">
        <router-link
          to="/admin/users"
          class="nav-item"
          :class="{ active: $route.path === '/admin/users' }"
          @click="closeMobileOnNavigate"
        >
          <i class="pi pi-users" />
          <span v-show="!isCollapsed || isMobileOpen">Quản lý Người dùng</span>
        </router-link>
      </template>
    </nav>

    <div class="sidebar-footer">
      <Button
        @click="logout"
        class="nav-item logout-btn"
        :label="!isCollapsed || isMobileOpen ? 'Đăng xuất' : undefined"
        icon="pi pi-sign-out"
        text
      />
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import Button from "primevue/button";

const authStore = useAuthStore();
const router = useRouter();

const user = computed(() => authStore.user);
const role = computed(() => user.value?.role || "");

const isCollapsed = ref(false);
const isMobileOpen = ref(false);

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value;
};
const toggleMobile = () => {
  isMobileOpen.value = !isMobileOpen.value;
};
const closeMobile = () => {
  isMobileOpen.value = false;
};

const closeMobileOnNavigate = () => {
  if (window.innerWidth < 768) closeMobile();
};

const logout = () => {
  authStore.logout();
  router.push("/login");
};
</script>

<style scoped>
.hamburger-btn {
  position: fixed;
  top: 1rem;
  left: 1rem;
  z-index: 1001;
  background: #1e40af !important;
  color: white !important;
  border: none;
  border-radius: 8px;
  padding: 0.5rem;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.2s;
}

.hamburger-btn:hover {
  background: #1e3a8a !important;
  transform: scale(1.05);
}

.mobile-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
  animation: fadeIn 0.2s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.sidebar {
  width: 230px;
  background: linear-gradient(180deg, #1e40af 0%, #1e3a8a 100%);
  color: white;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  transition:
    width 0.3s ease,
    transform 0.3s ease;
  position: relative;
  z-index: 100;
}

@media (min-width: 768px) {
  .sidebar.collapsed {
    width: 60px;
  }

  .sidebar.collapsed .logo-text,
  .sidebar.collapsed .nav-item span {
    opacity: 0;
    pointer-events: none;
  }

  .sidebar.collapsed .nav-item {
    justify-content: center !important;
    padding: 0.75rem !important;
    gap: 0 !important;
  }

  .sidebar.collapsed .nav-item :deep(.p-button-content),
  .sidebar.collapsed .nav-item :deep(.p-button-icon) {
    justify-content: center;
    margin: 0;
  }

  .sidebar.collapsed .sidebar-header {
    padding: 1.5rem 0.75rem;
  }
  .sidebar.collapsed .logo {
    justify-content: center;
  }
}

@media (max-width: 767px) {
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    transform: translateX(-100%);
    z-index: 1000;
  }

  .sidebar.mobile-open {
    transform: translateX(0);
  }
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  transition: all 0.3s;
  flex: 1;
}

.logo-icon {
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: white;
}

.logo-text {
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  white-space: nowrap;
  transition: opacity 0.2s;
}

.toggle-btn-center {
  position: absolute;
  top: 50%;
  right: -16px;
  transform: translateY(-50%);
  background: #1e40af !important;
  border: 2px solid white !important;
  color: white !important;
  padding: 0 !important;
  border-radius: 50% !important;
  cursor: pointer;
  transition: all 0.2s;
  align-items: center;
  justify-content: center;
  width: 32px !important;
  height: 32px !important;
  min-width: 32px !important;
  z-index: 1001;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.toggle-btn-center:hover {
  background: #1e3a8a !important;
  transform: translateY(-50%) scale(1.1) !important;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0;
  overflow-y: auto;
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
  background: none !important;
  width: 100%;
  cursor: pointer;
  font-size: 0.875rem;
  white-space: nowrap;
  border-radius: 0 !important;
  justify-content: flex-start !important;
  box-shadow: none !important;
}

.nav-item :deep(.p-button-label) {
  font-size: 0.875rem;
  font-weight: 400;
}

.nav-item .pi {
  flex-shrink: 0;
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.8);
}

.nav-item span {
  transition: opacity 0.2s;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1) !important;
  color: white;
}

.nav-item.active {
  background: rgba(255, 255, 255, 0.15) !important;
  color: white;
  border-right: 3px solid #60a5fa;
}

.sidebar-footer {
  padding: 1rem 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.logout-btn {
  color: rgba(255, 255, 255, 0.7) !important;
}

.logout-btn :deep(.p-button-icon),
.logout-btn :deep(.p-button-label) {
  color: rgba(255, 255, 255, 0.7) !important;
}

.logout-btn:hover {
  color: #fca5a5 !important;
  background: rgba(239, 68, 68, 0.1) !important;
}

.logout-btn:hover :deep(.p-button-icon),
.logout-btn:hover :deep(.p-button-label) {
  color: #fca5a5 !important;
}
</style>
