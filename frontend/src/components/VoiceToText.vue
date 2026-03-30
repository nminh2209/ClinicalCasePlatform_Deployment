<template>
  <div
    :class="[
      'voice-to-text-inline',
      { 'voice-to-text-small': size === 'small' },
    ]"
  >
    <Button
      @click="toggleRecording"
      :class="[
        'voice-btn',
        {
          'voice-btn-recording': isRecording,
          'voice-btn-processing': isProcessing,
        },
      ]"
      :disabled="isProcessing"
      :title="buttonTitle"
      :severity="buttonSeverity"
      :outlined="!isRecording && !isProcessing"
      :size="size === 'small' ? 'small' : undefined"
      rounded
      aria-label="Voice recording"
    >
      <!-- Microphone Icon (Idle) -->
      <i v-if="!isRecording && !isProcessing" class="pi pi-microphone"></i>

      <!-- Recording Animation -->
      <i v-if="isRecording" class="pi pi-circle-fill recording-pulse"></i>

      <!-- Processing Spinner -->
      <i v-if="isProcessing" class="pi pi-spin pi-spinner"></i>

      <!-- Timer Badge -->
      <Badge
        v-if="isRecording"
        :value="formattedTime"
        severity="danger"
        class="timer-badge"
      />
    </Button>

    <!-- Error Message -->
    <Message
      v-if="error"
      severity="error"
      :closable="true"
      @close="error = null"
      class="error-message"
    >
      {{ error }}
    </Message>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, watch } from "vue";
import axios from "axios";
import Button from "primevue/button";
import Badge from "primevue/badge";
import Message from "primevue/message";

// Web Speech API type declarations
interface SpeechRecognitionEvent extends Event {
  resultIndex: number;
  results: SpeechRecognitionResultList;
}

interface SpeechRecognitionErrorEvent extends Event {
  error: string;
}

declare global {
  interface Window {
    SpeechRecognition: new () => SpeechRecognition;
    webkitSpeechRecognition: new () => SpeechRecognition;
  }
}

interface SpeechRecognition extends EventTarget {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  start(): void;
  stop(): void;
  onstart: ((this: SpeechRecognition, ev: Event) => void) | null;
  onresult:
    | ((this: SpeechRecognition, ev: SpeechRecognitionEvent) => void)
    | null;
  onerror:
    | ((this: SpeechRecognition, ev: SpeechRecognitionErrorEvent) => void)
    | null;
  onend: ((this: SpeechRecognition, ev: Event) => void) | null;
}

// Props
const props = defineProps({
  modelValue: {
    type: String,
    default: "",
  },
  size: {
    type: String as () => "small" | "default",
    default: "default",
  },
  language: {
    type: String,
    default: "vi-VN",
  },
  continuous: {
    type: Boolean,
    default: false,
  },
  interimResults: {
    type: Boolean,
    default: true,
  },
  maxDuration: {
    type: Number,
    default: 60,
  },
  autoApply: {
    type: Boolean,
    default: true,
  },
  showMethodInfo: {
    type: Boolean,
    default: false,
  },
  idleText: {
    type: String,
    default: "🎤 Nhấn để bắt đầu ghi âm",
  },
  recordingText: {
    type: String,
    default: "Đang ghi âm...",
  },
  processingText: {
    type: String,
    default: "Đang xử lý âm thanh...",
  },
});

// Emits
const emit = defineEmits([
  "update:modelValue",
  "transcription",
  "error",
  "recording-start",
  "recording-stop",
]);

// State
const isRecording = ref(false);
const isProcessing = ref(false);
const transcription = ref("");
const error = ref<string | null>(null);
const confidence = ref<number | null>(null);
const recognitionMethod = ref<string | null>(null);
const recordingTime = ref(0);

// Web Speech API
let recognition: any = null;
let mediaRecorder: MediaRecorder | null = null;
let audioChunks: Blob[] = [];
let recordingInterval: ReturnType<typeof setInterval> | null = null;

// Computed
const buttonTitle = computed(() => {
  if (isProcessing.value) return "Processing...";
  if (isRecording.value) return "Click to stop recording";
  return "Click to start recording";
});

const formattedTime = computed(() => {
  const minutes = Math.floor(recordingTime.value / 60);
  const seconds = recordingTime.value % 60;
  return `${minutes}:${seconds.toString().padStart(2, "0")}`;
});

const buttonSeverity = computed(() => {
  if (isRecording.value) return "danger";
  if (isProcessing.value) return "info";
  return "secondary";
});

// Initialize
onMounted(() => {
  detectRecognitionMethod();
});

onBeforeUnmount(() => {
  cleanup();
});

// Watch for manual value changes
watch(
  () => props.modelValue,
  (newValue) => {
    if (newValue !== transcription.value) {
      transcription.value = newValue;
    }
  },
);

function detectRecognitionMethod() {
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  if (SpeechRecognition) {
    recognitionMethod.value = "Web Speech API (Browser Native)";
    initializeWebSpeechAPI();
  } else {
    recognitionMethod.value = "PhoWhisper (Backend ASR)";
  }
}

function initializeWebSpeechAPI() {
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) return;

  recognition = new SpeechRecognition();
  recognition.continuous = props.continuous;
  recognition.interimResults = props.interimResults;
  recognition.lang = props.language;

  recognition.onresult = (event: SpeechRecognitionEvent) => {
    let interimTranscript = "";
    let finalTranscript = "";

    for (let i = event.resultIndex; i < event.results.length; i++) {
      const result = event.results[i];
      if (!result || !result[0]) continue;

      const transcript = result[0].transcript;

      if (result.isFinal) {
        finalTranscript += transcript + " ";
        if (result[0].confidence) {
          confidence.value = result[0].confidence;
        }
      } else {
        interimTranscript += transcript;
      }
    }

    if (finalTranscript) {
      transcription.value = finalTranscript.trim();
      emitTranscription(transcription.value);
    } else if (props.interimResults && interimTranscript) {
      transcription.value = interimTranscript.trim();
    }
  };

  recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
    handleError(`Speech recognition error: ${event.error}`);
    stopRecording();
  };

  recognition.onend = () => {
    if (isRecording.value) {
      if (props.continuous) {
        recognition.start();
      } else {
        stopRecording();
      }
    }
  };
}

async function toggleRecording() {
  if (isRecording.value) {
    stopRecording();
  } else {
    await startRecording();
  }
}

async function startRecording() {
  try {
    error.value = null;
    transcription.value = "";
    confidence.value = null;
    recordingTime.value = 0;

    if (recognition) {
      recognition.start();
      isRecording.value = true;
      startTimer();
      emit("recording-start");
    } else {
      await startMediaRecording();
    }
  } catch (err) {
    handleError(
      "Failed to start recording. Please check microphone permissions.",
    );
  }
}

async function startMediaRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.push(event.data);
      }
    };

    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
      await processAudioWithBackend(audioBlob);

      stream.getTracks().forEach((track) => track.stop());
    };

    mediaRecorder.start();
    isRecording.value = true;
    startTimer();
    emit("recording-start");
  } catch (err) {
    handleError("Failed to access microphone. Please check permissions.");
  }
}

function stopRecording() {
  if (!isRecording.value) return;

  isRecording.value = false;
  stopTimer();

  if (recognition) {
    recognition.stop();
  }

  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
  }

  emit("recording-stop");
}

async function processAudioWithBackend(audioBlob: Blob) {
  isProcessing.value = true;

  try {
    const token = localStorage.getItem("access_token");
    const headers = {
      Authorization: `Bearer ${token}`,
    };

    const statusResponse = await axios.get("/api/asr/status/", { headers });

    if (!statusResponse.data.available) {
      throw new Error(
        "ASR service is not available. Please contact administrator.",
      );
    }

    const formData = new FormData();
    formData.append("audio", audioBlob, "recording.wav");
    formData.append("language", props.language.startsWith("vi") ? "vi" : "en");
    formData.append("return_timestamps", "false");

    const response = await axios.post("/api/asr/transcribe/", formData, {
      headers: {
        ...headers,
        "Content-Type": "multipart/form-data",
      },
    });

    if (response.data.success) {
      transcription.value = response.data.text;
      emitTranscription(transcription.value);
    } else {
      throw new Error(response.data.error || "Transcription failed");
    }
  } catch (err: any) {
    handleError(
      err.response?.data?.error || err.message || "Failed to transcribe audio",
    );
  } finally {
    isProcessing.value = false;
  }
}

function startTimer() {
  recordingInterval = setInterval(() => {
    recordingTime.value++;

    if (recordingTime.value >= props.maxDuration) {
      stopRecording();
      handleError(
        `Recording stopped: Maximum duration of ${props.maxDuration} seconds reached`,
      );
    }
  }, 1000);
}

function stopTimer() {
  if (recordingInterval) {
    clearInterval(recordingInterval);
    recordingInterval = null;
  }
}

function emitTranscription(text: string) {
  if (props.autoApply) {
    emit("update:modelValue", text);
  }
  emit("transcription", text);
}

function clearTranscription() {
  transcription.value = "";
  confidence.value = null;
  emit("update:modelValue", "");
}

function handleError(message: string) {
  error.value = message;
  emit("error", message);
}

function cleanup() {
  if (isRecording.value) {
    stopRecording();
  }

  stopTimer();

  if (mediaRecorder) {
    mediaRecorder = null;
  }

  audioChunks = [];
}

defineExpose({
  startRecording,
  stopRecording,
  clearTranscription,
  isRecording,
  transcription,
});
</script>

<style scoped>
.voice-to-text-inline {
  display: inline-flex;
  align-items: center;
  position: relative;
  gap: 0.5rem;
}

/* PrimeVue Button customization */
.voice-btn {
  width: 2.75rem !important;
  height: 2.75rem !important;
  min-width: 2.75rem !important;
  padding: 0 !important;
  position: relative;
  overflow: visible !important;
  /* Consistent border radius — no sharp/acute stacking */
  border-radius: 50% !important;
}

.voice-btn :deep(.p-button-label) {
  display: none;
}

.voice-btn i {
  font-size: 1.125rem;
}

.voice-btn-recording {
  animation: pulse-border 1.5s ease-in-out infinite;
}

.voice-btn-processing {
  cursor: wait !important;
}

/* Recording pulse animation for the icon */
.recording-pulse {
  animation: pulse-icon 1s ease-in-out infinite;
  color: var(--p-red-500, #ef4444);
}

@keyframes pulse-border {
  0%,
  100% {
    box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.4);
  }
  50% {
    box-shadow: 0 0 0 6px rgba(220, 38, 38, 0.1);
  }
}

@keyframes pulse-icon {
  0%,
  100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.15);
  }
}

/* Timer Badge positioning */
.timer-badge {
  position: absolute !important;
  top: -0.5rem !important;
  right: -0.5rem !important;
  font-size: 0.625rem !important;
  font-family: "Monaco", "Courier New", monospace !important;
  min-width: auto !important;
  padding: 0.125rem 0.375rem !important;
  z-index: 100 !important;
  color: white !important;
  /* Ensure badge doesn't stack border-radius against the button */
  border-radius: 999px !important;
}

/* Error Message styling — floated above the button */
.error-message {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  margin-bottom: 0.5rem;
  white-space: nowrap;
  max-width: 250px;
  z-index: 50;
  /* Override any PrimeVue default border-radius stacking */
  border-radius: var(--radius, 0.5rem) !important;
}

.error-message :deep(.p-message-text) {
  font-size: 0.75rem;
}

/* Small variant */
.voice-to-text-small .voice-btn {
  width: 1.5rem !important;
  height: 1.5rem !important;
  min-width: 1.5rem !important;
}

.voice-to-text-small .voice-btn i {
  font-size: 0.75rem;
}

.voice-to-text-small .timer-badge {
  top: -0.375rem !important;
  right: -0.375rem !important;
  font-size: 0.5rem !important;
  padding: 0.0625rem 0.25rem !important;
}
</style>
