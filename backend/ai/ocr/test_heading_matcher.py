#!/usr/bin/env python3
"""
Interactive heading matcher tester.
Tests how headings from OCR would be matched to form fields.

Usage:
    cd backend
    python ai/ocr/test_heading_matcher.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ai.ocr.heading_matcher import HeadingMatcher, FIELD_MAPPINGS

def main():
    print("=" * 60)
    print("Heading Matcher Interactive Tester")
    print("=" * 60)
    print(f"\nThreshold: 0.6 (60% similarity required)")
    print(f"Total fields: {len(FIELD_MAPPINGS)}")
    print(f"Total synonyms: {sum(len(v) for v in FIELD_MAPPINGS.values())}")
    print("\nLoading Vietnamese SBERT model...")
    
    matcher = HeadingMatcher(confidence_threshold=0.6)
    
    print("✅ Model loaded!\n")
    print("Type a heading to test (or 'quit' to exit):")
    print("-" * 60)
    
    while True:
        try:
            heading = input("\n🔍 Heading: ").strip()
        except EOFError:
            break
            
        if not heading or heading.lower() in ('quit', 'exit', 'q'):
            break
        
        # Get match
        field, score = matcher.match_heading(heading)
        
        print(f"\n📊 Results for: \"{heading}\"")
        print(f"   Best match: {field or 'NONE'}")
        print(f"   Confidence: {score:.3f} ({score*100:.1f}%)")
        print(f"   Decision:   {'✅ MATCHED' if field else '❌ REJECTED (below 0.6 threshold)'}")
        
        if field:
            # Show what synonyms this field has
            synonyms = FIELD_MAPPINGS.get(field, [])
            print(f"   Field synonyms: {synonyms[:3]}{'...' if len(synonyms) > 3 else ''}")
    
    print("\nGoodbye!")

if __name__ == "__main__":
    main()
