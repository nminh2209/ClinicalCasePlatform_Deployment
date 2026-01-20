<template>
  <div class="min-h-screen bg-gray-50 ">
    <!-- Student View: Edit case and submit -->
    <CreateCase v-if="isStudent" :caseId="id" @navigate="handleNavigate" />

    <!-- Instructor View: Grade the case -->
    <InstructorGrading v-else-if="isInstructor" :caseId="id" @navigate="handleNavigate" />

    <!-- Admin/Other: Show student view by default -->
    <CreateCase v-else :caseId="id" @navigate="handleNavigate" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import CreateCase from '@/components/CaseNotes.vue'
import InstructorGrading from '@/components/InstructorGrading.vue'
import { requireRoles } from '@/composables/useAuthorize'

type UserRole = 'student' | 'instructor' | 'admin'

interface User {
  role?: UserRole
}

interface AuthStore {
  user: User | null
}

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore() as AuthStore

// Get case ID from route params
const id = computed(() => route.params.id as string)

// Check user role
const isStudent = computed(() => authStore.user?.role === 'student')
const isInstructor = computed(() => authStore.user?.role === 'instructor')

// Component-level guard (students + instructors)
requireRoles(['student', 'instructor'])

const handleNavigate = (destination: 'dashboard' | string) => {
  if (destination === 'dashboard') {
    router.push('/home')
  } else {
    router.push(destination)
  }
}
</script>
