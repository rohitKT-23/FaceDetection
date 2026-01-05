# 🚀 GPU Training Setup - Step by Step Guide

## Step 1: Install Python 3.10

You need Python 3.10 for GPU support. Here's how:

### Option A: Download Python 3.10 (Easiest)

1. **Download Python 3.10.11** from:
   https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe

2. **Run the installer**:

   - ✅ Check "Add Python 3.10 to PATH"
   - ✅ Check "Install for all users" (optional)
   - Click "Install Now"

3. **Verify installation**:
   ```powershell
   py -3.10 --version
   ```
   Should show: `Python 3.10.11`

---

### Option B: Use Chocolatey (If you have it)

```powershell
choco install python --version=3.10.11
```

---

## Step 2: Create Virtual Environment

After installing Python 3.10:

```powershell
# Navigate to project
cd "d:\ROhit DELL G15\DS-IITG\FaceDetection"

# Create virtual environment with Python 3.10
py -3.10 -m venv venv-gpu

# Activate it
.\venv-gpu\Scripts\Activate.ps1
```

---

## Step 3: Install PyTorch with CUDA

```powershell
# Make sure venv is activated (you'll see (venv-gpu) in prompt)

# Install PyTorch with CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Verify GPU is detected
python -c "import torch; print('CUDA Available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No GPU')"
```

Expected output:

```
CUDA Available: True
GPU: NVIDIA GeForce RTX 3050 Laptop GPU
```

---

## Step 4: Install Other Dependencies

```powershell
pip install ultralytics opencv-python albumentations streamlit matplotlib pillow pyyaml tqdm pandas
```

---

## Step 5: Start GPU Training! 🚀

```powershell
python src/train.py --config configs/yolov8_face.yaml --model-size n
```

You should see:

```
Device: CUDA:0 (NVIDIA GeForce RTX 3050 Laptop GPU)
```

---

## ⚡ Quick Commands (Copy-Paste After Installing Python 3.10)

```powershell
# All in one - run after Python 3.10 is installed
cd "d:\ROhit DELL G15\DS-IITG\FaceDetection"
py -3.10 -m venv venv-gpu
.\venv-gpu\Scripts\Activate.ps1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install ultralytics opencv-python albumentations streamlit matplotlib pillow pyyaml tqdm pandas
python -c "import torch; print('CUDA:', torch.cuda.is_available())"
python src/train.py --config configs/yolov8_face.yaml --model-size n
```

---

## 🔧 Troubleshooting

### If PowerShell blocks script execution:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### If py -3.10 doesn't work after installation:

- Restart PowerShell
- Or use full path: `C:\Python310\python.exe -m venv venv-gpu`

---

## ⏱️ Time Estimate

- Download Python 3.10: 2 minutes
- Install Python 3.10: 2 minutes
- Create venv & install packages: 10 minutes
- **Total setup: ~15 minutes**
- **Training with GPU: 1-2 hours**

---

## 📥 Download Link

**Python 3.10.11 (64-bit)**:
https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe

Click the link, download, and install. Then come back and run the commands above!
