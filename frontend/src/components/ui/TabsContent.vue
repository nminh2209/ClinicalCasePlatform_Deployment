<template>
  <div v-show="isActive"
    class="mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { computed, inject } from 'vue'

interface Props {
  value: string
}

const props = defineProps<Props>()

const tabsContext = inject('tabsContext', {
  activeTab: { value: '' }
})

const isActive = computed(() => {
  return tabsContext.activeTab.value === props.value
})
</script>
