<template>
  <div class="home-page">
    <StudentDashboard v-if="role === 'student'" />
    <TeacherDashboard v-if="role === 'instructor'" />
    <AdminDashboard v-if="role === 'admin'" :onNavigate="handleNavigate" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

import StudentDashboard from "./StudentDashboard.vue";
import AdminDashboard from "./AdminDashboard.vue";
import TeacherDashboard from "./TeacherDashboard.vue";

const router = useRouter();
const authStore = useAuthStore();
const user = computed(() => authStore.user);
const role = computed(() => user?.value?.role || null);

// Navigation handler for AdminDashboard
const handleNavigate = (page: string) => {
  router.push(`/${page}`);
};

// Check authentication on mount
onMounted(() => {
  if (!authStore.isAuthenticated || !user.value) {
    router.push("/login");
  } else {
    // Debug: log the user role
    console.log("User logged in with role:", role.value);
    console.log("User object:", user.value);
  }
});

// Dashboard data
const dashboardStats = ref({
  totalCases: 1284,
  todayReviews: 24,
  pendingReports: 12,
  activeCases: 38,
});

const todayReviews = ref([
  {
    id: 1,
    patient: "John Smith",
    type: "Regular Checkup",
    time: "09:00 AM",
    status: "Confirmed",
  },
  {
    id: 2,
    patient: "Emily Davis",
    type: "Follow-up",
    time: "10:30 AM",
    status: "Confirmed",
  },
  {
    id: 3,
    patient: "Michael Brown",
    type: "Lab Results Review",
    time: "11:45 AM",
    status: "Waiting",
  },
  {
    id: 4,
    patient: "Sarah Wilson",
    type: "New Patient",
    time: "02:00 PM",
    status: "Confirmed",
  },
]);

const recentCases = ref([
  {
    id: "P001",
    patient: "John Smith",
    age: "45y",
    updated_at: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
  },
  {
    id: "P002",
    patient: "Emily Davis",
    age: "32y",
    updated_at: new Date(Date.now() - 5 * 60 * 60 * 1000), // 5 hours ago
  },
  {
    id: "P003",
    patient: "Robert Chen",
    age: "58y",
    updated_at: new Date(Date.now() - 24 * 60 * 60 * 1000), // 1 day ago
  },
  {
    id: "P004",
    patient: "Lisa Anderson",
    age: "41y",
    updated_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000), // 3 days ago
  },
]);

const formatName = (firstName: string, lastName: string) => {
  if (!firstName) return "User";
  return lastName ? `${firstName} ${lastName}` : firstName;
};

const formatTimeAgo = (date: Date) => {
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
  const diffDays = Math.floor(diffHours / 24);

  if (diffHours < 1) return "Just now";
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays === 1) return "Yesterday";
  return `${diffDays} days ago`;
};
</script>

<style scoped>
/* Home Page - Renders role-based dashboards */
.home-page {
  min-height: 100vh;
  background: var(--background);
  color: var(--foreground);
}
</style>
