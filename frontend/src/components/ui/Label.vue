<template>
  <label :for="htmlFor" :class="labelClasses">
    <slot />
  </label>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
  htmlFor: {
    type: String,
    default: ''
  },
  class: {
    type: String,
    default: ''
  }
})

const labelClasses = computed(() => {
  const baseClasses = 'text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70'

  return [baseClasses, props.class].filter(Boolean).join(' ')
})
</script>
