<template>
  <div class="language-switcher">
    <div class="language-toggle">
      <button 
        @click="setLanguage('vi')"
        :class="['lang-button', { active: currentLanguage === 'vi' }]"
        type="button"
      >
        <span class="flag">🇻🇳</span>
        <span class="lang-text">VI</span>
      </button>
      <button 
        @click="setLanguage('en')"
        :class="['lang-button', { active: currentLanguage === 'en' }]"
        type="button"
      >
        <span class="flag">🇺🇸</span>
        <span class="lang-text">EN</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">  
import { ref, watch } from 'vue'
import { useLanguage } from '@/composables/useLanguage'

const { setLanguage: setLang, currentLang } = useLanguage()

const currentLanguage = ref(currentLang.value)

const setLanguage = (lang: string) => {
  currentLanguage.value = lang
  setLang(lang)
}

watch(currentLang, (newLang) => {
  currentLanguage.value = newLang
})
</script>

<style scoped>
.language-switcher {
  position: relative;
}

.language-toggle {
  display: inline-flex;
  background: #f3f4f6;
  border-radius: 10px;
  padding: 0.25rem;
  gap: 0.25rem;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.lang-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.875rem;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
  font-size: 0.875rem;
  color: #6b7280;
}

.lang-button:hover {
  background: rgba(255, 255, 255, 0.5);
  color: #374151;
}

.lang-button.active {
  background: white;
  color: #1f2937;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.flag {
  font-size: 1.125rem;
  line-height: 1;
}

.lang-text {
  font-weight: 600;
  letter-spacing: 0.025em;
}

.lang-button.active .lang-text {
  color: #3b82f6;
}
</style>
