// src/main.ts
import { createApp } from "vue";
import { createPinia } from "pinia";
import {
  createRouter,
  createWebHistory,
  type RouteRecordRaw,
} from "vue-router";
import { createI18n } from "vue-i18n";
import App from "./App.vue";
import '../styles/globals.css';

// Extend RouteMeta to include custom requiresRoles
declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean;
    requiresRoles?: string[];
  }
}


// Import views
import Home from "./views/Home.vue";
import Login from "./views/Login.vue";
import Cases from "./views/Cases.vue";
import CreateCase from "./views/CreateCase.vue";
import CaseNotes from "./views/CaseNotes.vue";
import NotFound from "./views/NotFound.vue";
import Landing from "./views/Landing.vue";
import PatientProfile from "./views/PatientProfile.vue";
import PatientRecords from "./views/PatientRecords.vue";
import ViewStudentList from "./views/ViewStudentList.vue";
import Users from "./views/Users.vue";
import SharedCases from "./views/SharedCases.vue";
import PublicFeed from "./views/PublicFeed.vue";


import { useToast } from '@/composables/useToast'

const { toast } = useToast();

// ---- Router ----

const routes: RouteRecordRaw[] = [
  { path: "/", component: Landing },
  { path: "/login", component: Login },
  { path: "/home", component: Home, meta: { requiresAuth: true } },
  
  // Student & Instructor routes (admin restricted)
  { path: "/cases", component: Cases, meta: { requiresAuth: true, requiresRoles: ["student", "instructor"] } },
  {
    path: "/students",
    component: ViewStudentList,
    meta: { requiresAuth: true, requiresRoles: ["instructor", "admin"] },
  },
  {
    path: "/cases/create",
    component: CreateCase,
    meta: { requiresAuth: true, requiresRoles: ["student", "instructor"] },
  },
  {
    path: "/cases/:id",
    component: CaseNotes,
    props: true,
    meta: { requiresAuth: true, requiresRoles: ["student", "instructor"] },
  },
  {
    path: "/patients",
    component: PatientRecords,
    meta: { requiresAuth: true, requiresRoles: ["student", "instructor"] },
  },
  {
    path: "/patients/:id",
    component: PatientProfile,
    props: true,
    meta: { requiresAuth: true, requiresRoles: ["student", "instructor"] },
  },
  {
    path: "/shared-cases",
    component: SharedCases,
    meta: { requiresAuth: true, requiresRoles: ["student", "instructor"] },
  },
  {
    path: "/public-feed",
    component: PublicFeed,
    meta: { requiresAuth: true, requiresRoles: ["student", "instructor"] },
  },
  {
    path: "/public-feed/:id",
    component: CaseNotes,
    props: true,
    meta: { requiresAuth: true, requiresRoles: ["student", "instructor"] },
  },
  
  // Admin routes
  {
    path: "/users",
    component: Users,
    meta: { requiresAuth: true, requiresRoles: ["admin"] },
  },

  // Shared routes (all authenticated users)
  { path: "/repositories", component: NotFound, meta: { requiresAuth: true } },
  { path: "/templates", component: NotFound, meta: { requiresAuth: true } },
  { path: "/settings", component: NotFound, meta: { requiresAuth: true } },

  // Fallback
  { path: "/:pathMatch(.*)*", name: "NotFound", component: NotFound },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// ---- Pinia ----

const pinia = createPinia();

// ---- i18n ----

const messages = {
  en: {
    createCase: {
      // Template Selection
      selectTemplate: "Select Case Template",
      templateDescription: "Choose a template to start building your clinical case",
      difficulty: "Difficulty",
      estimatedTime: "Est. Time",
      templatePreview: "Template Preview",
      templateDetails: "Template Details",
      category: "Category",
      specialty: "Specialty",
      department: "Department",
      createdBy: "Created By",
      sections: "Sections",
      requiredFields: "Required Fields",
      learningObjectives: "Learning Objectives",

      // Basic Information
      basicInformation: "Basic Information",
      basicInfoDescription: "Enter patient demographics and chief complaint",
      patientDemographics: "Patient Demographics",
      firstName: "First Name",
      enterFirstName: "Enter first name",
      lastName: "Last Name",
      enterLastName: "Enter last name",
      age: "Age",
      enterAge: "Enter age",
      gender: "Gender",
      selectGender: "Select gender",
      male: "Male",
      female: "Female",
      other: "Other",
      medicalRecordNumber: "Medical Record Number (MRN)",
      enterMRN: "Enter MRN",
      dateOfBirth: "Date of Birth",
      clinicalPresentation: "Clinical Presentation",
      chief_complaint: "Chief Complaint",
      describe_chief_complaint: "Describe the patient's chief complaint",
      historyOfPresentIllness: "History of Present Illness",
      describeHPI: "Describe the history of present illness",
      pastMedicalHistory: "Past Medical History",
      describePMH: "Describe relevant past medical history",
      firstNameRequired: "First name is required",
      lastNameRequired: "Last name is required",
      validAgeRequired: "Valid age is required (0-150)",
      genderRequired: "Gender is required",
      chief_complaintRequired: "Chief complaint is required",

      // Vital Signs
      vitalSigns: "Vital Signs",
      vitalSignsDescription: "Record patient vital signs and measurements",
      recordVitalSigns: "Record Vital Signs",
      temperature: "Temperature",
      heartRate: "Heart Rate",
      bloodPressure: "Blood Pressure",
      respiratoryRate: "Respiratory Rate",
      oxygenSaturation: "Oxygen Saturation",
      weight: "Weight",
      height: "Height",
      bmi: "BMI",
      painScale: "Pain Scale",
      additionalNotes: "Additional Notes",
      vitalSignsNotesPlaceholder: "Enter any additional notes about vital signs",
      underweight: "Underweight",
      normalWeight: "Normal Weight",
      overweight: "Overweight",
      obese: "Obese",

      // Physical Examination
      physicalExamination: "Physical Examination",
      physicalExamDescription: "Document physical examination findings",
      generalAppearance: "General Appearance",
      appearance: "Appearance",
      generalAppearancePlaceholder: "Describe general appearance (e.g., well-nourished, in no acute distress)",
      mentalStatus: "Mental Status",
      alert: "Alert",
      confused: "Confused",
      lethargic: "Lethargic",
      unresponsive: "Unresponsive",
      vitalSignsSummary: "Vital Signs Summary",
      systemsReview: "Systems Review",
      heent: "HEENT",
      heentPlaceholder: "Head, Eyes, Ears, Nose, Throat findings",
      cardiovascular: "Cardiovascular",
      cardiovascularPlaceholder: "Heart sounds, rhythm, murmurs",
      respiratory: "Respiratory",
      respiratoryPlaceholder: "Lung sounds, breathing pattern",
      gastrointestinal: "Gastrointestinal",
      gastrointestinalPlaceholder: "Abdomen examination findings",
      genitourinary: "Genitourinary",
      genitourinaryPlaceholder: "Genitourinary examination findings",
      musculoskeletal: "Musculoskeletal",
      musculoskeletalPlaceholder: "Muscle strength, range of motion",
      neurological: "Neurological",
      neurologicalPlaceholder: "Cranial nerves, motor, sensory, reflexes",
      skin: "Skin",
      skinPlaceholder: "Skin examination findings",
      psychiatric: "Psychiatric",
      psychiatricPlaceholder: "Mental status, mood, affect",
      physicalExamNotes: "Physical Examination Notes",
      examNotesPlaceholder: "Additional examination notes and findings",

      // Diagnostic Workup
      diagnosticWorkup: "Diagnostic Workup",
      diagnosticWorkupDescription: "Select and record diagnostic test results",
      laboratoryTests: "Laboratory Tests",
      result: "Result",
      otherLabTests: "Other Lab Tests",
      otherLabTestsPlaceholder: "List any other laboratory tests performed",
      imagingStudies: "Imaging Studies",
      findings: "Findings",
      otherImaging: "Other Imaging",
      otherImagingPlaceholder: "List any other imaging studies performed",
      otherDiagnosticTests: "Other Diagnostic Tests",
      results: "Results",
      additionalTests: "Additional Tests",
      additionalTestsPlaceholder: "List any additional diagnostic tests",
      completeBloodCount: "Complete Blood Count (CBC)",
      cbcDescription: "WBC, RBC, Hemoglobin, Hematocrit, Platelets",
      comprehensiveMetabolicPanel: "Comprehensive Metabolic Panel (CMP)",
      cmpDescription: "Glucose, Electrolytes, Kidney & Liver Function",
      lipidPanel: "Lipid Panel",
      lipidDescription: "Cholesterol, HDL, LDL, Triglycerides",
      thyroidFunction: "Thyroid Function",
      thyroidDescription: "TSH, T3, T4",
      urinalysis: "Urinalysis",
      urinalysisDescription: "Urine analysis for infection, protein, blood",
      cultures: "Cultures",
      culturesDescription: "Blood, Urine, or other cultures",
      chestXray: "Chest X-Ray",
      chestXrayDescription: "Radiographic imaging of chest",
      ctChest: "CT Chest",
      ctChestDescription: "Computed tomography of chest",
      ekg: "EKG/ECG",
      ekgDescription: "Electrocardiogram",
      echocardiogram: "Echocardiogram",
      echocardiogramDescription: "Ultrasound of heart",
      ultrasound: "Ultrasound",
      ultrasoundDescription: "Abdominal or other ultrasound",
      endoscopy: "Endoscopy",
      endoscopyDescription: "Upper GI endoscopy",
      colonoscopy: "Colonoscopy",
      colonoscopyDescription: "Lower GI endoscopy",
      biopsy: "Biopsy",
      biopsyDescription: "Tissue sample analysis",
      pulmonaryFunction: "Pulmonary Function Test",
      pulmonaryFunctionDescription: "Lung function assessment",

      // Assessment & Plan
      assessmentAndPlan: "Assessment & Plan",
      assessmentPlanDescription: "Document diagnosis, treatment plan, and learning objectives",
      assessment: "Assessment",
      primaryDiagnosis: "Primary Diagnosis",
      primaryDiagnosisPlaceholder: "Enter the primary diagnosis",
      differentialDiagnosis: "Differential Diagnosis",
      differentialDiagnosisPlaceholder: "List differential diagnoses",
      clinicalReasoning: "Clinical Reasoning",
      clinicalReasoningPlaceholder: "Explain the clinical reasoning and thought process",
      treatmentPlan: "Treatment Plan",
      medications: "Medications",
      medicationName: "Medication Name",
      medicationNamePlaceholder: "e.g., Lisinopril",
      dosage: "Dosage",
      route: "Route",
      selectRoute: "Select route",
      frequency: "Frequency",
      removeMedication: "Remove Medication",
      addMedication: "Add Medication",
      proceduresInterventions: "Procedures & Interventions",
      proceduresPlaceholder: "Describe any procedures or interventions planned",
      followUp: "Follow-Up",
      followUpPlaceholder: "Follow-up instructions and timeline",
      learningObjectivePlaceholder: "Enter a learning objective",
      addLearningObjective: "Add Learning Objective",
      primaryDiagnosisRequired: "Primary diagnosis is required",

      // Attachments
      attachments: "Attachments",
      attachmentsDescription: "Upload supporting documents and images",
      uploadFiles: "Upload Files",
      dragDropFiles: "Drag and drop files here",
      orClickToBrowse: "or click to browse",
      selectFiles: "Select Files",
      supportedFormats: "Supported formats",
      maxFileSize: "Max file size",
      perFile: "per file",
      uploadedFiles: "Uploaded Files",
      previewNotAvailable: "Preview not available for this file type",
      caseSummary: "Case Summary",
      patientInfo: "Patient Information",
      name: "Name",
      caseDetails: "Case Details",
      template: "Template",
      fileTooLarge: "File {fileName} is too large. Maximum size is 10MB.",
      unsupportedFileType: "File {fileName} has an unsupported file type.",
      
      // Attachment Form Fields
      attachmentType: "Attachment Type",
      selectType: "Select type",
      title: "Title",
      enterTitle: "Enter title",
      attachmentDepartment: "Department",
      selectDepartment: "Select department",
      description: "Description",
      enterDescription: "Enter description",
      dateTaken: "Date Taken",
      physicianNotes: "Physician Notes",
      enterPhysicianNotes: "Enter physician notes",
      isConfidential: "Is Confidential",
      confidentialDescription: "Only instructors can view confidential attachments",
      
      // Attachment Types
      xRay: "X-Ray",
      labReport: "Lab Report",
      ctScan: "CT Scan",
      mriScan: "MRI Scan",
      ultrasoundType: "Ultrasound",
      injuryPhoto: "Injury Photo",
      surgicalPhoto: "Surgical Photo",
      pathologySlide: "Pathology Slide",
      prescriptionType: "Prescription",
      dischargeSummary: "Discharge Summary",
      vitalSignsType: "Vital Signs",
      ekgEcg: "EKG/ECG",
      endoscopyType: "Endoscopy",
      biopsyReport: "Biopsy Report",
      medicalCertificate: "Medical Certificate",
      otherType: "Other",
      
      // Departments
      cardiology: "Cardiology",
      neurology: "Neurology",
      orthopedics: "Orthopedics",
      pediatrics: "Pediatrics",
      radiology: "Radiology",
      pathology: "Pathology",
      emergency: "Emergency",
      surgery: "Surgery",
      internalMedicine: "Internal Medicine",
    },
  },
  vi: {
    createCase: {
      // Template Selection
      selectTemplate: "Chọn Mẫu Hồ Sơ",
      templateDescription: "Chọn mẫu để bắt đầu tạo hồ sơ bệnh án",
      difficulty: "Độ Khó",
      estimatedTime: "Thời Gian Ước Tính",
      templatePreview: "Xem Trước Mẫu",
      templateDetails: "Chi Tiết Mẫu",
      category: "Danh Mục",
      specialty: "Chuyên Khoa",
      department: "Khoa",
      createdBy: "Tạo Bởi",
      sections: "Các Phần",
      requiredFields: "Trường Bắt Buộc",
      learningObjectives: "Mục Tiêu Học Tập",

      // Basic Information
      basicInformation: "Thông Tin Cơ Bản",
      basicInfoDescription: "Nhập thông tin nhân khẩu học và triệu chứng chính",
      patientDemographics: "Thông Tin Bệnh Nhân",
      firstName: "Tên",
      enterFirstName: "Nhập tên",
      lastName: "Họ",
      enterLastName: "Nhập họ",
      age: "Tuổi",
      enterAge: "Nhập tuổi",
      gender: "Giới Tính",
      selectGender: "Chọn giới tính",
      male: "Nam",
      female: "Nữ",
      other: "Khác",
      medicalRecordNumber: "Số Hồ Sơ Y Tế (MRN)",
      enterMRN: "Nhập MRN",
      dateOfBirth: "Ngày Sinh",
      clinicalPresentation: "Biểu Hiện Lâm Sàng",
      chief_complaint: "Triệu Chứng Chính",
      describe_chief_complaint: "Mô tả triệu chứng chính của bệnh nhân",
      historyOfPresentIllness: "Tiền Sử Bệnh Hiện Tại",
      describeHPI: "Mô tả tiền sử bệnh hiện tại",
      pastMedicalHistory: "Tiền Sử Bệnh Trước Đây",
      describePMH: "Mô tả tiền sử bệnh liên quan",
      firstNameRequired: "Tên là bắt buộc",
      lastNameRequired: "Họ là bắt buộc",
      validAgeRequired: "Tuổi hợp lệ là bắt buộc (0-150)",
      genderRequired: "Giới tính là bắt buộc",
      chief_complaintRequired: "Triệu chứng chính là bắt buộc",

      // Vital Signs
      vitalSigns: "Dấu Hiệu Sinh Tồn",
      vitalSignsDescription: "Ghi lại dấu hiệu sinh tồn và số đo của bệnh nhân",
      recordVitalSigns: "Ghi Dấu Hiệu Sinh Tồn",
      temperature: "Nhiệt Độ",
      heartRate: "Nhịp Tim",
      bloodPressure: "Huyết Áp",
      respiratoryRate: "Nhịp Thở",
      oxygenSaturation: "Độ Bão Hòa Oxy",
      weight: "Cân Nặng",
      height: "Chiều Cao",
      bmi: "BMI",
      painScale: "Thang Điểm Đau",
      additionalNotes: "Ghi Chú Bổ Sung",
      vitalSignsNotesPlaceholder: "Nhập ghi chú bổ sung về dấu hiệu sinh tồn",
      underweight: "Thiếu Cân",
      normalWeight: "Cân Nặng Bình Thường",
      overweight: "Thừa Cân",
      obese: "Béo Phì",

      // Physical Examination
      physicalExamination: "Khám Thể Lực",
      physicalExamDescription: "Ghi lại kết quả khám thể lực",
      generalAppearance: "Ngoại Hình Chung",
      appearance: "Ngoại Hình",
      generalAppearancePlaceholder: "Mô tả ngoại hình chung (ví dụ: dinh dưỡng tốt, không có triệu chứng cấp)",
      mentalStatus: "Tình Trạng Tâm Thần",
      alert: "Tỉnh Táo",
      confused: "Lú Lẫn",
      lethargic: "Hôn Mê",
      unresponsive: "Không Phản Ứng",
      vitalSignsSummary: "Tóm Tắt Dấu Hiệu Sinh Tồn",
      systemsReview: "Đánh Giá Hệ Thống",
      heent: "Đầu, Mắt, Tai, Mũi, Họng",
      heentPlaceholder: "Kết quả khám đầu, mắt, tai, mũi, họng",
      cardiovascular: "Tim Mạch",
      cardiovascularPlaceholder: "Âm tim, nhịp tim, tiếng thổi",
      respiratory: "Hô Hấp",
      respiratoryPlaceholder: "Âm phổi, mô hình thở",
      gastrointestinal: "Tiêu Hóa",
      gastrointestinalPlaceholder: "Kết quả khám bụng",
      genitourinary: "Sinh Dục Tiết Niệu",
      genitourinaryPlaceholder: "Kết quả khám sinh dục tiết niệu",
      musculoskeletal: "Cơ Xương Khớp",
      musculoskeletalPlaceholder: "Sức mạnh cơ, biên độ chuyển động",
      neurological: "Thần Kinh",
      neurologicalPlaceholder: "Dây thần kinh sọ, vận động, cảm giác, phản xạ",
      skin: "Da",
      skinPlaceholder: "Kết quả khám da",
      psychiatric: "Tâm Thần",
      psychiatricPlaceholder: "Tình trạng tâm thần, tâm trạng, cảm xúc",
      physicalExamNotes: "Ghi Chú Khám Thể Lực",
      examNotesPlaceholder: "Ghi chú và kết quả khám bổ sung",

      // Diagnostic Workup
      diagnosticWorkup: "Xét Nghiệm Chẩn Đoán",
      diagnosticWorkupDescription: "Chọn và ghi kết quả xét nghiệm chẩn đoán",
      laboratoryTests: "Xét Nghiệm Phòng Thí Nghiệm",
      result: "Kết Quả",
      otherLabTests: "Xét Nghiệm Khác",
      otherLabTestsPlaceholder: "Liệt kê các xét nghiệm khác đã thực hiện",
      imagingStudies: "Chẩn Đoán Hình Ảnh",
      findings: "Phát Hiện",
      otherImaging: "Hình Ảnh Khác",
      otherImagingPlaceholder: "Liệt kê các nghiên cứu hình ảnh khác",
      otherDiagnosticTests: "Xét Nghiệm Chẩn Đoán Khác",
      results: "Kết Quả",
      additionalTests: "Xét Nghiệm Bổ Sung",
      additionalTestsPlaceholder: "Liệt kê xét nghiệm chẩn đoán bổ sung",
      completeBloodCount: "Công Thức Máu Toàn Phần (CBC)",
      cbcDescription: "WBC, RBC, Hemoglobin, Hematocrit, Tiểu Cầu",
      comprehensiveMetabolicPanel: "Bảng Chuyển Hóa Toàn Diện (CMP)",
      cmpDescription: "Glucose, Chất Điện Giải, Chức Năng Thận & Gan",
      lipidPanel: "Bảng Lipid",
      lipidDescription: "Cholesterol, HDL, LDL, Triglycerides",
      thyroidFunction: "Chức Năng Tuyến Giáp",
      thyroidDescription: "TSH, T3, T4",
      urinalysis: "Xét Nghiệm Nước Tiểu",
      urinalysisDescription: "Phân tích nước tiểu để tìm nhiễm trùng, protein, máu",
      cultures: "Cấy",
      culturesDescription: "Cấy máu, nước tiểu hoặc cấy khác",
      chestXray: "X-Quang Ngực",
      chestXrayDescription: "Hình ảnh X-quang ngực",
      ctChest: "CT Ngực",
      ctChestDescription: "Chụp cắt lớp vi tính ngực",
      ekg: "Điện Tâm Đồ",
      ekgDescription: "Điện tâm đồ",
      echocardiogram: "Siêu Âm Tim",
      echocardiogramDescription: "Siêu âm tim",
      ultrasound: "Siêu Âm",
      ultrasoundDescription: "Siêu âm bụng hoặc siêu âm khác",
      endoscopy: "Nội Soi",
      endoscopyDescription: "Nội soi tiêu hóa trên",
      colonoscopy: "Nội Soi Đại Tràng",
      colonoscopyDescription: "Nội soi tiêu hóa dưới",
      biopsy: "Sinh Thiết",
      biopsyDescription: "Phân tích mẫu mô",
      pulmonaryFunction: "Xét Nghiệm Chức Năng Phổi",
      pulmonaryFunctionDescription: "Đánh giá chức năng phổi",

      // Assessment & Plan
      assessmentAndPlan: "Đánh Giá & Kế Hoạch",
      assessmentPlanDescription: "Ghi chẩn đoán, kế hoạch điều trị và mục tiêu học tập",
      assessment: "Đánh Giá",
      primaryDiagnosis: "Chẩn Đoán Chính",
      primaryDiagnosisPlaceholder: "Nhập chẩn đoán chính",
      differentialDiagnosis: "Chẩn Đoán Phân Biệt",
      differentialDiagnosisPlaceholder: "Liệt kê chẩn đoán phân biệt",
      clinicalReasoning: "Lý Luận Lâm Sàng",
      clinicalReasoningPlaceholder: "Giải thích lý luận lâm sàng và quá trình suy nghĩ",
      treatmentPlan: "Kế Hoạch Điều Trị",
      medications: "Thuốc",
      medicationName: "Tên Thuốc",
      medicationNamePlaceholder: "ví dụ: Lisinopril",
      dosage: "Liều Lượng",
      route: "Đường Dùng",
      selectRoute: "Chọn đường dùng",
      frequency: "Tần Suất",
      removeMedication: "Xóa Thuốc",
      addMedication: "Thêm Thuốc",
      proceduresInterventions: "Thủ Thuật & Can Thiệp",
      proceduresPlaceholder: "Mô tả các thủ thuật hoặc can thiệp dự kiến",
      followUp: "Theo Dõi",
      followUpPlaceholder: "Hướng dẫn và thời gian theo dõi",
      learningObjectivePlaceholder: "Nhập mục tiêu học tập",
      addLearningObjective: "Thêm Mục Tiêu Học Tập",
      primaryDiagnosisRequired: "Chẩn đoán chính là bắt buộc",

      // Attachments
      attachments: "Tệp Đính Kèm",
      attachmentsDescription: "Tải lên tài liệu và hình ảnh hỗ trợ",
      uploadFiles: "Tải Lên Tệp",
      dragDropFiles: "Kéo và thả tệp vào đây",
      orClickToBrowse: "hoặc nhấp để duyệt",
      selectFiles: "Chọn Tệp",
      supportedFormats: "Định dạng được hỗ trợ",
      maxFileSize: "Kích thước tệp tối đa",
      perFile: "mỗi tệp",
      uploadedFiles: "Tệp Đã Tải Lên",
      previewNotAvailable: "Xem trước không khả dụng cho loại tệp này",
      caseSummary: "Tóm Tắt Hồ Sơ",
      patientInfo: "Thông Tin Bệnh Nhân",
      name: "Tên",
      caseDetails: "Chi Tiết Hồ Sơ",
      template: "Mẫu",
      fileTooLarge: "Tệp {fileName} quá lớn. Kích thước tối đa là 10MB.",
      unsupportedFileType: "Tệp {fileName} có loại tệp không được hỗ trợ.",
      
      // Attachment Form Fields
      attachmentType: "Loại Tài Liệu",
      selectType: "Chọn loại",
      title: "Tiêu Đề",
      enterTitle: "Nhập tiêu đề",
      attachmentDepartment: "Khoa",
      selectDepartment: "Chọn khoa",
      description: "Mô Tả",
      enterDescription: "Nhập mô tả",
      dateTaken: "Ngày Chụp/Thực Hiện",
      physicianNotes: "Ghi Chú Bác Sĩ",
      enterPhysicianNotes: "Nhập ghi chú bác sĩ",
      isConfidential: "Bảo Mật",
      confidentialDescription: "Chỉ giảng viên mới có thể xem tài liệu bảo mật",
      
      // Attachment Types
      xRay: "Chụp X-Quang",
      labReport: "Phiếu Xét Nghiệm",
      ctScan: "Chụp CT/Scanner",
      mriScan: "Chụp MRI",
      ultrasoundType: "Siêu Âm",
      injuryPhoto: "Ảnh Chấn Thương",
      surgicalPhoto: "Ảnh Phẫu Thuật",
      pathologySlide: "Tiêu Bản Bệnh Học",
      prescriptionType: "Đơn Thuốc",
      dischargeSummary: "Tóm Tắt Xuất Viện",
      vitalSignsType: "Dấu Hiệu Sinh Tồn",
      ekgEcg: "Điện Tâm Đồ",
      endoscopyType: "Nội Soi",
      biopsyReport: "Kết Quả Sinh Thiết",
      medicalCertificate: "Giấy Chứng Nhận Y Tế",
      otherType: "Khác",
      
      // Departments
      cardiology: "Tim Mạch",
      neurology: "Thần Kinh",
      orthopedics: "Chỉnh Hình",
      pediatrics: "Nhi Khoa",
      radiology: "Chẩn Đoán Hình Ảnh",
      pathology: "Giải Phẫu Bệnh",
      emergency: "Cấp Cứu",
      surgery: "Phẫu Thuật",
      internalMedicine: "Nội Khoa",
    },
  },
} as const;

const i18n = createI18n({
  legacy: false,
  locale: "vi",
  messages,
});

// ---- App bootstrap ----

const app = createApp(App);

app.use(pinia);
app.use(router);
app.use(i18n);

// ---- Navigation guard ----

router.beforeEach((to, from, next) => {
  const authStore = pinia!.state.value.auth;
  const token = localStorage.getItem("access_token");
  const user = authStore?.user;

  // Check authentication
  if (to.meta.requiresAuth) {
    if (!token) {
      // Inform the user they need to login
      toast.info('Please log in to continue.');
      next("/login");
      return;
    }
  }

  // Check role-based access
  if (to.meta.requiresRoles) {
    const requiredRoles = to.meta.requiresRoles as string[];
    
    // Ensure user is loaded
    if (!user) {
      toast.info('Your session is expired. Please log in again.');
      next("/login");
      return;
    }

    // Check if user's role is in required roles
    if (!requiredRoles.includes(user.role)) {
      console.warn(`Access denied: user role "${user.role}" not in allowed roles:`, requiredRoles);
      toast.error('Access denied: You do not have permission to view this page.');
      // Redirect to home or 403 page
      next("/home");
      return;
    }
  }

  next();
});

app.mount("#app");
