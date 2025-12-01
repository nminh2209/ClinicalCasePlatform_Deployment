from django.db import models
from django.conf import settings
from django.forms import ValidationError
from django.utils import timezone
import os
import magic


class Department(models.Model):
    """
    Medical departments/specialties
    """

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    vietnamese_name = models.CharField(
        max_length=100, blank=True, help_text="Tên tiếng Việt"
    )
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    head_of_department = models.CharField(max_length=200, blank=True)
    contact_email = models.EmailField(blank=True, help_text="Email liên hệ")
    department_type = models.CharField(
        max_length=50,
        choices=[
            ("clinical", "Lâm sàng"),
            ("paraclinical", "Cận lâm sàng"),
            ("administrative", "Hành chính"),
        ],
        default="clinical",
        help_text="Loại khoa phòng",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cases_department"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class ClinicalHistory(models.Model):
    """
    Detailed clinical history section
    """

    case = models.OneToOneField(
        "Case", on_delete=models.CASCADE, related_name="clinical_history"
    )
    chief_complaint = models.TextField(help_text="Lý do chính đến khám")
    history_present_illness = models.TextField(help_text="Tiền sử bệnh hiện tại")
    symptom_duration_days = models.PositiveIntegerField(
        null=True, blank=True, help_text="Thời gian có triệu chứng (ngày)"
    )
    symptom_onset = models.CharField(
        max_length=50,
        choices=[
            ("sudden", "Đột ngột"),
            ("gradual", "Từ từ"),
            ("chronic", "Mạn tính"),
        ],
        blank=True,
        help_text="Khởi phát triệu chứng",
    )
    symptom_progression = models.CharField(
        max_length=50,
        choices=[
            ("improving", "Cải thiện"),
            ("worsening", "Xấu đi"),
            ("stable", "Ổn định"),
            ("fluctuating", "Biến đổi"),
        ],
        blank=True,
        help_text="Diễn biến triệu chứng",
    )
    past_medical_history = models.TextField(blank=True, help_text="Tiền sử bệnh tật")
    family_history = models.TextField(blank=True, help_text="Tiền sử gia đình")
    social_history = models.TextField(
        blank=True, help_text="Tiền sử xã hội (hút thuốc, uống rượu, v.v.)"
    )
    allergies = models.TextField(blank=True, help_text="Dị ứng")
    medications = models.TextField(blank=True, help_text="Thuốc đang sử dụng")
    review_systems = models.TextField(blank=True, help_text="Hỏi bệnh theo hệ thống")
    documented_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="documented_histories",
        help_text="Người ghi chép tiền sử",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cases_clinicalhistory"
        verbose_name = "Clinical History"
        verbose_name_plural = "Clinical Histories"

    def __str__(self):
        return f"Clinical History - {self.case.title}"


class PhysicalExamination(models.Model):
    """
    Detailed physical examination section
    """

    case = models.OneToOneField(
        "Case", on_delete=models.CASCADE, related_name="physical_examination"
    )
    general_appearance = models.TextField(help_text="Thể trạng chung")
    consciousness_level = models.CharField(
        max_length=50,
        choices=[
            ("alert", "Tỉnh táo"),
            ("drowsy", "Lơ mơ"),
            ("stupor", "Hôn mê nông"),
            ("coma", "Hôn mê sâu"),
        ],
        default="alert",
        help_text="Mức độ ý thức",
    )
    vital_signs = models.TextField(help_text="Dấu hiệu sinh tồn tổng hợp")
    # Detailed vital signs
    vital_signs_bp = models.CharField(
        max_length=20, blank=True, help_text="Huyết áp (mmHg)"
    )
    vital_signs_hr = models.PositiveIntegerField(
        null=True, blank=True, help_text="Nhịp tim (lần/phút)"
    )
    vital_signs_rr = models.PositiveIntegerField(
        null=True, blank=True, help_text="Nhịp thở (lần/phút)"
    )
    vital_signs_temp = models.FloatField(
        null=True, blank=True, help_text="Nhiệt độ (°C)"
    )
    vital_signs_spo2 = models.PositiveIntegerField(
        null=True, blank=True, help_text="SpO2 (%)"
    )
    height_cm = models.FloatField(null=True, blank=True, help_text="Chiều cao (cm)")
    weight_kg = models.FloatField(null=True, blank=True, help_text="Cân nặng (kg)")
    bmi = models.FloatField(null=True, blank=True, help_text="Chỉ số BMI")
    head_neck = models.TextField(blank=True, help_text="Đầu và cổ")
    cardiovascular = models.TextField(blank=True, help_text="Tim mạch")
    respiratory = models.TextField(blank=True, help_text="Hô hấp")
    abdominal = models.TextField(blank=True, help_text="Bụng")
    neurological = models.TextField(blank=True, help_text="Thần kinh")
    musculoskeletal = models.TextField(blank=True, help_text="Cơ xương khớp")
    skin = models.TextField(blank=True, help_text="Da")
    other_systems = models.TextField(blank=True, help_text="Các hệ khác")
    examined_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="conducted_examinations",
        help_text="Người thực hiện khám",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cases_physicalexamination"
        verbose_name = "Physical Examination"
        verbose_name_plural = "Physical Examinations"

    def __str__(self):
        return f"Physical Examination - {self.case.title}"


class MedicalTerm(models.Model):
    """
    Canonical medical terminology store supporting Vietnamese and English terms,
    synonyms, specialty categorization and simple metadata for autocomplete/search.
    """

    term = models.CharField(
        max_length=255, help_text="Canonical term (prefer Vietnamese)"
    )
    vietnamese_term = models.CharField(max_length=255, blank=True)
    english_term = models.CharField(max_length=255, blank=True)
    synonyms = models.JSONField(
        default=list, blank=True, help_text="List of alternative terms/synonyms"
    )
    definition = models.TextField(blank=True)
    specialty = models.CharField(
        max_length=100, blank=True, help_text="Medical specialty tag"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cases_medicalterm"
        indexes = [
            models.Index(fields=["term"]),
            models.Index(fields=["vietnamese_term"]),
        ]

    def __str__(self):
        return self.vietnamese_term or self.term


class ICD10Code(models.Model):
    """
    Basic ICD-10 code table with Vietnamese descriptions.
    """

    code = models.CharField(max_length=12, unique=True)
    description_en = models.TextField(blank=True)
    description_vi = models.TextField(blank=True)
    chapter = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "cases_icd10code"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.description_vi or self.description_en}"


class MedicalAbbreviation(models.Model):
    """
    Shortforms and their expansions to help with automatic expansion in forms.
    """

    abbr = models.CharField(max_length=64, unique=True)
    expansion = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    specialty = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "cases_medicalabbreviation"

    def __str__(self):
        return f"{self.abbr} -> {self.expansion}"


class Investigations(models.Model):
    """
    Laboratory and diagnostic investigations
    """

    case = models.OneToOneField(
        "Case", on_delete=models.CASCADE, related_name="investigations_detail"
    )
    laboratory_results = models.TextField(
        blank=True, help_text="Kết quả xét nghiệm tổng quát"
    )
    # Detailed lab values
    hemoglobin_level = models.FloatField(
        null=True, blank=True, help_text="Hemoglobin (g/dL)"
    )
    white_cell_count = models.FloatField(
        null=True, blank=True, help_text="Bạch cầu (10^9/L)"
    )
    platelet_count = models.FloatField(
        null=True, blank=True, help_text="Tiểu cầu (10^9/L)"
    )
    sodium_level = models.FloatField(
        null=True, blank=True, help_text="Natri (mmol/L)"
    )
    potassium_level = models.FloatField(
        null=True, blank=True, help_text="Kali (mmol/L)"
    )
    glucose_level = models.FloatField(
        null=True, blank=True, help_text="Glucose (mg/dL)"
    )
    creatinine_level = models.FloatField(
        null=True, blank=True, help_text="Creatinine (mg/dL)"
    )
    imaging_studies = models.TextField(
        blank=True, help_text="Chẩn đoán hình ảnh (X-quang, CT, MRI, siêu âm)"
    )
    ecg_findings = models.TextField(blank=True, help_text="Điện tim")
    ecg_rhythm = models.CharField(
        max_length=50, blank=True, help_text="Nhịp điện tim (sinus, AF, etc.)"
    )
    ecg_rate = models.PositiveIntegerField(
        null=True, blank=True, help_text="Tần số điện tim (bpm)"
    )
    pathology_results = models.TextField(blank=True, help_text="Kết quả giải phẫu bệnh")
    microbiology_results = models.TextField(blank=True, help_text="Kết quả vi sinh")
    other_investigations = models.TextField(blank=True, help_text="Xét nghiệm khác")
    arterial_blood_gas = models.TextField(blank=True, help_text="Khí máu động mạch")
    ph_level = models.FloatField(null=True, blank=True, help_text="pH máu")
    special_tests = models.TextField(blank=True, help_text="Các xét nghiệm đặc biệt")
    microbiology = models.TextField(blank=True, help_text="Vi sinh")
    biochemistry = models.TextField(blank=True, help_text="Sinh hóa")
    hematology = models.TextField(blank=True, help_text="Huyết học")
    ordered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ordered_investigations",
        help_text="Người chỉ định xét nghiệm",
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_investigations",
        help_text="Người xem xét kết quả",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cases_investigations"
        verbose_name = "Investigation"
        verbose_name_plural = "Investigations"

    def __str__(self):
        return f"Investigations - {self.case.title}"


class DiagnosisManagement(models.Model):
    """
    Diagnosis and management plan
    """

    case = models.OneToOneField(
        "Case", on_delete=models.CASCADE, related_name="diagnosis_management"
    )
    primary_diagnosis = models.TextField(help_text="Chẩn đoán chính")
    differential_diagnosis = models.TextField(
        blank=True, help_text="Chẩn đoán phân biệt"
    )
    icd10_codes = models.CharField(max_length=200, blank=True, help_text="Mã ICD-10")
    treatment_plan = models.TextField(help_text="Kế hoạch điều trị")
    medications_prescribed = models.TextField(blank=True, help_text="Thuốc được kê đơn")
    procedures_performed = models.TextField(
        blank=True, help_text="Các thủ thuật đã thực hiện"
    )
    follow_up_plan = models.TextField(blank=True, help_text="Kế hoạch theo dõi")
    prognosis = models.TextField(blank=True, help_text="Tiên lượng")
    complications = models.TextField(blank=True, help_text="Biến chứng")
    managed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_diagnoses",
        help_text="Người quản lý điều trị",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cases_diagnosismanagement"
        verbose_name = "Diagnosis & Management"
        verbose_name_plural = "Diagnosis & Management"

    def __str__(self):
        return f"Diagnosis & Management - {self.case.title}"


class LearningOutcomes(models.Model):
    """
    Learning objectives and educational outcomes
    """

    case = models.OneToOneField(
        "Case", on_delete=models.CASCADE, related_name="learning_outcomes"
    )
    learning_objectives = models.TextField(help_text="Mục tiêu học tập")
    key_concepts = models.TextField(blank=True, help_text="Khái niệm chính")
    clinical_pearls = models.TextField(blank=True, help_text="Kinh nghiệm lâm sàng")
    references = models.TextField(blank=True, help_text="Tài liệu tham khảo")
    discussion_points = models.TextField(blank=True, help_text="Điểm thảo luận")
    assessment_criteria = models.TextField(blank=True, help_text="Tiêu chí đánh giá")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cases_learningoutcomes"
        verbose_name = "Learning Outcome"
        verbose_name_plural = "Learning Outcomes"

    def __str__(self):
        return f"Learning Outcomes - {self.case.title}"


def medical_attachment_upload_to(instance, filename):
    """
    Dynamic upload path for medical attachments.
    Example: medical_attachments/case_12/xray/2025/11/scan_1.png
    """
    # Extract case id and attachment type for structured folder organization
    case_id = instance.case.id if instance.case_id else "unknown_case"
    attachment_type = instance.attachment_type or "other"

    # Include year/month folders for better scaling
    date_path = timezone.now().strftime("%Y/%m")

    # Sanitize filename
    base, ext = os.path.splitext(filename)
    safe_base = base.replace(" ", "_").replace("/", "_")

    return f"medical_attachments/case_{case_id}/{attachment_type}/{date_path}/{safe_base}{ext}"


class MedicalAttachment(models.Model):
    """
    Medical file attachments for cases (X-rays, lab reports, photos, etc.)
    """

    class AttachmentType(models.TextChoices):
        XRAY = "xray", "Ảnh chụp X-quang"
        CT_SCAN = "ct_scan", "Ảnh chụp CT"
        MRI = "mri", "Ảnh chụp MRI"
        ULTRASOUND = "ultrasound", "Ảnh siêu âm"
        ECG = "ecg", "Điện tim đồ"
        LAB_REPORT = "lab_report", "Phiếu xét nghiệm"
        BLOOD_TEST = "blood_test", "Kết quả xét nghiệm máu"
        URINE_TEST = "urine_test", "Kết quả xét nghiệm nước tiểu"
        PATHOLOGY = "pathology", "Kết quả giải phẫu bệnh"
        INJURY_PHOTO = "injury_photo", "Ảnh chụp chấn thương"
        SURGICAL_PHOTO = "surgical_photo", "Ảnh phẫu thuật"
        ENDOSCOPY = "endoscopy", "Ảnh nội soi"
        PRESCRIPTION = "prescription", "Đơn thuốc"
        DISCHARGE_SUMMARY = "discharge_summary", "Tóm tắt xuất viện"
        CONSENT_FORM = "consent_form", "Phiếu đồng ý"
        OTHER = "other", "Khác"

    """
    Medical file attachments for cases (X-rays, lab reports, photos, etc.)
    """

    class ConfidentialityLevel(models.TextChoices):
        PUBLIC = "public", "Public (all collaborators)"
        CONFIDENTIAL = "confidential", "Confidential (instructors + owner)"
        RESTRICTED = "restricted", "Restricted (owner + designated instructors)"
        DEPARTMENT = "department", "Department only"

    case = models.ForeignKey(
        "Case", on_delete=models.CASCADE, related_name="medical_attachments"
    )

    # File information
    file = models.FileField(
        upload_to=medical_attachment_upload_to, help_text="Tệp đính kèm y tế"
    )

    attachment_type = models.CharField(
        max_length=50, choices=AttachmentType.choices, help_text="Loại tệp đính kèm"
    )

    title = models.CharField(max_length=200, help_text="Tiêu đề mô tả tệp")

    description = models.TextField(blank=True, help_text="Mô tả chi tiết về tệp")

    # Medical context
    date_taken = models.DateTimeField(
        null=True, blank=True, help_text="Ngày chụp/thực hiện"
    )

    department = models.ForeignKey(
        "Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Khoa thực hiện",
    )

    physician_notes = models.TextField(blank=True, help_text="Ghi chú của bác sĩ")

    # File metadata
    file_size = models.BigIntegerField(
        null=True, blank=True, help_text="Kích thước tệp (bytes)"
    )

    file_type = models.CharField(
        max_length=200, blank=True, help_text="Loại tệp (MIME type)"
    )

    # Timestamps
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Access control
    is_confidential = models.BooleanField(default=False, help_text="Đánh dấu tệp là bảo mật")
    confidentiality_level = models.CharField(
        max_length=50,
        choices=ConfidentialityLevel.choices,
        default=ConfidentialityLevel.PUBLIC,
        help_text="Mức độ bảo mật của tệp",
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="uploaded_attachments",
        help_text="Người tải lên",
    )

    allowed_instructors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        limit_choices_to={"role": "instructor"},
        blank=True,
        related_name="restricted_attachments",
    )

    class Meta:
        db_table = "cases_medicalattachment"
        verbose_name = "Medical Attachment"
        verbose_name_plural = "Medical Attachments"
        ordering = ["-uploaded_at"]
        indexes = [
            models.Index(fields=["case", "attachment_type"]),
            models.Index(fields=["uploaded_at"]),
            models.Index(fields=["attachment_type"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.get_attachment_type_display()}"

    # def save(self, *args, **kwargs):
    #     # Trigger validation automatically
    #     self.full_clean()
    #     super().save(*args, **kwargs)

    # @property
    # def file_size_mb(self):
    #     """Return file size in MB"""
    #     if self.file_size:
    #         return round(self.file_size / (1024 * 1024), 2)
    #     return 0

    # @property
    # def is_image(self):
    #     """Check if the file is an image"""
    #     image_types = [
    #         "image/jpeg",
    #         "image/png",
    #         "image/gif",
    #         "image/bmp",
    #         "image/tiff",
    #     ]
    #     return self.file_type in image_types

    # @property
    # def is_pdf(self):
    #     """Check if the file is a PDF"""
    #     return self.file_type == "application/pdf"
    # --- Core validation logic ---
    ALLOWED_FILE_TYPES = {
        "application/pdf": "PDF",
        "image/jpeg": "JPG",
        "image/png": "PNG",
        "application/dicom": "DICOM",
        "application/msword": "DOC",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "DOCX",
    }
    MAX_FILE_SIZE_MB = 50

    def clean(self):
        """
        Runs file validation before saving.
        """
        if not self.file:
            return

        # File size check
        if self.file.size > self.MAX_FILE_SIZE_MB * 1024 * 1024:
            raise ValidationError(f"File exceeds {self.MAX_FILE_SIZE_MB} MB limit.")

        # Read a small chunk to detect type
        file_header = self.file.read(2048)
        mime_type = magic.from_buffer(file_header, mime=True)
        self.file.seek(0)

        # Check if MIME type is allowed
        allowed_types = list(self.ALLOWED_FILE_TYPES.keys()) + ["text/plain"]
        if mime_type not in allowed_types:
            raise ValidationError(f"Unsupported or invalid file type: {mime_type}")

        # Store metadata
        self.file_size = self.file.size
        self.file_type = mime_type

    def save(self, *args, **kwargs):
        # Trigger validation automatically
        self.full_clean()
        super().save(*args, **kwargs)


class StudentNotes(models.Model):
    """
    Student's clinical reasoning and learning notes for a case
    Helps track student's thought process and understanding
    """

    case = models.ForeignKey(
        "Case", on_delete=models.CASCADE, related_name="student_notes"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="my_case_notes",
        limit_choices_to={"role": "student"},
        help_text="Student who created these notes",
    )

    # Clinical Reasoning
    clinical_assessment = models.TextField(
        blank=True, help_text="Student's initial clinical assessment and key findings"
    )
    differential_diagnosis = models.TextField(
        blank=True, help_text="Student's differential diagnosis list with reasoning"
    )
    treatment_plan = models.TextField(
        blank=True,
        help_text="Student's proposed treatment plan and management strategy",
    )

    # Learning Reflections
    learning_reflections = models.TextField(
        blank=True, help_text="What the student learned from this case"
    )
    questions_for_instructor = models.TextField(
        blank=True, help_text="Questions or areas where the student needs clarification"
    )
    challenges_faced = models.TextField(
        blank=True, help_text="Challenges or difficulties encountered during the case"
    )
    resources_used = models.TextField(
        blank=True, help_text="References, textbooks, or resources consulted"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_submitted = models.BooleanField(
        default=False,
        help_text="Whether these notes have been submitted for instructor review",
    )
    submitted_at = models.DateTimeField(
        null=True, blank=True, help_text="When the notes were submitted"
    )

    class Meta:
        db_table = "cases_studentnotes"
        verbose_name = "Student Notes"
        verbose_name_plural = "Student Notes"
        ordering = ["-updated_at"]
        unique_together = [["case", "student"]]  # One set of notes per student per case

    def __str__(self):
        return f"Notes by {self.student.get_full_name()} for {self.case.title}"

    @property
    def has_clinical_assessment(self):
        """Check if clinical assessment has been completed"""
        return bool(self.clinical_assessment.strip())

    @property
    def has_differential_diagnosis(self):
        """Check if differential diagnosis has been completed"""
        return bool(self.differential_diagnosis.strip())

    @property
    def has_treatment_plan(self):
        """Check if treatment plan has been completed"""
        return bool(self.treatment_plan.strip())

    @property
    def completion_percentage(self):
        """Calculate completion percentage of notes"""
        total_fields = 7  # clinical_assessment, differential_diagnosis, treatment_plan, learning_reflections, questions, challenges, resources
        completed = sum(
            [
                bool(self.clinical_assessment.strip()),
                bool(self.differential_diagnosis.strip()),
                bool(self.treatment_plan.strip()),
                bool(self.learning_reflections.strip()),
                bool(self.questions_for_instructor.strip()),
                bool(self.challenges_faced.strip()),
                bool(self.resources_used.strip()),
            ]
        )
        return int((completed / total_fields) * 100)
