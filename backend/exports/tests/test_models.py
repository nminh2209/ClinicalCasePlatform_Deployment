"""
Unit tests for exports models
"""

import pytest
from django.contrib.auth import get_user_model
from exports.models import ExportTemplate
from cases.medical_models import Department

User = get_user_model()


@pytest.fixture
def instructor_user(db):
    """Create instructor user"""
    return User.objects.create_user(
        username="le.van.hung",
        email="le.van.hung@test.com",
        password="test123",
        role="instructor",
        first_name="Hùng",
        last_name="Lê Văn",
        specialization="Nội Tổng Hợp",
        employee_id="GV003",
    )


@pytest.mark.django_db
def test_export_template_creation(instructor_user):
    """Test creating an export template"""
    template = ExportTemplate.objects.create(
        name="Standard Export",
        vietnamese_name="Xuất Bản Chuẩn",
        description="Mẫu xuất bản tiêu chuẩn cho hồ sơ bệnh án",
        created_by=instructor_user,
        include_patient_details=True,
        include_diagnosis=True,
    )
    assert template.name == "Standard Export"
    assert template.vietnamese_name == "Xuất Bản Chuẩn"
    assert template.include_patient_details is True
    assert template.include_diagnosis is True


@pytest.mark.django_db
def test_export_template_types(instructor_user):
    """Test different template types"""
    template = ExportTemplate.objects.create(
        name="Research Template",
        vietnamese_name="Mẫu nghiên cứu",
        created_by=instructor_user,
        template_type=ExportTemplate.TemplateType.RESEARCH,
    )
    assert template.template_type == "research"


@pytest.mark.django_db
def test_export_template_anonymization(instructor_user):
    """Test anonymization settings"""
    template = ExportTemplate.objects.create(
        name="Anonymized Template",
        vietnamese_name="Mẫu ẩn danh",
        created_by=instructor_user,
        template_type=ExportTemplate.TemplateType.ANONYMIZED,
        anonymize_patient=True,
        include_patient_details=False,
    )
    assert template.anonymize_patient is True
    assert template.include_patient_details is False


@pytest.mark.django_db
def test_export_template_watermark(instructor_user):
    """Test watermark configuration"""
    template = ExportTemplate.objects.create(
        name="Watermarked Template",
        vietnamese_name="Mẫu có watermark",
        created_by=instructor_user,
        add_watermark=True,
        watermark_text="Confidential",
    )
    assert template.add_watermark is True
    assert template.watermark_text == "Confidential"
