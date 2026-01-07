"""
Face Detection CLI Tool
Command-line interface for YOLOv8 face detection on images, videos, and folders
"""

import os
import sys
import argparse
import time
import json
from pathlib import Path
from typing import List, Union
import cv2
import numpy as np

try:
    from ultralytics import YOLO
except ImportError:
    print("❌ Error: ultralytics not installed")
    print("Run: pip install ultralytics")
    sys.exit(1)


class FaceDetector:
    """Face detection wrapper for YOLOv8"""
    
    def __init__(self, weights: str, conf: float = 0.5, iou: float = 0.45, device: str = ''):
        """
        Initialize face detector
        
        Args:
            weights: Path to model weights (.pt or .onnx)
            conf: Confidence threshold
            iou: IoU threshold for NMS
            device: Device ('', 'cpu', '0', '1', etc.)
        """
        self.weights = weights
        self.conf = conf
        self.iou = iou
        self.device = device
        
        print(f"📦 Loading model: {weights}")
        self.model = YOLO(weights)
        print(f"✅ Model loaded successfully")
        print(f"   Confidence: {conf}")
        print(f"   IoU: {iou}")
        print(f"   Device: {device if device else 'auto'}")
    
    def detect_image(self, image_path: str, output_dir: str, save_json: bool = False):
        """
        Detect faces in single image
        
        Args:
            image_path: Path to image
            output_dir: Output directory
            save_json: Save detection results as JSON
        
        Returns:
            dict: Detection results
        """
        # Run inference
        results = self.model(image_path, conf=self.conf, iou=self.iou, device=self.device)[0]
        
        # Get detections
        boxes = results.boxes
        num_faces = len(boxes)
        
        # Prepare results
        detections = []
        for box in boxes:
            x1, y1, x2, y2 = map(float, box.xyxy[0])
            conf = float(box.conf[0])
            detections.append({
                'bbox': [x1, y1, x2, y2],
                'confidence': conf
            })
        
        # Save annotated image
        output_path = os.path.join(output_dir, f"annotated_{Path(image_path).name}")
        results.save(filename=output_path)
        
        # Save JSON if requested
        if save_json:
            json_path = os.path.join(output_dir, f"{Path(image_path).stem}_detections.json")
            with open(json_path, 'w') as f:
                json.dump({
                    'image': image_path,
                    'num_faces': num_faces,
                    'detections': detections
                }, f, indent=2)
        
        return {
            'image': image_path,
            'num_faces': num_faces,
            'detections': detections,
            'output': output_path
        }
    
    def detect_video(self, video_path: str, output_dir: str, save_json: bool = False):
        """
        Detect faces in video
        
        Args:
            video_path: Path to video
            output_dir: Output directory
            save_json: Save detection results as JSON
        
        Returns:
            dict: Detection results
        """
        cap = cv2.VideoCapture(video_path)
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Output video
        output_path = os.path.join(output_dir, f"annotated_{Path(video_path).name}")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        total_detections = 0
        all_detections = []
        
        print(f"🎬 Processing video: {total_frames} frames @ {fps} FPS")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Run inference
            results = self.model(frame, conf=self.conf, iou=self.iou, device=self.device, verbose=False)[0]
            boxes = results.boxes
            
            # Draw boxes
            frame_detections = []
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f'{conf:.2f}'
                cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX,
                           0.5, (0, 255, 0), 2)
                
                frame_detections.append({
                    'bbox': [x1, y1, x2, y2],
                    'confidence': conf
                })
                total_detections += 1
            
            all_detections.append({
                'frame': frame_count,
                'num_faces': len(boxes),
                'detections': frame_detections
            })
            
            out.write(frame)
            frame_count += 1
            
            # Progress
            if frame_count % 30 == 0:
                progress = (frame_count / total_frames) * 100
                print(f"   Progress: {progress:.1f}% ({frame_count}/{total_frames})")
        
        cap.release()
        out.release()
        
        # Save JSON if requested
        if save_json:
            json_path = os.path.join(output_dir, f"{Path(video_path).stem}_detections.json")
            with open(json_path, 'w') as f:
                json.dump({
                    'video': video_path,
                    'total_frames': total_frames,
                    'processed_frames': frame_count,
                    'total_detections': total_detections,
                    'avg_faces_per_frame': total_detections / frame_count if frame_count > 0 else 0,
                    'frames': all_detections
                }, f, indent=2)
        
        return {
            'video': video_path,
            'total_frames': total_frames,
            'processed_frames': frame_count,
            'total_detections': total_detections,
            'output': output_path
        }
    
    def detect_folder(self, folder_path: str, output_dir: str, save_json: bool = False):
        """
        Detect faces in all images in folder
        
        Args:
            folder_path: Path to folder
            output_dir: Output directory
            save_json: Save detection results as JSON
        
        Returns:
            dict: Detection results
        """
        # Get all images
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(Path(folder_path).glob(f'*{ext}'))
            image_files.extend(Path(folder_path).glob(f'*{ext.upper()}'))
        
        if not image_files:
            print(f"⚠️  No images found in {folder_path}")
            return None
        
        print(f"📁 Found {len(image_files)} images")
        
        all_results = []
        total_faces = 0
        
        for i, img_path in enumerate(image_files, 1):
            print(f"\n[{i}/{len(image_files)}] Processing: {img_path.name}")
            
            result = self.detect_image(str(img_path), output_dir, save_json=False)
            all_results.append(result)
            total_faces += result['num_faces']
            
            print(f"   Detected: {result['num_faces']} faces")
        
        # Save summary JSON if requested
        if save_json:
            json_path = os.path.join(output_dir, "batch_detections.json")
            with open(json_path, 'w') as f:
                json.dump({
                    'folder': folder_path,
                    'total_images': len(image_files),
                    'total_faces': total_faces,
                    'avg_faces_per_image': total_faces / len(image_files),
                    'results': all_results
                }, f, indent=2)
        
        return {
            'folder': folder_path,
            'total_images': len(image_files),
            'total_faces': total_faces,
            'results': all_results
        }


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='YOLOv8 Face Detection CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Detect faces in image
  python detect.py --source image.jpg --weights best_yolov8_face.pt
  
  # Detect in video with custom confidence
  python detect.py --source video.mp4 --conf 0.7 --output-dir results/
  
  # Batch process folder
  python detect.py --source images/ --save-json
  
  # Use ONNX model
  python detect.py --source image.jpg --weights model.onnx
        """
    )
    
    # Required arguments
    parser.add_argument('--source', required=True,
                       help='Input source (image, video, or folder path)')
    parser.add_argument('--weights', default='best_yolov8_face.pt',
                       help='Model weights path (.pt or .onnx)')
    
    # Optional arguments
    parser.add_argument('--conf', type=float, default=0.5,
                       help='Confidence threshold (0-1)')
    parser.add_argument('--iou', type=float, default=0.45,
                       help='IoU threshold for NMS (0-1)')
    parser.add_argument('--device', default='',
                       help='Device (cpu, 0, 1, etc.)')
    parser.add_argument('--output-dir', default='outputs/cli',
                       help='Output directory')
    parser.add_argument('--save-json', action='store_true',
                       help='Save detection results as JSON')
    parser.add_argument('--verbose', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Print header
    print("="*60)
    print("👤 YOLOv8 Face Detection CLI")
    print("="*60)
    
    # Validate inputs
    if not os.path.exists(args.source):
        print(f"❌ Error: Source not found: {args.source}")
        sys.exit(1)
    
    if not os.path.exists(args.weights):
        print(f"❌ Error: Weights not found: {args.weights}")
        sys.exit(1)
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Initialize detector
    detector = FaceDetector(
        weights=args.weights,
        conf=args.conf,
        iou=args.iou,
        device=args.device
    )
    
    # Determine source type and process
    source_path = Path(args.source)
    start_time = time.time()
    
    print(f"\n🔍 Processing: {args.source}")
    
    if source_path.is_file():
        # Check if image or video
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv'}
        
        if source_path.suffix.lower() in image_extensions:
            print("📸 Type: Image")
            result = detector.detect_image(args.source, args.output_dir, args.save_json)
            
            print(f"\n✅ Detection complete!")
            print(f"   Faces detected: {result['num_faces']}")
            print(f"   Output: {result['output']}")
            
        elif source_path.suffix.lower() in video_extensions:
            print("🎬 Type: Video")
            result = detector.detect_video(args.source, args.output_dir, args.save_json)
            
            print(f"\n✅ Detection complete!")
            print(f"   Frames processed: {result['processed_frames']}")
            print(f"   Total detections: {result['total_detections']}")
            print(f"   Output: {result['output']}")
            
        else:
            print(f"❌ Unsupported file type: {source_path.suffix}")
            sys.exit(1)
    
    elif source_path.is_dir():
        print("📁 Type: Folder")
        result = detector.detect_folder(args.source, args.output_dir, args.save_json)
        
        if result:
            print(f"\n✅ Batch processing complete!")
            print(f"   Images processed: {result['total_images']}")
            print(f"   Total faces: {result['total_faces']}")
            print(f"   Avg faces/image: {result['total_faces']/result['total_images']:.1f}")
    
    else:
        print(f"❌ Invalid source: {args.source}")
        sys.exit(1)
    
    # Print summary
    elapsed_time = time.time() - start_time
    print(f"\n⏱️  Total time: {elapsed_time:.2f}s")
    print(f"📁 Output directory: {args.output_dir}")
    
    if args.save_json:
        print(f"💾 JSON results saved")
    
    print("\n" + "="*60)
    print("✅ All done!")
    print("="*60)


if __name__ == '__main__':
    main()
