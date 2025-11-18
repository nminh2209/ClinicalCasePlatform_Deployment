<template>
  <button :class="triggerClasses" @click="setActiveTab" :disabled="disabled">
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed, inject } from 'vue'

interface Props {
  value: string
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false
})

const tabsContext = inject('tabsContext', {
  activeTab: { value: '' },
  setActiveTab: (value: string) => { },
  orientation: 'horizontal'
})

const setActiveTab = () => {
  if (!props.disabled) {
    tabsContext.setActiveTab(props.value)
  }
}

const triggerClasses = computed(() => {
  const baseClasses = 'inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50'
  // More prominent active styling to make selected tab obvious
  const activeClasses = 'bg-primary/10 text-primary shadow-sm ring-1 ring-primary/20'
  const inactiveClasses = 'hover:bg-muted/50'

  const isActive = tabsContext.activeTab.value === props.value

  return `${baseClasses} ${isActive ? activeClasses : inactiveClasses}`
})
</script>
