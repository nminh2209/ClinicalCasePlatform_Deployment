<template>
  <div class="space-y-6">
    <div class="text-center">
      <h2 class="text-2xl font-bold text-gray-900 mb-2">
        {{ $t('createCase.diagnosticWorkup') }}
      </h2>
      <p class="text-gray-600">
        {{ $t('createCase.diagnosticWorkupDescription') }}
      </p>
    </div>

    <!-- Laboratory Tests -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ $t('createCase.laboratoryTests') }}
        </h3>

        <div class="space-y-4">
          <div v-for="test in labTests" :key="test.key"
            class="flex flex-col sm:flex-row sm:items-center space-y-2 sm:space-y-0">
            <div class="flex items-center space-x-4 flex-1 max-w-xs">
              <input :id="test.key" type="checkbox" :checked="diagnosticWorkup.labTests?.includes(test.key)"
                @change="toggleLabTest(test.key)" class="rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
              <div>
                <Label :for="test.key" class="font-medium">{{ test.label }}</Label>
                <p class="text-sm text-gray-500">{{ test.description }}</p>
              </div>
            </div>
            <div class="w-full sm:flex-1 sm:ml-4">
              <Textarea :placeholder="$t('createCase.result')" v-model="diagnosticWorkup.labResults[test.key]"
                class="w-full" rows="2" />
            </div>
          </div>
        </div>

        <div class="mt-4 space-y-2">
          <Label for="otherLabTests">{{ $t('createCase.otherLabTests') }}</Label>
          <Textarea id="otherLabTests" v-model="diagnosticWorkup.otherLabTests"
            :placeholder="$t('createCase.otherLabTestsPlaceholder')" rows="2" />
        </div>
      </div>
    </Card>

    <!-- Imaging Studies -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ $t('createCase.imagingStudies') }}
        </h3>

        <div class="space-y-4">
          <div v-for="study in imagingStudies" :key="study.key"
            class="flex flex-col sm:flex-row sm:items-center space-y-2 sm:space-y-0">
            <div class="flex items-center space-x-4 flex-1 max-w-xs">
              <input :id="study.key" type="checkbox" :checked="diagnosticWorkup.imagingStudies?.includes(study.key)"
                @change="toggleImagingStudy(study.key)"
                class="rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
              <div>
                <Label :for="study.key" class="font-medium">{{ study.label }}</Label>
                <p class="text-sm text-gray-500">{{ study.description }}</p>
              </div>
            </div>
            <div class="flex-1 w-full sm:ml-4">
              <Textarea :placeholder="$t('createCase.findings')" v-model="diagnosticWorkup.imagingFindings[study.key]"
                class="w-full" rows="2" />
            </div>
          </div>
        </div>


        <div class="mt-4 space-y-2">
          <Label for="otherImaging">{{ $t('createCase.otherImaging') }}</Label>
          <Textarea id="otherImaging" v-model="diagnosticWorkup.otherImaging"
            :placeholder="$t('createCase.otherImagingPlaceholder')" rows="2" />
        </div>
      </div>
    </Card>

    <!-- Other Diagnostic Tests -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ $t('createCase.otherDiagnosticTests') }}
        </h3>

        <div class="space-y-4">
          <div v-for="test in otherTests" :key="test.key"
            class="flex flex-col sm:flex-row sm:items-center space-y-2 sm:space-y-0">
            <div class="flex items-center space-x-4 flex-1 max-w-xs">
              <input :id="test.key" type="checkbox" :checked="diagnosticWorkup.otherTests?.includes(test.key)"
                @change="toggleOtherTest(test.key)" class="rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
              <div>
                <Label :for="test.key" class="font-medium">{{ test.label }}</Label>
                <p class="text-sm text-gray-500">{{ test.description }}</p>
              </div>
            </div>
            <div class="w-full sm:flex-1 sm:ml-4">
              <Textarea :placeholder="$t('createCase.results')" v-model="diagnosticWorkup.otherTestResults[test.key]"
                class="w-full" rows="2" />
            </div>
          </div>
        </div>

        <div class="mt-4 space-y-2">
          <Label for="additionalTests">{{ $t('createCase.additionalTests') }}</Label>
          <Textarea id="additionalTests" v-model="diagnosticWorkup.additionalTests"
            :placeholder="$t('createCase.additionalTestsPlaceholder')" rows="3" />
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import Card from '@/components/ui/Card.vue'
import Input from '@/components/ui/Input.vue'
import Label from '@/components/ui/Label.vue'
import Textarea from '@/components/ui/Textarea.vue'

const { t } = useI18n()

const props = defineProps({
  caseData: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:caseData'])

const diagnosticWorkup = computed({
  get: () => props.caseData.diagnosticWorkup || {
    labTests: [],
    labResults: {},
    imagingStudies: [],
    imagingFindings: {},
    otherTests: [],
    otherTestResults: {}
  },
  set: (value) => emit('update:caseData', {
    ...props.caseData,
    diagnosticWorkup: value
  })
})

const labTests = [
  { key: 'cbc', label: t('createCase.completeBloodCount'), description: t('createCase.cbcDescription') },
  { key: 'cmp', label: t('createCase.comprehensiveMetabolicPanel'), description: t('createCase.cmpDescription') },
  { key: 'lipid', label: t('createCase.lipidPanel'), description: t('createCase.lipidDescription') },
  { key: 'thyroid', label: t('createCase.thyroidFunction'), description: t('createCase.thyroidDescription') },
  { key: 'urinalysis', label: t('createCase.urinalysis'), description: t('createCase.urinalysisDescription') },
  { key: 'cultures', label: t('createCase.cultures'), description: t('createCase.culturesDescription') }
]

const imagingStudies = [
  { key: 'chestXray', label: t('createCase.chestXray'), description: t('createCase.chestXrayDescription') },
  { key: 'ctChest', label: t('createCase.ctChest'), description: t('createCase.ctChestDescription') },
  { key: 'ekg', label: t('createCase.ekg'), description: t('createCase.ekgDescription') },
  { key: 'echocardiogram', label: t('createCase.echocardiogram'), description: t('createCase.echocardiogramDescription') },
  { key: 'ultrasound', label: t('createCase.ultrasound'), description: t('createCase.ultrasoundDescription') }
]

const otherTests = [
  { key: 'endoscopy', label: t('createCase.endoscopy'), description: t('createCase.endoscopyDescription') },
  { key: 'colonoscopy', label: t('createCase.colonoscopy'), description: t('createCase.colonoscopyDescription') },
  { key: 'biopsy', label: t('createCase.biopsy'), description: t('createCase.biopsyDescription') },
  { key: 'pulmonaryFunction', label: t('createCase.pulmonaryFunction'), description: t('createCase.pulmonaryFunctionDescription') }
]

const toggleLabTest = (testKey: string) => {
  const currentTests = diagnosticWorkup.value.labTests || []
  const newTests = currentTests.includes(testKey)
    ? currentTests.filter((t: string) => t !== testKey)
    : [...currentTests, testKey]

  diagnosticWorkup.value = {
    ...diagnosticWorkup.value,
    labTests: newTests
  }
}

const toggleImagingStudy = (studyKey: string) => {
  const currentStudies = diagnosticWorkup.value.imagingStudies || []
  const newStudies = currentStudies.includes(studyKey)
    ? currentStudies.filter((s: string) => s !== studyKey)
    : [...currentStudies, studyKey]

  diagnosticWorkup.value = {
    ...diagnosticWorkup.value,
    imagingStudies: newStudies
  }
}

const toggleOtherTest = (testKey: string) => {
  const currentTests = diagnosticWorkup.value.otherTests || []
  const newTests = currentTests.includes(testKey)
    ? currentTests.filter((t: string) => t !== testKey)
    : [...currentTests, testKey]

  diagnosticWorkup.value = {
    ...diagnosticWorkup.value,
    otherTests: newTests
  }
}
</script>
