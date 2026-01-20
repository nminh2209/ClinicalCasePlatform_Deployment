<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
  <div class="bg-white border-b border-gray-200 px-6 py-5">
  <div class="flex flex-col md:flex-row md:items-start justify-between gap-6">
    <!-- Left Section: Navigation & Case Info -->
    <div class="flex gap-4">
      <!-- Back Button -->
      <Button 
        variant="ghost" 
        size="icon" 
        @click="router.back()"
        class="shrink-0 h-10 w-10 rounded-lg hover:bg-gray-100 transition-colors"
      >
        <ArrowLeft class="h-5 w-5 text-gray-600" />
      </Button>

      <!-- Case Details -->
      <div class="min-w-0 flex-1">
        <h1 class="text-2xl font-semibold text-gray-900 mb-2 leading-tight">
          {{ caseData.title }}
        </h1>
        
        <!-- Badges Row -->
        <div class="flex flex-wrap items-center gap-2 mb-2">
          <Badge 
            variant="secondary" 
            class="bg-blue-50 text-blue-700 border border-blue-200 font-medium"
          >
            {{ caseData.specialty }}
          </Badge>
          <Badge :class="getStatusBadgeClass(caseData.case_status)">
            {{ getStatusLabel(caseData.case_status) }}
          </Badge>
          <Badge 
            v-if="caseData.created_by_role === 'instructor'" 
            class="bg-gradient-to-r from-purple-600 to-purple-700 text-white border-0 shadow-sm"
          >
            <span class="mr-1">📚</span>
            Hồ sơ mẫu
          </Badge>
        </div>

        <!-- Creator Info -->
        <div class="flex items-center gap-2 text-sm text-gray-600">
          <span class="font-medium">
            {{ caseData.created_by_role === 'instructor' ? 'Giảng viên' : 'Sinh viên' }}:
          </span>
          <span class="text-gray-900">{{ caseData.created_by_name }}</span>
          <span class="text-gray-400">•</span>
          <span class="text-gray-500">{{ caseData.created_by_id }}</span>
        </div>
      </div>
    </div>

    <!-- Right Section: Actions -->
    <div class="flex items-center gap-3 md:shrink-0">
      <Button 
        variant="outline" 
        @click="showShareModal = true" 
        class="flex items-center gap-2 px-4 py-2 border-gray-300 hover:bg-gray-50 hover:border-gray-400 transition-all shadow-sm"
      >
        <svg 
          class="w-4 h-4" 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
          stroke-width="2"
        >
          <path 
            stroke-linecap="round" 
            stroke-linejoin="round"
            d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" 
          />
        </svg>
        <span class="font-medium">Chia sẻ ca bệnh</span>
      </Button>
    </div>
  </div>
</div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Case Information (Read-only for instructors) -->
      <div class="space-y-3">
        <!-- Basic Information -->
        <Card class="bg-white shadow-sm border border-gray-200 overflow-hidden">
          <button @click="toggleSection('basic')"
            class="w-full p-4 flex items-center justify-between hover:bg-blue-50/50 transition-colors border-l-4 border-blue-500">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-blue-100 flex items-center justify-center">
                <InfoIcon stroke="#3b82f6" class="w-4 h-4" />
              </div>
              <CardTitle class="text-base font-semibold text-gray-800">Thông tin cơ bản</CardTitle>
            </div>
            <ChevronDown :class="['h-5 w-5 text-gray-400 transition-transform duration-200', expandedSections.basic && 'rotate-180']" />
          </button>
          <CardContent v-show="expandedSections.basic" class="pt-0 pb-4 px-4 bg-gray-50/30">
            <!-- Case Information Section -->
            <div class="pt-3">
              <h4 class="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
                <DocumentIcon class="w-4 h-4 text-blue-500" stroke="#3b82f6" />
                Thông tin hồ sơ
              </h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div class="p-3 bg-white rounded-lg border border-gray-200 md:col-span-2">
                  <label class="text-xs font-medium text-blue-600 uppercase tracking-wide">Tiêu đề hồ sơ</label>
                  <p class="text-gray-800 mt-1 font-medium">{{ caseData.title || "—" }}</p>
                </div>
                <div class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-blue-600 uppercase tracking-wide">Chuyên khoa</label>
                  <p class="text-gray-800 mt-1">{{ caseData.specialty || "—" }}</p>
                </div>
                <div class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-blue-600 uppercase tracking-wide">Mức độ phức tạp</label>
                  <p class="text-gray-800 mt-1">{{ getComplexityLabel(caseData.complexity_level) || "—" }}</p>
                </div>
                <div class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-blue-600 uppercase tracking-wide">Mức độ ưu tiên</label>
                  <p class="text-gray-800 mt-1">{{ getPriorityLabel(caseData.priority_level) || "—" }}</p>
                </div>
                <div v-if="caseData.estimated_study_hours" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-blue-600 uppercase tracking-wide">Thời gian học ước tính</label>
                  <p class="text-gray-800 mt-1">{{ caseData.estimated_study_hours }} giờ</p>
                </div>
                <div v-if="caseData.keywords" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-blue-600 uppercase tracking-wide">Từ khóa</label>
                  <p class="text-gray-800 mt-1">{{ caseData.keywords }}</p>
                </div>
                <div v-if="caseData.learning_tags" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-blue-600 uppercase tracking-wide">Nhãn học tập</label>
                  <p class="text-gray-800 mt-1">{{ caseData.learning_tags }}</p>
                </div>
                <div v-if="caseData.chief_complaint_brief" class="p-3 bg-white rounded-lg border border-gray-200 md:col-span-2">
                  <label class="text-xs font-medium text-blue-600 uppercase tracking-wide">Lý do khám tóm tắt</label>
                  <p class="text-gray-800 mt-1">{{ caseData.chief_complaint_brief }}</p>
                </div>
                <div v-if="caseData.case_summary" class="p-3 bg-white rounded-lg border border-gray-200 md:col-span-2">
                  <label class="text-xs font-medium text-blue-600 uppercase tracking-wide">Tóm tắt ca bệnh</label>
                  <p class="text-gray-800 mt-1 whitespace-pre-wrap">{{ caseData.case_summary }}</p>
                </div>
              </div>
            </div>
            
            <!-- Patient Demographics Section -->
            <div class="pt-4 mt-4 border-t border-gray-200">
              <h4 class="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
                <User class="w-4 h-4 text-green-500" />
                Thông tin bệnh nhân
              </h4>
              <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-green-600 uppercase tracking-wide">Tuổi</label>
                  <p class="text-gray-800 mt-1">{{ caseData.patient_age || "—" }}</p>
                </div>
                <div class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-green-600 uppercase tracking-wide">Giới tính</label>
                  <p class="text-gray-800 mt-1">{{ getGenderLabel(caseData.patient_gender) || "—" }}</p>
                </div>
                <div v-if="caseData.patient_ethnicity" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-green-600 uppercase tracking-wide">Dân tộc</label>
                  <p class="text-gray-800 mt-1">{{ caseData.patient_ethnicity }}</p>
                </div>
                <div v-if="caseData.patient_occupation" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-green-600 uppercase tracking-wide">Nghề nghiệp</label>
                  <p class="text-gray-800 mt-1">{{ caseData.patient_occupation }}</p>
                </div>
                <div v-if="caseData.medical_record_number" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-green-600 uppercase tracking-wide">Số hồ sơ bệnh án</label>
                  <p class="text-gray-800 mt-1">{{ caseData.medical_record_number }}</p>
                </div>
                <div v-if="caseData.admission_date" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-green-600 uppercase tracking-wide">Ngày nhập viện</label>
                  <p class="text-gray-800 mt-1">{{ formatDate(caseData.admission_date) }}</p>
                </div>
                <div v-if="caseData.discharge_date" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-green-600 uppercase tracking-wide">Ngày xuất viện</label>
                  <p class="text-gray-800 mt-1">{{ formatDate(caseData.discharge_date) }}</p>
                </div>
                <div v-if="caseData.requires_follow_up" class="p-3 bg-white rounded-lg border border-orange-100 bg-orange-50/30">
                  <label class="text-xs font-medium text-orange-600 uppercase tracking-wide">Cần theo dõi</label>
                  <p class="text-gray-800 mt-1">{{ caseData.follow_up_date ? formatDate(caseData.follow_up_date) : 'Có' }}</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Clinical History -->
        <Card class="bg-white shadow-sm border border-gray-200 overflow-hidden">
          <button @click="toggleSection('clinical')"
            class="w-full p-4 flex items-center justify-between hover:bg-amber-50/50 transition-colors border-l-4 border-amber-500">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-amber-100 flex items-center justify-center">
                <DocumentIcon class="w-4 h-4 text-amber-600" stroke="#d97706" />
              </div>
              <div class="flex items-center gap-2">
                <CardTitle class="text-base font-semibold text-gray-800">Tiền sử lâm sàng</CardTitle>
                <span v-if="!hasData('clinical_history')" class="px-2 py-0.5 text-xs font-medium bg-gray-100 text-gray-500 rounded-full">
                  Chưa có dữ liệu
                </span>
              </div>
            </div>
            <ChevronDown :class="['h-5 w-5 text-gray-400 transition-transform duration-200', expandedSections.clinical && 'rotate-180']" />
          </button>
          <CardContent v-show="expandedSections.clinical" class="pt-0 pb-4 px-4 bg-gray-50/30">
            <!-- Empty State -->
            <div v-if="!hasData('clinical_history')" class="py-8 text-center">
              <div class="w-12 h-12 mx-auto mb-3 rounded-full bg-gray-100 flex items-center justify-center">
                <DocumentIcon class="w-6 h-6 text-gray-400" stroke="#9ca3af" />
              </div>
              <p class="text-gray-500 text-sm">Chưa có thông tin tiền sử lâm sàng</p>
              <p class="text-gray-400 text-xs mt-1">Sinh viên chưa điền phần này</p>
            </div>
            <!-- Data Display -->
            <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-3">
              <div v-if="caseData.clinical_history?.chief_complaint" class="p-3 bg-white rounded-lg border border-gray-200">
                <label class="text-xs font-medium text-amber-600 uppercase tracking-wide">Lý do khám chính</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.clinical_history?.chief_complaint }}
                </p>
              </div>
              <div v-if="caseData.clinical_history?.history_present_illness" class="p-3 bg-white rounded-lg border border-gray-200">
                <label class="text-xs font-medium text-amber-600 uppercase tracking-wide">Bệnh sử hiện tại</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.clinical_history?.history_present_illness }}
                </p>
              </div>
              <div v-if="caseData.clinical_history?.past_medical_history" class="p-3 bg-white rounded-lg border border-gray-200">
                <label class="text-xs font-medium text-amber-600 uppercase tracking-wide">Tiền sử bệnh tật</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.clinical_history?.past_medical_history }}
                </p>
              </div>
              <div v-if="caseData.clinical_history?.family_history" class="p-3 bg-white rounded-lg border border-gray-200">
                <label class="text-xs font-medium text-amber-600 uppercase tracking-wide">Tiền sử gia đình</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.clinical_history?.family_history }}
                </p>
              </div>
              <div v-if="caseData.clinical_history?.social_history" class="p-3 bg-white rounded-lg border border-gray-200">
                <label class="text-xs font-medium text-amber-600 uppercase tracking-wide">Tiền sử xã hội</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.clinical_history?.social_history }}
                </p>
              </div>
              <div v-if="caseData.clinical_history?.allergies" class="p-3 bg-white rounded-lg border border-red-100 bg-red-50/30">
                <label class="text-xs font-medium text-red-600 uppercase tracking-wide">⚠️ Dị ứng</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.clinical_history?.allergies }}
                </p>
              </div>
              <div v-if="caseData.clinical_history?.medications" class="p-3 bg-white rounded-lg border border-gray-200">
                <label class="text-xs font-medium text-amber-600 uppercase tracking-wide">Thuốc đang sử dụng</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.clinical_history?.medications }}
                </p>
              </div>
              <div v-if="caseData.clinical_history?.review_systems" class="p-3 bg-white rounded-lg border border-gray-200">
                <label class="text-xs font-medium text-amber-600 uppercase tracking-wide">Đánh giá hệ thống</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.clinical_history?.review_systems }}
                </p>
              </div>
              <div v-if="caseData.clinical_history?.immunizations" class="p-3 bg-white rounded-lg border border-gray-200">
                <label class="text-xs font-medium text-amber-600 uppercase tracking-wide">Tiêm chủng</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.clinical_history?.immunizations }}
                </p>
              </div>
              <div v-if="caseData.clinical_history?.surgical_history" class="p-3 bg-white rounded-lg border border-gray-200">
                <label class="text-xs font-medium text-amber-600 uppercase tracking-wide">Tiền sử phẫu thuật</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.clinical_history?.surgical_history }}
                </p>
              </div>
              <div v-if="caseData.clinical_history?.symptom_onset || caseData.clinical_history?.symptom_duration_days" class="p-3 bg-white rounded-lg border border-gray-200">
                <label class="text-xs font-medium text-amber-600 uppercase tracking-wide">Triệu chứng khởi phát</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  <span v-if="caseData.clinical_history?.symptom_onset">{{ caseData.clinical_history?.symptom_onset }}</span>
                  <span v-if="caseData.clinical_history?.symptom_duration_days"> ({{ caseData.clinical_history?.symptom_duration_days }} ngày)</span>
                </p>
              </div>
              <div v-if="caseData.clinical_history?.symptom_progression" class="p-3 bg-white rounded-lg border border-gray-200">
                <label class="text-xs font-medium text-amber-600 uppercase tracking-wide">Diễn tiến triệu chứng</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.clinical_history?.symptom_progression }}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Physical Examination -->
        <Card class="bg-white shadow-sm border border-gray-200 overflow-hidden">
          <button @click="toggleSection('physical')"
            class="w-full p-4 flex items-center justify-between hover:bg-purple-50/50 transition-colors border-l-4 border-purple-500">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-purple-100 flex items-center justify-center">
                <Stethoscope class="w-4 h-4 text-purple-600" stroke="#9333ea" />
              </div>
              <div class="flex items-center gap-2">
                <CardTitle class="text-base font-semibold text-gray-800">Khám lâm sàng</CardTitle>
                <span v-if="!hasData('physical_examination')" class="px-2 py-0.5 text-xs font-medium bg-gray-100 text-gray-500 rounded-full">
                  Chưa có dữ liệu
                </span>
              </div>
            </div>
            <ChevronDown :class="['h-5 w-5 text-gray-400 transition-transform duration-200', expandedSections.physical && 'rotate-180']" />
          </button>
          <CardContent v-show="expandedSections.physical" class="pt-0 pb-4 px-4 bg-gray-50/30">
            <!-- Empty State -->
            <div v-if="!hasData('physical_examination')" class="py-8 text-center">
              <div class="w-12 h-12 mx-auto mb-3 rounded-full bg-gray-100 flex items-center justify-center">
                <Stethoscope class="w-6 h-6 text-gray-400" stroke="#9ca3af" />
              </div>
              <p class="text-gray-500 text-sm">Chưa có thông tin khám lâm sàng</p>
              <p class="text-gray-400 text-xs mt-1">Sinh viên chưa điền phần này</p>
            </div>
            <!-- Data Display -->
            <div v-else class="pt-3">
              <!-- Vital Signs Grid -->
              <div v-if="hasVitalSigns" class="p-3 bg-white rounded-lg border border-purple-100 mb-3">
                <label class="text-xs font-medium text-purple-600 uppercase tracking-wide mb-3 block">Sinh hiệu</label>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div v-if="caseData.physical_examination?.vital_signs_temp" class="text-center p-2 bg-purple-50 rounded-lg">
                    <p class="text-lg font-bold text-purple-700">{{ caseData.physical_examination.vital_signs_temp }}°C</p>
                    <p class="text-xs text-gray-500">Nhiệt độ</p>
                  </div>
                  <div v-if="caseData.physical_examination?.vital_signs_hr" class="text-center p-2 bg-purple-50 rounded-lg">
                    <p class="text-lg font-bold text-purple-700">{{ caseData.physical_examination.vital_signs_hr }}</p>
                    <p class="text-xs text-gray-500">Nhịp tim (bpm)</p>
                  </div>
                  <div v-if="caseData.physical_examination?.vital_signs_bp" class="text-center p-2 bg-purple-50 rounded-lg">
                    <p class="text-lg font-bold text-purple-700">{{ caseData.physical_examination.vital_signs_bp }}</p>
                    <p class="text-xs text-gray-500">Huyết áp (mmHg)</p>
                  </div>
                  <div v-if="caseData.physical_examination?.vital_signs_rr" class="text-center p-2 bg-purple-50 rounded-lg">
                    <p class="text-lg font-bold text-purple-700">{{ caseData.physical_examination.vital_signs_rr }}</p>
                    <p class="text-xs text-gray-500">Nhịp thở (/phút)</p>
                  </div>
                  <div v-if="caseData.physical_examination?.vital_signs_spo2" class="text-center p-2 bg-purple-50 rounded-lg">
                    <p class="text-lg font-bold text-purple-700">{{ caseData.physical_examination.vital_signs_spo2 }}%</p>
                    <p class="text-xs text-gray-500">SpO2</p>
                  </div>
                  <div v-if="caseData.physical_examination?.weight_kg" class="text-center p-2 bg-purple-50 rounded-lg">
                    <p class="text-lg font-bold text-purple-700">{{ caseData.physical_examination.weight_kg }} kg</p>
                    <p class="text-xs text-gray-500">Cân nặng</p>
                  </div>
                  <div v-if="caseData.physical_examination?.height_cm" class="text-center p-2 bg-purple-50 rounded-lg">
                    <p class="text-lg font-bold text-purple-700">{{ caseData.physical_examination.height_cm }} cm</p>
                    <p class="text-xs text-gray-500">Chiều cao</p>
                  </div>
                  <div v-if="caseData.physical_examination?.bmi" class="text-center p-2 bg-purple-50 rounded-lg">
                    <p class="text-lg font-bold text-purple-700">{{ caseData.physical_examination.bmi }}</p>
                    <p class="text-xs text-gray-500">BMI</p>
                  </div>
                </div>
              </div>

              <!-- Physical Exam Fields - 2 columns -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div v-if="caseData.physical_examination?.general_appearance" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-purple-600 uppercase tracking-wide">Tình trạng chung</label>
                  <p class="text-gray-800 mt-2">
                    {{ caseData.physical_examination.general_appearance }}
                  </p>
                </div>
                <div v-if="caseData.physical_examination?.vital_signs" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-purple-600 uppercase tracking-wide">Ghi chú sinh hiệu</label>
                  <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                    {{ caseData.physical_examination.vital_signs }}
                  </p>
                </div>
                <div v-if="caseData.physical_examination?.cardiovascular" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-purple-600 uppercase tracking-wide">Tim mạch</label>
                  <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                    {{ caseData.physical_examination.cardiovascular }}
                  </p>
                </div>
                <div v-if="caseData.physical_examination?.respiratory" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-purple-600 uppercase tracking-wide">Hô hấp</label>
                  <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                    {{ caseData.physical_examination.respiratory }}
                  </p>
                </div>
                <div v-if="caseData.physical_examination?.abdominal" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-purple-600 uppercase tracking-wide">Bụng</label>
                  <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                    {{ caseData.physical_examination.abdominal }}
                  </p>
                </div>
                <div v-if="caseData.physical_examination?.neurological" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-purple-600 uppercase tracking-wide">Thần kinh</label>
                  <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                    {{ caseData.physical_examination.neurological }}
                  </p>
                </div>
                <div v-if="caseData.physical_examination?.musculoskeletal" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-purple-600 uppercase tracking-wide">Cơ xương khớp</label>
                  <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                    {{ caseData.physical_examination.musculoskeletal }}
                  </p>
                </div>
                <div v-if="caseData.physical_examination?.skin" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-purple-600 uppercase tracking-wide">Da</label>
                  <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                    {{ caseData.physical_examination.skin }}
                  </p>
                </div>
                <div v-if="caseData.physical_examination?.head_neck" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-purple-600 uppercase tracking-wide">Đầu và cổ</label>
                  <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                    {{ caseData.physical_examination.head_neck }}
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Investigations -->
        <Card class="bg-white shadow-sm border border-gray-200 overflow-hidden">
          <button @click="toggleSection('investigations')"
            class="w-full p-4 flex items-center justify-between hover:bg-cyan-50/50 transition-colors border-l-4 border-cyan-500">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-cyan-100 flex items-center justify-center">
                <FlaskConical class="w-4 h-4 text-cyan-600" stroke="#0891b2" />
              </div>
              <div class="flex items-center gap-2">
                <CardTitle class="text-base font-semibold text-gray-800">Cận lâm sàng</CardTitle>
                <span v-if="!hasData('investigations')" class="px-2 py-0.5 text-xs font-medium bg-gray-100 text-gray-500 rounded-full">
                  Chưa có dữ liệu
                </span>
              </div>
            </div>
            <ChevronDown :class="['h-5 w-5 text-gray-400 transition-transform duration-200', expandedSections.investigations && 'rotate-180']" />
          </button>
          <CardContent v-show="expandedSections.investigations" class="pt-0 pb-4 px-4 bg-gray-50/30">
            <!-- Empty State -->
            <div v-if="!hasData('investigations')" class="py-8 text-center">
              <div class="w-12 h-12 mx-auto mb-3 rounded-full bg-gray-100 flex items-center justify-center">
                <FlaskConical class="w-6 h-6 text-gray-400" stroke="#9ca3af" />
              </div>
              <p class="text-gray-500 text-sm">Chưa có kết quả cận lâm sàng</p>
              <p class="text-gray-400 text-xs mt-1">Sinh viên chưa điền phần này</p>
            </div>
            <!-- Data Display -->
            <div v-else class="pt-3">
              <!-- Lab Values Grid -->
              <div v-if="hasLabValues" class="p-3 bg-white rounded-lg border border-cyan-100 mb-3">
                <label class="text-xs font-medium text-cyan-600 uppercase tracking-wide mb-3 block">Chỉ số xét nghiệm</label>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div v-if="caseData.investigations?.hemoglobin_level" class="text-center p-2 bg-cyan-50 rounded-lg">
                    <p class="text-lg font-bold text-cyan-700">{{ caseData.investigations.hemoglobin_level }}</p>
                    <p class="text-xs text-gray-500">Hemoglobin (g/dL)</p>
                  </div>
                  <div v-if="caseData.investigations?.white_cell_count" class="text-center p-2 bg-cyan-50 rounded-lg">
                    <p class="text-lg font-bold text-cyan-700">{{ caseData.investigations.white_cell_count }}</p>
                    <p class="text-xs text-gray-500">WBC (×10⁹/L)</p>
                  </div>
                  <div v-if="caseData.investigations?.platelet_count" class="text-center p-2 bg-cyan-50 rounded-lg">
                    <p class="text-lg font-bold text-cyan-700">{{ caseData.investigations.platelet_count }}</p>
                    <p class="text-xs text-gray-500">Tiểu cầu (×10⁹/L)</p>
                  </div>
                  <div v-if="caseData.investigations?.sodium_level" class="text-center p-2 bg-cyan-50 rounded-lg">
                    <p class="text-lg font-bold text-cyan-700">{{ caseData.investigations.sodium_level }}</p>
                    <p class="text-xs text-gray-500">Natri (mmol/L)</p>
                  </div>
                  <div v-if="caseData.investigations?.potassium_level" class="text-center p-2 bg-cyan-50 rounded-lg">
                    <p class="text-lg font-bold text-cyan-700">{{ caseData.investigations.potassium_level }}</p>
                    <p class="text-xs text-gray-500">Kali (mmol/L)</p>
                  </div>
                  <div v-if="caseData.investigations?.creatinine_level" class="text-center p-2 bg-cyan-50 rounded-lg">
                    <p class="text-lg font-bold text-cyan-700">{{ caseData.investigations.creatinine_level }}</p>
                    <p class="text-xs text-gray-500">Creatinine (mg/dL)</p>
                  </div>
                  <div v-if="caseData.investigations?.glucose_level" class="text-center p-2 bg-cyan-50 rounded-lg">
                    <p class="text-lg font-bold text-cyan-700">{{ caseData.investigations.glucose_level }}</p>
                    <p class="text-xs text-gray-500">Glucose (mg/dL)</p>
                  </div>
                </div>
              </div>

              <!-- Investigation Fields - 2 columns -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div v-if="caseData.investigations?.laboratory_results" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-cyan-600 uppercase tracking-wide">Xét nghiệm tổng quát</label>
                  <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                    {{ caseData.investigations.laboratory_results }}
                  </p>
                </div>
                <div v-if="caseData.investigations?.imaging_studies" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-cyan-600 uppercase tracking-wide">Chẩn đoán hình ảnh</label>
                  <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                    {{ caseData.investigations.imaging_studies }}
                  </p>
                </div>
                <div v-if="caseData.investigations?.ecg_findings" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-cyan-600 uppercase tracking-wide">Điện tâm đồ</label>
                  <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                    {{ caseData.investigations.ecg_findings }}
                  </p>
                </div>
                <div v-if="caseData.investigations?.pathology_results" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-cyan-600 uppercase tracking-wide">Giải phẫu bệnh</label>
                  <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                    {{ caseData.investigations.pathology_results }}
                  </p>
                </div>
                <div v-if="caseData.investigations?.microbiology_results" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-cyan-600 uppercase tracking-wide">Vi sinh</label>
                  <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                    {{ caseData.investigations.microbiology_results }}
                  </p>
                </div>
                <div v-if="caseData.investigations?.other_investigations" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-cyan-600 uppercase tracking-wide">Xét nghiệm khác</label>
                  <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                    {{ caseData.investigations.other_investigations }}
                  </p>
                </div>
                <div v-if="caseData.investigations?.arterial_blood_gas" class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-cyan-600 uppercase tracking-wide">Khí máu động mạch</label>
                  <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                    {{ caseData.investigations.arterial_blood_gas }}
                    <span v-if="caseData.investigations?.ph_level"> (pH: {{ caseData.investigations.ph_level }})</span>
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Diagnosis and Management -->
        <Card class="bg-white shadow-sm border border-gray-200 overflow-hidden">
          <button @click="toggleSection('diagnosis')"
            class="w-full p-4 flex items-center justify-between hover:bg-rose-50/50 transition-colors border-l-4 border-rose-500">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-rose-100 flex items-center justify-center">
                <Activity class="w-4 h-4 text-rose-600" stroke="#e11d48" />
              </div>
              <div class="flex items-center gap-2">
                <CardTitle class="text-base font-semibold text-gray-800">Chẩn đoán và điều trị</CardTitle>
                <span v-if="!hasData('diagnosis_management')" class="px-2 py-0.5 text-xs font-medium bg-gray-100 text-gray-500 rounded-full">
                  Chưa có dữ liệu
                </span>
              </div>
            </div>
            <ChevronDown :class="['h-5 w-5 text-gray-400 transition-transform duration-200', expandedSections.diagnosis && 'rotate-180']" />
          </button>
          <CardContent v-show="expandedSections.diagnosis" class="pt-0 pb-4 px-4 bg-gray-50/30">
            <!-- Empty State -->
            <div v-if="!hasData('diagnosis_management')" class="py-8 text-center">
              <div class="w-12 h-12 mx-auto mb-3 rounded-full bg-gray-100 flex items-center justify-center">
                <Activity class="w-6 h-6 text-gray-400" stroke="#9ca3af" />
              </div>
              <p class="text-gray-500 text-sm">Chưa có thông tin chẩn đoán và điều trị</p>
              <p class="text-gray-400 text-xs mt-1">Sinh viên chưa điền phần này</p>
            </div>
            <!-- Data Display -->
            <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-3">
              <div v-if="caseData.diagnosis_management?.primary_diagnosis" class="p-3 bg-white rounded-lg border border-gray-200 md:col-span-2">
                <label class="text-xs font-medium text-rose-600 uppercase tracking-wide">Chẩn đoán chính</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed font-medium">
                  {{ caseData.diagnosis_management.primary_diagnosis }}
                </p>
              </div>
              <div v-if="caseData.diagnosis_management?.differential_diagnosis" class="p-3 bg-white rounded-lg border border-gray-200">
                <label class="text-xs font-medium text-rose-600 uppercase tracking-wide">Chẩn đoán phân biệt</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.diagnosis_management.differential_diagnosis }}
                </p>
              </div>
              <div v-if="caseData.diagnosis_management?.icd10_codes" class="p-3 bg-white rounded-lg border border-gray-200">
                <label class="text-xs font-medium text-rose-600 uppercase tracking-wide">Mã ICD-10</label>
                <p class="text-gray-800 mt-2 font-mono text-sm">
                  {{ caseData.diagnosis_management.icd10_codes }}
                </p>
              </div>
              <div v-if="caseData.diagnosis_management?.treatment_plan" class="p-3 bg-white rounded-lg border border-gray-200">
                <label class="text-xs font-medium text-rose-600 uppercase tracking-wide">Kế hoạch điều trị</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.diagnosis_management.treatment_plan }}
                </p>
              </div>
              <div v-if="caseData.diagnosis_management?.medications_prescribed" class="p-3 bg-white rounded-lg border border-gray-200">
                <label class="text-xs font-medium text-rose-600 uppercase tracking-wide">Thuốc được kê đơn</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.diagnosis_management.medications_prescribed }}
                </p>
              </div>
              <div v-if="caseData.diagnosis_management?.procedures_performed" class="p-3 bg-white rounded-lg border border-gray-200">
                <label class="text-xs font-medium text-rose-600 uppercase tracking-wide">Thủ thuật đã thực hiện</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.diagnosis_management.procedures_performed }}
                </p>
              </div>
              <div v-if="caseData.diagnosis_management?.follow_up_plan" class="p-3 bg-white rounded-lg border border-gray-200">
                <label class="text-xs font-medium text-rose-600 uppercase tracking-wide">Kế hoạch theo dõi</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.diagnosis_management.follow_up_plan }}
                </p>
              </div>
              <div v-if="caseData.diagnosis_management?.prognosis" class="p-3 bg-white rounded-lg border border-gray-200">
                <label class="text-xs font-medium text-rose-600 uppercase tracking-wide">Tiên lượng</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.diagnosis_management.prognosis }}
                </p>
              </div>
              <div v-if="caseData.diagnosis_management?.complications" class="p-3 bg-white rounded-lg border border-orange-100 bg-orange-50/30">
                <label class="text-xs font-medium text-orange-600 uppercase tracking-wide">Biến chứng</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.diagnosis_management.complications }}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Student Notes -->
        <Card class="bg-white shadow-sm border border-gray-200 overflow-hidden">
          <button @click="toggleSection('notes')"
            class="w-full p-4 flex items-center justify-between hover:bg-indigo-50/50 transition-colors border-l-4 border-indigo-500">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-indigo-100 flex items-center justify-center">
                <FileText class="w-4 h-4 text-indigo-600" stroke="#4f46e5" />
              </div>
              <div class="flex items-center gap-2">
                <CardTitle class="text-base font-semibold text-gray-800">Ghi chú của sinh viên</CardTitle>
                <span v-if="!hasStudentNotes" class="px-2 py-0.5 text-xs font-medium bg-gray-100 text-gray-500 rounded-full">
                  Chưa có ghi chú
                </span>
              </div>
            </div>
            <ChevronDown :class="['h-5 w-5 text-gray-400 transition-transform duration-200', expandedSections.notes && 'rotate-180']" />
          </button>
          <CardContent v-show="expandedSections.notes" class="pt-0 pb-4 px-4 bg-gray-50/30">
            <!-- Empty State -->
            <div v-if="!hasStudentNotes" class="py-8 text-center">
              <div class="w-12 h-12 mx-auto mb-3 rounded-full bg-gray-100 flex items-center justify-center">
                <FileText class="w-6 h-6 text-gray-400" stroke="#9ca3af" />
              </div>
              <p class="text-gray-500 text-sm">Sinh viên chưa thêm ghi chú nào</p>
              <p class="text-gray-400 text-xs mt-1">Ghi chú sẽ hiển thị khi sinh viên điền vào</p>
            </div>
            <!-- Data Display -->
            <div v-else class="pt-3">
              <!-- Tab Navigation -->
              <div class="flex gap-2 border-b border-gray-200 mb-4">
                <button @click="activeNotesTab = 'clinical'" :class="[
                  'px-4 py-2 text-sm font-medium transition-colors rounded-t-lg',
                  activeNotesTab === 'clinical'
                    ? 'text-indigo-600 border-b-2 border-indigo-500 bg-indigo-50'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50',
                ]">
                  Tổng quan
                </button>
                <button @click="activeNotesTab = 'learning'" :class="[
                  'px-4 py-2 text-sm font-medium transition-colors rounded-t-lg',
                  activeNotesTab === 'learning'
                    ? 'text-indigo-600 border-b-2 border-indigo-500 bg-indigo-50'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50',
                ]">
                  Phản ánh học tập
                </button>
              </div>

              <!-- Clinical Tab Content -->
              <div v-if="activeNotesTab === 'clinical'" class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-indigo-600 uppercase tracking-wide">Đánh giá lâm sàng</label>
                  <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed" :class="{ 'text-gray-400 italic': !studentNotes?.clinical_assessment }">
                    {{ studentNotes?.clinical_assessment || "Chưa điền" }}
                  </p>
                </div>
                <div class="p-3 bg-white rounded-lg border border-gray-200">
                  <label class="text-xs font-medium text-indigo-600 uppercase tracking-wide">Chẩn đoán phân biệt</label>
                  <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed" :class="{ 'text-gray-400 italic': !studentNotes?.differential_diagnosis }">
                    {{ studentNotes?.differential_diagnosis || "Chưa điền" }}
                  </p>
                </div>
                <div class="p-3 bg-white rounded-lg border border-gray-200 md:col-span-2">
                  <label class="text-xs font-medium text-indigo-600 uppercase tracking-wide">Kế hoạch điều trị</label>
                  <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed" :class="{ 'text-gray-400 italic': !studentNotes?.treatment_plan }">
                    {{ studentNotes?.treatment_plan || "Chưa điền" }}
                  </p>
                </div>
              </div>

              <!-- Learning Tab Content -->
              <div v-if="activeNotesTab === 'learning'" class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div class="p-3 bg-white rounded-lg border border-gray-200 md:col-span-2">
                  <label class="text-xs font-medium text-indigo-600 uppercase tracking-wide">Suy ngẫm về học tập</label>
                  <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed" :class="{ 'text-gray-400 italic': !studentNotes?.learning_reflections }">
                    {{ studentNotes?.learning_reflections || "Chưa điền" }}
                  </p>
                </div>
                <div class="p-3 bg-white rounded-lg border border-blue-100 bg-blue-50/30">
                  <label class="text-xs font-medium text-blue-600 uppercase tracking-wide">Câu hỏi cho giảng viên</label>
                  <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed" :class="{ 'text-gray-400 italic': !studentNotes?.questions_for_instructor }">
                    {{ studentNotes?.questions_for_instructor || "Không có câu hỏi" }}
                  </p>
                </div>
                <div class="p-3 bg-white rounded-lg border border-orange-100 bg-orange-50/30">
                  <label class="text-xs font-medium text-orange-600 uppercase tracking-wide">Thách thức gặp phải</label>
                  <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed" :class="{ 'text-gray-400 italic': !studentNotes?.challenges_faced }">
                    {{ studentNotes?.challenges_faced || "Không có thách thức được ghi nhận" }}
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Learning Outcomes -->
        <Card class="bg-white shadow-sm border border-gray-200 overflow-hidden">
          <button @click="toggleSection('learning')"
            class="w-full p-4 flex items-center justify-between hover:bg-emerald-50/50 transition-colors border-l-4 border-emerald-500">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-emerald-100 flex items-center justify-center">
                <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <div class="flex items-center gap-2">
                <CardTitle class="text-base font-semibold text-gray-800">Mục tiêu học tập</CardTitle>
                <span v-if="!hasLearningOutcomes" class="px-2 py-0.5 text-xs font-medium bg-gray-100 text-gray-500 rounded-full">
                  Chưa có dữ liệu
                </span>
              </div>
            </div>
            <ChevronDown :class="['h-5 w-5 text-gray-400 transition-transform duration-200', expandedSections.learning && 'rotate-180']" />
          </button>
          <CardContent v-show="expandedSections.learning" class="pt-0 pb-4 px-4 bg-gray-50/30">
            <!-- Empty State -->
            <div v-if="!hasLearningOutcomes" class="py-8 text-center">
              <div class="w-12 h-12 mx-auto mb-3 rounded-full bg-gray-100 flex items-center justify-center">
                <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <p class="text-gray-500 text-sm">Chưa có thông tin mục tiêu học tập</p>
              <p class="text-gray-400 text-xs mt-1">Phần này có thể được thêm bởi giảng viên</p>
            </div>
            <!-- Data Display -->
            <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-3">
              <div v-if="caseData.learning_outcomes?.learning_objectives" class="p-3 bg-white rounded-lg border border-gray-200 md:col-span-2">
                <label class="text-xs font-medium text-emerald-600 uppercase tracking-wide">🎯 Mục tiêu học tập</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.learning_outcomes?.learning_objectives }}
                </p>
              </div>
              <div v-if="caseData.learning_outcomes?.key_concepts" class="p-3 bg-white rounded-lg border border-gray-200">
                <label class="text-xs font-medium text-emerald-600 uppercase tracking-wide">📚 Khái niệm chính</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.learning_outcomes?.key_concepts }}
                </p>
              </div>
              <div v-if="caseData.learning_outcomes?.clinical_pearls" class="p-3 bg-white rounded-lg border border-yellow-100 bg-yellow-50/30">
                <label class="text-xs font-medium text-yellow-600 uppercase tracking-wide">💡 Kinh nghiệm lâm sàng</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.learning_outcomes?.clinical_pearls }}
                </p>
              </div>
              <div v-if="caseData.learning_outcomes?.discussion_points" class="p-3 bg-white rounded-lg border border-gray-200">
                <label class="text-xs font-medium text-emerald-600 uppercase tracking-wide">💬 Điểm thảo luận</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.learning_outcomes?.discussion_points }}
                </p>
              </div>
              <div v-if="caseData.learning_outcomes?.assessment_criteria" class="p-3 bg-white rounded-lg border border-gray-200">
                <label class="text-xs font-medium text-emerald-600 uppercase tracking-wide">✅ Tiêu chí đánh giá</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.learning_outcomes?.assessment_criteria }}
                </p>
              </div>
              <div v-if="caseData.learning_outcomes?.references" class="p-3 bg-white rounded-lg border border-gray-200 md:col-span-2">
                <label class="text-xs font-medium text-emerald-600 uppercase tracking-wide">📖 Tài liệu tham khảo</label>
                <p class="text-gray-800 mt-2 whitespace-pre-wrap leading-relaxed">
                  {{ caseData.learning_outcomes?.references }}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- Grading Section -->
      <div class="space-y-6">
        <Card class="bg-white">
          <CardHeader>
            <div class="flex items-center gap-2">
              <Activity class="text-blue-500 w-5 h-5" stroke="#3b82f6" />
              <CardTitle>Đánh giá và chấm điểm</CardTitle>
            </div>
            <CardDescription class="text-gray-500">
              Đánh giá bệnh án của {{ caseData.created_by_role === 'instructor' ? 'giảng viên' : 'sinh viên' }} {{
                caseData.created_by_name }}
            </CardDescription>
          </CardHeader>
          <CardContent class="space-y-6">
            <!-- Detailed Rubric Criteria -->
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-800">
                  Tiêu chí đánh giá chi tiết <span class="text-red-500">*</span>
                </label>
                <p class="text-sm text-gray-600">
                  Tổng: <span class="text-lg font-bold text-blue-600">{{ totalRubricScore }}/100</span>
                </p>
              </div>

              <div class="grid gap-3">
                <!-- History -->
                <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                  <div class="flex-1">
                    <label class="text-sm font-medium text-gray-700">Tiền sử & Bệnh sử</label>
                  </div>
                  <Input v-model.number="gradingForm.criteria.history" type="number" min="0" max="25" placeholder="0"
                    class="w-14 text-center font-bold" />
                  <span class="text-sm text-gray-500">/25</span>
                </div>

                <!-- Examination -->
                <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                  <div class="flex-1">
                    <label class="text-sm font-medium text-gray-700">Khám lâm sàng</label>
                  </div>
                  <Input v-model.number="gradingForm.criteria.examination" type="number" min="0" max="25"
                    placeholder="0" class="w-14 text-center font-bold" />
                  <span class="text-sm text-gray-500">/25</span>
                </div>

                <!-- Differential Diagnosis -->
                <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                  <div class="flex-1">
                    <label class="text-sm font-medium text-gray-700">Chẩn đoán phân biệt</label>
                  </div>
                  <Input v-model.number="gradingForm.criteria.differential" type="number" min="0" max="20"
                    placeholder="0" class="w-14 text-center font-bold" />
                  <span class="text-sm text-gray-500">/20</span>
                </div>

                <!-- Treatment -->
                <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                  <div class="flex-1">
                    <label class="text-sm font-medium text-gray-700">Kế hoạch điều trị</label>
                  </div>
                  <Input v-model.number="gradingForm.criteria.treatment" type="number" min="0" max="20" placeholder="0"
                    class="w-14 text-center font-bold" />
                  <span class="text-sm text-gray-500">/20</span>
                </div>

                <!-- Presentation -->
                <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                  <div class="flex-1">
                    <label class="text-sm font-medium text-gray-700">Trình bày ca bệnh</label>
                  </div>
                  <Input v-model.number="gradingForm.criteria.presentation" type="number" min="0" max="10"
                    placeholder="0" class="w-14 text-center font-bold" />
                  <span class="text-sm text-gray-500">/10</span>
                </div>
              </div>
            </div>

            <!-- Total Score Display -->
            <div class="space-y-1">
              <label class="text-sm font-medium text-gray-800">
                Điểm tổng <span class="text-red-500">*</span>
              </label>
              <div :class="[
                'p-4 border-2 rounded-lg text-center',
                totalRubricScore > 100 ? 'bg-red-50 border-red-200' : 'bg-blue-50 border-blue-200'
              ]">
                <p :class="[
                  'text-4xl font-bold',
                  totalRubricScore > 100 ? 'text-red-600' : 'text-blue-600'
                ]">{{ totalRubricScore }}/100</p>
                <p class="text-sm text-gray-600 mt-1">
                  <span v-if="totalRubricScore <= 100">
                    Xếp loại: <span class="font-semibold">{{ getLetterGrade(totalRubricScore) }}</span>
                  </span>
                  <span v-else class="text-red-600 font-medium">
                    ⚠ Tổng điểm vượt quá 100
                  </span>
                </p>
              </div>
            </div>

            <!-- Evaluation Notes -->
            <div class="space-y-1">
              <label class="text-sm font-medium text-gray-800">
                Nhận xét chung <span class="text-red-500">*</span>
              </label>
              <p class="text-sm text-gray-500">
                Đưa ra nhận xét tổng quan về bệnh án của sinh viên
              </p>
              <Textarea v-model="gradingForm.evaluation_notes" placeholder="Nhập nhận xét đánh giá tổng quan..."
                class="" />
            </div>

            <!-- Strengths -->
            <div class="space-y-1">
              <label class="text-sm font-medium text-gray-800">
                Điểm mạnh
              </label>
              <p class="text-sm text-gray-500">Những điểm sinh viên làm tốt</p>
              <Textarea v-model="gradingForm.strengths"
                placeholder="- Đánh giá lâm sàng chính xác&#10;- Chẩn đoán phân biệt đầy đủ&#10;- Kế hoạch điều trị hợp lý..."
                class="" />
            </div>

            <!-- Weaknesses / Areas for Improvement -->
            <div class="space-y-1">
              <label class="text-sm font-medium text-gray-800">
                Cần cải thiện
              </label>
              <p class="text-sm text-gray-500">
                Những điểm sinh viên cần phát triển thêm
              </p>
              <Textarea v-model="gradingForm.weaknesses"
                placeholder="- Chẩn đoán phân biệt chưa đầy đủ&#10;- Kế hoạch theo dõi cần chi tiết hơn..." class="" />
            </div>

            <!-- Recommendations -->
            <div class="space-y-1">
              <label class="text-sm font-medium text-gray-800"> Bổ sung </label>
              <p class="text-sm text-gray-500">
                Các điều sinh viên cần bổ sung
              </p>
              <Textarea v-model="gradingForm.recommendations" placeholder="Cần bổ sung thêm xét nghiệm" class="" />
            </div>

            <!-- Grading Criteria (Optional) -->
            <!-- <div class="space-y-3">
              <label class="text-sm font-medium text-gray-800">
                Tiêu chí đánh giá chi tiết (Tùy chọn)
              </label>
              <div class="space-y-2">
                <div
                  class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <span class="text-sm">Tiền sử bệnh</span>
                  <Input
                    v-model.number="gradingForm.criteria.history"
                    type="number"
                    min="0"
                    max="20"
                    class="w-20"
                    placeholder="0-20"
                  />
                </div>
                <div
                  class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <span class="text-sm">Khám lâm sàng</span>
                  <Input
                    v-model.number="gradingForm.criteria.examination"
                    type="number"
                    min="0"
                    max="20"
                    class="w-20"
                    placeholder="0-20"
                  />
                </div>
                <div
                  class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <span class="text-sm">Chẩn đoán phân biệt</span>
                  <Input
                    v-model.number="gradingForm.criteria.differential"
                    type="number"
                    min="0"
                    max="20"
                    class="w-20"
                    placeholder="0-20"
                  />
                </div>
                <div
                  class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <span class="text-sm">Kế hoạch điều trị</span>
                  <Input
                    v-model.number="gradingForm.criteria.treatment"
                    type="number"
                    min="0"
                    max="20"
                    class="w-20"
                    placeholder="0-20"
                  />
                </div>
                <div
                  class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <span class="text-sm">Trình bày và chuyên môn</span>
                  <Input
                    v-model.number="gradingForm.criteria.presentation"
                    type="number"
                    min="0"
                    max="20"
                    class="w-20"
                    placeholder="0-20"
                  />
                </div>
              </div>
            </div> -->

            <!-- Action Buttons -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 text-white">
              <Button @click="saveGrade" :disabled="!canSaveGrade || saving"
                class="w-full bg-blue-600 hover:bg-blue-700"
                :title="rubricValidationMessage || 'Lưu đánh giá dạng nháp'">
                <Save class="h-4 w-4 mr-2" />
                {{ saving ? "Đang lưu..." : "Lưu đánh giá" }}
              </Button>
              <Button @click="submitGrade" :disabled="!canSaveGrade || submitting"
                class="w-full bg-green-600 hover:bg-green-700"
                :title="rubricValidationMessage || 'Nộp điểm chính thức'">
                <CheckCircle class="h-4 w-4 mr-2" />
                {{ submitting ? "Đang gửi..." : "Nộp chấm điểm" }}
              </Button>
            </div>

            <!-- Publish to Feed (only for approved cases, not for instructor templates) -->
            <div v-if="caseData.case_status === 'approved' && caseData.created_by_role !== 'instructor'" class="pt-4 border-t">
              <div class="space-y-3">
                <div class="flex items-center justify-between">
                  <div>
                    <h4 class="text-sm font-medium text-gray-800">Xuất bản lên feed công khai 🌐</h4>
                    <p class="text-xs text-gray-500 mt-1">Chia sẻ ca bệnh chất lượng cao này với sinh viên khác</p>
                  </div>
                </div>

                <div v-if="!isPublishedToFeed" class="space-y-3">
                  <div class="space-y-2">
                    <label class="text-sm font-medium text-gray-700">Phạm vi hiển thị:</label>
                    <select v-model="publishSettings.feedVisibility"
                      class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                      <option value="department">🏢 Cùng khoa</option>
                      <option value="university">🌐 Toàn trường</option>
                    </select>
                  </div>

                  <div class="flex items-center gap-2">
                    <input type="checkbox" id="is-featured" v-model="publishSettings.isFeatured"
                      class="rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
                    <label for="is-featured" class="text-sm text-gray-700">⭐ Đánh dấu là ca bệnh nổi bật</label>
                  </div>

                  <Button @click="publishToFeed" :disabled="publishing"
                    class="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white">
                    {{ publishing ? "Đang xuất bản..." : "📢 Xuất bản lên Feed" }}
                  </Button>
                </div>

                <div v-else class="bg-green-50 border border-green-200 rounded-lg p-4">
                  <div class="flex items-center justify-between">
                    <div>
                      <p class="text-sm font-medium text-green-800">✅ Đã xuất bản lên feed công khai</p>
                      <p class="text-xs text-green-600 mt-1">
                        Phạm vi: {{ publishedFeedVisibility === 'university' ? '🌐 Toàn trường' : '🏢 Cùng khoa' }}
                        {{ publishedIsFeatured ? ' • ⭐ Nổi bật' : '' }}
                      </p>
                    </div>
                    <Button @click="unpublishFromFeed" :disabled="unpublishing" variant="outline" size="sm"
                      class="text-red-600 border-red-300 hover:bg-red-50">
                      {{ unpublishing ? "Đang gỡ..." : "Gỡ xuống" }}
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Medical Attachments -->
        <!-- <Card>
          <CardHeader>
            <CardTitle>📎 Tệp đính kèm y tế</CardTitle>
          </CardHeader>
          <CardContent>
            <MedicalAttachments :case-id="caseId" :can-edit="false" />
          </CardContent>
        </Card> -->
      </div>
    </div>

    <!-- Share Permission Modal -->
    <SharePermissionModal v-model:open="showShareModal" :case-id="Number(caseId)"
      @permission-granted="handlePermissionGranted" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useToast } from "@/composables/useToast";
import Button from "@/components/ui/Button.vue";
import Card from "@/components/ui/Card.vue";
import CardContent from "@/components/ui/CardContent.vue";
import CardDescription from "@/components/ui/CardDescription.vue";
import CardHeader from "@/components/ui/CardHeader.vue";
import CardTitle from "@/components/ui/CardTitle.vue";
import Textarea from "@/components/ui/Textarea.vue";
import Input from "@/components/ui/Input.vue";
import Badge from "@/components/ui/Badge.vue";
import User from "@/components/icons/User.vue";
import FileIcon from "@/components/icons/FileIcon.vue";
import InfoIcon from "@/components/icons/InfoIcon.vue";
import Paperclip from "@/components/icons/Paperclip.vue";

import { ArrowLeft, Save, CheckCircle, ChevronDown } from "@/components/icons";
import { casesService } from "@/services/cases";
import { gradesService } from "@/services/grades";
import feedService from "@/services/feed";
import DocumentIcon from "./icons/DocumentIcon.vue";
import FlaskConical from "./icons/FlaskConical.vue";
import Stethoscope from "./icons/Stethoscope.vue";
import Activity from "./icons/Activity.vue";
import FileText from "./icons/FileText.vue";
import SharePermissionModal from "./SharePermissionModal.vue";

const router = useRouter();

const activeNotesTab = ref<"clinical" | "learning">("clinical");
const showShareModal = ref(false);

// Collapsible sections state
const expandedSections = ref<Record<string, boolean>>({
  basic: true,
  clinical: true,
  physical: true,
  investigations: true,
  diagnosis: true,
  notes: true,
  learning: true
});

const toggleSection = (section: string) => {
  expandedSections.value[section] = !expandedSections.value[section];
};

const props = defineProps<{
  caseId: string;
}>();

const emit = defineEmits<{
  (e: "navigate", page: string): void;
}>();

const { toast } = useToast();

// === Social Feed Publishing ===
const publishing = ref(false);
const unpublishing = ref(false);
const isPublishedToFeed = ref(false);
const publishedFeedVisibility = ref<'department' | 'university'>('department');
const publishedIsFeatured = ref(false);
const publishSettings = ref({
  feedVisibility: 'department' as 'department' | 'university',
  isFeatured: false
});

const publishToFeed = async () => {
  if (publishing.value) return;

  try {
    publishing.value = true;
    await feedService.publishToFeed(
      parseInt(props.caseId),
      {
        feed_visibility: publishSettings.value.feedVisibility,
        is_featured: publishSettings.value.isFeatured
      }
    );

    isPublishedToFeed.value = true;
    publishedFeedVisibility.value = publishSettings.value.feedVisibility;
    publishedIsFeatured.value = publishSettings.value.isFeatured;

    toast.success('Đã xuất bản ca bệnh lên feed công khai!');
  } catch (error) {
    console.error('Failed to publish:', error);
    toast.error('Không thể xuất bản ca bệnh. Vui lòng thử lại.');
  } finally {
    publishing.value = false;
  }
};

const unpublishFromFeed = async () => {
  if (unpublishing.value) return;

  try {
    unpublishing.value = true;
    await feedService.unpublishFromFeed(parseInt(props.caseId));

    isPublishedToFeed.value = false;
    toast.success('Đã gỡ ca bệnh khỏi feed công khai');
  } catch (error) {
    console.error('Failed to unpublish:', error);
    toast.error('Không thể gỡ ca bệnh. Vui lòng thử lại.');
  } finally {
    unpublishing.value = false;
  }
};

// === Unified Reactive Data (used in template) ===
const caseData = ref<UnifiedCaseData>({
  title: "",
  specialty: "",
  case_status: "draft",
  created_by_name: "",
  created_by_id: "",
  created_by_role: "student",
  patient_name: "",
  patient_age: 0,
  patient_gender: "other",
  medical_record_number: "",
  
  // Additional basic fields
  priority_level: "medium",
  complexity_level: "intermediate",
  admission_date: "",
  discharge_date: "",
  case_summary: "",
  chief_complaint_brief: "",
  keywords: "",
  learning_tags: "",
  patient_ethnicity: "",
  patient_occupation: "",
  estimated_study_hours: null,
  requires_follow_up: false,
  follow_up_date: "",

  // Nested or flat — normalized here
  clinical_history: {
    chief_complaint: "",
    history_present_illness: "",
    past_medical_history: "",
    medications: "",
    family_history: "",
    social_history: "",
    allergies: "",
    review_systems: "",
    immunizations: "",
    surgical_history: "",
    review_of_systems: "",
    symptom_duration_days: null,
    symptom_onset: "",
    symptom_progression: "",
  },
  physical_examination: {
    general_appearance: "",
    vital_signs: "",
    vital_signs_temp: "",
    vital_signs_hr: "",
    vital_signs_bp: "",
    vital_signs_rr: "",
    vital_signs_spo2: "",
    weight_kg: "",
    height_cm: "",
    bmi: null,
    consciousness_level: "",
    cardiovascular: "",
    respiratory: "",
    head_neck: "",
    abdominal: "",
    neurological: "",
    musculoskeletal: "",
    skin: "",
    other_systems: "",
  },
  investigations: {
    laboratory_results: "",
    hemoglobin_level: "",
    white_cell_count: "",
    platelet_count: "",
    sodium_level: "",
    potassium_level: "",
    glucose_level: "",
    creatinine_level: "",
    imaging_studies: "",
    ecg_findings: "",
    ecg_rhythm: "",
    ecg_rate: "",
    pathology_results: "",
    microbiology_results: "",
    other_investigations: "",
    special_tests: "",
    microbiology: "",
    biochemistry: "",
    hematology: "",
    arterial_blood_gas: "",
    ph_level: null,
  },
  diagnosis_management: {
    primary_diagnosis: "",
    differential_diagnosis: "",
    treatment_plan: "",
    medications_prescribed: "",
    procedures_performed: "",
    follow_up_plan: "",
    prognosis: "",
    complications: "",
    icd10_codes: "",
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

const studentNotes = ref<StudentNote | null>(null);
const saving = ref(false);
const submitting = ref(false);
const existingGradeId = ref<number | null>(null);
const isFinalGrade = ref(false);

const gradingForm = ref<GradingForm>({
  score: 0,
  evaluation_notes: "",
  strengths: "",
  weaknesses: "",
  recommendations: "",
  criteria: {
    history: 0,
    examination: 0,
    differential: 0,
    treatment: 0,
    presentation: 0,
  },
});

const totalRubricScore = computed(() => {
  const criteria = gradingForm.value.criteria;
  return (
    Number(criteria.history || 0) +
    Number(criteria.examination || 0) +
    Number(criteria.differential || 0) +
    Number(criteria.treatment || 0) +
    Number(criteria.presentation || 0)
  );
});

const canSaveGrade = computed(() => {
  return (
    !isFinalGrade.value &&
    totalRubricScore.value >= 0 &&
    totalRubricScore.value <= 100 &&
    gradingForm.value.evaluation_notes.trim() !== ""
  );
});

const rubricValidationMessage = computed(() => {
  if (totalRubricScore.value > 100) {
    return `Tổng điểm vượt quá 100 (hiện tại: ${totalRubricScore.value}). Vui lòng điều chỉnh.`;
  }
  if (totalRubricScore.value < 0) {
    return "Điểm không thể âm.";
  }
  return "";
});

// Computed properties for checking if sections have data
const hasVitalSigns = computed(() => {
  const pe = caseData.value.physical_examination;
  return pe?.vital_signs_temp || pe?.vital_signs_hr || pe?.vital_signs_bp || 
         pe?.vital_signs_rr || pe?.vital_signs_spo2 || pe?.weight_kg || pe?.height_cm;
});

const hasLabValues = computed(() => {
  const inv = caseData.value.investigations;
  return inv?.hemoglobin_level || inv?.white_cell_count || inv?.platelet_count ||
         inv?.sodium_level || inv?.potassium_level || inv?.glucose_level || inv?.creatinine_level;
});

const hasStudentNotes = computed(() => {
  return studentNotes.value && (
    studentNotes.value.clinical_assessment ||
    studentNotes.value.differential_diagnosis ||
    studentNotes.value.treatment_plan ||
    studentNotes.value.learning_reflections ||
    studentNotes.value.questions_for_instructor ||
    studentNotes.value.challenges_faced
  );
});

const hasLearningOutcomes = computed(() => {
  const lo = caseData.value.learning_outcomes;
  if (!lo) return false;
  return lo.learning_objectives || lo.key_concepts || lo.clinical_pearls ||
         lo.references || lo.discussion_points || lo.assessment_criteria;
});

// === Helper Functions ===
function hasData(section: keyof UnifiedCaseData): boolean {
  const data = caseData.value[section];
  if (!data || typeof data !== "object") return false;
  return Object.values(data).some(
    (v) => v != null && v.toString().trim() !== ""
  );
}

function getStatusLabel(status: CaseStatus): string {
  const map: Record<CaseStatus, string> = {
    draft: "Bản nháp",
    submitted: "Đã nộp",
    reviewed: "Đã duyệt",
    approved: "Đã phê duyệt",
  };
  return map[status] || status;
}

function getStatusBadgeClass(status: CaseStatus): string {
  const map: Record<CaseStatus, string> = {
    draft: "bg-gray-500 text-white",
    submitted: "bg-yellow-500 text-white",
    reviewed: "bg-blue-500 text-white",
    approved: "bg-green-500 text-white",
  };
  return map[status] || "bg-gray-500 text-white";
}

function getGenderLabel(gender: PatientGender): string {
  const map: Record<PatientGender, string> = {
    male: "Nam",
    female: "Nữ",
    other: "Khác",
  };
  return map[gender] || gender;
}

function getComplexityLabel(level: string): string {
  const map: Record<string, string> = {
    basic: "Cơ bản",
    intermediate: "Trung bình",
    advanced: "Nâng cao",
    expert: "Chuyên sâu",
  };
  return map[level] || level || "—";
}

function getPriorityLabel(level: string): string {
  const map: Record<string, string> = {
    low: "Thấp",
    medium: "Trung bình",
    high: "Cao",
    urgent: "Khẩn cấp",
  };
  return map[level] || level || "—";
}

function formatDate(dateStr: string): string {
  if (!dateStr) return "—";
  const date = new Date(dateStr);
  return date.toLocaleDateString("vi-VN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });
}

function getLetterGrade(score: number): string {
  if (score >= 90) return "A";
  if (score >= 80) return "B";
  if (score >= 70) return "C";
  if (score >= 60) return "D";
  return "F";
}

// === Normalize API Data to Unified Format ===
function normalizeCaseData(apiCase: any): UnifiedCaseData {
  return {
    title: apiCase.title || "",
    specialty: apiCase.specialty || "",
    case_status: apiCase.case_status || "draft",
    created_by_name: apiCase.student?.full_name || "",
    created_by_id:
      apiCase.student?.student_id || apiCase.student?.id?.toString() || "",
    created_by_role: apiCase.student?.role || "student",
    patient_name: apiCase.patient_name || "",
    patient_age: apiCase.patient_age || 0,
    patient_gender: apiCase.patient_gender || "other",
    medical_record_number: apiCase.medical_record_number || "",

    // === Additional Basic Fields ===
    priority_level: apiCase.priority_level || "medium",
    complexity_level: apiCase.complexity_level || "intermediate",
    admission_date: apiCase.admission_date || "",
    discharge_date: apiCase.discharge_date || "",
    case_summary: apiCase.case_summary || "",
    chief_complaint_brief: apiCase.chief_complaint_brief || "",
    keywords: apiCase.keywords || "",
    learning_tags: apiCase.learning_tags || "",
    patient_ethnicity: apiCase.patient_ethnicity || "",
    patient_occupation: apiCase.patient_occupation || "",
    estimated_study_hours: apiCase.estimated_study_hours || null,
    requires_follow_up: apiCase.requires_follow_up || false,
    follow_up_date: apiCase.follow_up_date || "",

    // === Clinical History ===
    clinical_history: {
      chief_complaint:
        apiCase.clinical_history?.chief_complaint ||
        apiCase.history?.split("\n")[0] ||
        "",
      history_present_illness:
        apiCase.clinical_history?.history_present_illness ||
        apiCase.history ||
        "",
      past_medical_history:
        apiCase.clinical_history?.past_medical_history || "",
      medications: apiCase.clinical_history?.medications || "",
      family_history: apiCase.clinical_history?.family_history || "",
      social_history: apiCase.clinical_history?.social_history || "",
      allergies: apiCase.clinical_history?.allergies || "",
      review_systems: apiCase.clinical_history?.review_systems || "",
      immunizations: apiCase.clinical_history?.immunizations || "",
      surgical_history: apiCase.clinical_history?.surgical_history || "",
      review_of_systems: apiCase.clinical_history?.review_of_systems || "",
      symptom_duration_days: apiCase.clinical_history?.symptom_duration_days || null,
      symptom_onset: apiCase.clinical_history?.symptom_onset || "",
      symptom_progression: apiCase.clinical_history?.symptom_progression || "",
    },

    // === Physical Examination ===
    physical_examination: {
      general_appearance:
        apiCase.physical_examination?.general_appearance || "",
      vital_signs: apiCase.physical_examination?.vital_signs || "",
      vital_signs_temp: apiCase.physical_examination?.vital_signs_temp || "",
      vital_signs_hr: apiCase.physical_examination?.vital_signs_hr || "",
      vital_signs_bp: apiCase.physical_examination?.vital_signs_bp || "",
      vital_signs_rr: apiCase.physical_examination?.vital_signs_rr || "",
      vital_signs_spo2: apiCase.physical_examination?.vital_signs_spo2 || "",
      weight_kg: apiCase.physical_examination?.weight_kg || "",
      height_cm: apiCase.physical_examination?.height_cm || "",
      bmi: apiCase.physical_examination?.bmi || null,
      consciousness_level: apiCase.physical_examination?.consciousness_level || "",
      cardiovascular: apiCase.physical_examination?.cardiovascular || "",
      respiratory: apiCase.physical_examination?.respiratory || "",
      head_neck: apiCase.physical_examination?.head_neck || "",
      abdominal: apiCase.physical_examination?.abdominal || "",
      neurological: apiCase.physical_examination?.neurological || "",
      musculoskeletal: apiCase.physical_examination?.musculoskeletal || "",
      skin: apiCase.physical_examination?.skin || "",
      other_systems: apiCase.physical_examination?.other_systems || "",
    },

    // === Investigations ===
    investigations: {
      laboratory_results:
        apiCase.detailed_investigations?.laboratory_results ||
        apiCase.investigations ||
        "",
      hemoglobin_level: apiCase.detailed_investigations?.hemoglobin_level || "",
      white_cell_count: apiCase.detailed_investigations?.white_cell_count || "",
      platelet_count: apiCase.detailed_investigations?.platelet_count || "",
      sodium_level: apiCase.detailed_investigations?.sodium_level || "",
      potassium_level: apiCase.detailed_investigations?.potassium_level || "",
      glucose_level: apiCase.detailed_investigations?.glucose_level || "",
      creatinine_level: apiCase.detailed_investigations?.creatinine_level || "",
      imaging_studies: apiCase.detailed_investigations?.imaging_studies || "",
      ecg_findings: apiCase.detailed_investigations?.ecg_findings || "",
      ecg_rhythm: apiCase.detailed_investigations?.ecg_rhythm || "",
      ecg_rate: apiCase.detailed_investigations?.ecg_rate || "",
      pathology_results:
        apiCase.detailed_investigations?.pathology_results || "",
      microbiology_results: apiCase.detailed_investigations?.microbiology_results || "",
      other_investigations: apiCase.detailed_investigations?.other_investigations || "",
      special_tests: apiCase.detailed_investigations?.special_tests || "",
      microbiology: apiCase.detailed_investigations?.microbiology || "",
      biochemistry: apiCase.detailed_investigations?.biochemistry || "",
      hematology: apiCase.detailed_investigations?.hematology || "",
      arterial_blood_gas: apiCase.detailed_investigations?.arterial_blood_gas || "",
      ph_level: apiCase.detailed_investigations?.ph_level || null,
    },

    // === Diagnosis & Management ===
    diagnosis_management: {
      primary_diagnosis:
        apiCase.diagnosis_management?.primary_diagnosis ||
        apiCase.diagnosis ||
        "",
      differential_diagnosis:
        apiCase.diagnosis_management?.differential_diagnosis || "",
      treatment_plan:
        apiCase.diagnosis_management?.treatment_plan || apiCase.treatment || "",
      medications_prescribed:
        apiCase.diagnosis_management?.medications_prescribed || "",
      procedures_performed:
        apiCase.diagnosis_management?.procedures_performed || "",
      follow_up_plan:
        apiCase.diagnosis_management?.follow_up_plan || apiCase.follow_up || "",
      prognosis: apiCase.diagnosis_management?.prognosis || "",
      complications: apiCase.diagnosis_management?.complications || "",
      icd10_codes: apiCase.diagnosis_management?.icd10_codes || "",
    },

    // === Learning Outcomes ===
    learning_outcomes: {
      learning_objectives: apiCase.learning_outcomes?.learning_objectives || "",
      key_concepts: apiCase.learning_outcomes?.key_concepts || "",
      clinical_pearls: apiCase.learning_outcomes?.clinical_pearls || "",
      references: apiCase.learning_outcomes?.references || "",
      discussion_points: apiCase.learning_outcomes?.discussion_points || "",
      assessment_criteria: apiCase.learning_outcomes?.assessment_criteria || "",
    },
  };
}

// === Save / Submit Grade ===
async function saveGrade() {
  if (totalRubricScore.value > 100) {
    toast.error(`Tổng điểm vượt quá 100 (hiện tại: ${totalRubricScore.value}). Vui lòng điều chỉnh.`);
    return;
  }
  if (totalRubricScore.value < 0) {
    toast.error("Điểm không thể âm.");
    return;
  }
  if (!canSaveGrade.value) {
    toast.error("Vui lòng nhập điểm số và nhận xét");
    return;
  }
  saving.value = true;
  try {
    // Ensure all criteria values are valid numbers
    const criteria = {
      history: Number(gradingForm.value.criteria.history) || 0,
      examination: Number(gradingForm.value.criteria.examination) || 0,
      differential: Number(gradingForm.value.criteria.differential) || 0,
      treatment: Number(gradingForm.value.criteria.treatment) || 0,
      presentation: Number(gradingForm.value.criteria.presentation) || 0,
    };

    const payload: GradeSubmission = {
      grade_scale: "percentage",
      score: totalRubricScore.value,
      letter_grade: getLetterGrade(totalRubricScore.value),
      evaluation_notes: gradingForm.value.evaluation_notes || "",
      strengths: gradingForm.value.strengths || "",
      weaknesses: gradingForm.value.weaknesses || "",
      recommendations: gradingForm.value.recommendations || "",
      grading_criteria: criteria,
      is_final: false,
      case: Number(props.caseId),
    };

    console.log("SAVE payload →", payload);

    if (existingGradeId.value) {
      // Update existing draft grade
      await gradesService.updateGrade(existingGradeId.value.toString(), payload);
    } else {
      // Create new draft grade
      const result = await gradesService.saveGrade(payload);
      existingGradeId.value = result.id;
    }

    toast.success("Đánh giá đã được lưu thành công!");
  } catch (error: unknown) {
    const err = error as import("axios").AxiosError<{ [k: string]: string[] }>;
    console.error("Save error:", err);
    if (err.response?.data) console.error("Response data:", err.response.data);
    toast.error("Không thể lưu đánh giá.");
  } finally {
    saving.value = false;
  }
}

async function submitGrade() {
  if (isFinalGrade.value) {
    toast.error("Điểm đã được nộp. Không thể thay đổi.");
    return;
  }
  if (totalRubricScore.value > 100) {
    toast.error(`Tổng điểm vượt quá 100 (hiện tại: ${totalRubricScore.value}). Vui lòng điều chỉnh.`);
    return;
  }
  if (totalRubricScore.value < 0) {
    toast.error("Điểm không thể âm.");
    return;
  }
  if (!canSaveGrade.value) {
    toast.error("Vui lòng nhập điểm số và nhận xét");
    return;
  }
  submitting.value = true;
  try {
    // Ensure all criteria values are valid numbers
    const criteria = {
      history: Number(gradingForm.value.criteria.history) || 0,
      examination: Number(gradingForm.value.criteria.examination) || 0,
      differential: Number(gradingForm.value.criteria.differential) || 0,
      treatment: Number(gradingForm.value.criteria.treatment) || 0,
      presentation: Number(gradingForm.value.criteria.presentation) || 0,
    };

    const payload: GradeSubmission = {
      grade_scale: "percentage",
      score: totalRubricScore.value,
      letter_grade: getLetterGrade(totalRubricScore.value),
      evaluation_notes: gradingForm.value.evaluation_notes || "",
      strengths: gradingForm.value.strengths || "",
      weaknesses: gradingForm.value.weaknesses || "",
      recommendations: gradingForm.value.recommendations || "",
      grading_criteria: criteria,
      is_final: true,
      case: Number(props.caseId),
    };

    console.log("SUBMIT payload →", payload);

    if (existingGradeId.value) {
      // Update existing grade to final
      await gradesService.updateGrade(existingGradeId.value.toString(), payload);
    } else {
      // Create new final grade
      const result = await gradesService.submitGrade(payload);
      existingGradeId.value = result.id;
    }

    // Update case status to reviewed
    await casesService.updateCase(props.caseId, { case_status: 'reviewed' });

    // Set flag to disable further edits
    isFinalGrade.value = true;
    caseData.value.case_status = 'reviewed';

    toast.success("Chấm điểm hoàn tất!");

    // Refresh cases store before navigating
    const { useCasesStore } = await import('@/stores/cases');
    await useCasesStore().fetchCases();

    setTimeout(() => emit("navigate", "dashboard"), 1500);
  } catch (error: unknown) {
    const err = error as import("axios").AxiosError<{ [k: string]: string[] }>;
    console.error("Submit error:", err);
    if (err.response?.data) console.error("Response data:", err.response.data);
    toast.error("Không thể hoàn thành chấm điểm.");
  } finally {
    submitting.value = false;
  }
}

function handlePermissionGranted() {
  showShareModal.value = false;
  toast.success("Đã chia sẻ ca bệnh thành công!");
}

// === Lifecycle ===
onMounted(async () => {
  try {
    const apiCase = await casesService.getCase(props.caseId);

    // Normalize to unified structure
    caseData.value = normalizeCaseData(apiCase);

    // Load student notes
    try {
      studentNotes.value = await casesService.getStudentNotes(props.caseId);
    } catch (err) {
      console.log("No student notes");
    }

    // Always try to load existing grade (don't rely on has_grade flag)
    try {
      console.log("Fetching grade for case:", props.caseId);
      const grade = await gradesService.getGrade(props.caseId);
      console.log("Grade API response:", grade);
      if (grade) {
        existingGradeId.value = grade.id;
        isFinalGrade.value = grade.is_final || false;

        gradingForm.value = {
          score: grade.score ?? 0,
          evaluation_notes: grade.evaluation_notes || "",
          strengths: grade.strengths || "",
          weaknesses: grade.weaknesses || "",
          recommendations: grade.recommendations || "",
          criteria: {
            history: grade.grading_criteria?.history ?? 0,
            examination: grade.grading_criteria?.examination ?? 0,
            differential: grade.grading_criteria?.differential ?? 0,
            treatment: grade.grading_criteria?.treatment ?? 0,
            presentation: grade.grading_criteria?.presentation ?? 0,
          },
        };
        console.log("Loaded existing grade with criteria:", gradingForm.value.criteria);
      } else {
        console.log("No grade found in API response");
      }
    } catch (err) {
      console.log("Error fetching grade:", err);
    }
  } catch (error) {
    console.error("Load failed:", error);
    toast.error("Không thể tải dữ liệu ca bệnh");
  }
});

// === Types ===
type CaseStatus = "draft" | "submitted" | "reviewed" | "approved";
type PatientGender = "male" | "female" | "other";

interface ClinicalHistory {
  chief_complaint?: string;
  history_present_illness?: string;
  past_medical_history?: string;
  medications?: string;
  family_history?: string;
  social_history?: string;
  allergies?: string;
  review_systems?: string;
  immunizations?: string;
  surgical_history?: string;
  review_of_systems?: string;
  symptom_duration_days?: number | null;
  symptom_onset?: string;
  symptom_progression?: string;
}

interface PhysicalExamination {
  general_appearance?: string;
  vital_signs?: string;
  vital_signs_temp?: string;
  vital_signs_hr?: string;
  vital_signs_bp?: string;
  vital_signs_rr?: string;
  vital_signs_spo2?: string;
  weight_kg?: string;
  height_cm?: string;
  bmi?: number | null;
  consciousness_level?: string;
  cardiovascular?: string;
  respiratory?: string;
  head_neck?: string;
  abdominal?: string;
  neurological?: string;
  musculoskeletal?: string;
  skin?: string;
  other_systems?: string;
}

interface Investigations {
  laboratory_results?: string;
  hemoglobin_level?: string;
  white_cell_count?: string;
  platelet_count?: string;
  sodium_level?: string;
  potassium_level?: string;
  glucose_level?: string;
  creatinine_level?: string;
  imaging_studies?: string;
  ecg_findings?: string;
  ecg_rhythm?: string;
  ecg_rate?: string;
  pathology_results?: string;
  microbiology_results?: string;
  other_investigations?: string;
  special_tests?: string;
  microbiology?: string;
  biochemistry?: string;
  hematology?: string;
  arterial_blood_gas?: string;
  ph_level?: number | null;
}

interface DiagnosisManagement {
  primary_diagnosis?: string;
  differential_diagnosis?: string;
  treatment_plan?: string;
  medications_prescribed?: string;
  procedures_performed?: string;
  follow_up_plan?: string;
  prognosis?: string;
  complications?: string;
  icd10_codes?: string;
}

interface LearningOutcomes {
  learning_objectives?: string;
  key_concepts?: string;
  clinical_pearls?: string;
  references?: string;
  discussion_points?: string;
  assessment_criteria?: string;
}

interface UnifiedCaseData {
  title: string;
  specialty: string;
  case_status: CaseStatus;
  created_by_name: string;
  created_by_id: string;
  created_by_role: string;
  patient_name: string;
  patient_age: number;
  patient_gender: PatientGender;
  medical_record_number: string;
  // Additional basic fields
  priority_level?: string;
  complexity_level?: string;
  admission_date?: string;
  discharge_date?: string;
  case_summary?: string;
  chief_complaint_brief?: string;
  keywords?: string;
  learning_tags?: string;
  patient_ethnicity?: string;
  patient_occupation?: string;
  estimated_study_hours?: number | null;
  requires_follow_up?: boolean;
  follow_up_date?: string;
  // Nested sections
  clinical_history: ClinicalHistory;
  physical_examination: PhysicalExamination;
  investigations: Investigations;
  diagnosis_management: DiagnosisManagement;
  learning_outcomes?: LearningOutcomes;
}

interface StudentNote {
  clinical_assessment?: string;
  differential_diagnosis?: string;
  treatment_plan?: string;
  learning_reflections?: string;
  questions_for_instructor?: string;
  challenges_faced?: string;
}

interface GradingCriteria {
  history: number;
  examination: number;
  differential: number;
  treatment: number;
  presentation: number;
}

interface GradingForm {
  score: number;
  evaluation_notes: string;
  strengths: string;
  weaknesses: string;
  criteria: GradingCriteria;
  recommendations: string;
}

interface GradeSubmission {
  grade_scale: string;
  score: number;
  letter_grade: string;
  evaluation_notes: string;
  strengths: string;
  weaknesses: string;
  recommendations: string;
  grading_criteria: GradingCriteria;
  is_final: boolean;
  case: number;
}
</script>
