<template>
  <div class="p-6 space-y-4 max-w-7xl mx-auto">
    <!-- Header -->
    <div
      class="flex items-center justify-between gap-4 bg-white p-4 rounded-lg shadow-sm"
    >
      <div class="flex items-center gap-3">
        <Button
          class="h-button"
          size="small"
          icon="pi pi-arrow-left"
          @click="$emit('navigate', 'dashboard')"
        />
        <div>
          <h1 class="text-xl font-bold text-gray-800">{{ caseData.title }}</h1>
          <div class="flex items-center gap-2 mt-1">
            <Badge variant="outlined" class="text-xs badge">{{
              caseData.specialty
            }}</Badge>
            <Badge v-if="caseStatus === 'draft'" class="text-xs p-1"
              >Bản nháp</Badge
            >
            <Badge
              severity="success"
              v-else-if="caseStatus === 'submitted'"
              class="text-xs p-1"
              >Đã nộp</Badge
            >
            <Badge
              severity="success"
              v-else-if="caseStatus === 'reviewed'"
              class="text-xs p-1"
              >Đã xem xét</Badge
            >
            <Badge
              severity="success"
              v-else-if="caseStatus === 'approved'"
              class="text-xs p-1"
              >Đã phê duyệt</Badge
            >
            <Badge
              severity="danger"
              v-if="caseData.priority_level === 'urgent'"
              class="text-xs p-1"
              >Khẩn cấp</Badge
            >
            <Badge
              severity="warn"
              v-else-if="caseData.priority_level === 'high'"
              class="text-xs p-1"
              >Cao</Badge
            >
          </div>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <Button
          class="h-button"
          size="small"
          icon="pi pi-file-pdf"
          label="Xem PDF"
          @click="exportPDF"
          :disabled="exportingPDF"
        />
        <Button
          class="h-button"
          size="small"
          icon="pi pi-save"
          label="Lưu"
          @click="handleSave"
          :disabled="!hasUnsavedChanges || !canEdit"
        />
        <Button
          class="h-button"
          size="small"
          icon="pi pi-send"
          label="Nộp"
          @click="handleSubmit"
          :disabled="!canEdit"
        />
      </div>
    </div>

    <!-- Permission Notices -->
    <Tag
      style="color: var(--destructive)"
      class="me-1"
      severity="danger"
      v-if="!canEdit && !isOwner"
      value="Bạn không phải là chủ sở hữu của ca bệnh này. Chỉ được xem."
    />
    <Tag
      style="color: var(--destructive)"
      severity="danger"
      v-if="!canEdit && !isDraft"
      value="Ca bệnh đã được nộp. Không thể chỉnh sửa."
    />

    <!-- Grade Display for Students -->
    <Card v-if="gradeData && gradeData.is_final" class="bg-white">
      <template #header>
        <div class="flex items-center justify-between p-4 pb-0">
          <div class="flex items-center gap-2">
            <div class="p-2 bg-blue-100 rounded-lg">
              <i class="pi pi-verified text-blue-700"></i>
            </div>
            <span class="font-semibold text-blue-900">Kết quả đánh giá</span>
          </div>
          <div class="text-right">
            <div class="text-3xl font-bold text-blue-900">
              {{ gradeData.score }}%
            </div>
            <div class="text-sm">
              <span class="text-gray-700">Xếp loại:</span>
              <span class="text-blue-900 font-bold">{{
                gradeData.letter_grade
              }}</span>
            </div>
          </div>
        </div>
      </template>
      <template #content>
        <div class="space-y-3">
          <div v-if="gradeData.evaluation_notes">
            <label class="text-md font-semibold text-blue-900"
              >Nhận xét chung</label
            >
            <p class="text-sm text-gray-700 mt-1 whitespace-pre-wrap">
              {{ gradeData.evaluation_notes }}
            </p>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div v-if="gradeData.strengths">
              <label class="text-md text-blue-900 font-semibold"
                >Điểm mạnh</label
              >
              <p class="text-sm text-gray-700 mt-1 whitespace-pre-wrap">
                {{ gradeData.strengths }}
              </p>
            </div>
            <div v-if="gradeData.weaknesses">
              <label class="text-md font-semibold text-blue-900"
                >Cần cải thiện</label
              >
              <p class="text-sm text-gray-700 mt-1 whitespace-pre-wrap">
                {{ gradeData.weaknesses }}
              </p>
            </div>
          </div>
          <div v-if="gradeData.recommendations">
            <label class="text-md font-semibold text-blue-900"
              >Khuyến nghị</label
            >
            <p class="text-sm text-gray-700 mt-1 whitespace-pre-wrap">
              {{ gradeData.recommendations }}
            </p>
          </div>
          <div v-if="gradeData.grading_criteria" class="border-t pt-3">
            <label class="text-md font-semibold text-blue-900 mb-2 block"
              >Tiêu chí đánh giá chi tiết</label
            >
            <div class="grid grid-cols-2 md:grid-cols-5 gap-2">
              <div
                class="text-center p-2 bg-white rounded border border-gray-100"
              >
                <div class="text-xs text-gray-500">Tiền sử</div>
                <div class="text-2xl font-bold text-blue-900">
                  {{ gradeData.grading_criteria.history || 0 }}
                </div>
              </div>
              <div
                class="text-center p-2 bg-white rounded border border-gray-100"
              >
                <div class="text-xs text-gray-500">Khám</div>
                <div class="text-2xl font-bold text-blue-900">
                  {{ gradeData.grading_criteria.examination || 0 }}
                </div>
              </div>
              <div
                class="text-center p-2 bg-white rounded border border-gray-100"
              >
                <div class="text-xs text-gray-500">Chẩn đoán</div>
                <div class="text-2xl font-bold text-blue-900">
                  {{ gradeData.grading_criteria.differential || 0 }}
                </div>
              </div>
              <div
                class="text-center p-2 bg-white rounded border border-gray-100"
              >
                <div class="text-xs text-gray-500">Điều trị</div>
                <div class="text-2xl font-bold text-blue-900">
                  {{ gradeData.grading_criteria.treatment || 0 }}
                </div>
              </div>
              <div
                class="text-center p-2 bg-white rounded border border-gray-100"
              >
                <div class="text-xs text-gray-500">Trình bày</div>
                <div class="text-2xl font-bold text-blue-900">
                  {{ gradeData.grading_criteria.presentation || 0 }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </Card>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <!-- Left Column: Collapsible Case Information Sections -->
      <div class="space-y-3">
        <!-- Basic Information -->
        <div
          class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden"
        >
          <Button
            text
            class="w-full p-4 flex items-center justify-between"
            @click="toggleSection('basic')"
          >
            <div class="flex items-center gap-2">
              <i class="pi pi-info-circle text-gray-600"></i>
              <span class="font-semibold text-base">Thông tin cơ bản</span>
            </div>
            <i
              :class="[
                'pi pi-chevron-down text-gray-400 transition-transform duration-200',
                expandedSections.basic && 'rotate-180',
              ]"
            ></i>
          </Button>
          <div v-if="expandedSections.basic" class="px-4 pb-4 space-y-3 mt-6">
            <div class="grid grid-cols-2 gap-3">
              <div class="flex flex-col gap-2">
                <label for="tieude" class="text-xs text-gray-500"
                  >Tiêu đề</label
                >
                <InputText
                  id="tieude"
                  v-model="caseData.title"
                  placeholder="Nhập tiêu đề..."
                  :disabled="!canEdit"
                  class="text-sm"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label for="chuyenkhoa" class="text-xs text-gray-500"
                  >Chuyên khoa</label
                >
                <Select
                  id="chuyenkhoa"
                  v-model="caseData.specialty"
                  :options="specialties"
                  option-label="name"
                  option-value="name"
                  :placeholder="
                    choicesLoading ? 'Đang tải...' : 'Chọn chuyên khoa'
                  "
                  class="w-full text-sm"
                  :disabled="!canEdit || choicesLoading"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label for="uutien" class="text-xs text-gray-500"
                  >Mức độ ưu tiên</label
                >
                <Select
                  id="uutien"
                  v-model="caseData.priority_level"
                  :options="priorities"
                  option-label="name"
                  option-value="key"
                  :placeholder="choicesLoading ? 'Đang tải...' : 'Chọn mức độ'"
                  class="w-full text-sm"
                  :disabled="!canEdit || choicesLoading"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label for="phuctap" class="text-xs text-gray-500"
                  >Mức độ phức tạp</label
                >
                <Select
                  id="phuctap"
                  v-model="caseData.complexity_level"
                  :options="complexities"
                  option-label="name"
                  option-value="key"
                  :placeholder="choicesLoading ? 'Đang tải...' : 'Chọn mức độ'"
                  class="w-full text-sm"
                  :disabled="!canEdit || choicesLoading"
                />
              </div>
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label for="tomtat" class="text-xs text-gray-500"
                  >Tóm tắt ca bệnh</label
                >
                <VoiceToText v-model="caseData.case_summary" size="small" />
              </div>
              <Textarea
                id="tomtat"
                v-model="caseData.case_summary"
                placeholder="Tóm tắt ngắn gọn..."
                :disabled="!canEdit"
                rows="2"
                class="text-sm"
              />
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div class="flex flex-col gap-2">
                <label for="tag" class="text-xs text-gray-500"
                  >Tags học tập</label
                >
                <InputText
                  id="tag"
                  v-model="caseData.learning_tags"
                  placeholder="tim mạch, cấp cứu"
                  :disabled="!canEdit"
                  class="text-sm"
                />
              </div>
              <div>
                <label class="text-xs text-gray-500">Giờ học ước tính</label>
                <InputNumber
                  showButtons
                  fluid
                  v-model="caseData.estimated_study_hours"
                  placeholder="Số giờ"
                  :disabled="!canEdit"
                  class="text-sm"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Patient Information -->
        <div
          class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden"
        >
          <Button
            text
            class="w-full p-4 flex items-center justify-between"
            @click="toggleSection('patient')"
          >
            <div class="flex items-center gap-2">
              <i class="pi pi-user text-gray-600"></i>
              <span class="font-semibold text-base">Thông tin bệnh nhân</span>
            </div>
            <i
              :class="[
                'pi pi-chevron-down text-gray-400 transition-transform duration-200',
                expandedSections.patient && 'rotate-180',
              ]"
            ></i>
          </Button>
          <div v-if="expandedSections.patient" class="px-4 pb-4 space-y-3 mt-6">
            <div class="grid grid-cols-2 gap-4">
              <input type="hidden" v-model="caseData.patient_name" />
              <div class="flex flex-col gap-2">
                <label for="age" class="text-sm text-gray-500">Tuổi</label>
                <InputText
                  id="age"
                  v-model="caseData.patient_age"
                  placeholder="Tuổi..."
                  :disabled="!canEdit"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label for="gender" class="text-sm text-gray-500"
                  >Giới tính</label
                >
                <Select
                  id="gender"
                  v-model="caseData.patient_gender"
                  :options="genderOptions"
                  option-label="name"
                  option-value="value"
                  placeholder="Chọn giới tính"
                  class="w-full"
                  :disabled="!canEdit"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label for="rn" class="text-sm text-gray-500"
                  >Số hồ sơ bệnh án</label
                >
                <InputText
                  id="rn"
                  v-model="caseData.medical_record_number"
                  placeholder="Số hồ sơ..."
                  :disabled="!canEdit"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label for="dantoc" class="text-sm text-gray-500"
                  >Dân tộc</label
                >
                <InputText
                  id="dantoc"
                  v-model="caseData.patient_ethnicity"
                  placeholder="Dân tộc bệnh nhân..."
                  :disabled="!canEdit"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label for="job" class="text-sm text-gray-500"
                  >Nghề nghiệp</label
                >
                <InputText
                  id="job"
                  v-model="caseData.patient_occupation"
                  placeholder="Nghề nghiệp..."
                  :disabled="!canEdit"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-sm text-gray-500">Ngày nhập viện</label>
                <InputText
                  v-model="caseData.admission_date"
                  type="date"
                  :disabled="!canEdit"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-sm text-gray-500">Ngày xuất viện</label>
                <InputText
                  v-model="caseData.discharge_date"
                  type="date"
                  :disabled="!canEdit"
                />
              </div>
            </div>
            <div class="flex flex-col gap-2">
              <label class="text-sm text-gray-500">Lý do khám ngắn gọn</label>
              <InputText
                v-model="caseData.chief_complaint_brief"
                placeholder="Lý do chính đến khám..."
                :disabled="!canEdit"
              />
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div class="flex items-center space-x-2">
                <Checkbox
                  v-model="caseData.requires_follow_up"
                  :disabled="!canEdit"
                  binary
                />
                <label class="text-sm text-gray-500">Yêu cầu theo dõi</label>
              </div>
              <div v-if="caseData.requires_follow_up">
                <label class="text-sm text-gray-500">Ngày theo dõi</label>
                <InputText
                  v-model="caseData.follow_up_date"
                  type="date"
                  :disabled="!canEdit"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Clinical History -->
        <div
          class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden"
        >
          <Button
            text
            class="w-full p-5 flex items-center justify-between"
            @click="toggleSection('clinical')"
          >
            <div class="flex items-center gap-2">
              <i class="pi pi-book text-gray-600"></i>
              <span class="font-semibold text-base">Tiền sử lâm sàng</span>
            </div>
            <i
              :class="[
                'pi pi-chevron-down text-gray-400 transition-transform duration-200',
                expandedSections.clinical && 'rotate-180',
              ]"
            ></i>
          </Button>
          <div v-if="expandedSections.clinical" class="px-4 pb-4 space-y-3 mt-6">
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Lý do khám chính</label>
                <VoiceToText
                  v-model="caseData.clinical_history.chief_complaint"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.clinical_history.chief_complaint"
                placeholder="Lý do khám chính..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Bệnh sử hiện tại</label>
                <VoiceToText
                  v-model="caseData.clinical_history.history_present_illness"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.clinical_history.history_present_illness"
                placeholder="Bệnh sử hiện tại..."
                :disabled="!canEdit"
              />
            </div>
            <div class="grid grid-cols-3 gap-4">
              <div class="flex flex-col gap-2">
                <label class="text-sm text-gray-500"
                  >Thời gian có triệu chứng</label
                >
                <InputNumber
                  v-model="caseData.clinical_history.symptom_duration_days"
                  showButtons
                  fluid
                  placeholder="Số ngày..."
                  :disabled="!canEdit"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-sm text-gray-500"
                  >Khởi phát triệu chứng</label
                >
                <Select
                  v-model="caseData.clinical_history.symptom_onset"
                  :options="symptomOnsetOptions"
                  option-label="name"
                  option-value="value"
                  placeholder="Chọn"
                  class="w-full"
                  :disabled="!canEdit"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-sm text-gray-500"
                  >Diễn biến triệu chứng</label
                >
                <Select
                  v-model="caseData.clinical_history.symptom_progression"
                  :options="symptomProgressionOptions"
                  option-label="name"
                  option-value="value"
                  placeholder="Chọn"
                  class="w-full"
                  :disabled="!canEdit"
                />
              </div>
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Tiền sử bệnh tật</label>
                <VoiceToText
                  v-model="caseData.clinical_history.past_medical_history"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.clinical_history.past_medical_history"
                placeholder="Tiền sử bệnh tật..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Tiền sử gia đình</label>
                <VoiceToText
                  v-model="caseData.clinical_history.family_history"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.clinical_history.family_history"
                placeholder="Tiền sử gia đình..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500"
                  >Tiền sử xã hội (hút thuốc, uống rượu, v.v.)</label
                >
                <VoiceToText
                  v-model="caseData.clinical_history.social_history"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.clinical_history.social_history"
                placeholder="Tiền sử xã hội..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Dị ứng</label>
                <VoiceToText
                  v-model="caseData.clinical_history.allergies"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.clinical_history.allergies"
                placeholder="Các chất gây dị ứng..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Thuốc đang sử dụng</label>
                <VoiceToText
                  v-model="caseData.clinical_history.medications"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.clinical_history.medications"
                placeholder="Thuốc đang dùng..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500"
                  >Hỏi bệnh theo hệ thống</label
                >
                <VoiceToText
                  v-model="caseData.clinical_history.review_systems"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.clinical_history.review_systems"
                placeholder="Đánh giá các hệ thống..."
                :disabled="!canEdit"
              />
            </div>
          </div>
        </div>

        <!-- Physical Examination -->
        <div
          class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden"
        >
          <Button
            text
            class="w-full p-4 flex items-center justify-between"
            @click="toggleSection('physical')"
          >
            <div class="flex items-center gap-2">
              <i class="pi pi-heart text-gray-600"></i>
              <span class="font-semibold text-base">Khám lâm sàng</span>
            </div>
            <i
              :class="[
                'pi pi-chevron-down text-gray-400 transition-transform duration-200',
                expandedSections.physical && 'rotate-180',
              ]"
            ></i>
          </Button>
          <div v-if="expandedSections.physical" class="px-4 pb-4 space-y-3 mt-6">
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Tình trạng chung</label>
                <VoiceToText
                  v-model="caseData.physical_examination.general_appearance"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.physical_examination.general_appearance"
                placeholder="Tình trạng chung..."
                :disabled="!canEdit"
              />
            </div>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
              <div>
                <label class="text-sm text-gray-500">Nhiệt Độ (°C)</label>
                <InputNumber
                  showButtons
                  fluid
                  v-model="caseData.physical_examination.vital_signs_temp"
                  :step="0.1"
                  placeholder="37.0"
                  :disabled="!canEdit"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-sm text-gray-500">Nhịp Tim (BPM)</label>
                <InputNumber
                  showButtons
                  fluid
                  v-model="caseData.physical_examination.vital_signs_hr"
                  placeholder="72"
                  :disabled="!canEdit"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-sm text-gray-500">Huyết Áp (mmHg)</label>
                <InputText
                  fluid
                  v-model="caseData.physical_examination.vital_signs_bp"
                  placeholder="120/80"
                  :disabled="!canEdit"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-sm text-gray-500">Nhịp Thở (lần/phút)</label>
                <InputNumber
                  fluid
                  showButtons
                  v-model="caseData.physical_examination.vital_signs_rr"
                  placeholder="16"
                  :disabled="!canEdit"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-sm text-gray-500">Độ Bão Hòa Oxy (%)</label>
                <InputNumber
                  fluid
                  showButtons
                  v-model="caseData.physical_examination.vital_signs_spo2"
                  placeholder="98"
                  :disabled="!canEdit"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-sm text-gray-500">Cân Nặng (kg)</label>
                <InputNumber
                  fluid
                  showButtons
                  v-model="caseData.physical_examination.weight_kg"
                  :step="0.1"
                  placeholder="70"
                  :disabled="!canEdit"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-sm text-gray-500">Chiều Cao (cm)</label>
                <InputNumber
                  fluid
                  showButtons
                  v-model="caseData.physical_examination.height_cm"
                  :step="0.1"
                  placeholder="170"
                  :disabled="!canEdit"
                />
              </div>
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Sinh hiệu (Ghi chú)</label>
                <VoiceToText
                  v-model="caseData.physical_examination.vital_signs"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.physical_examination.vital_signs"
                placeholder="Ghi chú về sinh hiệu..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Tim mạch</label>
                <VoiceToText
                  v-model="caseData.physical_examination.cardiovascular"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.physical_examination.cardiovascular"
                placeholder="Khám tim mạch..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Hô hấp</label>
                <VoiceToText
                  v-model="caseData.physical_examination.respiratory"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.physical_examination.respiratory"
                placeholder="Khám hô hấp..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Bụng</label>
                <VoiceToText
                  v-model="caseData.physical_examination.abdominal"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.physical_examination.abdominal"
                placeholder="Khám bụng..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Thần kinh</label>
                <VoiceToText
                  v-model="caseData.physical_examination.neurological"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.physical_examination.neurological"
                placeholder="Khám thần kinh..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Cơ xương khớp</label>
                <VoiceToText
                  v-model="caseData.physical_examination.musculoskeletal"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.physical_examination.musculoskeletal"
                placeholder="Khám cơ xương khớp..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Da</label>
                <VoiceToText
                  v-model="caseData.physical_examination.skin"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.physical_examination.skin"
                placeholder="Khám da..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Đầu và cổ</label>
                <VoiceToText
                  v-model="caseData.physical_examination.head_neck"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.physical_examination.head_neck"
                placeholder="Khám đầu và cổ..."
                :disabled="!canEdit"
              />
            </div>
          </div>
        </div>

        <!-- Investigations -->
        <div
          class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden"
        >
          <Button
            text
            class="w-full p-4 flex items-center justify-between"
            @click="toggleSection('investigations')"
          >
            <div class="flex items-center gap-2">
              <i class="pi pi-search text-gray-600"></i>
              <span class="font-semibold text-base">Cận lâm sàng</span>
            </div>
            <i
              :class="[
                'pi pi-chevron-down text-gray-400 transition-transform duration-200',
                expandedSections.investigations && 'rotate-180',
              ]"
            ></i>
          </Button>
          <div
            v-if="expandedSections.investigations"
            class="px-4 pb-4 space-y-3 mt-6"
          >
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500"
                  >Xét nghiệm (Tổng quan)</label
                >
                <VoiceToText
                  v-model="caseData.investigations.laboratory_results"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.investigations.laboratory_results"
                placeholder="Kết quả xét nghiệm tổng quan..."
                :disabled="!canEdit"
              />
            </div>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
              <div class="flex flex-col gap-2">
                <label class="text-sm text-gray-500">Hemoglobin (g/dL)</label>
                <InputNumber
                  fluid
                  showButtons
                  v-model="caseData.investigations.hemoglobin_level"
                  :step="0.1"
                  placeholder="14.0"
                  :disabled="!canEdit"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-sm text-gray-500"
                  >Số Lượng Bạch Cầu (10^9/L)</label
                >
                <InputNumber
                  fluid
                  showButtons
                  v-model="caseData.investigations.white_cell_count"
                  :step="0.1"
                  placeholder="7.5"
                  :disabled="!canEdit"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-sm text-gray-500"
                  >Số Lượng Tiểu Cầu (10^9/L)</label
                >
                <InputNumber
                  fluid
                  showButtons
                  v-model="caseData.investigations.platelet_count"
                  placeholder="250"
                  :disabled="!canEdit"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-sm text-gray-500">Natri (mmol/L)</label>
                <InputNumber
                  fluid
                  showButtons
                  v-model="caseData.investigations.sodium_level"
                  :step="0.1"
                  placeholder="140"
                  :disabled="!canEdit"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-sm text-gray-500">Kali (mmol/L)</label>
                <InputNumber
                  fluid
                  showButtons
                  v-model="caseData.investigations.potassium_level"
                  :step="0.1"
                  placeholder="4.0"
                  :disabled="!canEdit"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-sm text-gray-500">Creatinine (mg/dL)</label>
                <InputNumber
                  fluid
                  showButtons
                  v-model="caseData.investigations.creatinine_level"
                  :step="0.1"
                  placeholder="1.0"
                  :disabled="!canEdit"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-sm text-gray-500">Glucose (mg/dL)</label>
                <InputNumber
                  fluid
                  showButtons
                  v-model="caseData.investigations.glucose_level"
                  placeholder="100"
                  :disabled="!canEdit"
                />
              </div>
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Chẩn đoán hình ảnh</label>
                <VoiceToText
                  v-model="caseData.investigations.imaging_studies"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.investigations.imaging_studies"
                placeholder="Kết quả chẩn đoán hình ảnh..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Điện tâm đồ</label>
                <VoiceToText
                  v-model="caseData.investigations.ecg_findings"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.investigations.ecg_findings"
                placeholder="Kết quả điện tâm đồ..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500"
                  >Kết quả giải phẫu bệnh</label
                >
                <VoiceToText
                  v-model="caseData.investigations.pathology_results"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.investigations.pathology_results"
                placeholder="Kết quả giải phẫu bệnh..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Kết quả Vi sinh</label>
                <VoiceToText
                  v-model="caseData.investigations.microbiology_results"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.investigations.microbiology_results"
                placeholder="Kết quả vi sinh..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Xét nghiệm khác</label>
                <VoiceToText
                  v-model="caseData.investigations.other_investigations"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.investigations.other_investigations"
                placeholder="Các xét nghiệm khác..."
                :disabled="!canEdit"
              />
            </div>
          </div>
        </div>

        <!-- Diagnosis and Management -->
        <div
          class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden"
        >
          <Button
            text
            class="w-full p-4 flex items-center justify-between"
            @click="toggleSection('diagnosis')"
          >
            <div class="flex items-center gap-2">
              <i class="pi pi-tag text-gray-600"></i>
              <span class="font-semibold text-base">Chẩn đoán và điều trị</span>
            </div>
            <i
              :class="[
                'pi pi-chevron-down text-gray-400 transition-transform duration-200',
                expandedSections.diagnosis && 'rotate-180',
              ]"
            ></i>
          </Button>
          <div v-if="expandedSections.diagnosis" class="px-4 pb-4 space-y-3 mt-6">
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Chẩn đoán chính</label>
                <VoiceToText
                  v-model="caseData.diagnosis_management.primary_diagnosis"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.diagnosis_management.primary_diagnosis"
                placeholder="Chẩn đoán chính..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Chẩn đoán phân biệt</label>
                <VoiceToText
                  v-model="caseData.diagnosis_management.differential_diagnosis"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.diagnosis_management.differential_diagnosis"
                placeholder="Các chẩn đoán phân biệt..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <label class="text-sm text-gray-500">Mã ICD-10</label>
              <InputText
                v-model="caseData.diagnosis_management.icd10_codes"
                placeholder="Mã ICD-10..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Kế hoạch điều trị</label>
                <VoiceToText
                  v-model="caseData.diagnosis_management.treatment_plan"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.diagnosis_management.treatment_plan"
                placeholder="Kế hoạch điều trị..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500"
                  >Thủ thuật đã thực hiện</label
                >
                <VoiceToText
                  v-model="caseData.diagnosis_management.procedures_performed"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.diagnosis_management.procedures_performed"
                placeholder="Các thủ thuật đã thực hiện..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Tiên lượng</label>
                <VoiceToText
                  v-model="caseData.diagnosis_management.prognosis"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.diagnosis_management.prognosis"
                placeholder="Tiên lượng bệnh..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Kế hoạch theo dõi</label>
                <VoiceToText
                  v-model="caseData.diagnosis_management.follow_up_plan"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.diagnosis_management.follow_up_plan"
                placeholder="Kế hoạch theo dõi..."
                :disabled="!canEdit"
              />
            </div>
          </div>
        </div>

        <!-- Learning Outcomes -->
        <div
          class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden"
        >
          <Button
            text
            class="w-full p-4 flex items-center justify-between"
            @click="toggleSection('learning')"
          >
            <div class="flex items-center gap-2">
              <i class="pi pi-graduation-cap text-gray-600"></i>
              <span class="font-semibold text-base">Kết quả học tập</span>
            </div>
            <i
              :class="[
                'pi pi-chevron-down text-gray-400 transition-transform duration-200',
                expandedSections.learning && 'rotate-180',
              ]"
            ></i>
          </Button>
          <div v-if="expandedSections.learning" class="px-4 pb-4 space-y-3 mt-6">
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Mục tiêu học tập</label>
                <VoiceToText
                  v-model="caseData.learning_outcomes.learning_objectives"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.learning_outcomes.learning_objectives"
                placeholder="Mục tiêu học tập từ ca bệnh này..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Khái niệm chính</label>
                <VoiceToText
                  v-model="caseData.learning_outcomes.key_concepts"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.learning_outcomes.key_concepts"
                placeholder="Các khái niệm y khoa chính..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500"
                  >Kinh nghiệm lâm sàng</label
                >
                <VoiceToText
                  v-model="caseData.learning_outcomes.clinical_pearls"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.learning_outcomes.clinical_pearls"
                placeholder="Những bài học và kinh nghiệm lâm sàng quan trọng..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Điểm thảo luận</label>
                <VoiceToText
                  v-model="caseData.learning_outcomes.discussion_points"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.learning_outcomes.discussion_points"
                placeholder="Các điểm để thảo luận..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Tiêu chí đánh giá</label>
                <VoiceToText
                  v-model="caseData.learning_outcomes.assessment_criteria"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.learning_outcomes.assessment_criteria"
                placeholder="Tiêu chí để đánh giá hiểu biết..."
                :disabled="!canEdit"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <label class="text-sm text-gray-500">Tài liệu tham khảo</label>
                <VoiceToText
                  v-model="caseData.learning_outcomes.references"
                  size="small"
                />
              </div>
              <Textarea
                v-model="caseData.learning_outcomes.references"
                placeholder="Tài liệu, bài báo tham khảo..."
                :disabled="!canEdit"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Student Notes & Attachments -->
      <div class="space-y-6">
        <!-- Student Notes -->
        <Card class="p-1">
          <template #title>
            <div class="p-4 pb-0">
              <p class="font-semibold text-lg">Ghi chú lâm sàng của bạn</p>
              <p class="text-sm text-gray-500 mt-1">
                Hoàn thành đánh giá và kế hoạch cho ca bệnh này
              </p>
            </div>
          </template>
          <template #content>
            <Tabs
              v-model:value="activeTab"
              class="mt-4"
              :dt="{
                activeBarBackground: '##1e3a8a',
                tabActiveBorderColor: '#1e3a8a',
              }"
            >
              <TabList>
                <Tab value="assessment">Đánh giá</Tab>
                <Tab value="differential">Chẩn đoán</Tab>
                <Tab value="plan">Kế hoạch</Tab>
                <Tab value="learning">Học tập</Tab>
              </TabList>

              <TabPanels>
                <TabPanel value="assessment" class="space-y-4">
                  <div class="space-y-2">
                    <div class="flex items-center gap-2">
                      <label class="text-sm font-medium text-gray-800"
                        >Đánh giá lâm sàng</label
                      >
                      <VoiceToText
                        v-model="notes.clinical_assessment"
                        size="small"
                      />
                    </div>
                    <p class="text-sm text-gray-500">
                      Đưa ra đánh giá lâm sàng của bạn về bệnh nhân này dựa trên
                      tiền sử, khám lâm sàng và các kết quả chẩn đoán.
                    </p>
                    <Textarea
                      fluid
                      rows="10"
                      v-model="notes.clinical_assessment"
                      placeholder="Viết đánh giá lâm sàng của bạn ở đây..."
                      class="min-h-[400px]"
                      @input="handleNoteChange"
                      :disabled="!canEdit"
                    />
                  </div>
                </TabPanel>

                <TabPanel value="differential" class="space-y-4">
                  <div class="space-y-2">
                    <div class="flex items-center gap-2">
                      <label class="text-sm font-medium text-gray-800"
                        >Chẩn đoán phân biệt</label
                      >
                      <VoiceToText
                        v-model="notes.differential_diagnosis"
                        size="small"
                      />
                    </div>
                    <p class="text-sm text-gray-500">
                      Liệt kê và giải thích các chẩn đoán phân biệt theo thứ tự
                      khả năng.
                    </p>
                    <Textarea
                      rows="10"
                      fluid
                      v-model="notes.differential_diagnosis"
                      placeholder="1. Chẩn đoán có khả năng nhất và lý do&#10;2. Chẩn đoán phân biệt thứ hai và tại sao...&#10;3. Những cân nhắc khác..."
                      class="min-h-[400px]"
                      @input="handleNoteChange"
                      :disabled="!canEdit"
                    />
                  </div>
                </TabPanel>

                <TabPanel value="plan" class="space-y-4">
                  <div class="space-y-2">
                    <div class="flex items-center gap-2">
                      <label class="text-sm font-medium text-gray-800"
                        >Kế hoạch điều trị</label
                      >
                      <VoiceToText
                        v-model="notes.treatment_plan"
                        size="small"
                      />
                    </div>
                    <p class="text-sm text-gray-500">
                      Phác thảo kế hoạch quản lý ngay lập tức và dài hạn cho
                      bệnh nhân này.
                    </p>
                    <Textarea
                      rows="10"
                      fluid
                      v-model="notes.treatment_plan"
                      placeholder="Xử trí ngay:&#10;- &#10;&#10;Xét nghiệm thêm:&#10;- &#10;&#10;Quản lý dài hạn:&#10;- "
                      class="min-h-[400px]"
                      @input="handleNoteChange"
                      :disabled="!canEdit"
                    />
                  </div>
                </TabPanel>

                <TabPanel value="learning" class="space-y-4">
                  <div class="space-y-2">
                    <div class="flex items-center gap-2">
                      <label class="text-sm font-medium text-gray-800"
                        >Điểm học tập</label
                      >
                      <VoiceToText
                        v-model="notes.learning_reflections"
                        size="small"
                      />
                    </div>
                    <p class="text-sm text-gray-500">
                      Suy ngẫm về những gì bạn đã học được từ ca bệnh này và bất
                      kỳ câu hỏi nào bạn có.
                    </p>
                    <Textarea
                      rows="10"
                      fluid
                      v-model="notes.learning_reflections"
                      placeholder="Điểm học tập chính:&#10;- &#10;&#10;Câu hỏi cho giảng viên:&#10;- &#10;&#10;Lĩnh vực cần nghiên cứu thêm:&#10;- "
                      class="min-h-[400px]"
                      @input="handleNoteChange"
                      :disabled="!canEdit"
                    />
                  </div>
                </TabPanel>
              </TabPanels>
            </Tabs>
          </template>
        </Card>

        <!-- Medical Attachments -->
        <Card class="p-1">
          <template #title>
            <div class="p-4 pb-0">
              <p class="font-semibold text-lg">
                <i class="pi pi-folder me-2"></i>Tệp đính kèm y tế
              </p>
            </div>
          </template>
          <template #content>
            <!-- Upload Area -->
            <div
              v-if="canEdit"
              class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors mb-4 cursor-pointer"
              :class="{ 'border-blue-400 bg-blue-50': isDragOver }"
              @dragover.prevent="isDragOver = true"
              @dragleave.prevent="isDragOver = false"
              @drop.prevent="handleDrop"
              @click="fileInput?.click()"
            >
              <div class="space-y-3">
                <i
                  class="pi pi-cloud-upload text-gray-400"
                  style="font-size: 3rem"
                ></i>
                <div>
                  <p class="text-md font-medium text-gray-900">
                    Kéo thả file vào đây
                  </p>
                  <p class="text-sm text-gray-500">hoặc nhấp để chọn file</p>
                </div>
                <input
                  ref="fileInput"
                  type="file"
                  multiple
                  accept="image/*,.pdf,.doc,.docx"
                  class="hidden"
                  @change="handleFileSelect"
                />
              </div>
            </div>

            <div v-if="canEdit" class="text-xs text-gray-500 mb-4">
              <p>Định dạng hỗ trợ: JPG, PNG, PDF, DOC, DOCX</p>
              <p>Kích thước tối đa: 10MB mỗi file</p>
            </div>

            <!-- Uploaded Files -->
            <div v-if="attachments.length > 0" class="space-y-4 mt-6">
              <h4 class="font-semibold text-gray-900">
                File đã tải lên ({{ attachments.length }})
              </h4>

              <div
                v-for="(file, index) in attachments"
                :key="file.id || index"
                class="border border-gray-200 rounded-lg p-4"
              >
                <div class="flex items-start justify-between mb-4">
                  <div class="flex flex-col space-y-2 flex-1 min-w-0">
                    <div class="flex items-start justify-between gap-2">
                      <div class="min-w-0 flex-1">
                        <p
                          class="font-medium text-gray-900 truncate"
                          :title="file.title || file.name"
                        >
                          {{ file.title || file.name }}
                        </p>
                        <p class="text-xs text-gray-500">
                          {{ formatFileSize(file.size) }}
                          <span
                            v-if="file.attachment_type_display"
                            class="ml-2 px-2 py-0.5 bg-blue-100 text-blue-700 rounded text-xs"
                            >{{ file.attachment_type_display }}</span
                          >
                          <span
                            v-if="file.uploaded_by_name"
                            class="ml-2 text-gray-400"
                            >• {{ file.uploaded_by_name }}</span
                          >
                        </p>
                        <p
                          v-if="file.description"
                          class="text-xs text-gray-600 mt-1"
                        >
                          {{ file.description }}
                        </p>
                      </div>

                      <div class="flex gap-2 shrink-0">
                        <!-- Download button for existing files -->
                        <Button
                          v-if="file.id"
                          as="a"
                          :href="getFileUrl(file.url || file.file)"
                          target="_blank"
                          icon="pi pi-download"
                          text
                          size="small"
                          title="Tải xuống"
                        />
                        <!-- Delete button for new uploads only -->
                        <Button
                          v-if="canEdit && !file.id"
                          icon="pi pi-trash"
                          text
                          size="small"
                          severity="danger"
                          @click="removeFile(index)"
                        />
                      </div>
                    </div>

                    <!-- Image preview or file icon -->
                    <div class="w-full">
                      <div
                        v-if="isImageFile(file)"
                        class="w-full h-64 rounded-lg overflow-hidden border border-gray-200"
                      >
                        <img
                          :src="getFileUrl(file.url || file.file)"
                          :alt="file.name || file.title"
                          class="w-full h-full object-cover"
                        />
                      </div>
                      <div
                        v-else
                        class="w-full h-64 rounded-lg bg-blue-100 flex items-center justify-center"
                      >
                        <div class="text-center">
                          <i
                            class="pi pi-file text-blue-600"
                            style="font-size: 6rem"
                          ></i>
                          <p class="mt-2 text-sm text-gray-600">
                            {{ file.name || file.title }}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Attachment Metadata Form — new uploads only -->
                <div
                  v-if="!file.id && canEdit"
                  class="border-t border-gray-200 pt-4 mt-4"
                >
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <!-- Attachment Type -->
                    <div>
                      <label
                        class="block text-xs font-medium text-gray-700 mb-1"
                        >Loại tài liệu</label
                      >
                      <Select
                        v-model="file.attachment_type"
                        :disabled="!canEdit"
                        :options="attachmentTypeOptions"
                        option-label="name"
                        option-value="value"
                        placeholder="Chọn loại"
                        class="w-full text-sm"
                      />
                    </div>

                    <!-- Title -->
                    <div>
                      <label
                        class="block text-xs font-medium text-gray-700 mb-1"
                        >Tiêu đề</label
                      >
                      <InputText
                        v-model="file.title"
                        :disabled="!canEdit"
                        class="w-full text-sm"
                        placeholder="Nhập tiêu đề..."
                      />
                    </div>

                    <!-- Date Taken -->
                    <div>
                      <label
                        class="block text-xs font-medium text-gray-700 mb-1"
                        >Ngày thực hiện</label
                      >
                      <InputText
                        v-model="file.date_taken"
                        type="date"
                        :disabled="!canEdit"
                        class="w-full text-sm"
                      />
                    </div>

                    <!-- Description -->
                    <div class="md:col-span-2">
                      <label
                        class="block text-xs font-medium text-gray-700 mb-1"
                        >Mô tả</label
                      >
                      <Textarea
                        v-model="file.description"
                        rows="2"
                        :disabled="!canEdit"
                        class="w-full text-sm"
                        placeholder="Nhập mô tả chi tiết..."
                      />
                    </div>

                    <!-- Physician Notes -->
                    <div class="md:col-span-2">
                      <label
                        class="block text-xs font-medium text-gray-700 mb-1"
                        >Ghi chú bác sĩ</label
                      >
                      <Textarea
                        v-model="file.physician_notes"
                        rows="2"
                        :disabled="!canEdit"
                        class="w-full text-sm"
                        placeholder="Ghi chú của bác sĩ..."
                      />
                    </div>

                    <!-- Is Confidential -->
                    <div class="md:col-span-2 flex items-center gap-2">
                      <Checkbox
                        v-model="file.is_confidential"
                        :disabled="!canEdit"
                        binary
                      />
                      <span class="text-xs font-medium text-gray-700"
                        >Tài liệu bảo mật</span
                      >
                      <span class="text-xs text-gray-500"
                        >(Chỉ giảng viên xem được)</span
                      >
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </Card>

        <!-- Preview Button -->
        <Button
          class="w-full h-button"
          icon="pi pi-eye"
          label="Xem trước bệnh án trước khi nộp"
          @click="showPreview = true"
        />
      </div>
    </div>

    <!-- Preview Dialog -->
    <CasePreview
      v-if="showPreview"
      :case-data="previewData"
      @close="showPreview = false"
      @submit="handleSubmit"
      :show-submit-button="true"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useToast } from "@/composables/useToast";
import { useAuthStore } from "@/stores/auth";
import { useChoices } from "@/composables/useChoices";
import Badge from "primevue/badge";
import Button from "primevue/button";
import Tag from "primevue/tag";
import Card from "primevue/card";
import Checkbox from "primevue/checkbox";
import Textarea from "primevue/textarea";
import InputNumber from "primevue/inputnumber";
import InputText from "primevue/inputtext";
import Select from "primevue/select";
import Tabs from "primevue/tabs";
import Tab from "primevue/tab";
import TabList from "primevue/tablist";
import TabPanel from "primevue/tabpanel";
import TabPanels from "primevue/tabpanels";
import VoiceToText from "@/components/VoiceToText.vue";
import CasePreview from "@/components/CasePreview.vue";
import { casesService } from "@/services/cases";
import { gradesService } from "@/services/grades";
import api from "@/services/api";

const {
  specialties,
  priorities,
  complexities,
  loading: choicesLoading,
} = useChoices();

const genderOptions = [
  { name: "Nam", value: "male" },
  { name: "Nữ", value: "female" },
  { name: "Khác", value: "other" },
  { name: "Không xác định", value: "not_specified" },
];

const symptomOnsetOptions = [
  { name: "Đột ngột", value: "sudden" },
  { name: "Từ từ", value: "gradual" },
  { name: "Mạn tính", value: "chronic" },
];

const symptomProgressionOptions = [
  { name: "Cải thiện", value: "improving" },
  { name: "Xấu đi", value: "worsening" },
  { name: "Ổn định", value: "stable" },
  { name: "Biến đổi", value: "fluctuating" },
];

const attachmentTypeOptions = [
  { name: "Ảnh chụp X-quang", value: "xray" },
  { name: "Ảnh chụp CT", value: "ct_scan" },
  { name: "Ảnh chụp MRI", value: "mri" },
  { name: "Ảnh siêu âm", value: "ultrasound" },
  { name: "Điện tim đồ", value: "ecg" },
  { name: "Phiếu xét nghiệm", value: "lab_report" },
  { name: "Xét nghiệm máu", value: "blood_test" },
  { name: "Xét nghiệm nước tiểu", value: "urine_test" },
  { name: "Giải phẫu bệnh", value: "pathology" },
  { name: "Ảnh chấn thương", value: "injury_photo" },
  { name: "Ảnh phẫu thuật", value: "surgical_photo" },
  { name: "Ảnh nội soi", value: "endoscopy" },
  { name: "Đơn thuốc", value: "prescription" },
  { name: "Tóm tắt xuất viện", value: "discharge_summary" },
  { name: "Phiếu đồng ý", value: "consent_form" },
  { name: "Khác", value: "other" },
];

const props = defineProps({
  caseId: { type: String, required: true },
});

const emit = defineEmits(["navigate"]);

// Collapsible sections state
const expandedSections = ref<Record<string, boolean>>({
  basic: true,
  patient: false,
  clinical: false,
  physical: false,
  investigations: false,
  diagnosis: false,
  learning: false,
  attachments: false,
  notes: true,
});

const toggleSection = (section: string) => {
  expandedSections.value[section] = !expandedSections.value[section];
};

const gradeData = ref<any>(null);

const notes = ref({
  clinical_assessment: "",
  differential_diagnosis: "",
  treatment_plan: "",
  learning_reflections: "",
  questions_for_instructor: "",
  challenges_faced: "",
  resources_used: "",
  final_diagnosis: "",
  plan: "",
  learning: "",
});

const hasUnsavedChanges = ref(false);
const showPreview = ref(false);
const activeTab = ref("assessment");
const { toast } = useToast();
const authStore = useAuthStore();

const caseOwnerId = ref<number | null>(null);
const caseStatus = ref<string>("draft");

const isOwner = computed(
  () =>
    authStore.user &&
    caseOwnerId.value &&
    authStore.user.id === caseOwnerId.value,
);
const isDraft = computed(() => caseStatus.value === "draft");
const canEdit = computed(() => isOwner.value && isDraft.value);

const fileInput = ref<HTMLInputElement>();
const isDragOver = ref(false);
const attachments = ref<any[]>([]);
const exportingPDF = ref(false);

const handleDrop = (event: DragEvent) => {
  isDragOver.value = false;
  addFiles(Array.from(event.dataTransfer?.files || []));
};

const handleFileSelect = (event: Event) => {
  addFiles(Array.from((event.target as HTMLInputElement).files || []));
};

const addFiles = (files: File[]) => {
  const validFiles = files.filter((file) => {
    if (file.size > 10 * 1024 * 1024) {
      toast.error(`File ${file.name} quá lớn. Kích thước tối đa là 10MB.`);
      return false;
    }
    const allowedTypes = [
      "image/jpeg",
      "image/png",
      "image/gif",
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];
    if (!allowedTypes.includes(file.type)) {
      toast.error(`File ${file.name} không được hỗ trợ.`);
      return false;
    }
    return true;
  });

  attachments.value = [
    ...attachments.value,
    ...validFiles.map((file) => ({
      name: file.name,
      size: file.size,
      type: file.type,
      url: URL.createObjectURL(file),
      file,
      attachment_type: "",
      title: file.name.split(".")[0] || "",
      department: "",
      description: "",
      date_taken: "",
      physician_notes: "",
      is_confidential: false,
    })),
  ];
  hasUnsavedChanges.value = true;
};

const removeFile = (index: number) => {
  const f = attachments.value[index];
  if (f.url) URL.revokeObjectURL(f.url);
  attachments.value.splice(index, 1);
  hasUnsavedChanges.value = true;
};

const isImageFile = (file: any) => file.type?.startsWith("image/");

const getFileUrl = (filePath: string): string => {
  if (filePath?.startsWith("http") || filePath?.startsWith("blob:"))
    return filePath;
  return `${import.meta.env.VITE_API_URL || "http://localhost:8000"}${filePath}`;
};

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
};

const caseData = ref({
  title: "",
  specialty: "",
  patient_name: "",
  patient_age: "",
  patient_gender: "",
  medical_record_number: "",
  patient_ethnicity: "",
  patient_occupation: "",
  admission_date: "",
  discharge_date: "",
  chief_complaint_brief: "",
  requires_follow_up: false,
  follow_up_date: "",
  priority_level: "medium",
  complexity_level: "basic",
  case_summary: "",
  learning_tags: "",
  estimated_study_hours: null,
  keywords: "",
  template: null,
  repository: null,
  clinical_history: {
    chief_complaint: "",
    history_present_illness: "",
    symptom_duration_days: null,
    symptom_onset: "",
    symptom_progression: "",
    past_medical_history: "",
    family_history: "",
    social_history: "",
    allergies: "",
    medications: "",
    review_systems: "",
  },
  physical_examination: {
    general_appearance: "",
    consciousness_level: "",
    vital_signs: "",
    vital_signs_bp: "",
    vital_signs_hr: null,
    vital_signs_rr: null,
    vital_signs_temp: null,
    vital_signs_spo2: null,
    weight_kg: null,
    height_cm: null,
    head_neck: "",
    cardiovascular: "",
    respiratory: "",
    abdominal: "",
    neurological: "",
    musculoskeletal: "",
    skin: "",
    other_findings: "",
  },
  investigations: {
    laboratory_results: "",
    hemoglobin_level: null,
    white_cell_count: null,
    platelet_count: null,
    sodium_level: null,
    potassium_level: null,
    glucose_level: null,
    creatinine_level: null,
    imaging_studies: "",
    ecg_findings: "",
    ecg_rhythm: "",
    ecg_rate: null,
    pathology_results: "",
    microbiology_results: "",
    other_investigations: "",
    arterial_blood_gas: "",
    ph_level: null,
    special_tests: "",
    biochemistry: "",
    hematology: "",
    microbiology: "",
  },
  diagnosis_management: {
    primary_diagnosis: "",
    differential_diagnosis: "",
    icd10_codes: "",
    treatment_plan: "",
    procedures_performed: "",
    prognosis: "",
    medications_prescribed: "",
    follow_up_plan: "",
    complications: "",
  },
  learning_outcomes: {
    learning_objectives: "",
    key_concepts: "",
    clinical_pearls: "",
    references: "",
    discussion_points: "",
    assessment_criteria: "",
  },
});

const handleNoteChange = () => {
  hasUnsavedChanges.value = true;
};

const handleSave = async () => {
  try {
    console.log("=== SAVING CASE ===");

    const cleanObject = (obj: any) => {
      if (!obj || typeof obj !== "object") return obj;
      const cleaned: any = {};
      for (const [key, value] of Object.entries(obj)) {
        if (value !== "" && value !== null && value !== undefined)
          cleaned[key] = value;
      }
      return Object.keys(cleaned).length > 0 ? cleaned : undefined;
    };

    const formatDate = (dateValue: any) => {
      if (!dateValue) return null;
      if (
        typeof dateValue === "string" &&
        /^\d{4}-\d{2}-\d{2}$/.test(dateValue)
      )
        return dateValue;
      const d = new Date(dateValue);
      if (isNaN(d.getTime())) return null;
      return d.toISOString().split("T")[0];
    };

    const payload: any = {
      title: caseData.value.title,
      specialty: caseData.value.specialty,
      patient_age: caseData.value.patient_age,
      patient_gender: caseData.value.patient_gender,
      medical_record_number: caseData.value.medical_record_number,
      patient_ethnicity: caseData.value.patient_ethnicity,
      patient_occupation: caseData.value.patient_occupation,
      admission_date: formatDate(caseData.value.admission_date),
      discharge_date: formatDate(caseData.value.discharge_date),
      chief_complaint_brief: caseData.value.chief_complaint_brief,
      requires_follow_up: caseData.value.requires_follow_up,
      follow_up_date: formatDate(caseData.value.follow_up_date),
      priority_level: caseData.value.priority_level,
      complexity_level: caseData.value.complexity_level,
      case_summary: caseData.value.case_summary,
      learning_tags: caseData.value.learning_tags,
      estimated_study_hours: caseData.value.estimated_study_hours,
    };

    const clinicalHistory = cleanObject(caseData.value.clinical_history);
    if (clinicalHistory) payload.clinical_history = clinicalHistory;

    const physicalExam = cleanObject(caseData.value.physical_examination);
    if (physicalExam) payload.physical_examination = physicalExam;

    const investigations = cleanObject(caseData.value.investigations);
    if (investigations) payload.detailed_investigations = investigations;

    const diagMgmt = cleanObject(caseData.value.diagnosis_management);
    if (diagMgmt) payload.diagnosis_management = diagMgmt;

    const learningOutcomes = cleanObject(caseData.value.learning_outcomes);
    if (learningOutcomes) payload.learning_outcomes = learningOutcomes;

    await casesService.updateCase(props.caseId, payload);

    const notesData = {
      case: props.caseId,
      clinical_assessment: notes.value.clinical_assessment,
      differential_diagnosis: notes.value.differential_diagnosis,
      treatment_plan: notes.value.treatment_plan,
      learning_reflections: notes.value.learning_reflections,
      questions_for_instructor: notes.value.questions_for_instructor,
      challenges_faced: notes.value.challenges_faced,
      resources_used: notes.value.resources_used,
    };

    const existingNotes = await casesService.getStudentNotes(props.caseId);
    if (existingNotes && existingNotes.id) {
      await casesService.updateStudentNotes(existingNotes.id, notesData);
    } else {
      await casesService.saveStudentNotes(props.caseId, notesData);
    }

    for (const attachment of attachments.value) {
      if (attachment.file && !attachment.id) {
        const formData = new FormData();
        formData.append("file", attachment.file);
        formData.append("title", attachment.title || attachment.name);
        formData.append(
          "attachment_type",
          attachment.attachment_type || "other",
        );
        if (attachment.description)
          formData.append("description", attachment.description);
        if (attachment.date_taken)
          formData.append("date_taken", attachment.date_taken);
        if (attachment.physician_notes)
          formData.append("physician_notes", attachment.physician_notes);
        formData.append(
          "confidentiality_level",
          attachment.is_confidential ? "confidential" : "public",
        );
        await casesService.uploadAttachment(props.caseId, formData);
      }
    }

    toast.success("Đã lưu nháp thành công!");
    hasUnsavedChanges.value = false;
  } catch (error: any) {
    console.error("Error saving case:", error);
    if (error.response?.data) {
      const errors = error.response.data;
      if (typeof errors === "object") {
        const errorMessages = Object.entries(errors)
          .map(
            ([field, msgs]) =>
              `${field}: ${(Array.isArray(msgs) ? msgs : [msgs]).join(", ")}`,
          )
          .join("\n");
        toast.error(`Lỗi: ${errorMessages}`);
      } else {
        toast.error(
          error.response?.data?.message ||
            error.response?.data ||
            "Không thể lưu nháp. Vui lòng thử lại.",
        );
      }
    } else {
      toast.error("Không thể lưu nháp. Vui lòng thử lại.");
    }
  }
};

const handleSubmit = async () => {
  try {
    await handleSave();
    await casesService.submitCase(props.caseId);
    toast.success("Ca bệnh đã được nộp để xem xét!");
    setTimeout(() => emit("navigate", "dashboard"), 1500);
  } catch (error: any) {
    console.error("Error submitting case:", error);
    if (error.response?.data) {
      const errorData = error.response.data;
      if (errorData.error) {
        toast.error(errorData.error);
      } else if (typeof errorData === "object") {
        const errorMessages = Object.entries(errorData)
          .map(
            ([field, msgs]) =>
              `${field}: ${(Array.isArray(msgs) ? msgs : [msgs]).join(", ")}`,
          )
          .join("\n");
        toast.error(`Lỗi: ${errorMessages}`);
      } else {
        toast.error(errorData || "Không thể nộp ca bệnh. Vui lòng thử lại.");
      }
    } else {
      toast.error("Không thể nộp ca bệnh. Vui lòng thử lại.");
    }
  }
};

const exportPDF = async () => {
  exportingPDF.value = true;
  try {
    const response = await api.get(`/cases/${props.caseId}/export_pdf/`, {
      responseType: "blob",
    });
    const blob = new Blob([response.data], { type: "application/pdf" });
    const url = window.URL.createObjectURL(blob);
    window.open(url, "_blank");
    setTimeout(() => window.URL.revokeObjectURL(url), 100);
    toast.success("Đã mở PDF trong tab mới!");
  } catch (err: any) {
    console.error("PDF export failed:", err);
    toast.error("Không thể tạo PDF. Vui lòng thử lại.");
  } finally {
    exportingPDF.value = false;
  }
};

const previewData = computed(() => ({
  title: caseData.value?.title || "Chưa có tiêu đề",
  specialty: caseData.value?.specialty || "Chưa chọn chuyên khoa",
  patientName: caseData.value?.patient_name || "Chưa nhập",
  patientAge: caseData.value?.patient_age || "Chưa nhập",
  patientGender:
    caseData.value?.patient_gender === "male"
      ? "Nam"
      : caseData.value?.patient_gender === "female"
        ? "Nữ"
        : caseData.value?.patient_gender || "Chưa nhập",
  medicalRecordNumber: caseData.value?.medical_record_number || "Chưa nhập",
  chief_complaint:
    caseData.value?.clinical_history?.chief_complaint || "Chưa nhập",
  historyOfPresentIllness:
    caseData.value?.clinical_history?.history_present_illness || "Chưa nhập",
  pastMedicalHistory:
    caseData.value?.clinical_history?.past_medical_history || "Chưa nhập",
  medications: caseData.value?.clinical_history?.medications || "Chưa nhập",
  generalAppearance:
    caseData.value?.physical_examination?.general_appearance || "Chưa nhập",
  vitalSigns: caseData.value?.physical_examination?.vital_signs || "Chưa nhập",
  cardiovascular:
    caseData.value?.physical_examination?.cardiovascular || "Chưa nhập",
  respiratory: caseData.value?.physical_examination?.respiratory || "Chưa nhập",
  labsAndImaging:
    caseData.value?.investigations?.laboratory_results || "Chưa nhập",
  imagingStudies:
    caseData.value?.investigations?.imaging_studies || "Chưa nhập",
  ecgFindings: caseData.value?.investigations?.ecg_findings || "Chưa nhập",
  primaryDiagnosis:
    caseData.value?.diagnosis_management?.primary_diagnosis || "Chưa nhập",
  treatmentPlanForm:
    caseData.value?.diagnosis_management?.treatment_plan || "Chưa nhập",
  differentialDiagnosis: notes.value?.differential_diagnosis || "Chưa nhập",
  finalDiagnosis: notes.value?.clinical_assessment || "Chưa nhập",
  treatmentPlan: notes.value?.treatment_plan || "Chưa nhập",
  notes: notes.value?.learning_reflections || "Chưa nhập",
  attachments: attachments.value || [],
}));

onMounted(async () => {
  try {
    const caseDetails = await casesService.getCase(props.caseId);

    if (caseDetails.student) {
      caseOwnerId.value =
        typeof caseDetails.student === "object"
          ? caseDetails.student.id
          : caseDetails.student;
    } else if (caseDetails.created_by) {
      caseOwnerId.value =
        typeof caseDetails.created_by === "object"
          ? caseDetails.created_by.id
          : caseDetails.created_by;
    }

    caseStatus.value = caseDetails.case_status || caseDetails.status || "draft";

    Object.assign(caseData.value, {
      title: caseDetails.title || "",
      specialty: caseDetails.specialty || "",
      patient_name: caseDetails.patient_name || "",
      patient_age: caseDetails.patient_age || "",
      patient_gender: caseDetails.patient_gender || "",
      medical_record_number: caseDetails.medical_record_number || "",
      patient_ethnicity: caseDetails.patient_ethnicity || "",
      patient_occupation: caseDetails.patient_occupation || "",
      admission_date: caseDetails.admission_date || "",
      discharge_date: caseDetails.discharge_date || "",
      chief_complaint_brief: caseDetails.chief_complaint_brief || "",
      requires_follow_up: caseDetails.requires_follow_up || false,
      follow_up_date: caseDetails.follow_up_date || "",
      priority_level: caseDetails.priority_level || "medium",
      complexity_level: caseDetails.complexity_level || "basic",
      case_summary: caseDetails.case_summary || "",
      learning_tags: caseDetails.learning_tags || "",
      estimated_study_hours: caseDetails.estimated_study_hours || null,
      keywords: caseDetails.keywords || "",
      template: caseDetails.template || null,
      repository: caseDetails.repository || null,
    });

    if (caseDetails.clinical_history)
      Object.assign(caseData.value.clinical_history, {
        chief_complaint: caseDetails.clinical_history.chief_complaint || "",
        history_present_illness:
          caseDetails.clinical_history.history_present_illness || "",
        symptom_duration_days:
          caseDetails.clinical_history.symptom_duration_days || null,
        symptom_onset: caseDetails.clinical_history.symptom_onset || "",
        symptom_progression:
          caseDetails.clinical_history.symptom_progression || "",
        past_medical_history:
          caseDetails.clinical_history.past_medical_history || "",
        family_history: caseDetails.clinical_history.family_history || "",
        social_history: caseDetails.clinical_history.social_history || "",
        allergies: caseDetails.clinical_history.allergies || "",
        medications: caseDetails.clinical_history.medications || "",
        review_systems: caseDetails.clinical_history.review_systems || "",
      });
    if (caseDetails.physical_examination)
      Object.assign(caseData.value.physical_examination, {
        general_appearance:
          caseDetails.physical_examination.general_appearance || "",
        consciousness_level:
          caseDetails.physical_examination.consciousness_level || "",
        vital_signs: caseDetails.physical_examination.vital_signs || "",
        vital_signs_bp: caseDetails.physical_examination.vital_signs_bp || "",
        vital_signs_hr: caseDetails.physical_examination.vital_signs_hr || null,
        vital_signs_rr: caseDetails.physical_examination.vital_signs_rr || null,
        vital_signs_temp:
          caseDetails.physical_examination.vital_signs_temp || null,
        vital_signs_spo2:
          caseDetails.physical_examination.vital_signs_spo2 || null,
        weight_kg: caseDetails.physical_examination.weight_kg || null,
        height_cm: caseDetails.physical_examination.height_cm || null,
        head_neck: caseDetails.physical_examination.head_neck || "",
        cardiovascular: caseDetails.physical_examination.cardiovascular || "",
        respiratory: caseDetails.physical_examination.respiratory || "",
        abdominal: caseDetails.physical_examination.abdominal || "",
        neurological: caseDetails.physical_examination.neurological || "",
        musculoskeletal: caseDetails.physical_examination.musculoskeletal || "",
        skin: caseDetails.physical_examination.skin || "",
        other_findings: caseDetails.physical_examination.other_systems || "",
      });
    if (caseDetails.detailed_investigations)
      Object.assign(caseData.value.investigations, {
        laboratory_results:
          caseDetails.detailed_investigations.laboratory_results || "",
        hemoglobin_level:
          caseDetails.detailed_investigations.hemoglobin_level || null,
        white_cell_count:
          caseDetails.detailed_investigations.white_cell_count || null,
        platelet_count:
          caseDetails.detailed_investigations.platelet_count || null,
        sodium_level: caseDetails.detailed_investigations.sodium_level || null,
        potassium_level:
          caseDetails.detailed_investigations.potassium_level || null,
        glucose_level:
          caseDetails.detailed_investigations.glucose_level || null,
        creatinine_level:
          caseDetails.detailed_investigations.creatinine_level || null,
        imaging_studies:
          caseDetails.detailed_investigations.imaging_studies || "",
        ecg_findings: caseDetails.detailed_investigations.ecg_findings || "",
        ecg_rhythm: caseDetails.detailed_investigations.ecg_rhythm || "",
        ecg_rate: caseDetails.detailed_investigations.ecg_rate || null,
        pathology_results:
          caseDetails.detailed_investigations.pathology_results || "",
        microbiology_results:
          caseDetails.detailed_investigations.microbiology_results || "",
        other_investigations:
          caseDetails.detailed_investigations.other_investigations || "",
        arterial_blood_gas:
          caseDetails.detailed_investigations.arterial_blood_gas || "",
        ph_level: caseDetails.detailed_investigations.ph_level || null,
        special_tests: caseDetails.detailed_investigations.special_tests || "",
        biochemistry: caseDetails.detailed_investigations.biochemistry || "",
        hematology: caseDetails.detailed_investigations.hematology || "",
        microbiology: caseDetails.detailed_investigations.microbiology || "",
      });
    if (caseDetails.diagnosis_management)
      Object.assign(caseData.value.diagnosis_management, {
        primary_diagnosis:
          caseDetails.diagnosis_management.primary_diagnosis || "",
        differential_diagnosis:
          caseDetails.diagnosis_management.differential_diagnosis || "",
        icd10_codes: caseDetails.diagnosis_management.icd10_codes || "",
        treatment_plan: caseDetails.diagnosis_management.treatment_plan || "",
        procedures_performed:
          caseDetails.diagnosis_management.procedures_performed || "",
        prognosis: caseDetails.diagnosis_management.prognosis || "",
        medications_prescribed:
          caseDetails.diagnosis_management.medications_prescribed || "",
        follow_up_plan: caseDetails.diagnosis_management.follow_up_plan || "",
        complications: caseDetails.diagnosis_management.complications || "",
      });
    if (caseDetails.learning_outcomes)
      Object.assign(caseData.value.learning_outcomes, {
        learning_objectives:
          caseDetails.learning_outcomes.learning_objectives || "",
        key_concepts: caseDetails.learning_outcomes.key_concepts || "",
        clinical_pearls: caseDetails.learning_outcomes.clinical_pearls || "",
        references: caseDetails.learning_outcomes.references || "",
        discussion_points:
          caseDetails.learning_outcomes.discussion_points || "",
        assessment_criteria:
          caseDetails.learning_outcomes.assessment_criteria || "",
      });

    if (caseDetails.medical_attachments?.length > 0) {
      attachments.value = caseDetails.medical_attachments.map((att: any) => ({
        ...att,
        url: att.file,
        type: att.file_type,
        size: att.file_size || 0,
        name: att.title,
      }));
    }

    try {
      const existingNotes = await casesService.getStudentNotes(props.caseId);
      if (existingNotes) {
        Object.assign(notes.value, {
          clinical_assessment: existingNotes.clinical_assessment || "",
          differential_diagnosis: existingNotes.differential_diagnosis || "",
          treatment_plan: existingNotes.treatment_plan || "",
          learning_reflections: existingNotes.learning_reflections || "",
          questions_for_instructor:
            existingNotes.questions_for_instructor || "",
          challenges_faced: existingNotes.challenges_faced || "",
          resources_used: existingNotes.resources_used || "",
        });
      }
    } catch (notesError) {
      console.error("Error loading student notes:", notesError);
    }

    if (caseDetails.has_grade) {
      try {
        const grade = await gradesService.getGrade(props.caseId);
        if (grade && grade.is_final) gradeData.value = grade;
      } catch (gradeError) {
        console.error("Error loading grade:", gradeError);
      }
    }
  } catch (error) {
    console.error("Error loading case data:", error);
    toast.error("Không thể tải dữ liệu ca bệnh");
  }
});
</script>

<style scoped>
.h-button {
  background: var(--primary) !important;
  border: 1px solid var(--primary) !important;
  color: var(--primary-foreground) !important;
  transition: all 0.3s ease !important;
  cursor: pointer;
}
.h-button:hover {
  background: var(--primary-hover) !important;
  border-color: var(--primary-hover) !important;
  box-shadow: 0 6px 16px var(--shadow-blue-hover) !important;
}
.badge {
  background: linear-gradient(
    135deg,
    var(--accent) 0%,
    rgba(59, 130, 246, 0.1) 100%
  );
  border: 1px solid var(--shadow-blue);
  color: var(--primary);
}
</style>
