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
import "../styles/globals.css";

// Extend RouteMeta to include custom requiresRoles
declare module "vue-router" {
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

import { useToast } from "@/composables/useToast";

const { toast } = useToast();

// ---- Router ----

const routes: RouteRecordRaw[] = [
  { path: "/", component: Landing },
  { path: "/login", component: Login },
  { path: "/home", component: Home, meta: { requiresAuth: true } },

  // Student & Instructor routes (admin restricted)
  {
    path: "/cases",
    component: Cases,
    meta: { requiresAuth: true, requiresRoles: ["student", "instructor"] },
  },
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
    wizard: {
      // Common Buttons & Actions
      cancel: "Cancel",
      saveDraft: "Save Draft",
      back: "Back",
      next: "Next",
      createCase: "Create Case",
      goTo: "Go to: {step}",

      // Messages
      completionRequired:
        "Please complete all required fields before proceeding",
      caseSavedDraft: "Case saved as draft successfully!",
      caseCreated: "Medical case created successfully!",
      failedToDraft: "Failed to save draft. Please try again.",
      failedToCreate: "Failed to create case. Please try again.",
      completeRequired:
        "Please complete all required fields before creating the case",
      buildCase: "Build a complete patient case for clinical practice",

      // Step Titles & Descriptions
      templateSelection: "Template Selection",
      templateSelectionDesc: "Choose a case template to get started",
      basicInfo: "Basic Information",
      basicInfoDesc: "Patient demographics and chief complaint",
      vitalSigns: "Vital Signs",
      vitalSignsDesc: "Record vital signs and measurements",
      physicalExam: "Physical Examination",
      physicalExamDesc: "Document physical examination findings",
      diagnosticWorkup: "Diagnostic Workup",
      diagnosticWorkupDesc: "Laboratory tests and imaging studies",
      assessmentPlan: "Assessment & Plan",
      assessmentPlanDesc: "Diagnosis, treatment plan, and learning objectives",
      attachmentsStep: "Attachments",
      attachmentsDesc: "Upload images and supporting documents",
    },
    createCase: {
      // Template Selection
      selectTemplate: "Select Case Template",
      templateDescription:
        "Choose a template to start building your clinical case",
      difficulty: "Difficulty",
      estimatedTime: "Est. Time",
      templatePreview: "Template Preview",
      templateDetails: "Template Details",
      category: "Category",
      specialty: "Specialty",
      department: "Department",
      createdBy: "Created By",
      sections: "Template Sections",
      requiredFields: "Required Fields",
      learningObjectives: "Learning Objectives",
      loadingTemplates: "Loading templates...",
      noTemplates: "No templates available",
      templateLoadError: "Error loading templates",
      noDescriptionAvailable: "No description available",
      notApplicable: "N/A",
      noSectionsDefined: "No sections defined",

      // Basic Information
      basicInformation: "Basic Information",
      basicInfoDescription: "Enter patient demographics and chief complaint",
      caseTitle: "Case Title",
      enterCaseTitle: "Enter case title",
      canBeAnonymized: "(can be anonymized)",
      specialtyExample: "e.g., Cardiology, Neurology",
      complexity: "Complexity Level",
      complexityBasic: "Basic",
      complexityIntermediate: "Intermediate",
      complexityAdvanced: "Advanced",
      complexityExpert: "Expert",
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
      ethnicity: "Ethnicity",
      enterEthnicity: "Enter patient ethnicity",
      occupation: "Occupation",
      enterOccupation: "Enter patient occupation",
      admissionDate: "Admission Date",
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
      caseTitleRequired: "Case title is required",
      patientNameRequired: "Patient name is required",
      specialtyRequired: "Specialty is required",
      briefChiefComplaint: "Brief Chief Complaint",
      enterBriefComplaint: "One-line summary",
      detailedHistory: "Detailed history of current illness",
      currentMedications: "Current Medications",
      listMedications: "List current medications",
      allergies: "Allergies",
      enterAllergies: "Known allergies",

      // Vital Signs
      vitalSigns: "Vital Signs",
      vitalSignsDescription: "Record patient vital signs and measurements",
      recordVitalSigns: "Record Vital Signs",
      vitalSignsPhysicalMeasurements: "Vital Signs & Physical Measurements",
      recordPatientVitalSigns:
        "Record the patient's vital signs and basic physical measurements",
      temperature: "Temperature",
      temperatureUnit: "(°C)",
      heartRate: "Heart Rate",
      heartRateUnit: "(bpm)",
      bloodPressure: "Blood Pressure",
      bloodPressureUnit: "(mmHg)",
      bloodPressureFormat: "Format: systolic/diastolic (e.g., 120/80)",
      respiratoryRate: "Respiratory Rate",
      respiratoryRateUnit: "(breaths/min)",
      oxygenSaturation: "Oxygen Saturation",
      oxygenSaturationUnit: "(%)",
      weight: "Weight",
      weightUnit: "(kg)",
      height: "Height",
      heightUnit: "(cm)",
      bmi: "BMI",
      bmiUnit: "(kg/m²)",
      bmiCategory: "BMI Category",
      autoCalculated: "Auto-calculated",
      generalAppearanceNotes: "General Appearance & Vital Signs Notes",
      generalAppearanceNotesPlaceholder:
        "Describe general appearance, vital signs stability, any abnormalities...",
      painScale: "Pain Scale",
      additionalNotes: "Additional Notes",
      vitalSignsNotesPlaceholder:
        "Enter any additional notes about vital signs",
      underweight: "Underweight",
      normalWeight: "Normal Weight",
      overweight: "Overweight",
      obese: "Obese",

      // Physical Examination
      physicalExamination: "Physical Examination",
      physicalExamDescription: "Document physical examination findings",
      generalAppearance: "General Appearance",
      appearance: "Appearance",
      generalAppearancePlaceholder:
        "Describe general appearance (e.g., well-nourished, in no acute distress)",
      consciousnessLevel: "Consciousness Level",
      obtunded: "Obtunded",
      stuporous: "Stuporous",
      comatose: "Comatose",
      mentalStatus: "Mental Status",
      alert: "Alert",
      confused: "Confused",
      lethargic: "Lethargic",
      unresponsive: "Unresponsive",
      vitalSignsSummary: "Vital Signs Summary",
      notRecorded: "Not recorded",
      physicalExaminationBySystem: "Physical Examination by System",
      headAndNeck: "Head and Neck",
      heentPlaceholder:
        "HEENT: pupils, ears, nose, throat, neck examination...",
      cardiovascular: "Cardiovascular",
      cardiovascularPlaceholder:
        "Heart sounds, murmurs, rhythm, peripheral pulses...",
      respiratory: "Respiratory",
      respiratoryPlaceholder:
        "Breath sounds, chest expansion, percussion findings...",
      abdominal: "Abdominal",
      abdominalPlaceholder:
        "Inspection, auscultation, palpation, percussion findings...",
      neurological: "Neurological",
      neurologicalPlaceholder:
        "Cranial nerves, motor, sensory, reflexes, coordination...",
      musculoskeletal: "Musculoskeletal",
      musculoskeletalPlaceholder:
        "Joint examination, range of motion, deformities, tenderness...",
      skin: "Skin",
      skinPlaceholder: "Color, turgor, lesions, rashes, wounds...",
      additionalExaminationNotes: "Additional Examination Notes",
      additionalFindingsPlaceholder:
        "Any additional examination findings, special tests, or pertinent negatives...",

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
      laboratoryResults: "Laboratory Results",
      completeLaboratoryResults: "Complete Laboratory Results",
      completeLabPlaceholder:
        "Enter all laboratory test results including CBC, CMP, liver function, coagulation studies...",
      hemoglobin: "Hemoglobin",
      hemoglobinUnit: "(g/dL)",
      whiteBloodCellCount: "White Blood Cell Count",
      wbcUnit: "(10^9/L)",
      plateletCount: "Platelet Count",
      plateletUnit: "(10^9/L)",
      sodium: "Sodium",
      sodiumUnit: "(mmol/L)",
      potassium: "Potassium",
      potassiumUnit: "(mmol/L)",
      creatinine: "Creatinine",
      creatinineUnit: "(mg/dL)",
      glucose: "Glucose",
      glucoseUnit: "(mg/dL)",
      imagingFindings: "Imaging Findings",
      imagingFindingsPlaceholder:
        "Describe all imaging findings: X-rays, CT scans, MRI, ultrasound, etc...",
      pathologyResults: "Pathology Results",
      pathologyPlaceholder: "Biopsy results, histopathology findings...",
      microbiologyResults: "Microbiology Results",
      microbiologyPlaceholder: "Culture results, sensitivity testing...",
      additionalInvestigations: "Additional Investigations",
      additionalInvestigationsPlaceholder:
        "ECG findings, echocardiography, endoscopy, other special tests...",
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
      pulmonaryFunctionDescription: "Lung function test results",

      // Assessment & Plan
      assessmentAndPlan: "Assessment & Plan",
      diagnosis: "Diagnosis",
      icdCode: "ICD-10 Code",
      icdCodePlaceholder: "e.g., J18.9 (Pneumonia, unspecified)",
      assessmentPlanDescription:
        "Document diagnosis, treatment plan, and learning objectives",
      assessment: "Assessment",
      primaryDiagnosis: "Primary Diagnosis",
      primaryDiagnosisPlaceholder: "Enter the primary diagnosis",
      differentialDiagnosis: "Differential Diagnosis",
      differentialDiagnosisPlaceholder: "List differential diagnoses",
      managementPlan: "Patient Management Plan",
      clinicalReasoning: "Clinical Reasoning",
      clinicalReasoningPlaceholder:
        "Explain the clinical reasoning and thought process",
      treatmentPlan: "Treatment Plan",
      treatmentPlanPlaceholder:
        "Detailed treatment approach including immediate interventions, ongoing management...",
      medications: "Medications",
      medicationsPrescribed: "Medications Prescribed",
      medicationsPrescribedPlaceholder:
        "List all medications with dosage, route, frequency, and duration...",
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
      prognosis: "Prognosis",
      prognosisPlaceholder: "Expected outcomes, potential complications...",
      educationalObjectives: "Educational Objectives",
      learningObjectivesPlaceholder:
        "What should students learn from this case? List specific objectives...",
      keyConcepts: "Key Concepts",
      keyConceptsPlaceholder:
        "Important medical concepts illustrated by this case...",
      clinicalPearls: "Clinical Pearls",
      clinicalPearlsPlaceholder:
        "Important clinical insights, tips, or teaching points...",
      references: "References",
      referencesPlaceholder: "Relevant literature, guidelines, or resources...",

      // Attachments
      attachments: "Attachments",
      mrn: "MRN",
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
      notSpecified: "Not specified",
      notAssigned: "Not assigned",
      caseDetails: "Case Details",
      template: "Template",
      fileTooLarge: " is too large. Maximum size is 10MB.",
      unsupportedFileType: " is an unsupported file type.",

      // Attachment Form Fields
      attachmentType: "Attachment Type",
      selectType: "Select type",
      title: "Title",
      untitledCase: "Untitled Case",
      enterTitle: "Enter title",
      attachmentDepartment: "Department",
      selectDepartment: "Select department",
      description: "Description",
      enterDescription: "Enter description",
      dateTaken: "Date Taken",
      physicianNotes: "Physician Notes",
      enterPhysicianNotes: "Enter physician notes",
      isConfidential: "Is Confidential",
      confidentialDescription:
        "Only instructors can view confidential attachments",

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

      // Field Names (for sections and required fields)
      clinicalHistory: "Clinical History",
      investigations: "Investigations",
      diagnosisManagement: "Diagnosis & Management",
      learningOutcomes: "Learning Outcomes",
      patientName: "Patient Name",
      patientAge: "Patient Age",

      // Departments
      cardiology: "Cardiology",
      neurology: "Neurology",
      orthopedics: "Orthopedics",
      pediatrics: "Pediatrics",
      gastroenterology: "Gastroenterology",
      emergency: "Emergency",
      surgery: "Surgery",
      internalMedicine: "Internal Medicine",
    },
  },
  vi: {
    wizard: {
      // Common Buttons & Actions
      cancel: "Hủy",
      saveDraft: "Lưu Nháp",
      back: "Quay Lại",
      next: "Tiếp Theo",
      createCase: "Tạo Hồ Sơ",
      goTo: "Đi tới: {step}",

      // Messages
      completionRequired:
        "Vui lòng hoàn thành tất cả các trường bắt buộc trước khi tiếp tục",
      caseSavedDraft: "Hồ sơ đã được lưu thành nháp thành công!",
      caseCreated: "Hồ sơ bệnh án được tạo thành công!",
      failedToDraft: "Không thể lưu nháp. Vui lòng thử lại.",
      failedToCreate: "Không thể tạo hồ sơ. Vui lòng thử lại.",
      completeRequired:
        "Vui lòng hoàn thành tất cả các trường bắt buộc trước khi tạo hồ sơ",
      buildCase: "Xây dựng hồ sơ bệnh án đầy đủ cho thực hành lâm sàng",

      // Step Titles & Descriptions
      templateSelection: "Chọn Mẫu Hồ Sơ",
      templateSelectionDesc: "Chọn mẫu để bắt đầu tạo hồ sơ",
      basicInfo: "Thông Tin Cơ Bản",
      basicInfoDesc: "Thông tin nhân khẩu học và triệu chứng chính",
      vitalSigns: "Dấu Hiệu Sinh Tồn",
      vitalSignsDesc: "Ghi lại dấu hiệu sinh tồn và số đo",
      physicalExam: "Khám Thể Lực",
      physicalExamDesc: "Ghi lại kết quả khám thể lực",
      diagnosticWorkup: "Xét Nghiệm Chẩn Đoán",
      diagnosticWorkupDesc: "Xét nghiệm phòng thí nghiệm và chẩn đoán hình ảnh",
      assessmentPlan: "Đánh Giá & Kế Hoạch",
      assessmentPlanDesc: "Chẩn đoán, kế hoạch điều trị và mục tiêu học tập",
      attachmentsStep: "Tệp Đính Kèm",
      attachmentsDesc: "Tải lên hình ảnh và tài liệu hỗ trợ",
    },
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
      sections: "Các Phần Mẫu",
      requiredFields: "Trường Bắt Buộc",
      learningObjectives: "Mục Tiêu Học Tập",
      loadingTemplates: "Đang tải mẫu...",
      noTemplates: "Không có mẫu nào",
      templateLoadError: "Lỗi khi tải mẫu",
      noDescriptionAvailable: "Không có mô tả",
      notApplicable: "N/A",
      noSectionsDefined: "Không có phần nào được xác định",

      // Basic Information
      basicInformation: "Thông Tin Cơ Bản",
      basicInfoDescription: "Nhập thông tin nhân khẩu học và triệu chứng chính",
      caseInformation: "Thông Tin Hồ Sơ",
      caseTitle: "Tiêu Đề Hồ Sơ",
      enterCaseTitle: "Nhập tiêu đề hồ sơ",
      canBeAnonymized: "(có thể được ẩn danh)",
      specialtyExample: "ví dụ: Tim Mạch, Thần Kinh",
      complexity: "Mức Độ Phức Tạp",
      complexityBasic: "Cơ Bản",
      complexityIntermediate: "Trung Bình",
      complexityAdvanced: "Nâng Cao",
      complexityExpert: "Chuyên Gia",
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
      ethnicity: "Dân Tộc",
      enterEthnicity: "Nhập dân tộc bệnh nhân",
      occupation: "Nghề Nghiệp",
      enterOccupation: "Nhập nghề nghiệp bệnh nhân",
      admissionDate: "Ngày Nhập Viện",
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
      caseTitleRequired: "Tiêu đề hồ sơ là bắt buộc",
      patientNameRequired: "Tên bệnh nhân là bắt buộc",
      specialtyRequired: "Chuyên khoa là bắt buộc",
      briefChiefComplaint: "Tóm Tắt Triệu Chứng Chính",
      enterBriefComplaint: "Tóm tắt một dòng",
      detailedHistory: "Tiền sử chi tiết của bệnh hiện tại",
      currentMedications: "Thuốc Hiện Tại",
      listMedications: "Liệt kê các thuốc hiện tại",
      allergies: "Dị Ứng",
      enterAllergies: "Dị ứng đã biết",

      // Vital Signs
      vitalSigns: "Dấu Hiệu Sinh Tồn",
      vitalSignsDescription: "Ghi lại dấu hiệu sinh tồn và số đo của bệnh nhân",
      recordVitalSigns: "Ghi Dấu Hiệu Sinh Tồn",
      vitalSignsPhysicalMeasurements: "Dấu Hiệu Sinh Tồn & Số Đo Thể Chất",
      recordPatientVitalSigns:
        "Ghi lại dấu hiệu sinh tồn và số đo thể chất cơ bản của bệnh nhân",
      temperature: "Nhiệt Độ",
      temperatureUnit: "(°C)",
      heartRate: "Nhịp Tim",
      heartRateUnit: "(bpm)",
      bloodPressure: "Huyết Áp",
      bloodPressureUnit: "(mmHg)",
      bloodPressureFormat: "Định dạng: tâm trương/tâm nhân (ví dụ: 120/80)",
      respiratoryRate: "Nhịp Thở",
      respiratoryRateUnit: "(lần/phút)",
      oxygenSaturation: "Độ Bão Hòa Oxy",
      oxygenSaturationUnit: "(%)",
      weight: "Cân Nặng",
      weightUnit: "(kg)",
      height: "Chiều Cao",
      heightUnit: "(cm)",
      bmi: "BMI",
      bmiUnit: "(kg/m²)",
      bmiCategory: "Phân Loại BMI",
      autoCalculated: "Tự động tính toán",
      generalAppearanceNotes: "Ngoại Hình Chung & Ghi Chú Dấu Hiệu Sinh Tồn",
      generalAppearanceNotesPlaceholder:
        "Mô tả ngoại hình chung, tính ổn định dấu hiệu sinh tồn, bất kỳ bất thường nào...",
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
      generalAppearancePlaceholder:
        "Mô tả ngoại hình chung (ví dụ: dinh dưỡng tốt, không có triệu chứng cấp)",
      consciousnessLevel: "Mức Độ Tỉnh Táo",
      obtunded: "Buồn Ngủ",
      stuporous: "Thần Trí Mơ Màng",
      comatose: "Hôn Mê",
      mentalStatus: "Tình Trạng Tinh Thần",
      alert: "Tỉnh Táo",
      confused: "Lú Lẫn",
      lethargic: "Hôn Mê",
      unresponsive: "Không Phản Ứng",
      vitalSignsSummary: "Tóm Tắt Dấu Hiệu Sinh Tồn",
      notRecorded: "Chưa ghi nhận",
      physicalExaminationBySystem: "Khám Thể Lực Theo Hệ Thống",
      headAndNeck: "Đầu và Cổ",
      heentPlaceholder: "HEENT: sơ cơ, tai, mũi, họng, khám cổ...",
      cardiovascular: "Tim Mạch",
      cardiovascularPlaceholder:
        "Âm tim, tiếng thổi, nhịp tim, xung động ngoại biên...",
      respiratory: "Hô Hấp",
      respiratoryPlaceholder: "Âm phổi, mở rộng ngực, phát hiện gõ phổi...",
      abdominal: "Bụng",
      abdominalPlaceholder: "Khám nhìn, nghe, sờ, gõ bụng...",
      neurological: "Thần Kinh",
      neurologicalPlaceholder:
        "Dây thần kinh sọ, vận động, cảm giác, phản xạ, điều phối...",
      musculoskeletal: "Cơ Xương Khớp",
      musculoskeletalPlaceholder:
        "Khám khớp, biên độ chuyển động, dị hình, cảm giác đau...",
      skin: "Da",
      skinPlaceholder: "Màu sắc, mất độ, tổn thương, phát ban, vết thương...",
      additionalExaminationNotes: "Ghi Chú Khám Bổ Sung",
      additionalFindingsPlaceholder:
        "Bất kỳ phát hiện khám bổ sung, xét nghiệm đặc biệt hoặc những điều không có triệu chứng...",
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
      urinalysisDescription:
        "Phân tích nước tiểu để tìm nhiễm trùng, protein, máu",
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
      pulmonaryFunctionDescription: "Kết quả xét nghiệm chức năng phổi",
      laboratoryResults: "Kết Quả Xét Nghiệm Phòng Thí Nghiệm",
      completeLaboratoryResults:
        "Kết Quả Xét Nghiệm Phòng Thí Nghiệm Hoàn Chỉnh",
      completeLabPlaceholder:
        "Nhập tất cả kết quả xét nghiệm phòng thí nghiệm bao gồm CBC, CMP, chức năng gan, xét nghiệm đông máu...",
      hemoglobin: "Hemoglobin",
      hemoglobinUnit: "(g/dL)",
      whiteBloodCellCount: "Số Lượng Bạch Cầu",
      wbcUnit: "(10^9/L)",
      plateletCount: "Số Lượng Tiểu Cầu",
      plateletUnit: "(10^9/L)",
      sodium: "Natri",
      sodiumUnit: "(mmol/L)",
      potassium: "Kali",
      potassiumUnit: "(mmol/L)",
      creatinine: "Creatinine",
      creatinineUnit: "(mg/dL)",
      glucose: "Glucose",
      glucoseUnit: "(mg/dL)",
      imagingFindings: "Phát Hiện Hình Ảnh",
      imagingFindingsPlaceholder:
        "Mô tả tất cả phát hiện hình ảnh: X-quang, CT, MRI, siêu âm, v.v...",
      pathologyResults: "Kết Quả Bệnh Học",
      pathologyPlaceholder: "Kết quả sinh thiết, phát hiện mô bệnh học...",
      microbiologyResults: "Kết Quả Vi Sinh Vật",
      microbiologyPlaceholder: "Kết quả cấy, xét nghiệm nhạy cảm...",
      additionalInvestigations: "Xét Nghiệm Bổ Sung",
      additionalInvestigationsPlaceholder:
        "Phát hiện điện tâm đồ, siêu âm tim, nội soi, các xét nghiệm đặc biệt khác...",

      // Assessment & Plan
      assessmentAndPlan: "Đánh Giá & Kế Hoạch",
      diagnosis: "Chẩn Đoán",
      icdCode: "Mã ICD-10",
      icdCodePlaceholder: "ví dụ: J18.9 (Viêm phổi, không xác định)",
      assessmentPlanDescription:
        "Ghi chẩn đoán, kế hoạch điều trị và mục tiêu học tập",
      assessment: "Đánh Giá",
      primaryDiagnosis: "Chẩn Đoán Chính",
      primaryDiagnosisPlaceholder: "Nhập chẩn đoán chính",
      differentialDiagnosis: "Chẩn Đoán Phân Biệt",
      differentialDiagnosisPlaceholder: "Liệt kê chẩn đoán phân biệt",
      clinicalReasoning: "Lý Luận Lâm Sàng",
      clinicalReasoningPlaceholder:
        "Giải thích lý luận lâm sàng và quá trình suy nghĩ",
      managementPlan: "Kế Hoạch Quản Lý Bệnh Nhân",
      treatmentPlan: "Kế Hoạch Điều Trị",
      treatmentPlanPlaceholder:
        "Phương pháp điều trị chi tiết bao gồm can thiệp ngay lập tức, quản lý liên tục...",
      medications: "Thuốc",
      medicationsPrescribed: "Thuốc Được Kê Đơn",
      medicationsPrescribedPlaceholder:
        "Liệt kê tất cả các thuốc được kê đơn trong kế hoạch điều trị với liều lượng, đường dùng, tần suất và thời gian...",
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
      prognosis: "Tiên Lượng",
      prognosisPlaceholder: "Kết quả dự kiến, các biến chứng tiềm ẩn...",
      educationalObjectives: "Mục Tiêu Giáo Dục",
      learningObjectivesPlaceholder:
        "Học sinh nên học gì từ hồ sơ này? Liệt kê các mục tiêu cụ thể...",
      keyConcepts: "Khái Niệm Chính",
      keyConceptsPlaceholder:
        "Các khái niệm y học quan trọng được minh họa bởi hồ sơ này...",
      clinicalPearls: "Mẹo Lâm Sàng",
      clinicalPearlsPlaceholder:
        "Những hiểu biết lâm sàng quan trọng, mẹo hoặc điểm giảng dạy...",
      references: "Tài Liệu Tham Khảo",
      referencesPlaceholder: "Tài liệu, hướng dẫn hoặc nguồn liên quan...",

      // Attachments
      attachments: "Tệp Đính Kèm",
      mrn: "Số Hồ Sơ Y Tế",
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
      notSpecified: "Chưa xác định",
      notAssigned: "Chưa được gán",
      caseDetails: "Chi Tiết Hồ Sơ",
      template: "Mẫu",
      fileTooLarge: " quá lớn. Kích thước tối đa là 10MB.",
      unsupportedFileType: " là loại tệp không được hỗ trợ.",

      // Attachment Form Fields
      attachmentType: "Loại Tài Liệu",
      selectType: "Chọn loại",
      title: "Tiêu Đề",
      untitledCase: "Hồ Sơ Chưa Đặt Tên",
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

      // Field Names (for sections and required fields)
      clinicalHistory: "Lịch Sử Lâm Sàng",
      investigations: "Xét Nghiệm & Chẩn Đoán Hình Ảnh",
      diagnosisManagement: "Chẩn Đoán & Quản Lý",
      learningOutcomes: "Kết Quả Học Tập",
      patientName: "Tên Bệnh Nhân",
      patientAge: "Tuổi Bệnh Nhân",

      // Departments
      cardiology: "Tim Mạch",
      neurology: "Thần Kinh",
      orthopedics: "Chỉnh Hình",
      pediatrics: "Nhi Khoa",
      gastroenterology: "Tiêu Hóa",
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
      toast.info("Please log in to continue.");
      next("/login");
      return;
    }
  }

  // Check role-based access
  if (to.meta.requiresRoles) {
    const requiredRoles = to.meta.requiresRoles as string[];

    // Ensure user is loaded
    if (!user) {
      toast.info("Your session is expired. Please log in again.");
      next("/login");
      return;
    }

    // Check if user's role is in required roles
    if (!requiredRoles.includes(user.role)) {
      console.warn(
        `Access denied: user role "${user.role}" not in allowed roles:`,
        requiredRoles,
      );
      toast.error(
        "Access denied: You do not have permission to view this page.",
      );
      // Redirect to home or 403 page
      next("/home");
      return;
    }
  }

  next();
});

app.mount("#app");
