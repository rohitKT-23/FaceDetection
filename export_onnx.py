"""
ONNX Model Export Script
Exports YOLOv8 PyTorch model to ONNX format for faster CPU inference
"""

import os
import sys
import time
import numpy as np
import cv2
from pathlib import Path

try:
    from ultralytics import YOLO
    import onnxruntime as ort
except ImportError as e:
    print(f"Error: {e}")
    print("\nPlease install required packages:")
    print("pip install ultralytics onnxruntime")
    sys.exit(1)


def export_to_onnx(
    model_path: str = 'best_yolov8_face.pt',
    output_path: str = None,
    imgsz: int = 640,
    simplify: bool = True,
    opset: int = 12
):
    """
    Export YOLOv8 model to ONNX format
    
    Args:
        model_path: Path to PyTorch model (.pt)
        output_path: Output ONNX path (auto-generated if None)
        imgsz: Input image size
        simplify: Simplify ONNX model
        opset: ONNX opset version
    """
    print("="*60)
    print("🚀 YOLOv8 ONNX Export")
    print("="*60)
    
    # Check if model exists
    if not os.path.exists(model_path):
        print(f"❌ Error: Model not found at {model_path}")
        return None
    
    print(f"📦 Loading model: {model_path}")
    model = YOLO(model_path)
    
    # Auto-generate output path
    if output_path is None:
        output_path = model_path.replace('.pt', '.onnx')
    
    print(f"🔄 Exporting to ONNX...")
    print(f"   Output: {output_path}")
    print(f"   Image size: {imgsz}")
    print(f"   Simplify: {simplify}")
    print(f"   Opset: {opset}")
    
    try:
        # Export to ONNX
        model.export(
            format='onnx',
            imgsz=imgsz,
            simplify=simplify,
            opset=opset
        )
        
        print(f"✅ Export successful!")
        print(f"📁 ONNX model saved: {output_path}")
        
        # Get file size
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"📊 Model size: {size_mb:.2f} MB")
        
        return output_path
        
    except Exception as e:
        print(f"❌ Export failed: {e}")
        return None


def verify_onnx(onnx_path: str, test_image: str = None):
    """
    Verify ONNX model by running inference
    
    Args:
        onnx_path: Path to ONNX model
        test_image: Optional test image path
    """
    print("\n" + "="*60)
    print("🔍 Verifying ONNX Model")
    print("="*60)
    
    if not os.path.exists(onnx_path):
        print(f"❌ ONNX model not found: {onnx_path}")
        return False
    
    try:
        # Load ONNX model
        print(f"📦 Loading ONNX model: {onnx_path}")
        session = ort.InferenceSession(
            onnx_path,
            providers=['CPUExecutionProvider']
        )
        
        # Get model info
        input_name = session.get_inputs()[0].name
        input_shape = session.get_inputs()[0].shape
        output_names = [out.name for out in session.get_outputs()]
        
        print(f"✅ Model loaded successfully!")
        print(f"   Input: {input_name} {input_shape}")
        print(f"   Outputs: {len(output_names)} tensors")
        
        # Test inference if image provided
        if test_image and os.path.exists(test_image):
            print(f"\n🖼️  Testing inference on: {test_image}")
            
            # Load and preprocess image
            img = cv2.imread(test_image)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_resized = cv2.resize(img_rgb, (640, 640))
            img_normalized = img_resized.astype(np.float32) / 255.0
            img_transposed = np.transpose(img_normalized, (2, 0, 1))
            img_batch = np.expand_dims(img_transposed, axis=0)
            
            # Run inference
            start_time = time.time()
            outputs = session.run(None, {input_name: img_batch})
            inference_time = (time.time() - start_time) * 1000
            
            print(f"✅ Inference successful!")
            print(f"   Time: {inference_time:.2f} ms")
            print(f"   FPS: {1000/inference_time:.1f}")
            
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False


def benchmark_models(pt_path: str, onnx_path: str, test_image: str = None, iterations: int = 100):
    """
    Benchmark PyTorch vs ONNX inference speed
    
    Args:
        pt_path: PyTorch model path
        onnx_path: ONNX model path
        test_image: Test image path
        iterations: Number of iterations
    """
    print("\n" + "="*60)
    print("⚡ Benchmarking PyTorch vs ONNX")
    print("="*60)
    
    # Create dummy image if no test image
    if test_image is None or not os.path.exists(test_image):
        print("📸 Using dummy image for benchmark")
        img = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
    else:
        img = cv2.imread(test_image)
        img = cv2.resize(img, (640, 640))
    
    # Benchmark PyTorch
    print(f"\n🔥 PyTorch Model ({iterations} iterations)")
    try:
        model_pt = YOLO(pt_path)
        
        # Warmup
        for _ in range(10):
            _ = model_pt(img, verbose=False)
        
        # Benchmark
        start = time.time()
        for _ in range(iterations):
            _ = model_pt(img, verbose=False)
        pt_time = (time.time() - start) / iterations * 1000
        pt_fps = 1000 / pt_time
        
        print(f"   Avg time: {pt_time:.2f} ms")
        print(f"   FPS: {pt_fps:.1f}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        pt_time = None
        pt_fps = None
    
    # Benchmark ONNX
    print(f"\n⚡ ONNX Model ({iterations} iterations)")
    try:
        session = ort.InferenceSession(
            onnx_path,
            providers=['CPUExecutionProvider']
        )
        input_name = session.get_inputs()[0].name
        
        # Preprocess
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_normalized = img_rgb.astype(np.float32) / 255.0
        img_transposed = np.transpose(img_normalized, (2, 0, 1))
        img_batch = np.expand_dims(img_transposed, axis=0)
        
        # Warmup
        for _ in range(10):
            _ = session.run(None, {input_name: img_batch})
        
        # Benchmark
        start = time.time()
        for _ in range(iterations):
            _ = session.run(None, {input_name: img_batch})
        onnx_time = (time.time() - start) / iterations * 1000
        onnx_fps = 1000 / onnx_time
        
        print(f"   Avg time: {onnx_time:.2f} ms")
        print(f"   FPS: {onnx_fps:.1f}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        onnx_time = None
        onnx_fps = None
    
    # Comparison
    if pt_time and onnx_time:
        print("\n" + "="*60)
        print("📊 Comparison")
        print("="*60)
        speedup = pt_time / onnx_time
        print(f"PyTorch: {pt_time:.2f} ms ({pt_fps:.1f} FPS)")
        print(f"ONNX:    {onnx_time:.2f} ms ({onnx_fps:.1f} FPS)")
        print(f"Speedup: {speedup:.2f}x {'faster' if speedup > 1 else 'slower'}")


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Export YOLOv8 to ONNX')
    parser.add_argument('--model', default='best_yolov8_face.pt', help='PyTorch model path')
    parser.add_argument('--output', default=None, help='Output ONNX path')
    parser.add_argument('--imgsz', type=int, default=640, help='Input image size')
    parser.add_argument('--verify', action='store_true', help='Verify ONNX model')
    parser.add_argument('--benchmark', action='store_true', help='Benchmark PyTorch vs ONNX')
    parser.add_argument('--test-image', default=None, help='Test image for verification')
    
    args = parser.parse_args()
    
    # Export
    onnx_path = export_to_onnx(
        model_path=args.model,
        output_path=args.output,
        imgsz=args.imgsz
    )
    
    if onnx_path is None:
        return
    
    # Verify
    if args.verify:
        verify_onnx(onnx_path, args.test_image)
    
    # Benchmark
    if args.benchmark:
        benchmark_models(args.model, onnx_path, args.test_image)
    
    print("\n" + "="*60)
    print("✅ All done!")
    print("="*60)
    print(f"\nTo use ONNX model:")
    print(f"  import onnxruntime as ort")
    print(f"  session = ort.InferenceSession('{onnx_path}')")
    print(f"  outputs = session.run(None, {{input_name: image}})")


if __name__ == '__main__':
    main()
