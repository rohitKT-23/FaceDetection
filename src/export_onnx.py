"""
Export YOLOv8 Model to ONNX Format
Optimized for CPU inference with ONNX Runtime
"""

import os
from pathlib import Path
from ultralytics import YOLO
import onnx
import onnxruntime as ort


def export_to_onnx(
    model_path: str,
    output_dir: str = "weights",
    imgsz: int = 640,
    simplify: bool = True,
    dynamic: bool = False,
    opset: int = 12
):
    """
    Export YOLOv8 model to ONNX format
    
    Args:
        model_path: Path to trained .pt model
        output_dir: Directory to save ONNX model
        imgsz: Input image size
        simplify: Simplify ONNX model
        dynamic: Dynamic input shapes
        opset: ONNX opset version
    """
    
    if not ONNX_AVAILABLE:
        print("\n" + "="*60)
        print("ERROR: ONNX export not available")
        print("="*60)
        print("ONNX Runtime is not installed or not compatible with your Python version.")
        print("\nSolutions:")
        print("1. Use PyTorch models (.pt) - they work great!")
        print("2. Use Python 3.10-3.12 for ONNX support")
        print("3. Wait for ONNX Runtime Python 3.14 support")
        print("="*60)
        return None
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"{'='*60}")
    print(f"Exporting YOLOv8 Model to ONNX")
    print(f"{'='*60}")
    print(f"Model: {model_path}")
    print(f"Image Size: {imgsz}")
    print(f"Simplify: {simplify}")
    print(f"Dynamic: {dynamic}")
    print(f"ONNX Opset: {opset}")
    print(f"{'='*60}\n")
    
    # Load model
    model = YOLO(model_path)
    
    # Export to ONNX
    onnx_path = model.export(
        format='onnx',
        imgsz=imgsz,
        simplify=simplify,
        dynamic=dynamic,
        opset=opset
    )
    
    print(f"\n{'='*60}")
    print(f"Export Complete!")
    print(f"{'='*60}")
    print(f"ONNX model saved at: {onnx_path}")
    
    # Verify ONNX model
    print(f"\n{'='*60}")
    print(f"Verifying ONNX Model...")
    print(f"{'='*60}")
    
    try:
        # Load and check ONNX model
        onnx_model = onnx.load(onnx_path)
        onnx.checker.check_model(onnx_model)
        print("✓ ONNX model is valid")
        
        # Test with ONNX Runtime
        session = ort.InferenceSession(
            onnx_path,
            providers=['CPUExecutionProvider']
        )
        
        # Get input/output info
        input_info = session.get_inputs()[0]
        output_info = session.get_outputs()
        
        print(f"\nModel Information:")
        print(f"  Input name: {input_info.name}")
        print(f"  Input shape: {input_info.shape}")
        print(f"  Input type: {input_info.type}")
        print(f"  Number of outputs: {len(output_info)}")
        
        for i, output in enumerate(output_info):
            print(f"  Output {i} name: {output.name}")
            print(f"  Output {i} shape: {output.shape}")
        
        print(f"\n✓ ONNX Runtime verification successful")
        
        # Get model size
        model_size_mb = os.path.getsize(onnx_path) / (1024 * 1024)
        print(f"\nModel Size: {model_size_mb:.2f} MB")
        
    except Exception as e:
        print(f"✗ ONNX verification failed: {e}")
        return None
    
    return onnx_path


def benchmark_onnx(
    onnx_path: str,
    num_runs: int = 100,
    warmup_runs: int = 10
):
    """
    Benchmark ONNX model inference speed
    
    Args:
        onnx_path: Path to ONNX model
        num_runs: Number of inference runs
        warmup_runs: Number of warmup runs
    """
    import numpy as np
    import time
    
    print(f"\n{'='*60}")
    print(f"Benchmarking ONNX Model")
    print(f"{'='*60}")
    
    # Create session
    session = ort.InferenceSession(
        onnx_path,
        providers=['CPUExecutionProvider']
    )
    
    # Get input shape
    input_info = session.get_inputs()[0]
    input_shape = input_info.shape
    
    # Handle dynamic shapes
    if isinstance(input_shape[0], str):
        input_shape[0] = 1
    if isinstance(input_shape[2], str):
        input_shape[2] = 640
    if isinstance(input_shape[3], str):
        input_shape[3] = 640
    
    # Create dummy input
    dummy_input = np.random.randn(*input_shape).astype(np.float32)
    
    # Warmup
    print(f"Running {warmup_runs} warmup iterations...")
    for _ in range(warmup_runs):
        session.run(None, {input_info.name: dummy_input})
    
    # Benchmark
    print(f"Running {num_runs} benchmark iterations...")
    times = []
    
    for _ in range(num_runs):
        start = time.time()
        session.run(None, {input_info.name: dummy_input})
        times.append(time.time() - start)
    
    # Calculate statistics
    times = np.array(times) * 1000  # Convert to ms
    
    print(f"\n{'='*60}")
    print(f"Benchmark Results")
    print(f"{'='*60}")
    print(f"Mean inference time: {np.mean(times):.2f} ms")
    print(f"Median inference time: {np.median(times):.2f} ms")
    print(f"Min inference time: {np.min(times):.2f} ms")
    print(f"Max inference time: {np.max(times):.2f} ms")
    print(f"Std deviation: {np.std(times):.2f} ms")
    print(f"Average FPS: {1000 / np.mean(times):.2f}")
    print(f"{'='*60}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Export YOLOv8 to ONNX")
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Path to trained .pt model"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="weights",
        help="Output directory"
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="Input image size"
    )
    parser.add_argument(
        "--no-simplify",
        action="store_true",
        help="Don't simplify ONNX model"
    )
    parser.add_argument(
        "--dynamic",
        action="store_true",
        help="Enable dynamic input shapes"
    )
    parser.add_argument(
        "--opset",
        type=int,
        default=12,
        help="ONNX opset version"
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Run benchmark after export"
    )
    
    args = parser.parse_args()
    
    # Export model
    onnx_path = export_to_onnx(
        model_path=args.model,
        output_dir=args.output_dir,
        imgsz=args.imgsz,
        simplify=not args.no_simplify,
        dynamic=args.dynamic,
        opset=args.opset
    )
    
    # Benchmark if requested
    if args.benchmark and onnx_path:
        benchmark_onnx(onnx_path)
