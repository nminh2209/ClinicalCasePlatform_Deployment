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

export default {
  name: "NotificationCenter",
  components: { Button, Bell, Check, X, Clock, Award, MessageSquare, FileText },
  props: {
    userRole: {
      type: String,
      default: "student",
      validator: (v) => ["student", "teacher", "admin"].includes(v),
    },
  },
  emits: ["navigate"],
  setup(props, { emit }) {
    const open = ref(false);
    const root = ref(null);

    const notifications = ref([
      {
        id: "1",
        type: "grade",
        title: "Bệnh án đã được chấm điểm",
        message:
          "Bài nộp của bạn cho 'Nhồi máu cơ tim cấp' đã được chấm điểm: 92%",
        time: "2 giờ trước",
        read: false,
      },
      {
        id: "2",
        type: "comment",
        title: "Nhận xét mới",
        message: "BS. Trần Văn Minh đã nhận xét về chẩn đoán phân biệt của bạn",
        time: "5 giờ trước",
        read: false,
      },
      {
        id: "3",
        type: "assignment",
        title: "Bệnh án mới được giao",
        message: "Bệnh án mới 'Suy thận mạn' đã được giao cho bạn",
        time: "1 ngày trước",
        read: false,
      },
      {
        id: "4",
        type: "reminder",
        title: "Nhắc nhở hạn nộp",
        message:
          "Bệnh án 'Quản lý Đái tháo đường Type 2' sẽ hết hạn trong 2 ngày",
        time: "1 ngày trước",
        read: true,
      },
      {
        id: "5",
        type: "submission",
        title: "Sinh viên nộp bài",
        message:
          "Nguyễn Văn A đã nộp ghi chú cho bệnh án 'Nhồi máu cơ tim cấp'",
        time: "3 giờ trước",
        read: props.userRole === "student",
      },
    ]);

    const unreadCount = computed(
      () => notifications.value.filter((n) => !n.read).length
    );

    const markAsRead = (id) => {
      const idx = notifications.value.findIndex((n) => n.id === id);
      if (idx !== -1) notifications.value[idx].read = true;
    };

    const markAllAsRead = () => {
      notifications.value.forEach((n) => (n.read = true));
    };

    const removeNotification = (id) => {
      notifications.value = notifications.value.filter((n) => n.id !== id);
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
        emit("navigate", notification.actionUrl);
      }
    };

    const filteredNotifications = computed(() => {
      if (props.userRole === "student") {
        return notifications.value.filter((n) =>
          ["grade", "comment", "assignment", "reminder"].includes(n.type)
        );
      } else if (props.userRole === "teacher") {
        return notifications.value.filter((n) =>
          ["submission", "comment"].includes(n.type)
        );
      }
      return notifications.value;
    });

    const toggleOpen = () => (open.value = !open.value);
    const close = () => (open.value = false);

    // click outside to close
    const onClickOutside = (e) => {
      if (root.value && !root.value.contains(e.target)) close();
    };

    onMounted(() => document.addEventListener("click", onClickOutside));
    onBeforeUnmount(() =>
      document.removeEventListener("click", onClickOutside)
    );

    return {
      open,
      root,
      notifications,
      unreadCount,
      markAsRead,
      markAllAsRead,
      removeNotification,
      getIconComponent,
      onNotificationClick,
      filteredNotifications,
      toggleOpen,
      close,
    };
  },
};
</script>

<style scoped></style>
