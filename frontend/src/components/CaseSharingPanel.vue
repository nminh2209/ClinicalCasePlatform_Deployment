<template>
  <div class="case-sharing-panel bg-white rounded-lg">
    <!-- Action Buttons -->
    <div class="flex justify-between items-center mb-6">
      <div class="flex gap-2 flex-wrap">
        <Button
          icon="pi pi-user"
          label="Chia sẻ cá nhân"
          @click="openShareModal('individual')"
        />
        <Button
          icon="pi pi-building"
          label="Chia sẻ khoa"
          outlined
          @click="openShareModal('department')"
        />
        <Button
          icon="pi pi-share-alt"
          label="Chia sẻ khách"
          outlined
          @click="openGuestModal"
        />
        <Button
          icon="pi pi-globe"
          label="Công khai"
          outlined
          @click="openShareModal('public')"
        />
      </div>
    </div>

    <!-- Stats -->
    <div class="flex items-center gap-4 mb-6">
      <Tag severity="info">
        <i class="pi pi-chart-bar me-1" />
        {{ permissions.length }} quyền chia sẻ
      </Tag>
      <Tag severity="info">
        <i class="pi pi-link me-1" />
        {{ guestAccesses.length }} liên kết khách
      </Tag>
    </div>

    <!-- Permissions Table -->
    <div class="space-y-4">
      <!-- Bulk Actions Bar -->
      <div class="flex justify-between items-center">
        <div class="flex items-center gap-2">
          <Checkbox v-model="selectAll" @change="toggleSelectAll" binary />
          <span class="text-sm text-gray-600">Chọn tất cả</span>
        </div>
        <div class="flex gap-2">
          <Button
            icon="pi pi-trash"
            label="Xóa các mục đã chọn"
            severity="danger"
            :disabled="selectedPermissions.length === 0"
            @click="bulkRevoke"
          />
          <Button
            icon="pi pi-refresh"
            label="Làm mới"
            outlined
            size="small"
            @click="() => refreshData(true)"
          />
        </div>
      </div>

      <!-- DataTable -->
      <DataTable
        :value="permissions"
        :empty-message="''"
        table-style="table-layout: fixed;"
      >
        <!-- Checkbox column -->
        <Column style="width: 50px">
          <template #header>
            <Checkbox v-model="selectAll" @change="toggleSelectAll" binary />
          </template>
          <template #body="{ data }">
            <Checkbox :value="data.id" v-model="selectedPermissions" />
          </template>
        </Column>

        <!-- Shared With -->
        <Column header="Được chia sẻ với">
          <template #body="{ data }">
            <div class="flex items-center gap-2">
              <i
                :class="[
                  'pi',
                  data.share_type === 'individual' && 'pi-user text-blue-500',
                  data.share_type === 'department' &&
                    'pi-building text-green-500',
                  data.share_type === 'public' && 'pi-globe text-purple-500',
                ]"
              />
              <div>
                <div class="font-medium">
                  {{ getPermissionDisplayName(data) }}
                </div>
                <div class="text-xs text-gray-500">
                  {{ data.share_description }}
                </div>
              </div>
            </div>
          </template>
        </Column>

        <!-- Permission Type -->
        <Column header="Loại quyền">
          <template #body="{ data }">
            <Badge
              :severity="getPermissionSeverity(data.permission_type)"
              :value="getPermissionTypeText(data.permission_type)"
            />
          </template>
        </Column>

        <!-- Expiry -->
        <Column header="Hết hạn">
          <template #body="{ data }">
            <span
              class="text-sm"
              :class="data.is_expired ? 'text-red-600' : 'text-gray-600'"
            >
              {{ data.expires_at_display || "Không giới hạn" }}
            </span>
          </template>
        </Column>

        <!-- Status -->
        <Column header="Trạng thái">
          <template #body="{ data }">
            <Badge
              :severity="data.is_expired ? 'secondary' : 'success'"
              :value="data.is_expired ? 'Hết hạn' : 'Hoạt động'"
            />
          </template>
        </Column>

        <!-- Actions -->
        <Column header="Thao tác" style="width: 120px" body-class="text-center">
          <template #body="{ data }">
            <Button
              icon="pi pi-trash"
              severity="danger"
              size="small"
              text
              @click="revokePermission(data.id)"
            />
          </template>
        </Column>
      </DataTable>

      <!-- Empty State -->
      <div
        v-if="permissions.length === 0"
        class="text-center py-12 text-gray-500"
      >
        <i class="pi pi-lock text-4xl mb-3 block" />
        <h3 class="text-lg font-medium mb-2">Chưa có quyền chia sẻ nào</h3>
        <p class="mb-4">Bắt đầu chia sẻ ca bệnh này với đồng nghiệp của bạn</p>
        <Button
          label="Chia sẻ ngay"
          icon="pi pi-user"
          @click="openShareModal('individual')"
        />
      </div>
    </div>

    <!-- Guest Links -->
    <div v-if="guestAccesses.length > 0" class="mt-8">
      <h3 class="text-lg font-semibold mb-4">Liên kết khách mời</h3>
      <div class="space-y-3">
        <div
          v-for="guest in guestAccesses"
          :key="guest.id"
          class="border rounded-lg p-4"
        >
          <div class="flex justify-between items-start">
            <div>
              <h4 class="font-medium">
                {{ guest.guest_name || guest.guest_email }}
              </h4>
              <p class="text-sm text-gray-600">{{ guest.guest_email }}</p>
              <div class="flex items-center gap-4 mt-2 text-sm">
                <span class="flex items-center gap-1">
                  <i class="pi pi-clock text-gray-500" />
                  {{ guest.expires_at_display }}
                </span>
                <span class="flex items-center gap-1">
                  <i class="pi pi-eye text-gray-500" />
                  {{ guest.access_count || 0 }} lần truy cập
                </span>
                <Badge
                  :severity="guest.is_expired ? 'secondary' : 'success'"
                  :value="guest.is_expired ? 'Hết hạn' : 'Hoạt động'"
                />
              </div>
            </div>
            <div class="flex gap-2">
              <Button
                icon="pi pi-copy"
                label="Sao chép"
                size="small"
                outlined
                @click="copyGuestLink(guest)"
              />
              <Button
                v-if="!guest.is_expired"
                icon="pi pi-clock"
                label="Gia hạn"
                size="small"
                outlined
                @click="extendGuestAccess(guest)"
              />
              <Button
                icon="pi pi-trash"
                size="small"
                severity="danger"
                @click="deleteGuestAccess(guest.id)"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <SharePermissionModal
      :open="showShareModal"
      @update:open="(value: boolean) => (showShareModal = value)"
      :case-id="caseId"
      :share-type="shareType"
      @permission-created="onPermissionCreated"
    />

    <GuestAccessModal
      :open="showGuestModal"
      @update:open="(value: boolean) => (showGuestModal = value)"
      :case-id="caseId"
      @guest-created="onGuestCreated"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted } from "vue";
import { useToast } from "@/composables/useToast";
import sharingService from "@/services/sharing";
import Button from "primevue/button";
import Tag from "primevue/tag";
import Badge from "primevue/badge";
import Checkbox from "primevue/checkbox";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import SharePermissionModal from "./SharePermissionModal.vue";
import GuestAccessModal from "./GuestAccessModal.vue";

interface Permission {
  id: number;
  case: number;
  user?: number;
  user_name?: string;
  user_email?: string;
  share_type: "individual" | "department" | "class_group" | "public";
  target_department?: number;
  department_name?: string;
  class_group?: string;
  permission_type: "view" | "comment" | "analyze" | "edit";
  expires_at_display?: string;
  is_active: boolean;
  is_expired: boolean;
  access_count?: number;
  share_description?: string;
}

interface GuestAccess {
  id: number;
  case: number;
  guest_email: string;
  guest_name?: string;
  permission_type: "view" | "comment";
  expires_at_display: string;
  is_expired: boolean;
  access_count: number;
  access_token: string;
}

const props = defineProps<{ caseId: number }>();

const { toast } = useToast();

const permissions = ref<Permission[]>([]);
const guestAccesses = ref<GuestAccess[]>([]);
const selectedPermissions = ref<number[]>([]);
const selectAll = ref(false);

const showShareModal = ref(false);
const showGuestModal = ref(false);
type PanelShareType = "individual" | "department" | "public";
const shareType = ref<PanelShareType>("individual");

const dataCache = ref<
  Map<
    number,
    { permissions: Permission[]; guests: GuestAccess[]; timestamp: number }
  >
>(new Map());
const CACHE_DURATION = 10 * 60 * 1000;

const refreshData = async (forceRefresh = false) => {
  try {
    const cacheKey = props.caseId;
    const cachedData = dataCache.value.get(cacheKey);

    if (
      !forceRefresh &&
      cachedData &&
      Date.now() - cachedData.timestamp < CACHE_DURATION
    ) {
      permissions.value = [...cachedData.permissions];
      guestAccesses.value = [...cachedData.guests];
      console.log("Using cached data for case", cacheKey);
      return;
    }

    console.log("Loading fresh data for case", cacheKey);
    await Promise.all([loadPermissions(), loadGuestAccesses()]);

    dataCache.value.set(cacheKey, {
      permissions: [...permissions.value],
      guests: [...guestAccesses.value],
      timestamp: Date.now(),
    });

    if (forceRefresh) toast.success("Đã làm mới dữ liệu");
  } catch (error) {
    console.error("Error in refreshData:", error);
    toast.error("Lỗi khi tải dữ liệu");
  }
};

const loadPermissions = async () => {
  try {
    const data = await sharingService.getCasePermissions(props.caseId);
    permissions.value = (Array.isArray(data) ? data : [])
      .filter((p) => p && typeof p === "object" && typeof p.id === "number")
      .map((p) => ({
        ...p,
        share_type: p.share_type || "individual",
        permission_type: p.permission_type || "view",
        is_active: p.is_active !== undefined ? p.is_active : true,
        is_expired: p.is_expired !== undefined ? p.is_expired : false,
        user_name: p.user_name || "",
        user_email: p.user_email || "",
        department_name: p.department_name || "",
        class_group: p.class_group || "",
        share_description: p.share_description || "",
      }));
  } catch (error) {
    console.error("Error loading permissions:", error);
    permissions.value = [];
    toast.error("Lỗi khi tải quyền truy cập");
  }
};

const loadGuestAccesses = async () => {
  try {
    const data = await sharingService.getGuestAccesses(props.caseId);
    guestAccesses.value = Array.isArray(data) ? data : [];
  } catch (error) {
    console.error("Error loading guest accesses:", error);
    guestAccesses.value = [];
  }
};

const openShareModal = (type: PanelShareType) => {
  shareType.value = type;
  showShareModal.value = true;
};

const openGuestModal = () => {
  showGuestModal.value = true;
};

const onGuestCreated = (guest: any) => {
  const fullGuest: GuestAccess = {
    ...guest,
    expires_at_display: guest.expires_at_display || "",
    is_expired: false,
    access_count: 0,
    access_token: guest.access_token || "",
  };
  guestAccesses.value.unshift(fullGuest);
  const cacheKey = props.caseId;
  const cachedData = dataCache.value.get(cacheKey);
  if (cachedData) {
    cachedData.guests = [...guestAccesses.value];
    cachedData.timestamp = Date.now();
  } else {
    dataCache.value.set(cacheKey, {
      permissions: [...permissions.value],
      guests: [...guestAccesses.value],
      timestamp: Date.now(),
    });
  }
  console.log("Guest created and cache updated", {
    guestId: guest.id,
    cacheKey,
  });
};

const copyGuestLink = (guest: GuestAccess) => {
  const link = `${window.location.origin}/guest-access/${guest.access_token}`;
  navigator.clipboard.writeText(link);
  toast.success("Đã sao chép liên kết");
};

const extendGuestAccess = async (guest: GuestAccess) => {
  try {
    await sharingService.extendGuestAccess(props.caseId, guest.id, 24);
    await loadGuestAccesses();
    const cacheKey = props.caseId;
    const cachedData = dataCache.value.get(cacheKey);
    if (cachedData) {
      cachedData.guests = [...guestAccesses.value];
      cachedData.timestamp = Date.now();
    }
    console.log("Guest access extended and cache updated", {
      guestId: guest.id,
      cacheKey,
    });
    toast.success("Đã gia hạn 24 giờ");
  } catch (error) {
    console.error("Error extending guest access:", error);
    toast.error("Lỗi khi gia hạn");
  }
};

const deleteGuestAccess = async (guestId: number) => {
  if (!confirm("Bạn có chắc muốn xóa truy cập khách này?")) return;
  try {
    await sharingService.deleteGuestAccess(props.caseId, guestId);
    guestAccesses.value = guestAccesses.value.filter((g) => g.id !== guestId);
    const cacheKey = props.caseId;
    const cachedData = dataCache.value.get(cacheKey);
    if (cachedData) {
      cachedData.guests = [...guestAccesses.value];
      cachedData.timestamp = Date.now();
    }
    console.log("Guest access deleted and cache updated", {
      guestId,
      cacheKey,
    });
    toast.success("Đã xóa liên kết khách mời");
  } catch (error) {
    console.error("Error deleting guest access:", error);
    toast.error("Lỗi khi xóa liên kết khách mời");
  }
};

const onPermissionCreated = (permission: any) => {
  const fullPermission: Permission = {
    ...permission,
    is_active: true,
    is_expired: false,
  };
  permissions.value.unshift(fullPermission);
  const cacheKey = props.caseId;
  const cachedData = dataCache.value.get(cacheKey);
  if (cachedData) {
    cachedData.permissions = [...permissions.value];
    cachedData.timestamp = Date.now();
  } else {
    dataCache.value.set(cacheKey, {
      permissions: [...permissions.value],
      guests: [...guestAccesses.value],
      timestamp: Date.now(),
    });
  }
  console.log("Permission created and cache updated", {
    permissionId: permission.id,
    cacheKey,
  });
};

const revokePermission = async (permissionId: number) => {
  if (!confirm("Bạn có chắc muốn xóa quyền này?")) return;
  try {
    await sharingService.deletePermission(props.caseId, permissionId);
    permissions.value = permissions.value.filter((p) => p.id !== permissionId);
    const cacheKey = props.caseId;
    const cachedData = dataCache.value.get(cacheKey);
    if (cachedData) {
      cachedData.permissions = [...permissions.value];
      cachedData.timestamp = Date.now();
    }
    console.log("Permission deleted and cache updated", {
      permissionId,
      cacheKey,
    });
    toast.success("Quyền đã được xóa");
  } catch (error) {
    toast.error("Lỗi khi xóa quyền");
  }
};

const bulkRevoke = async () => {
  if (selectedPermissions.value.length === 0) return;
  if (
    !confirm(
      `Bạn có chắc muốn xóa ${selectedPermissions.value.length} quyền đã chọn?`,
    )
  )
    return;
  try {
    for (const permissionId of selectedPermissions.value) {
      await sharingService.deletePermission(props.caseId, permissionId);
    }
    permissions.value = permissions.value.filter(
      (p) => !selectedPermissions.value.includes(p.id),
    );
    selectedPermissions.value = [];
    selectAll.value = false;
    const cacheKey = props.caseId;
    const cachedData = dataCache.value.get(cacheKey);
    if (cachedData) {
      cachedData.permissions = [...permissions.value];
      cachedData.timestamp = Date.now();
    }
    console.log("Bulk permissions deleted and cache updated", { cacheKey });
    toast.success("Đã xóa các quyền đã chọn");
  } catch (error) {
    toast.error("Lỗi khi xóa quyền");
    loadPermissions();
  }
};

const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedPermissions.value = permissions.value.map((p) => p.id);
  } else {
    selectedPermissions.value = [];
  }
};

const getPermissionDisplayName = (permission: Permission): string => {
  if (permission.share_type === "individual")
    return permission.user_name || permission.user_email || "Unknown User";
  if (permission.share_type === "department")
    return permission.department_name || "Unknown Department";
  if (permission.share_type === "class_group")
    return permission.class_group || "Unknown Group";
  if (permission.share_type === "public") return "Công khai";
  return "Unknown";
};

const getPermissionTypeText = (type: string): string => {
  const types: Record<string, string> = {
    view: "Xem",
    comment: "Bình luận",
    analyze: "Phân tích",
    edit: "Chỉnh sửa",
  };
  return types[type] || type;
};

// Maps old shadcn variant names → PrimeVue severity strings
const getPermissionSeverity = (type: string): string => {
  const map: Record<string, string> = {
    view: "info",
    comment: "secondary",
    analyze: "warn",
    edit: "danger",
  };
  return map[type] || "info";
};

watch(
  () => selectedPermissions.value,
  (selected) => {
    selectAll.value =
      selected.length === permissions.value.length &&
      permissions.value.length > 0;
  },
  { deep: true },
);

onMounted(() => {
  console.log("Component mounted for case", props.caseId);
  refreshData(false);
});

watch(
  () => props.caseId,
  (newCaseId) => {
    console.log("Case changed to", newCaseId);
    refreshData(false);
  },
);

onUnmounted(() => {
  console.log("Component unmounted, keeping cache for case", props.caseId);
});
</script>

<style scoped>
.case-sharing-panel {
  max-width: 1200px;
  margin: 0 auto;
}
</style>
