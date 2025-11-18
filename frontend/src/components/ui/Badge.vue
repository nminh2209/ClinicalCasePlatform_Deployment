<template>
  <div :class="badgeClasses">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'default' | 'secondary' | 'destructive' | 'outline' | 'success' | 'warning'
  size?: 'default' | 'sm' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  size: 'default'
})

const badgeClasses = computed(() => {
  const baseClasses = 'inline-flex items-center rounded-lg border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2'

  const variantClasses = {
    default: 'border-transparent bg-primary text-primary-foreground hover:bg-primary/80',
    secondary: 'border-transparent bg-blue-400 text-white hover:bg-secondary/80',
    destructive: 'border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80',
    outline: 'text-foreground',
    success: 'border-transparent bg-green-500 text-white hover:bg-green-600',
    warning: 'border-transparent bg-yellow-500 text-white hover:bg-yellow-600'
  }

  const sizeClasses = {
    default: 'px-2.5 py-0.5 text-xs',
    sm: 'px-2 py-0.5 text-xs',
    lg: 'px-3 py-1 text-sm'
  }

  return `${baseClasses} ${variantClasses[props.variant]} ${sizeClasses[props.size]}`
})
</script>
