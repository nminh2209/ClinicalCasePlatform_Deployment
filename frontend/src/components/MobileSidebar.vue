<template>
  <template v-if="isOpen">
    <!-- Overlay -->
    <div class="fixed inset-0 bg-black/50 z-40 md:hidden" @click="emit('close')" />

    <!-- Sidebar -->
    <div class="fixed inset-y-0 left-0 w-64 bg-white border-r border-gray-200 z-50 md:hidden">
      <!-- Logo -->
      <div class="h-16 flex items-center justify-between px-6 border-b border-gray-200">
        <div class="flex items-center">
          <div class="w-10 h-10 bg-primary rounded-lg flex items-center justify-center mr-3">
            <Activity class="w-6 h-6 text-white" />
          </div>
          <span class="text-gray-800">{{ title }}</span>
        </div>
        <Button variant="ghost" size="icon" @click="emit('close')">
          <X class="w-5 h-5" />
        </Button>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 px-4 py-6 space-y-2">
        <button v-for="item in menuItems" :key="item.id" @click="
          emit('navigate', item.id);
        emit('close');
        " :class="[
            'w-full flex items-center px-4 py-3 rounded-lg transition-colors',
            currentPage === item.id
              ? 'bg-primary text-white'
              : 'text-gray-600 hover:bg-gray-100',
          ]">
          <component :is="item.icon" class="w-5 h-5 mr-3" />
          <span>{{ item.label }}</span>
        </button>
      </nav>

      <!-- Logout Button -->
      <div class="p-4 border-t border-gray-200">
        <Button @click="
          emit('logout');
        emit('close');
        " variant="outline" class="w-full justify-start text-gray-600 hover:text-gray-800">
          <LogOut class="w-5 h-5 mr-3" />
          Logout
        </Button>
      </div>
    </div>
  </template>
</template>

<script setup>
import { computed } from "vue";
import {
  LayoutDashboard,
  Users,
  Calendar,
  FileText,
  Settings,
  Activity,
  LogOut,
  X,
  GraduationCap,
} from "lucide-vue-next";
import { default as Button } from "./ui/Button.vue";

const props = defineProps({
  isOpen: Boolean,
  currentPage: String,
  userType: {
    type: String,
    validator: (value) =>
      ["student", "teacher", "admin", undefined].includes(value),
  },
});

const emit = defineEmits(["navigate", "close", "logout"]);

const menuItems = computed(() => {
  if (props.userType === "student") {
    return [
      { id: "dashboard", label: "My Cases", icon: LayoutDashboard },
      { id: "settings", label: "Settings", icon: Settings },
    ];
  } else if (props.userType === "teacher") {
    return [
      { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
      { id: "students", label: "My Students", icon: GraduationCap },
      { id: "settings", label: "Settings", icon: Settings },
    ];
  } else if (props.userType === "admin") {
    return [
      { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
      { id: "settings", label: "Settings", icon: Settings },
    ];
  } else {
    return [
      { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
      { id: "patients", label: "Patients", icon: Users },
      { id: "appointments", label: "Appointments", icon: Calendar },
      { id: "reports", label: "Reports", icon: FileText },
      { id: "settings", label: "Settings", icon: Settings },
    ];
  }
});

const title = computed(() => {
  if (props.userType === "student") return "MediCare Learning";
  if (props.userType === "teacher") return "MediCare Teaching";
  if (props.userType === "admin") return "MediCare Admin";
  return "MediCare EMR";
});
</script>
