<template>
  <div
    v-if="open"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    @click="$emit('update:open', false)"
  >
    <div class="bg-white rounded-lg p-6 w-full max-w-md m-4" @click.stop>
      <div class="mb-4">
        <h2 class="text-xl font-bold">Tạo liên kết khách mời</h2>
        <p class="text-gray-600 text-sm">
          Tạo liên kết truy cập cho người không có tài khoản
        </p>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">
              Tên khách mời
            </label>
            <InputText
              v-model="form.guestName"
              type="text"
              fluid
              placeholder="Nhập tên khách mời"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">
              Email khách mời
            </label>
            <InputText
              v-model="form.guestEmail"
              type="email"
              fluid
              placeholder="Nhập email khách mời"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">
              Thời gian truy cập
            </label>
            <Select
              v-model="form.duration"
              :options="durationOptions"
              optionLabel="label"
              optionValue="value"
              fluid
              placeholder="Chọn thời hạn"
            />
          </div>

          <div v-if="form.duration === 'custom'">
            <label class="block text-sm font-medium mb-1"> Ngày hết hạn </label>
            <input
              type="datetime-local"
              v-model="form.customExpiry"
              class="w-full border rounded-md p-2"
              :min="new Date().toISOString().slice(0, 16)"
            />
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">
              Giới hạn truy cập (tuỳ chọn)
            </label>
            <InputNumber
              v-model.number="form.accessLimit"
              type="number"
              fluid
              showButtons
              placeholder="Số lần truy cập tối đa"
              :min="1"
            />
            <p class="text-xs text-gray-500 mt-1">
              Để trống nếu không giới hạn
            </p>
          </div>

          <div class="flex items-center space-x-2">
            <Checkbox v-model="form.sendEmail" id="send-email" binary />
            <label for="send-email" class="text-sm">
              Gửi email thông báo cho khách mời
            </label>
          </div>

          <div v-if="form.sendEmail">
            <label class="block text-sm font-medium mb-1">
              Tin nhắn (tuỳ chọn)
            </label>
            <Textarea
              v-model="form.message"
              fluid
              placeholder="Thêm tin nhắn trong email..."
              rows="3"
            ></Textarea>
          </div>
        </div>

        <div class="flex justify-end space-x-2 mt-6">
          <Button
            type="button"
            @click="$emit('update:open', false)"
          >
            Huỷ
          </Button>
          <Button
            type="submit"
            :disabled="!canSubmit || loading"
          >
            <span v-if="loading"><i class="pi pi-hourglass"></i></span>
            Tạo liên kết
          </Button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useToast } from "@/composables/useToast";
import { sharingService } from "@/services/sharing";
import type { GuestAccess } from "@/services/sharing";
import InputText from "primevue/inputtext";
import Select from "primevue/select";
import InputNumber from "primevue/inputnumber";
import Checkbox from "primevue/checkbox";
import Textarea from "primevue/textarea";
import Button from "primevue/button";

const durationOptions = [
  { label: "1 giờ", value: "1" },
  { label: "6 giờ", value: "6" },
  { label: "1 ngày", value: "24" },
  { label: "1 tuần", value: "168" },
  { label: "1 tháng", value: "720" },
  { label: "Tùy chỉnh", value: "custom" },
];

interface Props {
  open: boolean;
  caseId: number;
}

interface Emits {
  (event: "update:open", value: boolean): void;
  (event: "guest-created", guest: GuestAccess): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const toast = useToast();

const loading = ref(false);

const form = ref({
  guestName: "",
  guestEmail: "",
  duration: "24", // hours
  customExpiry: "",
  accessLimit: null as number | null,
  sendEmail: true,
  message: "",
});

const canSubmit = computed(() => {
  return (
    form.value.guestName &&
    form.value.guestEmail &&
    (form.value.duration !== "custom" || form.value.customExpiry)
  );
});

// Reset form when modal opens/closes
watch(
  () => props.open,
  (isOpen) => {
    if (!isOpen) {
      resetForm();
    }
  },
);

const resetForm = () => {
  form.value = {
    guestName: "",
    guestEmail: "",
    duration: "24",
    customExpiry: "",
    accessLimit: null,
    sendEmail: true,
    message: "",
  };
};

const calculateExpiryDate = (): string => {
  if (form.value.duration === "custom") {
    return form.value.customExpiry;
  }

  const hours = parseInt(form.value.duration);
  const expiryDate = new Date();
  expiryDate.setHours(expiryDate.getHours() + hours);

  return expiryDate.toISOString();
};

const handleSubmit = async () => {
  if (!canSubmit.value) return;

  loading.value = true;
  try {
    const guestData: any = {
      case_id: props.caseId,
      guest_name: form.value.guestName,
      guest_email: form.value.guestEmail,
      expires_at: calculateExpiryDate(),
      access_limit: form.value.accessLimit || undefined,
      send_email: form.value.sendEmail,
      message: form.value.message || undefined,
    };

    const guest = await sharingService.createGuestAccess(
      props.caseId,
      guestData,
    );

    toast.toast.success("Đã tạo liên kết khách mời thành công!");

    emit("guest-created", guest);
    emit("update:open", false);
  } catch (error) {
    console.error("Failed to create guest access:", error);
    toast.toast.error("Không thể tạo liên kết khách mời");
  } finally {
    loading.value = false;
  }
};
</script>
