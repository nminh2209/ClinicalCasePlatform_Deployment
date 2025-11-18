import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'

/**
 * Component-level authorization helper.
 * Usage: call requireRoles(['student','instructor']) inside <script setup>.
 * The check runs onMounted and will redirect + show a toast when unauthorized.
 */
export function requireRoles(requiredRoles: string[]) {
  const router = useRouter()
  const authStore = useAuthStore()
  const { toast } = useToast()

  onMounted(() => {
    // If not authenticated, redirect to login
    if (!authStore?.isAuthenticated) {
      toast.info('Please log in to continue.')
      router.push('/login')
      return
    }

    const userRole = authStore.user?.role
    if (!userRole) {
      toast.info('Your session is expired. Please log in again.')
      router.push('/login')
      return
    }

    if (!requiredRoles.includes(userRole)) {
      console.warn(`Component guard: access denied for role ${userRole} (required: ${requiredRoles.join(',')})`)
      toast.error('Access denied: You do not have permission to view this page.')
      router.push('/home')
      return
    }
  })
}
