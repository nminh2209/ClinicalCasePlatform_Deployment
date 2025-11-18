<template>
  <transition name="fade-slide">
    <div
      v-if="visible"
      :class="[
        'fixed right-6 z-50 px-4 py-3 rounded-lg shadow-lg text-md font-medium',
        toastClass
      ]"
      :style="{ top: offset }"
    >
      <div class="flex items-center gap-3">
        <span class="text-lg leading-none" ></span>
        <div>{{ message }}</div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  message: { type: String, required: true },
  type: { type: String, default: 'default' },
  duration: { type: Number, default: 3000 },
  // allows stacking by calculating different offsets when you implement it
  offset: { type: String, default: '1.5rem' }
})

const visible = ref(true)

// immediate, deterministic class based on prop
const toastClass = computed(() => {
  switch (props.type) {
    case 'success':
      return 'bg-green-600 text-white'
    case 'error':
      return 'bg-red-600 text-white'
    case 'warning':
      return 'bg-yellow-400 text-white'
    case 'info':
      return 'bg-blue-600 text-white'
    default:
      return 'bg-gray-800 text-white'
  }
})


onMounted(() => {
  setTimeout(() => {
    visible.value = false
  }, props.duration)
})
</script>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.28s ease, transform 0.28s ease;
}
.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
.fixed {
  min-width: 200px;
  max-width: 420px;
}
</style>
