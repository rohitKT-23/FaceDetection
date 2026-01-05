"""
WIDER FACE Dataset Annotation Converter
Converts WIDER FACE annotations to YOLO format
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple
import shutil


def parse_wider_annotations(annotation_file: str) -> Dict[str, List[Tuple]]:
    """
    Parse WIDER FACE annotation file
    
    Args:
        annotation_file: Path to WIDER FACE annotation file
        
    Returns:
        Dictionary mapping image paths to list of bounding boxes
    """
    annotations = {}
    
    with open(annotation_file, 'r') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        # Image path
        img_path = lines[i].strip()
        i += 1
        
        if i >= len(lines):
            break
        
        # Number of faces
        try:
            num_faces = int(lines[i].strip())
        except ValueError:
            # Skip if we can't parse the number
            print(f"Warning: Could not parse number of faces for {img_path}")
            i += 1
            continue
        
        i += 1
        
        # Parse bounding boxes
        boxes = []
        for _ in range(num_faces):
            if i >= len(lines):
                break
            
            parts = lines[i].strip().split()
            if len(parts) >= 4:
                # WIDER FACE format: x y w h [blur expression illumination invalid occlusion pose]
                # We only need x, y, w, h
                x, y, w, h = map(int, parts[:4])
                
                # Filter out invalid boxes (width or height <= 0)
                if w > 0 and h > 0:
                    boxes.append((x, y, w, h))
            i += 1
        
        if boxes:  # Only add if there are valid boxes
            annotations[img_path] = boxes
    
    return annotations


def convert_to_yolo_format(
    bbox: Tuple[int, int, int, int],
    img_width: int,
    img_height: int
) -> Tuple[float, float, float, float]:
    """
    Convert WIDER FACE bbox to YOLO format
    
    Args:
        bbox: (x, y, w, h) in absolute coordinates
        img_width: Image width
        img_height: Image height
        
    Returns:
        (x_center, y_center, width, height) normalized to [0, 1]
    """
    x, y, w, h = bbox
    
    # Calculate center coordinates
    x_center = (x + w / 2) / img_width
    y_center = (y + h / 2) / img_height
    
    # Normalize width and height
    width = w / img_width
    height = h / img_height
    
    return x_center, y_center, width, height


def create_yolo_dataset(
    wider_root: str,
    output_root: str,
    split: str = "train"
):
    """
    Create YOLO format dataset from WIDER FACE
    
    Args:
        wider_root: Root directory of WIDER FACE dataset
        output_root: Output directory for YOLO dataset
        split: Dataset split (train/val/test)
    """
    print(f"Converting WIDER FACE {split} split to YOLO format...")
    
    # Paths
    annotation_file = os.path.join(wider_root, f"wider_face_split/wider_face_{split}_bbx_gt.txt")
    images_dir = os.path.join(wider_root, f"WIDER_{split}/images")
    
    output_images_dir = os.path.join(output_root, f"images/{split}")
    output_labels_dir = os.path.join(output_root, f"labels/{split}")
    
    os.makedirs(output_images_dir, exist_ok=True)
    os.makedirs(output_labels_dir, exist_ok=True)
    
    # Parse annotations
    if not os.path.exists(annotation_file):
        print(f"Annotation file not found: {annotation_file}")
        return
    
    annotations = parse_wider_annotations(annotation_file)
    
    print(f"Found {len(annotations)} images with annotations")
    
    # Convert each image
    converted = 0
    for img_rel_path, boxes in annotations.items():
        # Source image path
        src_img_path = os.path.join(images_dir, img_rel_path)
        
        if not os.path.exists(src_img_path):
            continue
        
        # Get image dimensions
        try:
            from PIL import Image
            img = Image.open(src_img_path)
            img_width, img_height = img.size
        except Exception as e:
            print(f"Error reading {src_img_path}: {e}")
            continue
        
        # Create output paths
        img_name = Path(img_rel_path).name
        dst_img_path = os.path.join(output_images_dir, img_name)
        label_path = os.path.join(output_labels_dir, Path(img_name).stem + ".txt")
        
        # Copy image
        os.makedirs(os.path.dirname(dst_img_path), exist_ok=True)
        shutil.copy2(src_img_path, dst_img_path)
        
        # Create label file
        with open(label_path, 'w') as f:
            for bbox in boxes:
                # Convert to YOLO format
                x_center, y_center, width, height = convert_to_yolo_format(
                    bbox, img_width, img_height
                )
                
                # Write to file (class_id x_center y_center width height)
                # class_id = 0 for face
                f.write(f"0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
        
        converted += 1
        
        if converted % 100 == 0:
            print(f"Converted {converted}/{len(annotations)} images")
    
    print(f"✓ Conversion complete! Converted {converted} images")
    print(f"  Images: {output_images_dir}")
    print(f"  Labels: {output_labels_dir}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert WIDER FACE to YOLO format")
    parser.add_argument(
        "--wider-root",
        type=str,
        required=True,
        help="Root directory of WIDER FACE dataset"
    )
    parser.add_argument(
        "--output-root",
        type=str,
        default="data/widerface",
        help="Output directory for YOLO dataset"
    )
    parser.add_argument(
        "--splits",
        nargs='+',
        default=['train', 'val'],
        help="Dataset splits to convert"
    )
    
    args = parser.parse_args()
    
    for split in args.splits:
        create_yolo_dataset(
            wider_root=args.wider_root,
            output_root=args.output_root,
            split=split
        )
    
    print("\n" + "="*60)
    print("Dataset conversion complete!")
    print("="*60)
    print(f"\nUpdate your config file (configs/yolov8_face.yaml):")
    print(f"  path: {args.output_root}")
