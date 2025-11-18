<template>
  <div class="min-h-screen bg-gray-50">
    <CreateCaseWizard :student-department="'General Medicine'" @close="handleClose" @complete="handleComplete" />
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import CreateCaseWizard from '@/components/CreateCaseWizard.vue'
import { requireRoles } from '@/composables/useAuthorize'

const router = useRouter()
requireRoles(['student', 'instructor'])

const handleClose = () => {
  router.push('/cases')
}

const handleComplete = (result: string) => {
  console.log('Case created:', result)
  router.push('/cases')
}
</script>
