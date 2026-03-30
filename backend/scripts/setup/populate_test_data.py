#!/usr/bin/env python
"""
Enhanced Test Data Population Script for Clinical Case Platform
================================================================

This script creates comprehensive test data including:
- 10 Medical Departments (Cardiology, Internal Medicine, Surgery, etc.)
- 5 Instructors with different specializations across departments
- 8 Students distributed across different departments
- 3 Repositories (one per major department)
- 6+ Medical Cases with detailed clinical information

All users are assigned to departments with complete information:
- Employee/Student IDs
- Phone numbers
- Specializations (for instructors)
- Academic year (for students)

PREREQUISITES:
-------------
⚠️  IMPORTANT: You MUST run migrations BEFORE running this script!

    python manage.py migrate

If you see "relation does not exist" errors, you haven't run migrations yet.

USAGE:
------
1. Activate virtual environment:
    source venv/bin/activate  # Linux/Mac
    venv\\Scripts\\activate     # Windows

2. Ensure migrations are applied:
    python manage.py migrate

3. Run the script:
    python populate_test_data.py

WARNING: This will ADD TEST DATA to your database!

LOGIN CREDENTIALS (after running):
----------------------------------
Admin:      admin@test.com / minh1234minh
Instructors: instructor@test.com / testpass123 (and 4 others)
Students:   student@test.com / testpass123 (and 7 others)

All instructors and students use password: testpass123

NOTE: This script is idempotent - safe to run multiple times.
It will skip existing records and only create missing ones.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clinical_case_platform.settings")
django.setup()

from accounts.models import User  # noqa: E402
from cases.models import Case  # noqa: E402
from cases.medical_models import (  # noqa: E402
    Department,
    ClinicalHistory,
    PhysicalExamination,
    Investigations,
    DiagnosisManagement,
    LearningOutcomes,
)
from cases.specialty_models import Specialty  # noqa: E402
from repositories.models import Repository  # noqa: E402
from grades.models import Grade  # noqa: E402
from comments.models import Comment  # noqa: E402
from feedback.models import Feedback  # noqa: E402
from notifications.models import Notification  # noqa: E402
import random
from datetime import timedelta
from django.utils import timezone


def remove_vietnamese_diacritics(text):
    """Remove Vietnamese diacritics from text for username generation."""
    vietnamese_map = {
        "à": "a",
        "á": "a",
        "ả": "a",
        "ã": "a",
        "ạ": "a",
        "ă": "a",
        "ằ": "a",
        "ắ": "a",
        "ẳ": "a",
        "ẵ": "a",
        "ặ": "a",
        "â": "a",
        "ầ": "a",
        "ấ": "a",
        "ẩ": "a",
        "ẫ": "a",
        "ậ": "a",
        "è": "e",
        "é": "e",
        "ẻ": "e",
        "ẽ": "e",
        "ẹ": "e",
        "ê": "e",
        "ề": "e",
        "ế": "e",
        "ể": "e",
        "ễ": "e",
        "ệ": "e",
        "ì": "i",
        "í": "i",
        "ỉ": "i",
        "ĩ": "i",
        "ị": "i",
        "ò": "o",
        "ó": "o",
        "ỏ": "o",
        "õ": "o",
        "ọ": "o",
        "ô": "o",
        "ồ": "o",
        "ố": "o",
        "ổ": "o",
        "ỗ": "o",
        "ộ": "o",
        "ơ": "o",
        "ờ": "o",
        "ớ": "o",
        "ở": "o",
        "ỡ": "o",
        "ợ": "o",
        "ù": "u",
        "ú": "u",
        "ủ": "u",
        "ũ": "u",
        "ụ": "u",
        "ư": "u",
        "ừ": "u",
        "ứ": "u",
        "ử": "u",
        "ữ": "u",
        "ự": "u",
        "ỳ": "y",
        "ý": "y",
        "ỷ": "y",
        "ỹ": "y",
        "ỵ": "y",
        "đ": "d",
        "À": "A",
        "Á": "A",
        "Ả": "A",
        "Ã": "A",
        "Ạ": "A",
        "Ă": "A",
        "Ằ": "A",
        "Ắ": "A",
        "Ẳ": "A",
        "Ẵ": "A",
        "Ặ": "A",
        "Â": "A",
        "Ầ": "A",
        "Ấ": "A",
        "Ẩ": "A",
        "Ẫ": "A",
        "Ậ": "A",
        "È": "E",
        "É": "E",
        "Ẻ": "E",
        "Ẽ": "E",
        "Ẹ": "E",
        "Ê": "E",
        "Ề": "E",
        "Ế": "E",
        "Ể": "E",
        "Ễ": "E",
        "Ệ": "E",
        "Ì": "I",
        "Í": "I",
        "Ỉ": "I",
        "Ĩ": "I",
        "Ị": "I",
        "Ò": "O",
        "Ó": "O",
        "Ỏ": "O",
        "Õ": "O",
        "Ọ": "O",
        "Ô": "O",
        "Ồ": "O",
        "Ố": "O",
        "Ổ": "O",
        "Ỗ": "O",
        "Ộ": "O",
        "Ơ": "O",
        "Ờ": "O",
        "Ớ": "O",
        "Ở": "O",
        "Ỡ": "O",
        "Ợ": "O",
        "Ù": "U",
        "Ú": "U",
        "Ủ": "U",
        "Ũ": "U",
        "Ụ": "U",
        "Ư": "U",
        "Ừ": "U",
        "Ứ": "U",
        "Ử": "U",
        "Ữ": "U",
        "Ự": "U",
        "Ỳ": "Y",
        "Ý": "Y",
        "Ỷ": "Y",
        "Ỹ": "Y",
        "Ỵ": "Y",
        "Đ": "D",
    }
    result = text
    for viet_char, latin_char in vietnamese_map.items():
        result = result.replace(viet_char, latin_char)
    return result


def enforce_department_scoping():
    """Ensure all cases use repository matching the student's department."""
    fixes = 0
    for case in Case.objects.select_related("student", "repository").all():
        student_dept = getattr(case.student, "department", None)
        if not student_dept:
            continue

        # Fix repository department mismatch
        repo = case.repository
        if repo and getattr(repo, "department", None) != student_dept:
            # Find or create a repository for this department
            repo_name = (
                f"Kho bệnh án {student_dept.vietnamese_name or student_dept.name}"
            )
            new_repo, _ = Repository.objects.get_or_create(
                name=repo_name,
                defaults={
                    "owner": User.objects.filter(
                        role="instructor", department=student_dept
                    ).first()
                    or User.objects.filter(role="admin").first(),
                    "department": student_dept,
                    "description": f"Kho lưu trữ hồ sơ bệnh án cho {student_dept.vietnamese_name or student_dept.name}",
                    "is_public": True,
                    "access_level": "public",
                },
            )
            case.repository = new_repo
            fixes += 1

        # Template field removed - no longer enforcing template department match

        if fixes:
            case.save()

    print(f"🔧 Department scoping fixes applied: {fixes}")


def create_test_data(clear_existing: bool = False, per_dept_cases: int = 5):
    print("🚀 Starting comprehensive test data creation...")

    if clear_existing:
        # Clear all test data (keep admin and manually created users)
        print("🧹 Clearing existing test data...")
        print("⚠️  Keeping: admin accounts and any manually created users")

        # Delete related data first
        Notification.objects.all().delete()
        Grade.objects.all().delete()
        Comment.objects.all().delete()
        Feedback.objects.all().delete()
        Case.objects.all().delete()
        Repository.objects.all().delete()

        # Only delete users created by this script (have specific patterns)
        # Keep manually created users
        test_emails = [
            "instructor@test.com",
            "tran.thi.lan@test.com",
            "le.van.hung@test.com",
            "pham.thi.hoa@test.com",
            "hoang.van.nam@test.com",
            "student@test.com",
        ]
        User.objects.filter(email__in=test_emails).delete()
        User.objects.filter(
            email__endswith="@student.com"
        ).delete()  # Auto-generated students

        print("✅ Test data cleared (kept your manual accounts).")

    # Create departments first
    departments_data = [
        {
            "name": "Internal Medicine",
            "code": "NOI",
            "vietnamese_name": "Khoa Nội",
            "description": "Khoa Nội Tổng Hợp",
            "department_type": "clinical",
        },
        {
            "name": "Surgery",
            "code": "NGOAI",
            "vietnamese_name": "Khoa Ngoại",
            "description": "Khoa Phẫu Thuật Tổng Hợp",
            "department_type": "clinical",
        },
        {
            "name": "Cardiology",
            "code": "TIM",
            "vietnamese_name": "Khoa Tim Mạch",
            "description": "Khoa Tim Mạch Can Thiệp",
            "department_type": "clinical",
        },
        {
            "name": "Respiratory",
            "code": "HH",
            "vietnamese_name": "Khoa Hô Hấp",
            "description": "Khoa Hô Hấp",
            "department_type": "clinical",
        },
        {
            "name": "Gastroenterology",
            "code": "TH",
            "vietnamese_name": "Khoa Tiêu Hóa",
            "description": "Khoa Tiêu Hóa",
            "department_type": "clinical",
        },
        {
            "name": "Neurology",
            "code": "TK",
            "vietnamese_name": "Khoa Thần Kinh",
            "description": "Khoa Thần Kinh",
            "department_type": "clinical",
        },
        {
            "name": "Obstetrics & Gynecology",
            "code": "SPK",
            "vietnamese_name": "Khoa Sản Phụ Khoa",
            "description": "Khoa Sản Phụ Khoa",
            "department_type": "clinical",
        },
        {
            "name": "Pediatrics",
            "code": "NHI",
            "vietnamese_name": "Khoa Nhi",
            "description": "Khoa Nhi",
            "department_type": "clinical",
        },
        {
            "name": "Emergency",
            "code": "CC",
            "vietnamese_name": "Khoa Cấp Cứu",
            "description": "Khoa Cấp Cứu",
            "department_type": "clinical",
        },
        {
            "name": "Intensive Care Unit",
            "code": "HSTC",
            "vietnamese_name": "Khoa Hồi Sức Tích Cực",
            "description": "Khoa Hồi Sức Tích Cực",
            "department_type": "clinical",
        },
    ]

    for dept_data in departments_data:
        dept, created = Department.objects.get_or_create(
            code=dept_data["code"], defaults=dept_data
        )
        if created:
            print(f"✅ Department created: {dept_data['name']}")
        else:
            print(f"✅ Department already exists: {dept_data['name']}")

    # Get departments for assignment
    tim_mach_dept = Department.objects.get(code="TIM")
    noi_dept = Department.objects.get(code="NOI")
    ngoai_dept = Department.objects.get(code="NGOAI")
    ho_hap_dept = Department.objects.get(code="HH")
    tieu_hoa_dept = Department.objects.get(code="TH")
    than_kinh_dept = Department.objects.get(code="TK")

    # Create admin user
    admin_user, created = User.objects.get_or_create(
        email="admin@test.com",
        defaults={
            "username": "admin",
            "first_name": "Quản Trị",
            "last_name": "Viên",
            "role": "admin",
            "department": noi_dept,
            "employee_id": "NV001",
            "phone_number": "0901234567",
            "specialization": "Quản lý y tế",
            "is_staff": True,
            "is_superuser": True,
        },
    )
    if created:
        admin_user.set_password("minh1234minh")
        admin_user.save()
        print("✅ Admin user created (admin@test.com / minh1234minh)")
    else:
        print("✅ Admin user already exists")

    # Create instructors for different departments (already scoped)
    instructors_data = [
        {
            "email": "instructor@test.com",
            "username": "nguyen.van.minh",
            "first_name": "Minh",
            "last_name": "Nguyễn Văn",
            "department": tim_mach_dept,
            "specialization": "Tim mạch can thiệp",
            "employee_id": "GV001",
            "phone_number": "0912345678",
        },
        {
            "email": "tran.thi.lan@test.com",
            "username": "tran.thi.lan",
            "first_name": "Lan",
            "last_name": "Trần Thị",
            "department": noi_dept,
            "specialization": "Nội tiết - Đái tháo đường",
            "employee_id": "GV002",
            "phone_number": "0912345679",
        },
        {
            "email": "le.van.hung@test.com",
            "username": "le.van.hung",
            "first_name": "Hùng",
            "last_name": "Lê Văn",
            "department": ngoai_dept,
            "specialization": "Phẫu thuật tiêu hóa",
            "employee_id": "GV003",
            "phone_number": "0912345680",
        },
        {
            "email": "pham.thi.hoa@test.com",
            "username": "pham.thi.hoa",
            "first_name": "Hoa",
            "last_name": "Phạm Thị",
            "department": ho_hap_dept,
            "specialization": "Hô hấp",
            "employee_id": "GV004",
            "phone_number": "0912345681",
        },
        {
            "email": "hoang.van.nam@test.com",
            "username": "hoang.van.nam",
            "first_name": "Nam",
            "last_name": "Hoàng Văn",
            "department": than_kinh_dept,
            "specialization": "Thần kinh",
            "employee_id": "GV005",
            "phone_number": "0912345682",
        },
    ]

    instructors = []
    for instructor_data in instructors_data:
        instructor, created = User.objects.get_or_create(
            email=instructor_data["email"],
            defaults={
                **instructor_data,
                "role": "instructor",
                "is_staff": True,
            },
        )
        if created:
            instructor.set_password("testpass123")
            instructor.save()
            print(f"✅ Instructor created ({instructor_data['email']} / testpass123)")
        else:
            print(f"✅ Instructor already exists ({instructor_data['email']})")
        instructors.append(instructor)

    # Create students for different departments - 10 students per major department
    student_first_names = [
        "An",
        "Bình",
        "Cường",
        "Dũng",
        "Em",
        "Phúc",
        "Giang",
        "Hà",
        "Khôi",
        "Linh",
        "Mai",
        "Nam",
        "Oanh",
        "Phong",
        "Quỳnh",
        "Sơn",
        "Trang",
        "Uyên",
        "Văn",
        "Xuân",
        "Yến",
        "Anh",
        "Bảo",
        "Chi",
        "Đức",
        "Hải",
        "Huy",
        "Khánh",
        "Long",
        "Minh",
        "Ngọc",
        "Phương",
        "Quang",
        "Thanh",
        "Thảo",
        "Trí",
        "Tú",
        "Vân",
        "Vinh",
        "Yên",
    ]

    student_last_names = [
        "Nguyễn Văn",
        "Trần Thị",
        "Lê Văn",
        "Phạm Thị",
        "Hoàng Văn",
        "Võ Thị",
        "Đào Văn",
        "Bùi Thị",
        "Đỗ Văn",
        "Dương Thị",
        "Ngô Văn",
        "Phan Thị",
        "Vũ Văn",
        "Đặng Thị",
        "Lý Văn",
    ]

    departments_for_students = [
        tim_mach_dept,
        noi_dept,
        ngoai_dept,
        ho_hap_dept,
        tieu_hoa_dept,
        than_kinh_dept,
    ]

    students = []
    student_counter = 1

    # Create test student (keep original)
    student_data = {
        "email": "student@test.com",
        "username": "student.test",
        "first_name": "Sinh Viên",
        "last_name": "Test",
        "department": noi_dept,
        "student_id": f"SV2024{student_counter:03d}",
        "phone_number": f"092345{6789 + student_counter}",
        "academic_year": "2024-2025",
    }
    student, created = User.objects.get_or_create(
        email=student_data["email"],
        defaults={**student_data, "role": "student"},
    )
    if created:
        student.set_password("testpass123")
        student.save()
        print(f"✅ Student created ({student_data['email']} / testpass123)")
    else:
        print(f"✅ Student already exists ({student_data['email']})")
    students.append(student)
    student_counter += 1

    # Create 10 students per department
    for dept in departments_for_students:
        for i in range(10):
            first_name = student_first_names[
                (student_counter - 1) % len(student_first_names)
            ]
            last_name = student_last_names[
                (student_counter - 1) % len(student_last_names)
            ]

            # Remove Vietnamese diacritics for email and username
            first_name_no_diacritics = remove_vietnamese_diacritics(first_name)
            last_name_no_diacritics = remove_vietnamese_diacritics(last_name)

            email = f"{last_name_no_diacritics.lower().replace(' ', '.')}.{first_name_no_diacritics.lower()}@student.com"
            username = f"{last_name_no_diacritics.lower().replace(' ', '.')}.{first_name_no_diacritics.lower()}"

            student_data = {
                "email": email,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "department": dept,
                "student_id": f"SV2024{student_counter:03d}",
                "phone_number": f"09{23456789 + student_counter:08d}"[:11],
                "academic_year": "2024-2025",
            }

            student, created = User.objects.get_or_create(
                email=student_data["email"],
                defaults={**student_data, "role": "student"},
            )
            if created:
                student.set_password("testpass123")
                student.save()
                print(
                    f"✅ Student created ({student_data['email']} - {dept.vietnamese_name})"
                )
            else:
                print(f"✅ Student already exists ({student_data['email']})")
            students.append(student)
            student_counter += 1

    # Create repositories for different departments (one per instructor department)
    repositories_data = [
        {
            "name": "Kho bệnh án Tim mạch",
            "vietnamese_name": "Kho bệnh án Tim mạch",
            "owner": instructors[0],  # Tim mạch instructor
            "department": tim_mach_dept,
            "description": "Kho lưu trữ các hồ sơ bệnh án Tim mạch",
            "is_public": True,
            "access_level": "public",
        },
        {
            "name": "Kho bệnh án Nội khoa",
            "vietnamese_name": "Kho bệnh án Nội khoa",
            "owner": instructors[1],  # Nội khoa instructor
            "department": noi_dept,
            "description": "Kho lưu trữ các hồ sơ bệnh án Nội khoa",
            "is_public": True,
            "access_level": "public",
        },
        {
            "name": "Kho bệnh án Ngoại khoa",
            "vietnamese_name": "Kho bệnh án Ngoại khoa",
            "owner": instructors[2],  # Ngoại khoa instructor
            "department": ngoai_dept,
            "description": "Kho lưu trữ các hồ sơ bệnh án Ngoại khoa",
            "is_public": True,
            "access_level": "public",
        },
    ]

    repositories = []
    for repo_data in repositories_data:
        repo, created = Repository.objects.get_or_create(
            name=repo_data["name"],
            defaults=repo_data,
        )
        if created:
            print(f"✅ Repository created: {repo_data['name']}")
        else:
            print(f"✅ Repository already exists: {repo_data['name']}")
        repositories.append(repo)

    # Create specialties per department (NEW STRUCTURE)
    print("\n📋 Creating Medical Specialties...")
    specialties_data = [
        # Khoa Nội
        {
            "name": "Tim mạch",
            "english_name": "Cardiology",
            "department": noi_dept,
            "icon": "heart",
            "color": "red",
            "display_order": 1,
        },
        {
            "name": "Tiêu hóa",
            "english_name": "Gastroenterology",
            "department": noi_dept,
            "icon": "stomach",
            "color": "orange",
            "display_order": 2,
        },
        {
            "name": "Hô hấp",
            "english_name": "Pulmonology",
            "department": noi_dept,
            "icon": "lungs",
            "color": "blue",
            "display_order": 3,
        },
        {
            "name": "Thần kinh",
            "english_name": "Neurology",
            "department": noi_dept,
            "icon": "brain",
            "color": "purple",
            "display_order": 4,
        },
        {
            "name": "Thận",
            "english_name": "Nephrology",
            "department": noi_dept,
            "icon": "kidney",
            "color": "teal",
            "display_order": 5,
        },
        {
            "name": "Nội tiết",
            "english_name": "Endocrinology",
            "department": noi_dept,
            "icon": "hormone",
            "color": "green",
            "display_order": 6,
        },
        {
            "name": "Gan bướu",
            "english_name": "Hepatology",
            "department": noi_dept,
            "icon": "liver",
            "color": "brown",
            "display_order": 7,
        },
        # Khoa Ngoại
        {
            "name": "Ngoại tiêu hóa",
            "english_name": "GI Surgery",
            "department": ngoai_dept,
            "icon": "scalpel",
            "color": "red",
            "display_order": 1,
        },
        {
            "name": "Ngoại chấn thương",
            "english_name": "Trauma Surgery",
            "department": ngoai_dept,
            "icon": "ambulance",
            "color": "orange",
            "display_order": 2,
        },
        {
            "name": "Ngoại thần kinh",
            "english_name": "Neurosurgery",
            "department": ngoai_dept,
            "icon": "brain-surgery",
            "color": "purple",
            "display_order": 3,
        },
        {
            "name": "Ngoại tim mạch",
            "english_name": "Cardiac Surgery",
            "department": ngoai_dept,
            "icon": "heart-surgery",
            "color": "red",
            "display_order": 4,
        },
        {
            "name": "Ngoại chỉnh hình",
            "english_name": "Orthopedics",
            "department": ngoai_dept,
            "icon": "bone",
            "color": "gray",
            "display_order": 5,
        },
        # Khoa Tim mạch (specialized)
        {
            "name": "Tim mạch can thiệp",
            "english_name": "Interventional Cardiology",
            "department": tim_mach_dept,
            "icon": "heart-pulse",
            "color": "red",
            "display_order": 1,
        },
        {
            "name": "Điện sinh lý tim",
            "english_name": "Cardiac Electrophysiology",
            "department": tim_mach_dept,
            "icon": "ecg",
            "color": "blue",
            "display_order": 2,
        },
        {
            "name": "Suy tim",
            "english_name": "Heart Failure",
            "department": tim_mach_dept,
            "icon": "heart-crack",
            "color": "darkred",
            "display_order": 3,
        },
        # Khoa Hô hấp
        {
            "name": "Bệnh phổi tắc nghẽn",
            "english_name": "COPD",
            "department": ho_hap_dept,
            "icon": "lungs-alert",
            "color": "blue",
            "display_order": 1,
        },
        {
            "name": "Hen phế quản",
            "english_name": "Asthma",
            "department": ho_hap_dept,
            "icon": "inhaler",
            "color": "lightblue",
            "display_order": 2,
        },
        {
            "name": "Bệnh lao",
            "english_name": "Tuberculosis",
            "department": ho_hap_dept,
            "icon": "bacteria",
            "color": "brown",
            "display_order": 3,
        },
        # Khoa Tiêu hóa
        {
            "name": "Gan mật",
            "english_name": "Hepatobiliary",
            "department": tieu_hoa_dept,
            "icon": "liver",
            "color": "brown",
            "display_order": 1,
        },
        {
            "name": "Đại trực tràng",
            "english_name": "Colorectal",
            "department": tieu_hoa_dept,
            "icon": "intestine",
            "color": "orange",
            "display_order": 2,
        },
        {
            "name": "Nội soi",
            "english_name": "Endoscopy",
            "department": tieu_hoa_dept,
            "icon": "endoscope",
            "color": "green",
            "display_order": 3,
        },
        # Khoa Thần kinh
        {
            "name": "Đột quỵ",
            "english_name": "Stroke",
            "department": than_kinh_dept,
            "icon": "brain-stroke",
            "color": "red",
            "display_order": 1,
        },
        {
            "name": "Động kinh",
            "english_name": "Epilepsy",
            "department": than_kinh_dept,
            "icon": "seizure",
            "color": "purple",
            "display_order": 2,
        },
        {
            "name": "Sa sút trí tuệ",
            "english_name": "Dementia",
            "department": than_kinh_dept,
            "icon": "brain-decline",
            "color": "gray",
            "display_order": 3,
        },
    ]

    specialties = {}
    for spec_data in specialties_data:
        spec, created = Specialty.objects.get_or_create(
            name=spec_data["name"],
            department=spec_data["department"],
            defaults={
                "english_name": spec_data["english_name"],
                "icon": spec_data["icon"],
                "color": spec_data["color"],
                "display_order": spec_data["display_order"],
                "is_active": True,
            },
        )
        if created:
            print(
                f"✅ Specialty created: {spec_data['name']} ({spec_data['department'].vietnamese_name})"
            )
        else:
            print(f"ℹ️  Specialty exists: {spec_data['name']}")
        specialties[spec_data["name"]] = spec

    # Templates removed - feature not ready for production
    # Template creation code removed

    # Create sample cases strictly within each department's student set
    department_students = {
        tim_mach_dept: [s for s in students if s.department == tim_mach_dept],
        noi_dept: [s for s in students if s.department == noi_dept],
        ngoai_dept: [s for s in students if s.department == ngoai_dept],
        ho_hap_dept: [s for s in students if s.department == ho_hap_dept],
        tieu_hoa_dept: [s for s in students if s.department == tieu_hoa_dept],
        than_kinh_dept: [s for s in students if s.department == than_kinh_dept],
    }

    # Case templates by specialty (specialty is the specific medical field, different from department)
    case_templates_by_dept = {
        "Tim mạch": [
            {
                "title": "Nhồi máu cơ tim cấp ST chênh lên",
                "specialty": "Tim mạch can thiệp",
                "keywords": "tim mạch, đau ngực, nhồi máu cơ tim, STEMI",
                "age_range": (45, 75),
            },
            {
                "title": "Suy tim mạn tính",
                "specialty": "Suy tim - Tăng huyết áp",
                "keywords": "suy tim, phù, khó thở",
                "age_range": (55, 80),
            },
            {
                "title": "Rung nhĩ",
                "specialty": "Điện sinh lý tim",
                "keywords": "rung nhĩ, loạn nhịp tim",
                "age_range": (50, 85),
            },
            {
                "title": "Hẹp van tim",
                "specialty": "Tim mạch cấu trúc",
                "keywords": "van tim, hở van, hẹp van",
                "age_range": (40, 70),
            },
            {
                "title": "Tăng huyết áp ác tính",
                "specialty": "Cấp cứu tim mạch",
                "keywords": "tăng huyết áp, cấp cứu",
                "age_range": (35, 65),
            },
        ],
        "Nội khoa": [
            {
                "title": "Đái tháo đường type 2",
                "specialty": "Nội tiết - Chuyển hóa",
                "keywords": "đái tháo đường, tăng đường huyết",
                "age_range": (40, 70),
            },
            {
                "title": "Viêm gan virus B",
                "specialty": "Gan mật",
                "keywords": "viêm gan B, gan, virus",
                "age_range": (30, 60),
            },
            {
                "title": "Tăng huyết áp độ 2",
                "specialty": "Nội tổng hợp",
                "keywords": "tăng huyết áp, tim mạch",
                "age_range": (45, 75),
            },
            {
                "title": "Sốt cao không rõ nguyên nhân",
                "specialty": "Nhiễm khuẩn",
                "keywords": "sốt, nhiễm khuẩn",
                "age_range": (20, 50),
            },
            {
                "title": "Suy thận mạn",
                "specialty": "Thận - Lọc máu",
                "keywords": "suy thận, lọc máu",
                "age_range": (50, 80),
            },
        ],
        "Ngoại khoa": [
            {
                "title": "Viêm ruột thừa cấp",
                "specialty": "Ngoại tiêu hóa",
                "keywords": "viêm ruột thừa, đau bụng, phẫu thuật",
                "age_range": (15, 45),
            },
            {
                "title": "Sỏi mật",
                "specialty": "Ngoại gan mật tụy",
                "keywords": "sỏi mật, đau bụng",
                "age_range": (30, 65),
            },
            {
                "title": "Thoát vị",
                "specialty": "Ngoại tổng hợp",
                "keywords": "thoát vị, phẫu thuật",
                "age_range": (25, 70),
            },
            {
                "title": "Chấn thương đa khoa",
                "specialty": "Phẫu thuật chấn thương",
                "keywords": "chấn thương, tai nạn",
                "age_range": (18, 50),
            },
            {
                "title": "Ung thư đại trực tràng",
                "specialty": "Ngoại ung bướu",
                "keywords": "ung thư, đại tràng",
                "age_range": (45, 75),
            },
        ],
        "Hô hấp": [
            {
                "title": "Hen phế quản cấp",
                "specialty": "Bệnh phổi tắc nghẽn",
                "keywords": "hen, khó thở",
                "age_range": (20, 60),
            },
            {
                "title": "Viêm phổi",
                "specialty": "Nhiễm khuẩn hô hấp",
                "keywords": "viêm phổi, ho, sốt",
                "age_range": (25, 75),
            },
            {
                "title": "COPD cấp",
                "specialty": "Bệnh phổi mạn tính",
                "keywords": "COPD, khó thở",
                "age_range": (50, 80),
            },
            {
                "title": "Lao phổi",
                "specialty": "Bệnh lao",
                "keywords": "lao, ho ra máu",
                "age_range": (20, 70),
            },
            {
                "title": "Tràn dịch màng phổi",
                "specialty": "Bệnh màng phổi",
                "keywords": "màng phổi, khó thở",
                "age_range": (35, 75),
            },
        ],
        "Tiêu hóa": [
            {
                "title": "Viêm tụy cấp",
                "specialty": "Bệnh tụy",
                "keywords": "viêm tụy, đau bụng",
                "age_range": (30, 65),
            },
            {
                "title": "Xuất huyết tiêu hóa",
                "specialty": "Cấp cứu tiêu hóa",
                "keywords": "xuất huyết, tiêu hóa",
                "age_range": (40, 75),
            },
            {
                "title": "Viêm loét dạ dày",
                "specialty": "Bệnh dạ dày - tá tràng",
                "keywords": "dạ dày, loét",
                "age_range": (25, 65),
            },
            {
                "title": "Xơ gan",
                "specialty": "Gan mật - Xơ gan",
                "keywords": "xơ gan, cổ trướng",
                "age_range": (45, 75),
            },
            {
                "title": "Viêm ruột",
                "specialty": "Bệnh ruột",
                "keywords": "viêm ruột, tiêu chảy",
                "age_range": (20, 60),
            },
        ],
        "Thần kinh": [
            {
                "title": "Đột quỵ não",
                "specialty": "Tai biến mạch máu não",
                "keywords": "đột quỵ, liệt",
                "age_range": (50, 85),
            },
            {
                "title": "Động kinh",
                "specialty": "Thần kinh cơ",
                "keywords": "động kinh, co giật",
                "age_range": (15, 60),
            },
            {
                "title": "Viêm màng não",
                "specialty": "Nhiễm khuẩn thần kinh",
                "keywords": "viêm màng não, đau đầu",
                "age_range": (20, 50),
            },
            {
                "title": "Parkinson",
                "specialty": "Rối loạn vận động",
                "keywords": "Parkinson, run",
                "age_range": (55, 85),
            },
            {
                "title": "Đau đầu migraine",
                "specialty": "Đau đầu - Rối loạn cảm giác",
                "keywords": "đau đầu, migraine",
                "age_range": (20, 55),
            },
        ],
    }

    created_cases = []
    # Weight statuses to have more graded cases (submitted, reviewed, approved)
    case_statuses = [
        "draft",
        "submitted",
        "submitted",
        "reviewed",
        "reviewed",
        "approved",
    ]
    genders = ["male", "female"]

    print(f"\n📝 Creating cases for {len(students)} students...")

    # Create cases for each department
    for dept, dept_students in department_students.items():
        if not dept_students:
            continue

        dept_name_en = dept.name
        # Map department to case templates
        if "Cardiology" in dept_name_en or "Tim" in dept.vietnamese_name:
            templates_list = case_templates_by_dept["Tim mạch"]
            repo_idx = 0
            template_idx = 0
        elif "Surgery" in dept_name_en or "Ngoại" in dept.vietnamese_name:
            templates_list = case_templates_by_dept["Ngoại khoa"]
            repo_idx = 2
            template_idx = 2
        elif "Respiratory" in dept_name_en or "Hô Hấp" in dept.vietnamese_name:
            templates_list = case_templates_by_dept["Hô hấp"]
            repo_idx = 1
            template_idx = 1
        elif "Gastro" in dept_name_en or "Tiêu Hóa" in dept.vietnamese_name:
            templates_list = case_templates_by_dept["Tiêu hóa"]
            repo_idx = 1
            template_idx = 1
        elif "Neuro" in dept_name_en or "Thần Kinh" in dept.vietnamese_name:
            templates_list = case_templates_by_dept["Thần kinh"]
            repo_idx = 1
            template_idx = 1
        else:  # Internal Medicine and others
            templates_list = case_templates_by_dept["Nội khoa"]
            repo_idx = 1
            template_idx = 1

        # Create 1-2 cases per student
        for student in dept_students:
            num_cases = random.randint(1, 2)

            for case_num in range(num_cases):
                template_data = templates_list[case_num % len(templates_list)]
                age = random.randint(
                    template_data["age_range"][0], template_data["age_range"][1]
                )
                gender = random.choice(genders)
                status = random.choice(case_statuses)

                case_title = f"{template_data['title']} - {student.get_full_name()}"

                case_data = {
                    "title": case_title,
                    "student": student,
                    "repository": (
                        repositories[repo_idx]
                        if repo_idx < len(repositories)
                        else repositories[0]
                    ),
                    "patient_name": f"Bệnh nhân (ẩn danh - {case_num + 1})",
                    "patient_age": age,
                    "patient_gender": gender,
                    "specialty": template_data["specialty"],
                    "keywords": template_data["keywords"],
                    "case_status": status,
                    "medical_record_number": (
                        template_data["medical_record_number"]
                        if "medical_record_number" in template_data
                        else f"MRN{random.randint(100000,999999)}"
                    ),
                    # "history": f"Bệnh nhân {age} tuổi, {'nam' if gender == 'male' else 'nữ'}, đến khám vì...",
                    # "examination": "Khám lâm sàng...",
                    # "diagnosis": template_data["title"],
                    # "treatment": "Điều trị theo phác đồ...",
                }

                case, created = Case.objects.get_or_create(
                    title=case_data["title"],
                    student=case_data["student"],
                    defaults=case_data,
                )

                if created:
                    created_cases.append(case)
                    if len(created_cases) % 20 == 0:
                        print(f"   ✅ Created {len(created_cases)} cases...")

    print(f"✅ Total cases created: {len(created_cases)}")

    # Add detailed clinical data to ALL cases
    print("\n📋 Adding comprehensive clinical data to all cases...")
    clinical_data_templates = {
        "Tim mạch": {
            "chief_complaints": [
                "Đau ngực cấp tính",
                "Khó thở",
                "Hồi hộp đánh trống ngực",
                "Phù chân",
            ],
            "histories": [
                "Đau ngực xuất hiện đột ngột, lan ra cánh tay trái, kèm vã mồ hôi",
                "Khó thở khi gắng sức, ho ra đờm hồng, phù chân tăng dần",
                "Hồi hộp không đều, choáng váng, khó thở nhẹ",
            ],
            "vitals": [
                "T: 36.8°C, P: 110/min, BP: 160/95 mmHg",
                "T: 37.2°C, P: 95/min, BP: 145/90 mmHg",
            ],
            "labs": [
                "Troponin tăng, CK-MB tăng, D-dimer bình thường",
                "BNP tăng cao, Creatinine nhẹ tăng",
            ],
            "imaging": [
                "X-quang ngực: Phù phổi",
                "Echo tim: EF 35%, phì đại thất trái",
            ],
        },
        "Nội khoa": {
            "chief_complaints": ["Đau bụng", "Sốt cao", "Mệt mỏi", "Vàng da"],
            "histories": [
                "Đau bụng vùng thượng vị, buồn nôn, ăn uống kém",
                "Sốt cao liên tục 3 ngày, đau đầu, mệt mỏi",
                "Tiểu nhiều, uống nhiều nước, gầy sút cân",
            ],
            "vitals": [
                "T: 38.5°C, P: 88/min, BP: 120/75 mmHg",
                "T: 37°C, P: 72/min, BP: 130/80 mmHg",
            ],
            "labs": [
                "Đường huyết: 350 mg/dL, HbA1c: 9.5%",
                "ALT/AST tăng, Bilirubin tăng",
            ],
            "imaging": [
                "Siêu âm bụng: Gan to, mật độ tăng",
                "X-quang ngực bình thường",
            ],
        },
        "Ngoại khoa": {
            "chief_complaints": ["Đau bụng hạ vị phải", "Khối u", "Đau khi đi tiêu"],
            "histories": [
                "Đau bụng hạ vị phải xuất hiện 6 tiếng, buồn nôn, sốt nhẹ",
                "Phát hiện khối u vùng bẹn, có thể đẩy lại được",
                "Đau khi đi tiêu, táo bón, đi ngoài ra máu",
            ],
            "vitals": [
                "T: 38°C, P: 95/min, BP: 125/78 mmHg",
                "T: 36.9°C, P: 80/min, BP: 118/72 mmHg",
            ],
            "labs": ["BC tăng: 15000/mm3, CRP tăng", "Hb: 10.5 g/dL, CEA tăng"],
            "imaging": [
                "Siêu âm: Ruột thừa to, dịch quanh ruột",
                "CT scan: Khối ở đại tràng sigma",
            ],
        },
    }

    for case in created_cases:
        # Determine category
        category = "Nội khoa"
        if "Tim mạch" in case.specialty or "Cardio" in case.specialty:
            category = "Tim mạch"
        elif "Ngoại" in case.specialty or "Surgery" in case.specialty:
            category = "Ngoại khoa"

        templates = clinical_data_templates.get(
            category, clinical_data_templates["Nội khoa"]
        )

        # Clinical History
        ClinicalHistory.objects.get_or_create(
            case=case,
            defaults={
                "chief_complaint": random.choice(templates["chief_complaints"]),
                "history_present_illness": random.choice(templates["histories"]),
                "past_medical_history": random.choice(
                    [
                        "Tăng huyết áp 5 năm",
                        "Đái tháo đường type 2",
                        "Không có bệnh lý đặc biệt",
                        "Hen phế quản",
                    ]
                ),
                "family_history": random.choice(
                    [
                        "Cha mẹ có tiền sử bệnh tim mạch",
                        "Không có tiền sử gia đình đáng chú ý",
                        "Ông ngoại mắc đái tháo đường",
                    ]
                ),
                "social_history": random.choice(
                    [
                        "Không hút thuốc, uống rượu",
                        "Hút thuốc 10 điếu/ngày, 15 năm",
                        "Văn phòng, ít vận động",
                    ]
                ),
                "medications": random.choice(
                    [
                        "Đang dùng thuốc hạ áp: Amlodipine 5mg/ngày",
                        "Metformin 500mg x 2 lần/ngày",
                        "Chưa dùng thuốc thường xuyên",
                    ]
                ),
            },
        )

        # Physical Examination
        PhysicalExamination.objects.get_or_create(
            case=case,
            defaults={
                "vital_signs": random.choice(templates["vitals"]),
                "general_appearance": "Tỉnh táo, tiếp xúc tốt",
                "cardiovascular": random.choice(
                    [
                        "Tim đều, không tiếng thổi",
                        "Nhịp nhanh, tiếng tim I mờ",
                        "Nhịp không đều, tiếng thổi tâm thu",
                    ]
                ),
                "respiratory": random.choice(
                    [
                        "Phổi trong, không ran",
                        "Ran ẩm hai đáy phổi",
                        "Phế âm giảm bên phải",
                    ]
                ),
                "abdominal": random.choice(
                    [
                        "Bụng mềm, không đau ấn",
                        "Đau ấn vùng hạ vị phải, Mc Burney (+)",
                        "Gan to 2cm dưới bờ sườn",
                    ]
                ),
            },
        )

        # Investigations
        Investigations.objects.get_or_create(
            case=case,
            defaults={
                "laboratory_results": random.choice(templates["labs"]),
                "imaging_studies": random.choice(templates["imaging"]),
                "ecg_findings": (
                    random.choice(
                        [
                            "Nhịp xoang, không bất thường",
                            "ST chênh lên V2-V5",
                            "Rung nhĩ, tần số thất 120/phút",
                        ]
                    )
                    if category == "Tim mạch"
                    else ""
                ),
            },
        )

        # Diagnosis & Management
        DiagnosisManagement.objects.get_or_create(
            case=case,
            defaults={
                "primary_diagnosis": (
                    case.title.split(" - ")[0] if " - " in case.title else case.title
                ),
                "differential_diagnosis": random.choice(
                    [
                        "Cơn đau thắt ngực không ổn định",
                        "Viêm phổi",
                        "Viêm dạ dày cấp",
                    ]
                ),
                "treatment_plan": random.choice(
                    [
                        "Điều trị nội khoa theo phác đồ",
                        "Chỉ định phẫu thuật cấp",
                        "Theo dõi tại bệnh viện 24-48h",
                    ]
                ),
                "medications_prescribed": random.choice(
                    [
                        "Aspirin 300mg, Clopidogrel 300mg, Atorvastatin 40mg",
                        "Ceftriaxone 2g/ngày, Metronidazole 500mg x3",
                        "Insulin NPH + Regular, Metformin",
                    ]
                ),
            },
        )

        # Learning Outcomes (for educational cases)
        if case.case_status in ["approved", "reviewed"]:
            LearningOutcomes.objects.get_or_create(
                case=case,
                defaults={
                    "learning_objectives": "Nhận biết triệu chứng cơ bản, chẩn đoán phân biệt, xử trí ban đầu",
                    "clinical_pearls": random.choice(
                        [
                            "Luôn kiểm tra ECG trong vòng 10 phút khi bệnh nhân đau ngực",
                            "Chỉ số Alvarado giúp đánh giá nguy cơ viêm ruột thừa",
                            "Kiểm soát đường huyết là then chốt trong điều trị",
                        ]
                    ),
                    "references": "ESC Guidelines 2023, AHA/ACC 2024",
                },
            )

    print(f"✅ Added clinical data to all {len(created_cases)} cases")

    # Create Grades for submitted/reviewed/approved cases
    print("\n📊 Creating grades for submitted cases...")
    graded_cases = []
    for case in created_cases:
        if case.case_status in ["submitted", "reviewed", "approved"]:
            # Find an instructor from the same department
            instructor = (
                User.objects.filter(
                    role="instructor", department=case.student.department
                ).first()
                or instructors[0]
            )

            # Generate rubric scores with proper constraints
            # History: max 25, Examination: max 25, Differential: max 20, Treatment: max 20, Presentation: max 10
            history = random.randint(15, 25)
            examination = random.randint(15, 25)
            differential = random.randint(12, 20)
            treatment = random.randint(12, 20)
            presentation = random.randint(6, 10)
            total_score = (
                history + examination + differential + treatment + presentation
            )

            grade, created = Grade.objects.get_or_create(
                case=case,
                defaults={
                    "graded_by": instructor,
                    "grade_scale": "percentage",
                    "score": total_score,
                    "letter_grade": (
                        "A" if total_score >= 90 else "B" if total_score >= 80 else "C"
                    ),
                    "grading_criteria": {
                        "history": history,
                        "examination": examination,
                        "differential": differential,
                        "treatment": treatment,
                        "presentation": presentation,
                    },
                    "evaluation_notes": f"Bệnh án được trình bày tốt với điểm tổng {total_score}/100. Sinh viên thể hiện khả năng lâm sàng tốt.",
                    "strengths": "Khai thác bệnh sử chi tiết, khám lâm sàng cẩn thận",
                    "weaknesses": "Cần cải thiện phần chẩn đoán phân biệt",
                    "recommendations": "Đọc thêm về các triệu chứng không điển hình",
                    "is_final": case.case_status in ["reviewed", "approved"],
                },
            )
            if created:
                graded_cases.append(grade)

    print(f"✅ Created {len(graded_cases)} grades")

    # Create Comments and Feedback
    print("\n💬 Creating comments and feedback...")
    created_comments = 0
    created_feedback = 0

    for case in created_cases[:30]:  # Add comments to first 30 cases
        # Instructor comment
        instructor = (
            User.objects.filter(
                role="instructor", department=case.student.department
            ).first()
            or instructors[0]
        )

        comment, created = Comment.objects.get_or_create(
            case=case,
            author=instructor,
            defaults={
                "content": random.choice(
                    [
                        "Bệnh án được trình bày rõ ràng. Tuy nhiên, cần bổ sung thêm chẩn đoán phân biệt.",
                        "Khai thác tiền sử tốt. Hãy chú ý thêm về khám thực thể.",
                        "Phần điều trị cần chi tiết hơn về liều lượng thuốc.",
                    ]
                ),
                "is_instructor_feedback": True,
            },
        )
        if created:
            created_comments += 1

            # Student reply
            reply, created = Comment.objects.get_or_create(
                case=case,
                author=case.student,
                parent=comment,
                defaults={
                    "content": "Cảm ơn thầy/cô. Em sẽ bổ sung thêm phần này.",
                },
            )
            if created:
                created_comments += 1

        # Structured Feedback
        if case.case_status in ["reviewed", "approved"]:
            feedback, created = Feedback.objects.get_or_create(
                case=case,
                instructor=instructor,
                defaults={
                    "feedback_type": random.choice(
                        ["general", "clinical_reasoning", "documentation"]
                    ),
                    "content": f"Nhận xét chung về ca bệnh {case.title}",
                    "strengths": "Trình bày logic, có hệ thống, khai thác bệnh sử đầy đủ",
                    "areas_for_improvement": "Cần cải thiện phần khám lâm sàng, chú ý các dấu hiệu đặc trưng",
                    "recommendations": "Đọc thêm guidelines ESC/AHA, thực hành kỹ năng khám thực thể",
                    "is_public": True,
                },
            )
            if created:
                created_feedback += 1

    print(f"✅ Created {created_comments} comments")
    print(f"✅ Created {created_feedback} feedback entries")

    # Create Notifications
    print("\n🔔 Creating notifications...")
    created_notifications = 0

    # Grade notifications
    for grade in graded_cases[:20]:
        notif, created = Notification.objects.get_or_create(
            recipient=grade.case.student,
            notification_type="grade",
            related_case=grade.case,
            related_grade=grade,
            defaults={
                "title": "Bạn nhận được điểm mới",
                "message": f"Bệnh án '{grade.case.title}' đã được chấm điểm: {grade.score}/100",
                "action_url": f"/cases/{grade.case.id}",
                "is_read": random.choice([True, False]),
            },
        )
        if created:
            created_notifications += 1

    # Comment notifications
    for comment in Comment.objects.filter(is_instructor_feedback=True)[:15]:
        notif, created = Notification.objects.get_or_create(
            recipient=comment.case.student,
            notification_type="comment",
            related_case=comment.case,
            related_comment=comment,
            defaults={
                "title": "Góp ý mới từ giảng viên",
                "message": f"{comment.author.get_full_name()} đã góp ý về bệnh án '{comment.case.title}'",
                "action_url": f"/cases/{comment.case.id}#comments",
                "is_read": random.choice([True, False]),
            },
        )
        if created:
            created_notifications += 1

    # Submission notifications (to instructors)
    for case in created_cases[:10]:
        if case.case_status == "submitted":
            instructor = User.objects.filter(
                role="instructor", department=case.student.department
            ).first()
            if instructor:
                notif, created = Notification.objects.get_or_create(
                    recipient=instructor,
                    notification_type="submission",
                    related_case=case,
                    defaults={
                        "title": "Bệnh án mới cần đánh giá",
                        "message": f"{case.student.get_full_name()} đã nộp bệnh án '{case.title}'",
                        "action_url": f"/cases/{case.id}",
                        "is_read": random.choice([True, False]),
                    },
                )
                if created:
                    created_notifications += 1

    print(f"✅ Created {created_notifications} notifications")

    # Enforce and validate department scoping
    enforce_department_scoping()

    # Print summary
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE DATABASE SUMMARY")
    print("=" * 60)
    print(f"   🏥 Departments: {Department.objects.count()}")
    print(f"   👥 Total Users: {User.objects.count()}")
    print(f"      └─ Instructors: {User.objects.filter(role='instructor').count()}")
    print(f"      └─ Students: {User.objects.filter(role='student').count()}")
    print(f"      └─ Admins: {User.objects.filter(role='admin').count()}")
    print(f"   📁 Repositories: {Repository.objects.count()}")
    print(f"   🏥 Cases: {Case.objects.count()}")
    print(f"      └─ Draft: {Case.objects.filter(case_status='draft').count()}")
    print(f"      └─ Submitted: {Case.objects.filter(case_status='submitted').count()}")
    print(f"      └─ Reviewed: {Case.objects.filter(case_status='reviewed').count()}")
    print(f"      └─ Approved: {Case.objects.filter(case_status='approved').count()}")
    print(f"   📋 Clinical Histories: {ClinicalHistory.objects.count()}")
    print(f"   🩺 Physical Examinations: {PhysicalExamination.objects.count()}")
    print(f"   🧪 Investigations: {Investigations.objects.count()}")
    print(f"   💊 Diagnosis & Management: {DiagnosisManagement.objects.count()}")
    print(f"   🎯 Learning Outcomes: {LearningOutcomes.objects.count()}")
    print(f"   📊 Grades: {Grade.objects.count()}")
    print(f"   💬 Comments: {Comment.objects.count()}")
    print(f"   📝 Feedback: {Feedback.objects.count()}")
    print(f"   🔔 Notifications: {Notification.objects.count()}")

    print("\n" + "=" * 60)
    print("🔐 LOGIN CREDENTIALS")
    print("=" * 60)
    print("\n 👨‍💼 ADMIN:")
    print("   Email: admin@test.com")
    print("   Password: minh1234minh")

    print("\n 👨‍🏫 INSTRUCTORS (all use password: testpass123):")
    for instructor in User.objects.filter(role="instructor")[:5]:
        dept_name = (
            instructor.department.vietnamese_name if instructor.department else "N/A"
        )
        print(f"   • {instructor.email} - {dept_name}")

    print("\n 🎓 STUDENTS (sample - all use password: testpass123):")
    for student in User.objects.filter(role="student")[:10]:
        dept_name = student.department.vietnamese_name if student.department else "N/A"
        print(f"   • {student.email} - {dept_name} - {student.student_id}")

    print("\n" + "=" * 60)
    print("✅ COMPREHENSIVE TEST DATA SETUP COMPLETE!")
    print("=" * 60)
    print("\n🎉 All systems ready:")
    print("   ✅ User accounts with departments")
    print("   ✅ Clinical cases with full medical data")
    print("   ✅ Grades with detailed rubric scoring")
    print("   ✅ Comments and threaded discussions")
    print("   ✅ Instructor feedback")
    print("   ✅ Real-time notifications")
    print("\n💡 You can now test the complete platform!")
    print("=" * 60)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Populate test data with departmental scoping"
    )
    parser.add_argument(
        "--clear-existing",
        action="store_true",
        help="Clear existing non-admin data before populating",
    )
    args = parser.parse_args()
    create_test_data(clear_existing=args.clear_existing)
