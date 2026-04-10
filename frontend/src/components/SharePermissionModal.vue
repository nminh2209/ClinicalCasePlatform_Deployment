<template>
  <Dialog
    :visible="open"
    @update:visible="$emit('update:open', false)"
    modal
    header="Cấp quyền truy cập"
    :style="{ width: '28rem', maxWidth: '95vw' }"
  >
    <template #header>
      <div>
        <div class="font-bold text-xl text-gray-900">Cấp quyền truy cập</div>
        <p class="text-gray-500 text-sm mt-0.5">
          Chia sẻ ca bệnh này với người dùng hoặc nhóm
        </p>
      </div>
    </template>

    <div class="flex flex-col gap-4 pt-1">
      <div class="flex flex-col gap-1">
        <label class="text-sm font-medium text-gray-700">Loại chia sẻ</label>
        <Select
          v-model="form.shareType"
          fluid
          :options="shareTypeOptions"
          optionLabel="label"
          optionValue="value"
        />
      </div>

      <div v-if="form.shareType === 'individual'" class="flex flex-col gap-1">
        <label class="text-sm font-medium text-gray-700">Người dùng</label>
        <AutoComplete
          v-model="form.searchQuery"
          :suggestions="searchResults"
          optionLabel="full_name"
          fluid
          placeholder="Tìm kiếm người dùng (giảng viên hoặc sinh viên)..."
          :delay="300"
          :min-length="2"
          @complete="searchUsers"
          @item-select="onUserSelect"
          @clear="clearSelectedUser"
        >
          <template #option="{ option }">
            <div class="flex flex-col py-1">
              <span class="font-medium text-gray-900">{{
                option.full_name
              }}</span>
              <span class="text-sm text-gray-500">{{ option.email }}</span>
              <span class="text-xs text-gray-400">{{ option.department }}</span>
            </div>
          </template>
          <template #empty>
            <span class="text-gray-500 text-sm"
              >Không tìm thấy người dùng nào.</span
            >
          </template>
        </AutoComplete>

        <div
          v-if="form.selectedUser"
          class="flex items-center justify-between bg-blue-50 rounded-md px-3 py-2 mt-1"
        >
          <span class="text-sm">
            <span class="font-medium">Đã chọn: </span>
            {{ form.selectedUser.full_name }} ({{ form.selectedUser.email }})
          </span>
          <Button
            icon="pi pi-times"
            text
            rounded
            severity="danger"
            size="small"
            @click="clearSelectedUser"
          />
        </div>
      </div>

      <div v-if="form.shareType === 'department'" class="flex flex-col gap-1">
        <label class="text-sm font-medium text-gray-700"
          >Chia sẻ với khoa</label
        >
        <div class="p-3 bg-blue-50 rounded-md border border-blue-200">
          <div class="flex items-center gap-2">
            <i class="pi pi-building text-blue-500" />
            <div>
              <div class="font-medium text-blue-800">
                {{
                  userDepartment?.vietnamese_name ||
                  userDepartment?.name ||
                  "Unknown Department"
                }}
              </div>
              <div class="text-sm text-blue-600">
                Tất cả sinh viên trong khoa này sẽ có thể xem ca bệnh
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="flex flex-col gap-1">
        <label class="text-sm font-medium text-gray-700">Loại quyền</label>
        <Select
          v-model="form.permissionType"
          :options="permissionOptions"
          optionLabel="label"
          optionValue="value"
          class="w-full"
        />
      </div>

      <div class="flex flex-col gap-1">
        <label class="text-sm font-medium text-gray-700"
          >Ngày hết hạn (tuỳ chọn)</label
        >
        <DatePicker
          v-model="form.expiresAt"
          showTime
          hourFormat="24"
          fluid
          :minDate="new Date()"
          placeholder="Chọn ngày hết hạn..."
          showButtonBar
        />
      </div>

      <div class="flex flex-col gap-1">
        <label class="text-sm font-medium text-gray-700"
          >Tin nhắn (tuỳ chọn)</label
        >
        <Textarea
          v-model="form.message"
          fluid
          placeholder="Thêm tin nhắn cho người nhận..."
          rows="3"
        />
      </div>

      <div
        v-if="conflictMessage"
        class="flex items-start gap-2 p-3 bg-amber-50 border border-amber-200 rounded-md"
      >
        <i class="pi pi-exclamation-triangle text-amber-600 mt-0.5" />
        <div class="text-sm text-amber-800">
          {{ conflictMessage }}
        </div>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-end gap-2 w-full">
        <Button
          label="Huỷ"
          icon="pi pi-times"
          outlined
          severity="secondary"
          @click="$emit('update:open', false)"
        />
        <Button
          label="Cấp quyền"
          icon="pi pi-check"
          :disabled="!canSubmit || loading"
          :loading="loading"
          @click="handleSubmit"
        />
      </div>
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from "vue";
import { useToast } from "@/composables/useToast";
import { sharingService } from "@/services/sharing";
import api from "@/services/api";
import type {
  SharePermission,
  CreatePermissionRequest,
} from "@/services/sharing";
import Dialog from "primevue/dialog";
import Button from "primevue/button";
import Select from "primevue/select";
import InputText from "primevue/inputtext";
import AutoComplete from "primevue/autocomplete";
import Textarea from "primevue/textarea";
import DatePicker from "primevue/datepicker";

const shareTypeOptions = [
  { label: "Chia sẻ cá nhân", value: "individual" },
  { label: "Chia sẻ khoa", value: "department" },
  { label: "Công khai", value: "public" },
];

const permissionOptions = [
  { label: "Chỉ xem", value: "view" },
  { label: "Xem và bình luận", value: "comment" },
  { label: "Xem, bình luận và phân tích", value: "analyze" },
  { label: "Toàn quyền chỉnh sửa", value: "edit" },
];

type ShareType = "individual" | "department" | "public";
type PermissionType = "view" | "comment" | "analyze" | "edit";

interface Props {
  open: boolean;
  caseId: number;
  shareType?: ShareType;
}

interface User {
  id: number;
  full_name: string;
  email: string;
  department: string;
}

interface Department {
  id: number;
  name: string;
  vietnamese_name?: string;
}

interface Emits {
  (event: "update:open", value: boolean): void;
  (event: "permission-created", permission: SharePermission): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const toast = useToast();

const loading = ref(false);
const searchResults = ref<User[]>([]);
const departments = ref<Department[]>([]);
const userDepartment = ref<Department | null>(null);
const existingPermissions = ref<any[]>([]);

const form = ref({
  shareType: "individual" as ShareType,
  permissionType: "view" as PermissionType,
  searchQuery: "" as string | User,
  selectedUser: null as User | null,
  departmentId: "",
  expiresAt: null as Date | null,
  message: "",
});

const getPermissionData = (): CreatePermissionRequest => {
  const data: CreatePermissionRequest = {
    share_type: form.value.shareType,
    permission_type: form.value.permissionType,
  };

  if (form.value.expiresAt) {
    data.expires_at = (form.value.expiresAt as Date).toISOString();
  }
  if (form.value.message) {
    data.notes = form.value.message;
  }
  if (form.value.shareType === "individual" && form.value.selectedUser) {
    data.user = form.value.selectedUser.id;
  } else if (form.value.shareType === "department" && userDepartment.value) {
    data.target_department = userDepartment.value.id;
  }

  return data;
};

const isPermissionActive = (p: any): boolean => {
  if (!p || p.is_active === false) return false;
  if (p.is_expired === true) return false;
  if (p.expires_at) {
    const expires = new Date(p.expires_at).getTime();
    if (!Number.isNaN(expires) && expires <= Date.now()) return false;
  }
  return true;
};

const conflictMessage = computed<string | null>(() => {
  const active = existingPermissions.value.filter(isPermissionActive);
  if (form.value.shareType === "public") {
    if (active.some((p) => p.share_type === "public")) {
      return "Ca bệnh này đã được chia sẻ công khai. Hãy thu hồi quyền hiện tại trước khi chia sẻ lại.";
    }
  } else if (form.value.shareType === "department") {
    const deptId = userDepartment.value?.id;
    if (deptId == null) return null;
    if (
      active.some(
        (p) => p.share_type === "department" && p.target_department === deptId,
      )
    ) {
      const deptName =
        userDepartment.value?.vietnamese_name || userDepartment.value?.name;
      return `Ca bệnh này đã được chia sẻ với khoa ${deptName}. Hãy thu hồi quyền hiện tại trước khi chia sẻ lại.`;
    }
  } else if (form.value.shareType === "individual") {
    const userId = form.value.selectedUser?.id;
    if (userId == null) return null;
    if (
      active.some((p) => p.share_type === "individual" && p.user === userId)
    ) {
      return `Ca bệnh này đã được chia sẻ với ${form.value.selectedUser?.full_name}. Hãy thu hồi quyền hiện tại trước khi chia sẻ lại.`;
    }
  }
  return null;
});

const canSubmit = computed(() => {
  if (conflictMessage.value) return false;
  if (form.value.shareType === "individual")
    return !!form.value.selectedUser && !!form.value.permissionType;
  if (form.value.shareType === "department")
    return !!userDepartment.value && !!form.value.permissionType;
  if (form.value.shareType === "public") return !!form.value.permissionType;
  return false;
});

watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) {
      form.value.shareType = props.shareType || "individual";
      loadDepartments();
      loadUserDepartment();
      loadExistingPermissions();
    } else {
      resetForm();
    }
  },
);

watch(
  () => form.value.shareType,
  (newType) => {
    if (newType !== "individual") clearSelectedUser();
    if (newType !== "department") form.value.departmentId = "";
  },
);

const resetForm = () => {
  form.value = {
    shareType: "individual",
    searchQuery: "",
    selectedUser: null,
    departmentId: "",
    permissionType: "view",
    expiresAt: null,
    message: "",
  };
  searchResults.value = [];
  existingPermissions.value = [];
};

const loadExistingPermissions = async () => {
  try {
    const data = await sharingService.getCasePermissions(props.caseId);
    const list = Array.isArray(data) ? data : (data?.results ?? []);
    existingPermissions.value = list;
  } catch {
    existingPermissions.value = [];
  }
};

const loadDepartments = async () => {
  if (departments.value.length > 0) return;
  try {
    const list = await sharingService.getDepartments({
      ordering: "name",
      page_size: 100,
    });
    departments.value = list;
  } catch (error) {
    departments.value = [];
    toast.toast.error("Không thể tải danh sách khoa");
  }
};

onMounted(() => {
  loadDepartments();
});

const loadUserDepartment = async () => {
  try {
    const response = await api.get("/auth/profile/");
    const user = response.data;

    if (user.department) {
      if (typeof user.department === "object") {
        userDepartment.value = user.department;
      } else {
        const depts = await sharingService.getDepartments();
        userDepartment.value = depts.find(
          (dept: Department) => dept.id === user.department,
        );
      }
    } else {
      toast.toast.error("Bạn chưa được phân vào khoa nào");
    }
  } catch (error) {
    toast.toast.error("Không thể tải thông tin khoa");
  }
};

const searchUsers = async (event: { query: string }) => {
  if (event.query.length < 2) {
    searchResults.value = [];
    return;
  }
  try {
    const response = await api.get("/auth/users/", {
      params: { search: event.query, page_size: 10 },
    });
    const users = Array.isArray(response.data)
      ? response.data
      : response.data.results || [];
    searchResults.value = users.map((user: any) => ({
      id: user.id,
      full_name:
        user.first_name && user.last_name
          ? `${user.first_name} ${user.last_name}`
          : user.username,
      email: user.email,
      department: user.department?.name || "Unknown Department",
    }));
  } catch {
    searchResults.value = [];
    toast.toast.error("Không thể tìm kiếm người dùng");
  }
};

const onUserSelect = (event: { value: User }) => {
  form.value.selectedUser = event.value;
  form.value.searchQuery = event.value.full_name;
};

const clearSelectedUser = () => {
  form.value.selectedUser = null;
  form.value.searchQuery = "";
  searchResults.value = [];
};

const handleSubmit = async () => {
  if (!canSubmit.value) return;

  loading.value = true;
  try {
    const permissionData = getPermissionData();
    const permission = await sharingService.createPermission(
      props.caseId,
      permissionData,
    );

    let successMessage = "";
    if (form.value.shareType === "department") {
      const deptName =
        userDepartment.value?.vietnamese_name || userDepartment.value?.name;
      successMessage = `Đã chia sẻ với tất cả sinh viên trong khoa ${deptName}!`;
    } else if (form.value.shareType === "public") {
      successMessage = "Ca bệnh đã được công khai cho tất cả người dùng!";
    } else {
      successMessage = `Đã chia sẻ với ${form.value.selectedUser?.full_name || "user"}!`;
    }

    toast.toast.success(successMessage);
    emit("permission-created", permission);
    emit("update:open", false);
  } catch (err: any) {
    if (err?.response?.status === 409) {
      const detail: string =
        err.response?.data?.detail ||
        err.response?.data?.error ||
        "Ca bệnh này đã được chia sẻ trước đó. Hãy thu hồi quyền hiện tại trước khi chia sẻ lại.";
      toast.toast.warning(detail);
      await loadExistingPermissions();
    } else {
      toast.toast.error("Không thể cấp quyền truy cập");
    }
  } finally {
    loading.value = false;
  }
};
</script>
