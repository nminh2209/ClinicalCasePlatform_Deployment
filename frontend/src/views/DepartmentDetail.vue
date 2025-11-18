<template>
  <div class="p-6">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-2xl font-semibold">Khoa: {{ departmentName }}</h2>
      <router-link :to="`/users?department=${encodeURIComponent(departmentName)}`" class="btn">Xem người dùng trong khoa</router-link>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-white shadow rounded p-4">
        <h3 class="text-lg font-medium mb-2">Tổng quan</h3>
        <p class="text-sm text-gray-600 mb-3">Một cái nhìn nhanh về các chỉ số chính của khoa.</p>
        <ul class="space-y-2 text-sm">
          <li>Giảng viên: <strong>{{ dept.teachers }}</strong></li>
          <li>Sinh viên: <strong>{{ dept.students }}</strong></li>
          <li>Bệnh án đang hoạt động: <strong>{{ dept.activeCases }}</strong></li>
        </ul>
      </div>

      <div class="bg-white shadow rounded p-4">
        <h3 class="text-lg font-medium mb-2">Hoạt động gần đây</h3>
        <p class="text-sm text-gray-600">(Ví dụ dữ liệu)</p>
        <ul class="mt-2 space-y-2 text-sm">
          <li>Bài nộp mới: 12</li>
          <li>Điểm trung bình: 86%</li>
          <li>Truy cập gần nhất: 2025-11-10</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const departmentName = String(route.params.name || route.query.name || 'Không rõ');

// Mock departments used in dashboard — duplicate to keep view standalone
const departments = [
  { name: "Tim mạch", teachers: 4, students: 24, activeCases: 8, color: "#1E88E5" },
  { name: "Hô hấp", teachers: 3, students: 18, activeCases: 6, color: "#43A047" },
  { name: "Thần kinh", teachers: 4, students: 28, activeCases: 10, color: "#FB8C00" },
  { name: "Tiêu hóa", teachers: 3, students: 20, activeCases: 7, color: "#E53935" },
  { name: "Nội tiết", teachers: 3, students: 22, activeCases: 6, color: "#8E24AA" },
  { name: "Thận", teachers: 3, students: 19, activeCases: 5, color: "#00ACC1" },
  { name: "Ung bướu", teachers: 4, students: 25, activeCases: 6, color: "#FDD835" }
];

const dept = computed(() => departments.find(d => d.name === departmentName) || { name: departmentName, teachers: 0, students: 0, activeCases: 0 });
</script>

<style scoped>
.btn { background: #1e40af; color: #fff; padding: 6px 10px; border-radius: 6px; }
</style>
