#!/usr/bin/env python
"""
Add detailed ICU case from Lê Thị Huyền
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clinical_case_platform.settings_test")
django.setup()
from datetime import date
from accounts.models import User
from cases.models import Case
from cases.medical_models import (
    Department,
    ClinicalHistory,
    PhysicalExamination,
    Investigations,
    DiagnosisManagement,
    LearningOutcomes,
)
from repositories.models import Repository
from templates.models import CaseTemplate

# Setup Django environment


def create_icu_case():
    print("🏥 Creating detailed ICU case...")

    # Get required objects
    student = User.objects.get(email="student@test.com")
    # instructor = User.objects.get(email="instructor@test.com")
    # hstc_dept = Department.objects.get(code="HSTC")
    repo = Repository.objects.first()
    template = CaseTemplate.objects.first()

    # Create the main case
    icu_case, created = Case.objects.get_or_create(
        title="Suy hô hấp cấp mức độ nặng - Viêm phổi - HSTC",
        defaults={
            "student": student,
            "template": template,
            "repository": repo,
            "patient_name": "NGUYỄN HỒNG ĐIỆP (ẩn danh)",
            "patient_age": 71,
            "patient_gender": "male",
            "medical_record_number": "HST001",
            "admission_date": date(2025, 3, 25),
            "specialty": "Hồi sức tích cực",
            "keywords": "suy hô hấp, viêm phổi, suy tim, thở máy, HSTC",
            "case_status": "reviewed",
            # Legacy fields for backward compatibility
            "history": "BN nam 71 tuổi, tiền sử tăng huyết áp, suy tim nhiều năm. Xuất hiện khó thở 9 ngày...",
            "examination": "BN an thần, thở máy qua nội khí quản. Da niêm mạc hồng, không phù...",
            "diagnosis": "Suy hô hấp cấp mức độ nặng - Viêm phổi - Tràn dịch màng phổi trái - Suy tim EF 40%",
            "treatment": "Thở máy xâm nhập, kháng sinh, điều trị suy tim...",
        },
    )

    if created:
        # Create detailed clinical history
        ClinicalHistory.objects.create(
            case=icu_case,
            chief_complaint="Khó thở",
            history_present_illness="""BN nam 71 tuổi, tiền sử tăng huyết áp, suy tim nhiều năm.
Cách vào khoa 9 ngày (17/3), bệnh nhân xuất hiện khó thở, khó thở cả 2 thì, kèm theo ho khan, không sốt, không đau ngực, không điều trị gì. 
Ngày 20/3, bệnh nhân khó thở tăng, ho đờm trắng đục số lượng tăng dần, ngày sốt 3 cơn, nhiệt độ cao, được đưa vào BV Thanh Nhàn với chẩn đoán Viêm phổi - Suy tim, điều trị tại khoa thận thở oxy kính, kháng sinh (Imipenem 500mg/12h x 2 ngày + Delivir 2g/24h x 2 ngày), kiểm soát huyết áp.
Ngày 23/3, bệnh nhân xuất hiện đi ngoài phân lỏng 10 lần/ngày.
Ngày 25/3, bệnh nhân khó thở tăng, được thở BiPAP chuyển trung tâm cấp cứu A9 được chẩn đoán Viêm phổi/ Suy tim - THA điều trị thở oxy mask túi 10l/p, kháng sinh (Meropenem + Ciprofloxacin), siêu âm tim sơ bộ, EF 40%, ít dịch màng ngoài tim, ít dịch màng phổi trái, chuyển HSTC.""",
            past_medical_history="""- Suy tim
- THA 10 năm đang dùng thuốc không rõ loại
- Chưa phát hiện bệnh lý mạn tính khác""",
            family_history="Chưa phát hiện bất thường",
            social_history="Chưa phát hiện bất thường về chế độ ăn uống, sinh hoạt, môi trường",
            allergies="Chưa phát hiện dị ứng",
            medications="Thuốc điều trị THA (không rõ loại cụ thể)",
            review_systems="Không sốt, không đau ngực ban đầu, sau đó xuất hiện sốt và ho đờm",
        )

        # Create physical examination
        PhysicalExamination.objects.create(
            case=icu_case,
            general_appearance="Bệnh nhân an thần, thở máy qua nội khí quản",
            vital_signs="BP: 130/80 mmHg, HR: 96 lần/phút, T: 37°C, SpO2: 92%, RR: 22 lần/phút",
            head_neck="Tuyến giáp không to, hạch ngoại vi không sờ thấy",
            cardiovascular="""- Lồng ngực bình thường, cân đối
- Mỏm tim khoang liên sườn V, đường giữa đòn T
- Không có rung miu, chạm dội Bard
- Nhịp tim đều, tần số 96 lần/phút
- T1, T2 rõ; không thấy tiếng thổi bất thường""",
            respiratory="""- BN thở máy qua ống nội khí quản số 8 (VCV, vT 420ml, FiO2 80%), cố định ống ngang mức 22- cung răng trên, tại mép môi bên phải, ống nhiều đờm dãi, ko bị gập ống
- Lồng ngực BN cân đối, di động tốt, không co kéo cơ hô hấp phụ, chưa phát hiện teo cơ hô hấp, không phát hiện kiểu thở bất thường
- Nhịp thở 22l/p
- Hội chứng đông đặc (+), hội chứng galliard (-)
- 01 catether dẫn lưu màng phổi trái, dẫn lưu được ~ 100ml dịch
- Phổi thông khí đều 2 bên
- Rale rít, rale ẩm rải rác 2 đáy phổi""",
            abdominal="""- Bụng mềm, cân đối, không chướng
- Gan lách không sờ thấy
- Dấu hiệu phản hồi gan - tĩnh mạch (-)
- Phản ứng thành bụng (-), cảm ứng phúc mạc (-)""",
            neurological="Bệnh nhân an thần, RASS -2. Đồng tử 2 bên 2mm, PXAS (+)",
            musculoskeletal="Chi dưới 2 bên cân đối, không sưng nóng đỏ đau, tím bất thường",
            skin="Da niêm mạc hồng, không phù",
        )

        # Create investigations
        Investigations.objects.create(
            case=icu_case,
            laboratory_results="""Khí máu động mạch (6h 28/3):
- pH: 7.313, pCO2: 40 mmHg, pO2: 90.5 mmHg
- HCO3: 20.44 mmol/L, BE: -6 mmol/L
- FiO2: 100%, P/F: 80.2
- Lactat: 2.1 mmol/L

Bilan nhiễm trùng (3h 28/3):
- Bạch cầu: 6.53, NEU%: 83%
- PCT: 4.64 ng/L, CRPhs: 49.5""",
            imaging_studies="""X-quang ngực thẳng:
- Bóng tim hạn chế đánh giá
- Trung thất cân đối, không rộng
- Mờ không đồng nhất trường phổi trái - theo dõi viêm
- Góc sườn hoành trái hạn chế đánh giá, bên phải nhọn
- Xương và phần mềm thành ngực không thấy bất thường

Siêu âm tim sơ bộ:
- Thất phải co bóp được, EF sơ bộ >50%
- Thành thất trái kissing wall
- Thất phải không giãn
- E/E' 11,54
- Ít dịch màng phổi trái""",
            ecg_findings="""Điện tâm đồ 26/3:
- Nhịp xoang 74 lần/phút
- Không có ST chênh lên
- Không thấy sóng Q sâu ở D1, Q sâu ở D3
- Trục tim lệch phải nhẹ
=> Không thấy nguy cơ thuyên tắc phổi trên điện tâm đồ""",
            special_tests="Nhuộm soi đờm trực tiếp (27/3): Vi nấm soi tươi (+), Vi khuẩn nhuộm soi (-), AFB đờm (-)",
            biochemistry="""NT-proBNP: 2839 pg/mL
Na/K/Cl: 137/4.8/105 mmol/L
Ure/Creatinin: 13.2/81 mmol/L
Bil TP/TT: 7.1/4.3 umol/L
AST/ALT: 144/25 umol/L""",
            hematology="""Hb: 119, Tiểu cầu: 72
APTT: 40.4s, APTT (bệnh/chứng): 1.36
Fibrinogen: 4.56 g/L
D-Dimer: 1.849 mg/l""",
        )

        # Create diagnosis and management
        DiagnosisManagement.objects.create(
            case=icu_case,
            primary_diagnosis="Suy hô hấp cấp mức độ nặng - Viêm phổi nặng (CURB65 3đ) có biến chứng suy hô hấp, có nguy cơ nhiễm nấm - Tràn dịch màng phổi trái - Suy tim EF 40%",
            differential_diagnosis="""- Suy hô hấp do phù phổi cấp
- Suy hô hấp do thuyên tắc động mạch phổi
- Đợt cấp suy tim""",
            treatment_plan="""Hỗ trợ Hô hấp và Cai máy thở:
- Tiếp tục thở máy xâm nhập qua NKQ (VCV, Vt 420ml, PEEP 10, FiO2 80%)
- Mục tiêu: Duy trì oxy hóa máu (SpO2 90-95%, PaO2 > 60 mmHg)
- Quản lý đường thở: Hút đờm thường xuyên, hiệu quả

Điều trị viêm phổi:
- Kháng sinh theo kinh nghiệm, thêm thuốc kháng nấm
- Kiểm soát nguồn nhiễm trùng
- Phục hồi chức năng hô hấp

Tràn dịch màng phổi trái:
- Tiếp tục để catether dẫn lưu
- Dùng lợi tiểu""",
            medications_prescribed="Kháng sinh (Meropenem + Ciprofloxacin), thuốc kháng nấm, lợi tiểu, PPI",
            procedures_performed="Đặt nội khí quản, thở máy, dẫn lưu màng phổi trái",
            follow_up_plan="Theo dõi chặt chẽ tại HSTC, đánh giá khả năng cai máy thở, xử trí biến chứng",
            prognosis="Tiên lượng phụ thuộc vào đáp ứng điều trị và kiểm soát nhiễm trùng",
            complications="Nguy cơ viêm phổi thở máy, nhiễm khuẩn huyết, tổn thương phổi do máy thở",
        )

        # Create learning outcomes
        LearningOutcomes.objects.create(
            case=icu_case,
            learning_objectives="""1. Nhận biết và quản lý suy hô hấp cấp mức độ nặng
2. Hiểu biết về viêm phổi nặng và chỉ định thở máy
3. Quản lý bệnh nhân thở máy tại HSTC
4. Đánh giá và xử trí tràn dịch màng phổi
5. Quản lý suy tim cấp tính""",
            key_concepts="""- EPA (Entrustable Professional Activities) trong HSTC
- CURB65 score đánh giá mức độ nặng viêm phổi
- Chỉ định và quản lý thở máy xâm nhập
- Hội chứng suy hô hấp và phân loại
- Bilan dịch và quản lý dịch tại HSTC""",
            clinical_pearls="""- SpO2 < 90% không đáp ứng với oxy mask là chỉ định thở máy
- CURB65 ≥ 3 điểm cần điều trị tích cực tại ICU
- Theo dõi P/F ratio để đánh giá mức độ suy hô hấp
- Vi nấm soi tươi (+) cần thêm thuốc kháng nấm
- NT-proBNP giúp phân biệt nguyên nhân suy hô hấp""",
            references="""1. Hướng dẫn chẩn đoán và điều trị viêm phổi - Bộ Y tế 2024
2. ARDS Definition Task Force 2012
3. Surviving Sepsis Campaign Guidelines 2021
4. Vietnamese ICU Guidelines 2023""",
            discussion_points="""1. Khi nào chỉ định thở máy xâm nhập?
2. Cách đánh giá và theo dõi bệnh nhân thở máy
3. Phân biệt suy hô hấp do viêm phổi vs phù phổi cấp
4. Chiến lược cai máy thở
5. Phòng ngừa biến chứng tại HSTC""",
            assessment_criteria="""- Đánh giá tình trạng suy hô hấp (25%)
- Chỉ định và quản lý thở máy (30%)
- Chẩn đoán phân biệt (20%)
- Kế hoạch điều trị và theo dõi (25%)""",
        )

        print(f"✅ Detailed ICU case created: {icu_case.title}")
        print("   📋 Clinical History: ✓")
        print("   🩺 Physical Examination: ✓")
        print("   🧪 Investigations: ✓")
        print("   💊 Diagnosis & Management: ✓")
        print("   🎯 Learning Outcomes: ✓")
    else:
        print("✅ ICU case already exists: {icu_case.title}")

    # Update summary
    print("\n📊 Updated Database Summary:")
    print(f"   🏥 Departments: {Department.objects.count()}")
    print(f"   👥 Users: {User.objects.count()}")
    print(f"   📁 Repositories: {Repository.objects.count()}")
    print(f"   📝 Templates: {CaseTemplate.objects.count()}")
    print(f"   🏥 Cases: {Case.objects.count()}")
    print(f"   📋 Clinical Histories: {ClinicalHistory.objects.count()}")
    print(f"   🩺 Physical Examinations: {PhysicalExamination.objects.count()}")
    print(f"   🧪 Investigations: {Investigations.objects.count()}")
    print(f"   💊 Diagnosis & Management: {DiagnosisManagement.objects.count()}")
    print(f"   🎯 Learning Outcomes: {LearningOutcomes.objects.count()}")


if __name__ == "__main__":
    create_icu_case()
