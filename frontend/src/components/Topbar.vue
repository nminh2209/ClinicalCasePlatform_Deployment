<template>
<header class="top-header">
<div class="header-left flex items-center gap-4">
<!-- Menu button for mobile -->
<button
class="md:hidden p-2 rounded-lg hover:bg-gray-100"
@click="$emit('menu-click')"
>
<Menu class="w-6 h-6" />
</button>
<div class="search-container">
<svg
width="20"
height="20"
viewBox="0 0 24 24"
fill="none"
stroke="currentColor"
stroke-width="2"
class="search-icon"
>
<circle cx="11" cy="11" r="8" />
<path d="m21 21-4.35-4.35" />
</svg>
<input
type="text"
placeholder="Tìm kiếm bệnh nhân, hồ sơ bệnh án..."
class="search-input"
v-model="searchQuery"
/>
</div>
</div>

<div class="header-right">
      
      <NotificationCenter :user-role="user?.role" />

<div class="user-profile">
<img
:src="user?.avatar || '/api/placeholder/32/32'"
:alt="user?.first_name || 'User'"
class="user-avatar"
/>
<div class="user-info">
<span class="user-name"
>{{ user?.first_name }} {{ user?.last_name }}</span
>
<span class="user-role">{{ formatRole(user?.role) }}</span>
</div>
</div>
</div>
</header>
</template>

<script setup>
import { ref, computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import { Menu } from "lucide-vue-next";
import NotificationCenter from "./NotificationCenter.vue";

defineEmits(["menu-click"]);

const authStore = useAuthStore();
const router = useRouter();
const searchQuery = ref("");

const user = computed(() => authStore.user);

const formatRole = (role) => {
 const roleMap = {
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
   gap: 0.5rem;
 }

 .page-content {
   padding: 1rem;
 }

 .search-container {
   max-width: none;
   width: 100%;
 }

 .search-input {
   width: 100%;
   padding-left: 2.5rem;
   padding-right: 0.5rem;
 }

 .header-right {
   gap: 0.5rem;
 }

 .user-info {
   display: none;
 }

 .notification-btn {
   padding: 0.375rem;
 }

 .user-avatar {
   width: 32px;
   height: 32px;
 }
}
</style>