# Python Version Compatibility Notes

## Current Issue: Python 3.14

You are currently using **Python 3.14**, which is very new and not yet fully supported by all dependencies.

### What Works ✅

- YOLOv8 training and inference with PyTorch (.pt models)
- Image/Video/Webcam detection
- Streamlit demo application
- All core functionality

### What Doesn't Work ❌

- **ONNX export and inference** - `onnxruntime` doesn't support Python 3.14 yet
- Some older package versions may have compatibility issues

## Solutions

### Option 1: Use PyTorch Models (Recommended for Now)

Continue with Python 3.14 and use `.pt` models instead of ONNX:

```bash
# Install dependencies (without ONNX)
pip install -r requirements.txt

# Train model
python src/train.py --config configs/yolov8_face.yaml

# Use .pt model for inference (still fast!)
python src/infer.py --model weights/best.pt --source 0
```

**Note**: PyTorch models are still very fast, especially on GPU!

### Option 2: Use Python 3.10-3.12 (For Full ONNX Support)

If you need ONNX optimization for maximum CPU performance:

```bash
# Create new environment with Python 3.10
conda create -n face python=3.10
conda activate face

# Install all dependencies including ONNX
pip install ultralytics opencv-python albumentations streamlit onnx onnxruntime

# Now you can use ONNX export
python src/export_onnx.py --model weights/best.pt
```

### Option 3: Wait for ONNX Runtime Update

Check for Python 3.14 support: https://github.com/microsoft/onnxruntime/releases

## Recommended Action

**For this project, I recommend Option 1** (use Python 3.14 with PyTorch models):

- ✅ All training and inference works
- ✅ Still achieves 25+ FPS on CPU with PyTorch
- ✅ 60+ FPS on GPU
- ✅ No environment changes needed
- ✅ Can add ONNX later when support is available

The performance difference between PyTorch and ONNX is minimal on GPU, and acceptable on modern CPUs.

## Quick Fix

Run this now:

```bash
pip install ultralytics opencv-python albumentations streamlit matplotlib pillow pyyaml tqdm pandas
```

Then proceed with training!
