#!/bin/bash
set -e

echo "🚀 Starting OCR GPU Upgrade..."

# 1. Uninstall existing CPU versions
echo "🧹 Uninstalling CPU versions..."
pip uninstall -y paddlepaddle paddlepaddle-gpu torch torchvision torchaudio

# 2. Install PyTorch with CUDA support
# GTX 1650 supports this. 
echo "🔥 Installing PyTorch (CUDA 12.1)..."
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# 3. Install PaddlePaddle (Standard - fallback if GPU wheel missing for py3.13)
# Note: Detection (Paddle) might run on CPU, but Recognition (VietOCR) uses Torch on GPU
echo "🔥 Installing PaddlePaddle (Standard)..."
pip install paddlepaddle>=2.6.0

# 4. Verification
echo "🔍 Verifying installation..."
python -c "
import torch
import paddle
print('-----------------------------------')
print(f'Torch Version: {torch.__version__}')
print(f'Torch CUDA Available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'Torch Device: {torch.cuda.get_device_name(0)}')

print('-----------------------------------')
print(f'Paddle Version: {paddle.__version__}')
print(f'Paddle Device: {paddle.device.get_device()}')
if 'gpu' in paddle.device.get_device():
    print('Paddle GPU: CHECKED')
print('-----------------------------------')
"

echo "✅ Upgrade script finished."
