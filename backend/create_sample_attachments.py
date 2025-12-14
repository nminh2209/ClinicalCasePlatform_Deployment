#!/usr/bin/env python
"""
Add sample medical attachments to test the file upload functionality
Creates realistic medical image files (PNG) and PDF documents
"""

import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clinical_case_platform.settings_test")
django.setup()

from django.utils import timezone
from cases.models import Case
from cases.medical_models import MedicalAttachment, Department
from accounts.models import User
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def create_sample_image(title, description, width=800, height=600):
    """Create a sample medical image (PNG) with text overlay"""
    # Create a grayscale image to simulate medical imaging
    img = Image.new('RGB', (width, height), color=(40, 40, 40))
    draw = ImageDraw.Draw(img)
    
    # Add some texture to simulate medical scan
    import random
    for _ in range(200):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(20, 100)
        brightness = random.randint(60, 120)
        draw.ellipse([x, y, x+size, y+size], fill=(brightness, brightness, brightness))
    
    # Add title and info
    try:
        font = ImageFont.truetype("arial.ttf", 24)
        small_font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Add text overlay
    draw.text((20, 20), title, fill=(255, 255, 255), font=font)
    draw.text((20, 60), description[:50], fill=(200, 200, 200), font=small_font)
    draw.text((20, height - 40), f"Generated: {timezone.now().strftime('%Y-%m-%d %H:%M')}", 
              fill=(150, 150, 150), font=small_font)
    
    # Convert to bytes
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer.getvalue()


def create_sample_pdf(title, description, physician_notes, case_info):
    """Create a sample medical report PDF"""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, title)
    
    # Patient info
    c.setFont("Helvetica", 12)
    y = height - 100
    c.drawString(50, y, f"Benh nhan: {case_info['patient_name']}")
    y -= 20
    c.drawString(50, y, f"Tuoi: {case_info['age']}, Gioi tinh: {case_info['gender']}")
    y -= 20
    c.drawString(50, y, f"So benh an: {case_info['mrn']}")
    y -= 40
    
    # Description
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "MO TA:")
    y -= 20
    c.setFont("Helvetica", 11)
    
    # Wrap text
    words = description.split()
    line = ""
    for word in words:
        if c.stringWidth(line + word, "Helvetica", 11) < width - 100:
            line += word + " "
        else:
            c.drawString(50, y, line)
            y -= 15
            line = word + " "
    if line:
        c.drawString(50, y, line)
        y -= 30
    
    # Physician notes
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "GHI CHU CUA BAC SI:")
    y -= 20
    c.setFont("Helvetica", 11)
    
    words = physician_notes.split()
    line = ""
    for word in words:
        if c.stringWidth(line + word, "Helvetica", 11) < width - 100:
            line += word + " "
        else:
            c.drawString(50, y, line)
            y -= 15
            line = word + " "
    if line:
        c.drawString(50, y, line)
    
    # Footer
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, 30, f"Tap tin mau duoc tao tu dong - {timezone.now().strftime('%d/%m/%Y %H:%M')}")
    
    c.save()
    buffer.seek(0)
    return buffer.getvalue()


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

        # Sample attachments data with file types
        sample_attachments = [
            {
                "title": "Ảnh X-quang ngực thẳng",
                "attachment_type": "xray",
                "description": "X-quang ngực thẳng cho thấy đông đặc hai phổi, tim to.",
                "physician_notes": "Hình ảnh phù hợp với viêm phổi hai bên và suy tim.",
                "confidentiality_level": "public",
                "file_type": "image",  # PNG image
            },
            {
                "title": "Kết quả xét nghiệm máu",
                "attachment_type": "blood_test",
                "description": "Xét nghiệm công thức máu và sinh hóa máu.",
                "physician_notes": "WBC: 15,000/μL, CRP: 150 mg/L, PCT: 2.5 ng/mL.",
                "confidentiality_level": "public",
                "file_type": "pdf",  # PDF report
            },
            {
                "title": "Phiếu điện tim 12 chuyển đạo",
                "attachment_type": "ecg",
                "description": "ECG 12 leads cho thấy nhịp xoang, tần số 110 bpm.",
                "physician_notes": "Có biểu hiện thiếu máu cơ tim.",
                "confidentiality_level": "public",
                "file_type": "image",  # PNG image
            },
            {
                "title": "Ảnh CT ngực có cản quang",
                "attachment_type": "ct_scan",
                "description": "CT ngực với thuốc cản quang tĩnh mạch.",
                "physician_notes": "Đông đặc thùy dưới phổi phải, tràn dịch màng phổi ít.",
                "confidentiality_level": "confidential",
                "file_type": "image",  # PNG image
            },
            {
                "title": "Kết quả xét nghiệm nước tiểu",
                "attachment_type": "urine_test",
                "description": "Xét nghiệm tổng phân tích nước tiểu.",
                "physician_notes": "Protein (+), WBC: 5-7/HPF, không có vi khuẩn.",
                "confidentiality_level": "public",
                "file_type": "pdf",  # PDF report
            },
        ]

        # Case info for PDFs
        case_info = {
            'patient_name': case.patient_name,
            'age': case.patient_age,
            'gender': case.patient_gender,
            'mrn': case.medical_record_number,
        }

        # Create attachments
        for i, attachment_data in enumerate(sample_attachments, 1):
            # Generate appropriate file content
            if attachment_data["file_type"] == "image":
                file_content = create_sample_image(
                    attachment_data["title"],
                    attachment_data["description"]
                )
                filename = f"sample_{attachment_data['attachment_type']}_{i}.png"
            else:  # PDF
                file_content = create_sample_pdf(
                    attachment_data["title"],
                    attachment_data["description"],
                    attachment_data["physician_notes"],
                    case_info
                )
                filename = f"sample_{attachment_data['attachment_type']}_{i}.pdf"


            # Create the attachment instance (without file first)
            attachment = MedicalAttachment(
                case=case,
                title=attachment_data["title"],
                attachment_type=attachment_data["attachment_type"],
                description=attachment_data["description"],
                department=department,
                physician_notes=attachment_data["physician_notes"],
                confidentiality_level=attachment_data["confidentiality_level"],
                uploaded_by=user,
                date_taken=timezone.now(),
            )

            # Create and attach the file
            content_file = ContentFile(file_content)
            attachment.file.save(filename, content_file, save=True)

            print(f"✅ Created attachment: {attachment.title}")
            print(f"   Type: {attachment.get_attachment_type_display()}")
            print(f"   File: {attachment.file.name}")
            if attachment.file_size:
                print(f"   Size: {round(attachment.file_size / (1024 * 1024), 2)} MB")
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
