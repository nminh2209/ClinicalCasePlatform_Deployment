<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-blue-100 p-4">
    <div class="w-full max-w-md">
      <div class="bg-white rounded-xl shadow-xl p-8 md:p-10 relative">
        <!-- Language Switcher -->
        <div class="absolute top-4 right-4">
          <LanguageSwitcher />
        </div>

        <!-- Logo and Title -->
        <div class="flex flex-col items-center mb-8">
          <div class="w-16 h-16 bg-primary rounded-full flex items-center justify-center mb-4">
            <Activity class="w-8 h-8 text-white" />
          </div>
          <h1 class="text-gray-800 mb-2">{{ t('login.title') }}</h1>
          <p class="text-muted-foreground">{{ t('login.subtitle') }}</p>
        </div>

        <!-- Single Login Form -->
        <form @submit.prevent="handleSubmit" class="space-y-5">
          <div class="space-y-2">
            <Label htmlFor="email">{{ t('login.username') }}</Label>
            <Input id="email" v-model="email" type="email" :placeholder="t('login.placeholder.username')" class="h-11"
              required />
          </div>

          <div class="space-y-2">
            <Label htmlFor="password">{{ t('login.password') }}</Label>
            <Input id="password" v-model="password" type="password" :placeholder="t('login.placeholder.password')"
              class="h-11" required />
          </div>

          <div v-if="error" class="text-red-500 text-sm bg-red-50 p-3 rounded-lg">
            {{ t('login.error.failedLogin') }}
          </div>

          <div class="flex items-center justify-end">
            <a href="#" class="text-primary hover:underline">
              {{ t('login.forgot') }}
            </a>
          </div>

          <Button type="submit" class="w-full h-11 text-grey hover:bg-blue-600" :disabled="loading">
            <span v-if="loading">Đang đăng nhập...</span>
            <span v-else>{{ t('login.button') }}</span>
          </Button>
        </form>

        <div class="mt-6 text-center">
          <p class="text-muted-foreground">
            {{ t('login.copyright') }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useLanguage } from '@/composables/useLanguage'
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Label from '@/components/ui/Label.vue'
import { Activity } from '@/components/icons'

const router = useRouter()
const authStore = useAuthStore()
const { t } = useLanguage()

const email = ref("")
const password = ref("")
const error = ref("")
const loading = ref(false)

const handleSubmit = async () => {
  loading.value = true
  error.value = ""

  try {
    await authStore.login(email.value, password.value)
    // Redirect to home to show role-based dashboard
    router.push('/home')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Đăng nhập thất bại. Vui lòng kiểm tra thông tin đăng nhập.'
  } finally {
    loading.value = false
  }
}
</script>
