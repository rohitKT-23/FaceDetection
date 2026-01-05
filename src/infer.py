"""
YOLOv8 Face Detection Inference Script
Supports: Images, Videos, Webcam
Outputs: Annotated images/videos + JSON results
"""

import os
import json
import cv2
import time
from pathlib import Path
from typing import Union, List, Dict
import numpy as np
from ultralytics import YOLO


class FaceDetector:
    """Face Detection Inference Pipeline"""
    
    def __init__(
        self,
        model_path: str,
        conf_threshold: float = 0.25,
        iou_threshold: float = 0.45,
        device: str = ''
    ):
        """
        Initialize Face Detector
        
        Args:
            model_path: Path to trained model (.pt or .onnx)
            conf_threshold: Confidence threshold for detections
            iou_threshold: IoU threshold for NMS
            device: Device to run inference on ('' for auto, 'cpu', '0', etc.)
        """
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.device = device
        
        print(f"Model loaded: {model_path}")
        print(f"Confidence threshold: {conf_threshold}")
        print(f"IoU threshold: {iou_threshold}")
    
    def detect_image(
        self,
        image_path: str,
        output_dir: str = "outputs",
        save_json: bool = True
    ) -> Dict:
        """
        Detect faces in a single image
        
        Args:
            image_path: Path to input image
            output_dir: Directory to save results
            save_json: Whether to save JSON output
            
        Returns:
            Dictionary containing detection results
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Run inference
        results = self.model.predict(
            source=image_path,
            conf=self.conf_threshold,
            iou=self.iou_threshold,
            device=self.device,
            save=False
        )[0]
        
        # Parse results
        detections = []
        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            conf = float(box.conf[0].cpu().numpy())
            
            detections.append({
                "bbox": [float(x1), float(y1), float(x2), float(y2)],
                "score": conf
            })
        
        # Save annotated image
        annotated = results.plot()
        output_path = os.path.join(output_dir, f"annotated_{Path(image_path).name}")
        cv2.imwrite(output_path, annotated)
        
        result_dict = {
            "image": image_path,
            "num_faces": len(detections),
            "detections": detections,
            "output_image": output_path
        }
        
        # Save JSON
        if save_json:
            json_path = os.path.join(output_dir, f"{Path(image_path).stem}_results.json")
            with open(json_path, 'w') as f:
                json.dump(result_dict, f, indent=2)
            result_dict["json_output"] = json_path
        
        print(f"Detected {len(detections)} faces in {image_path}")
        return result_dict
    
    def detect_video(
        self,
        video_path: str,
        output_dir: str = "outputs",
        save_json: bool = True,
        display: bool = False
    ) -> Dict:
        """
        Detect faces in video
        
        Args:
            video_path: Path to input video or webcam index (0, 1, etc.)
            output_dir: Directory to save results
            save_json: Whether to save JSON output
            display: Whether to display video in real-time
            
        Returns:
            Dictionary containing detection results
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Open video
        if isinstance(video_path, int) or video_path.isdigit():
            cap = cv2.VideoCapture(int(video_path))
            is_webcam = True
            output_name = f"webcam_{int(time.time())}"
        else:
            cap = cv2.VideoCapture(video_path)
            is_webcam = False
            output_name = Path(video_path).stem
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Video writer
        output_path = os.path.join(output_dir, f"annotated_{output_name}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_results = []
        frame_count = 0
        total_time = 0
        
        print(f"Processing {'webcam' if is_webcam else video_path}...")
        print("Press 'q' to quit")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Run inference
            start_time = time.time()
            results = self.model.predict(
                source=frame,
                conf=self.conf_threshold,
                iou=self.iou_threshold,
                device=self.device,
                verbose=False
            )[0]
            inference_time = time.time() - start_time
            total_time += inference_time
            
            # Parse detections
            detections = []
            for box in results.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = float(box.conf[0].cpu().numpy())
                
                detections.append({
                    "bbox": [float(x1), float(y1), float(x2), float(y2)],
                    "score": conf,
                    "frame": frame_count,
                    "timestamp": frame_count / fps
                })
            
            frame_results.append({
                "frame": frame_count,
                "timestamp": frame_count / fps,
                "num_faces": len(detections),
                "detections": detections
            })
            
            # Annotate frame
            annotated = results.plot()
            
            # Add FPS counter
            current_fps = 1.0 / inference_time if inference_time > 0 else 0
            cv2.putText(
                annotated,
                f"FPS: {current_fps:.1f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
            
            # Write frame
            out.write(annotated)
            
            # Display
            if display:
                cv2.imshow('Face Detection', annotated)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            frame_count += 1
            
            if frame_count % 30 == 0:
                avg_fps = frame_count / total_time if total_time > 0 else 0
                print(f"Processed {frame_count} frames | Avg FPS: {avg_fps:.2f}")
        
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        
        avg_fps = frame_count / total_time if total_time > 0 else 0
        
        result_dict = {
            "video": str(video_path),
            "total_frames": frame_count,
            "avg_fps": avg_fps,
            "output_video": output_path,
            "frame_results": frame_results
        }
        
        # Save JSON
        if save_json:
            json_path = os.path.join(output_dir, f"{output_name}_results.json")
            with open(json_path, 'w') as f:
                json.dump(result_dict, f, indent=2)
            result_dict["json_output"] = json_path
        
        print(f"\nProcessing complete!")
        print(f"Total frames: {frame_count}")
        print(f"Average FPS: {avg_fps:.2f}")
        print(f"Output saved to: {output_path}")
        
        return result_dict


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="YOLOv8 Face Detection Inference")
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Path to trained model (.pt or .onnx)"
    )
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="Path to image/video or webcam index (0, 1, etc.)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs",
        help="Output directory"
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Confidence threshold"
    )
    parser.add_argument(
        "--iou",
        type=float,
        default=0.45,
        help="IoU threshold for NMS"
    )
    parser.add_argument(
        "--device",
        type=str,
        default='',
        help="Device ('' for auto, 'cpu', '0', etc.)"
    )
    parser.add_argument(
        "--display",
        action="store_true",
        help="Display results in real-time (video only)"
    )
    
    args = parser.parse_args()
    
    # Initialize detector
    detector = FaceDetector(
        model_path=args.model,
        conf_threshold=args.conf,
        iou_threshold=args.iou,
        device=args.device
    )
    
    # Determine source type
    source = args.source
    if source.isdigit():
        # Webcam
        detector.detect_video(
            video_path=int(source),
            output_dir=args.output_dir,
            display=args.display
        )
    elif os.path.isfile(source):
        ext = Path(source).suffix.lower()
        if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.webp']:
            # Image
            detector.detect_image(
                image_path=source,
                output_dir=args.output_dir
            )
        elif ext in ['.mp4', '.avi', '.mov', '.mkv']:
            # Video
            detector.detect_video(
                video_path=source,
                output_dir=args.output_dir,
                display=args.display
            )
        else:
            print(f"Unsupported file format: {ext}")
    else:
        print(f"Source not found: {source}")
