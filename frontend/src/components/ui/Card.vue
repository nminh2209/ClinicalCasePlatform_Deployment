<template>
  <div :class="cardClasses">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'default' | 'elevated' | 'outlined'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default'
})

const cardClasses = computed(() => {
  const baseClasses = 'rounded-lg border bg-card text-card-foreground shadow-sm'

  const variantClasses = {
    default: 'border-border',
    elevated: 'border-border shadow-md',
    outlined: 'border-2 border-border'
  }

  return `${baseClasses} ${variantClasses[props.variant]}`
})
</script>
