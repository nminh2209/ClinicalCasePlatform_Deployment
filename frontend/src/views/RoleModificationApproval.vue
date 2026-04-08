<template>
  <div class="page-wrapper">
    <div class="page-header">
      <div>
        <h1 class="page-title">Duyệt yêu cầu đổi vai trò</h1>
        <p class="page-subtitle">
          Xem xét và phê duyệt / từ chối các yêu cầu thay đổi vai trò từ sinh
          viên.
        </p>
      </div>
      <div class="filter-group">
        <Select
          v-model="statusFilter"
          :options="filterOptions"
          optionLabel="label"
          optionValue="value"
          placeholder="Lọc theo trạng thái"
          style="min-width: 180px"
          @change="loadRequests"
        />
        <Button
          icon="pi pi-refresh"
          text
          severity="secondary"
          @click="loadRequests"
          title="Làm mới"
        />
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading-state">
      <i class="pi pi-spin pi-spinner loading-icon" />
      <span>Đang tải…</span>
    </div>

    <!-- Empty -->
    <div v-else-if="requests.length === 0" class="empty-state">
      <i class="pi pi-inbox empty-icon" />
      <p>Không có yêu cầu nào.</p>
    </div>

    <!-- Request cards -->
    <div v-else class="requests-list">
      <div v-for="req in requests" :key="req.id" class="request-card">
        <div class="card-header">
          <div class="requester-info">
            <span class="requester-name">{{ req.full_name }}</span>
            <span class="requester-email">{{ req.email }}</span>
          </div>
          <span :class="['status-badge', `status-${req.status}`]">
            {{ statusLabel(req.status) }}
          </span>
        </div>

        <div class="card-body">
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">MSSV</span>
              <span class="info-value">{{ req.student_id || "—" }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Khoa / Bộ môn</span>
              <span class="info-value">{{ req.department_name || "—" }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Chuyên ngành</span>
              <span class="info-value">{{ req.specialty }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Mã nhân viên</span>
              <span class="info-value">{{ req.employee_id || "—" }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Đơn vị công tác</span>
              <span class="info-value">{{ req.institution || "—" }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Ngày gửi</span>
              <span class="info-value">{{ formatDate(req.created_at) }}</span>
            </div>
          </div>

          <div class="reason-block">
            <span class="info-label">Lý do yêu cầu</span>
            <p class="reason-text">{{ req.reason }}</p>
          </div>

          <div
            v-if="req.status === 'rejected' && req.rejection_reason"
            class="rejection-block"
          >
            <span class="info-label">Lý do từ chối (đã ghi)</span>
            <p class="rejection-text">{{ req.rejection_reason }}</p>
          </div>

          <div
            v-if="req.status === 'approved' || req.status === 'rejected'"
            class="reviewed-by"
          >
            Đã xét duyệt bởi <strong>{{ req.reviewed_by_name }}</strong> vào
            {{ formatDate(req.reviewed_at) }}
          </div>
        </div>

        <!-- Actions (only for pending) -->
        <div v-if="req.status === 'pending'" class="card-footer">
          <Button
            label="Chấp thuận"
            icon="pi pi-check"
            severity="success"
            @click="openApproveDialog(req)"
          />
          <Button
            label="Từ chối"
            icon="pi pi-times"
            severity="danger"
            outlined
            @click="openRejectDialog(req)"
          />
        </div>
      </div>
    </div>

    <!-- Approve confirmation dialog -->
    <Dialog
      v-model:visible="approveDialog.visible"
      header="Xác nhận chấp thuận"
      :modal="true"
      style="max-width: 440px; width: 95vw"
    >
      <p>
        Bạn có chắc muốn <strong>chấp thuận</strong> yêu cầu của
        <strong>{{ approveDialog.request?.full_name }}</strong
        >? Vai trò của họ sẽ được đổi thành <strong>Giảng viên</strong> ngay lập
        tức.
      </p>
      <template #footer>
        <Button
          label="Huỷ"
          text
          @click="approveDialog.visible = false"
          :disabled="approveDialog.loading"
        />
        <Button
          label="Xác nhận chấp thuận"
          icon="pi pi-check"
          severity="success"
          :loading="approveDialog.loading"
          @click="confirmApprove"
        />
      </template>
    </Dialog>

    <!-- Reject dialog (requires reason) -->
    <Dialog
      v-model:visible="rejectDialog.visible"
      header="Từ chối yêu cầu"
      :modal="true"
      style="max-width: 480px; width: 95vw"
    >
      <div class="reject-form">
        <p>
          Từ chối yêu cầu của
          <strong>{{ rejectDialog.request?.full_name }}</strong
          >. Bạn <strong>bắt buộc</strong> phải cung cấp lý do để người dùng
          được thông báo.
        </p>
        <div class="form-group">
          <label class="form-label">
            Lý do từ chối <span class="required-star">*</span>
          </label>
          <Textarea
            v-model="rejectDialog.reason"
            placeholder="Nhập lý do từ chối..."
            rows="4"
            style="width: 100%; resize: vertical"
            :class="{ 'p-invalid': rejectDialog.reasonError }"
          />
          <p v-if="rejectDialog.reasonError" class="field-error">
            {{ rejectDialog.reasonError }}
          </p>
        </div>
      </div>
      <template #footer>
        <Button
          label="Huỷ"
          text
          @click="rejectDialog.visible = false"
          :disabled="rejectDialog.loading"
        />
        <Button
          label="Xác nhận từ chối"
          icon="pi pi-check"
          severity="danger"
          :loading="rejectDialog.loading"
          @click="confirmReject"
        />
      </template>
    </Dialog>

    <!-- Toast (success/error feedback) -->
    <Toast />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import api from "@/services/api";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import Select from "primevue/select";
import Textarea from "primevue/textarea";
import Toast from "primevue/toast";
import { useToast } from "primevue/usetoast";

const toast = useToast();

const requests = ref<any[]>([]);
const loading = ref(false);
const statusFilter = ref("pending");

const filterOptions = [
  { label: "Đang chờ", value: "pending" },
  { label: "Đã chấp thuận", value: "approved" },
  { label: "Đã từ chối", value: "rejected" },
  { label: "Tất cả", value: "" },
];

const approveDialog = ref<{
  visible: boolean;
  request: any | null;
  loading: boolean;
}>({ visible: false, request: null, loading: false });

const rejectDialog = ref<{
  visible: boolean;
  request: any | null;
  reason: string;
  reasonError: string;
  loading: boolean;
}>({
  visible: false,
  request: null,
  reason: "",
  reasonError: "",
  loading: false,
});

const loadRequests = async () => {
  loading.value = true;
  try {
    const params: Record<string, string> = {};
    if (statusFilter.value) params.status = statusFilter.value;
    const response = await api.get("/auth/role-requests/list/", { params });
    requests.value = response.data?.results || response.data || [];
  } catch {
    toast.add({
      severity: "error",
      summary: "Lỗi",
      detail: "Không thể tải danh sách yêu cầu.",
      life: 4000,
    });
  } finally {
    loading.value = false;
  }
};

const openApproveDialog = (req: any) => {
  approveDialog.value = { visible: true, request: req, loading: false };
};

const openRejectDialog = (req: any) => {
  rejectDialog.value = {
    visible: true,
    request: req,
    reason: "",
    reasonError: "",
    loading: false,
  };
};

const confirmApprove = async () => {
  if (!approveDialog.value.request) return;
  approveDialog.value.loading = true;
  try {
    await api.post(
      `/auth/role-requests/${approveDialog.value.request.id}/approve/`,
    );
    toast.add({
      severity: "success",
      summary: "Đã chấp thuận",
      detail: `Vai trò của ${approveDialog.value.request.full_name} đã được đổi thành Giảng viên. Người dùng đã được thông báo.`,
      life: 5000,
    });
    approveDialog.value.visible = false;
    await loadRequests();
  } catch (err: any) {
    const msg = err.response?.data?.error || "Không thể chấp thuận yêu cầu.";
    toast.add({ severity: "error", summary: "Lỗi", detail: msg, life: 4000 });
  } finally {
    approveDialog.value.loading = false;
  }
};

const confirmReject = async () => {
  if (!rejectDialog.value.request) return;
  const reason = rejectDialog.value.reason.trim();
  if (!reason) {
    rejectDialog.value.reasonError = "Lý do từ chối là bắt buộc.";
    return;
  }
  rejectDialog.value.reasonError = "";
  rejectDialog.value.loading = true;
  try {
    await api.post(
      `/auth/role-requests/${rejectDialog.value.request.id}/reject/`,
      {
        rejection_reason: reason,
      },
    );
    toast.add({
      severity: "info",
      summary: "Đã từ chối",
      detail: `Yêu cầu của ${rejectDialog.value.request.full_name} đã bị từ chối. Người dùng đã được thông báo kèm lý do.`,
      life: 5000,
    });
    rejectDialog.value.visible = false;
    await loadRequests();
  } catch (err: any) {
    const msg = err.response?.data?.error || "Không thể từ chối yêu cầu.";
    toast.add({ severity: "error", summary: "Lỗi", detail: msg, life: 4000 });
  } finally {
    rejectDialog.value.loading = false;
  }
};

const statusLabel = (s: string) => {
  return (
    { pending: "Đang chờ", approved: "Đã chấp thuận", rejected: "Đã từ chối" }[
      s
    ] ?? s
  );
};

const formatDate = (iso: string) => {
  if (!iso) return "—";
  return new Date(iso).toLocaleDateString("vi-VN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
};

onMounted(loadRequests);
</script>

<style scoped>
.page-wrapper {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 1.5rem;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--foreground);
  margin-bottom: 0.25rem;
}

.page-subtitle {
  font-size: 0.9375rem;
  color: var(--muted-foreground);
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 4rem 1rem;
  color: var(--muted-foreground);
}

.loading-icon,
.empty-icon {
  font-size: 2.5rem;
}

.requests-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.request-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--border);
  background: var(--secondary);
}

.requester-info {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.requester-name {
  font-weight: 700;
  font-size: 1rem;
  color: var(--foreground);
}

.requester-email {
  font-size: 0.8125rem;
  color: var(--muted-foreground);
}

.status-badge {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 3px 12px;
  border-radius: 999px;
  white-space: nowrap;
}

.status-pending {
  background: #fef9c3;
  color: #854d0e;
}

.status-approved {
  background: #dcfce7;
  color: #166534;
}

.status-rejected {
  background: #fee2e2;
  color: #991b1b;
}

.card-body {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.75rem 1.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.info-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--muted-foreground);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.info-value {
  font-size: 0.9375rem;
  color: var(--foreground);
}

.reason-block,
.rejection-block {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.reason-text {
  font-size: 0.9375rem;
  color: var(--foreground);
  white-space: pre-wrap;
  line-height: 1.6;
}

.rejection-block {
  background: #fff7f7;
  border: 1px solid #fecaca;
  border-radius: 10px;
  padding: 0.75rem 1rem;
}

.rejection-text {
  font-size: 0.9375rem;
  color: #7f1d1d;
  white-space: pre-wrap;
}

.reviewed-by {
  font-size: 0.8125rem;
  color: var(--muted-foreground);
}

.card-footer {
  display: flex;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  border-top: 1px solid var(--border);
  background: var(--secondary);
}

/* Reject dialog */
.reject-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 0.5rem 0;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--foreground);
}

.required-star {
  color: #ef4444;
}

.field-error {
  font-size: 0.8125rem;
  color: #ef4444;
}
</style>
