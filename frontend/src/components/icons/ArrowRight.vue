<template>
  <svg :width="size" :height="size" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"
    :class="props.class">
    <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round"
      stroke-linejoin="round" />
  </svg>
</template>

<script setup lang="ts">
interface Props {
  size?: number | string
  class?: string
}

const props = withDefaults(defineProps<Props>(), {
  size: 24,
  class: ''
})
</script>
