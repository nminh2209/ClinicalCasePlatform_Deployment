<template>
  <div class="audit-log-viewer">
    <div class="audit-header">
      <h3>📋 Lịch sử thay đổi</h3>
      <button @click="refresh" class="refresh-btn" :disabled="loading">
        🔄 Làm mới
      </button>
    </div>

    <div v-if="loading" class="loading">
      <p>Đang tải lịch sử...</p>
    </div>

    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="loadAuditLogs" class="btn btn-outline btn-sm">Thử lại</button>
    </div>

    <div v-else-if="auditLogs.length === 0" class="empty">
      <p>Không có thay đổi nào được ghi nhận</p>
    </div>

    <div v-else class="audit-timeline">
      <div v-for="(log, idx) in auditLogs" :key="log.id" class="audit-entry">
        <div class="entry-header">
          <div class="entry-time">
            <span class="change-type-badge" :class="`type-${log.change_type}`">
              {{ getChangeTypeLabel(log.change_type) }}
            </span>
            <span class="timestamp">{{ formatDate(log.timestamp) }}</span>
          </div>

          <div class="entry-actor">
            <span class="actor-name">{{ log.changed_by?.first_name || log.changed_by?.username }}</span>
            <span class="actor-role" v-if="log.changed_by?.is_instructor">
              (Giảng viên)
            </span>
          </div>
        </div>

        <div class="entry-content">
          <p class="summary">{{ log.summary }}</p>

          <!-- Optional: Show diff if available -->
          <div v-if="log.diff && Object.keys(log.diff).length > 0" class="diff-section">
            <details>
              <summary>Chi tiết thay đổi</summary>
              <div class="diff-content">
                <div v-for="(value, key) in log.diff" :key="key" class="diff-item">
                  <strong>{{ formatFieldName(key) }}:</strong>
                  <div class="diff-values">
                    <span v-if="value.old" class="old-value">{{ value.old }}</span>
                    <span class="arrow">→</span>
                    <span v-if="value.new" class="new-value">{{ value.new }}</span>
                  </div>
                </div>
              </div>
            </details>
          </div>
        </div>

        <!-- Timeline connector -->
        <div v-if="idx < auditLogs.length - 1" class="timeline-connector"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { casesService } from "../services/cases";
import type { InstructorCaseAuditLog } from "../types/instructor";

interface Props {
  caseId?: string | number;
}

const props = defineProps<Props>();

const auditLogs = ref<InstructorCaseAuditLog[]>([]);
const loading = ref(false);
const error = ref("");

onMounted(() => {
  loadAuditLogs();
});

const loadAuditLogs = async () => {
  loading.value = true;
  error.value = "";

  try {
    if (props.caseId) {
      const logs = await casesService.getInstructorCaseAuditLogs(props.caseId);
      auditLogs.value = logs;
    } else {
      const logs = await casesService.getInstructorCaseAuditLogs();
      auditLogs.value = logs;
    }
  } catch (err: any) {
    console.error("Error loading audit logs:", err);
    error.value = "Không thể tải lịch sử thay đổi. Vui lòng thử lại.";
  } finally {
    loading.value = false;
  }
};

const refresh = async () => {
  await loadAuditLogs();
};

const getChangeTypeLabel = (type: string): string => {
  const labels: Record<string, string> = {
    create: "✨ Tạo mới",
    update: "✏️ Chỉnh sửa",
    approve: "✅ Phê duyệt",
    clone: "🔄 Nhân bản",
  };
  return labels[type] || type;
};

const formatDate = (dateStr: string): string => {
  try {
    const date = new Date(dateStr);
    return date.toLocaleString("vi-VN", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return dateStr;
  }
};

const formatFieldName = (field: string): string => {
  const names: Record<string, string> = {
    title: "Tiêu đề",
    summary: "Tóm tắt",
    specialty: "Chuyên khoa",
    is_public: "Công khai",
    status: "Trạng thái",
    approved: "Phê duyệt",
  };
  return names[field] || field;
};
</script>

<style scoped lang="css">
.audit-log-viewer {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.audit-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.audit-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
}

.refresh-btn {
  background: transparent;
  border: none;
  color: #667eea;
  cursor: pointer;
  padding: 0.5rem;
  font-size: 1rem;
  transition: transform 0.2s;
}

.refresh-btn:hover:not(:disabled) {
  transform: rotate(180deg);
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading,
.error,
.empty {
  text-align: center;
  padding: 2rem 1rem;
  color: #999;
}

.error {
  background: #fee;
  border: 1px solid #fcc;
  border-radius: 6px;
  color: #c33;
}

.error .btn {
  margin-top: 1rem;
}

.audit-timeline {
  position: relative;
  padding-left: 2rem;
}

.audit-timeline::before {
  content: "";
  position: absolute;
  left: 0.5rem;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
}

.audit-entry {
  position: relative;
  margin-bottom: 2rem;
}

.audit-entry::before {
  content: "";
  position: absolute;
  left: -2.25rem;
  top: 0.5rem;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: white;
  border: 3px solid #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.entry-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 0.75rem;
  flex-wrap: wrap;
}

.entry-time {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.change-type-badge {
  display: inline-block;
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
  white-space: nowrap;
  color: white;
}

.type-create {
  background: #00b894;
}

.type-update {
  background: #fdcb6e;
  color: #333;
}

.type-approve {
  background: #667eea;
}

.type-clone {
  background: #a29bfe;
}

.timestamp {
  color: #999;
  font-size: 0.85rem;
}

.entry-actor {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  font-size: 0.9rem;
}

.actor-name {
  color: #333;
  font-weight: 600;
}

.actor-role {
  color: #999;
  font-size: 0.85rem;
}

.entry-content {
  background: #fafafa;
  padding: 1rem;
  border-radius: 6px;
  border-left: 3px solid #667eea;
}

.summary {
  margin: 0;
  color: #555;
  line-height: 1.5;
}

.diff-section {
  margin-top: 0.75rem;
}

.diff-section summary {
  cursor: pointer;
  color: #667eea;
  font-weight: 600;
  font-size: 0.9rem;
  user-select: none;
}

.diff-section summary:hover {
  text-decoration: underline;
}

.diff-content {
  margin-top: 0.75rem;
  padding: 0.75rem;
  background: white;
  border-radius: 4px;
  border: 1px solid #eee;
}

.diff-item {
  margin-bottom: 0.5rem;
  font-size: 0.85rem;
}

.diff-item strong {
  color: #333;
}

.diff-values {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  margin-top: 0.25rem;
  padding-left: 1rem;
}

.old-value {
  background: #ffebee;
  color: #c33;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  text-decoration: line-through;
  font-family: monospace;
}

.new-value {
  background: #e8f5e9;
  color: #2e7d32;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: monospace;
}

.arrow {
  color: #999;
  font-weight: bold;
}

.timeline-connector {
  position: relative;
  height: 1.5rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: transparent;
  color: #667eea;
  cursor: pointer;
  font-size: 0.85rem;
}

.btn:hover {
  background: #f5f5f5;
}

.btn-sm {
  padding: 0.4rem 0.8rem;
  font-size: 0.8rem;
}
</style>
