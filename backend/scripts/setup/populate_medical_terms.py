"""Populate a small set of medical terminology, ICD-10 codes and abbreviations for local testing.
Run: python populate_medical_terms.py
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import django
import sys

sys.path.append(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clinical_case_platform.settings")
django.setup()

from cases.medical_models import MedicalTerm, ICD10Code, MedicalAbbreviation

SAMPLE_TERMS = [
    {
        "term": "Sốt xuất huyết",
        "vietnamese_term": "Sốt xuất huyết",
        "english_term": "Dengue fever",
        "synonyms": ["SXH", "Dengue"],
        "definition": "Bệnh do virus Dengue gây ra, truyền qua muỗi Aedes.",
        "specialty": "Infectious Diseases",
    },
    {
        "term": "Viêm phổi",
        "vietnamese_term": "Viêm phổi",
        "english_term": "Pneumonia",
        "synonyms": ["Pneumonia"],
        "definition": "Nhiễm trùng nhu mô phổi.",
        "specialty": "Pulmonology",
    },
]

SAMPLE_ICD = [
    {
        "code": "A90",
        "description_en": "Dengue fever [classical dengue]",
        "description_vi": "Sốt xuất huyết Dengue",
    },
    {
        "code": "J18",
        "description_en": "Pneumonia, unspecified organism",
        "description_vi": "Viêm phổi không rõ tác nhân",
    },
]

SAMPLE_ABBR = [
    {"abbr": "BP", "expansion": "Blood Pressure", "description": "Huyết áp"},
    {"abbr": "HR", "expansion": "Heart Rate", "description": "Nhịp tim"},
]


def main():
    for t in SAMPLE_TERMS:
        MedicalTerm.objects.update_or_create(term=t["term"], defaults=t)
    for c in SAMPLE_ICD:
        ICD10Code.objects.update_or_create(code=c["code"], defaults=c)
    for a in SAMPLE_ABBR:
        MedicalAbbreviation.objects.update_or_create(abbr=a["abbr"], defaults=a)

    print("Populated sample medical terminology, ICD-10 codes and abbreviations")


if __name__ == "__main__":
    main()
