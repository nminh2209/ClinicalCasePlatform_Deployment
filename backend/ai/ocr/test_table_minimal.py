#!/usr/bin/env python3
"""
Ultra-minimal table extraction test using only essential PaddleX models.
Bypasses full PPStructureV3 to avoid loading 1.4GB PP-Chart2Table.

Usage:
    cd backend
    conda activate projectb-ai
    python ai/ocr/test_table_minimal.py
"""

import os
import sys
import gc
import time

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def clear_gpu_cache():
    """Clear GPU memory cache."""
    gc.collect()
    try:
        import paddle
        paddle.device.cuda.empty_cache()
        print("✅ Cleared PaddlePaddle GPU cache")
    except:
        pass
    try:
        import torch
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            print("✅ Cleared PyTorch GPU cache")
    except:
        pass

def test_slanet_only():
    """Test using only SLANet table structure model - bypasses PPStructureV3."""
    print("\n" + "="*60)
    print("TEST: SLANet-only Table Extraction")
    print("="*60)
    
    clear_gpu_cache()
    
    try:
        print("\n📦 Importing PaddleX pipeline...")
        start = time.time()
        
        # Try direct model loading instead of PPStructureV3
        from paddlex import create_pipeline
        
        print(f"   Import took {time.time() - start:.2f}s")
        
        # Use only table recognition pipeline - should be much lighter
        print("\n🔧 Creating table_recognition pipeline...")
        start = time.time()
        
        pipeline = create_pipeline(
            pipeline="table_recognition",
            device="cpu",  # Force CPU to avoid GPU memory issues
        )
        
        print(f"   Pipeline creation took {time.time() - start:.2f}s")
        print("✅ Table recognition pipeline loaded!")
        
        return pipeline
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_paddleocr_legacy():
    """Test using legacy PaddleOCR PPStructure (v2) instead of v3."""
    print("\n" + "="*60)
    print("TEST: Legacy PPStructure (v2) Table Extraction")
    print("="*60)
    
    clear_gpu_cache()
    
    try:
        print("\n📦 Importing PPStructure (legacy)...")
        start = time.time()
        
        from paddleocr import PPStructure
        
        print(f"   Import took {time.time() - start:.2f}s")
        
        print("\n🔧 Creating PPStructure (legacy) with minimal config...")
        start = time.time()
        
        # Legacy PPStructure - should be lighter than v3
        engine = PPStructure(
            lang='vi',
            show_log=True,
            table=True,
            ocr=False,  # Disable OCR, just do table structure
            layout=True,
            use_gpu=False,  # Force CPU
        )
        
        print(f"   Initialization took {time.time() - start:.2f}s")
        print("✅ PPStructure (legacy) loaded!")
        
        return engine
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_table_extraction(engine, image_path, is_legacy=False):
    """Test table extraction on a single image."""
    print("\n" + "="*60)
    print("TEST: Table Extraction")
    print("="*60)
    
    if engine is None:
        print("⚠️ Skipping - engine not loaded")
        return
    
    if not os.path.exists(image_path):
        print(f"⚠️ Test image not found: {image_path}")
        # Try to find any image in data folder
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        if os.path.exists(data_dir):
            for f in os.listdir(data_dir):
                if f.endswith(('.png', '.jpg', '.jpeg')):
                    image_path = os.path.join(data_dir, f)
                    print(f"   Using: {image_path}")
                    break
    
    if not os.path.exists(image_path):
        print("⚠️ No test image found. Skipping extraction test.")
        return
    
    clear_gpu_cache()
    
    try:
        print(f"\n📷 Processing: {image_path}")
        start = time.time()
        
        if is_legacy:
            # Legacy API
            from PIL import Image
            import numpy as np
            img = np.array(Image.open(image_path))
            results = engine(img)
        else:
            # PaddleX pipeline API
            results = engine.predict(image_path)
        
        elapsed = time.time() - start
        print(f"   Processing took {elapsed:.2f}s")
        
        print(f"\n📊 Results: {type(results)}")
        if isinstance(results, list):
            print(f"   Found {len(results)} result(s)")
            for i, r in enumerate(results[:3]):
                print(f"   Result {i}: {type(r)}")
                if isinstance(r, dict):
                    for k in list(r.keys())[:5]:
                        print(f"     - {k}: {type(r[k])}")
        
        print("\n✅ Table extraction completed!")
        return results
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("="*60)
    print("Minimal Table Extraction Test Suite")
    print("="*60)
    print(f"\nPython: {sys.executable}")
    print(f"CWD: {os.getcwd()}")
    
    # Default test image
    test_image = os.path.join(os.path.dirname(__file__), "data", "benhantonghop_page-07.png")
    
    # Test 1: Try SLANet-only pipeline
    print("\n\n" + "="*60)
    print("APPROACH 1: PaddleX table_recognition pipeline")
    print("="*60)
    pipeline = test_slanet_only()
    if pipeline:
        test_table_extraction(pipeline, test_image)
    
    clear_gpu_cache()
    
    # Test 2: Try legacy PPStructure
    print("\n\n" + "="*60)
    print("APPROACH 2: Legacy PPStructure (v2)")
    print("="*60)
    legacy = test_paddleocr_legacy()
    if legacy:
        test_table_extraction(legacy, test_image, is_legacy=True)
    
    print("\n" + "="*60)
    print("TEST SUITE COMPLETE")
    print("="*60)
    
    clear_gpu_cache()

if __name__ == "__main__":
    main()
