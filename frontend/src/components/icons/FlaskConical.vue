<template>
  <svg :width="size" :height="size" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"
    :class="props.class">
    <path
      d="M10 2L14 2C14.5523 2 15 2.44772 15 3V5.12602C15 5.57006 15.2107 5.98512 15.5858 6.22253L19.4142 8.77747C19.7893 9.01488 20 9.42994 20 9.87398V13C20 13.5523 19.5523 14 19 14H5C4.44772 14 4 13.5523 4 13V9.87398C4 9.42994 4.21071 9.01488 4.58579 8.77747L8.41421 6.22253C8.78929 5.98512 9 5.57006 9 5.12602V3C9 2.44772 9.44772 2 10 2Z"
      stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
    <path d="M9 14V20C9 20.5523 9.44772 21 10 21H14C14.5523 21 15 20.5523 15 20V14" stroke="currentColor"
      stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
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
