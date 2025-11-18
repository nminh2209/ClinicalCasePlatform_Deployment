"""
Populate initial validation rules and medical terminology
Run this after migrations to set up the validation system
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinical_case_platform.settings')
django.setup()

from cases.validation import CaseValidationRule, MedicalTerminologyCheck
from accounts.models import User


def create_validation_rules():
    """Create initial validation rules"""
    print("Creating validation rules...")
    
    # Get admin user for created_by
    admin = User.objects.filter(role='admin').first()
    if not admin:
        admin = User.objects.filter(is_superuser=True).first()
    
    rules = [
        # Required Fields
        {
            'name': 'Yêu cầu tiêu đề ca bệnh',
            'rule_type': 'required_field',
            'severity': 'error',
            'target_field': 'title',
            'rule_config': {},
            'error_message_vi': 'Tiêu đề ca bệnh là bắt buộc',
            'help_text': 'Vui lòng nhập tiêu đề mô tả ngắn gọn ca bệnh',
        },
        {
            'name': 'Yêu cầu lý do khám',
            'rule_type': 'required_field',
            'severity': 'error',
            'target_field': 'clinical_history.chief_complaint',
            'rule_config': {},
            'error_message_vi': 'Lý do khám là bắt buộc',
            'help_text': 'Vui lòng nhập lý do chính bệnh nhân đến khám',
        },
        {
            'name': 'Yêu cầu tiền sử bệnh hiện tại',
            'rule_type': 'required_field',
            'severity': 'error',
            'target_field': 'clinical_history.history_present_illness',
            'rule_config': {},
            'error_message_vi': 'Tiền sử bệnh hiện tại là bắt buộc',
            'help_text': 'Vui lòng mô tả chi tiết tiền sử bệnh hiện tại',
        },
        {
            'name': 'Yêu cầu dấu hiệu sinh tồn',
            'rule_type': 'required_field',
            'severity': 'error',
            'target_field': 'physical_examination.vital_signs',
            'rule_config': {},
            'error_message_vi': 'Dấu hiệu sinh tồn là bắt buộc',
            'help_text': 'Vui lòng ghi nhận các dấu hiệu sinh tồn',
        },
        {
            'name': 'Yêu cầu chẩn đoán chính',
            'rule_type': 'required_field',
            'severity': 'error',
            'target_field': 'diagnosis_management.primary_diagnosis',
            'rule_config': {},
            'error_message_vi': 'Chẩn đoán chính là bắt buộc',
            'help_text': 'Vui lòng nhập chẩn đoán chính cho ca bệnh',
        },
        {
            'name': 'Yêu cầu kế hoạch điều trị',
            'rule_type': 'required_field',
            'severity': 'error',
            'target_field': 'diagnosis_management.treatment_plan',
            'rule_config': {},
            'error_message_vi': 'Kế hoạch điều trị là bắt buộc',
            'help_text': 'Vui lòng mô tả kế hoạch điều trị cho bệnh nhân',
        },
        {
            'name': 'Yêu cầu mục tiêu học tập',
            'rule_type': 'learning_objective',
            'severity': 'error',
            'target_field': 'learning_outcomes.learning_objectives',
            'rule_config': {},
            'error_message_vi': 'Mục tiêu học tập là bắt buộc',
            'help_text': 'Vui lòng xác định mục tiêu học tập cho ca bệnh này',
        },
        
        # Minimum Length Requirements
        {
            'name': 'Độ dài tối thiểu tiêu đề',
            'rule_type': 'min_length',
            'severity': 'warning',
            'target_field': 'title',
            'rule_config': {'min_length': 10},
            'error_message_vi': 'Tiêu đề quá ngắn (tối thiểu {min_length} ký tự)',
            'help_text': 'Tiêu đề nên mô tả rõ ràng ca bệnh',
        },
        {
            'name': 'Độ dài tối thiểu lý do khám',
            'rule_type': 'min_length',
            'severity': 'warning',
            'target_field': 'clinical_history.chief_complaint',
            'rule_config': {'min_length': 20},
            'error_message_vi': 'Lý do khám quá ngắn (tối thiểu {min_length} ký tự)',
            'help_text': 'Lý do khám nên chi tiết và rõ ràng',
        },
        {
            'name': 'Độ dài tối thiểu tiền sử bệnh',
            'rule_type': 'min_length',
            'severity': 'warning',
            'target_field': 'clinical_history.history_present_illness',
            'rule_config': {'min_length': 50},
            'error_message_vi': 'Tiền sử bệnh quá ngắn (tối thiểu {min_length} ký tự)',
            'help_text': 'Tiền sử bệnh nên mô tả đầy đủ diễn biến',
        },
        {
            'name': 'Độ dài tối thiểu chẩn đoán',
            'rule_type': 'min_length',
            'severity': 'warning',
            'target_field': 'diagnosis_management.primary_diagnosis',
            'rule_config': {'min_length': 10},
            'error_message_vi': 'Chẩn đoán quá ngắn (tối thiểu {min_length} ký tự)',
            'help_text': 'Chẩn đoán nên chi tiết và chính xác',
        },
        {
            'name': 'Độ dài tối thiểu kế hoạch điều trị',
            'rule_type': 'min_length',
            'severity': 'warning',
            'target_field': 'diagnosis_management.treatment_plan',
            'rule_config': {'min_length': 30},
            'error_message_vi': 'Kế hoạch điều trị quá ngắn (tối thiểu {min_length} ký tự)',
            'help_text': 'Kế hoạch điều trị nên chi tiết và đầy đủ',
        },
        
        # Attachment Requirements
        {
            'name': 'Khuyến nghị tệp đính kèm',
            'rule_type': 'attachment_required',
            'severity': 'warning',
            'target_field': 'medical_attachments',
            'rule_config': {},
            'error_message_vi': 'Nên có ít nhất một tệp đính kèm (X-quang, xét nghiệm, v.v.)',
            'help_text': 'Tệp đính kèm giúp ca bệnh sinh động và thực tế hơn',
        },
    ]
    
    created_count = 0
    for rule_data in rules:
        rule, created = CaseValidationRule.objects.get_or_create(
            name=rule_data['name'],
            defaults={
                **rule_data,
                'created_by': admin,
                'is_active': True
            }
        )
        if created:
            created_count += 1
            print(f"  Created: {rule.name}")
    
    print(f"Created {created_count} validation rules")


def create_medical_terminology():
    """Create initial medical terminology"""
    print("\nCreating medical terminology...")
    
    terms = [
        # Common Diseases
        ('Diabetes Mellitus', 'Đái tháo đường', 'Disease', 'Bệnh chuyển hóa đường huyết', ['DM', 'Tiểu đường']),
        ('Hypertension', 'Tăng huyết áp', 'Disease', 'Huyết áp cao kéo dài', ['HTN', 'Cao huyết áp']),
        ('Pneumonia', 'Viêm phổi', 'Disease', 'Nhiễm trùng phổi', ['Lung infection']),
        ('Myocardial Infarction', 'Nhồi máu cơ tim', 'Disease', 'Thiếu máu cục bộ cơ tim', ['MI', 'Heart attack']),
        ('Stroke', 'Đột quỵ', 'Disease', 'Tai biến mạch máu não', ['CVA', 'Cerebrovascular accident']),
        ('Asthma', 'Hen phế quản', 'Disease', 'Bệnh viêm đường thở mạn tính', ['Bronchial asthma']),
        ('COPD', 'Bệnh phổi tắc nghẽn mạn tính', 'Disease', 'Tắc nghẽn đường thở không hồi phục', ['Chronic obstructive pulmonary disease']),
        ('Tuberculosis', 'Lao phổi', 'Disease', 'Nhiễm trùng do vi khuẩn lao', ['TB', 'Phthisis']),
        
        # Symptoms
        ('Dyspnea', 'Khó thở', 'Symptom', 'Cảm giác thiếu không khí', ['Shortness of breath']),
        ('Chest Pain', 'Đau ngực', 'Symptom', 'Đau vùng ngực', ['Thoracic pain']),
        ('Fever', 'Sốt', 'Symptom', 'Nhiệt độ cơ thể tăng cao', ['Pyrexia']),
        ('Cough', 'Ho', 'Symptom', 'Phản xạ đẩy dị vật ra khỏi đường thở', ['Tussis']),
        ('Headache', 'Đau đầu', 'Symptom', 'Đau vùng đầu', ['Cephalgia']),
        ('Nausea', 'Buồn nôn', 'Symptom', 'Cảm giác muốn nôn', []),
        ('Vomiting', 'Nôn', 'Symptom', 'Đẩy thức ăn ra ngoài qua miệng', ['Emesis']),
        ('Diarrhea', 'Tiêu chảy', 'Symptom', 'Phân lỏng nhiều lần', []),
        
        # Anatomy
        ('Heart', 'Tim', 'Anatomy', 'Cơ quan bơm máu', ['Cardiac']),
        ('Lung', 'Phổi', 'Anatomy', 'Cơ quan hô hấp', ['Pulmonary']),
        ('Liver', 'Gan', 'Anatomy', 'Cơ quan chuyển hóa', ['Hepatic']),
        ('Kidney', 'Thận', 'Anatomy', 'Cơ quan lọc máu', ['Renal']),
        ('Brain', 'Não', 'Anatomy', 'Cơ quan thần kinh trung ương', ['Cerebral']),
        ('Stomach', 'Dạ dày', 'Anatomy', 'Cơ quan tiêu hóa', ['Gastric']),
        
        # Procedures
        ('X-ray', 'Chụp X-quang', 'Procedure', 'Chẩn đoán hình ảnh bằng tia X', ['Radiography']),
        ('CT Scan', 'Chụp CT', 'Procedure', 'Chụp cắt lớp vi tính', ['Computed Tomography']),
        ('MRI', 'Chụp cộng hưởng từ', 'Procedure', 'Chẩn đoán hình ảnh bằng từ trường', ['Magnetic Resonance Imaging']),
        ('Ultrasound', 'Siêu âm', 'Procedure', 'Chẩn đoán hình ảnh bằng sóng âm', ['Sonography']),
        ('ECG', 'Điện tim', 'Procedure', 'Ghi nhận hoạt động điện của tim', ['Electrocardiogram', 'EKG']),
        ('Blood Test', 'Xét nghiệm máu', 'Procedure', 'Phân tích mẫu máu', ['Hematology']),
        
        # Medications
        ('Antibiotic', 'Kháng sinh', 'Medication', 'Thuốc diệt vi khuẩn', ['Antimicrobial']),
        ('Analgesic', 'Thuốc giảm đau', 'Medication', 'Thuốc làm giảm cơn đau', ['Painkiller']),
        ('Antipyretic', 'Thuốc hạ sốt', 'Medication', 'Thuốc làm giảm nhiệt độ', ['Fever reducer']),
        ('Antihypertensive', 'Thuốc hạ huyết áp', 'Medication', 'Thuốc điều trị tăng huyết áp', []),
        ('Insulin', 'Insulin', 'Medication', 'Hormone điều hòa đường huyết', []),
    ]
    
    created_count = 0
    for term, vietnamese, category, definition, synonyms in terms:
        terminology, created = MedicalTerminologyCheck.objects.get_or_create(
            term=term,
            defaults={
                'vietnamese_term': vietnamese,
                'category': category,
                'definition': definition,
                'synonyms': synonyms,
                'is_approved': True,
                'requires_context': False
            }
        )
        if created:
            created_count += 1
            print(f"  Created: {term} ({vietnamese})")
    
    print(f"Created {created_count} medical terms")


def main():
    print("=" * 60)
    print("Populating Validation Data")
    print("=" * 60)
    
    create_validation_rules()
    create_medical_terminology()
    
    print("\n" + "=" * 60)
    print("Validation data population completed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run migrations: python manage.py migrate")
    print("2. Generate analytics: python manage.py generate_analytics --period daily")
    print("3. Validate cases: python manage.py validate_cases --all")
    print("\nSee ANALYTICS_VALIDATION_SETUP.md for detailed documentation")


if __name__ == '__main__':
    main()
