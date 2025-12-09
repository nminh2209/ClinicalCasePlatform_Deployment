<template>
  <div class="relative" ref="root">
    <!-- Trigger -->
    <Button variant="ghost" size="icon" class="relative" @click="toggleOpen">
      <Bell class="h-5 w-5" />
      <span
        v-if="unreadCount > 0"
        class="absolute -top-1 -right-1 inline-flex items-center justify-center w-5 h-5 text-xs font-medium text-white bg-red-500 rounded-full"
      >
        {{ unreadCount > 9 ? "9+" : unreadCount }}
      </span>
    </Button>

    <!-- Popover -->
    <div
      v-if="open"
      class="absolute right-0 mt-2 w-[380px] bg-white border rounded shadow-lg z-50"
      @click.outside="close"
    >
      <div class="flex items-center justify-between p-4 border-b">
        <div>
          <h3 class="text-gray-800 text-sm font-semibold">Thông báo</h3>
          <p v-if="unreadCount > 0" class="text-xs text-gray-500">
            {{ unreadCount }} chưa đọc
          </p>
        </div>
        <Button
          v-if="unreadCount > 0"
          variant="ghost"
          size="sm"
          class="text-xs"
          @click="markAllAsRead"
        >
          Đánh dấu đã đọc tất cả
        </Button>
      </div>

      <div class="max-h-[400px] overflow-y-auto">
        <div
          v-if="filteredNotifications.length === 0"
          class="py-12 text-center text-sm text-gray-500"
        >
          <Bell class="h-12 w-12 mx-auto mb-3 text-gray-300" />
          Không có thông báo
        </div>

        <div v-else class="divide-y">
          <div
            v-for="notif in filteredNotifications"
            :key="notif.id"
            :class="[
              'p-4 cursor-pointer transition-colors',
              !notif.read ? 'bg-blue-50/50' : 'hover:bg-gray-50',
            ]"
            @click="onNotificationClick(notif)"
          >
            <div class="flex items-start gap-3">
              <div class="shrink-0 mt-1">
                <component :is="getIconComponent(notif.type)" class="h-4 w-4" />
              </div>

              <div class="flex-1 min-w-0">
                <div class="flex items-start justify-between gap-2 mb-1">
                  <p
                    :class="
                      !notif.read
                        ? 'font-medium text-gray-800'
                        : 'text-gray-700'
                    "
                  >
                    {{ notif.title }}
                  </p>

                  <div class="flex items-center gap-2">
                    <Button
                      variant="ghost"
                      size="icon"
                      class="h-6 w-6 shrink-0"
                      @click.stop="removeNotification(notif.id)"
                    >
                      <X class="h-3 w-3" />
                    </Button>
                  </div>
                </div>

                <p class="text-sm text-gray-500 mb-2 truncate">
                  {{ notif.message }}
                </p>
                <div class="flex items-center justify-between">
                  <p class="text-xs text-gray-400">{{ notif.time }}</p>

                  <Button
                    v-if="!notif.read"
                    variant="ghost"
                    size="icon"
                    class="h-6 w-6 shrink-0"
                    @click.stop="markAsRead(notif.id)"
                  >
                    <Check class="h-3 w-3" />
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- <div v-if="filteredNotifications.length > 0" class="border-t p-2">
        <Button
          variant="ghost"
          size="sm"
          class="w-full text-sm"
          @click="$emit('navigate', 'notifications')"
        >
          Xem tất cả thông báo
        </Button>
      </div> -->
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import {
  Bell,
  Check,
  X,
  Clock,
  Award,
  MessageSquare,
  FileText,
} from "lucide-vue-next";
import Button from "./ui/Button.vue";
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default {
  name: "NotificationCenter",
  components: { Button, Bell, Check, X, Clock, Award, MessageSquare, FileText },
  props: {
    userRole: {
      type: String,
      default: "student",
      validator: (v) => ["student", "instructor", "admin"].includes(v),
    },
  },
  emits: ["navigate"],
  setup(props, { emit }) {
    const open = ref(false);
    const root = ref(null);
    const notifications = ref([]);
    const loading = ref(false);

    const fetchNotifications = async () => {
      try {
        loading.value = true;
        const token = localStorage.getItem('access_token');
        const response = await axios.get(`${API_URL}/api/notifications/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        
        // Handle both paginated and non-paginated responses
        const data = response.data.results || response.data;
        
        // Map backend data to frontend format
        if (Array.isArray(data)) {
          notifications.value = data.map(n => ({
            id: n.id.toString(),
            type: n.notification_type,
            title: n.title,
            message: n.message,
            time: n.time_ago,
            read: n.is_read,
            actionUrl: n.action_url,
          }));
        } else {
          console.warn('Unexpected notification data format:', data);
          notifications.value = [];
        }
      } catch (error) {
        console.error('Error fetching notifications:', error);
        notifications.value = [];
      } finally {
        loading.value = false;
      }
    };

    const unreadCount = computed(
      () => notifications.value.filter((n) => !n.read).length
    );

    const markAsRead = async (id) => {
      try {
        const token = localStorage.getItem('access_token');
        await axios.post(
          `${API_URL}/api/notifications/${id}/mark-read/`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        const idx = notifications.value.findIndex((n) => n.id === id);
        if (idx !== -1) notifications.value[idx].read = true;
      } catch (error) {
        console.error('Error marking notification as read:', error);
      }
    };

    const markAllAsRead = async () => {
      try {
        const token = localStorage.getItem('access_token');
        await axios.post(
          `${API_URL}/api/notifications/mark-all-read/`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        notifications.value.forEach((n) => (n.read = true));
      } catch (error) {
        console.error('Error marking all as read:', error);
      }
    };

    const removeNotification = async (id) => {
      try {
        const token = localStorage.getItem('access_token');
        await axios.delete(`${API_URL}/api/notifications/${id}/delete/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        notifications.value = notifications.value.filter((n) => n.id !== id);
      } catch (error) {
        console.error('Error deleting notification:', error);
      }
    };

    const getIconComponent = (type) => {
      switch (type) {
        case "grade":
          return Award;
        case "submission":
          return FileText;
        case "comment":
          return MessageSquare;
        case "assignment":
          return FileText;
        case "reminder":
          return Clock;
        default:
          return Bell;
      }
    };

    const onNotificationClick = (notification) => {
      markAsRead(notification.id);
      if (notification.actionUrl) {
        // Use router to navigate
        window.location.href = notification.actionUrl;
      }
    };

    const filteredNotifications = computed(() => {
      if (props.userRole === "student") {
        return notifications.value.filter((n) =>
          ["grade", "comment", "assignment", "reminder", "feedback"].includes(n.type)
        );
      } else if (props.userRole === "instructor") {
        return notifications.value.filter((n) =>
          ["submission", "comment"].includes(n.type)
        );
      }
      return notifications.value;
    });

    const toggleOpen = () => {
      open.value = !open.value;
      if (open.value && notifications.value.length === 0) {
        fetchNotifications();
      }
    };
    const close = () => (open.value = false);

    // click outside to close
    const onClickOutside = (e) => {
      if (root.value && !root.value.contains(e.target)) close();
    };

    onMounted(() => {
      document.addEventListener("click", onClickOutside);
      fetchNotifications(); // Fetch on mount
      
      // Poll for new notifications every 30 seconds
      const interval = setInterval(fetchNotifications, 30000);
      onBeforeUnmount(() => clearInterval(interval));
    });
    
    onBeforeUnmount(() =>
      document.removeEventListener("click", onClickOutside)
    );

    return {
      open,
      root,
      notifications,
      loading,
      unreadCount,
      markAsRead,
      markAllAsRead,
      removeNotification,
      getIconComponent,
      onNotificationClick,
      filteredNotifications,
      toggleOpen,
      close,
      fetchNotifications,
    };
  },
};
</script>

<style scoped></style>
