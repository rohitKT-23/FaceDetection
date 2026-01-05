"""
Comprehensive Benchmarking Script for Face Detection Model
Evaluates: Precision, Recall, mAP, FPS, Latency
"""

import os
import time
import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List
from ultralytics import YOLO
import cv2


class FaceDetectionBenchmark:
    """Comprehensive benchmarking for face detection models"""
    
    def __init__(self, model_path: str, device: str = ''):
        """
        Initialize benchmark
        
        Args:
            model_path: Path to model (.pt or .onnx)
            device: Device for inference
        """
        self.model = YOLO(model_path)
        self.device = device
        self.model_path = model_path
        
        print(f"Loaded model: {model_path}")
    
    def benchmark_accuracy(
        self,
        data_yaml: str,
        conf_threshold: float = 0.25,
        iou_threshold: float = 0.45
    ) -> Dict:
        """
        Benchmark model accuracy on validation set
        
        Args:
            data_yaml: Path to dataset YAML
            conf_threshold: Confidence threshold
            iou_threshold: IoU threshold
            
        Returns:
            Dictionary with accuracy metrics
        """
        print(f"\n{'='*60}")
        print(f"Accuracy Benchmark")
        print(f"{'='*60}")
        
        # Run validation
        metrics = self.model.val(
            data=data_yaml,
            conf=conf_threshold,
            iou=iou_threshold,
            device=self.device
        )
        
        results = {
            "map50": float(metrics.box.map50),
            "map50_95": float(metrics.box.map),
            "precision": float(metrics.box.mp),
            "recall": float(metrics.box.mr),
            "conf_threshold": conf_threshold,
            "iou_threshold": iou_threshold
        }
        
        print(f"\nAccuracy Metrics:")
        print(f"  mAP@0.5: {results['map50']:.4f}")
        print(f"  mAP@0.5:0.95: {results['map50_95']:.4f}")
        print(f"  Precision: {results['precision']:.4f}")
        print(f"  Recall: {results['recall']:.4f}")
        
        return results
    
    def benchmark_speed(
        self,
        image_size: int = 640,
        batch_size: int = 1,
        num_runs: int = 100,
        warmup_runs: int = 10
    ) -> Dict:
        """
        Benchmark inference speed
        
        Args:
            image_size: Input image size
            batch_size: Batch size
            num_runs: Number of inference runs
            warmup_runs: Number of warmup runs
            
        Returns:
            Dictionary with speed metrics
        """
        print(f"\n{'='*60}")
        print(f"Speed Benchmark")
        print(f"{'='*60}")
        print(f"Image size: {image_size}")
        print(f"Batch size: {batch_size}")
        print(f"Runs: {num_runs}")
        
        # Create dummy input
        dummy_input = np.random.randint(
            0, 255,
            (image_size, image_size, 3),
            dtype=np.uint8
        )
        
        # Warmup
        print(f"\nRunning {warmup_runs} warmup iterations...")
        for _ in range(warmup_runs):
            self.model.predict(
                source=dummy_input,
                verbose=False,
                device=self.device
            )
        
        # Benchmark
        print(f"Running {num_runs} benchmark iterations...")
        times = []
        
        for i in range(num_runs):
            start = time.time()
            self.model.predict(
                source=dummy_input,
                verbose=False,
                device=self.device
            )
            times.append(time.time() - start)
            
            if (i + 1) % 20 == 0:
                print(f"  Progress: {i + 1}/{num_runs}")
        
        # Calculate statistics
        times = np.array(times) * 1000  # Convert to ms
        
        results = {
            "mean_latency_ms": float(np.mean(times)),
            "median_latency_ms": float(np.median(times)),
            "min_latency_ms": float(np.min(times)),
            "max_latency_ms": float(np.max(times)),
            "std_latency_ms": float(np.std(times)),
            "mean_fps": float(1000 / np.mean(times)),
            "image_size": image_size,
            "batch_size": batch_size
        }
        
        print(f"\nSpeed Metrics:")
        print(f"  Mean latency: {results['mean_latency_ms']:.2f} ms")
        print(f"  Median latency: {results['median_latency_ms']:.2f} ms")
        print(f"  Min latency: {results['min_latency_ms']:.2f} ms")
        print(f"  Max latency: {results['max_latency_ms']:.2f} ms")
        print(f"  Std deviation: {results['std_latency_ms']:.2f} ms")
        print(f"  Average FPS: {results['mean_fps']:.2f}")
        
        return results
    
    def benchmark_nms_iou(
        self,
        test_images: List[str],
        iou_thresholds: List[float] = [0.3, 0.4, 0.5, 0.6, 0.7],
        conf_threshold: float = 0.25
    ) -> Dict:
        """
        Benchmark different NMS IoU thresholds
        
        Args:
            test_images: List of test image paths
            iou_thresholds: IoU thresholds to test
            conf_threshold: Confidence threshold
            
        Returns:
            Dictionary with results for each IoU threshold
        """
        print(f"\n{'='*60}")
        print(f"NMS IoU Ablation Study")
        print(f"{'='*60}")
        
        results = {}
        
        for iou in iou_thresholds:
            print(f"\nTesting IoU threshold: {iou}")
            
            total_detections = 0
            total_time = 0
            
            for img_path in test_images:
                start = time.time()
                preds = self.model.predict(
                    source=img_path,
                    conf=conf_threshold,
                    iou=iou,
                    verbose=False,
                    device=self.device
                )[0]
                total_time += time.time() - start
                
                total_detections += len(preds.boxes)
            
            avg_detections = total_detections / len(test_images)
            avg_time = (total_time / len(test_images)) * 1000
            
            results[f"iou_{iou}"] = {
                "iou_threshold": iou,
                "avg_detections_per_image": avg_detections,
                "avg_inference_time_ms": avg_time
            }
            
            print(f"  Avg detections/image: {avg_detections:.2f}")
            print(f"  Avg inference time: {avg_time:.2f} ms")
        
        return results
    
    def generate_report(
        self,
        output_dir: str = "outputs/benchmark",
        **benchmark_results
    ):
        """
        Generate comprehensive benchmark report
        
        Args:
            output_dir: Output directory for report
            **benchmark_results: Results from various benchmarks
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Save JSON report
        report = {
            "model": self.model_path,
            "device": self.device,
            **benchmark_results
        }
        
        report_path = os.path.join(output_dir, "benchmark_report.json")
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n{'='*60}")
        print(f"Benchmark Report Generated")
        print(f"{'='*60}")
        print(f"Report saved to: {report_path}")
        
        # Generate visualizations if matplotlib available
        try:
            self._generate_visualizations(output_dir, report)
        except Exception as e:
            print(f"Could not generate visualizations: {e}")
    
    def _generate_visualizations(self, output_dir: str, report: Dict):
        """Generate visualization plots"""
        
        # Speed metrics bar chart
        if "speed" in report:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            metrics = ["mean_latency_ms", "median_latency_ms", "min_latency_ms", "max_latency_ms"]
            values = [report["speed"][m] for m in metrics]
            labels = ["Mean", "Median", "Min", "Max"]
            
            ax.bar(labels, values, color=['#3498db', '#2ecc71', '#f39c12', '#e74c3c'])
            ax.set_ylabel('Latency (ms)')
            ax.set_title('Inference Latency Metrics')
            ax.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, "latency_metrics.png"), dpi=150)
            plt.close()
            
            print(f"  Saved: latency_metrics.png")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Benchmark Face Detection Model")
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Path to model (.pt or .onnx)"
    )
    parser.add_argument(
        "--data",
        type=str,
        help="Path to dataset YAML (for accuracy benchmark)"
    )
    parser.add_argument(
        "--source",
        type=str,
        help="Path to test images/video (for speed benchmark)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs/benchmark",
        help="Output directory"
    )
    parser.add_argument(
        "--device",
        type=str,
        default='',
        help="Device ('' for auto, 'cpu', '0', etc.)"
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=100,
        help="Number of benchmark runs"
    )
    
    args = parser.parse_args()
    
    # Initialize benchmark
    benchmark = FaceDetectionBenchmark(
        model_path=args.model,
        device=args.device
    )
    
    results = {}
    
    # Accuracy benchmark
    if args.data:
        results["accuracy"] = benchmark.benchmark_accuracy(args.data)
    
    # Speed benchmark
    results["speed"] = benchmark.benchmark_speed(num_runs=args.runs)
    
    # NMS IoU ablation (if test images provided)
    if args.source and os.path.isdir(args.source):
        test_images = [
            os.path.join(args.source, f)
            for f in os.listdir(args.source)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ][:20]  # Limit to 20 images
        
        if test_images:
            results["nms_ablation"] = benchmark.benchmark_nms_iou(test_images)
    
    # Generate report
    benchmark.generate_report(args.output_dir, **results)
