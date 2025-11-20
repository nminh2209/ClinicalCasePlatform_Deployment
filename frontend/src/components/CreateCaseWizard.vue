<template>
  <div class="fixed inset-0 bg-black/50 z-50 overflow-y-auto">
    <div class="min-h-screen p-4 md:p-6">
      <div class="max-w-5xl mx-auto">
        <Card class=" bg-white my-6">
          <CardHeader class="border-b mb-2">
            <div class="flex items-center justify-between">
              <div>
                <CardTitle>Tạo ca bệnh thực hành</CardTitle>
                <CardDescription>
                  Xây dựng một ca bệnh hoàn chỉnh cho thực hành lâm sàng.
                </CardDescription>
              </div>
              <Button variant="ghost" @click="$emit('close')">
                <ArrowLeft class=" h-4 w-4 mr-2" />
                Huỷ
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
                  Lưu bản nháp
                </Button>
              </div>

              <div class="flex gap-2">
                <Button v-if="currentStep > 0" variant="outline" @click="handleBack">
                  <ArrowLeft class="h-4 w-4 mr-2" />
                  Quay lại
                </Button>

                <Button v-if="currentStep < steps.length - 1" @click="handleNext"
                  class="bg-primary text-white hover:bg-blue-600" :disabled="stepValidations[currentStep] === false">
                  Tiếp tục
                  <ArrowRight class="h-4 w-4 ml-2" />
                </Button>
                <Button v-else @click="handleComplete" class="text-white bg-green-600 hover:bg-green-700"
                  :disabled="stepValidations[currentStep] === false">
                  <CheckCircle class="h-4 w-4 mr-2" />
                  Tạo ca bệnh
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
  // Template selection
  template: null,

  // Patient information
  patient: {
    firstName: '',
    lastName: '',
    age: null,
    gender: '',
    mrn: '',
    dateOfBirth: ''
  },

  // Clinical presentation
  chiefComplaint: '',
  historyOfPresentIllness: '',
  pastMedicalHistory: '',

  // Vital signs
  vitalSigns: {
    temperature: null,
    heartRate: null,
    bloodPressureSystolic: null,
    bloodPressureDiastolic: null,
    respiratoryRate: null,
    oxygenSaturation: null,
    weight: null,
    height: null,
    bmi: null,
    painScale: null,
    notes: ''
  },

  // Physical examination
  physicalExam: {
    generalAppearance: '',
    mentalStatus: '',
    notes: ''
  },

  // Diagnostic workup
  diagnosticWorkup: {
    labTests: [],
    labResults: {},
    imagingStudies: [],
    imagingFindings: {},
    otherTests: [],
    otherTestResults: {},
    otherLabTests: '',
    otherImaging: '',
    additionalTests: ''
  },

  // Assessment and plan
  assessment: {
    primaryDiagnosis: '',
    differentialDiagnosis: '',
    clinicalReasoning: '',
    medications: [],
    procedures: '',
    followUp: '',
    learningObjectives: []
  },

  // Attachments
  attachments: []
})

const steps = ref([
  {
    id: 0,
    title: "Chọn mẫu",
    icon: Sparkles,
    description: "Chọn mẫu ca bệnh để bắt đầu"
  },
  {
    id: 1,
    title: "Thông tin cơ bản",
    icon: User,
    description: "Thông tin bệnh nhân và lý do nhập viện"
  },
  {
    id: 2,
    title: "Dấu hiệu sinh tồn",
    icon: Activity,
    description: "Ghi lại các dấu hiệu sinh tồn và các phép đo"
  },
  {
    id: 3,
    title: "Khám lâm sàng",
    icon: Stethoscope,
    description: "Ghi lại các kết quả khám lâm sàng"
  },
  {
    id: 4,
    title: "Chẩn đoán cận lâm sàng",
    icon: FlaskConical,
    description: "Xét nghiệm và hình ảnh chẩn đoán"
  },
  {
    id: 5,
    title: "Đánh giá & Kế hoạch",
    icon: FileText,
    description: "Chẩn đoán, kế hoạch điều trị và mục tiêu học tập"
  },
  {
    id: 6,
    title: "Tệp đính kèm",
    icon: Paperclip,
    description: "Tải lên hình ảnh và tài liệu hỗ trợ"
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

const handleComplete = () => {
  // Check if final step is valid
  const isValid = stepValidations.value[currentStep.value] !== false
  if (!isValid) {
    toast.error("Please complete all required fields before creating the case")
    return
  }

  // Generate case ID
  const newCaseId = `case-${Date.now()}`

  // In a real app, save to backend here
  toast.success("Medical case created successfully!")

  // Navigate to the new case
  setTimeout(() => {
    emit('complete', { caseId: newCaseId, caseData: caseData.value })
  }, 500)
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
