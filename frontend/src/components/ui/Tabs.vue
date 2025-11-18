<template>
  <div :class="tabsClasses">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { computed, provide, ref } from 'vue'

interface Props {
  defaultValue?: string
  modelValue?: string
  orientation?: 'horizontal' | 'vertical'
}

const props = withDefaults(defineProps<Props>(), {
  defaultValue: '',
  modelValue: '',
  orientation: 'horizontal'
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const activeTab = ref(props.modelValue || props.defaultValue)

const setActiveTab = (value: string) => {
  activeTab.value = value
  emit('update:modelValue', value)
}

// Provide context for child components
provide('tabsContext', {
  activeTab,
  setActiveTab,
  orientation: props.orientation
})

const tabsClasses = computed(() => {
  const baseClasses = 'w-full'
  const orientationClasses = {
    horizontal: 'space-y-2',
    vertical: 'flex space-x-2'
  }

  return `${baseClasses} ${orientationClasses[props.orientation]}`
})
</script>
