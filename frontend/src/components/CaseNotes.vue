<template>
  <div class="p-6 space-y-4 max-w-7xl mx-auto">
    <!-- Compact Header -->
    <div class="flex items-center justify-between gap-4 bg-white p-4 rounded-lg shadow-sm">
      <div class="flex items-center gap-3">
        <Button variant="ghost" size="sm" @click="$emit('navigate', 'dashboard')">
          <ArrowLeft class="h-4 w-4" />
        </Button>
        <div>
          <h1 class="text-xl font-bold text-gray-800">{{ caseData.title }}</h1>
          <div class="flex items-center gap-2 mt-1">
            <Badge variant="secondary" class="text-xs">{{ caseData.specialty }}</Badge>
            <Badge v-if="caseStatus === 'draft'" class="bg-yellow-500 text-white text-xs">Bản nháp</Badge>
            <Badge v-else-if="caseStatus === 'submitted'" class="bg-blue-500 text-white text-xs">Đã nộp</Badge>
            <Badge v-else-if="caseStatus === 'reviewed'" class="bg-purple-500 text-white text-xs">Đã xem xét</Badge>
            <Badge v-else-if="caseStatus === 'approved'" class="bg-green-500 text-white text-xs">Đã phê duyệt</Badge>
            <Badge v-if="caseData.priority_level === 'urgent'" class="bg-red-500 text-white text-xs">Khẩn cấp</Badge>
            <Badge v-else-if="caseData.priority_level === 'high'" class="bg-orange-500 text-white text-xs">Cao</Badge>
          </div>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <Button variant="outline" size="sm" @click="handleSave" :disabled="!hasUnsavedChanges || !canEdit">
          <Save class="h-4 w-4 mr-2" />
          Lưu
        </Button>
        <Button size="sm" @click="handleSubmit" class="bg-blue-600 hover:bg-blue-700" :disabled="!canEdit">
          <Send class="h-4 w-4 mr-2" />
          Nộp
        </Button>
      </div>
    </div>

    <!-- Permission Notice -->
    <div v-if="!canEdit" class="text-sm text-amber-600 bg-amber-50 px-3 py-2 rounded-md border border-amber-200">
      <span v-if="!isOwner">⚠️ Bạn không phải là chủ sở hữu của ca bệnh này. Chỉ được xem.</span>
      <span v-else-if="!isDraft">ℹ️ Ca bệnh đã được nộp. Không thể chỉnh sửa.</span>
    </div>

    <!-- Grade Display for Students -->
    <Card v-if="gradeData && gradeData.is_final" class="bg-gradient-to-br from-purple-50 to-indigo-50 border-purple-200">
      <CardHeader>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <div class="p-2 bg-purple-100 rounded-lg">
              <svg class="h-5 w-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
              </svg>
            </div>
            <CardTitle class="text-purple-900">Kết quả đánh giá</CardTitle>
          </div>
          <div class="text-right">
            <div class="text-3xl font-bold text-purple-900">{{ gradeData.score }}%</div>
            <div class="text-sm text-purple-700">Xếp loại: {{ gradeData.letter_grade }}</div>
          </div>
        </div>
      </CardHeader>
      <CardContent class="space-y-3">
        <div v-if="gradeData.evaluation_notes">
          <label class="text-sm font-semibold text-purple-900">Nhận xét chung</label>
          <p class="text-sm text-gray-700 mt-1 whitespace-pre-wrap">{{ gradeData.evaluation_notes }}</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div v-if="gradeData.strengths">
            <label class="text-sm font-semibold text-green-900">✓ Điểm mạnh</label>
            <p class="text-sm text-gray-700 mt-1 whitespace-pre-wrap">{{ gradeData.strengths }}</p>
          </div>
          <div v-if="gradeData.weaknesses">
            <label class="text-sm font-semibold text-orange-900">⚠ Cần cải thiện</label>
            <p class="text-sm text-gray-700 mt-1 whitespace-pre-wrap">{{ gradeData.weaknesses }}</p>
          </div>
        </div>
        <div v-if="gradeData.recommendations">
          <label class="text-sm font-semibold text-blue-900">💡 Khuyến nghị</label>
          <p class="text-sm text-gray-700 mt-1 whitespace-pre-wrap">{{ gradeData.recommendations }}</p>
        </div>
        <div v-if="gradeData.grading_criteria" class="border-t border-purple-200 pt-3">
          <label class="text-sm font-semibold text-purple-900 mb-2 block">Tiêu chí đánh giá chi tiết</label>
          <div class="grid grid-cols-2 md:grid-cols-5 gap-2">
            <div class="text-center p-2 bg-white rounded border border-purple-100">
              <div class="text-xs text-gray-500">Tiền sử</div>
              <div class="text-lg font-bold text-purple-900">{{ gradeData.grading_criteria.history || 0 }}</div>
            </div>
            <div class="text-center p-2 bg-white rounded border border-purple-100">
              <div class="text-xs text-gray-500">Khám</div>
              <div class="text-lg font-bold text-purple-900">{{ gradeData.grading_criteria.examination || 0 }}</div>
            </div>
            <div class="text-center p-2 bg-white rounded border border-purple-100">
              <div class="text-xs text-gray-500">Chẩn đoán</div>
              <div class="text-lg font-bold text-purple-900">{{ gradeData.grading_criteria.differential || 0 }}</div>
            </div>
            <div class="text-center p-2 bg-white rounded border border-purple-100">
              <div class="text-xs text-gray-500">Điều trị</div>
              <div class="text-lg font-bold text-purple-900">{{ gradeData.grading_criteria.treatment || 0 }}</div>
            </div>
            <div class="text-center p-2 bg-white rounded border border-purple-100">
              <div class="text-xs text-gray-500">Trình bày</div>
              <div class="text-lg font-bold text-purple-900">{{ gradeData.grading_criteria.presentation || 0 }}</div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <!-- Left Column: Case Information (Collapsible Sections) -->
      <div class="space-y-3">
        <!-- Basic Information -->
        <Card>
          <button 
            @click="toggleSection('basic')" 
            class="w-full p-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
          >
            <div class="flex items-center gap-2">
              <span class="text-lg">🏥</span>
              <CardTitle class="text-base">Thông tin cơ bản</CardTitle>
            </div>
            <ChevronDown :class="['h-5 w-5 transition-transform', expandedSections.basic && 'rotate-180']" />
          </button>
          <CardContent v-show="expandedSections.basic" class="pt-0 pb-4 px-4 space-y-3">
            <div class="space-y-3">
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="text-xs text-gray-500">Tiêu đề</label>
                  <Input v-model="caseData.title" placeholder="Nhập tiêu đề..." :disabled="!canEdit" class="text-sm" />
                </div>
                <div>
                  <label class="text-xs text-gray-500">Chuyên khoa</label>
                  <select v-model="caseData.specialty" class="w-full p-2 text-sm border rounded-md" :disabled="!canEdit">
                    <option value="">Chọn chuyên khoa</option>
                    <option value="Hồi sức tích cực">Hồi sức tích cực</option>
                    <option value="Tim mạch">Tim mạch</option>
                    <option value="Nội khoa">Nội khoa</option>
                    <option value="Phẫu thuật">Phẫu thuật</option>
                    <option value="Hô hấp">Hô hấp</option>
                    <option value="Tiêu hóa">Tiêu hóa</option>
                    <option value="Thần kinh">Thần kinh</option>
                    <option value="Sản phụ khoa">Sản phụ khoa</option>
                    <option value="Nhi khoa">Nhi khoa</option>
                    <option value="Khác">Khác</option>
                  </select>
                </div>
                <div>
                  <label class="text-xs text-gray-500">Mức độ ưu tiên</label>
                  <select v-model="caseData.priority_level" class="w-full p-2 text-sm border rounded-md" :disabled="!canEdit">
                    <option value="low">Thấp</option>
                    <option value="medium">Trung bình</option>
                    <option value="high">Cao</option>
                    <option value="urgent">Khẩn cấp</option>
                  </select>
                </div>
                <div>
                  <label class="text-xs text-gray-500">Mức độ phức tạp</label>
                  <select v-model="caseData.complexity_level" class="w-full p-2 text-sm border rounded-md" :disabled="!canEdit">
                    <option value="basic">Cơ bản</option>
                    <option value="intermediate">Trung cấp</option>
                    <option value="advanced">Nâng cao</option>
                    <option value="expert">Chuyên gia</option>
                  </select>
                </div>
              </div>
              <div>
                <label class="text-xs text-gray-500">Tóm tắt ca bệnh</label>
                <Textarea v-model="caseData.case_summary" placeholder="Tóm tắt ngắn gọn..." :disabled="!canEdit" rows="2" class="text-sm" />
              </div>
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="text-xs text-gray-500">Tags học tập</label>
                  <Input v-model="caseData.learning_tags" placeholder="tim mạch, cấp cứu" :disabled="!canEdit" class="text-sm" />
                </div>
                <div>
                  <label class="text-xs text-gray-500">Giờ học ước tính</label>
                  <Input v-model="caseData.estimated_study_hours" type="number" placeholder="Số giờ" :disabled="!canEdit" class="text-sm" />
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Patient Information -->
        <Card>
          <button 
            @click="toggleSection('patient')" 
            class="w-full p-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
          >
            <div class="flex items-center gap-2">
              <span class="text-lg">👤</span>
              <CardTitle class="text-base">Thông tin bệnh nhân</CardTitle>
            </div>
            <ChevronDown :class="['h-5 w-5 transition-transform', expandedSections.patient && 'rotate-180']" />
          </button>
          <CardContent v-show="expandedSections.patient" class="pt-0 pb-4 px-4 space-y-3">
            <div class="grid grid-cols-2 gap-4">
              <!-- Patient name hidden - auto-generated -->
              <input type="hidden" v-model="caseData.patient_name" />
              <div>
                <label class="text-sm text-gray-500">Tuổi</label>
                <Input v-model="caseData.patient_age" type="number" placeholder="Tuổi..." :disabled="!canEdit" />
              </div>
              <div>
                <label class="text-sm text-gray-500">Giới tính</label>
                <select v-model="caseData.patient_gender" class="w-full p-2 border rounded-md" :disabled="!canEdit">
                  <option value="">Chọn giới tính</option>
                  <option value="male">Nam</option>
                  <option value="female">Nữ</option>
                  <option value="other">Khác</option>
                  <option value="not_specified">Không xác định</option>
                </select>
              </div>
              <div>
                <label class="text-sm text-gray-500">Số hồ sơ bệnh án</label>
                <Input v-model="caseData.medical_record_number" placeholder="Số hồ sơ..." :disabled="!canEdit" />
              </div>
              <div>
                <label class="text-sm text-gray-500">Dân tộc</label>
                <Input v-model="caseData.patient_ethnicity" placeholder="Dân tộc bệnh nhân..." :disabled="!canEdit" />
              </div>
              <div>
                <label class="text-sm text-gray-500">Nghề nghiệp</label>
                <Input v-model="caseData.patient_occupation" placeholder="Nghề nghiệp..." :disabled="!canEdit" />
              </div>
              <div>
                <label class="text-sm text-gray-500">Ngày nhập viện</label>
                <Input v-model="caseData.admission_date" type="date" :disabled="!canEdit" />
              </div>
              <div>
                <label class="text-sm text-gray-500">Ngày xuất viện</label>
                <Input v-model="caseData.discharge_date" type="date" :disabled="!canEdit" />
              </div>
            </div>
            <div>
              <label class="text-sm text-gray-500">Lý do khám ngắn gọn</label>
              <Input v-model="caseData.chief_complaint_brief" placeholder="Lý do chính đến khám..." :disabled="!canEdit" />
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div class="flex items-center space-x-2">
                <input v-model="caseData.requires_follow_up" type="checkbox" :disabled="!canEdit" class="w-4 h-4" />
                <label class="text-sm text-gray-500">Yêu cầu theo dõi</label>
              </div>
              <div v-if="caseData.requires_follow_up">
                <label class="text-sm text-gray-500">Ngày theo dõi</label>
                <Input v-model="caseData.follow_up_date" type="date" :disabled="!canEdit" />
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Clinical History -->
        <Card>
          <button 
            @click="toggleSection('clinical')" 
            class="w-full p-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
          >
            <div class="flex items-center gap-2">
              <span class="text-lg">📋</span>
              <CardTitle class="text-base">Tiền sử lâm sàng</CardTitle>
            </div>
            <ChevronDown :class="['h-5 w-5 transition-transform', expandedSections.clinical && 'rotate-180']" />
          </button>
          <CardContent v-show="expandedSections.clinical" class="pt-0 pb-4 px-4 space-y-3">
            <div>
              <label class="text-sm text-gray-500">Lý do khám chính</label>
              <Textarea v-model="caseData.clinical_history.chief_complaint" placeholder="Lý do khám chính..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Bệnh sử hiện tại</label>
              <Textarea v-model="caseData.clinical_history.history_present_illness" placeholder="Bệnh sử hiện tại..." :disabled="!canEdit" />
            </div>
            <div class="grid grid-cols-3 gap-4">
              <div>
                <label class="text-sm text-gray-500">Thời gian có triệu chứng (ngày)</label>
                <Input v-model="caseData.clinical_history.symptom_duration_days" type="number" placeholder="Số ngày..." :disabled="!canEdit" />
              </div>
              <div>
                <label class="text-sm text-gray-500">Khởi phát triệu chứng</label>
                <select v-model="caseData.clinical_history.symptom_onset" class="w-full p-2 border rounded-md" :disabled="!canEdit">
                  <option value="">Chọn</option>
                  <option value="sudden">Đột ngột</option>
                  <option value="gradual">Từ từ</option>
                  <option value="chronic">Mạn tính</option>
                </select>
              </div>
              <div>
                <label class="text-sm text-gray-500">Diễn biến triệu chứng</label>
                <select v-model="caseData.clinical_history.symptom_progression" class="w-full p-2 border rounded-md" :disabled="!canEdit">
                  <option value="">Chọn</option>
                  <option value="improving">Cải thiện</option>
                  <option value="worsening">Xấu đi</option>
                  <option value="stable">Ổn định</option>
                  <option value="fluctuating">Biến đổi</option>
                </select>
              </div>
            </div>
            <div>
              <label class="text-sm text-gray-500">Tiền sử bệnh tật</label>
              <Textarea v-model="caseData.clinical_history.past_medical_history" placeholder="Tiền sử bệnh tật..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Tiền sử gia đình</label>
              <Textarea v-model="caseData.clinical_history.family_history" placeholder="Tiền sử gia đình..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Tiền sử xã hội (hút thuốc, uống rượu, v.v.)</label>
              <Textarea v-model="caseData.clinical_history.social_history" placeholder="Tiền sử xã hội..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Dị ứng</label>
              <Textarea v-model="caseData.clinical_history.allergies" placeholder="Các chất gây dị ứng..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Thuốc đang sử dụng</label>
              <Textarea v-model="caseData.clinical_history.medications" placeholder="Thuốc đang dùng..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Hỏi bệnh theo hệ thống</label>
              <Textarea v-model="caseData.clinical_history.review_systems" placeholder="Đánh giá các hệ thống..." :disabled="!canEdit" />
            </div>
          </CardContent>
        </Card>

        <!-- Physical Examination -->
        <Card>
          <button 
            @click="toggleSection('physical')" 
            class="w-full p-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
          >
            <div class="flex items-center gap-2">
              <span class="text-lg">🩺</span>
              <CardTitle class="text-base">Khám lâm sàng</CardTitle>
            </div>
            <ChevronDown :class="['h-5 w-5 transition-transform', expandedSections.physical && 'rotate-180']" />
          </button>
          <CardContent v-show="expandedSections.physical" class="pt-0 pb-4 px-4 space-y-3">
            <div>
              <label class="text-sm text-gray-500">Tình trạng chung</label>
              <Textarea v-model="caseData.physical_examination.general_appearance" placeholder="Tình trạng chung..." :disabled="!canEdit" />
            </div>
            
            <!-- Vital Signs Detail -->
            <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
              <div>
                <label class="text-sm text-gray-500">Nhiệt Độ (°C)</label>
                <Input v-model="caseData.physical_examination.vital_signs_temp" type="number" step="0.1" placeholder="37.0" :disabled="!canEdit" />
              </div>
              <div>
                <label class="text-sm text-gray-500">Nhịp Tim (bpm)</label>
                <Input v-model="caseData.physical_examination.vital_signs_hr" type="number" placeholder="72" :disabled="!canEdit" />
              </div>
              <div>
                <label class="text-sm text-gray-500">Huyết Áp (mmHg)</label>
                <Input v-model="caseData.physical_examination.vital_signs_bp" placeholder="120/80" :disabled="!canEdit" />
              </div>
              <div>
                <label class="text-sm text-gray-500">Nhịp Thở (lần/phút)</label>
                <Input v-model="caseData.physical_examination.vital_signs_rr" type="number" placeholder="16" :disabled="!canEdit" />
              </div>
              <div>
                <label class="text-sm text-gray-500">Độ Bão Hòa Oxy (%)</label>
                <Input v-model="caseData.physical_examination.vital_signs_spo2" type="number" placeholder="98" :disabled="!canEdit" />
              </div>
              <div>
                <label class="text-sm text-gray-500">Cân Nặng (kg)</label>
                <Input v-model="caseData.physical_examination.weight_kg" type="number" step="0.1" placeholder="70" :disabled="!canEdit" />
              </div>
              <div>
                <label class="text-sm text-gray-500">Chiều Cao (cm)</label>
                <Input v-model="caseData.physical_examination.height_cm" type="number" step="0.1" placeholder="170" :disabled="!canEdit" />
              </div>
            </div>
            
            <div>
              <label class="text-sm text-gray-500">Sinh hiệu (Ghi chú)</label>
              <Textarea v-model="caseData.physical_examination.vital_signs" placeholder="Ghi chú về sinh hiệu..." :disabled="!canEdit" />
            </div>
            
            <div>
              <label class="text-sm text-gray-500">Tim mạch</label>
              <Textarea v-model="caseData.physical_examination.cardiovascular" placeholder="Khám tim mạch..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Hô hấp</label>
              <Textarea v-model="caseData.physical_examination.respiratory" placeholder="Khám hô hấp..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Bụng</label>
              <Textarea v-model="caseData.physical_examination.abdominal" placeholder="Khám bụng..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Thần kinh</label>
              <Textarea v-model="caseData.physical_examination.neurological" placeholder="Khám thần kinh..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Cơ xương khớp</label>
              <Textarea v-model="caseData.physical_examination.musculoskeletal" placeholder="Khám cơ xương khớp..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Da</label>
              <Textarea v-model="caseData.physical_examination.skin" placeholder="Khám da..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Đầu và cổ</label>
              <Textarea v-model="caseData.physical_examination.head_neck" placeholder="Khám đầu và cổ..." :disabled="!canEdit" />
            </div>
          </CardContent>
        </Card>

        <!-- Investigations -->
        <Card>
          <button 
            @click="toggleSection('investigations')" 
            class="w-full p-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
          >
            <div class="flex items-center gap-2">
              <span class="text-lg">🧪</span>
              <CardTitle class="text-base">Cận lâm sàng</CardTitle>
            </div>
            <ChevronDown :class="['h-5 w-5 transition-transform', expandedSections.investigations && 'rotate-180']" />
          </button>
          <CardContent v-show="expandedSections.investigations" class="pt-0 pb-4 px-4 space-y-3">
            <div>
              <label class="text-sm text-gray-500">Xét nghiệm (Tổng quan)</label>
              <Textarea v-model="caseData.investigations.laboratory_results" placeholder="Kết quả xét nghiệm tổng quan..." :disabled="!canEdit" />
            </div>
            
            <!-- Lab Values Detail -->
            <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
              <div>
                <label class="text-sm text-gray-500">Hemoglobin (g/dL)</label>
                <Input v-model="caseData.investigations.hemoglobin_level" type="number" step="0.1" placeholder="14.0" :disabled="!canEdit" />
              </div>
              <div>
                <label class="text-sm text-gray-500">Số Lượng Bạch Cầu (10^9/L)</label>
                <Input v-model="caseData.investigations.white_cell_count" type="number" step="0.1" placeholder="7.5" :disabled="!canEdit" />
              </div>
              <div>
                <label class="text-sm text-gray-500">Số Lượng Tiểu Cầu (10^9/L)</label>
                <Input v-model="caseData.investigations.platelet_count" type="number" placeholder="250" :disabled="!canEdit" />
              </div>
              <div>
                <label class="text-sm text-gray-500">Natri (mmol/L)</label>
                <Input v-model="caseData.investigations.sodium_level" type="number" step="0.1" placeholder="140" :disabled="!canEdit" />
              </div>
              <div>
                <label class="text-sm text-gray-500">Kali (mmol/L)</label>
                <Input v-model="caseData.investigations.potassium_level" type="number" step="0.1" placeholder="4.0" :disabled="!canEdit" />
              </div>
              <div>
                <label class="text-sm text-gray-500">Creatinine (mg/dL)</label>
                <Input v-model="caseData.investigations.creatinine_level" type="number" step="0.1" placeholder="1.0" :disabled="!canEdit" />
              </div>
              <div>
                <label class="text-sm text-gray-500">Glucose (mg/dL)</label>
                <Input v-model="caseData.investigations.glucose_level" type="number" placeholder="100" :disabled="!canEdit" />
              </div>
            </div>
            
            <div>
              <label class="text-sm text-gray-500">Chẩn đoán hình ảnh</label>
              <Textarea v-model="caseData.investigations.imaging_studies" placeholder="Kết quả chẩn đoán hình ảnh..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Điện tâm đồ</label>
              <Textarea v-model="caseData.investigations.ecg_findings" placeholder="Kết quả điện tâm đồ..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Kết quả giải phẫu bệnh</label>
              <Textarea v-model="caseData.investigations.pathology_results" placeholder="Kết quả giải phẫu bệnh..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Kết quả Vi sinh</label>
              <Textarea v-model="caseData.investigations.microbiology_results" placeholder="Kết quả vi sinh..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Xét nghiệm khác</label>
              <Textarea v-model="caseData.investigations.other_investigations" placeholder="Các xét nghiệm khác..." :disabled="!canEdit" />
            </div>
          </CardContent>
        </Card>

        <!-- Diagnosis and Management -->
        <Card>
          <button 
            @click="toggleSection('diagnosis')" 
            class="w-full p-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
          >
            <div class="flex items-center gap-2">
              <span class="text-lg">💊</span>
              <CardTitle class="text-base">Chẩn đoán và điều trị</CardTitle>
            </div>
            <ChevronDown :class="['h-5 w-5 transition-transform', expandedSections.diagnosis && 'rotate-180']" />
          </button>
          <CardContent v-show="expandedSections.diagnosis" class="pt-0 pb-4 px-4 space-y-3">
            <div>
              <label class="text-sm text-gray-500">Chẩn đoán chính</label>
              <Textarea v-model="caseData.diagnosis_management.primary_diagnosis" placeholder="Chẩn đoán chính..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Chẩn đoán phân biệt</label>
              <Textarea v-model="caseData.diagnosis_management.differential_diagnosis" placeholder="Các chẩn đoán phân biệt..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Mã ICD-10</label>
              <Input v-model="caseData.diagnosis_management.icd10_codes" placeholder="Mã ICD-10..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Kế hoạch điều trị</label>
              <Textarea v-model="caseData.diagnosis_management.treatment_plan" placeholder="Kế hoạch điều trị..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Thủ thuật đã thực hiện</label>
              <Textarea v-model="caseData.diagnosis_management.procedures_performed" placeholder="Các thủ thuật đã thực hiện..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Tiên lượng</label>
              <Textarea v-model="caseData.diagnosis_management.prognosis" placeholder="Tiên lượng bệnh..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Kế hoạch theo dõi</label>
              <Textarea v-model="caseData.diagnosis_management.follow_up_plan" placeholder="Kế hoạch theo dõi..." :disabled="!canEdit" />
            </div>
          </CardContent>
        </Card>

        <!-- Learning Outcomes -->
        <Card>
          <button 
            @click="toggleSection('learning')" 
            class="w-full p-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
          >
            <div class="flex items-center gap-2">
              <span class="text-lg">📚</span>
              <CardTitle class="text-base">Kết quả học tập</CardTitle>
            </div>
            <ChevronDown :class="['h-5 w-5 transition-transform', expandedSections.learning && 'rotate-180']" />
          </button>
          <CardContent v-show="expandedSections.learning" class="pt-0 pb-4 px-4 space-y-3">
            <div>
              <label class="text-sm text-gray-500">Mục tiêu học tập</label>
              <Textarea v-model="caseData.learning_outcomes.learning_objectives" placeholder="Mục tiêu học tập từ ca bệnh này..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Khái niệm chính</label>
              <Textarea v-model="caseData.learning_outcomes.key_concepts" placeholder="Các khái niệm y khoa chính..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Kinh nghiệm lâm sàng</label>
              <Textarea v-model="caseData.learning_outcomes.clinical_pearls" placeholder="Những bài học và kinh nghiệm lâm sàng quan trọng..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Điểm thảo luận</label>
              <Textarea v-model="caseData.learning_outcomes.discussion_points" placeholder="Các điểm để thảo luận..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Tiêu chí đánh giá</label>
              <Textarea v-model="caseData.learning_outcomes.assessment_criteria" placeholder="Tiêu chí để đánh giá hiểu biết..." :disabled="!canEdit" />
            </div>
            <div>
              <label class="text-sm text-gray-500">Tài liệu tham khảo</label>
              <Textarea v-model="caseData.learning_outcomes.references" placeholder="Tài liệu, bài báo tham khảo..." :disabled="!canEdit" />
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- Student Notes Section -->
      <div class="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Ghi chú lâm sàng của bạn</CardTitle>
            <CardDescription>
              Hoàn thành đánh giá và kế hoạch cho ca bệnh này
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs v-model="activeTab" default-value="assessment" class="w-full">
              <TabsList class="grid w-full grid-cols-2 sm:grid-cols-4">
                <TabsTrigger value="assessment">Đánh giá</TabsTrigger>
                <TabsTrigger value="differential">Chẩn đoán</TabsTrigger>
                <TabsTrigger value="plan">Kế hoạch</TabsTrigger>
                <TabsTrigger value="learning">Học tập</TabsTrigger>
              </TabsList>

              <TabsContent value="assessment" class="space-y-4">
                <div class="space-y-2">
                  <label class="text-sm font-medium text-gray-800">Đánh giá lâm sàng</label>
                  <p class="text-sm text-gray-500">
                    Đưa ra đánh giá lâm sàng của bạn về bệnh nhân này dựa trên tiền sử, khám lâm sàng và các kết quả
                    chẩn đoán.
                  </p>
                  <Textarea rows="10" v-model="notes.clinical_assessment" placeholder="Viết đánh giá lâm sàng của bạn ở đây..."
                    class="min-h-[400px]" @input="handleNoteChange" />
                </div>
              </TabsContent>

              <TabsContent value="differential" class="space-y-4">
                <div class="space-y-2">
                  <label class="text-sm font-medium text-gray-800">Chẩn đoán phân biệt</label>
                  <p class="text-sm text-gray-500">
                    Liệt kê và giải thích các chẩn đoán phân biệt theo thứ tự khả năng.
                  </p>
                  <Textarea rows="10" v-model="notes.differential_diagnosis"
                    placeholder="1. Chẩn đoán có khả năng nhất và lý do&#10;2. Chẩn đoán phân biệt thứ hai và tại sao...&#10;3. Những cân nhắc khác..."
                    class="min-h-[400px]" @input="handleNoteChange" />
                </div>
              </TabsContent>

              <TabsContent value="plan" class="space-y-4">
                <div class="space-y-2">
                  <label class="text-sm font-medium text-gray-800">Kế hoạch điều trị</label>
                  <p class="text-sm text-gray-500">
                    Phác thảo kế hoạch quản lý ngay lập tức và dài hạn cho bệnh nhân này.
                  </p>
                  <Textarea rows="10" v-model="notes.treatment_plan"
                    placeholder="Xử trí ngay:&#10;- &#10;&#10;Xét nghiệm thêm:&#10;- &#10;&#10;Quản lý dài hạn:&#10;- "
                    class="min-h-[400px]" @input="handleNoteChange" />
                </div>
              </TabsContent>

              <TabsContent value="learning" class="space-y-4">
                <div class="space-y-2">
                  <label class="text-sm font-medium text-gray-800">Điểm học tập</label>
                  <p class="text-sm text-gray-500">
                    Suy ngẫm về những gì bạn đã học được từ ca bệnh này và bất kỳ câu hỏi nào bạn có.
                  </p>
                  <Textarea rows="10" v-model="notes.learning_reflections"
                    placeholder="Điểm học tập chính:&#10;- &#10;&#10;Câu hỏi cho giảng viên:&#10;- &#10;&#10;Lĩnh vực cần nghiên cứu thêm:&#10;- "
                    class="min-h-[400px]" @input="handleNoteChange" />
                </div>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>📎 Tệp đính kèm y tế</CardTitle>
          </CardHeader>
          <CardContent>
            <!-- File Upload Area -->
            <div
              class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors mb-4 cursor-pointer"
              :class="{ 'border-blue-400 bg-blue-50': isDragOver }" @dragover.prevent="isDragOver = true"
              @dragleave.prevent="isDragOver = false" @drop.prevent="handleDrop" @click="fileInput?.click()">
              <div class="space-y-3">
                <svg class="w-12 h-12 text-gray-400 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <div>
                  <p class="text-md font-medium text-gray-900">Kéo thả file vào đây</p>
                  <p class="text-sm text-gray-500">hoặc nhấp để chọn file</p>
                </div>
                <input ref="fileInput" type="file" multiple accept="image/*,.pdf,.doc,.docx" class="hidden"
                  @change="handleFileSelect" />
              </div>
            </div>

            <div class="text-xs text-gray-500 mb-4">
              <p>Định dạng hỗ trợ: JPG, PNG, PDF, DOC, DOCX</p>
              <p>Kích thước tối đa: 10MB mỗi file</p>
            </div>

            <!-- Uploaded Files -->
            <div v-if="attachments.length > 0" class="space-y-4 mt-6">
              <h4 class="font-semibold text-gray-900">File đã tải lên ({{ attachments.length }})</h4>

              <div v-for="(file, index) in attachments" :key="index" class="border border-gray-200 rounded-lg p-4">
                <div class="flex items-start justify-between mb-4">
                  <div class="flex flex-col space-y-2 flex-1 min-w-0">
                    <!-- Title and size placed above preview -->
                    <div class="flex items-start justify-between gap-2">
                      <div class="min-w-0 flex-1">
                        <p class="font-medium text-gray-900 truncate" :title="file.title || file.name">
                          {{ file.title || file.name }}
                        </p>
                        <p class="text-xs text-gray-500">
                          {{ formatFileSize(file.size) }}
                        </p>
                      </div>
                      
                      <Button variant="outline" size="sm" @click="removeFile(index)"
                        class="text-red-600 hover:text-red-700 flex-shrink-0">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </Button>
                    </div>

                    <!-- Image Preview or Icon - takes full width -->
                    <div class="w-full">
                      <div v-if="isImageFile(file)"
                        class="w-full h-64 rounded-lg overflow-hidden border border-gray-200">
                        <img :src="file.url" :alt="file.name" class="w-full h-full object-cover" />
                      </div>

                      <div v-else
                        class="w-full h-64 rounded-lg bg-blue-100 flex items-center justify-center">
                        <svg class="w-24 h-24 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Attachment Metadata Form -->
                <div class="border-t border-gray-200 pt-4 mt-4">
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <!-- Attachment Type -->
                    <div>
                      <label class="block text-xs font-medium text-gray-700 mb-1">Loại tài liệu</label>
                      <select v-model="file.attachment_type"
                        class="w-full px-2 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option value="">Chọn loại</option>
                        <option value="x_ray">📷 Chụp X-quang</option>
                        <option value="lab_report">🧪 Phiếu xét nghiệm</option>
                        <option value="ct_scan">🔬 Chụp CT</option>
                        <option value="mri_scan">🧠 Chụp MRI</option>
                        <option value="ultrasound">📡 Siêu âm</option>
                        <option value="ekg_ecg">❤️ Điện tâm đồ</option>
                        <option value="other">📄 Khác</option>
                      </select>
                    </div>

                    <!-- Title -->
                    <div>
                      <label class="block text-xs font-medium text-gray-700 mb-1">Tiêu đề</label>
                      <input v-model="file.title" type="text"
                        class="w-full px-2 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Nhập tiêu đề..." />
                    </div>

                    <!-- Department -->
                    <div>
                      <label class="block text-xs font-medium text-gray-700 mb-1">Khoa</label>
                      <select v-model="file.department"
                        class="w-full px-2 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option value="">Chọn khoa</option>
                        <option value="cardiology">Tim mạch</option>
                        <option value="neurology">Thần kinh</option>
                        <option value="radiology">Chẩn đoán hình ảnh</option>
                        <option value="pathology">Giải phẫu bệnh</option>
                        <option value="emergency">Cấp cứu</option>
                        <option value="internal_medicine">Nội khoa</option>
                      </select>
                    </div>

                    <!-- Date Taken -->
                    <div>
                      <label class="block text-xs font-medium text-gray-700 mb-1">Ngày thực hiện</label>
                      <input v-model="file.date_taken" type="date"
                        class="w-full px-2 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
                    </div>

                    <!-- Description (Full Width) -->
                    <div class="md:col-span-2">
                      <label class="block text-xs font-medium text-gray-700 mb-1">Mô tả</label>
                      <textarea v-model="file.description" rows="2"
                        class="w-full px-2 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Nhập mô tả chi tiết..."></textarea>
                    </div>

                    <!-- Physician Notes (Full Width) -->
                    <div class="md:col-span-2">
                      <label class="block text-xs font-medium text-gray-700 mb-1">Ghi chú bác sĩ</label>
                      <textarea v-model="file.physician_notes" rows="2"
                        class="w-full px-2 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Ghi chú của bác sĩ..."></textarea>
                    </div>

                    <!-- Is Confidential -->
                    <div class="md:col-span-2">
                      <label class="flex items-center space-x-2 cursor-pointer">
                        <input v-model="file.is_confidential" type="checkbox"
                          class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500" />
                        <span class="text-xs font-medium text-gray-700">Tài liệu bảo mật</span>
                        <span class="text-xs text-gray-500">(Chỉ giảng viên xem được)</span>
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Preview Button -->
        <Button variant="outline" class="w-full" @click="showPreview = true">
          <Eye class="h-4 w-4 mr-2" />
          Xem trước bệnh án trước khi nộp
        </Button>
      </div>
    </div>

    <!-- Preview Dialog -->
    <CasePreview v-if="showPreview" :case-data="previewData" @close="showPreview = false" @submit="handleSubmit"
      :show-submit-button="true" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useToast } from '@/composables/useToast'
import { useAuthStore } from '@/stores/auth'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import Textarea from '@/components/ui/Textarea.vue'
import Input from '@/components/ui/Input.vue'
import Badge from '@/components/ui/Badge.vue'
import Tabs from '@/components/ui/Tabs.vue'
import TabsContent from '@/components/ui/TabsContent.vue'
import TabsList from '@/components/ui/TabsList.vue'
import TabsTrigger from '@/components/ui/TabsTrigger.vue'
import CasePreview from '@/components/CasePreview.vue'
import { ArrowLeft, Save, Send, Eye, ChevronDown } from '@/components/icons'
import { casesService } from '@/services/cases'
import { gradesService } from '@/services/grades'

const props = defineProps({
  caseId: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['navigate'])

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
  notes: true
})

const toggleSection = (section: string) => {
  expandedSections.value[section] = !expandedSections.value[section]
}

// Grade data for students
const gradeData = ref<any>(null)

const notes = ref({
  clinical_assessment: '',
  differential_diagnosis: '',
  treatment_plan: '',
  learning_reflections: '',
  questions_for_instructor: '',
  challenges_faced: '',
  resources_used: '',
  final_diagnosis: '',
  plan: '',
  learning: ''
})

const hasUnsavedChanges = ref(false)
const showPreview = ref(false)
const activeTab = ref('assessment')
const { toast } = useToast()
const authStore = useAuthStore()

// Loaded case metadata
const caseOwnerId = ref<number | null>(null)
const caseStatus = ref<string>('draft')

// Permission checks
const isOwner = computed(() => {
  return authStore.user && caseOwnerId.value && authStore.user.id === caseOwnerId.value
})

const isDraft = computed(() => {
  return caseStatus.value === 'draft'
})

const canEdit = computed(() => {
  return isOwner.value && isDraft.value
})

// File upload state
const fileInput = ref<HTMLInputElement>()
const isDragOver = ref(false)
const attachments = ref<any[]>([])

const handleDrop = (event: DragEvent) => {
  isDragOver.value = false
  const files = Array.from(event.dataTransfer?.files || [])
  addFiles(files)
}

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  const files = Array.from(target.files || [])
  addFiles(files)
}

const addFiles = (files: File[]) => {
  const validFiles = files.filter(file => {
    // Check file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      toast.error(`File ${file.name} quá lớn. Kích thước tối đa là 10MB.`)
      return false
    }

    // Check file type
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    if (!allowedTypes.includes(file.type)) {
      toast.error(`File ${file.name} không được hỗ trợ.`)
      return false
    }

    return true
  })

  // Create file objects with URLs for preview and metadata fields
  const fileObjects = validFiles.map(file => ({
    name: file.name,
    size: file.size,
    type: file.type,
    url: URL.createObjectURL(file),
    file: file,
    attachment_type: '',
    title: file.name.split('.')[0] || '',
    department: '',
    description: '',
    date_taken: '',
    physician_notes: '',
    is_confidential: false
  }))

  attachments.value = [...attachments.value, ...fileObjects]
  hasUnsavedChanges.value = true
}

const removeFile = (index: number) => {
  const fileToRemove = attachments.value[index]
  if (fileToRemove.url) {
    URL.revokeObjectURL(fileToRemove.url)
  }
  attachments.value.splice(index, 1)
  hasUnsavedChanges.value = true
}

const isImageFile = (file: any) => {
  return file.type?.startsWith('image/')
}

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// Case data using the same structure as CreateCase.vue
const caseData = ref({
  title: '',
  specialty: '',
  patient_name: '',
  patient_age: '',
  patient_gender: '',
  medical_record_number: '',
  patient_ethnicity: '',
  patient_occupation: '',
  admission_date: '',
  discharge_date: '',
  chief_complaint_brief: '',
  requires_follow_up: false,
  follow_up_date: '',
  priority_level: 'medium',
  complexity_level: 'basic',
  case_summary: '',
  learning_tags: '',
  estimated_study_hours: null,
  keywords: '',
  template: null,
  repository: null,
  // Detailed medical sections
  clinical_history: {
    chief_complaint: '',
    history_present_illness: '',
    symptom_duration_days: null,
    symptom_onset: '',
    symptom_progression: '',
    past_medical_history: '',
    family_history: '',
    social_history: '',
    allergies: '',
    medications: '',
    review_systems: ''
  },
  physical_examination: {
    general_appearance: '',
    consciousness_level: '',
    vital_signs: '',
    vital_signs_bp: '',
    vital_signs_hr: null,
    vital_signs_rr: null,
    vital_signs_temp: null,
    vital_signs_spo2: null,
    weight_kg: null,
    height_cm: null,
    head_neck: '',
    cardiovascular: '',
    respiratory: '',
    abdominal: '',
    neurological: '',
    musculoskeletal: '',
    skin: '',
    other_findings: ''
  },
  investigations: {
    laboratory_results: '',
    hemoglobin_level: null,
    white_cell_count: null,
    platelet_count: null,
    sodium_level: null,
    potassium_level: null,
    glucose_level: null,
    creatinine_level: null,
    imaging_studies: '',
    ecg_findings: '',
    ecg_rhythm: '',
    ecg_rate: null,
    pathology_results: '',
    microbiology_results: '',
    other_investigations: '',
    arterial_blood_gas: '',
    ph_level: null,
    special_tests: '',
    biochemistry: '',
    hematology: '',
    microbiology: ''
  },
  diagnosis_management: {
    primary_diagnosis: '',
    differential_diagnosis: '',
    icd10_codes: '',
    treatment_plan: '',
    procedures_performed: '',
    prognosis: '',
    medications_prescribed: '',
    follow_up_plan: '',
    complications: ''
  },
  learning_outcomes: {
    learning_objectives: '',
    key_concepts: '',
    clinical_pearls: '',
    references: '',
    discussion_points: '',
    assessment_criteria: ''
  }
})

const handleNoteChange = () => {
  hasUnsavedChanges.value = true
}

const handleSave = async () => {
  try {
    console.log('=== SAVING CASE ===')
    console.log('Current notes data:', notes.value)
    console.log('Current case data:', caseData.value)
    
    // Helper function to clean nested objects
    const cleanObject = (obj: any) => {
      if (!obj || typeof obj !== 'object') return obj
      
      const cleaned: any = {}
      for (const [key, value] of Object.entries(obj)) {
        if (value !== '' && value !== null && value !== undefined) {
          cleaned[key] = value
        }
      }
      return Object.keys(cleaned).length > 0 ? cleaned : undefined
    }
    
    // Helper function to format date to YYYY-MM-DD or null
    const formatDate = (dateValue: any) => {
      if (!dateValue || dateValue === '') return null
      // If already in YYYY-MM-DD format, return as-is
      if (typeof dateValue === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(dateValue)) {
        return dateValue
      }
      // Try to parse and format
      try {
        const date = new Date(dateValue)
        if (isNaN(date.getTime())) return null
        return date.toISOString().split('T')[0]
      } catch {
        return null
      }
    }

    // 1. Update main case data with properly formatted nested objects
    const caseUpdateData: any = {
      title: caseData.value.title,
      specialty: caseData.value.specialty,
      patient_name: caseData.value.patient_name,
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
      keywords: caseData.value.keywords,
      case_status: 'draft',
    }
    
    // Build nested objects and only include if they have data
    const clinicalHistory = cleanObject({
      chief_complaint: caseData.value.clinical_history?.chief_complaint,
      history_present_illness: caseData.value.clinical_history?.history_present_illness,
      symptom_duration_days: caseData.value.clinical_history?.symptom_duration_days,
      symptom_onset: caseData.value.clinical_history?.symptom_onset,
      symptom_progression: caseData.value.clinical_history?.symptom_progression,
      past_medical_history: caseData.value.clinical_history?.past_medical_history,
      family_history: caseData.value.clinical_history?.family_history,
      social_history: caseData.value.clinical_history?.social_history,
      allergies: caseData.value.clinical_history?.allergies,
      medications: caseData.value.clinical_history?.medications,
      review_systems: caseData.value.clinical_history?.review_systems
    })
    if (clinicalHistory) caseUpdateData.clinical_history = clinicalHistory
    
    const physicalExam = cleanObject({
      general_appearance: caseData.value.physical_examination?.general_appearance,
      consciousness_level: caseData.value.physical_examination?.consciousness_level,
      vital_signs: caseData.value.physical_examination?.vital_signs,
      vital_signs_bp: caseData.value.physical_examination?.vital_signs_bp,
      vital_signs_hr: caseData.value.physical_examination?.vital_signs_hr,
      vital_signs_rr: caseData.value.physical_examination?.vital_signs_rr,
      vital_signs_temp: caseData.value.physical_examination?.vital_signs_temp,
      vital_signs_spo2: caseData.value.physical_examination?.vital_signs_spo2,
      weight_kg: caseData.value.physical_examination?.weight_kg,
      height_cm: caseData.value.physical_examination?.height_cm,
      head_neck: caseData.value.physical_examination?.head_neck,
      cardiovascular: caseData.value.physical_examination?.cardiovascular,
      respiratory: caseData.value.physical_examination?.respiratory,
      abdominal: caseData.value.physical_examination?.abdominal,
      neurological: caseData.value.physical_examination?.neurological,
      musculoskeletal: caseData.value.physical_examination?.musculoskeletal,
      skin: caseData.value.physical_examination?.skin,
      other_systems: caseData.value.physical_examination?.other_findings
    })
    if (physicalExam) caseUpdateData.physical_examination = physicalExam
    
    const investigations = cleanObject({
      laboratory_results: caseData.value.investigations?.laboratory_results,
      hemoglobin_level: caseData.value.investigations?.hemoglobin_level,
      white_cell_count: caseData.value.investigations?.white_cell_count,
      platelet_count: caseData.value.investigations?.platelet_count,
      sodium_level: caseData.value.investigations?.sodium_level,
      potassium_level: caseData.value.investigations?.potassium_level,
      glucose_level: caseData.value.investigations?.glucose_level,
      creatinine_level: caseData.value.investigations?.creatinine_level,
      imaging_studies: caseData.value.investigations?.imaging_studies,
      ecg_findings: caseData.value.investigations?.ecg_findings,
      ecg_rhythm: caseData.value.investigations?.ecg_rhythm,
      ecg_rate: caseData.value.investigations?.ecg_rate,
      pathology_results: caseData.value.investigations?.pathology_results,
      microbiology_results: caseData.value.investigations?.microbiology_results,
      other_investigations: caseData.value.investigations?.other_investigations,
      arterial_blood_gas: caseData.value.investigations?.arterial_blood_gas,
      ph_level: caseData.value.investigations?.ph_level,
      special_tests: caseData.value.investigations?.special_tests,
      biochemistry: caseData.value.investigations?.biochemistry,
      hematology: caseData.value.investigations?.hematology,
      microbiology: caseData.value.investigations?.microbiology
    })
    if (investigations) caseUpdateData.detailed_investigations = investigations
    
    const diagnosisManagement = cleanObject({
      primary_diagnosis: caseData.value.diagnosis_management?.primary_diagnosis,
      differential_diagnosis: caseData.value.diagnosis_management?.differential_diagnosis,
      icd10_codes: caseData.value.diagnosis_management?.icd10_codes,
      treatment_plan: caseData.value.diagnosis_management?.treatment_plan,
      procedures_performed: caseData.value.diagnosis_management?.procedures_performed,
      prognosis: caseData.value.diagnosis_management?.prognosis,
      medications_prescribed: caseData.value.diagnosis_management?.medications_prescribed,
      follow_up_plan: caseData.value.diagnosis_management?.follow_up_plan,
      complications: caseData.value.diagnosis_management?.complications
    })
    if (diagnosisManagement) caseUpdateData.diagnosis_management = diagnosisManagement
    
    const learningOutcomes = cleanObject({
      learning_objectives: caseData.value.learning_outcomes?.learning_objectives,
      key_concepts: caseData.value.learning_outcomes?.key_concepts,
      clinical_pearls: caseData.value.learning_outcomes?.clinical_pearls,
      references: caseData.value.learning_outcomes?.references,
      discussion_points: caseData.value.learning_outcomes?.discussion_points,
      assessment_criteria: caseData.value.learning_outcomes?.assessment_criteria
    })
    if (learningOutcomes) caseUpdateData.learning_outcomes = learningOutcomes
    
    // Only include repository and template if they exist and are valid IDs
    if (caseData.value.repository) {
      caseUpdateData.repository = caseData.value.repository
    }
    if (caseData.value.template) {
      caseUpdateData.template = caseData.value.template
    }

    console.log('Sending case update:', caseUpdateData)
    await casesService.updateCase(props.caseId, caseUpdateData)

    // 2. Save/Update student notes (case and student are set by backend)
    const notesData = {
      clinical_assessment: notes.value.clinical_assessment,
      differential_diagnosis: notes.value.differential_diagnosis,
      treatment_plan: notes.value.treatment_plan,
      learning_reflections: notes.value.learning_reflections,
      questions_for_instructor: notes.value.questions_for_instructor || '',
      challenges_faced: notes.value.challenges_faced || '',
      resources_used: notes.value.resources_used || ''
    }
    
    console.log('Saving student notes:', notesData)

    // Check if notes already exist
    const existingNotes = await casesService.getStudentNotes(props.caseId)
    console.log('Existing notes found:', existingNotes)
    if (existingNotes && existingNotes.id) {
      console.log('Updating existing notes with ID:', existingNotes.id)
      const updateResult = await casesService.updateStudentNotes(existingNotes.id, notesData)
      console.log('Update result:', updateResult)
    } else {
      console.log('Creating new notes for case:', props.caseId)
      const createResult = await casesService.saveStudentNotes(props.caseId, notesData)
      console.log('Create result:', createResult)
    }

    // 3. Upload new attachments
    for (const attachment of attachments.value) {
      // Only upload if this is a new file (has the 'file' property)
      if (attachment.file && !attachment.id) {
        const formData = new FormData()
        formData.append('file', attachment.file)
        formData.append('title', attachment.title || attachment.name)
        formData.append('attachment_type', attachment.attachment_type || 'other')
        if (attachment.description) formData.append('description', attachment.description)
        if (attachment.department) formData.append('department', attachment.department)
        if (attachment.date_taken) formData.append('date_taken', attachment.date_taken)
        if (attachment.physician_notes) formData.append('physician_notes', attachment.physician_notes)
        formData.append('is_confidential', attachment.is_confidential ? 'true' : 'false')

        await casesService.uploadAttachment(props.caseId, formData)
      }
    }

    toast.success('Đã lưu nháp thành công!')
    hasUnsavedChanges.value = false
  } catch (error: any) {
    console.error('Error saving case:', error)
    console.error('Error response:', error.response?.data)
    console.error('Error status:', error.response?.status)
    console.error('Full error object:', JSON.stringify(error.response?.data, null, 2))
    
    // Show specific error messages
    if (error.response?.data) {
      const errors = error.response.data
      if (typeof errors === 'object') {
        const errorMessages = Object.entries(errors).map(([field, msgs]) => {
          const messages = Array.isArray(msgs) ? msgs : [msgs]
          return `${field}: ${messages.join(', ')}`
        }).join('\n')
        toast.error(`Lỗi: ${errorMessages}`)
      } else {
        toast.error(error.response?.data?.message || error.response?.data || 'Không thể lưu nháp. Vui lòng thử lại.')
      }
    } else {
      toast.error('Không thể lưu nháp. Vui lòng thử lại.')
    }
  }
}

const handleSubmit = async () => {
  try {
    console.log('Starting submit...')
    
    // First save all data
    await handleSave()

    // Then submit the case (this will change status to 'submitted')
    console.log('Submitting case...')
    await casesService.submitCase(props.caseId)

    toast.success('Ca bệnh đã được nộp để xem xét!')
    setTimeout(() => emit('navigate', 'dashboard'), 1500)
  } catch (error: any) {
    console.error('Error submitting case:', error)
    console.error('Error response:', error.response?.data)
    
    // Show specific error messages
    if (error.response?.data) {
      const errorData = error.response.data
      if (errorData.error) {
        toast.error(errorData.error)
      } else if (typeof errorData === 'object') {
        const errorMessages = Object.entries(errorData).map(([field, msgs]) => {
          const messages = Array.isArray(msgs) ? msgs : [msgs]
          return `${field}: ${messages.join(', ')}`
        }).join('\n')
        toast.error(`Lỗi: ${errorMessages}`)
      } else {
        toast.error(errorData || 'Không thể nộp ca bệnh. Vui lòng thử lại.')
      }
    } else {
      toast.error('Không thể nộp ca bệnh. Vui lòng thử lại.')
    }
  }
}

const previewData = computed(() => ({
  // Basic Information
  title: caseData.value?.title || 'Chưa có tiêu đề',
  specialty: caseData.value?.specialty || 'Chưa chọn chuyên khoa',

  // Patient Information
  patientName: caseData.value?.patient_name || 'Chưa nhập',
  patientAge: caseData.value?.patient_age || 'Chưa nhập',
  patientGender: caseData.value?.patient_gender === 'male' ? 'Nam' : caseData.value?.patient_gender === 'female' ? 'Nữ' : caseData.value?.patient_gender || 'Chưa nhập',
  medicalRecordNumber: caseData.value?.medical_record_number || 'Chưa nhập',

  // Clinical History
  chief_complaint: caseData.value?.clinical_history?.chief_complaint || 'Chưa nhập',
  historyOfPresentIllness: caseData.value?.clinical_history?.history_present_illness || 'Chưa nhập',
  pastMedicalHistory: caseData.value?.clinical_history?.past_medical_history || 'Chưa nhập',
  medications: caseData.value?.clinical_history?.medications || 'Chưa nhập',

  // Physical Examination
  generalAppearance: caseData.value?.physical_examination?.general_appearance || 'Chưa nhập',
  vitalSigns: caseData.value?.physical_examination?.vital_signs || 'Chưa nhập',
  cardiovascular: caseData.value?.physical_examination?.cardiovascular || 'Chưa nhập',
  respiratory: caseData.value?.physical_examination?.respiratory || 'Chưa nhập',

  // Investigations
  labsAndImaging: caseData.value?.investigations?.laboratory_results || 'Chưa nhập',
  imagingStudies: caseData.value?.investigations?.imaging_studies || 'Chưa nhập',
  ecgFindings: caseData.value?.investigations?.ecg_findings || 'Chưa nhập',

  // Diagnosis and Management (from form)
  primaryDiagnosis: caseData.value?.diagnosis_management?.primary_diagnosis || 'Chưa nhập',
  treatmentPlanForm: caseData.value?.diagnosis_management?.treatment_plan || 'Chưa nhập',

  // Student Notes
  differentialDiagnosis: notes.value?.differential_diagnosis || 'Chưa nhập',
  finalDiagnosis: notes.value?.clinical_assessment || 'Chưa nhập',
  treatmentPlan: notes.value?.treatment_plan || 'Chưa nhập',
  notes: notes.value?.learning_reflections || 'Chưa nhập',

  // Attachments
  attachments: attachments.value || []
}))

onMounted(async () => {
  try {
    // Load case data from API
    const caseDetails = await casesService.getCase(props.caseId)
    
    // Store owner and status for permission checks
    // Backend uses 'student' field instead of 'created_by'
    if (caseDetails.student) {
      caseOwnerId.value = typeof caseDetails.student === 'object' 
        ? caseDetails.student.id 
        : caseDetails.student
    } else if (caseDetails.created_by) {
      caseOwnerId.value = typeof caseDetails.created_by === 'object' 
        ? caseDetails.created_by.id 
        : caseDetails.created_by
    }
    
    caseStatus.value = caseDetails.case_status || caseDetails.status || 'draft'
    
    // Merge all basic fields
    Object.assign(caseData.value, {
      title: caseDetails.title || '',
      specialty: caseDetails.specialty || '',
      patient_name: caseDetails.patient_name || '',
      patient_age: caseDetails.patient_age || '',
      patient_gender: caseDetails.patient_gender || '',
      medical_record_number: caseDetails.medical_record_number || '',
      patient_ethnicity: caseDetails.patient_ethnicity || '',
      patient_occupation: caseDetails.patient_occupation || '',
      admission_date: caseDetails.admission_date || '',
      discharge_date: caseDetails.discharge_date || '',
      chief_complaint_brief: caseDetails.chief_complaint_brief || '',
      requires_follow_up: caseDetails.requires_follow_up || false,
      follow_up_date: caseDetails.follow_up_date || '',
      priority_level: caseDetails.priority_level || 'medium',
      complexity_level: caseDetails.complexity_level || 'basic',
      case_summary: caseDetails.case_summary || '',
      learning_tags: caseDetails.learning_tags || '',
      estimated_study_hours: caseDetails.estimated_study_hours || null,
      keywords: caseDetails.keywords || '',
      template: caseDetails.template || null,
      repository: caseDetails.repository || null
    })
    
    // Merge nested objects to preserve reactivity
    if (caseDetails.clinical_history) {
      Object.assign(caseData.value.clinical_history, {
        chief_complaint: caseDetails.clinical_history.chief_complaint || '',
        history_present_illness: caseDetails.clinical_history.history_present_illness || '',
        symptom_duration_days: caseDetails.clinical_history.symptom_duration_days || null,
        symptom_onset: caseDetails.clinical_history.symptom_onset || '',
        symptom_progression: caseDetails.clinical_history.symptom_progression || '',
        past_medical_history: caseDetails.clinical_history.past_medical_history || '',
        family_history: caseDetails.clinical_history.family_history || '',
        social_history: caseDetails.clinical_history.social_history || '',
        allergies: caseDetails.clinical_history.allergies || '',
        medications: caseDetails.clinical_history.medications || '',
        review_systems: caseDetails.clinical_history.review_systems || ''
      })
    }
    
    if (caseDetails.physical_examination) {
      Object.assign(caseData.value.physical_examination, {
        general_appearance: caseDetails.physical_examination.general_appearance || '',
        consciousness_level: caseDetails.physical_examination.consciousness_level || '',
        vital_signs: caseDetails.physical_examination.vital_signs || '',
        vital_signs_bp: caseDetails.physical_examination.vital_signs_bp || '',
        vital_signs_hr: caseDetails.physical_examination.vital_signs_hr || null,
        vital_signs_rr: caseDetails.physical_examination.vital_signs_rr || null,
        vital_signs_temp: caseDetails.physical_examination.vital_signs_temp || null,
        vital_signs_spo2: caseDetails.physical_examination.vital_signs_spo2 || null,
        weight_kg: caseDetails.physical_examination.weight_kg || null,
        height_cm: caseDetails.physical_examination.height_cm || null,
        head_neck: caseDetails.physical_examination.head_neck || '',
        cardiovascular: caseDetails.physical_examination.cardiovascular || '',
        respiratory: caseDetails.physical_examination.respiratory || '',
        abdominal: caseDetails.physical_examination.abdominal || '',
        neurological: caseDetails.physical_examination.neurological || '',
        musculoskeletal: caseDetails.physical_examination.musculoskeletal || '',
        skin: caseDetails.physical_examination.skin || '',
        other_findings: caseDetails.physical_examination.other_systems || ''
      })
    }
    
    if (caseDetails.detailed_investigations) {
      Object.assign(caseData.value.investigations, {
        laboratory_results: caseDetails.detailed_investigations.laboratory_results || '',
        hemoglobin_level: caseDetails.detailed_investigations.hemoglobin_level || null,
        white_cell_count: caseDetails.detailed_investigations.white_cell_count || null,
        platelet_count: caseDetails.detailed_investigations.platelet_count || null,
        sodium_level: caseDetails.detailed_investigations.sodium_level || null,
        potassium_level: caseDetails.detailed_investigations.potassium_level || null,
        glucose_level: caseDetails.detailed_investigations.glucose_level || null,
        creatinine_level: caseDetails.detailed_investigations.creatinine_level || null,
        imaging_studies: caseDetails.detailed_investigations.imaging_studies || '',
        ecg_findings: caseDetails.detailed_investigations.ecg_findings || '',
        ecg_rhythm: caseDetails.detailed_investigations.ecg_rhythm || '',
        ecg_rate: caseDetails.detailed_investigations.ecg_rate || null,
        pathology_results: caseDetails.detailed_investigations.pathology_results || '',
        microbiology_results: caseDetails.detailed_investigations.microbiology_results || '',
        other_investigations: caseDetails.detailed_investigations.other_investigations || '',
        arterial_blood_gas: caseDetails.detailed_investigations.arterial_blood_gas || '',
        ph_level: caseDetails.detailed_investigations.ph_level || null,
        special_tests: caseDetails.detailed_investigations.special_tests || '',
        biochemistry: caseDetails.detailed_investigations.biochemistry || '',
        hematology: caseDetails.detailed_investigations.hematology || '',
        microbiology: caseDetails.detailed_investigations.microbiology || ''
      })
    }
    
    if (caseDetails.diagnosis_management) {
      Object.assign(caseData.value.diagnosis_management, {
        primary_diagnosis: caseDetails.diagnosis_management.primary_diagnosis || '',
        differential_diagnosis: caseDetails.diagnosis_management.differential_diagnosis || '',
        icd10_codes: caseDetails.diagnosis_management.icd10_codes || '',
        treatment_plan: caseDetails.diagnosis_management.treatment_plan || '',
        procedures_performed: caseDetails.diagnosis_management.procedures_performed || '',
        prognosis: caseDetails.diagnosis_management.prognosis || '',
        medications_prescribed: caseDetails.diagnosis_management.medications_prescribed || '',
        follow_up_plan: caseDetails.diagnosis_management.follow_up_plan || '',
        complications: caseDetails.diagnosis_management.complications || ''
      })
    }
    
    if (caseDetails.learning_outcomes) {
      Object.assign(caseData.value.learning_outcomes, {
        learning_objectives: caseDetails.learning_outcomes.learning_objectives || '',
        key_concepts: caseDetails.learning_outcomes.key_concepts || '',
        clinical_pearls: caseDetails.learning_outcomes.clinical_pearls || '',
        references: caseDetails.learning_outcomes.references || '',
        discussion_points: caseDetails.learning_outcomes.discussion_points || '',
        assessment_criteria: caseDetails.learning_outcomes.assessment_criteria || ''
      })
    }

    // Load existing attachments
    if (caseDetails.medical_attachments && caseDetails.medical_attachments.length > 0) {
      attachments.value = caseDetails.medical_attachments.map((att: any) => ({
        ...att,
        url: att.file,
        type: att.file_type,
        size: att.file_size || 0
      }))
    }

    // Load existing student notes if any
    console.log('Attempting to load student notes for case:', props.caseId)
    try {
      const existingNotes = await casesService.getStudentNotes(props.caseId)
      console.log('Loaded student notes:', existingNotes)
      if (existingNotes) {
        Object.assign(notes.value, {
          clinical_assessment: existingNotes.clinical_assessment || '',
          differential_diagnosis: existingNotes.differential_diagnosis || '',
          treatment_plan: existingNotes.treatment_plan || '',
          learning_reflections: existingNotes.learning_reflections || '',
          questions_for_instructor: existingNotes.questions_for_instructor || '',
          challenges_faced: existingNotes.challenges_faced || '',
          resources_used: existingNotes.resources_used || ''
        })
        console.log('Notes after assignment:', notes.value)
      }
    } catch (notesError) {
      console.error('Error loading student notes:', notesError)
    }

    // Load grade if available
    if (caseDetails.has_grade) {
      try {
        const grade = await gradesService.getGrade(props.caseId)
        console.log('Loaded grade for student:', grade)
        if (grade && grade.is_final) {
          gradeData.value = grade
        }
      } catch (gradeError) {
        console.error('Error loading grade:', gradeError)
      }
    }
    
    console.log('Final caseData:', caseData.value)
  } catch (error) {
    console.error('Error loading case data:', error)
    toast.error('Không thể tải dữ liệu ca bệnh')
  }
})
</script>
