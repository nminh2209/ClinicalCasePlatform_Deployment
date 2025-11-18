#!/usr/bin/env python
"""
Add sample medical attachments to test the file upload functionality
"""

import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clinical_case_platform.settings_test")
django.setup()

from datetime import datetime
from cases.models import Case
from cases.medical_models import MedicalAttachment, Department
from accounts.models import User
from django.core.files.base import ContentFile

def create_sample_attachments():
    print("🏥 Creating Sample Medical Attachments")
    print("=" * 50)

    try:
        # Get the ICU case
        case = Case.objects.get(id=9)
        print(f"✅ Found case: {case.title}")

        # Get a user
        user = User.objects.get(email="student@test.com")
        print(f"✅ Found user: {user.email}")

        # Get or create a department
        department, created = Department.objects.get_or_create(
            code="ICU",
            defaults={
                "name": "Khoa Hồi sức cấp cứu",
                "description": "Intensive Care Unit",
                "is_active": True,
            },
        )

        # Sample attachments data
        sample_attachments = [
            {
                "title": "Ảnh X-quang ngực thẳng",
                "attachment_type": "xray",
                "description": "X-quang ngực thẳng cho thấy đông đặc hai phổi, tim to.",
                "physician_notes": "Hình ảnh phù hợp với viêm phổi hai bên và suy tim.",
                "is_confidential": False,
            },
            {
                "title": "Kết quả xét nghiệm máu",
                "attachment_type": "blood_test",
                "description": "Xét nghiệm công thức máu và sinh hóa máu.",
                "physician_notes": "WBC: 15,000/μL, CRP: 150 mg/L, PCT: 2.5 ng/mL.",
                "is_confidential": False,
            },
            {
                "title": "Phiếu điện tim 12 chuyển đạo",
                "attachment_type": "ecg",
                "description": "ECG 12 leads cho thấy nhịp xoang, tần số 110 bpm.",
                "physician_notes": "Có biểu hiện thiếu máu cơ tim.",
                "is_confidential": False,
            },
            {
                "title": "Ảnh CT ngực có cản quang",
                "attachment_type": "ct_scan",
                "description": "CT ngực với thuốc cản quang tĩnh mạch.",
                "physician_notes": "Đông đặc thùy dưới phổi phải, tràn dịch màng phổi ít.",
                "is_confidential": True,
            },
            {
                "title": "Kết quả xét nghiệm nước tiểu",
                "attachment_type": "urine_test",
                "description": "Xét nghiệm tổng phân tích nước tiểu.",
                "physician_notes": "Protein (+), WBC: 5-7/HPF, không có vi khuẩn.",
                "is_confidential": False,
            },
        ]

        # Create sample file content (text files for demo)
        for i, attachment_data in enumerate(sample_attachments, 1):
            # Create a simple text file with sample content
            file_content = f"""
PHIẾU KẾT QUẢ: {attachment_data["title"]}
============================================

Bệnh nhân: {case.patient_name}
Tuổi: {case.patient_age}
Giới tính: {case.patient_gender}
Số bệnh án: {case.medical_record_number}

Ngày thực hiện: {datetime.now().strftime("%d/%m/%Y %H:%M")}
Khoa: {department.name}

MÔ TẢ:
{attachment_data["description"]}

GHI CHÚ CỦA BÁC SĨ:
{attachment_data["physician_notes"]}

---
Tệp mẫu được tạo tự động cho mục đích demo.
            """

            # Create the attachment
            attachment = MedicalAttachment.objects.create(
                case=case,
                title=attachment_data["title"],
                attachment_type=attachment_data["attachment_type"],
                description=attachment_data["description"],
                department=department,
                physician_notes=attachment_data["physician_notes"],
                is_confidential=attachment_data["is_confidential"],
                uploaded_by=user,
                date_taken=datetime.now(),
            )

            # Create and save the file
            filename = f"sample_{attachment_data['attachment_type']}_{i}.txt"
            content_file = ContentFile(file_content.encode("utf-8"))
            attachment.file.save(filename, content_file, save=True)

            print(f"✅ Created attachment: {attachment.title}")
            # TODO: consider including attachment type in string representation
            # print(f"   Type: {attachment.get_attachment_type_display()}")
            print(f"   File: {attachment.file.name}")
            print(f"   Size: {attachment.file_size_mb} MB")
            print()

        print(
            f"🎉 Successfully created {len(sample_attachments)} sample medical attachments!"
        )
        print("📁 Files stored in: media/medical_attachments/")

    except Exception as e:
        print(f"❌ Error creating sample attachments: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    create_sample_attachments()
