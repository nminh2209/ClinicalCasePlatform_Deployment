<template>
  <svg :width="size" :height="size" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"
    :class="props.class">
    <path d="M9.75 9.75L2.25 12L9.75 14.25L12 21.75L14.25 14.25L21.75 12L14.25 9.75L12 2.25L9.75 9.75Z"
      stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
    <path d="M6.75 6.75L5.25 5.25" stroke="currentColor" stroke-width="2" stroke-linecap="round"
      stroke-linejoin="round" />
    <path d="M18.75 6.75L17.25 5.25" stroke="currentColor" stroke-width="2" stroke-linecap="round"
      stroke-linejoin="round" />
    <path d="M6.75 17.25L5.25 18.75" stroke="currentColor" stroke-width="2" stroke-linecap="round"
      stroke-linejoin="round" />
    <path d="M18.75 17.25L17.25 18.75" stroke="currentColor" stroke-width="2" stroke-linecap="round"
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
