<template>
  <div class="fixed inset-0 bg-black/50 z-50 overflow-y-auto">
    <div class="min-h-screen p-4 md:p-6">
      <div class="max-w-5xl mx-auto">
        <Card class=" bg-white my-6">
          <CardHeader class="border-b mb-2">
            <div class="flex items-center justify-between">
              <div>
                <CardTitle>Create Practice Case</CardTitle>
                <CardDescription>
                  Build a complete patient case for clinical practice
                </CardDescription>
              </div>
              <Button variant="ghost" @click="$emit('close')">
                <ArrowLeft class=" h-4 w-4 mr-2" />
                Cancel
              </Button>
            </div>

            <!-- Progress Steps -->
            <div class="mt-6">
              <div class="flex items-start justify-between mt-1 mb-2">
                <div v-for="(step, index) in steps" :key="step.id" class="flex items-start flex-1">
                  <div class="flex flex-col items-center flex-1">
                    <button type="button" @click="handleStepClick(index)" :disabled="currentStep === -1" :class="`w-10 h-10 rounded-full flex items-center justify-center border-2 transition-all cursor-pointer hover:scale-110 disabled:cursor-default disabled:hover:scale-100 ${currentStep === index
                      ? 'bg-primary text-white border-primary shadow-lg'
                      : currentStep > index
                        ? 'bg-green-500 text-white border-green-500 hover:shadow-md'
                        : 'bg-white text-gray-400 border-gray-300 hover:border-primary hover:text-primary'
                      }`" :title="`Go to: ${step.title}`">
                      <component :is="currentStep > index ? CheckCircle : step.icon" class="h-5 w-5" />
                    </button>
                    <p :class="`text-xs mt-2 text-center hidden md:block min-h-[2rem] ${currentStep === index ? 'font-medium text-gray-900' : 'text-gray-500'
                      }`">
                      {{ step.title }}
                    </p>
                  </div>
                  <div v-if="index < steps.length - 1" :class="`mt-5 h-0.5 flex-1 mx-2 transition-colors ${currentStep > index ? 'bg-green-500' : 'bg-gray-300'
                    }`" />
                </div>
              </div>
            </div>
          </CardHeader>

          <CardContent class="p-6">
            <!-- Current Step Title -->
            <div class="mb-6">
              <h2 class="text-gray-800 mb-1">{{ steps[currentStep]?.title }}</h2>
              <p class="text-muted-foreground">{{ steps[currentStep]?.description }}</p>
            </div>

            <!-- Step Content -->
            <div class="max-h-[60vh] overflow-y-auto pr-2">
              <component :is="currentStepComponent" :case-data="caseData" @update:case-data="updateCaseData"
                @validation-changed="onValidationChanged" ref="currentStepRef" />
            </div>

            <!-- Navigation Buttons -->
            <div class="flex items-center justify-between mt-8 pt-6 border-t">
              <div class="flex gap-2">
                <Button variant="outline" @click="handleSaveDraft">
                  <Save class="h-4 w-4 mr-2" />
                  Save Draft
                </Button>
              </div>

              <div class="flex gap-2">
                <Button v-if="currentStep > 0" variant="outline" @click="handleBack">
                  <ArrowLeft class="h-4 w-4 mr-2" />
                  Back
                </Button>

                <Button v-if="currentStep < steps.length - 1" @click="handleNext" class="bg-primary text-white hover:bg-blue-600"
                  :disabled="stepValidations[currentStep] === false">
                  Next
                  <ArrowRight class="h-4 w-4 ml-2" />
                </Button>
                <Button v-else @click="handleComplete" class="text-white bg-green-600 hover:bg-green-700"
                  :disabled="stepValidations[currentStep] === false">
                  <CheckCircle class="h-4 w-4 mr-2" />
                  Create Case
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
import { useToast } from '@/composables/useToast'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import Button from '@/components/ui/Button.vue'
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

const currentStep = ref(0) // Start at 0 for template selection
const selectedTemplate = ref(null)
const currentStepRef = ref(null)
const stepValidations = ref<Record<number, boolean>>({})

const caseData = ref<Record<string, any>>({
  // Case Basic Fields (from Case model)
  title: '',
  template: null,
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

const steps = ref([
  {
    id: 0,
    title: "Template Selection",
    icon: Sparkles,
    description: "Choose a case template to get started"
  },
  {
    id: 1,
    title: "Basic Information",
    icon: User,
    description: "Patient demographics and chief complaint"
  },
  {
    id: 2,
    title: "Vital Signs",
    icon: Activity,
    description: "Record vital signs and measurements"
  },
  {
    id: 3,
    title: "Physical Examination",
    icon: Stethoscope,
    description: "Document physical examination findings"
  },
  {
    id: 4,
    title: "Diagnostic Workup",
    icon: FlaskConical,
    description: "Laboratory tests and imaging studies"
  },
  {
    id: 5,
    title: "Assessment & Plan",
    icon: FileText,
    description: "Diagnosis, treatment plan, and learning objectives"
  },
  {
    id: 6,
    title: "Attachments",
    icon: Paperclip,
    description: "Upload images and supporting documents"
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
    toast.error("Please complete all required fields before proceeding")
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

const handleSaveDraft = () => {
  toast.success("Case saved as draft!")
  emit('close')
}

const handleComplete = async () => {
  // Check if final step is valid
  const isValid = stepValidations.value[currentStep.value] !== false
  if (!isValid) {
    toast.error("Please complete all required fields before creating the case")
    return
  }

  try {
    // Prepare FormData for multipart upload (for files)
    const formData = new FormData()
    
    // Prepare the case data payload
    const payload = {
      title: caseData.value.title,
      specialty: caseData.value.specialty,
      difficulty_level: caseData.value.difficulty_level,
      complexity_level: caseData.value.complexity_level,
      patient_age: caseData.value.patient_age,
      patient_gender: caseData.value.patient_gender,
      patient_ethnicity: caseData.value.patient_ethnicity,
      patient_occupation: caseData.value.patient_occupation,
      medical_record_number: caseData.value.medical_record_number,
      admission_date: caseData.value.admission_date,
      presenting_location: caseData.value.presenting_location,
      
      // Nested models
      clinical_history: caseData.value.clinical_history,
      physical_examination: caseData.value.physical_examination,
      detailed_investigations: caseData.value.detailed_investigations,
      diagnosis_management: caseData.value.diagnosis_management,
      learning_outcomes: caseData.value.learning_outcomes
    }

    // Append case data as JSON
    formData.append('data', JSON.stringify(payload))

    // Append files if any
    if (caseData.value.attachments && caseData.value.attachments.length > 0) {
      caseData.value.attachments.forEach((file: File, index: number) => {
        formData.append(`attachment_${index}`, file)
      })
    }

    // Make API call to create case
    const response = await api.post('/cases/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    toast.success("Medical case created successfully!")

    // Navigate to the new case
    setTimeout(() => {
      emit('complete', { caseId: response.data.id, caseData: response.data })
    }, 500)
  } catch (error: any) {
    console.error('Error creating case:', error)
    const errorMessage = error.response?.data?.message || 'Failed to create case. Please try again.'
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
