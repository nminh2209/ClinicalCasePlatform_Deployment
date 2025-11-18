<template>
  <div :class="tabsListClasses">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { computed, inject } from 'vue'

type Orientation = 'horizontal' | 'vertical'

const tabsContext = inject<{ orientation: Orientation }>('tabsContext', {
  orientation: 'horizontal'
})

const tabsListClasses = computed(() => {
  const baseClasses = 'rounded-lg bg-gray-100 p-1 text-muted-foreground'
  const orientationClasses: Record<Orientation, string> = {
    horizontal: 'inline-flex items-center justify-center',
    vertical: 'flex flex-col items-stretch'
  }

  return `${baseClasses} ${orientationClasses[tabsContext.orientation]}`
})
</script>
