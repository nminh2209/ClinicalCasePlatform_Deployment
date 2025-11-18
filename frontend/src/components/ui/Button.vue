<template>
  <button :class="[buttonClasses, $attrs.class]" :disabled="disabled" v-bind="$attrs" @click="$emit('click', $event)">
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const variantOptions = ['default', 'primary', 'secondary', 'outline', 'ghost', 'destructive'] as const
const sizeOptions = ['default', 'sm', 'lg', 'icon'] as const

type Variant = typeof variantOptions[number]
type Size = typeof sizeOptions[number]

const props = defineProps<{
  variant?: Variant
  size?: Size
  disabled?: boolean
}>()

defineEmits(['click'])

const buttonClasses = computed(() => {
  const baseClasses = 'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50'

  const variantClasses = {
    default: 'bg-primary text-primary-foreground hover:bg-primary/90',
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
    outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
    ghost: 'hover:bg-accent hover:text-accent-foreground',
    destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90'
  }

  const sizeClasses = {
    default: 'h-10 px-4 py-2',
    sm: 'h-9 rounded-md px-3',
    lg: 'h-11 rounded-md px-8',
    icon: 'h-10 w-10'
  }

  const variant = props.variant ?? 'default'
  const size = props.size ?? 'default'

  return `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]}`
})
</script>
