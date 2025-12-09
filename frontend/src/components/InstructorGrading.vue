<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <div
      class="flex flex-col md:flex-row md:items-center justify-between gap-4"
    >
      <div class="flex items-center gap-3">
        <Button
          variant="ghost"
          size="icon"
          @click="$emit('navigate', 'dashboard')"
        >
          <ArrowLeft class="h-5 w-5" />
        </Button>
        <div>
          <h1 class="text-2xl font-bold text-gray-800 mb-1">
            {{ caseData.title }}
          </h1>
          <div class="flex items-center gap-2">
            <Badge variant="secondary">{{ caseData.specialty }}</Badge>
            <Badge :class="getStatusBadgeClass(caseData.case_status)">
              {{ getStatusLabel(caseData.case_status) }}
            </Badge>
          </div>
          <p class="text-sm text-gray-500 mt-1">
            Sinh viên: {{ caseData.created_by_name }} ({{
              caseData.created_by_id
            }})
          </p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <Button
          variant="outline"
          @click="showShareModal = true"
          class="flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
          </svg>
          Chia sẻ ca bệnh
        </Button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Case Information (Read-only for instructors) -->
      <div class="space-y-3">
        <!-- Basic Information -->
        <Card class="bg-white">
          <button 
            @click="toggleSection('basic')" 
            class="w-full p-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
          >
            <div class="flex items-center gap-2">
              <InfoIcon stroke="#3b82f6" />
              <CardTitle class="text-base">Thông tin cơ bản</CardTitle>
            </div>
            <ChevronDown :class="['h-5 w-5 transition-transform', expandedSections.basic && 'rotate-180']" />
          </button>
          <CardContent v-show="expandedSections.basic" class="pt-0 pb-4 px-4 space-y-3">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm text-gray-500">Tiêu đề</label>
                <p class="text-gray-800">{{ caseData.title || "N/A" }}</p>
              </div>
              <div>
                <label class="text-sm text-gray-500">Chuyên khoa</label>
                <p class="text-gray-800">{{ caseData.specialty || "N/A" }}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Patient Information -->
        <Card class="bg-white">
          <button 
            @click="toggleSection('patient')" 
            class="w-full p-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
          >
            <div class="flex items-center gap-2">
              <User class="w-5 h-5 text-blue-500" />
              <CardTitle class="text-base">Thông tin bệnh nhân</CardTitle>
            </div>
            <ChevronDown :class="['h-5 w-5 transition-transform', expandedSections.patient && 'rotate-180']" />
          </button>
          <CardContent v-show="expandedSections.patient" class="pt-0 pb-4 px-4 space-y-3">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm text-gray-500">Tuổi</label>
                <p class="text-gray-800">{{ caseData.patient_age || "N/A" }}</p>
              </div>
              <div>
                <label class="text-sm text-gray-500">Giới tính</label>
                <p class="text-gray-800">
                  {{ getGenderLabel(caseData.patient_gender) || "N/A" }}
                </p>
              </div>
              <div>
                <label class="text-sm text-gray-500">Số hồ sơ bệnh án</label>
                <p class="text-gray-800">
                  {{ caseData.medical_record_number || "N/A" }}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Clinical History -->
        <Card v-if="hasData('clinical_history')" class="bg-white">
          <button 
            @click="toggleSection('clinical')" 
            class="w-full p-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
          >
            <div class="flex items-center gap-2">
              <DocumentIcon class="text-blue-500 w-5 h-5" stroke="#3b82f6" />
              <CardTitle class="text-base">Tiền sử lâm sàng</CardTitle>
            </div>
            <ChevronDown :class="['h-5 w-5 transition-transform', expandedSections.clinical && 'rotate-180']" />
          </button>
          <CardContent v-show="expandedSections.clinical" class="pt-0 pb-4 px-4 space-y-3">
            <div v-if="caseData.clinical_history?.chief_complaint">
              <label class="text-sm font-medium text-gray-500"
                >Lý do khám chính</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.clinical_history?.chief_complaint || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.clinical_history?.history_present_illness">
              <label class="text-sm font-medium text-gray-500"
                >Bệnh sử hiện tại</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{
                  caseData.clinical_history?.history_present_illness || "N/A"
                }}
              </p>
            </div>
            <div v-if="caseData.clinical_history?.past_medical_history">
              <label class="text-sm font-medium text-gray-500"
                >Tiền sử bệnh tật</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.clinical_history?.past_medical_history || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.clinical_history?.family_history">
              <label class="text-sm font-medium text-gray-500"
                >Tiền sử gia đình</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.clinical_history?.family_history || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.clinical_history?.social_history">
              <label class="text-sm font-medium text-gray-500"
                >Tiền sử xã hội</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.clinical_history?.social_history || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.clinical_history?.allergies">
              <label class="text-sm font-medium text-gray-500"
                >Dị ứng</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.clinical_history?.allergies || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.clinical_history?.medications">
              <label class="text-sm font-medium text-gray-500"
                >Thuốc đang sử dụng</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.clinical_history?.medications || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.clinical_history?.review_systems">
              <label class="text-sm font-medium text-gray-500"
                >Đánh giá hệ thống</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.clinical_history?.review_systems || "N/A" }}
              </p>
            </div>
          </CardContent>
        </Card>

        <!-- Physical Examination -->
        <Card v-if="hasData('physical_examination')" class="bg-white">
          <button 
            @click="toggleSection('physical')" 
            class="w-full p-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
          >
            <div class="flex items-center gap-2">
              <FlaskConical class="text-blue-500 w-5 h-5" stroke="#3b82f6" />
              <CardTitle class="text-base">Khám lâm sàng</CardTitle>
            </div>
            <ChevronDown :class="['h-5 w-5 transition-transform', expandedSections.physical && 'rotate-180']" />
          </button>
          <CardContent v-show="expandedSections.physical" class="pt-0 pb-4 px-4 space-y-3">
            <div v-if="caseData.physical_examination?.general_appearance">
              <label class="text-sm font-medium text-gray-500"
                >Tình trạng chung</label
              >
              <p class="text-gray-800 mt-1">
                {{ caseData.physical_examination.general_appearance || "N/A" }}
              </p>
            </div>
            
            <!-- Detailed Vital Signs -->
            <div class="grid grid-cols-2 gap-3">
              <div v-if="caseData.physical_examination?.vital_signs_temp">
                <label class="text-sm font-medium text-gray-500">Nhiệt độ</label>
                <p class="text-gray-800 mt-1">{{ caseData.physical_examination.vital_signs_temp }}°C</p>
              </div>
              <div v-if="caseData.physical_examination?.vital_signs_hr">
                <label class="text-sm font-medium text-gray-500">Nhịp tim</label>
                <p class="text-gray-800 mt-1">{{ caseData.physical_examination.vital_signs_hr }} bpm</p>
              </div>
              <div v-if="caseData.physical_examination?.vital_signs_bp">
                <label class="text-sm font-medium text-gray-500">Huyết áp</label>
                <p class="text-gray-800 mt-1">{{ caseData.physical_examination.vital_signs_bp }} mmHg</p>
              </div>
              <div v-if="caseData.physical_examination?.vital_signs_rr">
                <label class="text-sm font-medium text-gray-500">Nhịp thở</label>
                <p class="text-gray-800 mt-1">{{ caseData.physical_examination.vital_signs_rr }} /phút</p>
              </div>
              <div v-if="caseData.physical_examination?.vital_signs_spo2">
                <label class="text-sm font-medium text-gray-500">SpO2</label>
                <p class="text-gray-800 mt-1">{{ caseData.physical_examination.vital_signs_spo2 }}%</p>
              </div>
              <div v-if="caseData.physical_examination?.weight_kg">
                <label class="text-sm font-medium text-gray-500">Cân nặng</label>
                <p class="text-gray-800 mt-1">{{ caseData.physical_examination.weight_kg }} kg</p>
              </div>
              <div v-if="caseData.physical_examination?.height_cm">
                <label class="text-sm font-medium text-gray-500">Chiều cao</label>
                <p class="text-gray-800 mt-1">{{ caseData.physical_examination.height_cm }} cm</p>
              </div>
            </div>

            <div v-if="caseData.physical_examination?.vital_signs">
              <label class="text-sm font-medium text-gray-500">Ghi chú sinh hiệu</label>
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.physical_examination.vital_signs || "N/A" }}
              </p>
            </div>
            
            <div v-if="caseData.physical_examination?.cardiovascular">
              <label class="text-sm font-medium text-gray-500">Tim mạch</label>
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.physical_examination.cardiovascular || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.physical_examination?.respiratory">
              <label class="text-sm font-medium text-gray-500">Hô hấp</label>
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.physical_examination.respiratory || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.physical_examination?.abdominal">
              <label class="text-sm font-medium text-gray-500">Bụng</label>
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.physical_examination.abdominal || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.physical_examination?.neurological">
              <label class="text-sm font-medium text-gray-500">Thần kinh</label>
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.physical_examination.neurological || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.physical_examination?.musculoskeletal">
              <label class="text-sm font-medium text-gray-500">Cơ xương khớp</label>
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.physical_examination.musculoskeletal || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.physical_examination?.skin">
              <label class="text-sm font-medium text-gray-500">Da</label>
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.physical_examination.skin || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.physical_examination?.head_neck">
              <label class="text-sm font-medium text-gray-500">Đầu và cổ</label>
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.physical_examination.head_neck || "N/A" }}
              </p>
            </div>
          </CardContent>
        </Card>

        <!-- Investigations -->
        <Card v-if="hasData('investigations')" class="bg-white">
          <button 
            @click="toggleSection('investigations')" 
            class="w-full p-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
          >
            <div class="flex items-center gap-2">
              <FlaskConical class="text-blue-500 w-5 h-5" stroke="#3b82f6" />
              <CardTitle class="text-base">Cận lâm sàng</CardTitle>
            </div>
            <ChevronDown :class="['h-5 w-5 transition-transform', expandedSections.investigations && 'rotate-180']" />
          </button>
          <CardContent v-show="expandedSections.investigations" class="pt-0 pb-4 px-4 space-y-3">
            <div v-if="caseData.investigations?.laboratory_results">
              <label class="text-sm font-medium text-gray-500"
                >Xét nghiệm tổng quát</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.investigations.laboratory_results || "N/A" }}
              </p>
            </div>
            
            <!-- Detailed Lab Values -->
            <div class="grid grid-cols-2 gap-3">
              <div v-if="caseData.investigations?.hemoglobin_level">
                <label class="text-sm font-medium text-gray-500">Hemoglobin</label>
                <p class="text-gray-800 mt-1">{{ caseData.investigations.hemoglobin_level }} g/dL</p>
              </div>
              <div v-if="caseData.investigations?.white_cell_count">
                <label class="text-sm font-medium text-gray-500">WBC</label>
                <p class="text-gray-800 mt-1">{{ caseData.investigations.white_cell_count }} ×10⁹/L</p>
              </div>
              <div v-if="caseData.investigations?.platelet_count">
                <label class="text-sm font-medium text-gray-500">Tiểu cầu</label>
                <p class="text-gray-800 mt-1">{{ caseData.investigations.platelet_count }} ×10⁹/L</p>
              </div>
              <div v-if="caseData.investigations?.sodium_level">
                <label class="text-sm font-medium text-gray-500">Natri</label>
                <p class="text-gray-800 mt-1">{{ caseData.investigations.sodium_level }} mmol/L</p>
              </div>
              <div v-if="caseData.investigations?.potassium_level">
                <label class="text-sm font-medium text-gray-500">Kali</label>
                <p class="text-gray-800 mt-1">{{ caseData.investigations.potassium_level }} mmol/L</p>
              </div>
              <div v-if="caseData.investigations?.creatinine_level">
                <label class="text-sm font-medium text-gray-500">Creatinine</label>
                <p class="text-gray-800 mt-1">{{ caseData.investigations.creatinine_level }} mg/dL</p>
              </div>
              <div v-if="caseData.investigations?.glucose_level">
                <label class="text-sm font-medium text-gray-500">Glucose</label>
                <p class="text-gray-800 mt-1">{{ caseData.investigations.glucose_level }} mg/dL</p>
              </div>
            </div>

            <div v-if="caseData.investigations?.imaging_studies">
              <label class="text-sm font-medium text-gray-500"
                >Chẩn đoán hình ảnh</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.investigations.imaging_studies || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.investigations?.ecg_findings">
              <label class="text-sm font-medium text-gray-500"
                >Điện tâm đồ</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.investigations.ecg_findings || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.investigations?.pathology_results">
              <label class="text-sm font-medium text-gray-500"
                >Giải phẫu bệnh</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.investigations.pathology_results || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.investigations?.microbiology_results">
              <label class="text-sm font-medium text-gray-500"
                >Vi sinh</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.investigations.microbiology_results || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.investigations?.other_investigations">
              <label class="text-sm font-medium text-gray-500"
                >Xét nghiệm khác</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.investigations.other_investigations || "N/A" }}
              </p>
            </div>
          </CardContent>
        </Card>

        <!-- Diagnosis and Management -->
        <Card v-if="hasData('diagnosis_management')" class="bg-white">
          <button 
            @click="toggleSection('diagnosis')" 
            class="w-full p-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
          >
            <div class="flex items-center gap-2">
              <Stethoscope class="text-blue-500 w-5 h-5" stroke="#3b82f6" />
              <CardTitle class="text-base">Chẩn đoán và điều trị</CardTitle>
            </div>
            <ChevronDown :class="['h-5 w-5 transition-transform', expandedSections.diagnosis && 'rotate-180']" />
          </button>
          <CardContent v-show="expandedSections.diagnosis" class="pt-0 pb-4 px-4 space-y-3">
            <div v-if="caseData.diagnosis_management?.primary_diagnosis">
              <label class="text-sm font-medium text-gray-500"
                >Chẩn đoán chính</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.diagnosis_management.primary_diagnosis || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.diagnosis_management?.differential_diagnosis">
              <label class="text-sm font-medium text-gray-500"
                >Chẩn đoán phân biệt</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.diagnosis_management.differential_diagnosis || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.diagnosis_management?.icd10_codes">
              <label class="text-sm font-medium text-gray-500"
                >Mã ICD-10</label
              >
              <p class="text-gray-800 mt-1">
                {{ caseData.diagnosis_management.icd10_codes || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.diagnosis_management?.treatment_plan">
              <label class="text-sm font-medium text-gray-500"
                >Kế hoạch điều trị</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.diagnosis_management.treatment_plan || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.diagnosis_management?.medications_prescribed">
              <label class="text-sm font-medium text-gray-500"
                >Thuốc được kê đơn</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.diagnosis_management.medications_prescribed || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.diagnosis_management?.procedures_performed">
              <label class="text-sm font-medium text-gray-500"
                >Thủ thuật đã thực hiện</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.diagnosis_management.procedures_performed || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.diagnosis_management?.follow_up_plan">
              <label class="text-sm font-medium text-gray-500"
                >Kế hoạch theo dõi</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.diagnosis_management.follow_up_plan || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.diagnosis_management?.prognosis">
              <label class="text-sm font-medium text-gray-500"
                >Tiên lượng</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.diagnosis_management.prognosis || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.diagnosis_management?.complications">
              <label class="text-sm font-medium text-gray-500"
                >Biến chứng</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.diagnosis_management.complications || "N/A" }}
              </p>
            </div>
          </CardContent>
        </Card>

        <!-- Student Notes -->
        <Card class="bg-white">
          <button 
            @click="toggleSection('notes')" 
            class="w-full p-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
          >
            <div class="flex items-center gap-2">
              <FileText class="text-blue-500 w-5 h-5" stroke="#3b82f6" />
              <CardTitle class="text-base">Ghi chú của sinh viên</CardTitle>
            </div>
            <ChevronDown :class="['h-5 w-5 transition-transform', expandedSections.notes && 'rotate-180']" />
          </button>
          <CardContent v-show="expandedSections.notes" class="pt-0 pb-4 px-4 space-y-3">
            <CardDescription class="text-gray-500 text-sm">
              Xem lại ghi chú lâm sàng của sinh viên
            </CardDescription>
            <!-- Tab Navigation -->
            <div class="flex gap-2 border-b border-gray-200">
              <button
                @click="activeNotesTab = 'clinical'"
                :class="[
                  'px-4 py-2 text-sm font-medium transition-colors',
                  activeNotesTab === 'clinical'
                    ? 'text-blue-500 border-b-2 border-blue-500'
                    : 'text-gray-500 hover:text-gray-700',
                ]"
              >
                Tổng quan
              </button>
              <button
                @click="activeNotesTab = 'learning'"
                :class="[
                  'px-4 py-2 text-sm font-medium transition-colors',
                  activeNotesTab === 'learning'
                    ? 'text-blue-500 border-b-2 border-blue-500'
                    : 'text-gray-500 hover:text-gray-700',
                ]"
              >
                Phản ánh học tập
              </button>
            </div>

            <!-- Clinical Tab Content -->
            <div v-if="activeNotesTab === 'clinical'" class="space-y-4">
              <div>
                <label class="text-sm font-medium text-gray-500"
                  >Đánh giá lâm sàng</label
                >
                <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                  {{ studentNotes?.clinical_assessment || "Trống" }}
                </p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500"
                  >Chẩn đoán phân biệt</label
                >
                <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                  {{ studentNotes?.differential_diagnosis || "Trống" }}
                </p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500"
                  >Kế hoạch điều trị</label
                >
                <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                  {{ studentNotes?.treatment_plan || "Trống" }}
                </p>
              </div>
            </div>

            <!-- Learning Tab Content -->
            <div v-if="activeNotesTab === 'learning'" class="space-y-4">
              <div>
                <label class="text-sm font-medium text-gray-500"
                  >Suy ngẫm về học tập</label
                >
                <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                  {{ studentNotes?.learning_reflections || "Trống" }}
                </p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500"
                  >Câu hỏi cho giảng viên</label
                >
                <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                  {{ studentNotes?.questions_for_instructor || "Trống" }}
                </p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500"
                  >Thách thức gặp phải</label
                >
                <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                  {{ studentNotes?.challenges_faced || "Trống" }}
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
              Đánh giá bệnh án của sinh viên {{ caseData.created_by_name }}
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
                  <Input
                    v-model.number="gradingForm.criteria.history"
                    type="number"
                    min="0"
                    max="25"
                    placeholder="0"
                    class="w-14 text-center font-bold"
                  />
                  <span class="text-sm text-gray-500">/25</span>
                </div>
                
                <!-- Examination -->
                <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                  <div class="flex-1">
                    <label class="text-sm font-medium text-gray-700">Khám lâm sàng</label>
                  </div>
                  <Input
                    v-model.number="gradingForm.criteria.examination"
                    type="number"
                    min="0"
                    max="25"
                    placeholder="0"
                    class="w-14 text-center font-bold"
                  />
                  <span class="text-sm text-gray-500">/25</span>
                </div>
                
                <!-- Differential Diagnosis -->
                <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                  <div class="flex-1">
                    <label class="text-sm font-medium text-gray-700">Chẩn đoán phân biệt</label>
                  </div>
                  <Input
                    v-model.number="gradingForm.criteria.differential"
                    type="number"
                    min="0"
                    max="20"
                    placeholder="0"
                    class="w-14 text-center font-bold"
                  />
                  <span class="text-sm text-gray-500">/20</span>
                </div>
                
                <!-- Treatment -->
                <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                  <div class="flex-1">
                    <label class="text-sm font-medium text-gray-700">Kế hoạch điều trị</label>
                  </div>
                  <Input
                    v-model.number="gradingForm.criteria.treatment"
                    type="number"
                    min="0"
                    max="20"
                    placeholder="0"
                    class="w-14 text-center font-bold"
                  />
                  <span class="text-sm text-gray-500">/20</span>
                </div>
                
                <!-- Presentation -->
                <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                  <div class="flex-1">
                    <label class="text-sm font-medium text-gray-700">Trình bày ca bệnh</label>
                  </div>
                  <Input
                    v-model.number="gradingForm.criteria.presentation"
                    type="number"
                    min="0"
                    max="10"
                    placeholder="0"
                    class="w-14 text-center font-bold"
                  />
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
              <Textarea
                v-model="gradingForm.evaluation_notes"
                placeholder="Nhập nhận xét đánh giá tổng quan..."
                class=""
              />
            </div>

            <!-- Strengths -->
            <div class="space-y-1">
              <label class="text-sm font-medium text-gray-800">
                Điểm mạnh
              </label>
              <p class="text-sm text-gray-500">Những điểm sinh viên làm tốt</p>
              <Textarea
                v-model="gradingForm.strengths"
                placeholder="- Đánh giá lâm sàng chính xác&#10;- Chẩn đoán phân biệt đầy đủ&#10;- Kế hoạch điều trị hợp lý..."
                class=""
              />
            </div>

            <!-- Weaknesses / Areas for Improvement -->
            <div class="space-y-1">
              <label class="text-sm font-medium text-gray-800">
                Cần cải thiện
              </label>
              <p class="text-sm text-gray-500">
                Những điểm sinh viên cần phát triển thêm
              </p>
              <Textarea
                v-model="gradingForm.weaknesses"
                placeholder="- Chẩn đoán phân biệt chưa đầy đủ&#10;- Kế hoạch theo dõi cần chi tiết hơn..."
                class=""
              />
            </div>

            <!-- Recommendations -->
            <div class="space-y-1">
              <label class="text-sm font-medium text-gray-800"> Bổ sung </label>
              <p class="text-sm text-gray-500">
                Các điều sinh viên cần bổ sung
              </p>
              <Textarea
                v-model="gradingForm.recommendations"
                placeholder="Cần bổ sung thêm xét nghiệm"
                class=""
              />
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
              <Button
                @click="saveGrade"
                :disabled="!canSaveGrade || saving"
                class="w-full bg-blue-600 hover:bg-blue-700"
                :title="rubricValidationMessage || 'Lưu đánh giá dạng nháp'"
              >
                <Save class="h-4 w-4 mr-2" />
                {{ saving ? "Đang lưu..." : "Lưu đánh giá" }}
              </Button>
              <Button
                @click="submitGrade"
                :disabled="!canSaveGrade || submitting"
                class="w-full bg-green-600 hover:bg-green-700"
                :title="rubricValidationMessage || 'Nộp điểm chính thức'"
              >
                <CheckCircle class="h-4 w-4 mr-2" />
                {{ submitting ? "Đang gửi..." : "Nộp chấm điểm" }}
              </Button>
            </div>

            <!-- Publish to Feed (only for approved cases) -->
            <div v-if="caseData.case_status === 'approved'" class="pt-4 border-t">
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
                    <select 
                      v-model="publishSettings.feedVisibility" 
                      class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="department">🏢 Cùng khoa</option>
                      <option value="university">🌐 Toàn trường</option>
                    </select>
                  </div>
                  
                  <div class="flex items-center gap-2">
                    <input 
                      type="checkbox" 
                      id="is-featured" 
                      v-model="publishSettings.isFeatured"
                      class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <label for="is-featured" class="text-sm text-gray-700">⭐ Đánh dấu là ca bệnh nổi bật</label>
                  </div>
                  
                  <Button
                    @click="publishToFeed"
                    :disabled="publishing"
                    class="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white"
                  >
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
                    <Button
                      @click="unpublishFromFeed"
                      :disabled="unpublishing"
                      variant="outline"
                      size="sm"
                      class="text-red-600 border-red-300 hover:bg-red-50"
                    >
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
    <SharePermissionModal
      v-model:open="showShareModal"
      :case-id="Number(caseId)"
      @permission-granted="handlePermissionGranted"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
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

const activeNotesTab = ref<"clinical" | "learning">("clinical");
const showShareModal = ref(false);

// Collapsible sections state
const expandedSections = ref<Record<string, boolean>>({
  basic: true,
  patient: true,
  clinical: true,
  physical: true,
  investigations: true,
  diagnosis: true,
  notes: true
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
  patient_name: "",
  patient_age: 0,
  patient_gender: "other",
  medical_record_number: "",

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
  },
  physical_examination: {
    general_appearance: "",
    vital_signs: "",
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
    imaging_studies: "",
    ecg_findings: "",
    pathology_results: "",
    special_tests: "",
    microbiology: "",
    biochemistry: "",
    hematology: "",
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
    patient_name: apiCase.patient_name || "",
    patient_age: apiCase.patient_age || 0,
    patient_gender: apiCase.patient_gender || "other",
    medical_record_number: apiCase.medical_record_number || "",

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

interface UnifiedCaseData {
  title: string;
  specialty: string;
  case_status: CaseStatus;
  created_by_name: string;
  created_by_id: string;
  patient_name: string;
  patient_age: number;
  patient_gender: PatientGender;
  medical_record_number: string;
  clinical_history: ClinicalHistory;
  physical_examination: PhysicalExamination;
  investigations: Investigations;
  diagnosis_management: DiagnosisManagement;
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
