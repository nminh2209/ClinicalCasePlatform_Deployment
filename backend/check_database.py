#!/usr/bin/env python
"""
Check database status
"""

import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clinical_case_platform.settings_test")
django.setup()

from accounts.models import User
from cases.models import Case
from cases.medical_models import (
    ClinicalHistory,
    PhysicalExamination,
    Investigations,
    DiagnosisManagement,
    LearningOutcomes,
)

def check_database():
    print("🔍 Database Status Check")
    print("=" * 50)

    # Check users
    print(f"👥 Users: {User.objects.count()}")
    for user in User.objects.all():
        print(f"   {user.email} - {user.role} - {user.first_name} {user.last_name}")

    print()

    # Check cases
    print(f"🏥 Cases: {Case.objects.count()}")
    for case in Case.objects.all():
        print(f"   Case ID {case.id}: {case.title[:50]}...")
        print(f"      Student: {case.student.email}")
        print(f"      Status: {case.case_status}")

        # Check detailed sections
        has_clinical = hasattr(case, "clinical_history") and case.clinical_history
        has_physical = (
            hasattr(case, "physical_examination") and case.physical_examination
        )
        has_investigations = (
            hasattr(case, "investigations_detail") and case.investigations_detail
        )
        has_diagnosis = (
            hasattr(case, "diagnosis_management") and case.diagnosis_management
        )
        has_learning = hasattr(case, "learning_outcomes") and case.learning_outcomes

        print(
            f"      Detailed sections: Clinical={has_clinical}, Physical={has_physical}, Investigations={has_investigations}, Diagnosis={has_diagnosis}, Learning={has_learning}"
        )

    print()

    # Check medical sections
    print(f"📋 Clinical Histories: {ClinicalHistory.objects.count()}")
    print(f"🩺 Physical Examinations: {PhysicalExamination.objects.count()}")
    print(f"🧪 Investigations: {Investigations.objects.count()}")
    print(f"💊 Diagnosis Management: {DiagnosisManagement.objects.count()}")
    print(f"🎯 Learning Outcomes: {LearningOutcomes.objects.count()}")


if __name__ == "__main__":
    check_database()
