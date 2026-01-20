#!/usr/bin/env python
"""
OCR Smoke Test - Tests OCR improvements with GPU monitoring
"""
import os
import sys
import time
import gc

# Add backend to path
sys.path.insert(0, '/home/zilus/Desktop/SwinCode/Sem7/HN2.1ProjectA/backend')
os.chdir('/home/zilus/Desktop/SwinCode/Sem7/HN2.1ProjectA/backend')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinical_case_platform.settings')

# Force ASR disabled
os.environ['ASR_ENABLED'] = 'false'

import django
django.setup()

import torch

def get_gpu_memory():
    """Get current GPU memory usage in MB"""
    if torch.cuda.is_available():
        return {
            'allocated': torch.cuda.memory_allocated() / 1024**2,
            'reserved': torch.cuda.memory_reserved() / 1024**2,
        }
    return {'allocated': 0, 'reserved': 0}

def clear_gpu():
    """Clear GPU memory"""
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
    print("✅ GPU cache cleared")

def main():
    print("=" * 60)
    print("OCR Smoke Test - Page 7")
    print("=" * 60)
    
    # Test file
    test_file = "/home/zilus/Desktop/SwinCode/Sem7/HN2.1ProjectA/backend/ai/ocr/data/benhantonghop_page-07.png"
    
    if not os.path.exists(test_file):
        print(f"❌ Test file not found: {test_file}")
        return
    
    print(f"📄 Test file: {test_file}")
    print(f"📊 File size: {os.path.getsize(test_file) / 1024:.1f} KB")
    print()
    
    # Clear GPU before test
    print("🧹 Clearing GPU memory...")
    clear_gpu()
    mem_before = get_gpu_memory()
    print(f"   GPU before: {mem_before['allocated']:.1f} MB allocated, {mem_before['reserved']:.1f} MB reserved")
    print()
    
    # Import OCR service
    print("📦 Loading OCR service...")
    from ai.ocr.ocr_service import OCRService
    
    ocr = OCRService()
    
    # Run OCR
    print("🔄 Running OCR...")
    start_time = time.time()
    
    try:
        result = ocr.process(test_file)
        elapsed = time.time() - start_time
        
        # Get GPU memory after
        mem_after = get_gpu_memory()
        
        print()
        print("=" * 60)
        print("✅ OCR RESULTS")
        print("=" * 60)
        print(f"⏱️  Time: {elapsed:.2f}s ({result.get('metadata', {}).get('elapsed_ms', 0)}ms reported)")
        print(f"📑 Pages: {result.get('metadata', {}).get('page_count', 0)}")
        print(f"🔧 Engine: {result.get('metadata', {}).get('engine', 'unknown')}")
        print(f"👷 Workers: {result.get('metadata', {}).get('parallel_workers', 1)}")
        print()
        
        # Text preview
        text = result.get('text', '')
        print(f"📝 Text extracted: {len(text)} characters")
        if text:
            preview = text[:500].replace('\n', ' ')
            print(f"   Preview: {preview}...")
        else:
            print("   ⚠️ NO TEXT EXTRACTED!")
        print()
        
        # GPU memory
        print("💾 GPU Memory:")
        print(f"   Before: {mem_before['allocated']:.1f} MB allocated")
        print(f"   After:  {mem_after['allocated']:.1f} MB allocated")
        print(f"   Delta:  {mem_after['allocated'] - mem_before['allocated']:.1f} MB")
        print()
        
        # Success/Fail
        if text and len(text) > 50:
            print("=" * 60)
            print("🎉 TEST PASSED - OCR working correctly!")
            print("=" * 60)
        else:
            print("=" * 60)
            print("❌ TEST FAILED - No/insufficient text extracted")
            print("=" * 60)
            
    except Exception as e:
        print(f"❌ OCR FAILED: {e}")
        import traceback
        traceback.print_exc()
        
        # Check GPU memory on failure
        mem_after = get_gpu_memory()
        print(f"\n💾 GPU Memory on failure: {mem_after['allocated']:.1f} MB")

if __name__ == '__main__':
    main()
