<template>
  <div class="space-y-6">
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-6">{{ t('createCase.caseInformation') }}</h3>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2 md:col-span-2">
            <Label for="title">{{ t('createCase.caseTitle') }} *</Label>
            <Input id="title" v-model="localData.title" :placeholder="t('createCase.enterCaseTitle')"
              :error="getTranslatedError('title')" />
            <p class="text-xs text-gray-500 mt-1">{{ t('createCase.focusOnDiseasesAndSymptoms') }}</p>
          </div>

          <!-- Patient name hidden - auto-generated from title -->
          <input type="hidden" v-model="localData.patient_name" />

          <div class="space-y-2">
            <Label for="specialty">{{ t('createCase.specialty') }} *</Label>
            <Input id="specialty" v-model="localData.specialty" :placeholder="t('createCase.specialtyExample')"
              :error="getTranslatedError('specialty')" />
          </div>

          <div class="space-y-2">
            <Label for="complexity">{{ t('createCase.complexity') }}</Label>
            <select id="complexity" v-model="localData.complexity_level"
              class="w-full px-3 py-2 border border-gray-300 rounded-md">
              <option value="basic">{{ t('createCase.complexityBasic') }}</option>
              <option value="intermediate">{{ t('createCase.complexityIntermediate') }}</option>
              <option value="advanced">{{ t('createCase.complexityAdvanced') }}</option>
              <option value="expert">{{ t('createCase.complexityExpert') }}</option>
            </select>
          </div>
        </div>
      </div>
    </Card>

    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-6">{{ t('createCase.patientDemographics') }}</h3>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2">
            <Label for="age">{{ t('createCase.age') }} *</Label>
            <Input id="age" type="number" v-model.number="localData.patient_age" :placeholder="t('createCase.patientAge')"
              :error="getTranslatedError('patient_age')" min="0" max="150" />
          </div>

          <div class="space-y-2">
            <Label for="gender">{{ t('createCase.gender') }} *</Label>
            <select id="gender" v-model="localData.patient_gender"
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
              :class="{ 'border-red-500': getTranslatedError('patient_gender') }">
              <option value="">{{ t('createCase.selectGender') }}</option>
              <option value="male">{{ t('createCase.male') }}</option>
              <option value="female">{{ t('createCase.female') }}</option>
              <option value="other">{{ t('createCase.other') }}</option>
            </select>
            <p v-if="getTranslatedError('patient_gender')" class="text-sm text-red-600">{{ getTranslatedError('patient_gender') }}</p>
          </div>

          <div class="space-y-2">
            <Label for="mrn">{{ t('createCase.medicalRecordNumber') }}</Label>
            <Input id="mrn" v-model="localData.medical_record_number" :placeholder="t('createCase.enterMRN')" />
          </div>

          <div class="space-y-2">
            <Label for="ethnicity">{{ t('createCase.ethnicity') }}</Label>
            <Input id="ethnicity" v-model="localData.patient_ethnicity" :placeholder="t('createCase.enterEthnicity')" />
          </div>

          <div class="space-y-2">
            <Label for="occupation">{{ t('createCase.occupation') }}</Label>
            <Input id="occupation" v-model="localData.patient_occupation" :placeholder="t('createCase.enterOccupation')" />
          </div>

          <div class="space-y-2">
            <Label for="admission">{{ t('createCase.admissionDate') }}</Label>
            <Input id="admission" type="date" v-model="localData.admission_date" />
          </div>
        </div>
      </div>
    </Card>

    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-6">{{ t('createCase.clinicalPresentation') }}</h3>

        <div class="space-y-6">
          <div class="space-y-2">
            <Label for="chief_complaint">{{ t('createCase.chief_complaint') }} *</Label>
            <Textarea id="chief_complaint" v-model="localData.clinical_history.chief_complaint"
              :placeholder="t('createCase.describe_chief_complaint')" :error="getTranslatedError('chief_complaint')" rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="chief_complaintBrief">{{ t('createCase.briefChiefComplaint') }}</Label>
            <Input id="chief_complaintBrief" v-model="localData.chief_complaint_brief"
              :placeholder="t('createCase.enterBriefComplaint')" />
          </div>

          <div class="space-y-2">
            <Label for="historyPresent">{{ t('createCase.historyOfPresentIllness') }}</Label>
            <Textarea id="historyPresent" v-model="localData.clinical_history.history_present_illness"
              :placeholder="t('createCase.detailedHistory')" rows="6" />
          </div>

          <div class="space-y-2">
            <Label for="pastMedical">{{ t('createCase.pastMedicalHistory') }}</Label>
            <Textarea id="pastMedical" v-model="localData.clinical_history.past_medical_history"
              :placeholder="t('createCase.describePMH')" rows="4" />
          </div>

          <div class="space-y-2">
            <Label for="medications">{{ t('createCase.currentMedications') }}</Label>
            <Textarea id="medications" v-model="localData.clinical_history.medications"
              :placeholder="t('createCase.listMedications')" rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="allergies">{{ t('createCase.allergies') }}</Label>
            <Textarea id="allergies" v-model="localData.clinical_history.allergies"
              :placeholder="t('createCase.enterAllergies')" rows="2" />
          </div>

          <!-- Missing Fields - Symptom Details -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="space-y-2">
              <Label for="symptom_duration">Thời gian có triệu chứng (ngày)</Label>
              <Input id="symptom_duration" type="number" v-model.number="localData.clinical_history.symptom_duration_days"
                placeholder="Ví dụ: 7" min="0" />
            </div>

            <div class="space-y-2">
              <Label for="symptom_onset">Khởi phát triệu chứng</Label>
              <Input id="symptom_onset" v-model="localData.clinical_history.symptom_onset"
                placeholder="Ví dụ: Đột ngột, Từ từ" />
            </div>

            <div class="space-y-2">
              <Label for="symptom_progression">Diễn biến triệu chứng</Label>
              <Input id="symptom_progression" v-model="localData.clinical_history.symptom_progression"
                placeholder="Ví dụ: Tiến triển, Ổn định, Giảm dần" />
            </div>
          </div>

          <!-- Missing Fields - Family & Social History -->
          <div class="space-y-2">
            <Label for="family_history">Tiền sử gia đình</Label>
            <Textarea id="family_history" v-model="localData.clinical_history.family_history"
              :placeholder="t('createCase.describeFamilyHistory')" rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="social_history">Tiền sử xã hội</Label>
            <Textarea id="social_history" v-model="localData.clinical_history.social_history"
              :placeholder="t('createCase.describeSocialHistory')" rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="review_systems">Hỏi bệnh theo hệ thống</Label>
            <Textarea id="review_systems" v-model="localData.clinical_history.review_systems"
              :placeholder="t('createCase.describeSystemsReview')" rows="4" />
          </div>
        </div>
      </div>
    </Card>

    <!-- Missing Fields - Case Summary & Learning Info -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-6">Tóm tắt và Thông tin Học tập</h3>

        <div class="space-y-6">
          <div class="space-y-2">
            <Label for="case_summary">Tóm tắt ca bệnh</Label>
            <Textarea id="case_summary" v-model="localData.case_summary"
              placeholder="Tóm tắt ngắn gọn về ca bệnh này..." rows="4" />
            <p class="text-xs text-gray-500 mt-1">Tóm tắt chung về ca bệnh để sinh viên dễ hiểu</p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="space-y-2">
              <Label for="learning_tags">Tags học tập</Label>
              <Input id="learning_tags" v-model="localData.learning_tags"
                placeholder="Ví dụ: Tim mạch, Cấp cứu, Nội khoa" />
              <p class="text-xs text-gray-500 mt-1">Các từ khóa giúp tìm kiếm, cách nhau bởi dấu phẩy</p>
            </div>

            <div class="space-y-2">
              <Label for="estimated_hours">Số giờ học ước tính</Label>
              <Input id="estimated_hours" type="number" v-model.number="localData.estimated_study_hours"
                placeholder="Ví dụ: 2" min="0" step="0.5" />
              <p class="text-xs text-gray-500 mt-1">Thời gian học tập dự kiến (giờ)</p>
            </div>
          </div>
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import Card from '@/components/ui/Card.vue'
import Input from '@/components/ui/Input.vue'
import Label from '@/components/ui/Label.vue'
import Textarea from '@/components/ui/Textarea.vue'

const { t } = useI18n()

const props = defineProps<{
  caseData: any
}>()

const emit = defineEmits<{
  'update:caseData': [any]
  'validation-changed': [boolean]
}>()

const localData = computed({
  get: () => props.caseData,
  set: (value) => emit('update:caseData', value)
})

const errors = ref<Record<string, string>>({})

const getTranslatedError = (field: string): string | undefined => {
  if (!errors.value[field]) return undefined
  
  // Map field names to i18n keys for error messages
  const errorKeyMap: Record<string, string> = {
    title: 'createCase.caseTitleRequired',
    patient_name: 'createCase.patientNameRequired',
    specialty: 'createCase.specialtyRequired',
    patient_age: 'createCase.validAgeRequired',
    patient_gender: 'createCase.genderRequired',
    chief_complaint: 'createCase.chief_complaintRequired',
  }
  
  const keyForError = errorKeyMap[field]
  if (keyForError) {
    return t(keyForError)
  }
  return errors.value[field]
}

const validateStep = () => {
  errors.value = {}

  if (!localData.value.title?.trim()) {
    errors.value.title = 'Case title is required'
  }

  // Auto-generate patient name from title if not provided (since field is hidden)
  if (!localData.value.patient_name?.trim()) {
    localData.value.patient_name = `Patient - ${localData.value.title?.substring(0, 20) || 'Anonymous'}`
  }

  if (!localData.value.specialty?.trim()) {
    errors.value.specialty = 'Specialty is required'
  }

  if (!localData.value.patient_age || localData.value.patient_age < 0 || localData.value.patient_age > 150) {
    errors.value.patient_age = 'Valid age is required'
  }

  if (!localData.value.patient_gender) {
    errors.value.patient_gender = 'Gender is required'
  }

  if (!localData.value.clinical_history?.chief_complaint?.trim()) {
    errors.value.chief_complaint = 'Chief complaint is required'
  }

  return Object.keys(errors.value).length === 0
}

watch(localData, () => {
  emit('validation-changed', validateStep())
}, { deep: true })

defineExpose({
  validateStep
})
</script>
