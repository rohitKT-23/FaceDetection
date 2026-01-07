"""
Simple ONNX Export Script (Python 3.14 Compatible)
Exports YOLOv8 model to ONNX format without verification
"""

import os
import sys

try:
    from ultralytics import YOLO
except ImportError:
    print("❌ Error: ultralytics not installed")
    print("Run: pip install ultralytics")
    sys.exit(1)


def export_to_onnx(model_path='best_yolov8_face.pt', imgsz=640):
    """
    Export YOLOv8 model to ONNX format
    
    Args:
        model_path: Path to PyTorch model
        imgsz: Input image size
    """
    print("="*60)
    print("🚀 YOLOv8 ONNX Export (Simple)")
    print("="*60)
    
    # Check model exists
    if not os.path.exists(model_path):
        print(f"❌ Model not found: {model_path}")
        return False
    
    print(f"📦 Loading model: {model_path}")
    model = YOLO(model_path)
    
    # Get output path
    onnx_path = model_path.replace('.pt', '.onnx')
    
    print(f"\n🔄 Exporting to ONNX...")
    print(f"   Input size: {imgsz}x{imgsz}")
    print(f"   Output: {onnx_path}")
    
    try:
        # Export
        model.export(
            format='onnx',
            imgsz=imgsz,
            simplify=True,
            opset=12
        )
        
        # Check if file was created
        if os.path.exists(onnx_path):
            size_mb = os.path.getsize(onnx_path) / (1024 * 1024)
            print(f"\n✅ Export successful!")
            print(f"📁 ONNX model: {onnx_path}")
            print(f"📊 File size: {size_mb:.2f} MB")
            
            print(f"\n" + "="*60)
            print("⚠️  Note: ONNX Runtime requires Python 3.10-3.12")
            print("="*60)
            print("To use this ONNX model:")
            print("1. Set up Python 3.10-3.12 environment")
            print("2. Install: pip install onnxruntime")
            print("3. Run inference with ONNX Runtime")
            print("\nSee ONNX_EXPORT_GUIDE.md for details")
            
            return True
        else:
            print(f"❌ Export failed: ONNX file not created")
            return False
            
    except Exception as e:
        print(f"❌ Export error: {e}")
        return False


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Simple ONNX Export')
    parser.add_argument('--model', default='best_yolov8_face.pt', help='PyTorch model path')
    parser.add_argument('--imgsz', type=int, default=640, help='Input image size')
    
    args = parser.parse_args()
    
    success = export_to_onnx(args.model, args.imgsz)
    
    if success:
        print("\n✅ Done! ONNX model ready for deployment.")
    else:
        print("\n❌ Export failed. Check error messages above.")
        sys.exit(1)
