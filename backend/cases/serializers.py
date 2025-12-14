from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Case, CasePermission, GuestAccess, CaseGroup, PermissionAuditLog
from .medical_models import (
    Department,
    ClinicalHistory,
    PhysicalExamination,
    Investigations,
    DiagnosisManagement,
    LearningOutcomes,
    MedicalAttachment,
    StudentNotes,
    MedicalTerm,
    ICD10Code,
    MedicalAbbreviation,
)
from accounts.serializers import UserSerializer
from accounts.models import User

# from templates.models import CaseTemplate
from repositories.models import Repository


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model"""

    class Meta:  # type: ignore[misc, assignment]
        model = Department
        fields = ["id", "name", "vietnamese_name", "code", "description", "is_active"]


class ClinicalHistorySerializer(serializers.ModelSerializer):
    """Serializer for Clinical History model"""

    class Meta:  # type: ignore[misc, assignment]
        model = ClinicalHistory
        fields = [
            "id",
            "chief_complaint",
            "history_present_illness",
            "symptom_duration_days",
            "symptom_onset",
            "symptom_progression",
            "past_medical_history",
            "family_history",
            "social_history",
            "allergies",
            "medications",
            "review_systems",
        ]
        extra_kwargs = {
            "history_present_illness": {"required": False},
            "symptom_duration_days": {"required": False},
            "symptom_onset": {"required": False},
            "symptom_progression": {"required": False},
            "past_medical_history": {"required": False},
            "family_history": {"required": False},
            "social_history": {"required": False},
            "allergies": {"required": False},
            "medications": {"required": False},
            "review_systems": {"required": False},
        }


class PhysicalExaminationSerializer(serializers.ModelSerializer):
    """Serializer for Physical Examination model"""

    class Meta:  # type: ignore[misc, assignment]
        model = PhysicalExamination
        fields = [
            "id",
            "general_appearance",
            "consciousness_level",
            "vital_signs",
            "vital_signs_bp",
            "vital_signs_hr",
            "vital_signs_rr",
            "vital_signs_temp",
            "vital_signs_spo2",
            "height_cm",
            "weight_kg",
            "bmi",
            "head_neck",
            "cardiovascular",
            "respiratory",
            "abdominal",
            "neurological",
            "musculoskeletal",
            "skin",
            "other_systems",
        ]
        extra_kwargs = {
            "general_appearance": {"required": False},
            "consciousness_level": {"required": False},
            "vital_signs": {"required": False},
            "vital_signs_bp": {"required": False},
            "vital_signs_hr": {"required": False},
            "vital_signs_rr": {"required": False},
            "vital_signs_temp": {"required": False},
            "vital_signs_spo2": {"required": False},
            "height_cm": {"required": False},
            "weight_kg": {"required": False},
            "bmi": {"required": False},
            "head_neck": {"required": False},
            "cardiovascular": {"required": False},
            "respiratory": {"required": False},
            "abdominal": {"required": False},
            "neurological": {"required": False},
            "musculoskeletal": {"required": False},
            "skin": {"required": False},
            "other_systems": {"required": False},
        }


class InvestigationsSerializer(serializers.ModelSerializer):
    """Serializer for Investigations model"""

    class Meta:  # type: ignore[misc, assignment]
        model = Investigations
        fields = [
            "id",
            "laboratory_results",
            "hemoglobin_level",
            "white_cell_count",
            "platelet_count",
            "sodium_level",
            "potassium_level",
            "glucose_level",
            "creatinine_level",
            "imaging_studies",
            "ecg_findings",
            "ecg_rhythm",
            "ecg_rate",
            "pathology_results",
            "microbiology_results",
            "other_investigations",
            "arterial_blood_gas",
            "ph_level",
            "special_tests",
            "microbiology",
            "biochemistry",
            "hematology",
        ]
        extra_kwargs = {
            "laboratory_results": {"required": False},
            "hemoglobin_level": {"required": False},
            "white_cell_count": {"required": False},
            "platelet_count": {"required": False},
            "sodium_level": {"required": False},
            "potassium_level": {"required": False},
            "glucose_level": {"required": False},
            "creatinine_level": {"required": False},
            "imaging_studies": {"required": False},
            "ecg_findings": {"required": False},
            "ecg_rhythm": {"required": False},
            "ecg_rate": {"required": False},
            "pathology_results": {"required": False},
            "microbiology_results": {"required": False},
            "other_investigations": {"required": False},
            "arterial_blood_gas": {"required": False},
            "ph_level": {"required": False},
            "special_tests": {"required": False},
            "microbiology": {"required": False},
            "biochemistry": {"required": False},
            "hematology": {"required": False},
        }


class DiagnosisManagementSerializer(serializers.ModelSerializer):
    """Serializer for Diagnosis and Management model"""

    class Meta:  # type: ignore[misc, assignment]
        model = DiagnosisManagement
        fields = [
            "id",
            "primary_diagnosis",
            "differential_diagnosis",
            "icd10_codes",
            "treatment_plan",
            "medications_prescribed",
            "procedures_performed",
            "follow_up_plan",
            "prognosis",
            "complications",
        ]
        extra_kwargs = {
            "primary_diagnosis": {"required": False},
            "differential_diagnosis": {"required": False},
            "icd10_codes": {"required": False},
            "treatment_plan": {"required": False},
            "medications_prescribed": {"required": False},
            "procedures_performed": {"required": False},
            "follow_up_plan": {"required": False},
            "prognosis": {"required": False},
            "complications": {"required": False},
        }


class LearningOutcomesSerializer(serializers.ModelSerializer):
    """Serializer for Learning Outcomes model"""

    class Meta:  # type: ignore[misc, assignment]
        model = LearningOutcomes
        fields = [
            "id",
            "learning_objectives",
            "key_concepts",
            "clinical_pearls",
            "references",
            "discussion_points",
            "assessment_criteria",
        ]
        extra_kwargs = {
            "learning_objectives": {"required": False},
            "key_concepts": {"required": False},
            "clinical_pearls": {"required": False},
            "references": {"required": False},
            "discussion_points": {"required": False},
            "assessment_criteria": {"required": False},
        }


class CaseListSerializer(serializers.ModelSerializer):
    """
    Serializer for case list view (minimal data)
    """

    student_name = serializers.CharField(source="student.get_full_name", read_only=True)
    created_by_name = serializers.CharField(
        source="student.get_full_name", read_only=True
    )
    created_by_id = serializers.IntegerField(source="student.id", read_only=True)
    student_department = serializers.CharField(
        source="student.department.name", read_only=True
    )
    student_department_vietnamese = serializers.CharField(
        source="student.department.vietnamese_name", read_only=True
    )
    template_name = serializers.CharField(source="template.name", read_only=True)
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:  # type: ignore[misc, assignment]
        model = Case
        fields = [
            "id",
            "title",
            "student_name",
            "created_by_name",
            "created_by_id",
            "student_department",
            "student_department_vietnamese",
            "template_name",
            "specialty",
            "case_status",
            "comment_count",
            "created_at",
            "updated_at",
            "submitted_at",
            "reviewed_at",
            # Patient information fields added for list view
            "patient_name",
            "patient_age",
            "patient_gender",
            "medical_record_number",
            "admission_date",
            "discharge_date",
        ]


class MedicalAttachmentSerializer(serializers.ModelSerializer):
    """Serializer for Medical Attachments"""

    uploaded_by_name = serializers.CharField(
        source="uploaded_by.get_full_name", read_only=True
    )
    department_name = serializers.CharField(source="department.name", read_only=True)
    attachment_type_display = serializers.CharField(
        source="get_attachment_type_display", read_only=True
    )
    case = serializers.PrimaryKeyRelatedField(read_only=True)  # Optional, for clarity

    allowed_instructors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.filter(role="instructor"),
        required=False,
    )

    class Meta:  # type: ignore[misc, assignment]
        model = MedicalAttachment
        fields = [
            "id",
            "case",
            "file",
            "attachment_type",
            "attachment_type_display",
            "title",
            "description",
            "date_taken",
            "department",
            "department_name",
            "physician_notes",
            "file_size",
            "file_type",
            "uploaded_at",
            "updated_at",
            "confidentiality_level",
            "uploaded_by",
            "uploaded_by_name",
            "allowed_instructors",
        ]
        read_only_fields = [
            "uploaded_by",
            "file_size",
            "file_type",
            "uploaded_at",
            "updated_at",
            "case",
        ]

    def validate_file(self, file):
        """Optional lightweight validation for API feedback"""
        max_size = 50 * 1024 * 1024  # 50 MB
        if file.size > max_size:
            raise serializers.ValidationError("File exceeds 50 MB limit.")
        allowed_types = [
            "application/pdf",
            "image/jpeg",
            "image/png",
            "application/dicom",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ]
        if hasattr(file, "content_type") and file.content_type not in allowed_types:
            raise serializers.ValidationError("Unsupported file type.")
        return file

    def create(self, validated_data):
        allowed_instructors = validated_data.pop("allowed_instructors", [])
        validated_data["uploaded_by"] = self.context["request"].user
        attachment = super().create(validated_data)
        if allowed_instructors:
            attachment.allowed_instructors.set(allowed_instructors)
        return attachment

    def update(self, instance, validated_data):
        allowed_instructors = validated_data.pop("allowed_instructors", None)
        attachment = super().update(instance, validated_data)
        if allowed_instructors is not None:
            attachment.allowed_instructors.set(allowed_instructors)
        return attachment


class CaseDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed case view with all medical sections
    """

    student = UserSerializer(read_only=True)
    template_name = serializers.CharField(source="template.name", read_only=True)
    repository_name = serializers.CharField(source="repository.name", read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    has_grade = serializers.BooleanField(read_only=True)

    # Medical sections
    clinical_history = ClinicalHistorySerializer(read_only=True)
    physical_examination = PhysicalExaminationSerializer(read_only=True)
    detailed_investigations = InvestigationsSerializer(
        source="investigations_detail", read_only=True
    )
    diagnosis_management = DiagnosisManagementSerializer(read_only=True)
    learning_outcomes = LearningOutcomesSerializer(read_only=True)

    # Medical attachments
    medical_attachments = MedicalAttachmentSerializer(many=True, read_only=True)

    class Meta:  # type: ignore[misc, assignment]
        model = Case
        fields = [
            "id",
            "title",
            "student",
            "template",
            "template_name",
            "repository",
            "repository_name",
            "patient_name",
            "patient_age",
            "patient_gender",
            "patient_ethnicity",
            "patient_occupation",
            "medical_record_number",
            "admission_date",
            "discharge_date",
            "chief_complaint_brief",
            "case_summary",
            "specialty",
            "keywords",
            "learning_tags",
            "priority_level",
            "complexity_level",
            "estimated_study_hours",
            "requires_follow_up",
            "follow_up_date",
            "case_status",
            "comment_count",
            "has_grade",
            "created_at",
            "updated_at",
            "submitted_at",
            "reviewed_at",
            # New detailed medical sections
            "clinical_history",
            "physical_examination",
            "detailed_investigations",
            "diagnosis_management",
            "learning_outcomes",
            "medical_attachments",
        ]


class CaseCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating cases with detailed medical sections
    """

    clinical_history = ClinicalHistorySerializer(required=False)
    physical_examination = PhysicalExaminationSerializer(required=False)
    detailed_investigations = InvestigationsSerializer(required=False)
    diagnosis_management = DiagnosisManagementSerializer(required=False)
    learning_outcomes = LearningOutcomesSerializer(required=False)

    class Meta:  # type: ignore[misc, assignment]
        model = Case
        fields = [
            "title",
            "template",
            "repository",
            "patient_name",
            "patient_age",
            "patient_gender",
            "patient_ethnicity",
            "patient_occupation",
            "medical_record_number",
            "admission_date",
            "discharge_date",
            "chief_complaint_brief",
            "case_summary",
            "specialty",
            "keywords",
            "learning_tags",
            "priority_level",
            "complexity_level",
            "estimated_study_hours",
            "requires_follow_up",
            "follow_up_date",
            "case_status",
            # New detailed medical sections
            "clinical_history",
            "physical_examination",
            "detailed_investigations",
            "diagnosis_management",
            "learning_outcomes",
        ]

    def create(self, validated_data):
        # Extract detailed medical sections
        clinical_history_data = validated_data.pop("clinical_history", None)
        physical_examination_data = validated_data.pop("physical_examination", None)
        investigations_data = validated_data.pop("detailed_investigations", None)
        diagnosis_management_data = validated_data.pop("diagnosis_management", None)
        learning_outcomes_data = validated_data.pop("learning_outcomes", None)

        # Set the student to the current user
        validated_data["student"] = self.context["request"].user

        # Auto-public for instructor cases
        user = self.context["request"].user
        if hasattr(user, "is_instructor") and user.is_instructor:
            validated_data["is_public"] = True

        # Create the case
        case = super().create(validated_data)

        # ALWAYS create detailed medical sections (even if empty) so they exist for later editing
        # This ensures the serializer returns objects instead of null
        ClinicalHistory.objects.create(
            case=case, 
            **(clinical_history_data or {})
        )

        PhysicalExamination.objects.create(
            case=case, 
            **(physical_examination_data or {})
        )

        Investigations.objects.create(
            case=case, 
            **(investigations_data or {})
        )

        DiagnosisManagement.objects.create(
            case=case, 
            **(diagnosis_management_data or {})
        )

        LearningOutcomes.objects.create(
            case=case, 
            **(learning_outcomes_data or {})
        )

        return case

    def update(self, instance, validated_data):
        # Extract detailed medical sections
        clinical_history_data = validated_data.pop("clinical_history", None)
        physical_examination_data = validated_data.pop("physical_examination", None)
        investigations_data = validated_data.pop("detailed_investigations", None)
        diagnosis_management_data = validated_data.pop("diagnosis_management", None)
        learning_outcomes_data = validated_data.pop("learning_outcomes", None)

        # Update the case
        instance = super().update(instance, validated_data)

        # Update or create detailed medical sections
        if clinical_history_data:
            ClinicalHistory.objects.update_or_create(
                case=instance, defaults=clinical_history_data
            )

        if physical_examination_data:
            PhysicalExamination.objects.update_or_create(
                case=instance, defaults=physical_examination_data
            )

        if investigations_data:
            Investigations.objects.update_or_create(
                case=instance, defaults=investigations_data
            )

        if diagnosis_management_data:
            DiagnosisManagement.objects.update_or_create(
                case=instance, defaults=diagnosis_management_data
            )

        if learning_outcomes_data:
            LearningOutcomes.objects.update_or_create(
                case=instance, defaults=learning_outcomes_data
            )

        return instance

    def validate_template(self, value):
        if value and not value.is_active:
            raise serializers.ValidationError("Selected template is not active")
        return value

    def validate_repository(self, value):
        if not value:
            # If no repository provided, get the first public repository
            try:
                value = Repository.objects.filter(is_public=True).first()
                if not value:
                    raise serializers.ValidationError("No public repository available")
            except Repository.DoesNotExist:
                raise serializers.ValidationError("No repository available")

        user = self.context["request"].user
        if value.owner != user and not value.is_public:
            raise serializers.ValidationError(
                "You don't have access to this repository"
            )
        return value
        return value


class CasePermissionSerializer(serializers.ModelSerializer):
    """
    Enhanced serializer for case permissions with time-limited access and group sharing
    """

    user_name = serializers.CharField(source="user.get_full_name", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)
    granted_by_name = serializers.CharField(
        source="granted_by.get_full_name", read_only=True
    )
    department_name = serializers.CharField(
        source="target_department.name", read_only=True
    )
    is_expired = serializers.ReadOnlyField()

    # Validation fields
    expires_at_display = serializers.SerializerMethodField()
    share_description = serializers.SerializerMethodField()

    class Meta:  # type: ignore[misc, assignment]
        model = CasePermission
        fields = [
            "id",
            "case",
            "user",
            "user_name",
            "user_email",
            "share_type",
            "target_department",
            "department_name",
            "class_group",
            "permission_type",
            "granted_by",
            "granted_by_name",
            "granted_at",
            "expires_at",
            "expires_at_display",
            "is_active",
            "is_expired",
            "notes",
            "access_count",
            "last_accessed",
            "share_description",
        ]
        read_only_fields = [
            "case",
            "granted_by",
            "granted_at",
            "access_count",
            "last_accessed",
        ]

    def get_expires_at_display(self, obj):
        """Human-readable expiration time"""
        if not obj.expires_at:
            return "Không giới hạn"
        return obj.expires_at.strftime("%d/%m/%Y %H:%M")

    def get_share_description(self, obj):
        """Human-readable sharing description"""
        if obj.share_type == CasePermission.ShareTypeChoices.INDIVIDUAL:
            return f"Cá nhân: {obj.user.get_full_name() if obj.user else 'N/A'}"
        elif obj.share_type == CasePermission.ShareTypeChoices.DEPARTMENT:
            return f"Khoa: {obj.target_department.name if obj.target_department else 'N/A'}"
        elif obj.share_type == CasePermission.ShareTypeChoices.CLASS_GROUP:
            return f"Lớp: {obj.class_group}"
        elif obj.share_type == CasePermission.ShareTypeChoices.PUBLIC:
            return "Công khai"
        return obj.get_share_type_display()

    def validate(self, attrs):
        """Custom validation for permission logic"""
        share_type = attrs.get("share_type", CasePermission.ShareTypeChoices.INDIVIDUAL)

        # Validate individual sharing
        if share_type == CasePermission.ShareTypeChoices.INDIVIDUAL:
            if not attrs.get("user"):
                raise serializers.ValidationError(
                    {"user": "Bắt buộc phải chọn người dùng cho chia sẻ cá nhân"}
                )

        # Validate department sharing
        elif share_type == CasePermission.ShareTypeChoices.DEPARTMENT:
            if not attrs.get("target_department"):
                raise serializers.ValidationError(
                    {"target_department": "Bắt buộc phải chọn khoa cho chia sẻ khoa"}
                )
            attrs["user"] = None  # Clear user for department sharing

        # Validate class group sharing
        elif share_type == CasePermission.ShareTypeChoices.CLASS_GROUP:
            if not attrs.get("class_group"):
                raise serializers.ValidationError(
                    {"class_group": "Bắt buộc phải nhập mã lớp cho chia sẻ lớp"}
                )
            attrs["user"] = None  # Clear user for class sharing

        # Public sharing doesn't need specific target
        elif share_type == CasePermission.ShareTypeChoices.PUBLIC:
            attrs["user"] = None
            attrs["target_department"] = None
            attrs["class_group"] = ""

        return attrs

    def create(self, validated_data):
        validated_data["granted_by"] = self.context["request"].user
        return super().create(validated_data)


class GuestAccessSerializer(serializers.ModelSerializer):
    """
    Serializer for guest access system
    """

    created_by_name = serializers.CharField(
        source="created_by.get_full_name", read_only=True
    )
    case_title = serializers.CharField(source="case.title", read_only=True)
    is_expired = serializers.ReadOnlyField()
    expires_at_display = serializers.SerializerMethodField()

    # Write-only field for setting expiration in hours
    expiration_hours = serializers.IntegerField(
        write_only=True, required=False, default=72
    )

    class Meta:  # type: ignore[misc, assignment]
        model = GuestAccess
        fields = [
            "id",
            "case",
            "case_title",
            "access_token",
            "guest_email",
            "guest_name",
            "permission_type",
            "created_by",
            "created_by_name",
            "created_at",
            "expires_at",
            "expires_at_display",
            "expiration_hours",
            "is_active",
            "is_expired",
            "access_count",
            "last_accessed",
            "accessed_ips",
        ]
        read_only_fields = [
            "case",
            "access_token",
            "created_by",
            "created_at",
            "expires_at",
            "access_count",
            "last_accessed",
            "accessed_ips",
        ]

    def get_expires_at_display(self, obj):
        """Human-readable expiration time"""
        return obj.expires_at.strftime("%d/%m/%Y %H:%M")

    def validate_guest_email(self, value):
        """Validate guest email format"""
        if not value:
            raise serializers.ValidationError("Email khách là bắt buộc")
        return value.lower()

    def create(self, validated_data):
        """Create guest access with auto-generated token and expiration"""
        import secrets
        from datetime import timedelta

        # Remove expiration_hours from validated_data
        expiration_hours = validated_data.pop("expiration_hours", 72)

        # Generate unique access token
        validated_data["access_token"] = secrets.token_urlsafe(32)

        # Set expiration time
        validated_data["expires_at"] = timezone.now() + timedelta(
            hours=expiration_hours
        )

        return super().create(validated_data)


class CaseGroupSerializer(serializers.ModelSerializer):
    """
    Serializer for case groups and bulk permission management
    """

    created_by_name = serializers.CharField(
        source="created_by.get_full_name", read_only=True
    )
    department_name = serializers.CharField(source="department.name", read_only=True)
    case_count = serializers.SerializerMethodField()
    cases_detail = serializers.SerializerMethodField()

    # Write-only fields for bulk operations
    add_cases_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        help_text="Danh sách ID ca bệnh để thêm vào nhóm",
    )
    remove_cases_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        help_text="Danh sách ID ca bệnh để loại khỏi nhóm",
    )

    class Meta:  # type: ignore[misc, assignment]
        model = CaseGroup
        fields = [
            "id",
            "name",
            "description",
            "group_type",
            "created_by",
            "created_by_name",
            "department",
            "department_name",
            "class_identifier",
            "is_active",
            "is_public",
            "created_at",
            "updated_at",
            "case_count",
            "cases_detail",
            "add_cases_ids",
            "remove_cases_ids",
        ]
        read_only_fields = ["created_by", "created_at", "updated_at"]

    def get_case_count(self, obj):
        """Get number of cases in group"""
        return obj.cases.count()

    def get_cases_detail(self, obj):
        """Get basic info about cases in group"""
        return [
            {
                "id": case.id,
                "title": case.title,
                "specialty": case.specialty,
                "complexity_level": case.get_complexity_level_display(),
            }
            for case in obj.cases.all()[:10]  # Limit to first 10 for performance
        ]

    def create(self, validated_data):
        """Create case group with bulk case operations"""
        add_cases_ids = validated_data.pop("add_cases_ids", [])
        remove_cases_ids = validated_data.pop("remove_cases_ids", [])

        validated_data["created_by"] = self.context["request"].user
        instance = super().create(validated_data)

        # Add cases to group
        if add_cases_ids:
            cases_to_add = Case.objects.filter(id__in=add_cases_ids)
            instance.cases.add(*cases_to_add)

        return instance


class MedicalTermSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore[misc, assignment]
        model = MedicalTerm
        fields = [
            "id",
            "term",
            "vietnamese_term",
            "english_term",
            "synonyms",
            "definition",
            "specialty",
            "is_active",
        ]


class ICD10Serializer(serializers.ModelSerializer):
    class Meta:  # type: ignore[misc, assignment]
        model = ICD10Code
        fields = [
            "id",
            "code",
            "description_en",
            "description_vi",
            "chapter",
            "category",
            "is_active",
        ]


class AbbreviationSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore[misc, assignment]
        model = MedicalAbbreviation
        fields = ["id", "abbr", "expansion", "description", "specialty", "is_active"]

    def update(self, instance, validated_data):
        """Update case group with bulk case operations"""
        add_cases_ids = validated_data.pop("add_cases_ids", [])
        remove_cases_ids = validated_data.pop("remove_cases_ids", [])

        instance = super().update(instance, validated_data)

        # Add new cases
        if add_cases_ids:
            cases_to_add = Case.objects.filter(id__in=add_cases_ids)
            instance.cases.add(*cases_to_add)

        # Remove cases
        if remove_cases_ids:
            cases_to_remove = Case.objects.filter(id__in=remove_cases_ids)
            instance.cases.remove(*cases_to_remove)

        return instance


class PermissionAuditLogSerializer(serializers.ModelSerializer):
    """
    Serializer for permission audit logs (read-only)
    """

    case_title = serializers.CharField(source="case.title", read_only=True)
    target_user_name = serializers.CharField(
        source="target_user.get_full_name", read_only=True
    )
    target_user_email = serializers.CharField(
        source="target_user.email", read_only=True
    )
    actor_user_name = serializers.CharField(
        source="actor_user.get_full_name", read_only=True
    )
    created_at_display = serializers.SerializerMethodField()

    class Meta:  # type: ignore[misc, assignment]
        model = PermissionAuditLog
        fields = [
            "id",
            "case",
            "case_title",
            "target_user",
            "target_user_name",
            "target_user_email",
            "actor_user",
            "actor_user_name",
            "action",
            "permission_type",
            "description",
            "ip_address",
            "user_agent",
            "additional_data",
            "created_at",
            "created_at_display",
        ]

    def get_created_at_display(self, obj):
        """Human-readable timestamp"""
        return obj.created_at.strftime("%d/%m/%Y %H:%M:%S")


class BulkPermissionSerializer(serializers.Serializer):
    """
    Serializer for bulk permission operations
    """

    cases_ids = serializers.ListField(
        child=serializers.IntegerField(), help_text="Danh sách ID ca bệnh"
    )
    users_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text="Danh sách ID người dùng (cho chia sẻ cá nhân)",
    )
    department_id = serializers.IntegerField(
        required=False, help_text="ID khoa (cho chia sẻ khoa)"
    )
    class_group = serializers.CharField(
        max_length=100, required=False, help_text="Mã lớp (cho chia sẻ lớp)"
    )
    permission_type = serializers.ChoiceField(
        choices=CasePermission.PermissionChoices.choices,
        default=CasePermission.PermissionChoices.VIEW,
    )
    share_type = serializers.ChoiceField(
        choices=CasePermission.ShareTypeChoices.choices,
        default=CasePermission.ShareTypeChoices.INDIVIDUAL,
    )
    expires_hours = serializers.IntegerField(
        required=False, help_text="Số giờ hết hạn (để trống nếu không giới hạn)"
    )
    notes = serializers.CharField(max_length=500, required=False, help_text="Ghi chú")

    def validate(self, attrs):
        """Validate bulk permission request"""
        share_type = attrs.get("share_type")

        if share_type == CasePermission.ShareTypeChoices.INDIVIDUAL:
            if not attrs.get("users_ids"):
                raise serializers.ValidationError(
                    {"users_ids": "Bắt buộc phải chọn người dùng cho chia sẻ cá nhân"}
                )
        elif share_type == CasePermission.ShareTypeChoices.DEPARTMENT:
            if not attrs.get("department_id"):
                raise serializers.ValidationError(
                    {"department_id": "Bắt buộc phải chọn khoa cho chia sẻ khoa"}
                )
        elif share_type == CasePermission.ShareTypeChoices.CLASS_GROUP:
            if not attrs.get("class_group"):
                raise serializers.ValidationError(
                    {"class_group": "Bắt buộc phải nhập mã lớp cho chia sẻ lớp"}
                )

        return attrs


class StudentNotesSerializer(serializers.ModelSerializer):
    """
    Serializer for student notes
    """

    student_name = serializers.CharField(source="student.get_full_name", read_only=True)
    completion_percentage = serializers.IntegerField(read_only=True)

    class Meta:  # type: ignore[misc, assignment]
        model = StudentNotes
        fields = [
            "id",
            "case",
            "student",
            "student_name",
            "clinical_assessment",
            "differential_diagnosis",
            "treatment_plan",
            "learning_reflections",
            "questions_for_instructor",
            "challenges_faced",
            "resources_used",
            "completion_percentage",
            "is_submitted",
            "submitted_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "case",
            "student",
            "submitted_at",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        validated_data["student"] = self.context["request"].user
        return super().create(validated_data)


class PublicFeedSerializer(serializers.ModelSerializer):
    """Serializer for cases in the public social feed"""

    student = serializers.SerializerMethodField()
    published_by = serializers.SerializerMethodField()
    reactions = serializers.SerializerMethodField()
    user_reaction = serializers.SerializerMethodField()
    comments_count = serializers.IntegerField(read_only=True)

    # Medical sections - use related serializers
    clinical_history = ClinicalHistorySerializer(read_only=True)
    physical_examination = PhysicalExaminationSerializer(read_only=True)
    detailed_investigations = InvestigationsSerializer(
        source="investigations_detail", read_only=True
    )
    diagnosis_management = DiagnosisManagementSerializer(read_only=True)
    learning_outcomes = LearningOutcomesSerializer(read_only=True)
    student_notes = StudentNotesSerializer(read_only=True)

    class Meta:  # type: ignore[misc, assignment]
        model = Case
        fields = [
            "id",
            "title",
            "student",
            "patient_name",
            "patient_age",
            "patient_gender",
            "medical_record_number",
            "admission_date",
            "discharge_date",
            "specialty",
            "keywords",
            "case_summary",
            "chief_complaint_brief",
            # Medical content sections
            "clinical_history",
            "physical_examination",
            "detailed_investigations",
            "diagnosis_management",
            "learning_outcomes",
            "student_notes",
            # Feed-specific fields
            "is_published_to_feed",
            "published_to_feed_at",
            "published_by",
            "feed_visibility",
            "is_featured",
            "reaction_count",
            "reactions",
            "user_reaction",
            "comments_count",
            "created_at",
            "updated_at",
        ]

    def get_student(self, obj):
        """Get student info including department"""
        if not obj.student:
            return None

        full_name = f"{obj.student.first_name} {obj.student.last_name}".strip()
        if not full_name:
            full_name = obj.student.username

        return {
            "id": obj.student.id,
            "username": obj.student.username,
            "full_name": full_name,
            "department_name": obj.student.department.name
            if obj.student.department
            else None,
        }

    def get_published_by(self, obj):
        """Get instructor who published this case"""
        if not obj.published_by:
            return None

        full_name = (
            f"{obj.published_by.first_name} {obj.published_by.last_name}".strip()
        )
        if not full_name:
            full_name = obj.published_by.username

        return {
            "id": obj.published_by.id,
            "username": obj.published_by.username,
            "full_name": full_name,
        }

    def get_reactions(self, obj):
        """Get reaction summary"""
        try:
            return obj.get_reaction_summary()
        except Exception:
            return {"like": 0, "love": 0, "insightful": 0, "learned": 0}

    def get_user_reaction(self, obj):
        """Get current user's reaction to this case"""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            from comments.models import Comment

            try:
                reaction = Comment.objects.filter(
                    case=obj, user=request.user, is_reaction=True
                ).first()
                return reaction.reaction_type if reaction else None
            except Exception:
                return None
        return None


class CaseSummarySerializer(serializers.Serializer):
    """
    Serializer for comprehensive case summary statistics
    Provides overview of all cases with analytics and metrics
    """

    total_cases = serializers.IntegerField()
    by_status = serializers.DictField()
    by_specialty = serializers.DictField()
    by_priority = serializers.DictField()
    by_complexity = serializers.DictField()
    completion_stats = serializers.DictField()
    recent_cases = CaseListSerializer(many=True)
    top_specialties = serializers.ListField()
    learning_metrics = serializers.DictField()
