<template>
  <div class="relative inline-block">
    <!-- Bell button with overlaid unread badge -->
    <div class="bell-wrapper">
      <Button
        icon="pi pi-bell"
        text
        severity="secondary"
        aria-label="Thông báo"
        @click="toggleOpen"
      />
      <!-- Badge overlay: absolute-positioned over the button -->
      <Badge
        v-if="unreadCount > 0"
        :value="unreadCount > 9 ? '9+' : String(unreadCount)"
        severity="danger"
        class="bell-badge"
      />
    </div>

    <!-- Role approved: mandatory re-login dialog -->
    <Dialog
      v-model:visible="roleApprovedDialog"
      header="Vai trò đã được nâng cấp!"
      :modal="true"
      :closable="false"
      style="max-width: 460px; width: 95vw"
    >
      <div
        style="
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 1rem;
          padding: 1rem 0;
          text-align: center;
        "
      >
        <i class="pi pi-check-circle" style="font-size: 3rem; color: #16a34a" />
        <p>
          Chúc mừng! Yêu cầu trở thành <strong>Giảng viên</strong> của bạn đã
          được chấp thuận.
        </p>
        <p>
          Để vai trò mới có hiệu lực, bạn
          <strong>phải đăng xuất và đăng nhập lại</strong>. Sau khi đăng nhập,
          bạn sẽ được chuyển sang giao diện Giảng viên.
        </p>
      </div>
      <template #footer>
        <Button
          label="Đăng xuất ngay"
          icon="pi pi-sign-out"
          severity="success"
          @click="handleRoleApprovedLogout"
        />
      </template>
    </Dialog>

    <Popover ref="popoverRef" class="notification-popover">
      <!-- Header -->
      <div class="notif-header">
        <div>
          <h1 class="notif-title">Thông báo</h1>
          <p v-if="unreadCount > 0" class="notif-subtitle">
            {{ unreadCount }} chưa đọc
          </p>
        </div>
        <Button
          v-if="unreadCount > 0"
          label="Đánh dấu đã đọc tất cả"
          text
          severity="secondary"
          size="small"
          @click="markAllAsRead"
        />
      </div>

      <!-- Body -->
      <div class="notif-body">
        <!-- Empty state -->
        <div v-if="filteredNotifications.length === 0" class="notif-empty">
          <i class="pi pi-bell notif-empty-icon" />
          <span>Không có thông báo</span>
        </div>

        <!-- Notification list -->
        <div v-else class="notif-list">
          <div
            v-for="notif in filteredNotifications"
            :key="notif.id"
            :class="['notif-item', { 'notif-item--unread': !notif.read }]"
            @click="onNotificationClick(notif)"
          >
            <div class="notif-item-inner">
              <!-- Icon -->
              <div class="notif-icon-wrap">
                <i
                  :class="[
                    getIconClass(notif.type),
                    'notif-type-icon',
                    getIconColor(notif.type),
                  ]"
                />
              </div>

              <!-- Content -->
              <div class="notif-content">
                <div class="notif-row-top">
                  <p
                    :class="[
                      'notif-msg-title',
                      { 'font-semibold': !notif.read },
                    ]"
                  >
                    {{ notif.title }}
                  </p>
                  <Button
                    icon="pi pi-times"
                    text
                    rounded
                    severity="secondary"
                    size="small"
                    class="notif-dismiss-btn"
                    @click.stop="removeNotification(notif.id)"
                  />
                </div>

                <p class="notif-msg-body">{{ notif.message }}</p>

                <div class="notif-row-bottom">
                  <p class="notif-time">{{ notif.time }}</p>
                  <Button
                    v-if="!notif.read"
                    icon="pi pi-check"
                    label="Đã đọc"
                    text
                    severity="info"
                    size="small"
                    class="notif-read-btn"
                    @click.stop="markAsRead(notif.id)"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Popover>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import Popover from "primevue/popover";
import Badge from "primevue/badge";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const WS_URL = API_URL.replace(/^http/, "ws");

const props = defineProps({
  userRole: {
    type: String,
    default: "student",
    validator: (v) => ["student", "instructor", "admin"].includes(v),
  },
});

const emit = defineEmits(["navigate"]);

const popoverRef = ref(null);
const notifications = ref([]);
const loading = ref(false);
const roleApprovedDialog = ref(false);

let websocket = null;
let reconnectTimeout = null;
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 3;
let pingInterval = null;

const connectWebSocket = () => {
  const token = localStorage.getItem("access_token");
  if (!token) return;
  if (reconnectAttempts >= MAX_RECONNECT_ATTEMPTS) return;

  try {
    websocket = new WebSocket(`${WS_URL}/ws/notifications/?token=${token}`);

    websocket.onopen = () => {
      reconnectAttempts = 0;
      pingInterval = setInterval(() => {
        if (websocket && websocket.readyState === WebSocket.OPEN) {
          websocket.send(JSON.stringify({ type: "ping" }));
        }
      }, 30000);
    };

    websocket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === "notification") {
          const newNotif = {
            id: data.notification.id.toString(),
            type: data.notification.type,
            title: data.notification.title,
            message: data.notification.message,
            time: "Vừa xong",
            read: data.notification.is_read,
            actionUrl: data.notification.action_url,
          };
          notifications.value.unshift(newNotif);
          // Automatically show re-login dialog when role is approved via WebSocket
          if (newNotif.type === "role_approved") {
            roleApprovedDialog.value = true;
          }
          if (Notification.permission === "granted") {
            new Notification(newNotif.title, {
              body: newNotif.message,
              icon: "/favicon.ico",
            });
          }
        }
      } catch {}
    };

    websocket.onclose = () => {
      if (pingInterval) {
        clearInterval(pingInterval);
        pingInterval = null;
      }
      reconnectAttempts++;
      if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
        reconnectTimeout = setTimeout(() => connectWebSocket(), 5000);
      }
    };
  } catch {}
};

const disconnectWebSocket = () => {
  if (reconnectTimeout) {
    clearTimeout(reconnectTimeout);
    reconnectTimeout = null;
  }
  if (pingInterval) {
    clearInterval(pingInterval);
    pingInterval = null;
  }
  if (websocket) {
    websocket.close();
    websocket = null;
  }
};

const fetchNotifications = async () => {
  try {
    loading.value = true;
    const token = localStorage.getItem("access_token");
    const response = await axios.get(`${API_URL}/api/notifications/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const data = response.data.results || response.data;
    if (Array.isArray(data)) {
      notifications.value = data.map((n) => ({
        id: n.id.toString(),
        type: n.notification_type,
        title: n.title,
        message: n.message,
        time: n.time_ago,
        read: n.is_read,
        actionUrl: n.action_url,
      }));
    } else {
      notifications.value = [];
    }
  } catch {
    notifications.value = [];
  } finally {
    loading.value = false;
  }
};

const unreadCount = computed(
  () => notifications.value.filter((n) => !n.read).length,
);

const markAsRead = async (id) => {
  try {
    const token = localStorage.getItem("access_token");
    await axios.post(
      `${API_URL}/api/notifications/${id}/mark-read/`,
      {},
      {
        headers: { Authorization: `Bearer ${token}` },
      },
    );
    const idx = notifications.value.findIndex((n) => n.id === id);
    if (idx !== -1) notifications.value[idx].read = true;
  } catch {}
};

const markAllAsRead = async () => {
  try {
    const token = localStorage.getItem("access_token");
    await axios.post(
      `${API_URL}/api/notifications/mark-all-read/`,
      {},
      {
        headers: { Authorization: `Bearer ${token}` },
      },
    );
    notifications.value.forEach((n) => (n.read = true));
  } catch {}
};

const removeNotification = async (id) => {
  try {
    const token = localStorage.getItem("access_token");
    await axios.delete(`${API_URL}/api/notifications/${id}/delete/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    notifications.value = notifications.value.filter((n) => n.id !== id);
  } catch {}
};

const getIconClass = (type) => {
  const map = {
    grade: "pi pi-star",
    submission: "pi pi-file",
    comment: "pi pi-comment",
    assignment: "pi pi-file-edit",
    reminder: "pi pi-clock",
    role_request: "pi pi-user-edit",
    role_approved: "pi pi-check-circle",
    role_rejected: "pi pi-times-circle",
  };
  return map[type] || "pi pi-bell";
};

const getIconColor = (type) => {
  const map = {
    grade: "text-yellow-500",
    submission: "text-blue-500",
    comment: "text-indigo-500",
    assignment: "text-purple-500",
    reminder: "text-orange-500",
    role_request: "text-violet-500",
    role_approved: "text-green-500",
    role_rejected: "text-red-500",
  };
  return map[type] || "text-gray-400";
};

const handleRoleApprovedLogout = () => {
  roleApprovedDialog.value = false;
  // Clear auth and redirect to login
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user");
  window.location.href = "/login";
};

const onNotificationClick = (notification) => {
  markAsRead(notification.id);
  if (notification.type === "role_approved") {
    // Show mandatory re-login dialog instead of navigating
    roleApprovedDialog.value = true;
    return;
  }
  if (notification.actionUrl) window.location.href = notification.actionUrl;
};

const filteredNotifications = computed(() => {
  if (props.userRole === "student") {
    return notifications.value.filter((n) =>
      [
        "grade",
        "comment",
        "assignment",
        "reminder",
        "feedback",
        "role_approved",
        "role_rejected",
      ].includes(n.type),
    );
  }
  if (props.userRole === "instructor") {
    return notifications.value.filter((n) =>
      ["submission", "comment"].includes(n.type),
    );
  }
  // admin sees everything including role_request
  return notifications.value;
});

const toggleOpen = (event) => {
  popoverRef.value.toggle(event);
  if (notifications.value.length === 0) fetchNotifications();
};

onMounted(() => {
  fetchNotifications();
  if ("Notification" in window && Notification.permission === "default") {
    Notification.requestPermission();
  }
});

onBeforeUnmount(() => disconnectWebSocket());
</script>

<style scoped>
/* Bell button wrapper — positions the badge overlay */
.bell-wrapper {
  position: relative;
  display: inline-flex;
}

/* Override PrimeVue Badge default position so it sits on the button corner.
   globals.css .p-badge sets background/color; we only add layout here. */
.bell-badge {
  position: absolute;
  top: 2px;
  right: 2px;
  min-width: 18px;
  height: 18px;
  font-size: 0.65rem;
  line-height: 18px;
  padding: 0 4px;
  pointer-events: none;
}

/* Popover width */
.notification-popover {
  width: 380px;
}

/* Header */
.notif-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1rem 0.75rem;
  border-bottom: 1px solid var(--border);
}

.notif-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--foreground);
  margin: 0;
}

.notif-subtitle {
  font-size: 0.75rem;
  color: var(--muted-foreground);
  margin: 0.125rem 0 0;
}

/* Body scroll container */
.notif-body {
  max-height: 400px;
  overflow-y: auto;
}

/* Empty state */
.notif-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 3rem 1rem;
  font-size: 0.875rem;
  color: var(--muted-foreground);
}

.notif-empty-icon {
  font-size: 2rem;
  color: var(--muted);
}

/* Notification list */
.notif-list {
  divide-y: 1px solid var(--border);
}

.notif-item {
  padding: 0.75rem 1rem;
  cursor: pointer;
  transition: background-color 0.15s;
}

.notif-item:hover {
  background-color: var(--secondary);
}

.notif-item--unread {
  background-color: rgba(59, 130, 246, 0.04);
}

.notif-item-inner {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.notif-icon-wrap {
  flex-shrink: 0;
  margin-top: 2px;
}

.notif-type-icon {
  font-size: 1rem;
}

.notif-content {
  flex: 1;
  min-width: 0;
}

.notif-row-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
}

.notif-msg-title {
  font-size: 0.875rem;
  line-height: 1.4;
  color: var(--foreground);
  margin: 0;
}

.notif-dismiss-btn {
  flex-shrink: 0;
  width: 1.5rem;
  height: 1.5rem;
  margin-top: -4px;
  margin-right: -8px;
}

.notif-msg-body {
  font-size: 0.75rem;
  color: var(--muted-foreground);
  margin: 0 0 0.5rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.notif-row-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.notif-time {
  font-size: 0.75rem;
  color: var(--muted-foreground);
  margin: 0;
}

.notif-read-btn {
  height: 1.5rem;
  font-size: 0.75rem;
}
</style>
