<template>
  <input :type="type" :class="inputClasses" :disabled="disabled" :placeholder="placeholder" :value="modelValue"
    @input="handleInput" @blur="$emit('blur', $event)" @focus="$emit('focus', $event)" />
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  type?: string
  modelValue?: number | string
  placeholder?: string
  disabled?: boolean
  class?: string
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  disabled: false
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  blur: [event: FocusEvent]
  focus: [event: FocusEvent]
}>()

const inputClasses = computed(() => {
  const baseClasses = 'flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-gray-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50'

  return [baseClasses, props.class].filter(Boolean).join(' ')
})

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}
</script>
