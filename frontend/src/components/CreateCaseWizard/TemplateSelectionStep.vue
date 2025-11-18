<template>
  <div class="flex flex-col h-full">
    <!-- Scrollable template selection area -->
    <div class="flex-1 overflow-y-auto pr-2 -mr-2">
      <div class="space-y-6">
        <div class="text-center">
          <h2 class="text-2xl font-bold text-gray-900 mb-2">
            {{ $t('createCase.selectTemplate') }}
          </h2>
          <p class="text-gray-600">
            {{ $t('createCase.templateDescription') }}
          </p>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-12">
          <p class="text-gray-500">{{ $t('createCase.loadingTemplates') || 'Đang tải mẫu...' }}</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="text-center py-12">
          <p class="text-red-500">{{ error }}</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="caseTemplates.length === 0" class="text-center py-12">
          <p class="text-gray-500">{{ $t('createCase.noTemplates') || 'Không có mẫu nào' }}</p>
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
                    <ActivityIcon class="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <h3 class="font-semibold text-gray-900">{{ template.name }}</h3>
                    <p class="text-sm text-gray-500">{{ template.specialty }}</p>
                  </div>
                </div>
                <div v-if="selectedTemplate?.id === template.id"
                  class="w-6 h-6 rounded-full bg-blue-500 flex items-center justify-center">
                  <CheckIcon class="w-4 h-4 text-white" />
                </div>
              </div>

              <p class="text-gray-600 text-sm mb-4">{{ template.description || 'No description available' }}</p>

              <div class="flex flex-wrap gap-2 mb-3">
                <Badge v-if="template.department_name" variant="secondary" class="text-xs">
                  {{ template.department_name }}
                </Badge>
                <Badge v-if="template.specialty" variant="outline" class="text-xs">
                  {{ template.specialty }}
                </Badge>
              </div>

              <div class="mt-4 pt-4 border-t border-gray-200">
                <div class="text-sm text-gray-500">
                  <span>{{ t('createCase.createdBy') || 'Created by' }}: {{ template.created_by_name }}</span>
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
              <h4 class="font-medium text-gray-900 mb-2">{{ t('createCase.templateDetails') || 'Template Details' }}</h4>
              <dl class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div class="flex flex-col">
                  <dt class="text-gray-600 text-sm">{{ t('createCase.specialty') || 'Specialty' }}</dt>
                  <dd class="font-medium">{{ selectedTemplate.specialty || 'N/A' }}</dd>
                </div>
                <div class="flex flex-col">
                  <dt class="text-gray-600 text-sm">{{ t('createCase.department') || 'Department' }}</dt>
                  <dd class="font-medium">{{ selectedTemplate.department_name || 'N/A' }}</dd>
                </div>
                <div class="flex flex-col">
                  <dt class="text-gray-600 text-sm">{{ t('createCase.createdBy') || 'Created By' }}</dt>
                  <dd class="font-medium">{{ selectedTemplate.created_by_name || 'N/A' }}</dd>
                </div>
              </dl>
            </div>

            <!-- Sections and Required Fields - Side by Side -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 class="font-medium text-gray-900 mb-2">{{ t('createCase.sections') || 'Template Sections' }}</h4>
                <ul class="space-y-1">
                  <li v-for="section in selectedTemplate.fields_schema?.sections || []" :key="section"
                    class="text-sm text-gray-600 flex items-start">
                    <CheckCircleIcon class="w-4 h-4 text-green-500 mr-2 mt-0.5 shrink-0" />
                    {{ formatSectionName(section) }}
                  </li>
                </ul>
                <div v-if="!selectedTemplate.fields_schema?.sections?.length" class="text-sm text-gray-500">
                  No sections defined
                </div>
              </div>

              <div v-if="selectedTemplate.fields_schema?.required_fields?.length">
                <h4 class="font-medium text-gray-900 mb-2">{{ t('createCase.requiredFields') || 'Required Fields' }}</h4>
                <ul class="space-y-1">
                  <li v-for="field in selectedTemplate.fields_schema.required_fields" :key="field"
                    class="text-sm text-gray-600 flex items-start">
                    <CheckCircleIcon class="w-4 h-4 text-red-500 mr-2 mt-0.5 shrink-0" />
                    {{ formatSectionName(field) }}
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
import { Activity as ActivityIcon, CheckIcon, CheckCircleIcon } from '@/components/icons'
import { type CaseTemplate, useCaseTemplates } from '@/composables/useCaseTemplates'

const { t } = useI18n()

const { caseTemplates, loading, error, fetchCaseTemplates } = useCaseTemplates()

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
