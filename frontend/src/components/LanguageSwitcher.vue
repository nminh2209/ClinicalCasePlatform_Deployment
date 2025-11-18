<template>
  <div class="language-switcher">
    <select v-model="currentLanguage" @change="handleLanguageChange" class="language-select">
      <option value="vi">🇻🇳 Tiếng Việt</option>
      <option value="en">🇺🇸 English</option>
    </select>
  </div>
</template>

<script setup lang="ts">  
import { ref, watch } from 'vue'
import { useLanguage } from '@/composables/useLanguage'

const { setLanguage, currentLang } = useLanguage()

const currentLanguage = ref(currentLang.value)

const handleLanguageChange = () => {
  setLanguage(currentLanguage.value)
}

watch(currentLang, (newLang) => {
  currentLanguage.value = newLang
})
</script>

<style scoped>
.language-switcher {
  position: relative;
}

.language-select {
  padding: 0.5rem 0.75rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  font-size: 0.875rem;
  color: #424242;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 120px;
}

.language-select:focus {
  outline: none;
  border-color: #2196f3;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.1);
}

.language-select:hover {
  border-color: #bdbdbd;
}
</style>
