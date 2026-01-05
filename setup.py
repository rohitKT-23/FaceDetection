"""
Quick Setup Script for Face Detection System
Automates environment setup and dependency installation
"""

import subprocess
import sys
import os


def run_command(cmd, description):
    """Run a command and print status"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    print(f"Running: {cmd}\n")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        print(result.stdout)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        print(e.stderr)
        return False


def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║     Face Detection System - Quick Setup Script           ║
    ║                  YOLOv8 + ONNX                           ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Check Python version
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        sys.exit(1)
    
    # Install dependencies
    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    ):
        print("\n✗ Failed to install dependencies")
        sys.exit(1)
    
    # Create necessary directories
    print(f"\n{'='*60}")
    print("Creating necessary directories")
    print(f"{'='*60}")
    
    directories = [
        "data/widerface",
        "data/samples",
        "weights",
        "outputs",
        "outputs/benchmark"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created: {directory}")
    
    # Download sample YOLOv8 model
    print(f"\n{'='*60}")
    print("Downloading YOLOv8 pretrained model")
    print(f"{'='*60}")
    
    try:
        from ultralytics import YOLO
        model = YOLO('yolov8n.pt')
        print("✓ YOLOv8n model downloaded successfully")
    except Exception as e:
        print(f"Note: Model will be downloaded during first training: {e}")
    
    # Setup complete
    print(f"\n{'='*60}")
    print("✓ Setup Complete!")
    print(f"{'='*60}")
    
    print("""
    Next Steps:
    
    1. Download WIDER FACE dataset:
       - Visit: http://shuoyang1213.me/WIDERFACE/
       - Place in: data/widerface/
    
    2. Convert dataset to YOLO format:
       python src/convert_dataset.py --wider-root <path_to_wider_face>
    
    3. Train the model:
       python src/train.py --config configs/yolov8_face.yaml
    
    4. Run inference:
       python src/infer.py --model weights/best.pt --source <image/video>
    
    5. Launch Streamlit demo:
       streamlit run app/streamlit_app.py
    
    For more information, see README.md
    """)


if __name__ == "__main__":
    main()
