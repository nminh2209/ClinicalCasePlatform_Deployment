"""
Script to create default export templates
Run with: python manage.py shell < create_system_templates.py
"""

from exports.models import ExportTemplate

print("Creating system export templates...")

# 1. Standard Medical Case Template
template1, created = ExportTemplate.objects.get_or_create(
    name="Standard Medical Case",
    defaults={
        "vietnamese_name": "Ca Bệnh Chuẩn",
        "description": "Complete case export with all sections for comprehensive documentation",
        "template_type": ExportTemplate.TemplateType.STANDARD,
        "is_system_template": True,
        "include_patient_details": True,
        "include_medical_history": True,
        "include_examination": True,
        "include_investigations": True,
        "include_diagnosis": True,
        "include_treatment": True,
        "include_learning_objectives": True,
        "include_comments": False,
        "include_attachments": True,
        "include_grades": False,
        "anonymize_patient": False,
        "add_watermark": False,
        "is_active": True,
    },
)
print(f"{'Created' if created else 'Found'}: {template1.name}")

# 2. Anonymized Template
template2, created = ExportTemplate.objects.get_or_create(
    name="Anonymized Case",
    defaults={
        "vietnamese_name": "Ca Bệnh Ẩn Danh",
        "description": "Case export with anonymized patient information for public sharing",
        "template_type": ExportTemplate.TemplateType.ANONYMIZED,
        "is_system_template": True,
        "include_patient_details": True,
        "include_medical_history": True,
        "include_examination": True,
        "include_investigations": True,
        "include_diagnosis": True,
        "include_treatment": True,
        "include_learning_objectives": True,
        "include_comments": False,
        "include_attachments": False,
        "include_grades": False,
        "anonymize_patient": True,
        "add_watermark": True,
        "watermark_text": "ANONYMIZED - FOR EDUCATIONAL USE ONLY",
        "is_active": True,
    },
)
print(f"{'Created' if created else 'Found'}: {template2.name}")

# 3. Academic/Teaching Template
template3, created = ExportTemplate.objects.get_or_create(
    name="Academic Teaching",
    defaults={
        "vietnamese_name": "Giảng Dạy / Học Thuật",
        "description": "Template optimized for teaching purposes with comments and feedback",
        "template_type": ExportTemplate.TemplateType.ACADEMIC,
        "is_system_template": True,
        "include_patient_details": True,
        "include_medical_history": True,
        "include_examination": True,
        "include_investigations": True,
        "include_diagnosis": True,
        "include_treatment": True,
        "include_learning_objectives": True,
        "include_comments": True,
        "include_attachments": True,
        "include_grades": False,
        "anonymize_patient": False,
        "add_watermark": False,
        "header_text": "Educational Material - For Academic Use",
        "is_active": True,
    },
)
print(f"{'Created' if created else 'Found'}: {template3.name}")

# 4. Research Template
template4, created = ExportTemplate.objects.get_or_create(
    name="Research Publication",
    defaults={
        "vietnamese_name": "Nghiên Cứu / Công Bố",
        "description": "Template for research papers and publications with anonymized data",
        "template_type": ExportTemplate.TemplateType.RESEARCH,
        "is_system_template": True,
        "include_patient_details": True,
        "include_medical_history": True,
        "include_examination": True,
        "include_investigations": True,
        "include_diagnosis": True,
        "include_treatment": True,
        "include_learning_objectives": False,
        "include_comments": False,
        "include_attachments": True,
        "include_grades": False,
        "anonymize_patient": True,
        "add_watermark": False,
        "is_active": True,
    },
)
print(f"{'Created' if created else 'Found'}: {template4.name}")

# 5. Clinical Documentation Template
template5, created = ExportTemplate.objects.get_or_create(
    name="Clinical Documentation",
    defaults={
        "vietnamese_name": "Hồ Sơ Lâm Sàng",
        "description": "Template for official clinical documentation with full patient details",
        "template_type": ExportTemplate.TemplateType.CLINICAL,
        "is_system_template": True,
        "include_patient_details": True,
        "include_medical_history": True,
        "include_examination": True,
        "include_investigations": True,
        "include_diagnosis": True,
        "include_treatment": True,
        "include_learning_objectives": False,
        "include_comments": True,
        "include_attachments": True,
        "include_grades": False,
        "anonymize_patient": False,
        "add_watermark": True,
        "watermark_text": "CONFIDENTIAL MEDICAL RECORD",
        "footer_text": "This document contains confidential patient information",
        "is_active": True,
    },
)
print(f"{'Created' if created else 'Found'}: {template5.name}")

# 6. Presentation Template
template6, created = ExportTemplate.objects.get_or_create(
    name="Presentation Format",
    defaults={
        "vietnamese_name": "Trình Bày / Thuyết Trình",
        "description": "Concise template for presentations and case discussions",
        "template_type": ExportTemplate.TemplateType.PRESENTATION,
        "is_system_template": True,
        "include_patient_details": True,
        "include_medical_history": True,
        "include_examination": True,
        "include_investigations": True,
        "include_diagnosis": True,
        "include_treatment": True,
        "include_learning_objectives": True,
        "include_comments": False,
        "include_attachments": False,
        "include_grades": False,
        "anonymize_patient": True,
        "add_watermark": False,
        "is_active": True,
    },
)
print(f"{'Created' if created else 'Found'}: {template6.name}")

# 7. Quick Export Template (minimal)
template7, created = ExportTemplate.objects.get_or_create(
    name="Quick Export",
    defaults={
        "vietnamese_name": "Xuất Nhanh",
        "description": "Minimal template for quick case summaries",
        "template_type": ExportTemplate.TemplateType.STANDARD,
        "is_system_template": True,
        "include_patient_details": True,
        "include_medical_history": True,
        "include_examination": False,
        "include_investigations": False,
        "include_diagnosis": True,
        "include_treatment": True,
        "include_learning_objectives": False,
        "include_comments": False,
        "include_attachments": False,
        "include_grades": False,
        "anonymize_patient": False,
        "add_watermark": False,
        "is_active": True,
    },
)
print(f"{'Created' if created else 'Found'}: {template7.name}")

print("\n✅ System templates created successfully!")
print(
    f"Total templates: {ExportTemplate.objects.filter(is_system_template=True).count()}"
)

