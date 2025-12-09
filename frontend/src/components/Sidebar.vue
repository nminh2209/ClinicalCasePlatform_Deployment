<template>
  <!-- Mobile hamburger button -->
  <button @click="toggleMobile" class="hamburger-btn md:hidden">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <line x1="3" y1="12" x2="21" y2="12" />
      <line x1="3" y1="6" x2="21" y2="6" />
      <line x1="3" y1="18" x2="21" y2="18" />
    </svg>
  </button>

  <!-- Mobile overlay -->
  <div v-if="isMobileOpen" @click="closeMobile" class="mobile-overlay md:hidden"></div>

  <!-- Sidebar -->
  <aside class="sidebar" :class="{
    'collapsed': isCollapsed && !isMobileOpen,
    'mobile-open': isMobileOpen
  }">
    <!-- Desktop toggle button - centered vertically -->
    <button @click="toggleCollapse" class="toggle-btn-center hidden md:flex"
      :title="isCollapsed ? 'Expand' : 'Collapse'">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline :points="isCollapsed ? '9,18 15,12 9,6' : '15,18 9,12 15,6'" />
      </svg>
    </button>

    <div class="sidebar-header">
      <div class="logo">
        <div class="logo-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
          </svg>
        </div>
        <span class="logo-text" v-show="!isCollapsed || isMobileOpen">Hồ sơ Bệnh án</span>
      </div>
    </div>

    <nav class="sidebar-nav">
      <!-- Home link (all roles) -->
      <router-link to="/home" class="nav-item" :class="{ active: $route.path === '/home' }"
        @click="closeMobileOnNavigate">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
          <polyline points="9,22 9,12 15,12 15,22" />
        </svg>
        <span v-show="!isCollapsed || isMobileOpen">Trang chính</span>
      </router-link>



      <!-- Student navigation -->
      <template v-if="role === 'student'">
        <router-link to="/cases" class="nav-item" :class="{ active: $route.path.includes('/cases') }"
          @click="closeMobileOnNavigate">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <polyline points="14,2 14,8 20,8" />
          </svg>
          <span v-show="!isCollapsed || isMobileOpen">Hồ sơ Bệnh án</span>
        </router-link>
        <router-link to="/patients" class="nav-item" :class="{ active: $route.path.includes('/patients') }"
          @click="closeMobileOnNavigate">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
          <span v-show="!isCollapsed || isMobileOpen">Bệnh nhân</span>
        </router-link>
        <router-link to="/public-feed" class="nav-item" :class="{ active: $route.path.includes('/public-feed') }"
          @click="closeMobileOnNavigate">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10" />
            <line x1="2" y1="12" x2="22" y2="12" />
            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
          </svg>
          <span v-show="!isCollapsed || isMobileOpen">Bệnh Án Công Khai</span>
        </router-link>
        <router-link to="/shared-cases" class="nav-item" :class="{ active: $route.path.includes('/shared-cases') }"
          @click="closeMobileOnNavigate">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
          </svg>
          <span v-show="!isCollapsed || isMobileOpen">Ca bệnh chia sẻ</span>
        </router-link>
      </template>






      <!-- Instructor navigation -->
      <template v-else-if="role === 'instructor'">
        <router-link to="/cases" class="nav-item" :class="{ active: $route.path.includes('/cases') }"
          @click="closeMobileOnNavigate">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <polyline points="14,2 14,8 20,8" />
          </svg>
          <span v-show="!isCollapsed || isMobileOpen">Hồ sơ Bệnh án</span>
        </router-link>

        <!-- NEED TO ADD A STUDENT PAGE -->
        <router-link to="/students" class="nav-item" :class="{ active: $route.path.includes('/students') }"
          @click="closeMobileOnNavigate">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
          <span v-show="!isCollapsed || isMobileOpen">Sinh viên</span>
        </router-link>

        <router-link to="/public-feed" class="nav-item" :class="{ active: $route.path.includes('/public-feed') }"
          @click="closeMobileOnNavigate">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10" />
            <line x1="2" y1="12" x2="22" y2="12" />
            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
          </svg>
          <span v-show="!isCollapsed || isMobileOpen">Bệnh Án Công Khai</span>
        </router-link>

        <router-link to="/shared-cases" class="nav-item" :class="{ active: $route.path.includes('/shared-cases') }"
          @click="closeMobileOnNavigate">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
          </svg>
          <span v-show="!isCollapsed || isMobileOpen">Ca bệnh chia sẻ</span>
        </router-link>
      </template>






      <!-- Admin navigation -->
      <template v-else-if="role === 'admin'">
        <router-link to="/users" class="nav-item" :class="{ active: $route.path.includes('/users') }"
          @click="closeMobileOnNavigate">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="8" r="4" />
            <path d="M6 20v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2" />
          </svg>
          <span v-show="!isCollapsed || isMobileOpen">Người Dùng</span>
        </router-link>
      </template>
    </nav>

    <div class="sidebar-footer">
      <button @click="logout" class="nav-item logout-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
          <polyline points="16,17 21,12 16,7" />
          <line x1="21" y1="12" x2="9" y2="12" />
        </svg>
        <span v-show="!isCollapsed || isMobileOpen">Đăng xuất</span>
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

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
  if (window.innerWidth < 768) {
    closeMobile();
  }
};

const logout = () => {
  authStore.logout();
  router.push("/login");
};
</script>

<style scoped>
/* Hamburger button for mobile */
.hamburger-btn {
  position: fixed;
  top: 1rem;
  left: 1rem;
  z-index: 1001;
  background: #1e40af;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.5rem;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.2s;
}

.hamburger-btn:hover {
  background: #1e3a8a;
  transform: scale(1.05);
}

/* Mobile overlay */
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

/* Sidebar Styles */
.sidebar {
  width: 230px;
  background: linear-gradient(180deg, #1e40af 0%, #1e3a8a 100%);
  color: white;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  transition: width 0.3s ease, transform 0.3s ease;
  position: relative;
  z-index: 100;
}

/* Desktop collapsed state */
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
    justify-content: center;
    padding: 0.75rem;
  }

  .sidebar.collapsed .sidebar-header {
    padding: 1.5rem 0.75rem;
  }

  .sidebar.collapsed .logo {
    justify-content: center;
  }
}

/* Mobile styles */
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
  background: #1e40af;
  border: 2px solid white;
  color: white;
  padding: 0.5rem;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  z-index: 1001;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.toggle-btn-center:hover {
  background: #1e3a8a;
  transform: translateY(-50%) scale(1.1);
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
  background: none;
  width: 100%;
  cursor: pointer;
  font-size: 0.875rem;
  white-space: nowrap;
}

.nav-item svg {
  flex-shrink: 0;
}

.nav-item span {
  transition: opacity 0.2s;
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
</style>
