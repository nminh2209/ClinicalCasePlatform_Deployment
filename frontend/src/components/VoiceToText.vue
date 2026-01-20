<template>
  <div class="voice-to-text-inline">
    <button
      @click="toggleRecording"
      :class="['voice-btn', { recording: isRecording, processing: isProcessing }]"
      :disabled="isProcessing"
      :title="buttonTitle"
      type="button"
    >
      <!-- Microphone Icon (Idle) -->
      <svg
        v-if="!isRecording && !isProcessing"
        class="icon"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2.5"
      >
        <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
        <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
        <line x1="12" y1="19" x2="12" y2="23" />
        <line x1="8" y1="23" x2="16" y2="23" />
      </svg>

      <!-- Recording Animation -->
      <svg
        v-if="isRecording"
        class="icon recording-pulse"
        viewBox="0 0 24 24"
        fill="currentColor"
      >
        <circle cx="12" cy="12" r="8" />
      </svg>

      <!-- Processing Spinner -->
      <svg
        v-if="isProcessing"
        class="icon spinner"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2.5"
      >
        <circle cx="12" cy="12" r="10" opacity="0.25" />
        <path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round" />
      </svg>
      
      <!-- Timer Badge -->
      <span v-if="isRecording" class="timer-badge">{{ formattedTime }}</span>
    </button>

    <!-- Compact Error Tooltip -->
    <div v-if="error" class="error-tooltip">
      {{ error }}
      <button @click="error = null" class="close-error">×</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import axios from 'axios'

// Props
const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  language: {
    type: String,
    default: 'vi-VN' // Vietnamese by default
  },
  continuous: {
    type: Boolean,
    default: false
  },
  interimResults: {
    type: Boolean,
    default: true
  },
  maxDuration: {
    type: Number,
    default: 60 // Max recording duration in seconds
  },
  autoApply: {
    type: Boolean,
    default: true // Automatically emit text when recording stops
  },
  showMethodInfo: {
    type: Boolean,
    default: false // Show which method is being used (dev mode)
  },
  idleText: {
    type: String,
    default: '🎤 Nhấn để bắt đầu ghi âm' // Vietnamese default
  },
  recordingText: {
    type: String,
    default: 'Đang ghi âm...' // Vietnamese default
  },
  processingText: {
    type: String,
    default: 'Đang xử lý âm thanh...' // Vietnamese default
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'transcription', 'error', 'recording-start', 'recording-stop'])

// State
const isRecording = ref(false)
const isProcessing = ref(false)
const transcription = ref('')
const error = ref(null)
const confidence = ref(null)
const recognitionMethod = ref(null)
const recordingTime = ref(0)

// Web Speech API
let recognition = null
let mediaRecorder = null
let audioChunks = []
let recordingInterval = null

// Computed
const buttonTitle = computed(() => {
  if (isProcessing.value) return 'Processing...'
  if (isRecording.value) return 'Click to stop recording'
  return 'Click to start recording'
})

const formattedTime = computed(() => {
  const minutes = Math.floor(recordingTime.value / 60)
  const seconds = recordingTime.value % 60
  return `${minutes}:${seconds.toString().padStart(2, '0')}`
})

// Initialize
onMounted(() => {
  detectRecognitionMethod()
})

onBeforeUnmount(() => {
  cleanup()
})

// Watch for manual value changes
watch(() => props.modelValue, (newValue) => {
  if (newValue !== transcription.value) {
    transcription.value = newValue
  }
})

/**
 * Detect which speech recognition method to use
 */
function detectRecognitionMethod() {
  // Check for Web Speech API support
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  
  if (SpeechRecognition) {
    recognitionMethod.value = 'Web Speech API (Browser Native)'
    initializeWebSpeechAPI()
  } else {
    recognitionMethod.value = 'PhoWhisper (Backend ASR)'
    // Fallback will be handled when recording
  }
}

/**
 * Initialize Web Speech API
 */
function initializeWebSpeechAPI() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  
  if (!SpeechRecognition) return
  
  recognition = new SpeechRecognition()
  recognition.continuous = props.continuous
  recognition.interimResults = props.interimResults
  recognition.lang = props.language
  
  recognition.onstart = () => {
    console.log('Speech recognition started')
  }
  
  recognition.onresult = (event) => {
    let interimTranscript = ''
    let finalTranscript = ''
    
    for (let i = event.resultIndex; i < event.results.length; i++) {
      const transcript = event.results[i][0].transcript
      
      if (event.results[i].isFinal) {
        finalTranscript += transcript + ' '
        if (event.results[i][0].confidence) {
          confidence.value = event.results[i][0].confidence
        }
      } else {
        interimTranscript += transcript
      }
    }
    
    if (finalTranscript) {
      transcription.value = finalTranscript.trim()
      emitTranscription(transcription.value)
    } else if (props.interimResults && interimTranscript) {
      transcription.value = interimTranscript.trim()
    }
  }
  
  recognition.onerror = (event) => {
    console.error('Speech recognition error:', event.error)
    handleError(`Speech recognition error: ${event.error}`)
    stopRecording()
  }
  
  recognition.onend = () => {
    if (isRecording.value) {
      // Restart if continuous mode and still recording
      if (props.continuous) {
        recognition.start()
      } else {
        stopRecording()
      }
    }
  }
}

/**
 * Toggle recording on/off
 */
async function toggleRecording() {
  if (isRecording.value) {
    stopRecording()
  } else {
    await startRecording()
  }
}

/**
 * Start recording
 * Automatically uses Web Speech API if available (Chrome/Edge/Safari)
 * Falls back to PhoWhisper backend if not available (Firefox, etc.)
 */
async function startRecording() {
  try {
    error.value = null
    transcription.value = ''
    confidence.value = null
    recordingTime.value = 0
    
    // Use Web Speech API if available (instant transcription)
    if (recognition) {
      recognition.start()
      isRecording.value = true
      startTimer()
      emit('recording-start')
    } else {
      // Automatic fallback: Use PhoWhisper backend for browsers without Web Speech API
      await startMediaRecording()
    }
  } catch (err) {
    console.error('Failed to start recording:', err)
    handleError('Failed to start recording. Please check microphone permissions.')
  }
}

/**
 * Start media recording for backend processing
 */
async function startMediaRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    
    mediaRecorder = new MediaRecorder(stream)
    audioChunks = []
    
    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.push(event.data)
      }
    }
    
    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/wav' })
      await processAudioWithBackend(audioBlob)
      
      // Stop all tracks
      stream.getTracks().forEach(track => track.stop())
    }
    
    mediaRecorder.start()
    isRecording.value = true
    startTimer()
    emit('recording-start')
    
  } catch (err) {
    console.error('Failed to start media recording:', err)
    handleError('Failed to access microphone. Please check permissions.')
  }
}

/**
 * Stop recording
 */
function stopRecording() {
  if (!isRecording.value) return
  
  isRecording.value = false
  stopTimer()
  
  if (recognition) {
    recognition.stop()
  }
  
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop()
  }
  
  emit('recording-stop')
}

/**
 * Process audio with backend ASR service
 */
async function processAudioWithBackend(audioBlob) {
  isProcessing.value = true
  
  try {
    // Get auth token
    const token = localStorage.getItem('access_token')
    const headers = {
      Authorization: `Bearer ${token}`
    }
    
    // Check if ASR service is available
    const statusResponse = await axios.get('/api/asr/status/', { headers })
    
    if (!statusResponse.data.available) {
      throw new Error('ASR service is not available. Please contact administrator.')
    }
    
    // Create form data
    const formData = new FormData()
    formData.append('audio', audioBlob, 'recording.wav')
    formData.append('language', props.language.startsWith('vi') ? 'vi' : 'en')
    formData.append('return_timestamps', 'false')
    
    // Send to backend
    const response = await axios.post('/api/asr/transcribe/', formData, {
      headers: {
        ...headers,
        'Content-Type': 'multipart/form-data'
      }
    })
    
    if (response.data.success) {
      transcription.value = response.data.text
      emitTranscription(transcription.value)
    } else {
      throw new Error(response.data.error || 'Transcription failed')
    }
    
  } catch (err) {
    console.error('Backend transcription error:', err)
    handleError(err.response?.data?.error || err.message || 'Failed to transcribe audio')
  } finally {
    isProcessing.value = false
  }
}

/**
 * Start recording timer
 */
function startTimer() {
  recordingInterval = setInterval(() => {
    recordingTime.value++
    
    // Auto-stop after max duration
    if (recordingTime.value >= props.maxDuration) {
      stopRecording()
      handleError(`Recording stopped: Maximum duration of ${props.maxDuration} seconds reached`)
    }
  }, 1000)
}

/**
 * Stop recording timer
 */
function stopTimer() {
  if (recordingInterval) {
    clearInterval(recordingInterval)
    recordingInterval = null
  }
}

/**
 * Emit transcription
 */
function emitTranscription(text) {
  if (props.autoApply) {
    emit('update:modelValue', text)
  }
  emit('transcription', text)
}

/**
 * Clear transcription
 */
function clearTranscription() {
  transcription.value = ''
  confidence.value = null
  emit('update:modelValue', '')
}

/**
 * Handle error
 */
function handleError(message) {
  error.value = message
  emit('error', message)
}

/**
 * Cleanup
 */
function cleanup() {
  if (isRecording.value) {
    stopRecording()
  }
  
  stopTimer()
  
  if (mediaRecorder) {
    mediaRecorder = null
  }
  
  audioChunks = []
}

// Expose methods for parent components
defineExpose({
  startRecording,
  stopRecording,
  clearTranscription,
  isRecording,
  transcription
})
</script>

<style scoped>
.voice-to-text-inline {
  display: inline-flex;
  align-items: center;
  position: relative;
}

.voice-btn {
  width: 36px;
  height: 36px;
  min-width: 36px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  background: white;
  color: #6b7280;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  position: relative;
  padding: 0;
}

.voice-btn:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #9ca3af;
  color: #374151;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.voice-btn:active:not(:disabled) {
  transform: translateY(0);
}

.voice-btn.recording {
  background: #fee2e2;
  border-color: #f87171;
  color: #dc2626;
  animation: pulse-border 1.5s ease-in-out infinite;
}

.voice-btn.processing {
  background: #e0e7ff;
  border-color: #818cf8;
  color: #4f46e5;
  cursor: wait;
}

.voice-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.recording-pulse {
  animation: pulse-icon 1s ease-in-out infinite;
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes pulse-border {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.4);
  }
  50% {
    box-shadow: 0 0 0 4px rgba(220, 38, 38, 0.1);
  }
}

@keyframes pulse-icon {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.1);
  }
}

.timer-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #dc2626;
  color: white;
  font-size: 10px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 10px;
  line-height: 1;
  font-family: 'Monaco', 'Courier New', monospace;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  pointer-events: none;
}

.error-tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  margin-bottom: 8px;
  background: #fef2f2;
  border: 1px solid #fca5a5;
  color: #991b1b;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 12px;
  white-space: nowrap;
  max-width: 250px;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 50;
}

.error-tooltip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 6px solid transparent;
  border-top-color: #fca5a5;
}

.close-error {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  color: #991b1b;
  padding: 0;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.2s;
  flex-shrink: 0;
}

.close-error:hover {
  background: rgba(0, 0, 0, 0.1);
}
</style>
