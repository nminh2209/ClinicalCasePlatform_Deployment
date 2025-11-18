<template>
  <svg :class="iconClasses" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
  </svg>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
  size: {
    type: String,
    default: 'w-5 h-5'
  },
  color: {
    type: String,
    default: 'text-white'
  }
})

const iconClasses = computed(() => `${props.size} ${props.color}`)
</script>
