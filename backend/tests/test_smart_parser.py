
import sys
import os
import django
from django.conf import settings

# Setup Django standalone
sys.path.append('/home/zilus/Desktop/SwinCode/Sem7/HN2.1ProjectA/backend')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clinical_case_platform.settings")
django.setup()

from ai.ocr.ocr_service import ocr_service
import json

def test_parsing():
    # Read the provided raw text
    with open('/home/zilus/Desktop/SwinCode/Sem7/HN2.1ProjectA/return.txt', 'r') as f:
        raw_text = f.read()
    
    print("--- RAW TEXT ---")
    print(raw_text[:200] + "...")
    print("----------------")
    
    # Run parsing logic
    structured_data = ocr_service._extract_structured_data(raw_text)
    
    print("\n--- EXTRACTED DATA ---")
    print(json.dumps(structured_data, indent=2, ensure_ascii=False))
    
    # Assertions
    print("\n--- VERIFICATION ---")
    
    # Admin fields
    name = structured_data.get('patient_name')
    age = structured_data.get('patient_age')
    
    if "NGUYỄN" in str(name):
        print(f"[PASS] Patient Name found: {name}")
    else:
        print(f"[FAIL] Patient Name extraction failed: {name}")
        
    if str(age) == "71":
        print(f"[PASS] Age found: {age}")
    else:
        print(f"[FAIL] Age extraction failed: {age}")
        
    # Clinical fields
    history = structured_data.get('clinical_history', {}).get('history_present_illness')
    if history and "BN nam 71 tuổi" in history:
        print("[PASS] History of Present Illness extracted correctly")
    else:
        print(f"[FAIL] HPI extraction failed: {history}")

    chief_complaint = structured_data.get('clinical_history', {}).get('chief_complaint')
    # Note: Text says "Lý do vào vin: Khó th"
    # Fuzzy match should catch "Lý do vào vin"
    # Content should be "Khó th" (OCR typo for Khó thở)
    print(f"Chief Complaint: {chief_complaint}")
    if chief_complaint:
         print("[PASS] Chief Complaint extracted")
    else:
         print("[FAIL] Chief Complaint NOT extracted")

if __name__ == "__main__":
    test_parsing()
