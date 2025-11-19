<template>
  <div class="space-y-6">
    <div class="text-center">
      <h2 class="text-2xl font-bold text-gray-900 mb-2">
        Physical Examination
      </h2>
      <p class="text-gray-600">
        Detailed physical examination findings by body system
      </p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- General Appearance -->
      <Card>
        <div class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            General Appearance
          </h3>

          <div class="space-y-4">
            <div class="space-y-2">
              <Label for="generalAppearance">General Appearance</Label>
              <Textarea id="generalAppearance" v-model="localData.physical_examination.general_appearance"
                placeholder="Describe patient's overall appearance, grooming, positioning, distress level..." rows="3" />
            </div>

            <div class="space-y-2">
              <Label>Consciousness Level</Label>
              <div class="grid grid-cols-2 gap-2">
                <label v-for="status in consciousnessOptions" :key="status.value" class="flex items-center">
                  <input type="radio" :value="status.value" v-model="localData.physical_examination.consciousness_level"
                    class="text-blue-600 focus:ring-blue-500" />
                  <span class="ml-2 text-sm">{{ status.label }}</span>
                </label>
              </div>
            </div>
          </div>
        </div>
      </Card>

      <!-- Vital Signs Summary -->
      <Card>
        <div class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            Vital Signs Summary
          </h3>

          <div class="space-y-3">
            <div class="flex justify-between">
              <span class="text-gray-600">Temperature:</span>
              <span class="font-medium">{{ localData.physical_examination?.vital_signs_temp || 'Not recorded' }}°C</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Heart Rate:</span>
              <span class="font-medium">{{ localData.physical_examination?.vital_signs_hr || 'Not recorded' }} bpm</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Blood Pressure:</span>
              <span class="font-medium">{{ localData.physical_examination?.vital_signs_bp || 'Not recorded' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Respiratory Rate:</span>
              <span class="font-medium">{{ localData.physical_examination?.vital_signs_rr || 'Not recorded' }}/min</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Oxygen Saturation:</span>
              <span class="font-medium">{{ localData.physical_examination?.vital_signs_spo2 || 'Not recorded' }}%</span>
            </div>
          </div>
        </div>
      </Card>
    </div>

    <!-- Systems Review -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-6">
          Physical Examination by System
        </h3>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2">
            <Label for="headNeck">Head and Neck</Label>
            <Textarea id="headNeck" v-model="localData.physical_examination.head_neck" 
              placeholder="HEENT: pupils, ears, nose, throat, neck examination..." rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="cardiovascular">Cardiovascular</Label>
            <Textarea id="cardiovascular" v-model="localData.physical_examination.cardiovascular" 
              placeholder="Heart sounds, murmurs, rhythm, peripheral pulses..." rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="respiratory">Respiratory</Label>
            <Textarea id="respiratory" v-model="localData.physical_examination.respiratory" 
              placeholder="Breath sounds, chest expansion, percussion findings..." rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="abdominal">Abdominal</Label>
            <Textarea id="abdominal" v-model="localData.physical_examination.abdominal" 
              placeholder="Inspection, auscultation, palpation, percussion findings..." rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="neurological">Neurological</Label>
            <Textarea id="neurological" v-model="localData.physical_examination.neurological" 
              placeholder="Cranial nerves, motor, sensory, reflexes, coordination..." rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="musculoskeletal">Musculoskeletal</Label>
            <Textarea id="musculoskeletal" v-model="localData.physical_examination.musculoskeletal" 
              placeholder="Joint examination, range of motion, deformities, tenderness..." rows="3" />
          </div>

          <div class="space-y-2">
            <Label for="skin">Skin</Label>
            <Textarea id="skin" v-model="localData.physical_examination.skin" 
              placeholder="Color, turgor, lesions, rashes, wounds..." rows="3" />
          </div>
        </div>
      </div>
    </Card>

    <!-- Additional Physical Exam Notes -->
    <Card>
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          Additional Examination Notes
        </h3>

        <div class="space-y-2">
          <Textarea id="examNotes" v-model="localData.physical_examination.other_findings" 
            placeholder="Any additional examination findings, special tests, or pertinent negatives..." rows="4" />
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Card from '@/components/ui/Card.vue'
import Label from '@/components/ui/Label.vue'
import Textarea from '@/components/ui/Textarea.vue'

const props = defineProps<{
  caseData: any
}>()

const emit = defineEmits<{
  'update:caseData': [any]
}>()

const localData = computed({
  get: () => props.caseData,
  set: (value) => emit('update:caseData', value)
})

const consciousnessOptions = [
  { value: 'alert', label: 'Alert' },
  { value: 'confused', label: 'Confused' },
  { value: 'lethargic', label: 'Lethargic' },
  { value: 'obtunded', label: 'Obtunded' },
  { value: 'stuporous', label: 'Stuporous' },
  { value: 'comatose', label: 'Comatose' }
]
</script>
