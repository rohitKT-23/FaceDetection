"""
YOLOv8 Face Detection Training Script
Trains YOLOv8 model on WIDER FACE dataset
"""

import os
import yaml
from pathlib import Path
from ultralytics import YOLO
import torch


def train_yolov8_face(
    config_path: str = "configs/yolov8_face.yaml",
    model_size: str = "n",  # n, s, m, l, x
    resume: bool = False,
    pretrained: bool = True
):
    """
    Train YOLOv8 model for face detection
    
    Args:
        config_path: Path to YAML configuration file
        model_size: Model size (n=nano, s=small, m=medium, l=large, x=xlarge)
        resume: Resume training from last checkpoint
        pretrained: Use pretrained weights
    """
    
    # Load configuration
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    print(f"{'='*60}")
    print(f"YOLOv8 Face Detection Training")
    print(f"{'='*60}")
    print(f"Model Size: YOLOv8{model_size}")
    print(f"Image Size: {config.get('imgsz', 640)}")
    print(f"Batch Size: {config.get('batch', 16)}")
    print(f"Epochs: {config.get('epochs', 50)}")
    print(f"Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")
    print(f"{'='*60}\n")
    
    # Initialize model
    model_name = f"yolov8{model_size}.pt" if pretrained else f"yolov8{model_size}.yaml"
    model = YOLO(model_name)
    
    # Train the model
    results = model.train(
        data=config_path,
        epochs=config.get('epochs', 50),
        imgsz=config.get('imgsz', 640),
        batch=config.get('batch', 16),
        workers=config.get('workers', 8),
        device=config.get('device', ''),
        optimizer=config.get('optimizer', 'AdamW'),
        lr0=config.get('lr0', 0.001),
        lrf=config.get('lrf', 0.01),
        momentum=config.get('momentum', 0.937),
        weight_decay=config.get('weight_decay', 0.0005),
        augment=config.get('augment', True),
        project=config.get('project', 'runs/detect'),
        name=config.get('name', 'yolov8_face'),
        exist_ok=config.get('exist_ok', False),
        pretrained=config.get('pretrained', True),
        verbose=config.get('verbose', True),
        seed=config.get('seed', 0),
        deterministic=config.get('deterministic', True),
        single_cls=config.get('single_cls', True),
        rect=config.get('rect', False),
        cos_lr=config.get('cos_lr', False),
        close_mosaic=config.get('close_mosaic', 10),
        resume=resume,
        amp=config.get('amp', True),
    )
    
    print(f"\n{'='*60}")
    print(f"Training Complete!")
    print(f"{'='*60}")
    print(f"Best model saved at: {model.trainer.best}")
    print(f"Results saved at: {model.trainer.save_dir}")
    
    # Validate the model
    print(f"\n{'='*60}")
    print(f"Running Validation...")
    print(f"{'='*60}")
    metrics = model.val()
    
    print(f"\nValidation Metrics:")
    print(f"  mAP@0.5: {metrics.box.map50:.4f}")
    print(f"  mAP@0.5:0.95: {metrics.box.map:.4f}")
    print(f"  Precision: {metrics.box.mp:.4f}")
    print(f"  Recall: {metrics.box.mr:.4f}")
    
    return model, results, metrics


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Train YOLOv8 Face Detection Model")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/yolov8_face.yaml",
        help="Path to config file"
    )
    parser.add_argument(
        "--model-size",
        type=str,
        default="n",
        choices=["n", "s", "m", "l", "x"],
        help="Model size (n=nano, s=small, m=medium, l=large, x=xlarge)"
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume training from last checkpoint"
    )
    parser.add_argument(
        "--no-pretrained",
        action="store_true",
        help="Train from scratch without pretrained weights"
    )
    
    args = parser.parse_args()
    
    train_yolov8_face(
        config_path=args.config,
        model_size=args.model_size,
        resume=args.resume,
        pretrained=not args.no_pretrained
    )
