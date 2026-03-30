<template>
  <div class="p-6 space-y-6">
    <!-- Page Header -->
    <div>
      <h1 class="text-2xl font-bold text-gray-800 mb-2">
        {{ t("admin.title") }}
      </h1>
      <p class="text-gray-600">{{ t("admin.overview") }}</p>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- Total Users -->
      <div
        class="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow"
      >
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-500">
                {{ t("admin.totalUsers") }}
              </p>
              <p class="text-3xl font-bold text-gray-900 mt-2">
                {{ stats.totalStudents + stats.totalTeachers }}
              </p>
              <p class="text-xs text-gray-500 mt-1">Sinh viên + Giảng viên</p>
            </div>
            <div class="p-3 bg-blue-50 rounded-lg">
              <Users class="h-6 w-6 text-blue-600" />
            </div>
          </div>
        </div>
      </div>

      <!-- Active Students -->
      <div
        class="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow"
      >
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-500">
                {{ t("admin.activeStudents") }}
              </p>
              <p class="text-3xl font-bold text-gray-900 mt-2">
                {{ stats.totalStudents }}
              </p>
              <p class="text-xs text-gray-500 mt-1">Sinh viên đang học</p>
            </div>
            <div class="p-3 bg-green-50 rounded-lg">
              <GraduationCap class="h-6 w-6 text-green-600" />
            </div>
          </div>
        </div>
      </div>

      <!-- Teachers -->
      <div
        class="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow"
      >
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-500">
                {{ t("admin.teachers") }}
              </p>
              <p class="text-3xl font-bold text-gray-900 mt-2">
                {{ stats.totalTeachers }}
              </p>
              <p class="text-xs text-gray-500 mt-1">Giảng viên hoạt động</p>
            </div>
            <div class="p-3 bg-purple-50 rounded-lg">
              <Users class="h-6 w-6 text-purple-600" />
            </div>
          </div>
        </div>
      </div>

      <!-- Submissions -->
      <div
        class="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow"
      >
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-500">Bài nộp</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">
                {{ stats.totalSubmissions }}
              </p>
              <p class="text-xs text-gray-500 mt-1">Tổng số bài</p>
            </div>
            <div class="p-3 bg-yellow-50 rounded-lg">
              <Activity class="h-6 w-6 text-yellow-600" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Section -->
    <Tabs value="0" class="w-full">
      <TabList class="flex border-b border-gray-200">
        <Tab value="0" class="flex items-center gap-2 px-4 py-2">
          <TrendingUp class="h-4 w-4" />
          {{ t("admin.statistics") }}
        </Tab>
        <Tab value="1" class="flex items-center gap-2 px-4 py-2">
          <BarChart3 class="h-4 w-4" />
          Khoa
        </Tab>
        <Tab value="2" class="flex items-center gap-2 px-4 py-2">
          <Activity class="h-4 w-4" />
          Hoạt động
        </Tab>
      </TabList>

      <TabPanels>
      <!-- Analytics Tab -->
      <TabPanel value="0" class="space-y-6 pt-4">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- User Growth Chart -->
          <Card class="bg-white">
            <template #title>{{ t("admin.userGrowth") }}</template>
            <template #subtitle>Tăng trưởng sinh viên và giảng viên theo tháng</template>
            <template #content>
              <div
                class="w-full h-72 bg-gray-50 rounded-lg p-4 flex flex-col justify-between"
              >
                <div class="flex h-full gap-2">
                  <div
                    class="flex flex-col justify-between text-xs text-gray-500 pr-2 border-r border-gray-300 min-w-max"
                  >
                    <span>160</span>
                    <span>120</span>
                    <span>80</span>
                    <span>40</span>
                    <span>0</span>
                  </div>
                  <div class="flex items-end justify-between flex-1 gap-2">
                    <div
                      v-for="(item, idx) in userGrowthData"
                      :key="idx"
                      class="flex-1 flex flex-col items-center gap-2"
                    >
                      <div
                        class="w-full flex gap-1 items-end justify-center h-40"
                      >
                        <div
                          class="flex-1 bg-blue-500 rounded-t opacity-80 hover:opacity-100 cursor-pointer transition-opacity relative group/bar"
                          :style="{ height: (item.students / 160) * 100 + '%' }"
                        >
                          <div
                            class="absolute -top-6 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover/bar:opacity-100 transition-opacity whitespace-nowrap z-50 pointer-events-none"
                          >
                            Sinh viên: {{ item.students }}
                          </div>
                        </div>
                        <div
                          class="flex-1 bg-green-500 rounded-t opacity-80 hover:opacity-100 cursor-pointer transition-opacity relative group/bar"
                          :style="{ height: (item.teachers / 160) * 100 + '%' }"
                        >
                          <div
                            class="absolute -top-6 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover/bar:opacity-100 transition-opacity whitespace-nowrap z-50 pointer-events-none"
                          >
                            Giảng viên: {{ item.teachers }}
                          </div>
                        </div>
                      </div>
                      <span class="text-xs text-gray-600 truncate">{{
                        item.month.replace("Tháng ", "T")
                      }}</span>
                    </div>
                  </div>
                </div>
                <div
                  class="flex justify-center gap-4 mt-4 text-xs border-t pt-3"
                >
                  <div class="flex items-center gap-2">
                    <div class="w-3 h-3 bg-blue-500 rounded"></div>
                    <span>Sinh viên</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <div class="w-3 h-3 bg-green-500 rounded"></div>
                    <span>Giảng viên</span>
                  </div>
                </div>
              </div>
            </template>
          </Card>

          <!-- Submission Trend Chart -->
          <Card class="bg-white">
            <template #title>{{ t("admin.caseSubmissions") }}</template>
            <template #subtitle>Số lượng bài nộp theo tháng</template>
            <template #content>
              <div
                class="w-full h-72 bg-gray-50 rounded-lg p-4 flex flex-col justify-between"
              >
                <div class="flex h-40 gap-2 mb-4">
                  <div
                    class="flex flex-col justify-between text-xs text-gray-500 pr-2 border-r border-gray-300 min-w-max"
                  >
                    <span>200</span>
                    <span>150</span>
                    <span>100</span>
                    <span>50</span>
                    <span>0</span>
                  </div>
                  <div class="flex items-end justify-between flex-1 gap-2">
                    <div
                      v-for="(item, idx) in submissionData"
                      :key="idx"
                      class="flex-1 group relative"
                    >
                      <div
                        class="w-full bg-blue-500 rounded-t hover:opacity-80 cursor-pointer transition-opacity relative"
                        :style="{
                          height: (item.submissions / 200) * 160 + 'px',
                        }"
                      >
                        <div
                          class="absolute -top-6 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-50 pointer-events-none"
                        >
                          {{ item.submissions }} bài
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="grid grid-cols-6 gap-2 text-xs text-gray-600 mt-4">
                  <div
                    v-for="item in submissionData"
                    :key="item.month"
                    class="text-center truncate"
                  >
                    {{ item.month.replace("Tháng ", "T") }}
                  </div>
                </div>
              </div>
            </template>
          </Card>

          <!-- Student Distribution by Department -->
          <Card class="bg-white">
            <template #title>{{ t("admin.departmentActivity") }}</template>
            <template #subtitle>Phân bố sinh viên theo khoa</template>
            <template #content>
              <div
                class="w-full h-72 flex flex-col items-center justify-center"
              >
                <div class="relative">
                  <svg
                    width="200"
                    height="200"
                    viewBox="0 0 280 280"
                    class="drop-shadow-lg"
                  >
                    <g v-for="(slice, idx) in pieslices" :key="idx">
                      <path
                        :d="slice.path"
                        :fill="slice.color"
                        stroke="white"
                        stroke-width="2"
                      />
                    </g>
                  </svg>
                  <div
                    class="absolute inset-0 flex items-center justify-center"
                  >
                    <div
                      class="w-20 h-20 bg-white rounded-full flex flex-col items-center justify-center shadow-lg border-4 border-gray-50"
                    >
                      <div class="text-center">
                        <p class="text-lg font-bold text-gray-800">
                          {{
                            departments.reduce(
                              (s: number, d: any) => s + d.students,
                              0,
                            )
                          }}
                        </p>
                        <p class="text-xs text-gray-600">sinh viên</p>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="grid grid-cols-2 gap-2 text-xs w-full mt-4 px-4">
                  <div
                    v-for="dept in departmentDistribution"
                    :key="dept.name"
                    class="flex items-center gap-2"
                  >
                    <div
                      class="w-3 h-3 rounded-full"
                      :style="{ backgroundColor: dept.color }"
                    ></div>
                    <span class="truncate"
                      >{{ dept.name }}: {{ dept.value }}</span
                    >
                  </div>
                </div>
              </div>
            </template>
          </Card>

          <Card class="bg-white">
            <template #title>{{ t("admin.performanceMetrics") }}</template>
            <template #subtitle>Số bệnh án theo khoa (tỉ lệ tương đối)</template>
            <template #content>
              <div class="w-full h-72 flex flex-col justify-between">
                <div class="space-y-2">
                  <div
                    v-for="dept in performanceData"
                    :key="dept.department"
                    class="flex items-center gap-3 group"
                  >
                    <div
                      class="w-24 text-sm font-medium text-gray-700 truncate"
                    >
                      {{ dept.department }}
                    </div>
                    <div
                      class="flex-1 bg-gray-200 rounded-full h-6 overflow-visible relative group/bar"
                    >
                      <div
                        class="bg-green-500 h-full rounded-full hover:opacity-80 transition-opacity"
                        :style="{ width: dept.avgGrade + '%' }"
                      ></div>
                      <span
                        class="absolute right-2 top-1/2 transform -translate-y-1/2 text-xs font-semibold text-white mix-blend-darken"
                      >
                        {{ dept.submissions }}
                      </span>
                      <div
                        class="absolute -top-6 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover/bar:opacity-100 transition-opacity whitespace-nowrap z-50 pointer-events-none"
                      >
                        {{ dept.submissions }} bệnh án
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </template>
          </Card>
        </div>
      </TabPanel>

      <!-- Departments Tab -->
      <TabPanel value="1">
        <Card class="bg-white">
          <template #title>Tổng quan các khoa</template>
          <template #subtitle>Chuyên khoa y khoa và thống kê. Nhấp vào khoa để xem chi tiết người dùng</template>
          <template #content>
            <div class="space-y-3">
              <div
                v-for="(dept, index) in departments"
                :key="index"
                class="p-4 border border-gray-200 rounded-lg hover:bg-blue-50 hover:border-blue-300 transition-all cursor-pointer hover:shadow-sm"
                @click="navigateToDepartment(String(dept.id))"
              >
                <div
                  class="flex flex-col md:flex-row md:items-center justify-between gap-3"
                >
                  <div class="flex items-center gap-3">
                    <div
                      class="w-4 h-4 rounded-full"
                      :style="{ backgroundColor: dept.color }"
                    ></div>
                    <div>
                      <h3 class="text-base font-semibold text-gray-900 mb-2">
                        {{ dept.vietnamese_name }}
                      </h3>
                      <div class="flex flex-wrap gap-4 text-sm text-gray-600">
                        <div class="flex items-center gap-1.5">
                          <Users class="h-4 w-4" />
                          <span>{{ dept.teachers }} Giảng viên</span>
                        </div>
                        <div class="flex items-center gap-1.5">
                          <GraduationCap class="h-4 w-4" />
                          <span>{{ dept.students }} Sinh viên</span>
                        </div>
                        <div class="flex items-center gap-1.5">
                          <BookOpen class="h-4 w-4" />
                          <span>{{ dept.activeCases }} Bệnh án</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <Badge value="Hoạt động" severity="success" />
                </div>
              </div>
            </div>
          </template>
        </Card>
      </TabPanel>

      <!-- Activity Tab -->
      <TabPanel value="2">
        <Card class="bg-white">
          <template #title>Hoạt động gần đây</template>
          <template #subtitle>Cập nhật và thay đổi hệ thống mới nhất</template>
          <template #content>
            <div class="space-y-3">
              <div
                v-for="(activity, index) in recentActivity"
                :key="index"
                class="flex items-start gap-3 p-4 border border-gray-200 rounded-lg"
              >
                <div class="w-2 h-2 rounded-full mt-2 bg-blue-500"></div>
                <div class="flex-1">
                  <p class="text-sm text-gray-900 font-medium">
                    {{ activity.message }}
                  </p>
                  <p class="text-xs text-gray-500 mt-1">
                    {{ formatDate(activity.timestamp) }}
                  </p>
                </div>
              </div>
            </div>
          </template>
        </Card>
      </TabPanel>
      </TabPanels>
    </Tabs>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import {
  Users,
  GraduationCap,
  BookOpen,
  Activity,
  TrendingUp,
  BarChart3,
} from "lucide-vue-next";
import Card from "primevue/card";
import Badge from "primevue/badge";
import Tabs from "primevue/tabs";
import TabList from "primevue/tablist";
import Tab from "primevue/tab";
import TabPanels from "primevue/tabpanels";
import TabPanel from "primevue/tabpanel";
import api from "@/services/api";

const router = useRouter();

interface AdminDashboardProps {
  onNavigate: (page: string) => void;
}

const props = defineProps<AdminDashboardProps>();

// Translation helper - replace with your i18n solution
const t = (key: string) => {
  const translations: Record<string, string> = {
    "admin.title": "Bảng điều khiển Quản trị",
    "admin.overview": "Tổng quan hệ thống và thống kê",
    "admin.totalUsers": "Tổng người dùng",
    "admin.activeStudents": "Sinh viên",
    "admin.teachers": "Giảng viên",
    "admin.statistics": "Thống kê",
    "admin.userGrowth": "Tăng trưởng người dùng",
    "admin.caseSubmissions": "Bài nộp",
    "admin.departmentActivity": "Hoạt động khoa",
    "admin.performanceMetrics": "Hiệu suất",
  };
  return translations[key] || key;
};

// Live data from backend
const stats = ref({
  totalStudents: 0,
  totalTeachers: 0,
  activeCases: 0,
  totalSubmissions: 0,
});

const departments = ref<
  Array<{
    id: number;
    name: string;
    vietnamese_name: string;
    teachers: number;
    students: number;
    activeCases: number;
    color: string;
  }>
>([]);

const colors = [
  "#1E88E5",
  "#43A047",
  "#FB8C00",
  "#E53935",
  "#8E24AA",
  "#00ACC1",
  "#FDD835",
  "#5E35B1",
  "#D81B60",
];

// Load departments and their stats from backend
async function loadDepartmentData() {
  try {
    // Fetch all departments
    const deptsRes = await api.get("/cases/departments/");
    const deptsList = deptsRes.data.results
      ? deptsRes.data.results
      : Array.isArray(deptsRes.data)
        ? deptsRes.data
        : [];

    // For each department, fetch user and case counts
    const departmentsWithStats = await Promise.all(
      deptsList.map(async (dept: any, idx: number) => {
        try {
          // Count students in this department
          const studentsRes = await api.get("/auth/users/", {
            params: { role: "student", department: dept.id },
          });
          const studentsList = studentsRes.data.results
            ? studentsRes.data.results
            : Array.isArray(studentsRes.data)
              ? studentsRes.data
              : [];
          const studentCount = studentsList.length;

          // Count teachers in this department
          const teachersRes = await api.get("/auth/users/", {
            params: { role: "instructor", department: dept.id },
          });
          const teachersList = teachersRes.data.results
            ? teachersRes.data.results
            : Array.isArray(teachersRes.data)
              ? teachersRes.data
              : [];
          const teacherCount = teachersList.length;

          // Count cases in this department
          // Assuming cases are linked via repository__department
          const casesRes = await api.get("/cases/", {
            params: { repository__department: dept.id },
          });
          const casesList = casesRes.data.results
            ? casesRes.data.results
            : Array.isArray(casesRes.data)
              ? casesRes.data
              : [];
          const caseCount = casesList.length;

          return {
            id: dept.id,
            name: dept.name,
            vietnamese_name: dept.vietnamese_name || dept.name,
            teachers: teacherCount,
            students: studentCount,
            activeCases: caseCount,
            color: colors[idx % colors.length],
          };
        } catch (error) {
          console.error(
            `Error loading stats for department ${dept.name}:`,
            error,
          );
          return {
            id: dept.id,
            name: dept.name,
            vietnamese_name: dept.vietnamese_name || dept.name,
            teachers: 0,
            students: 0,
            activeCases: 0,
            color: colors[idx % colors.length],
          };
        }
      }),
    );

    departments.value = departmentsWithStats;

    // Aggregate stats
    stats.value.totalStudents = departmentsWithStats.reduce(
      (sum, d) => sum + d.students,
      0,
    );
    stats.value.totalTeachers = departmentsWithStats.reduce(
      (sum, d) => sum + d.teachers,
      0,
    );
    stats.value.activeCases = departmentsWithStats.reduce(
      (sum, d) => sum + d.activeCases,
      0,
    );
  } catch (error) {
    console.error("Error loading department data:", error);
  }
}

const userGrowthData = ref<
  { month: string; students: number; teachers: number }[]
>([]);
const submissionData = ref<{ month: string; submissions: number }[]>([]);

const departmentDistribution = computed(() =>
  departments.value.map((dept: any) => ({
    name: dept.name,
    value: dept.students,
    color: dept.color,
  })),
);

const pieslices = computed(() => {
  const total = departmentDistribution.value.reduce(
    (sum: number, item: any) => sum + item.value,
    0,
  );
  const radius = 120;
  const centerX = 140;
  const centerY = 140;
  let currentAngle = -Math.PI / 2;

  return departmentDistribution.value.map((item: any) => {
    const slicePercent = item.value / total;
    const sliceAngle = slicePercent * 2 * Math.PI;

    const x1 = centerX + radius * Math.cos(currentAngle);
    const y1 = centerY + radius * Math.sin(currentAngle);

    const endAngle = currentAngle + sliceAngle;
    const x2 = centerX + radius * Math.cos(endAngle);
    const y2 = centerY + radius * Math.sin(endAngle);

    const largeArc = sliceAngle > Math.PI ? 1 : 0;

    const path = `M ${centerX} ${centerY} L ${x1} ${y1} A ${radius} ${radius} 0 ${largeArc} 1 ${x2} ${y2} Z`;

    currentAngle = endAngle;

    return {
      path,
      color: item.color,
      name: item.name,
      value: item.value,
    };
  });
});

const performanceData = ref<
  { department: string; avgGrade: number; submissions: number }[]
>([]);

const recentActivity = ref<
  { type: string; message: string; timestamp: string }[]
>([]);

const formatDate = (timestamp: string) => {
  return new Date(timestamp).toLocaleDateString("vi-VN");
};

const navigateToDepartment = (_departmentId: string) => {
  router.push({ path: "/admin/users" });
};

// Build an array of the last 6 calendar months
function buildLast6Months() {
  const now = new Date();
  return Array.from({ length: 6 }, (_, i) => {
    const d = new Date(now.getFullYear(), now.getMonth() - 5 + i, 1);
    return { year: d.getFullYear(), month: d.getMonth(), label: `Tháng ${d.getMonth() + 1}` };
  });
}

async function loadChartData() {
  try {
    // 1. Fetch all users (pagination is disabled on this endpoint)
    const usersRes = await api.get("/auth/admin/users/");
    const allUsers: any[] = Array.isArray(usersRes.data)
      ? usersRes.data
      : (usersRes.data?.results ?? []);

    // 2. Get total cases count from analytics overview
    const overviewRes = await api.get("/analytics-dashboard/overview/");
    stats.value.totalSubmissions = overviewRes.data?.total_cases ?? 0;

    // 3. Get daily case creation trends for the last ~180 days (6 months)
    const trendsRes = await api.get("/analytics-dashboard/trends/", {
      params: { period: 180 },
    });
    const dailyStats: { date: string; cases_created: number }[] =
      trendsRes.data?.daily_stats ?? [];

    const months = buildLast6Months();

    // User growth per month
    userGrowthData.value = months.map((m) => ({
      month: m.label,
      students: allUsers.filter((u) => {
        const d = new Date(u.created_at);
        return u.role === "student" && d.getFullYear() === m.year && d.getMonth() === m.month;
      }).length,
      teachers: allUsers.filter((u) => {
        const d = new Date(u.created_at);
        return u.role === "instructor" && d.getFullYear() === m.year && d.getMonth() === m.month;
      }).length,
    }));

    // Case creation trend per month
    submissionData.value = months.map((m) => ({
      month: m.label,
      submissions: dailyStats
        .filter((day) => {
          const d = new Date(day.date);
          return d.getFullYear() === m.year && d.getMonth() === m.month;
        })
        .reduce((sum, day) => sum + (day.cases_created ?? 0), 0),
    }));

    // Performance data: relative case count per department (bar chart 0-100%)
    const maxCases = Math.max(1, ...departments.value.map((d) => d.activeCases));
    performanceData.value = departments.value.map((d) => ({
      department: d.vietnamese_name.replace(/^Khoa\s+/i, ""),
      avgGrade: Math.round((d.activeCases / maxCases) * 100),
      submissions: d.activeCases,
    }));

    // Recent activity: latest users + latest cases merged by timestamp
    const sortedUsers = [...allUsers]
      .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
      .slice(0, 5);

    const casesRes = await api.get("/cases/", { params: { ordering: "-created_at" } });
    const recentCases: any[] = casesRes.data?.results ?? [];

    const activities = [
      ...sortedUsers.map((u) => ({
        type: u.role === "instructor" ? "teacher_added" : "student_enrolled",
        message: `${u.full_name || u.username} đã đăng ký tài khoản (${u.role === "instructor" ? "Giảng viên" : "Sinh viên"})`,
        timestamp: u.created_at as string,
      })),
      ...recentCases.slice(0, 5).map((c: any) => ({
        type: "case_created",
        message: `Bệnh án mới '${c.title}' được tạo`,
        timestamp: c.created_at as string,
      })),
    ];
    activities.sort(
      (a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime(),
    );
    recentActivity.value = activities.slice(0, 8);
  } catch (err) {
    console.error("Error loading chart data:", err);
  }
}

// Load data on mount
onMounted(async () => {
  await loadDepartmentData();
  await loadChartData();
});
</script>
