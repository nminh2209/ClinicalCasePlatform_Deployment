<template>
  <div class="flex flex-col h-full">
    <!-- Scrollable template selection area -->
    <div class="flex-1 overflow-y-auto pr-2 -mr-2">
      <div class="space-y-6">
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-12">
          <p class="text-gray-500">{{ t('createCase.loadingTemplates') }}</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="text-center py-12">
          <p class="text-red-500">{{ t('createCase.templateLoadError') }}: {{ error }}</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="caseTemplates.length === 0" class="text-center py-12">
          <p class="text-gray-500">{{ t('createCase.noTemplates') }}</p>
        </div>

        <!-- Templates Grid -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-2 max-h-[50vh] overflow-y-auto">
          <Card v-for="template in caseTemplates" :key="template.id"
            class="cursor-pointer transition-all duration-200 hover:shadow-lg"
            :class="{ 'ring-2 ring-blue-500 bg-blue-50': selectedTemplate?.id === template.id }"
            @click="selectTemplate(template)">
            <div class="p-6">
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center space-x-3">
                  <div class="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
                    <component :is="getSpecialtyIcon(template.specialty)" class="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <h3 class="font-semibold text-gray-900">{{ translateTemplateField(template.name) }}</h3>
                    <p class="text-sm text-gray-500">{{ translateSpecialty(template.specialty) }}</p>
                  </div>
                </div>
                <div v-if="selectedTemplate?.id === template.id"
                  class="w-6 h-6 rounded-full bg-blue-500 flex items-center justify-center">
                  <CheckIcon class="w-4 h-4 text-white" />
                </div>
              </div>

              <p class="text-gray-600 text-sm mb-4">{{ template.description || t('createCase.noDescriptionAvailable') }}</p>

              <div class="flex flex-wrap gap-2 mb-3">
                <Badge v-if="template.department_name" variant="secondary" class="text-xs">
                  {{ translateDepartment(template.department_name) }}
                </Badge>
                <Badge v-if="template.specialty" variant="outline" class="text-xs">
                  {{ translateSpecialty(template.specialty) }}
                </Badge>
              </div>

              <div class="mt-4 pt-4 border-t border-gray-200">
                <div class="text-sm text-gray-500">
                  <span>{{ t('createCase.createdBy') }}: {{ template.created_by_name }}</span>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>

    <!-- template preview at bottom -->
    <div v-if="selectedTemplate" class="mt-6 pt-6 border-t flex-shrink-0">
      <Card class="bg-blue-50 border-blue-200">
        <div class="p-6">
          <h3 class="font-semibold text-lg text-gray-900 mb-4">
            {{ t('createCase.templatePreview') }}
          </h3>

          <div class="space-y-6">
            <!-- Template Details - Full Row -->
            <div>
              <h4 class="font-medium text-gray-900 mb-2">{{ t('createCase.templateDetails') }}</h4>
              <dl class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div class="flex flex-col">
                  <dt class="text-gray-600 text-sm">{{ t('createCase.specialty') }}</dt>
                  <dd class="font-medium">{{ translateSpecialty(selectedTemplate.specialty) || t('createCase.notApplicable') }}</dd>
                </div>
                <div class="flex flex-col">
                  <dt class="text-gray-600 text-sm">{{ t('createCase.department') }}</dt>
                  <dd class="font-medium">{{ translateDepartment(selectedTemplate.department_name) || t('createCase.notApplicable') }}</dd>
                </div>
                <div class="flex flex-col">
                  <dt class="text-gray-600 text-sm">{{ t('createCase.createdBy') }}</dt>
                  <dd class="font-medium">{{ selectedTemplate.created_by_name || t('createCase.notApplicable') }}</dd>
                </div>
              </dl>
            </div>

            <!-- Sections and Required Fields - Side by Side -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 class="font-medium text-gray-900 mb-2">{{ t('createCase.sections') }}</h4>
                <ul class="space-y-1">
                  <li v-for="section in selectedTemplate.fields_schema?.sections || []" :key="section"
                    class="text-sm text-gray-600 flex items-start">
                    <CheckCircleIcon class="w-4 h-4 text-green-500 mr-2 mt-0.5 shrink-0" />
                    {{ translateFieldName(section) }}
                  </li>
                </ul>
                <div v-if="!selectedTemplate.fields_schema?.sections?.length" class="text-sm text-gray-500">
                  {{ t('createCase.noSectionsDefined') }}
                </div>
              </div>

              <div v-if="selectedTemplate.fields_schema?.required_fields?.length">
                <h4 class="font-medium text-gray-900 mb-2">{{ t('createCase.requiredFields') }}</h4>
                <ul class="space-y-1">
                  <li v-for="field in selectedTemplate.fields_schema.required_fields" :key="field"
                    class="text-sm text-gray-600 flex items-start">
                    <CheckCircleIcon class="w-4 h-4 text-red-500 mr-2 mt-0.5 shrink-0" />
                    {{ translateFieldName(field) }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, type Ref } from 'vue'
import { useI18n } from 'vue-i18n'
import Card from '@/components/ui/Card.vue'
import Badge from '@/components/ui/Badge.vue'
import { 
  Activity as ActivityIcon, 
  CheckIcon, 
  CheckCircleIcon,
  Stethoscope,
  FlaskConical,
  Eye,
  User
} from '@/components/icons'
import { type CaseTemplate, useCaseTemplates } from '@/composables/useCaseTemplates'
import { useBackendTranslations } from '@/composables/useBackendTranslations'
import { shallowRef, type Component } from 'vue'

const { t } = useI18n()
const { translateSpecialty, translateDepartment } = useBackendTranslations()

const { caseTemplates, loading, error, fetchCaseTemplates } = useCaseTemplates()

// Map specialties to icons
const getSpecialtyIcon = (specialty: string | null | undefined): Component => {
  if (!specialty) return ActivityIcon
  
  const specialtyLower = specialty.toLowerCase()
  
  // Map Vietnamese specialties to icons
  if (specialtyLower.includes('tiêu hóa') || specialtyLower.includes('digestive') || specialtyLower.includes('gastro')) {
    return FlaskConical // Digestive/lab work
  } else if (specialtyLower.includes('thần kinh') || specialtyLower.includes('neuro') || specialtyLower.includes('brain')) {
    return Eye // Neurology
  } else if (specialtyLower.includes('ngoại') || specialtyLower.includes('surgery') || specialtyLower.includes('surgical')) {
    return Stethoscope // Surgery
  } else if (specialtyLower.includes('nội') || specialtyLower.includes('internal') || specialtyLower.includes('medicine')) {
    return Stethoscope // Internal medicine
  } else if (specialtyLower.includes('hô hấp') || specialtyLower.includes('respiratory') || specialtyLower.includes('pulmonary')) {
    return ActivityIcon // Respiratory (Activity = heartbeat/breathing)
  } else if (specialtyLower.includes('tim') || specialtyLower.includes('cardio') || specialtyLower.includes('heart')) {
    return ActivityIcon // Cardiology
  } else if (specialtyLower.includes('nhi') || specialtyLower.includes('pediatric') || specialtyLower.includes('child')) {
    return User // Pediatrics
  }
  
  return ActivityIcon // Default
}

const props = defineProps({
  caseData: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:caseData'])

const selectedTemplate = computed({
  get: () => props.caseData.template,
  set: (value: CaseTemplate | null) => emit('update:caseData', { ...props.caseData, template: value })
})

const selectTemplate = (template: CaseTemplate) => {
  selectedTemplate.value = template
}

const translateTemplateField = (value: string | null | undefined): string => {
  if (!value) return ''
  // Return value as-is (it's the template name from backend)
  return value
}

const translateFieldName = (fieldName: string): string => {
  if (fieldName === "chief_complaint") {
    return t('createCase.chief_complaint')
  }
  try {
    // Try to translate the field name (convert snake_case to camelCase for i18n key)
    const camelCaseKey = fieldName
      .split('_')
      .map((word, index) => {
        if (index === 0) return word
        return word.charAt(0).toUpperCase() + word.slice(1)
      })
      .join('')
    
    const translationKey = `createCase.${camelCaseKey}`
    const translated = t(translationKey)
    
    // If translation key exists and is different from the key itself, return translated
    if (translated !== translationKey) {
      return translated
    }

    // Fallback: format as Title Case
    return fieldName
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  } catch {
    // If translation fails, format as Title Case
    return fieldName
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  }
}

const formatSectionName = (section: string) => {
  // Convert snake_case to Title Case
  return section
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

onMounted(() => {
  fetchCaseTemplates()
})
</script>
