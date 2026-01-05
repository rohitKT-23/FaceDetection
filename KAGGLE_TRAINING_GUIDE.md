# 🚀 Kaggle Par Face Detection Training - Complete Guide

## Kyun Kaggle?

✅ **Free GPU** - Tesla P100 ya T4 GPU (30 hours/week free)  
✅ **Fast Training** - 1-2 hours mein training complete  
✅ **No Setup** - Sab kuch pre-installed  
✅ **Free Dataset Storage** - WIDER FACE dataset already available

---

## Step-by-Step Guide

### Step 1: Kaggle Account Setup (5 minutes)

1. **Kaggle par jao**: https://www.kaggle.com
2. **Sign up/Login** karo (Google account se bhi kar sakte ho)
3. **Phone Verification** karo (GPU access ke liye zaroori hai)
   - Settings → Account → Phone Verification

---

### Step 2: Dataset Add Karo (10 minutes)

#### Option A: Kaggle ka WIDER FACE Dataset Use Karo (Recommended)

1. Kaggle par search karo: "WIDER FACE"
2. Yeh dataset use karo: https://www.kaggle.com/datasets/sujaykapadnis/widerface
3. Click on **"+ New Notebook"**

#### Option B: Apna Dataset Upload Karo

1. Kaggle → Datasets → New Dataset
2. Apna converted dataset upload karo (agar local mein hai)

---

### Step 3: New Notebook Banao

1. **Kaggle → Code → New Notebook**
2. **Settings** (right side) mein jao:
   - **Accelerator**: GPU T4 x2 (ya P100) select karo ✅
   - **Internet**: ON karo ✅
   - **Persistence**: Files Only

---

### Step 4: GitHub Repo Clone Karo

Notebook mein yeh code run karo:

```python
# Cell 1: Clone your GitHub repository
!git clone https://github.com/rohitKT-23/FaceDetection.git
%cd FaceDetection
!ls -la
```

---

### Step 5: Dependencies Install Karo

```python
# Cell 2: Install required packages
!pip install ultralytics opencv-python albumentations matplotlib pillow pyyaml tqdm pandas -q

# Verify GPU
import torch
print(f"CUDA Available: {torch.cuda.is_available()}")
print(f"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No GPU'}")
```

Expected Output:

```
CUDA Available: True
GPU: Tesla T4
```

---

### Step 6: WIDER FACE Dataset Setup

#### Option A: Kaggle Dataset Use Karo

```python
# Cell 3: Add Kaggle WIDER FACE dataset
# Notebook settings mein "Add Data" → Search "WIDER FACE" → Add

# Dataset path check karo
!ls /kaggle/input/
```

#### Option B: Dataset Download Karo

```python
# Cell 3: Download WIDER FACE dataset
!mkdir -p dataset
%cd dataset

# Download training set
!wget http://shuoyang1213.me/WIDERFACE/WIDERFace.zip
!unzip -q WIDERFace.zip

%cd ..
```

---

### Step 7: Dataset Convert Karo (Agar Kaggle dataset use kar rahe ho)

```python
# Cell 4: Convert WIDER FACE to YOLO format
!python src/convert_dataset.py \
    --wider-root /kaggle/input/widerface \
    --output-root data/widerface \
    --splits train val
```

---

### Step 8: Config File Update Karo

```python
# Cell 5: Update config for Kaggle paths
import yaml

config_path = 'configs/yolov8_face.yaml'

# Read config
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Update paths
config['path'] = 'data/widerface'
config['epochs'] = 50
config['batch'] = 32  # Kaggle GPU has more memory
config['device'] = 0  # Use GPU

# Save config
with open(config_path, 'w') as f:
    yaml.dump(config, f)

print("✓ Config updated for Kaggle")
```

---

### Step 9: Training Start Karo! 🚀

```python
# Cell 6: Start training
!python src/train.py \
    --config configs/yolov8_face.yaml \
    --model-size n
```

**Training Time**: 1-2 hours on GPU T4

---

### Step 10: Results Check Karo

```python
# Cell 7: Check training results
!ls runs/detect/yolov8_face/

# View metrics
import pandas as pd
results = pd.read_csv('runs/detect/yolov8_face/results.csv')
print(results.tail())

# Display training plots
from IPython.display import Image, display

print("Training Results:")
display(Image('runs/detect/yolov8_face/results.png'))
display(Image('runs/detect/yolov8_face/confusion_matrix.png'))
```

---

### Step 11: Best Model Download Karo

```python
# Cell 8: Download trained model
from IPython.display import FileLink

# Best model path
best_model = 'runs/detect/yolov8_face/weights/best.pt'

print(f"✓ Training complete!")
print(f"Best model: {best_model}")

# Create download link
FileLink(best_model)
```

**Download** button par click karke model save karo!

---

### Step 12: Inference Test Karo

```python
# Cell 9: Test inference
!python src/infer.py \
    --model runs/detect/yolov8_face/weights/best.pt \
    --source data/widerface/images/val/0_Parade_marchingband_1_849.jpg \
    --output-dir outputs/test

# Display result
from IPython.display import Image
display(Image('outputs/test/annotated_0_Parade_marchingband_1_849.jpg'))
```

---

### Step 13: Model Ko GitHub Par Push Karo (Optional)

```python
# Cell 10: Save model to Kaggle Output
# Kaggle automatically saves files in /kaggle/working/ to output

!cp runs/detect/yolov8_face/weights/best.pt /kaggle/working/best_yolov8_face.pt
!cp runs/detect/yolov8_face/results.csv /kaggle/working/training_results.csv

print("✓ Files saved to Kaggle output")
print("Download from: Notebook → Output → Download")
```

---

## 📊 Complete Kaggle Notebook Template

Yeh ek complete notebook hai jo aap directly use kar sakte ho:

```python
# ============================================
# CELL 1: Setup
# ============================================
!git clone https://github.com/rohitKT-23/FaceDetection.git
%cd FaceDetection
!pip install ultralytics opencv-python albumentations matplotlib pillow pyyaml tqdm pandas -q

import torch
print(f"✓ CUDA: {torch.cuda.is_available()}")
print(f"✓ GPU: {torch.cuda.get_device_name(0)}")

# ============================================
# CELL 2: Dataset Setup (Use Kaggle Dataset)
# ============================================
# Add WIDER FACE dataset from Kaggle in notebook settings
!ls /kaggle/input/

# ============================================
# CELL 3: Convert Dataset
# ============================================
!python src/convert_dataset.py \
    --wider-root /kaggle/input/widerface \
    --output-root data/widerface \
    --splits train val

# ============================================
# CELL 4: Update Config
# ============================================
import yaml
with open('configs/yolov8_face.yaml', 'r') as f:
    config = yaml.safe_load(f)
config['batch'] = 32
config['device'] = 0
with open('configs/yolov8_face.yaml', 'w') as f:
    yaml.dump(config, f)

# ============================================
# CELL 5: Train Model
# ============================================
!python src/train.py --config configs/yolov8_face.yaml --model-size n

# ============================================
# CELL 6: View Results
# ============================================
import pandas as pd
from IPython.display import Image, display

results = pd.read_csv('runs/detect/yolov8_face/results.csv')
print(results.tail())
display(Image('runs/detect/yolov8_face/results.png'))

# ============================================
# CELL 7: Save Model
# ============================================
!cp runs/detect/yolov8_face/weights/best.pt /kaggle/working/best_yolov8_face.pt
print("✓ Model saved! Download from Output section")
```

---

## ⚡ Quick Checklist

- [ ] Kaggle account banaya
- [ ] Phone verification kiya
- [ ] New Notebook banaya
- [ ] GPU enable kiya (Settings → Accelerator → GPU T4)
- [ ] Internet ON kiya
- [ ] GitHub repo clone kiya
- [ ] Dependencies install kiye
- [ ] WIDER FACE dataset add kiya
- [ ] Dataset convert kiya
- [ ] Training start kiya
- [ ] Model download kiya

---

## 🎯 Expected Results

**Training Time**: 1-2 hours  
**mAP@0.5**: > 0.90  
**Model Size**: ~6 MB (YOLOv8n)  
**FPS on GPU**: 60+ FPS

---

## 💡 Pro Tips

1. **GPU Time Save Karo**: Kaggle 30 hours/week deta hai, use wisely
2. **Notebook Save Karo**: Training ke baad notebook save karo
3. **Model Download Karo**: Training complete hone ke baad turant download karo
4. **Batch Size Badhao**: Kaggle GPU pe batch=32 use kar sakte ho
5. **Version Save Karo**: Different experiments ke liye notebook versions banao

---

## 🔗 Useful Links

- **Your GitHub Repo**: https://github.com/rohitKT-23/FaceDetection
- **Kaggle**: https://www.kaggle.com
- **WIDER FACE Dataset**: https://www.kaggle.com/datasets/sujaykapadnis/widerface
- **YOLOv8 Docs**: https://docs.ultralytics.com

---

## ❓ Agar Problem Aaye

1. **GPU nahi mil raha**: Phone verification check karo
2. **Dataset nahi mila**: Notebook settings → Add Data
3. **Out of Memory**: Batch size kam karo (16 ya 8)
4. **Training slow hai**: GPU enable hai ya nahi check karo

---

**Ready?** Kaggle par jao aur training start karo! 🚀

Koi doubt ho toh batao, main help karunga!
