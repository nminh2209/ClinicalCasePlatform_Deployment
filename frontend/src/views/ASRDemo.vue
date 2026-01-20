<template>
  <div class="asr-demo">
    <h1>🎤 Voice-to-Text Demo</h1>
    <p class="subtitle">Test the ASR component with different configurations</p>

    <!-- Example 1: Basic Usage -->
    <section class="demo-section">
      <h2>1. Basic Usage</h2>
      <p>Simple voice-to-text with default settings</p>
      
      <div class="demo-box">
        <VoiceToText v-model="basicText" />
        
        <div v-if="basicText" class="output">
          <strong>Output:</strong>
          <pre>{{ basicText }}</pre>
        </div>
      </div>
      
      <details class="code-snippet">
        <summary>View Code</summary>
        <pre><code>&lt;VoiceToText v-model="basicText" /&gt;</code></pre>
      </details>
    </section>

    <!-- Example 2: Vietnamese Language -->
    <section class="demo-section">
      <h2>2. Vietnamese Language (Optimized)</h2>
      <p>Optimized for Vietnamese with custom text</p>
      
      <div class="demo-box">
        <VoiceToText
          v-model="vietnameseText"
          language="vi-VN"
          idle-text="Nhấn để bắt đầu ghi âm"
          recording-text="Đang ghi âm..."
          processing-text="Đang xử lý âm thanh..."
        />
        
        <div v-if="vietnameseText" class="output">
          <strong>Văn bản:</strong>
          <pre>{{ vietnameseText }}</pre>
        </div>
      </div>
      
      <details class="code-snippet">
        <summary>View Code</summary>
        <pre><code>&lt;VoiceToText
  v-model="vietnameseText"
  language="vi-VN"
  idle-text="Nhấn để bắt đầu ghi âm"
  recording-text="Đang ghi âm..."
  processing-text="Đang xử lý âm thanh..."
/&gt;</code></pre>
      </details>
    </section>

    <!-- Example 3: Form Integration -->
    <section class="demo-section">
      <h2>3. Form Integration</h2>
      <p>Integrate voice input into a medical case form</p>
      
      <div class="demo-box">
        <form @submit.prevent="submitForm" class="case-form">
          <div class="form-group">
            <label>Patient Symptoms</label>
            <textarea
              v-model="formData.symptoms"
              rows="3"
              placeholder="Enter symptoms or use voice input..."
            ></textarea>
            <VoiceToText
              v-model="formData.symptoms"
              language="vi-VN"
              :max-duration="60"
            />
          </div>

          <div class="form-group">
            <label>Medical History</label>
            <textarea
              v-model="formData.history"
              rows="3"
              placeholder="Enter medical history or use voice input..."
            ></textarea>
            <VoiceToText
              v-model="formData.history"
              language="vi-VN"
              :max-duration="120"
            />
          </div>

          <div class="form-group">
            <label>Physical Examination</label>
            <textarea
              v-model="formData.examination"
              rows="3"
              placeholder="Enter examination findings or use voice input..."
            ></textarea>
            <VoiceToText
              v-model="formData.examination"
              language="vi-VN"
              :max-duration="120"
            />
          </div>

          <button type="submit" class="submit-btn">Submit Case</button>
        </form>

        <div v-if="formSubmitted" class="output success">
          <strong>✅ Form Submitted Successfully!</strong>
          <pre>{{ JSON.stringify(formData, null, 2) }}</pre>
        </div>
      </div>
      
      <details class="code-snippet">
        <summary>View Code</summary>
        <pre><code>&lt;form @submit.prevent="submitForm"&gt;
  &lt;div class="form-group"&gt;
    &lt;label&gt;Patient Symptoms&lt;/label&gt;
    &lt;textarea v-model="formData.symptoms"&gt;&lt;/textarea&gt;
    &lt;VoiceToText
      v-model="formData.symptoms"
      language="vi-VN"
      :max-duration="60"
    /&gt;
  &lt;/div&gt;
  &lt;!-- More fields... --&gt;
  &lt;button type="submit"&gt;Submit&lt;/button&gt;
&lt;/form&gt;</code></pre>
      </details>
    </section>

    <!-- Example 4: Advanced Features -->
    <section class="demo-section">
      <h2>4. Advanced Features</h2>
      <p>Longer recordings with event handlers and method info</p>
      
      <div class="demo-box">
        <VoiceToText
          v-model="advancedText"
          language="vi-VN"
          :max-duration="180"
          :show-method-info="true"
          @transcription="onTranscription"
          @error="onError"
          @recording-start="onRecordingStart"
          @recording-stop="onRecordingStop"
        />
        
        <div class="event-log">
          <strong>Event Log:</strong>
          <div
            v-for="(event, index) in eventLog"
            :key="index"
            class="event-item"
          >
            <span class="event-time">{{ event.time }}</span>
            <span :class="['event-type', event.type]">{{ event.type }}</span>
            <span class="event-message">{{ event.message }}</span>
          </div>
        </div>
      </div>
      
      <details class="code-snippet">
        <summary>View Code</summary>
        <pre><code>&lt;VoiceToText
  v-model="advancedText"
  language="vi-VN"
  :max-duration="180"
  :show-method-info="true"
  @transcription="onTranscription"
  @error="onError"
  @recording-start="onRecordingStart"
  @recording-stop="onRecordingStop"
/&gt;</code></pre>
      </details>
    </section>

    <!-- Example 5: Programmatic Control -->
    <section class="demo-section">
      <h2>5. Programmatic Control</h2>
      <p>Control recording with external buttons</p>
      
      <div class="demo-box">
        <div class="control-buttons">
          <button @click="startRecording" class="control-btn start">
            ▶️ Start Recording
          </button>
          <button @click="stopRecording" class="control-btn stop">
            ⏹️ Stop Recording
          </button>
          <button @click="clearTranscription" class="control-btn clear">
            🗑️ Clear
          </button>
        </div>

        <VoiceToText
          ref="voiceRef"
          v-model="controlledText"
          language="vi-VN"
        />

        <div v-if="controlledText" class="output">
          <strong>Transcription:</strong>
          <pre>{{ controlledText }}</pre>
        </div>
      </div>
      
      <details class="code-snippet">
        <summary>View Code</summary>
        <pre><code>&lt;template&gt;
  &lt;button @click="startRecording"&gt;Start&lt;/button&gt;
  &lt;button @click="stopRecording"&gt;Stop&lt;/button&gt;
  &lt;button @click="clearTranscription"&gt;Clear&lt;/button&gt;
  
  &lt;VoiceToText ref="voiceRef" v-model="text" /&gt;
&lt;/template&gt;

&lt;script setup&gt;
import { ref } from 'vue'

const voiceRef = ref(null)

function startRecording() {
  voiceRef.value.startRecording()
}

function stopRecording() {
  voiceRef.value.stopRecording()
}

function clearTranscription() {
  voiceRef.value.clearTranscription()
}
&lt;/script&gt;</code></pre>
      </details>
    </section>

    <!-- ASR Status -->
    <section class="demo-section">
      <h2>📊 ASR Service Status</h2>
      
      <div class="demo-box">
        <button @click="checkStatus" class="control-btn">
          Check Backend Status
        </button>

        <div v-if="asrStatus" class="status-info">
          <div class="status-row">
            <span class="label">Available:</span>
            <span :class="['value', asrStatus.available ? 'success' : 'error']">
              {{ asrStatus.available ? '✅ Yes' : '❌ No' }}
            </span>
          </div>
          <div v-if="asrStatus.model_name" class="status-row">
            <span class="label">Model:</span>
            <span class="value">{{ asrStatus.model_name }}</span>
          </div>
          <div v-if="asrStatus.device" class="status-row">
            <span class="label">Device:</span>
            <span class="value">{{ asrStatus.device }}</span>
          </div>
          <div v-if="asrStatus.language_support" class="status-row">
            <span class="label">Languages:</span>
            <span class="value">{{ asrStatus.language_support.join(', ') }}</span>
          </div>
          <div v-if="asrStatus.description" class="status-row">
            <span class="label">Description:</span>
            <span class="value">{{ asrStatus.description }}</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import VoiceToText from '@/components/VoiceToText.vue'
import axios from 'axios'

// Example 1: Basic
const basicText = ref('')

// Example 2: Vietnamese
const vietnameseText = ref('')

// Example 3: Form
const formData = ref({
  symptoms: '',
  history: '',
  examination: ''
})
const formSubmitted = ref(false)

function submitForm() {
  console.log('Form submitted:', formData.value)
  formSubmitted.value = true
  
  setTimeout(() => {
    formSubmitted.value = false
  }, 5000)
}

// Example 4: Advanced
const advancedText = ref('')
const eventLog = ref([])

function addEvent(type, message) {
  const now = new Date()
  const time = now.toLocaleTimeString()
  
  eventLog.value.unshift({
    time,
    type,
    message
  })
  
  // Keep only last 10 events
  if (eventLog.value.length > 10) {
    eventLog.value.pop()
  }
}

function onTranscription(text) {
  addEvent('transcription', `Transcribed: ${text.substring(0, 50)}...`)
}

function onError(error) {
  addEvent('error', error)
}

function onRecordingStart() {
  addEvent('info', 'Recording started')
}

function onRecordingStop() {
  addEvent('info', 'Recording stopped')
}

// Example 5: Programmatic Control
const voiceRef = ref(null)
const controlledText = ref('')

function startRecording() {
  voiceRef.value?.startRecording()
}

function stopRecording() {
  voiceRef.value?.stopRecording()
}

function clearTranscription() {
  voiceRef.value?.clearTranscription()
}

// ASR Status
const asrStatus = ref(null)

async function checkStatus() {
  try {
    const response = await axios.get('/api/asr/status/')
    asrStatus.value = response.data
    addEvent('info', 'ASR status checked successfully')
  } catch (error) {
    addEvent('error', 'Failed to check ASR status: ' + error.message)
  }
}
</script>

<style scoped>
.asr-demo {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  color: #333;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #666;
  margin-bottom: 3rem;
}

.demo-section {
  margin-bottom: 4rem;
}

.demo-section h2 {
  color: #667eea;
  margin-bottom: 0.5rem;
}

.demo-section > p {
  color: #666;
  margin-bottom: 1rem;
}

.demo-box {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 2rem;
  margin-bottom: 1rem;
}

.output {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 6px;
  border-left: 4px solid #667eea;
}

.output.success {
  border-left-color: #4caf50;
  background: #e8f5e9;
}

.output strong {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
}

.output pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  color: #555;
  font-size: 0.95rem;
}

.code-snippet {
  margin-top: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 0.5rem 1rem;
  background: #fafafa;
}

.code-snippet summary {
  cursor: pointer;
  color: #667eea;
  font-weight: 600;
}

.code-snippet pre {
  margin-top: 1rem;
  background: #2d2d2d;
  color: #f8f8f2;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
}

.code-snippet code {
  font-family: 'Monaco', 'Courier New', monospace;
  font-size: 0.9rem;
}

/* Form Styles */
.case-form {
  max-width: 600px;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.form-group textarea,
.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
}

.form-group textarea:focus,
.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.submit-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.submit-btn:active {
  transform: translateY(0);
}

/* Event Log */
.event-log {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 6px;
  max-height: 300px;
  overflow-y: auto;
}

.event-log strong {
  display: block;
  margin-bottom: 0.75rem;
  color: #333;
}

.event-item {
  padding: 0.5rem;
  margin-bottom: 0.5rem;
  background: white;
  border-radius: 4px;
  display: flex;
  gap: 0.75rem;
  font-size: 0.9rem;
}

.event-time {
  color: #999;
  font-family: 'Monaco', monospace;
  font-size: 0.85rem;
}

.event-type {
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 3px;
  font-size: 0.85rem;
}

.event-type.transcription {
  background: #e3f2fd;
  color: #1565c0;
}

.event-type.error {
  background: #ffebee;
  color: #c62828;
}

.event-type.info {
  background: #e8f5e9;
  color: #2e7d32;
}

.event-message {
  flex: 1;
  color: #555;
}

/* Control Buttons */
.control-buttons {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.control-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  color: white;
}

.control-btn.start {
  background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
}

.control-btn.stop {
  background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
}

.control-btn.clear {
  background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
}

.control-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.control-btn:active {
  transform: translateY(0);
}

/* Status Info */
.status-info {
  margin-top: 1rem;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 6px;
}

.status-row {
  display: flex;
  padding: 0.5rem 0;
  border-bottom: 1px solid #e0e0e0;
}

.status-row:last-child {
  border-bottom: none;
}

.status-row .label {
  font-weight: 600;
  color: #333;
  width: 150px;
}

.status-row .value {
  flex: 1;
  color: #555;
}

.status-row .value.success {
  color: #4caf50;
}

.status-row .value.error {
  color: #f44336;
}
</style>
