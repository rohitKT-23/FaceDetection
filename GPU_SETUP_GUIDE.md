# 🎮 GPU Training Setup - Python 3.14 Limitation

## ⚠️ Current Situation

You have:

- ✅ **NVIDIA GeForce RTX 3050 Laptop GPU** (4GB VRAM)
- ✅ **CUDA 13.0** installed
- ❌ **Python 3.14** (PyTorch with CUDA not yet available)

## 🔴 The Problem

PyTorch with CUDA support is **not yet available for Python 3.14**. The official PyTorch only supports up to Python 3.12 currently.

## ✅ Solutions

### **Option 1: Use Python 3.10-3.12 (RECOMMENDED for GPU Training)**

This is the best option for GPU training:

```bash
# Create new conda environment with Python 3.10
conda create -n face-gpu python=3.10
conda activate face-gpu

# Install PyTorch with CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install other dependencies
pip install ultralytics opencv-python albumentations streamlit matplotlib pillow pyyaml tqdm pandas

# Verify GPU is detected
python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0))"

# Start training with GPU
python src/train.py --config configs/yolov8_face.yaml --model-size n
```

**Advantages**:

- ✅ Full GPU acceleration (60+ FPS)
- ✅ Training will be 10-20x faster
- ✅ ONNX export available
- ✅ All features work

**Training Time Estimate**:

- With GPU: ~1-2 hours for 50 epochs
- With CPU: ~12-24 hours for 50 epochs

---

### **Option 2: Continue with Python 3.14 + CPU (Current Setup)**

Stay with Python 3.14 but train on CPU:

```bash
# Just continue training (already set up)
python src/train.py --config configs/yolov8_face.yaml --model-size n
```

**Advantages**:

- ✅ No environment changes needed
- ✅ Everything already installed

**Disadvantages**:

- ❌ Very slow training (12-24 hours)
- ❌ No GPU acceleration

---

### **Option 3: Reduce Training for Quick Testing**

If you want to test quickly on CPU first:

```bash
# Train for just 10 epochs to test
python src/train.py --config configs/yolov8_face.yaml --model-size n
```

Then edit `configs/yolov8_face.yaml` and change:

```yaml
epochs: 10 # Instead of 50
batch: 8 # Reduce batch size for faster iteration
```

---

## 🎯 My Recommendation

**For this project, I strongly recommend Option 1** (Python 3.10 + GPU):

1. **Create Python 3.10 environment** (5 minutes)
2. **Install dependencies** (10 minutes)
3. **Train with GPU** (1-2 hours vs 12-24 hours)

The time saved in training (20+ hours) is worth the 15 minutes to set up a new environment.

## 📋 Quick Setup Commands (Option 1)

```bash
# 1. Create environment
conda create -n face-gpu python=3.10 -y
conda activate face-gpu

# 2. Navigate to project
cd "d:\ROhit DELL G15\DS-IITG\FaceDetection"

# 3. Install PyTorch with CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 4. Install other packages
pip install ultralytics opencv-python albumentations streamlit matplotlib pillow pyyaml tqdm pandas

# 5. Verify GPU
python -c "import torch; print('CUDA Available:', torch.cuda.is_available())"

# 6. Start training
python src/train.py --config configs/yolov8_face.yaml --model-size n
```

## ⏱️ Time Comparison

| Setup                 | Training Time (50 epochs) | Total Time |
| --------------------- | ------------------------- | ---------- |
| **Python 3.10 + GPU** | 1-2 hours                 | ~1.5 hours |
| **Python 3.14 + CPU** | 12-24 hours               | ~18 hours  |

**Time saved: ~16 hours!** 🚀

## 🤔 What Should You Do?

**If you want fast training and the best results**: Use Option 1 (Python 3.10 + GPU)

**If you want to test quickly first**: Use Option 3 (reduce epochs to 10)

**If you're okay waiting overnight**: Continue with current CPU training

Let me know which option you'd like to proceed with!
