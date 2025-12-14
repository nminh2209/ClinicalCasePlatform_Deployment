"""
Script to create missing medical section records for existing cases.
This ensures all cases have ClinicalHistory, PhysicalExamination, etc. records,
even if they're empty, so the API returns objects instead of null.

Run this with: python manage.py shell < fix_missing_medical_sections.py
Or: python manage.py shell
     >>> exec(open('fix_missing_medical_sections.py').read())
"""

from cases.models import Case
from cases.medical_models import (
    ClinicalHistory,
    PhysicalExamination,
    Investigations,
    DiagnosisManagement,
    LearningOutcomes,
)

def fix_missing_medical_sections():
    """Create missing medical section records for all existing cases"""
    
    cases = Case.objects.all()
    total_cases = cases.count()
    
    print(f"\n=== Checking {total_cases} cases for missing medical sections ===\n")
    
    fixed_counts = {
        'clinical_history': 0,
        'physical_examination': 0,
        'investigations': 0,
        'diagnosis_management': 0,
        'learning_outcomes': 0,
    }
    
    for case in cases:
        # Check and create ClinicalHistory
        if not hasattr(case, 'clinical_history'):
            ClinicalHistory.objects.create(
                case=case,
                chief_complaint="",
                history_present_illness=""
            )
            fixed_counts['clinical_history'] += 1
            print(f"✓ Created ClinicalHistory for case #{case.id}: {case.title}")
        
        # Check and create PhysicalExamination
        if not hasattr(case, 'physical_examination'):
            PhysicalExamination.objects.create(
                case=case,
                general_appearance="",
                vital_signs=""
            )
            fixed_counts['physical_examination'] += 1
            print(f"✓ Created PhysicalExamination for case #{case.id}: {case.title}")
        
        # Check and create Investigations
        if not hasattr(case, 'investigations_detail'):
            Investigations.objects.create(case=case)
            fixed_counts['investigations'] += 1
            print(f"✓ Created Investigations for case #{case.id}: {case.title}")
        
        # Check and create DiagnosisManagement
        if not hasattr(case, 'diagnosis_management'):
            DiagnosisManagement.objects.create(
                case=case,
                primary_diagnosis=""
            )
            fixed_counts['diagnosis_management'] += 1
            print(f"✓ Created DiagnosisManagement for case #{case.id}: {case.title}")
        
        # Check and create LearningOutcomes
        if not hasattr(case, 'learning_outcomes'):
            LearningOutcomes.objects.create(
                case=case,
                learning_objectives=""
            )
            fixed_counts['learning_outcomes'] += 1
            print(f"✓ Created LearningOutcomes for case #{case.id}: {case.title}")
    
    print(f"\n=== Summary ===")
    print(f"Total cases checked: {total_cases}")
    print(f"ClinicalHistory records created: {fixed_counts['clinical_history']}")
    print(f"PhysicalExamination records created: {fixed_counts['physical_examination']}")
    print(f"Investigations records created: {fixed_counts['investigations']}")
    print(f"DiagnosisManagement records created: {fixed_counts['diagnosis_management']}")
    print(f"LearningOutcomes records created: {fixed_counts['learning_outcomes']}")
    print(f"\nAll cases now have complete medical section records!")
    print(f"Cases will now display all sections in the frontend.\n")

if __name__ == '__main__':
    fix_missing_medical_sections()
