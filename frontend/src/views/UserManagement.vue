<template>
  <div class="user-management-page p-6 space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">Quản lý Người Dùng</h1>
        <p class="text-sm text-gray-500 mt-1">
          Tạo và quản lý tài khoản sinh viên, giảng viên, quản trị viên
        </p>
      </div>
      <Button
        @click="openCreateModal"
        icon="pi pi-plus"
        label="Tạo người dùng mới"
      />
    </div>

    <!-- Loading State -->
    <div
      v-if="loading"
      class="bg-white rounded-lg border border-gray-200 p-6 shadow-sm text-center"
    >
      <ProgressSpinner style="width: 50px; height: 50px" strokeWidth="4" />
      <p class="text-gray-600 mt-2">Đang tải dữ liệu...</p>
    </div>

    <!-- Error State -->
    <div
      v-if="error && !loading"
      class="bg-red-50 rounded-lg border border-red-200 p-4 shadow-sm"
    >
      <p class="text-red-700 font-medium">Lỗi:</p>
      <p class="text-red-600 text-sm mt-1">{{ error }}</p>
      <Button @click="loadUsers()" label="Thử lại" size="small" class="mt-2" />
    </div>

    <!-- Search and Filter -->
    <div
      v-if="!loading"
      class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm"
    >
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-xs font-medium text-gray-700 mb-2"
            >Tìm kiếm</label
          >
          <IconField>
            <InputIcon class="pi pi-search" />
            <InputText v-model="searchQuery" placeholder="Tên, email, ID..." />
          </IconField>
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-700 mb-2"
            >Vai trò</label
          >
          <Select
            v-model="roleFilter"
            :options="roleFilterOptions"
            placeholder="Tất cả vai trò"
            optionLabel="label"
            optionValue="value"
          />
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-700 mb-2"
            >Trạng thái</label
          >
          <Select
            v-model="statusFilter"
            :options="statusFilterOptions"
            placeholder="Tất cả"
            optionLabel="label"
            optionValue="value"
          />
        </div>
        <div class="flex items-end">
          <Button @click="resetFilters" label="Xóa bộ lọc" class="w-full" />
        </div>
      </div>
    </div>

    <!-- Users Table -->
    <div
      v-if="!loading"
      class="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden"
    >
      <div class="p-4 border-b border-gray-200">
        <h3 class="font-semibold text-gray-800">
          Danh sách người dùng ({{ filteredUsers.length
          }}<span v-if="filteredUsers.length !== users.length">
            / {{ users.length }}</span
          >)
        </h3>
      </div>

      <div class="overflow-x-auto">
        <table class="min-w-full text-sm">
          <thead>
            <tr class="bg-gray-50 border-b border-gray-200">
              <th class="px-6 py-3 text-left font-medium text-gray-700">Tên</th>
              <th class="px-6 py-3 text-left font-medium text-gray-700">
                Email
              </th>
              <th class="px-6 py-3 text-left font-medium text-gray-700">
                Vai trò
              </th>
              <th class="px-6 py-3 text-left font-medium text-gray-700">
                Khoa
              </th>
              <th class="px-6 py-3 text-left font-medium text-gray-700">
                Trạng thái
              </th>
              <th class="px-6 py-3 text-left font-medium text-gray-700">
                Hành động
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="user in filteredUsers"
              :key="user.id"
              class="border-b border-gray-100 hover:bg-gray-50"
            >
              <td class="px-6 py-4">
                <div class="font-medium text-gray-900">
                  {{ user.full_name || `${user.first_name} ${user.last_name}` }}
                </div>
                <div class="text-xs text-gray-500">{{ user.username }}</div>
              </td>
              <td class="px-6 py-4 text-gray-600">{{ user.email }}</td>
              <td class="px-6 py-4">
                <span
                  :class="getRoleBadgeClass(user.role)"
                  class="px-2 py-1 rounded-full text-xs font-medium"
                >
                  {{ getRoleLabel(user.role) }}
                </span>
              </td>
              <td class="px-6 py-4 text-gray-600">
                {{ user.department_vietnamese_name || "Chưa có" }}
              </td>
              <td class="px-6 py-4">
                <span
                  :class="
                    user.is_active
                      ? 'bg-green-100 text-green-800'
                      : 'bg-red-100 text-red-800'
                  "
                  class="px-2 py-1 rounded-full text-xs font-medium"
                >
                  {{ user.is_active ? "Hoạt động" : "Không hoạt động" }}
                </span>
              </td>
              <td class="px-6 py-4">
                <div class="flex gap-2">
                  <Button
                    @click="openEditModal(user)"
                    icon="pi pi-pencil"
                    text
                    severity="info"
                    rounded
                    title="Chỉnh sửa"
                  />
                  <Button
                    @click="toggleUserStatus(user)"
                    :icon="
                      user.is_active ? 'pi pi-eye-slash' : 'pi pi-check-circle'
                    "
                    text
                    :severity="user.is_active ? 'warning' : 'success'"
                    rounded
                    :title="user.is_active ? 'Vô hiệu hóa' : 'Kích hoạt'"
                  />
                  <Button
                    @click="confirmDelete(user)"
                    icon="pi pi-trash"
                    text
                    severity="danger"
                    rounded
                    title="Xóa"
                  />
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div
        class="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto"
      >
        <div class="p-6 border-b border-gray-200">
          <h2 class="text-xl font-bold text-gray-800">
            {{ isEditing ? "Chỉnh sửa người dùng" : "Tạo người dùng mới" }}
          </h2>
        </div>

        <form @submit.prevent="submitUser" class="p-6 space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1"
                >Họ <span class="text-red-500">*</span></label
              >
              <input
                v-model="formData.first_name"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1"
                >Tên <span class="text-red-500">*</span></label
              >
              <input
                v-model="formData.last_name"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Username <span class="text-red-500">*</span></label
            >
            <input
              v-model="formData.username"
              required
              :disabled="isEditing"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Email <span class="text-red-500">*</span></label
            >
            <input
              v-model="formData.email"
              type="email"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Mật khẩu {{ isEditing ? "(để trống nếu không đổi)" : "" }}
              <span v-if="!isEditing" class="text-red-500">*</span>
            </label>
            <input
              v-model="formData.password"
              type="password"
              :required="!isEditing"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1"
                >Vai trò <span class="text-red-500">*</span></label
              >
              <select
                v-model="formData.role"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">-- Chọn vai trò --</option>
                <option value="student">Sinh viên</option>
                <option value="instructor">Giảng viên</option>
                <option value="admin">Quản trị viên</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1"
                >Khoa</label
              >
              <select
                v-model="formData.department"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option :value="null">-- Chưa chọn --</option>
                <option
                  v-for="dept in departments"
                  :key="dept?.id || 'empty'"
                  :value="dept?.id"
                >
                  {{ dept?.vietnamese_name || dept?.name }}
                </option>
              </select>
            </div>
          </div>

          <div v-if="formData.role === 'student'">
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Mã sinh viên</label
            >
            <input
              v-model="formData.student_id"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div
            v-if="formData.role === 'instructor' || formData.role === 'admin'"
          >
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Mã nhân viên</label
            >
            <input
              v-model="formData.employee_id"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div class="flex items-center gap-2">
            <input
              v-model="formData.is_active"
              type="checkbox"
              id="is_active"
              class="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
            />
            <label for="is_active" class="text-sm font-medium text-gray-700"
              >Tài khoản hoạt động</label
            >
          </div>

          <div class="flex items-center gap-2">
            <input
              v-model="formData.is_staff"
              type="checkbox"
              id="is_staff"
              class="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
            />
            <label for="is_staff" class="text-sm font-medium text-gray-700"
              >Quyền truy cập Django Admin</label
            >
          </div>

          <div class="flex justify-end gap-3 pt-4 border-t border-gray-200">
            <Button type="button" @click="closeModal" label="Hủy" outlined />
            <Button
              type="submit"
              :label="
                submitting ? 'Đang lưu...' : isEditing ? 'Cập nhật' : 'Tạo mới'
              "
              :disabled="submitting"
            />
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div
      v-if="showDeleteConfirm"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white rounded-lg shadow-xl w-full max-w-md p-6">
        <h3 class="text-lg font-bold text-gray-800 mb-2">Xác nhận xóa</h3>
        <p class="text-gray-600 mb-4">
          Bạn có chắc muốn xóa người dùng
          <strong>{{ userToDelete?.full_name }}</strong
          >?
        </p>
        <div class="flex justify-end gap-3">
          <Button @click="showDeleteConfirm = false" label="Hủy" outlined />
          <Button @click="deleteUser" label="Xóa" severity="danger" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import api from "@/services/api";
import Button from "primevue/button";
import ProgressSpinner from "primevue/progressspinner";
import InputText from "primevue/inputtext";
import Select from "primevue/select";
import IconField from "primevue/iconfield";
import InputIcon from "primevue/inputicon";

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  role: string;
  department: number | null;
  department_name: string;
  department_vietnamese_name: string;
  student_id?: string;
  employee_id?: string;
  is_active: boolean;
  is_staff: boolean;
  created_at: string;
}

interface Department {
  id: number;
  name: string;
  vietnamese_name: string;
}

const users = ref<User[]>([]);
const departments = ref<Department[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
const searchQuery = ref("");
const roleFilter = ref("");
const statusFilter = ref("");
const showModal = ref(false);
const showDeleteConfirm = ref(false);
const isEditing = ref(false);
const submitting = ref(false);
const userToDelete = ref<User | null>(null);

const formData = ref({
  id: null as number | null,
  username: "",
  email: "",
  password: "",
  first_name: "",
  last_name: "",
  role: "",
  department: null as number | null,
  student_id: "",
  employee_id: "",
  is_active: true,
  is_staff: false,
});

const roleFilterOptions = computed(() => [
  { label: "Tất cả vai trò", value: "" },
  { label: "Sinh viên", value: "student" },
  { label: "Giảng viên", value: "instructor" },
  { label: "Quản trị", value: "admin" },
]);

const statusFilterOptions = computed(() => [
  { label: "Tất cả", value: "" },
  { label: "Hoạt động", value: "active" },
  { label: "Không hoạt động", value: "inactive" },
]);

const filteredUsers = computed(() => {
  // Filter out null/undefined users first
  let filtered = users.value.filter((u) => u && u.id);

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(
      (u) =>
        u.username?.toLowerCase().includes(query) ||
        u.email?.toLowerCase().includes(query) ||
        u.first_name?.toLowerCase().includes(query) ||
        u.last_name?.toLowerCase().includes(query) ||
        (u.student_id && u.student_id.toLowerCase().includes(query)) ||
        (u.employee_id && u.employee_id.toLowerCase().includes(query)),
    );
  }

  if (roleFilter.value) {
    filtered = filtered.filter((u) => u.role === roleFilter.value);
  }

  if (statusFilter.value) {
    filtered = filtered.filter((u) =>
      statusFilter.value === "active" ? u.is_active : !u.is_active,
    );
  }

  return filtered;
});

const loadUsers = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await api.get("/auth/admin/users/");
    // Handle paginated or direct array response, and filter out null users
    const data = response.data?.results || response.data || [];
    users.value = Array.isArray(data) ? data.filter((u: any) => u && u.id) : [];
  } catch (err: any) {
    error.value = err.response?.data?.detail || "Failed to load users";
    users.value = [];
  } finally {
    loading.value = false;
  }
};

const loadDepartments = async () => {
  try {
    const response = await api.get("/cases/departments/");
    // Handle both paginated and non-paginated responses
    const data = response.data?.results || response.data || [];
    // Filter out any null/undefined departments
    departments.value = Array.isArray(data)
      ? data.filter((dept: any) => dept && dept.id)
      : [];
  } catch (err) {
    departments.value = [];
  }
};

const openCreateModal = () => {
  isEditing.value = false;
  formData.value = {
    id: null,
    username: "",
    email: "",
    password: "",
    first_name: "",
    last_name: "",
    role: "",
    department: null,
    student_id: "",
    employee_id: "",
    is_active: true,
    is_staff: false,
  };
  showModal.value = true;
};

const openEditModal = (user: User) => {
  isEditing.value = true;
  formData.value = {
    id: user.id,
    username: user.username,
    email: user.email,
    password: "",
    first_name: user.first_name,
    last_name: user.last_name,
    role: user.role,
    department: user.department,
    student_id: user.student_id || "",
    employee_id: user.employee_id || "",
    is_active: user.is_active,
    is_staff: user.is_staff,
  };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const submitUser = async () => {
  submitting.value = true;
  error.value = null;

  try {
    const payload: any = {
      username: formData.value.username,
      email: formData.value.email,
      first_name: formData.value.first_name,
      last_name: formData.value.last_name,
      role: formData.value.role,
      department: formData.value.department,
      is_active: formData.value.is_active,
      is_staff: formData.value.is_staff,
    };

    if (formData.value.password) {
      payload.password = formData.value.password;
    }

    if (formData.value.role === "student" && formData.value.student_id) {
      payload.student_id = formData.value.student_id;
    }

    if (
      (formData.value.role === "instructor" ||
        formData.value.role === "admin") &&
      formData.value.employee_id
    ) {
      payload.employee_id = formData.value.employee_id;
    }

    if (isEditing.value && formData.value.id) {
      await api.put(`/auth/admin/users/${formData.value.id}/`, payload);
    } else {
      await api.post("/auth/admin/users/", payload);
    }

    closeModal();
    await loadUsers();
  } catch (err: any) {
    error.value =
      err.response?.data?.detail ||
      err.response?.data?.error ||
      "Failed to save user";
    alert(error.value);
  } finally {
    submitting.value = false;
  }
};

const toggleUserStatus = async (user: User) => {
  try {
    const action = user.is_active ? "deactivate" : "activate";
    await api.post(`/auth/admin/users/${user.id}/${action}/`);
    await loadUsers();
  } catch (err: any) {
    alert(err.response?.data?.detail || "Failed to update user status");
  }
};

const confirmDelete = (user: User) => {
  userToDelete.value = user;
  showDeleteConfirm.value = true;
};

const deleteUser = async () => {
  if (!userToDelete.value) return;

  try {
    await api.delete(`/auth/admin/users/${userToDelete.value.id}/`);
    showDeleteConfirm.value = false;
    userToDelete.value = null;
    await loadUsers();
  } catch (err: any) {
    alert(err.response?.data?.detail || "Failed to delete user");
  }
};

const resetFilters = () => {
  searchQuery.value = "";
  roleFilter.value = "";
  statusFilter.value = "";
};

const getRoleLabel = (role: string) => {
  const labels: Record<string, string> = {
    student: "Sinh viên",
    instructor: "Giảng viên",
    admin: "Quản trị viên",
  };
  return labels[role] || role;
};

const getRoleBadgeClass = (role: string) => {
  const classes: Record<string, string> = {
    student: "bg-blue-100 text-blue-800",
    instructor: "bg-purple-100 text-purple-800",
    admin: "bg-red-100 text-red-800",
  };
  return classes[role] || "bg-gray-100 text-gray-800";
};

onMounted(() => {
  loadUsers();
  loadDepartments();
});
</script>

<style scoped>
/* User Management Page - CSS Variable Overrides */
.p-6 {
  background: var(--background);
}

/* Headers */
h1,
h2,
h3,
h4 {
  color: var(--foreground);
}

/* Text colors */
:deep(.text-gray-800) {
  color: var(--foreground) !important;
}

:deep(.text-gray-700) {
  color: var(--foreground) !important;
}

:deep(.text-gray-600) {
  color: var(--muted-foreground) !important;
}

:deep(.text-gray-500) {
  color: var(--muted-foreground) !important;
}

/* Card backgrounds */
:deep(.bg-white) {
  background: var(--card) !important;
}

:deep(.bg-gray-50) {
  background: var(--secondary) !important;
}

:deep(.bg-gray-100) {
  background: var(--secondary) !important;
}

/* Border colors */
:deep(.border-gray-200) {
  border-color: var(--border) !important;
}

:deep(.border-gray-300) {
  border-color: var(--border) !important;
}

/* Primary buttons */
:deep(.bg-blue-600) {
  background: var(--primary) !important;
}

:deep(.bg-blue-700) {
  background: var(--primary-hover) !important;
}

:deep(.hover\:bg-blue-700:hover) {
  background: var(--primary-hover) !important;
}

/* Focus rings */
:deep(.focus\:ring-blue-500:focus) {
  --tw-ring-color: var(--primary) !important;
}

/* Role badges */
:deep(.bg-blue-100) {
  background: var(--accent) !important;
}

:deep(.text-blue-800) {
  color: var(--primary) !important;
}

:deep(.bg-purple-100) {
  background: rgba(139, 92, 246, 0.15) !important;
}

:deep(.text-purple-800) {
  color: rgb(109, 40, 217) !important;
}

/* Success (green) - semantic */
:deep(.bg-green-100) {
  background: rgba(16, 185, 129, 0.15) !important;
}

:deep(.text-green-800) {
  color: rgb(6, 95, 70) !important;
}

/* Destructive (red) - semantic */
:deep(.bg-red-50) {
  background: rgba(220, 38, 38, 0.1) !important;
}

:deep(.bg-red-100) {
  background: rgba(220, 38, 38, 0.15) !important;
}

:deep(.border-red-200) {
  border-color: rgba(220, 38, 38, 0.3) !important;
}

:deep(.text-red-700),
:deep(.text-red-800) {
  color: var(--destructive) !important;
}

:deep(.bg-red-600) {
  background: var(--destructive) !important;
}

:deep(.hover\:bg-red-700:hover) {
  background: rgba(185, 28, 28, 1) !important;
}

/* Gray accent for buttons */
:deep(.bg-gray-600) {
  background: var(--muted-foreground) !important;
}

:deep(.hover\:bg-gray-700:hover) {
  background: var(--foreground) !important;
}

/* Hover states */
:deep(.hover\:bg-gray-50:hover) {
  background: var(--secondary) !important;
}

:deep(.hover\:bg-gray-100:hover) {
  background: var(--secondary) !important;
}

/* Input styling */
:deep(input:focus),
:deep(select:focus) {
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 3px var(--shadow-blue-hover) !important;
}

/* Modal overlay */
:deep(.bg-black) {
  background: rgba(0, 0, 0, 0.5) !important;
}
</style>
