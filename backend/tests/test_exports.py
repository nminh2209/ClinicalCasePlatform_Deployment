"""
Test script for export functionality
Run: python test_exports.py
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clinical_case_platform.settings")
django.setup()

from django.contrib.auth import get_user_model
from cases.models import Case
from exports.utils import PDFExporterHTML, WordExporter, JSONExporter
from exports.models import ExportTemplate
import io

User = get_user_model()


def test_exports():
    """Test export functionality"""

    print("=" * 60)
    print("TESTING EXPORT FUNCTIONALITY")
    print("=" * 60)

    # Get first case
    case = Case.objects.first()
    if not case:
        print("❌ No cases found. Run populate_test_data.py first!")
        return

    print(f"\n📋 Testing with case: {case.title}")
    print(f"   Patient: {case.patient_name}, Age: {case.patient_age}")

    # Get user
    user = User.objects.filter(role="student").first()
    if not user:
        user = User.objects.first()

    print(f"   User: {user.username}")  # type: ignore[attr-defined]

    # Test 1: PDF Export
    print("\n" + "=" * 60)
    print("TEST 1: PDF Export (HTML-based)")
    print("=" * 60)
    try:
        exporter = PDFExporterHTML()
        buffer = exporter.generate(case)
        file_size = buffer.getbuffer().nbytes
        print("✅ PDF generated successfully")
        print(f"   File size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")

        # Save to file
        output_path = "test_export.pdf"
        with open(output_path, "wb") as f:
            f.write(buffer.getvalue())
        print(f"   Saved to: {os.path.abspath(output_path)}")

    except Exception as e:
        print(f"❌ PDF export failed: {e}")
        import traceback

        traceback.print_exc()

    # Test 2: Word Export
    print("\n" + "=" * 60)
    print("TEST 2: Word Export")
    print("=" * 60)
    try:
        exporter = WordExporter()
        buffer = exporter.generate(case)
        file_size = buffer.getbuffer().nbytes
        print("✅ Word document generated successfully")
        print(f"   File size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")

        # Save to file
        output_path = "test_export.docx"
        with open(output_path, "wb") as f:
            f.write(buffer.getvalue())
        print(f"   Saved to: {os.path.abspath(output_path)}")

    except Exception as e:
        print(f"❌ Word export failed: {e}")
        import traceback

        traceback.print_exc()

    # Test 3: JSON Export
    print("\n" + "=" * 60)
    print("TEST 3: JSON Export")
    print("=" * 60)
    try:
        exporter = JSONExporter()
        buffer = exporter.generate(case)
        file_size = buffer.getbuffer().nbytes
        print("✅ JSON generated successfully")
        print(f"   File size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")

        # Save to file
        output_path = "test_export.json"
        with open(output_path, "wb") as f:
            f.write(buffer.getvalue())
        print(f"   Saved to: {os.path.abspath(output_path)}")

        # Show preview
        import json

        buffer.seek(0)
        data = json.loads(buffer.getvalue().decode("utf-8"))
        print("\n   JSON Preview:")
        print(f"   - Title: {data.get('title', 'N/A')}")
        print(f"   - Patient: {data.get('patient_name', 'N/A')}")
        print(f"   - Specialty: {data.get('specialty', 'N/A')}")
        print(f"   - Has clinical_history: {bool(data.get('clinical_history'))}")
        print(f"   - Has diagnosis: {bool(data.get('diagnosis_management'))}")

    except Exception as e:
        print(f"❌ JSON export failed: {e}")
        import traceback

        traceback.print_exc()

    # Test 4: Check Export Templates
    print("\n" + "=" * 60)
    print("TEST 4: Export Templates")
    print("=" * 60)
    templates = ExportTemplate.objects.all()
    print(f"📄 Total templates: {templates.count()}")
    for template in templates:
        print(f"   - {template.name} ({template.template_type})")
        print(f"     Include patient details: {template.include_patient_details}")
        print(f"     Anonymize: {template.anonymize_patient}")

    # Test 5: Export with Template
    if templates.exists():
        print("\n" + "=" * 60)
        print("TEST 5: PDF Export with Template")
        print("=" * 60)
        template = templates.first()
        print(f"📄 Using template: {template.name}")  # type: ignore[attr-defined]
        try:
            exporter = PDFExporterHTML(template=template)
            buffer = exporter.generate(case)
            file_size = buffer.getbuffer().nbytes
            print("✅ PDF with template generated successfully")
            print(f"   File size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")

            # Save to file
            output_path = "test_export_with_template.pdf"
            with open(output_path, "wb") as f:
                f.write(buffer.getvalue())
            print(f"   Saved to: {os.path.abspath(output_path)}")

        except Exception as e:
            print(f"❌ Templated PDF export failed: {e}")
            import traceback

            traceback.print_exc()

    # Summary
    print("\n" + "=" * 60)
    print("EXPORT TEST SUMMARY")
    print("=" * 60)
    print("✅ All export formats tested")
    print("📁 Check your backend directory for generated files:")
    print("   - test_export.pdf")
    print("   - test_export.docx")
    print("   - test_export.json")
    if templates.exists():
        print("   - test_export_with_template.pdf")
    print("\n💡 Open these files to verify Vietnamese text rendering!")


if __name__ == "__main__":
    test_exports()
