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
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Case Information (Read-only for instructors) -->
      <div class="space-y-6">
        <!-- Basic Information -->
        <Card class="bg-white">
          <CardHeader>
            <div class="flex items-center gap-2">
              <InfoIcon stroke="#3b82f6" />
              <CardTitle>Thông tin cơ bản</CardTitle>
            </div>
          </CardHeader>
          <CardContent class="space-y-4">
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
          <CardHeader>
            <div class="flex items-center gap-2">
              <User class="w-5 h-5 text-blue-500" />
              <CardTitle>Thông tin bệnh nhân</CardTitle>
            </div>
          </CardHeader>
          <CardContent class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm text-gray-500">Tên bệnh nhân</label>
                <p class="text-gray-800">
                  {{ caseData.patient_name || "N/A" }}
                </p>
              </div>
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
          <CardHeader>
            <div class="flex items-center gap-2">
              <DocumentIcon class="text-blue-500 w-5 h-5" stroke="#3b82f6" />
              <CardTitle>Tiền sử lâm sàng</CardTitle>
            </div>
          </CardHeader>
          <CardContent class="space-y-4">
            <div v-if="caseData.clinical_history?.chief_complaint">
              <label class="text-sm font-medium text-gray-500"
                >Lý do khám chính</label
              >
              <p class="text-gray-800 mt-1">
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
              <p class="text-gray-800 mt-1">
                {{ caseData.clinical_history?.past_medical_history || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.clinical_history?.medications">
              <label class="text-sm font-medium text-gray-500"
                >Thuốc đang sử dụng</label
              >
              <p class="text-gray-800 mt-1">
                {{ caseData.clinical_history?.medications || "N/A" }}
              </p>
            </div>
          </CardContent>
        </Card>

        <!-- Physical Examination -->
        <Card v-if="hasData('physical_examination')" class="bg-white">
          <CardHeader>
            <div class="flex items-center gap-2">
              <FlaskConical class="text-blue-500 w-5 h-5" stroke="#3b82f6" />
              <CardTitle>Khám lâm sàng</CardTitle>
            </div>
          </CardHeader>
          <CardContent class="space-y-4">
            <div v-if="caseData.physical_examination?.general_appearance">
              <label class="text-sm font-medium text-gray-500"
                >Tình trạng chung</label
              >
              <p class="text-gray-800 mt-1">
                {{ caseData.physical_examination.general_appearance || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.physical_examination?.vital_signs">
              <label class="text-sm font-medium text-gray-500">Sinh hiệu</label>
              <p class="text-gray-800 mt-1">
                {{ caseData.physical_examination.vital_signs || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.physical_examination?.cardiovascular">
              <label class="text-sm font-medium text-gray-500">Tim mạch</label>
              <p class="text-gray-800 mt-1">
                {{ caseData.physical_examination.cardiovascular || "N/A" }}
              </p>
            </div>
            <div v-if="caseData.physical_examination?.respiratory">
              <label class="text-sm font-medium text-gray-500">Hô hấp</label>
              <p class="text-gray-800 mt-1">
                {{ caseData.physical_examination.respiratory || "N/A" }}
              </p>
            </div>
          </CardContent>
        </Card>

        <!-- Investigations -->
        <Card v-if="hasData('investigations')" class="bg-white">
          <CardHeader>
            <div class="flex items-center gap-2">
              <FlaskConical class="text-blue-500 w-5 h-5" stroke="#3b82f6" />
              <CardTitle>Cận lâm sàng</CardTitle>
            </div>
          </CardHeader>
          <CardContent class="space-y-4">
            <div v-if="caseData.investigations?.laboratory_results">
              <label class="text-sm font-medium text-gray-500"
                >Xét nghiệm</label
              >
              <p class="text-gray-800 mt-1 whitespace-pre-wrap">
                {{ caseData.investigations.laboratory_results || "N/A" }}
              </p>
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
              <p class="text-gray-800 mt-1">
                {{ caseData.investigations.ecg_findings || "N/A" }}
              </p>
            </div>
          </CardContent>
        </Card>

        <!-- Diagnosis and Management -->
        <Card v-if="hasData('diagnosis_management')" class="bg-white">
          <CardHeader>
            <div class="flex items-center gap-2">
              <Stethoscope class="text-blue-500 w-5 h-5" stroke="#3b82f6" />
              <CardTitle>Chuẩn đoán và điều trị</CardTitle>
            </div>
          </CardHeader>
          <CardContent class="space-y-4">
            <div v-if="caseData.diagnosis_management?.primary_diagnosis">
              <label class="text-sm font-medium text-gray-500"
                >Chẩn đoán chính</label
              >
              <p class="text-gray-800 mt-1">
                {{ caseData.diagnosis_management.primary_diagnosis || "N/A" }}
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
          </CardContent>
        </Card>

        <!-- Student Notes -->
        <Card class="bg-white">
          <CardHeader>
            <div class="flex items-center gap-2">
              <FileText class="text-blue-500 w-5 h-5" stroke="#3b82f6" />
              <CardTitle>Ghi chú của sinh viên</CardTitle>
            </div>
            <CardDescription class="text-gray-500">
              Xem lại ghi chú lâm sàng của sinh viên
            </CardDescription>
          </CardHeader>
          <CardContent class="space-y-4">
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
            <!-- Score Input -->
            <div class="space-y-1">
              <label class="text-sm font-medium text-gray-800">
                Điểm số (0-100) <span class="text-red-500">*</span>
              </label>
              <div class="grid grid-cols-5">
                <div class="col-span-2">
                  <Input
                    v-model.number="gradingForm.score"
                    type="number"
                    min="0"
                    max="100"
                    placeholder="Nhập điểm số..."
                    class="text-2xl font-bold text-center"
                  />
                </div>
              </div>
              <p class="text-sm text-gray-500 text-left">
                Xếp loại:
                <span class="font-semibold">{{
                  getLetterGrade(gradingForm.score)
                }}</span>
              </p>
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
              >
                <Save class="h-4 w-4 mr-2" />
                {{ saving ? "Đang lưu..." : "Lưu đánh giá" }}
              </Button>
              <Button
                @click="submitGrade"
                :disabled="!canSaveGrade || submitting"
                class="w-full bg-green-600 hover:bg-green-700"
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

import { ArrowLeft, Save, CheckCircle } from "@/components/icons";
import { casesService } from "@/services/cases";
import { gradesService } from "@/services/grades";
import feedService from "@/services/feed";
import DocumentIcon from "./icons/DocumentIcon.vue";
import FlaskConical from "./icons/FlaskConical.vue";
import Stethoscope from "./icons/Stethoscope.vue";
import Activity from "./icons/Activity.vue";
import FileText from "./icons/FileText.vue";

const activeNotesTab = ref<"clinical" | "learning">("clinical");

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

const canSaveGrade = computed(() => {
  return (
    gradingForm.value.score >= 0 &&
    gradingForm.value.score <= 100 &&
    gradingForm.value.evaluation_notes.trim() !== ""
  );
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
      imaging_studies: apiCase.detailed_investigations?.imaging_studies || "",
      ecg_findings: apiCase.detailed_investigations?.ecg_findings || "",
      pathology_results:
        apiCase.detailed_investigations?.pathology_results || "",
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
  if (!canSaveGrade.value) {
    toast.error("Vui lòng nhập điểm số và nhận xét");
    return;
  }
  saving.value = true;
  try {
    const payload: GradeSubmission = {
      grade_scale: "percentage",
      score: gradingForm.value.score,
      letter_grade: getLetterGrade(gradingForm.value.score),
      evaluation_notes: gradingForm.value.evaluation_notes,
      strengths: gradingForm.value.strengths,
      weaknesses: gradingForm.value.weaknesses,
      recommendations: gradingForm.value.recommendations, // can be a textarea later
      grading_criteria: gradingForm.value.criteria,
      is_final: false,
      case: Number(props.caseId), // integer
    };

    console.log("SAVE payload →", payload); // <-- debug
    await gradesService.saveGrade(payload);
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
  if (!canSaveGrade.value) {
    toast.error("Vui lòng nhập điểm số và nhận xét");
    return;
  }
  submitting.value = true;
  try {
    const payload: GradeSubmission = {
      grade_scale: "percentage",
      score: gradingForm.value.score,
      letter_grade: getLetterGrade(gradingForm.value.score),
      evaluation_notes: gradingForm.value.evaluation_notes,
      strengths: gradingForm.value.strengths,
      weaknesses: gradingForm.value.weaknesses,
      recommendations: gradingForm.value.recommendations,
      grading_criteria: gradingForm.value.criteria,
      is_final: true,
      case: Number(props.caseId),
    };

    console.log("SUBMIT payload →", payload); // <-- debug
    console.log(typeof payload.letter_grade);
    await gradesService.submitGrade(payload);
    toast.success("Chấm điểm hoàn tất!");
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

    // Load existing grade
    if (apiCase.has_grade) {
      try {
        const grade = await gradesService.getGrade(props.caseId);
        if (grade) {
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
        }
      } catch (err) {
        console.log("No grade loaded");
      }
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
  imaging_studies?: string;
  ecg_findings?: string;
  pathology_results?: string;
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
