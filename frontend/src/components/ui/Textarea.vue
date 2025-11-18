<template>
  <div>
    <textarea :class="textareaClasses" :disabled="disabled" :placeholder="placeholder" :value="modelValue"
      @input="handleInput" v-bind="$attrs" />
    <p v-if="error" class="mt-1 text-sm text-red-600">
      {{ error }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  modelValue?: string
  disabled?: boolean
  placeholder?: string
  variant?: 'default' | 'error'
  error?: string
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  disabled: false,
  placeholder: '',
  variant: 'default',
  error: ''
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const handleInput = (event: Event) => {
  const target = event.target as HTMLTextAreaElement
  emit('update:modelValue', target.value)
}

const textareaClasses = computed(() => {
  const baseClasses = 'flex min-h-[80px] w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:cursor-not-allowed disabled:opacity-50'

  const variantClasses = {
    default: 'border-gray-300',
    error: 'border-red-500 focus:ring-red-500'
  }

  return `${baseClasses} ${variantClasses[props.variant]}`
})
</script>
