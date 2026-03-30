#!/usr/bin/env python3
"""
Standalone test script for PPStructure table/image extraction.
Run this outside the main system to avoid crashes.

Usage:
    cd backend
    conda activate projectb-ai
    python ai/ocr/test_ppstructure.py
"""

import os
import sys
import gc
import time

# Add backend to path
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


def clear_gpu_cache():
    """Clear GPU memory cache."""
    try:
        import paddle

        paddle.device.cuda.empty_cache()
        print("✅ Cleared PaddlePaddle GPU cache")
    except Exception as e:
        print(f"⚠️ Could not clear Paddle cache: {e}")

    try:
        import torch

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            print("✅ Cleared PyTorch GPU cache")
    except Exception as e:
        print(f"⚠️ Could not clear PyTorch cache: {e}")

    gc.collect()
    print("✅ Ran garbage collection")


def test_minimal_ppstructure():
    """Test PPStructure with absolute minimal configuration."""
    print("\n" + "=" * 60)
    print("TEST 1: Minimal PPStructureV3 Load Test")
    print("=" * 60)

    clear_gpu_cache()

    try:
        print("\n📦 Importing PPStructureV3...")
        start = time.time()
        from paddleocr import PPStructureV3

        print(f"   Import took {time.time() - start:.2f}s")

        print("\n🔧 Creating PPStructureV3 with MINIMAL config...")
        print("   - lang='vi'")
        print("   - use_table_recognition=True (needed for tables)")
        print("   - All other modules DISABLED")

        start = time.time()
        engine = PPStructureV3(
            lang="vi",
            # Core: Keep only table recognition
            use_table_recognition=True,
            # Disable EVERYTHING else
            use_chart_recognition=False,
            use_formula_recognition=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            use_seal_recognition=False,
            use_doc_orientation_classify=False,
        )
        print(f"   Initialization took {time.time() - start:.2f}s")
        print("✅ PPStructureV3 loaded successfully!")

        return engine

    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback

        traceback.print_exc()
        return None


def test_table_extraction(engine, image_path):
    """Test table extraction on a single image."""
    print("\n" + "=" * 60)
    print("TEST 2: Table Extraction Test")
    print("=" * 60)

    if engine is None:
        print("⚠️ Skipping - engine not loaded")
        return

    if not os.path.exists(image_path):
        print(f"⚠️ Test image not found: {image_path}")
        # Try to find any image in data folder
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        if os.path.exists(data_dir):
            for f in os.listdir(data_dir):
                if f.endswith((".png", ".jpg", ".jpeg")):
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

        results = engine.predict(image_path)

        elapsed = time.time() - start
        print(f"   Processing took {elapsed:.2f}s")

        # Parse results
        for i, result in enumerate(results):
            print(f"\n📄 Result {i+1}:")

            # Layout detection
            layout_det = result.get("layout_det_res", {})
            boxes = layout_det.get("boxes", [])
            print(f"   - Layout boxes: {len(boxes)}")
            for box in boxes[:5]:  # Show first 5
                print(
                    f"     • {box.get('label', 'unknown')}: {box.get('score', 0):.2f}"
                )

            # Tables
            table_res = result.get("table_res_list", [])
            print(f"   - Tables found: {len(table_res) if table_res else 0}")
            for j, table in enumerate(table_res or []):
                html = table.get("pred_html", "")
                print(f"     • Table {j+1}: {len(html)} chars HTML")

        print("\n✅ Table extraction completed!")
        return results

    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback

        traceback.print_exc()
        return None


def test_figure_detection(engine, image_path):
    """Test figure/image detection."""
    print("\n" + "=" * 60)
    print("TEST 3: Figure Detection Test")
    print("=" * 60)

    if engine is None:
        print("⚠️ Skipping - engine not loaded")
        return

    if not os.path.exists(image_path):
        print("⚠️ No test image found. Skipping.")
        return

    try:
        print(f"\n🔍 Looking for figures in: {image_path}")

        results = engine.predict(image_path)

        figures_found = []
        for result in results:
            layout_det = result.get("layout_det_res", {})
            boxes = layout_det.get("boxes", [])

            for box in boxes:
                label = box.get("label", "").lower()
                if label in ("figure", "image", "chart", "graph"):
                    figures_found.append(box)

        print(f"\n📊 Figures found: {len(figures_found)}")
        for fig in figures_found:
            print(
                f"   • {fig.get('label')}: score={fig.get('score', 0):.2f}, coord={fig.get('coordinate', [])[:4]}"
            )

        print("\n✅ Figure detection completed!")
        return figures_found

    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback

        traceback.print_exc()
        return None


def main():
    print("=" * 60)
    print("PPStructure Table/Image Extraction Test Suite")
    print("=" * 60)
    print(f"\nPython: {sys.executable}")
    print(f"CWD: {os.getcwd()}")

    # Default test image
    test_image = os.path.join(
        os.path.dirname(__file__), "data", "benhantonghop_page-07.png"
    )

    # Run tests
    engine = test_minimal_ppstructure()

    if engine:
        test_table_extraction(engine, test_image)
        test_figure_detection(engine, test_image)

    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETE")
    print("=" * 60)

    # Final cleanup
    clear_gpu_cache()


if __name__ == "__main__":
    main()
