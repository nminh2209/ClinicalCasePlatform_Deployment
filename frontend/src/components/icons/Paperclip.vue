<template>
  <svg :width="size" :height="size" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"
    :class="props.class">
    <path
      d="M21.44 11.05L12.25 20.24C11.1242 21.3658 9.59718 21.9983 8.005 21.9983C6.41282 21.9983 4.88584 21.3658 3.76 20.24C2.63416 19.1142 2.00166 17.5872 2.00166 15.995C2.00166 14.4028 2.63416 12.8758 3.76 11.75L12.33 3.18C13.0806 2.42944 14.0991 2.00758 15.165 2.00758C16.2309 2.00758 17.2494 2.42944 18 3.18C18.7506 3.93056 19.1724 4.94905 19.1724 6.015C19.1724 7.08095 18.7506 8.09944 18 9.85L9.41 18.44C9.03472 18.8153 8.52573 19.026 8 19.026C7.47427 19.026 6.96528 18.8153 6.59 18.44C6.21472 18.0647 6.00403 17.5557 6.00403 17.03C6.00403 16.5043 6.21472 15.9953 6.59 15.62L15.07 7.14"
      stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
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
