<template>
  <div class="min-h-screen bg-gray-50">
    <CreateCaseWizard :student-department="'General Medicine'" @close="handleClose" @complete="handleComplete" />
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import CreateCaseWizard from '@/components/CreateCaseWizard.vue'
import { requireRoles } from '@/composables/useAuthorize'
import { useCasesStore } from '@/stores/cases'

const router = useRouter()
requireRoles(['student', 'instructor'])

const handleClose = () => {
  router.push('/cases')
}

const handleComplete = async (result: { caseId: number; caseData: any }) => {
  console.log('Case created:', result)
  // Fetch updated cases list to ensure the new case appears
  const casesStore = useCasesStore()
  await casesStore.fetchCases()
  // Navigate to the newly created case
  if (result.caseId) {
    router.push(`/cases/${result.caseId}`)
  } else {
    router.push('/cases')
  }
}
</script>
