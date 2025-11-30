<template>
  <div class="space-y-6">
    <!-- Laboratory Tests -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ t('createCase.laboratoryResults') }}
        </h3>

        <div class="space-y-4">
          <div class="space-y-2">
            <Label for="labResults">{{ t('createCase.completeLaboratoryResults') }}</Label>
            <Textarea id="labResults" v-model="localData.detailed_investigations.laboratory_results"
              :placeholder="t('createCase.completeLabPlaceholder')" rows="4" />
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div class="space-y-2">
              <Label for="hemoglobin">{{ t('createCase.hemoglobin') }} {{ t('createCase.hemoglobinUnit') }}</Label>
              <Input id="hemoglobin" type="number" step="0.1" v-model.number="localData.detailed_investigations.hemoglobin_level"
                placeholder="14.0" />
            </div>

            <div class="space-y-2">
              <Label for="wbc">{{ t('createCase.whiteBloodCellCount') }} {{ t('createCase.wbcUnit') }}</Label>
              <Input id="wbc" type="number" step="0.1" v-model.number="localData.detailed_investigations.white_cell_count"
                placeholder="7.5" />
            </div>

            <div class="space-y-2">
              <Label for="platelet">{{ t('createCase.plateletCount') }} {{ t('createCase.plateletUnit') }}</Label>
              <Input id="platelet" type="number" step="1" v-model.number="localData.detailed_investigations.platelet_count"
                placeholder="250" />
            </div>

            <div class="space-y-2">
              <Label for="sodium">{{ t('createCase.sodium') }} {{ t('createCase.sodiumUnit') }}</Label>
              <Input id="sodium" type="number" step="0.1" v-model.number="localData.detailed_investigations.sodium_level"
                placeholder="140" />
            </div>

            <div class="space-y-2">
              <Label for="potassium">{{ t('createCase.potassium') }} {{ t('createCase.potassiumUnit') }}</Label>
              <Input id="potassium" type="number" step="0.1" v-model.number="localData.detailed_investigations.potassium_level"
                placeholder="4.0" />
            </div>

            <div class="space-y-2">
              <Label for="creatinine">{{ t('createCase.creatinine') }} {{ t('createCase.creatinineUnit') }}</Label>
              <Input id="creatinine" type="number" step="0.1" v-model.number="localData.detailed_investigations.creatinine_level"
                placeholder="1.0" />
            </div>

            <div class="space-y-2">
              <Label for="glucose">{{ t('createCase.glucose') }} {{ t('createCase.glucoseUnit') }}</Label>
              <Input id="glucose" type="number" step="1" v-model.number="localData.detailed_investigations.glucose_level"
                placeholder="100" />
            </div>
          </div>
        </div>
      </div>
    </Card>

    <!-- Imaging Studies -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ t('createCase.imagingStudies') }}
        </h3>

        <div class="space-y-4">
          <div class="space-y-2">
            <Label for="imaging">{{ t('createCase.imagingFindings') }}</Label>
            <Textarea id="imaging" v-model="localData.detailed_investigations.imaging_studies"
              :placeholder="t('createCase.imagingFindingsPlaceholder')" rows="4" />
          </div>

          <!-- Missing Field: ECG Findings -->
          <div class="space-y-2">
            <Label for="ecg_findings">Điện tâm đồ (ECG)</Label>
            <Textarea id="ecg_findings" v-model="localData.detailed_investigations.ecg_findings"
              placeholder="Nhập kết quả điện tâm đồ..." rows="3" />
          </div>
        </div>
      </div>
    </Card>

    <!-- Other Diagnostic Tests -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ t('createCase.otherDiagnosticTests') }}
        </h3>

        <div class="space-y-4">
          <div class="space-y-2">
            <Label for="pathology">{{ t('createCase.pathologyResults') }}</Label>
            <Textarea id="pathology" v-model="localData.detailed_investigations.pathology_results"
              :placeholder="t('createCase.pathologyPlaceholder')" rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="microbiology">{{ t('createCase.microbiologyResults') }}</Label>
            <Textarea id="microbiology" v-model="localData.detailed_investigations.microbiology_results"
              :placeholder="t('createCase.microbiologyPlaceholder')" rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="otherInvestigations">{{ t('createCase.additionalInvestigations') }}</Label>
            <Textarea id="otherInvestigations" v-model="localData.detailed_investigations.other_investigations"
              :placeholder="t('createCase.additionalInvestigationsPlaceholder')" rows="3" />
          </div>
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import Card from '@/components/ui/Card.vue'
import Input from '@/components/ui/Input.vue'
import Label from '@/components/ui/Label.vue'
import Textarea from '@/components/ui/Textarea.vue'

const props = defineProps<{
  caseData: any
}>()

const { t } = useI18n()

const emit = defineEmits<{
  'update:caseData': [any]
}>()

const localData = computed({
  get: () => props.caseData,
  set: (value) => emit('update:caseData', value)
})
</script>
