#!/bin/bash
# Clean PaddleOCR model cache
# Run this script when changing model configurations to force re-download of only needed models

echo "🧹 Cleaning PaddleOCR model cache..."

CACHE_DIR="$HOME/.paddlex/official_models"

# Models we DON'T need for medical document OCR
UNUSED_MODELS=(
    "PP-Chart2Table"           # Chart recognition - disabled
    "PP-FormulaNet_plus-L"     # Formula recognition - disabled
    "UVDoc"                    # Document unwarping - disabled
    "PP-DocBlockLayout"        # Unused layout model
    "PP-DocLayout_plus-L"      # Unused layout model
    "PaddleOCR-VL"             # Vision-language model - not needed
    "PP-LCNet_x1_0_table_cls"  # Table classification - redundant
    # Keep these for table structure (if needed):
    # "SLANet_plus"
    # "SLANeXt_wired"
    # "RT-DETR-L_wired_table_cell_det"
    # "RT-DETR-L_wireless_table_cell_det"
)

# Models we NEED
REQUIRED_MODELS=(
    "PP-OCRv3_mobile_det"        # Mobile text detection (fast)
    "PP-OCRv5_server_rec"        # Server text recognition (accurate)
    "latin_PP-OCRv3_mobile_rec"  # Fallback recognition
    "PP-LCNet_x1_0_doc_ori"      # Document orientation
    "PP-LCNet_x1_0_textline_ori" # Textline orientation
)

echo ""
echo "📁 Cache directory: $CACHE_DIR"
echo ""

# Show current cache size
echo "Current cache contents:"
du -sh "$CACHE_DIR"/* 2>/dev/null | sort -h
echo ""

# Ask for confirmation before proceeding
read -p "Remove unused models? (y/N): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Cancelled."
    exit 0
fi

# Remove unused models
echo ""
echo "🗑️  Removing unused models..."
for model in "${UNUSED_MODELS[@]}"; do
    model_path="$CACHE_DIR/$model"
    if [ -d "$model_path" ]; then
        size=$(du -sh "$model_path" | cut -f1)
        echo "  Removing $model ($size)..."
        rm -rf "$model_path"
    fi
done

# Show remaining cache size
echo ""
echo "📊 Cache after cleanup:"
du -sh "$CACHE_DIR"/* 2>/dev/null | sort -h
echo ""
echo "Total:"
du -sh "$CACHE_DIR" 2>/dev/null

echo ""
echo "✅ Done! Restart Django server to apply changes."
echo ""
echo "Note: Missing models will be re-downloaded automatically when needed."
