<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <div>
      <h1 class="text-2xl font-bold text-gray-800">Quản lý Người Dùng</h1>
      <p class="text-sm text-gray-500 mt-1">Quản lý tài khoản sinh viên, giảng viên và quản trị viên</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="bg-white rounded-lg border border-gray-200 p-6 shadow-sm text-center">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-blue-500"></div>
      <p class="text-gray-600 mt-2">Đang tải dữ liệu...</p>
    </div>

    <!-- Error State -->
    <div v-if="error && !loading" class="bg-red-50 rounded-lg border border-red-200 p-4 shadow-sm">
      <p class="text-red-700 font-medium">Lỗi tải dữ liệu:</p>
      <p class="text-red-600 text-sm mt-1">{{ error }}</p>
      <button @click="loadData()" class="mt-2 px-3 py-1 text-sm bg-red-600 hover:bg-red-700 text-white rounded transition-colors">
        Thử lại
      </button>
    </div>

    <!-- Search and Filter -->
    <div v-if="!loading" class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-xs font-medium text-gray-700 mb-2">Tìm kiếm</label>
          <input 
            v-model="q" 
            placeholder="Tên hoặc email..." 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
          />
        </div>
        <div> 
          <label class="block text-xs font-medium text-gray-700 mb-2">Vai trò</label>
          <select v-model="role" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm">
            <option value="">Tất cả vai trò</option>
            <option value="student">Sinh viên</option>
            <option value="instructor">Giảng viên</option>
            <option value="admin">Quản trị</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-700 mb-2">Khoa</label>
          <select v-model="departmentFilter" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm">
            <option value="">Tất cả khoa</option>
            <option v-for="d in departments" :key="d.id" :value="String(d.id)">{{ d.vietnamese_name }}</option>
          </select>
        </div>
        <div class="flex items-end">
          <button 
            @click="resetFilters" 
            class="w-full px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-md text-sm font-medium transition-colors"
          >
            Xóa bộ lọc
          </button>
        </div>
      </div>
    </div>

    <!-- Users Table Card -->
    <div v-if="!loading" class="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
      <div class="p-4 border-b border-gray-200">
        <h3 class="font-semibold text-gray-800">Danh sách người dùng ({{ filtered.length }} trên trang hiện tại)</h3>
      </div>

      <div class="overflow-x-auto">
        <table class="min-w-full text-sm">
          <thead>
            <tr class="bg-gray-50 border-b border-gray-200">
              <th class="px-6 py-3 text-left font-medium text-gray-700">Tên</th>
              <th class="px-6 py-3 text-left font-medium text-gray-700">Email</th>
              <th class="px-6 py-3 text-left font-medium text-gray-700">Vai trò</th>
              <th class="px-6 py-3 text-left font-medium text-gray-700">Khoa</th>
              <th class="px-6 py-3 text-left font-medium text-gray-700">Trạng thái</th>
              <th class="px-6 py-3 text-left font-medium text-gray-700">Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in filtered" :key="user.id" class="border-b border-gray-200 hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4 font-medium text-gray-800">{{ user.full_name || `${user.first_name} ${user.last_name}` || user.username }}</td>
              <td class="px-6 py-4 text-gray-600">{{ user.email }}</td>
              <td class="px-6 py-4">
                <span 
                  class="inline-flex px-2 py-1 text-xs font-medium rounded-full"
                  :class="user.role === 'student' ? 'bg-blue-100 text-blue-800' : user.role === 'instructor' ? 'bg-green-100 text-green-800' : 'bg-purple-100 text-purple-800'"
                >
                  {{ roleLabel(user.role) }}
                </span>
              </td>
              <td class="px-6 py-4 text-gray-600">{{ user.department_vietnamese_name || user.department_name || '—' }}</td>
              <td class="px-6 py-4">
                <span 
                  class="inline-flex px-2 py-1 text-xs font-medium rounded-full"
                  :class="user.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
                >
                  {{ user.is_active ? 'Hoạt động' : 'Vô hiệu' }}
                </span>
              </td>
              <td class="px-6 py-4">
                <div class="flex gap-2">
                  <button 
                    @click="edit(user)" 
                    class="px-3 py-1 text-xs bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors"
                  >
                    Sửa
                  </button>
                  <button 
                    @click="toggleActive(user)" 
                    class="px-3 py-1 text-xs bg-gray-600 hover:bg-gray-700 text-white rounded transition-colors"
                  >
                    {{ user.is_active ? 'Vô hiệu' : 'Kích hoạt' }}
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="filtered.length === 0">
              <td class="px-6 py-8 text-center text-gray-500 text-sm" colspan="6">Không có người dùng phù hợp</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="!loading && count > 0" class="mt-4 flex items-center justify-between bg-white p-4 rounded-b border-t border-gray-100">
      <div class="text-sm text-gray-600">
        Hiển thị <strong>{{ startIndex }}</strong> - <strong>{{ endIndex }}</strong> / <strong>{{ count }}</strong>
      </div>
      <div class="flex items-center space-x-2">
        <button @click="gotoPage(page - 1)" :disabled="!previous" class="px-3 py-1 rounded-md bg-gray-100 hover:bg-gray-200 disabled:opacity-50">Trước</button>

        <template v-for="p in pagesToShow" :key="p">
          <button
            v-if="p === '...'"
            disabled
            class="px-3 py-1 text-sm"
          >...
          </button>
          <button
            v-else
            @click="gotoPage(p)"
            :class="['px-3 py-1 rounded-md text-sm', p === page ? 'bg-blue-600 text-white' : 'bg-gray-100 hover:bg-gray-200']"
          >{{ p }}</button>
        </template>

        <button @click="gotoPage(page + 1)" :disabled="!next" class="px-3 py-1 rounded-md bg-gray-100 hover:bg-gray-200 disabled:opacity-50">Tiếp</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { requireRoles } from '@/composables/useAuthorize';
import api from '@/services/api';

// Component-level admin guard
requireRoles(['admin']);

const route = useRoute();
const router = useRouter();

// Live data
const departments = ref<Array<{ id: number; vietnamese_name: string }>>([]);
const users = ref<Array<any>>([]);
const loading = ref(false);
const error = ref<string | null>(null);

// Pagination state
const count = ref(0);
const next = ref<string | null>(null);
const previous = ref<string | null>(null);
const page = ref<number>(Number(route.query.page) || 1);
const pageSize = ref<number>(20);

// Search inputs
const q = ref(''); // bound to input
const debouncedQuery = ref(''); // updates after debounce
const role = ref('');
const departmentFilter = ref(route.query.department ? String(route.query.department) : '');

// Debounce input (250ms)
let debounceTimer: ReturnType<typeof setTimeout> | null = null;
watch(q, (val) => {
  if (debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    debouncedQuery.value = val;
  }, 250);
});

// If route query changes (e.g., clicking a department card), sync it and reload page 1
watch(
  () => route.query.department,
  (d) => {
    departmentFilter.value = d ? String(d) : '';
    page.value = 1;
    loadData(1);
  }
);

// Keep route.page in sync (so back/forward works)
watch(
  () => route.query.page,
  (p) => {
    page.value = p ? Number(p) : 1;
    loadData(page.value);
  }
);

// When role filter changes, reset to page 1 and reload
watch(role, () => {
  page.value = 1;
  loadData(1);
});

// Normalize helper: remove diacritics and lowercase
function normalize(s = ''): string {
  return s
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase();
}

// Tokenize and match all tokens against combined haystack
const filtered = computed(() => {
  const term = normalize(debouncedQuery.value || '');
  const tokens = term.split(/\s+/).filter(Boolean);
  
  // If no search query, return all current page users as-is (filtering is server-side now)
  if (!tokens.length) return users.value;

  // Otherwise, client-side search within current page results
  return users.value.filter((u) => {
    const fullName = u.full_name || `${u.first_name} ${u.last_name}`.trim() || u.username || '';
    const hay = normalize(`${fullName} ${u.email} ${u.department_name || ''} ${u.role}`);
    return tokens.every((tok) => hay.includes(tok));
  });
});

// Load users and departments from backend
async function loadData(requestedPage: number = page.value) {
  loading.value = true;
  error.value = null;
  try {
    // Build params for users endpoint
    const params: Record<string, any> = { page: requestedPage };
    if (role.value) params.role = role.value;
    if (departmentFilter.value) params.department = departmentFilter.value;

    const [usersRes, deptsRes] = await Promise.all([
      api.get('/auth/users/', { params }),
      api.get('/cases/departments/')
    ]);

    // Handle paginated response (DRF default pagination wraps results)
    const usersData = usersRes.data;
    console.log('Loaded users:', usersData);
    const results = usersData.results ? usersData.results : (Array.isArray(usersData) ? usersData : []);
    users.value = results;
    count.value = typeof usersData.count === 'number' ? usersData.count : results.length;
    next.value = usersData.next ?? null;
    previous.value = usersData.previous ?? null;
    pageSize.value = results.length || pageSize.value;
    page.value = requestedPage;

    // sync route query param for page
    router.replace({ query: { ...route.query, page: String(page.value) } }).catch(() => {});

    // Handle departments (should be array or paginated)
    const deptsData = deptsRes.data;
    const deptsList = deptsData.results ? deptsData.results : (Array.isArray(deptsData) ? deptsData : []);
    departments.value = deptsList.map((d: any) => ({ id: d.id, name: d.name, vietnamese_name: d.vietnamese_name }));
    console.log('Loaded departments:', departments.value);
  } catch (err: any) {
    console.error('Error loading users/departments', err);
    error.value = err.response?.data?.detail || err.message || 'Failed to load data';
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  loadData(page.value);
});

function roleLabel(roleValue: string): string {
  const labels: Record<string, string> = {
    student: 'Sinh viên',
    instructor: 'Giảng viên',
    admin: 'Quản trị'
  };
  return labels[roleValue] || roleValue;
}

function resetFilters() {
  q.value = '';
  debouncedQuery.value = '';
  role.value = '';
  departmentFilter.value = '';
  page.value = 1;
  router.replace({ query: {} });
  loadData(1);
}

function edit(user: any) {
  alert(`Edit user ${user.full_name || user.username}`);
}

function toggleActive(user: any) {
  user.is_active = !user.is_active;
}

// Pagination helpers
const totalPages = computed(() => {
  return Math.max(1, Math.ceil(count.value / (pageSize.value || 1)));
});

const startIndex = computed(() => (count.value === 0 ? 0 : (page.value - 1) * pageSize.value + 1));
const endIndex = computed(() => Math.min(count.value, (page.value - 1) * pageSize.value + users.value.length));

function gotoPage(p: number) {
  if (p < 1 || p > totalPages.value) return;
  loadData(p);
}

function buildPagesArray(): Array<number | '...'> {
  const total = totalPages.value;
  const current = page.value;
  const pages: Array<number | '...'> = [];
  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i);
    return pages;
  }
  // show first, maybe ellipsis, some around current, ellipsis, last
  pages.push(1);
  if (current > 4) pages.push('...');
  const start = Math.max(2, current - 2);
  const end = Math.min(total - 1, current + 2);
  for (let i = start; i <= end; i++) pages.push(i);
  if (current + 2 < total - 1) pages.push('...');
  pages.push(total);
  return pages;
}

const pagesToShow = computed(() => buildPagesArray());
</script>

<style scoped>
.input { border: 1px solid #e5e7eb; }
.btn { background: #1e40af; color: #fff; padding: 6px 10px; border-radius: 6px; }
.btn-sm { padding: 4px 8px; font-size: 12px }
</style>
