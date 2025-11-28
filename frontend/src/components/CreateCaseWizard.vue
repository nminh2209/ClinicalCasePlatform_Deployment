<template>
  <div class="fixed inset-0 bg-black/50 z-50 overflow-y-auto">
    <div class="min-h-screen p-4 md:p-6 flex items-center justify-center">
      <div class="max-w-4xl w-full">
        <Card class="bg-white">
          <CardHeader class="border-b">
            <div class="flex items-center justify-between">
              <div>
                <CardTitle>{{ steps[currentStep]?.title }}</CardTitle>
                <CardDescription>{{ t('wizard.step') }} {{ currentStep + 1 }}/{{ steps.length }}</CardDescription>
              </div>
              <Button variant="ghost" size="sm" @click="$emit('close')">
                <X class="h-4 w-4" />
              </Button>
            </div>

            <!-- Compact Progress Bar -->
            <div class="mt-4">
              <div class="flex gap-1">
                <div v-for="(step, index) in steps" :key="step.id" 
                  :class="`h-2 flex-1 rounded-full transition-all ${
                    currentStep === index ? 'bg-blue-500' :
                    currentStep > index ? 'bg-green-500' : 'bg-gray-200'
                  }`" 
                />
              </div>
            </div>
          </CardHeader>

          <CardContent class="p-6">
            <!-- Step Content with max height -->
            <div class="max-h-[calc(100vh-300px)] overflow-y-auto pr-2">
              <component 
                :is="currentStepComponent" 
                :case-data="caseData" 
                @update:case-data="updateCaseData"
                @validation-changed="onValidationChanged" 
                ref="currentStepRef" 
              />
            </div>

            <!-- Navigation Buttons -->
            <div class="flex items-center justify-between mt-6 pt-6 border-t">
              <Button variant="outline" size="sm" @click="handleSaveDraft">
                <Save class="h-4 w-4 mr-2" />
                {{ t('wizard.saveDraft') }}
              </Button>

              <div class="flex gap-2">
                <Button v-if="currentStep > 0" variant="outline" @click="handleBack">
                  <ArrowLeft class="h-4 w-4 mr-2" />
                  {{ t('wizard.back') }}
                </Button>

                <Button v-if="currentStep < steps.length - 1" @click="handleNext"
                  :disabled="stepValidations[currentStep] === false">
                  {{ t('wizard.next') }}
                  <ArrowRight class="h-4 w-4 ml-2" />
                </Button>
                <Button v-else @click="handleComplete" class="bg-green-600 hover:bg-green-700"
                  :disabled="stepValidations[currentStep] === false">
                  <CheckCircle class="h-4 w-4 mr-2" />
                  {{ t('wizard.createCase') }}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineAsyncComponent } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToast } from '@/composables/useToast'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import Button from '@/components/ui/Button.vue'
import X from '@/components/icons/X.vue'
import {
  ArrowLeft,
  ArrowRight,
  Save,
  CheckCircle,
  User,
  FileText,
  Activity,
  FlaskConical,
  Paperclip,
  Sparkles
} from '@/components/icons'
import { Stethoscope } from 'lucide-vue-next'
import api from '@/services/api'

const props = defineProps({
  studentDepartment: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['close', 'complete'])

const { toast } = useToast()
const { t } = useI18n()

const currentStep = ref(0) // Start at 0 for template selection
const selectedTemplate = ref(null)
const currentStepRef = ref(null)
const stepValidations = ref<Record<number, boolean>>({})

const caseData = ref<Record<string, any>>({
  // Case Basic Fields (from Case model)
  title: '',
  patient_name: '',
  repository: null,
  specialty: '',
  complexity_level: 'intermediate',
  patient_age: null,
  patient_gender: '',
  medical_record_number: '',
  admission_date: null,
  discharge_date: null,
  case_summary: '',
  chief_complaint_brief: '',
  keywords: '',
  patient_ethnicity: '',
  patient_occupation: '',
  estimated_study_hours: null,
  requires_follow_up: false,
  follow_up_date: null,

  // ClinicalHistory (OneToOne)
  clinical_history: {
    chief_complaint: '',
    history_present_illness: '',
    past_medical_history: '',
    family_history: '',
    social_history: '',
    medications: '',
    allergies: '',
    immunizations: '',
    surgical_history: '',
    review_of_systems: ''
  },

  // PhysicalExamination (OneToOne)
  physical_examination: {
    general_appearance: '',
    consciousness_level: 'alert',
    vital_signs: '',
    vital_signs_bp: '',
    vital_signs_hr: null,
    vital_signs_rr: null,
    vital_signs_temp: null,
    vital_signs_spo2: null,
    head_neck: '',
    cardiovascular: '',
    respiratory: '',
    abdominal: '',
    neurological: '',
    musculoskeletal: '',
    skin: '',
    other_systems: ''
  },

  // Investigations (OneToOne as investigations_detail)
  detailed_investigations: {
    laboratory_results: '',
    hemoglobin_level: null,
    white_cell_count: null,
    glucose_level: null,
    creatinine_level: null,
    imaging_studies: '',
    ecg_findings: '',
    ecg_rhythm: '',
    ecg_rate: null,
    pathology_results: '',
    arterial_blood_gas: '',
    ph_level: null,
    special_tests: '',
    microbiology: '',
    biochemistry: '',
    hematology: ''
  },

  // DiagnosisManagement (OneToOne)
  diagnosis_management: {
    primary_diagnosis: '',
    differential_diagnosis: '',
    icd10_codes: '',
    treatment_plan: '',
    medications_prescribed: '',
    procedures_performed: '',
    follow_up_plan: '',
    prognosis: '',
    complications: ''
  },

  // LearningOutcomes (OneToOne)
  learning_outcomes: {
    learning_objectives: '',
    key_concepts: '',
    clinical_pearls: '',
    references: '',
    discussion_points: '',
    assessment_criteria: ''
  },

  // Medical attachments (will be uploaded separately)
  attachments: []
})

const steps = computed(() => [
  {
    id: 0,
    title: t('wizard.templateSelection'),
    icon: Sparkles,
    description: t('wizard.templateSelectionDesc')
  },
  {
    id: 1,
    title: t('wizard.basicInfo'),
    icon: User,
    description: t('wizard.basicInfoDesc')
  },
  {
    id: 2,
    title: t('wizard.vitalSigns'),
    icon: Activity,
    description: t('wizard.vitalSignsDesc')
  },
  {
    id: 3,
    title: t('wizard.physicalExam'),
    icon: Stethoscope,
    description: t('wizard.physicalExamDesc')
  },
  {
    id: 4,
    title: t('wizard.diagnosticWorkup'),
    icon: FlaskConical,
    description: t('wizard.diagnosticWorkupDesc')
  },
  {
    id: 5,
    title: t('wizard.assessmentPlan'),
    icon: FileText,
    description: t('wizard.assessmentPlanDesc')
  },
  {
    id: 6,
    title: t('wizard.attachmentsStep'),
    icon: Paperclip,
    description: t('wizard.attachmentsDesc')
  }
])

const currentStepComponent = computed(() => {
  switch (currentStep.value) {
    case 0: return TemplateSelectionStep
    case 1: return BasicInfoStep
    case 2: return VitalSignsStep
    case 3: return PhysicalExamStep
    case 4: return DiagnosticWorkupStep
    case 5: return AssessmentPlanStep
    case 6: return AttachmentsStep
    default: return null
  }
})

// Lazy load step components
const TemplateSelectionStep = defineAsyncComponent(() => import('./CreateCaseWizard/TemplateSelectionStep.vue'))
const BasicInfoStep = defineAsyncComponent(() => import('./CreateCaseWizard/BasicInfoStep.vue'))
const VitalSignsStep = defineAsyncComponent(() => import('./CreateCaseWizard/VitalSignsStep.vue'))
const PhysicalExamStep = defineAsyncComponent(() => import('./CreateCaseWizard/PhysicalExamStep.vue'))
const DiagnosticWorkupStep = defineAsyncComponent(() => import('./CreateCaseWizard/DiagnosticWorkupStep.vue'))
const AssessmentPlanStep = defineAsyncComponent(() => import('./CreateCaseWizard/AssessmentPlanStep.vue'))
const AttachmentsStep = defineAsyncComponent(() => import('./CreateCaseWizard/AttachmentsStep.vue'))

const updateField = (field: keyof typeof caseData.value, value: any) => {
  caseData.value[field] = value
}

const handleNext = () => {
  // Check if current step is valid
  const isValid = stepValidations.value[currentStep.value] !== false
  if (!isValid) {
    toast.error(t('wizard.completionRequired'))
    return
  }

  if (currentStep.value < steps.value.length - 1) {
    currentStep.value++
  }
}

const handleBack = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const handleStepClick = (stepIndex: number) => {
  // Allow navigation to any step
  currentStep.value = stepIndex
}

const handleSaveDraft = async () => {
  try {
    // Prepare the case data payload with draft status
    const payload = {
      title: caseData.value.title,
      patient_name: caseData.value.patient_name || caseData.value.title,
      repository: caseData.value.repository || 1,
      specialty: caseData.value.specialty,
      complexity_level: caseData.value.complexity_level,
      patient_age: caseData.value.patient_age,
      patient_gender: caseData.value.patient_gender,
      patient_ethnicity: caseData.value.patient_ethnicity,
      patient_occupation: caseData.value.patient_occupation,
      medical_record_number: caseData.value.medical_record_number,
      admission_date: caseData.value.admission_date,
      chief_complaint_brief: caseData.value.chief_complaint_brief,
      keywords: caseData.value.keywords,
      case_status: 'draft', // Explicitly set as draft

      // Nested models
      clinical_history: caseData.value.clinical_history,
      physical_examination: caseData.value.physical_examination,
      detailed_investigations: caseData.value.detailed_investigations,
      diagnosis_management: caseData.value.diagnosis_management,
      learning_outcomes: caseData.value.learning_outcomes
    }

    // Check if there are attachments
    const hasAttachments = caseData.value.attachments && caseData.value.attachments.length > 0

    let response
    if (hasAttachments) {
      // Use FormData for multipart upload
      const formData = new FormData()
      formData.append('data', JSON.stringify(payload))

      caseData.value.attachments.forEach((file: File, index: number) => {
        formData.append(`attachment_${index}`, file)
      })

      response = await api.post('/cases/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    } else {
      // Use regular JSON for cases without attachments
      response = await api.post('/cases/', payload)
    }

    toast.success(t('wizard.caseSavedDraft'))

    // Navigate to the new case
    setTimeout(() => {
      emit('complete', { caseId: response.data.id, caseData: response.data })
    }, 500)
  } catch (error: any) {
    console.error('Error saving draft:', error)
    const errorMessage = error.response?.data?.message || error.response?.data?.detail || t('wizard.failedToDraft')
    toast.error(errorMessage)
  }
}

const handleComplete = async () => {
  // Check if final step is valid
  const isValid = stepValidations.value[currentStep.value] !== false
  if (!isValid) {
    toast.error(t('wizard.completeRequired'))
    return
  }

  try {
    // Helper function to remove empty fields from nested objects
    const cleanObject = (obj: any) => {
      if (!obj || typeof obj !== 'object') return obj

      const cleaned: any = {}
      for (const [key, value] of Object.entries(obj)) {
        // Keep non-empty values and numbers (including 0)
        if (value !== '' && value !== null && value !== undefined) {
          cleaned[key] = value
        }
      }
      return Object.keys(cleaned).length > 0 ? cleaned : undefined
    }

    // Prepare the case data payload
    const payload: any = {
      title: caseData.value.title,
      patient_name: caseData.value.patient_name || caseData.value.title, // Use title as fallback
      repository: caseData.value.repository || 1, // Default repository ID - should be configurable
      specialty: caseData.value.specialty,
      complexity_level: caseData.value.complexity_level,
      patient_age: caseData.value.patient_age || 25, // Default age if not provided
    }

    // Add optional basic fields only if they have values
    if (caseData.value.patient_gender) payload.patient_gender = caseData.value.patient_gender
    if (caseData.value.patient_ethnicity) payload.patient_ethnicity = caseData.value.patient_ethnicity
    if (caseData.value.patient_occupation) payload.patient_occupation = caseData.value.patient_occupation
    if (caseData.value.medical_record_number) payload.medical_record_number = caseData.value.medical_record_number
    if (caseData.value.admission_date) payload.admission_date = caseData.value.admission_date
    if (caseData.value.chief_complaint_brief) payload.chief_complaint_brief = caseData.value.chief_complaint_brief
    if (caseData.value.keywords) payload.keywords = caseData.value.keywords

    // Add nested models only if they have data
    const cleanedClinicalHistory = cleanObject(caseData.value.clinical_history)
    if (cleanedClinicalHistory) payload.clinical_history = cleanedClinicalHistory

    const cleanedPhysicalExam = cleanObject(caseData.value.physical_examination)
    if (cleanedPhysicalExam) payload.physical_examination = cleanedPhysicalExam

    const cleanedInvestigations = cleanObject(caseData.value.detailed_investigations)
    if (cleanedInvestigations) payload.detailed_investigations = cleanedInvestigations

    const cleanedDiagnosis = cleanObject(caseData.value.diagnosis_management)
    if (cleanedDiagnosis) payload.diagnosis_management = cleanedDiagnosis

    const cleanedLearning = cleanObject(caseData.value.learning_outcomes)
    if (cleanedLearning) payload.learning_outcomes = cleanedLearning

    console.log('=== CASE CREATION PAYLOAD ===')
    console.log('Full payload:', JSON.stringify(payload, null, 2))
    console.log('=== END PAYLOAD ===')

    // Check if there are attachments
    const hasAttachments = caseData.value.attachments && caseData.value.attachments.length > 0

    let response
    if (hasAttachments) {
      // Use FormData for multipart upload
      const formData = new FormData()
      formData.append('data', JSON.stringify(payload))

      caseData.value.attachments.forEach((file: File, index: number) => {
        formData.append(`attachment_${index}`, file)
      })

      response = await api.post('/cases/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    } else {
      // Use regular JSON for cases without attachments
      response = await api.post('/cases/', payload)
    }

    toast.success(t('wizard.caseCreated'))

    // Navigate to the new case
    setTimeout(() => {
      emit('complete', { caseId: response.data.id, caseData: response.data })
    }, 500)
  } catch (error: any) {
    console.error('Error creating case:', error)
    console.error('Error response:', error.response?.data)
    console.error('Error status:', error.response?.status)

    // Display detailed error information
    let errorMessage = t('wizard.failedToCreate')

    if (error.response?.data) {
      // Log the full error object to see all validation errors
      console.error('Full error object:', JSON.stringify(error.response.data, null, 2))

      // If there's a specific error message
      if (error.response.data.message || error.response.data.detail) {
        errorMessage = error.response.data.message || error.response.data.detail
      } else {
        // If there are field-specific errors, show them
        const errors = error.response.data
        const errorFields = Object.keys(errors)
        if (errorFields.length > 0) {
          const firstField = errorFields[0]
          if (firstField) {
            const firstError = Array.isArray(errors[firstField]) ? errors[firstField][0] : errors[firstField]
            errorMessage = `${firstField}: ${firstError}`
            console.error('Validation errors:', errors)
          }
        }
      }
    }

    toast.error(errorMessage)
  }
}

const handleTemplateSelect = (template: any) => {
  selectedTemplate.value = template
  updateCaseData({ template })
  currentStep.value = 1 // Move to basic info step after template selection
}

const updateCaseData = (newData: Partial<typeof caseData.value>) => {
  caseData.value = { ...caseData.value, ...newData }
}

const onValidationChanged = (isValid: boolean) => {
  stepValidations.value[currentStep.value] = isValid
}

// Provide reactive data to child components
defineExpose({
  caseData,
  updateField,
  studentDepartment: props.studentDepartment
})
</script>
