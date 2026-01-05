"""
Streamlit Face Detection Demo App
Features: Image/Video Upload, Webcam, Real-time FPS, Confidence Slider
"""

import streamlit as st
import cv2
import numpy as np
import tempfile
import time
from pathlib import Path
from PIL import Image
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from ultralytics import YOLO
except ImportError:
    st.error("Please install ultralytics: pip install ultralytics")
    st.stop()


# Page config
st.set_page_config(
    page_title="Face Detection System",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model(model_path: str):
    """Load YOLO model with caching"""
    try:
        model = YOLO(model_path)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None


def detect_faces(model, image, conf_threshold, iou_threshold):
    """Run face detection on image"""
    results = model.predict(
        source=image,
        conf=conf_threshold,
        iou=iou_threshold,
        verbose=False
    )[0]
    
    return results


def process_image(model, image, conf_threshold, iou_threshold):
    """Process single image"""
    start_time = time.time()
    results = detect_faces(model, image, conf_threshold, iou_threshold)
    inference_time = time.time() - start_time
    
    # Get annotated image
    annotated = results.plot()
    
    # Get detection info
    num_faces = len(results.boxes)
    
    return annotated, num_faces, inference_time


def process_video(model, video_path, conf_threshold, iou_threshold, progress_bar, status_text):
    """Process video file"""
    cap = cv2.VideoCapture(video_path)
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Create temporary output file
    output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    frame_count = 0
    total_faces = 0
    total_time = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Run detection
        start_time = time.time()
        results = detect_faces(model, frame, conf_threshold, iou_threshold)
        inference_time = time.time() - start_time
        
        total_time += inference_time
        total_faces += len(results.boxes)
        
        # Annotate frame
        annotated = results.plot()
        
        # Add FPS
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
        
        out.write(annotated)
        frame_count += 1
        
        # Update progress
        progress = frame_count / total_frames
        progress_bar.progress(progress)
        status_text.text(f"Processing frame {frame_count}/{total_frames}")
    
    cap.release()
    out.release()
    
    avg_fps = frame_count / total_time if total_time > 0 else 0
    
    return output_path, frame_count, total_faces, avg_fps


def main():
    # Header
    st.markdown('<h1 class="main-header">👤 Real-Time Face Detection System</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    st.sidebar.header("⚙️ Configuration")
    
    # Model selection
    model_path = st.sidebar.text_input(
        "Model Path",
        value="weights/best.pt",
        help="Path to trained model (.pt or .onnx)"
    )
    
    # Load model
    if not os.path.exists(model_path):
        st.sidebar.error(f"Model not found: {model_path}")
        st.info("👈 Please specify a valid model path in the sidebar")
        st.stop()
    
    model = load_model(model_path)
    if model is None:
        st.stop()
    
    st.sidebar.success("✓ Model loaded successfully")
    
    # Detection parameters
    st.sidebar.subheader("Detection Parameters")
    conf_threshold = st.sidebar.slider(
        "Confidence Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.25,
        step=0.05,
        help="Minimum confidence for detections"
    )
    
    iou_threshold = st.sidebar.slider(
        "IoU Threshold (NMS)",
        min_value=0.0,
        max_value=1.0,
        value=0.45,
        step=0.05,
        help="IoU threshold for Non-Maximum Suppression"
    )
    
    # Input source
    st.sidebar.subheader("Input Source")
    source_type = st.sidebar.radio(
        "Select Input Type",
        ["📷 Upload Image", "🎥 Upload Video", "📹 Webcam"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 About")
    st.sidebar.info(
        "This face detection system uses YOLOv8 for real-time face detection. "
        "Upload an image or video, or use your webcam for live detection."
    )
    
    # Main content
    if source_type == "📷 Upload Image":
        st.header("📷 Image Detection")
        
        uploaded_file = st.file_uploader(
            "Upload an image",
            type=['jpg', 'jpeg', 'png', 'bmp', 'webp']
        )
        
        if uploaded_file is not None:
            # Load image
            image = Image.open(uploaded_file)
            image_np = np.array(image)
            
            # Convert RGB to BGR for OpenCV
            if len(image_np.shape) == 3 and image_np.shape[2] == 3:
                image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            
            # Process image
            with st.spinner("🔍 Detecting faces..."):
                annotated, num_faces, inference_time = process_image(
                    model, image_np, conf_threshold, iou_threshold
                )
            
            # Display results
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(
                    f'<div class="metric-card"><h3>{num_faces}</h3><p>Faces Detected</p></div>',
                    unsafe_allow_html=True
                )
            
            with col2:
                fps = 1.0 / inference_time if inference_time > 0 else 0
                st.markdown(
                    f'<div class="metric-card"><h3>{fps:.1f}</h3><p>FPS</p></div>',
                    unsafe_allow_html=True
                )
            
            with col3:
                st.markdown(
                    f'<div class="metric-card"><h3>{inference_time*1000:.1f}ms</h3><p>Inference Time</p></div>',
                    unsafe_allow_html=True
                )
            
            st.markdown("---")
            
            # Display images
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Original Image")
                st.image(image, use_container_width=True)
            
            with col2:
                st.subheader("Detected Faces")
                # Convert BGR to RGB for display
                annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
                st.image(annotated_rgb, use_container_width=True)
    
    elif source_type == "🎥 Upload Video":
        st.header("🎥 Video Detection")
        
        uploaded_file = st.file_uploader(
            "Upload a video",
            type=['mp4', 'avi', 'mov', 'mkv']
        )
        
        if uploaded_file is not None:
            # Save uploaded video
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            tfile.write(uploaded_file.read())
            video_path = tfile.name
            
            # Process video
            st.info("🎬 Processing video... This may take a while.")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            output_path, total_frames, total_faces, avg_fps = process_video(
                model, video_path, conf_threshold, iou_threshold,
                progress_bar, status_text
            )
            
            status_text.text("✓ Processing complete!")
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(
                    f'<div class="metric-card"><h3>{total_frames}</h3><p>Total Frames</p></div>',
                    unsafe_allow_html=True
                )
            
            with col2:
                st.markdown(
                    f'<div class="metric-card"><h3>{total_faces}</h3><p>Total Faces</p></div>',
                    unsafe_allow_html=True
                )
            
            with col3:
                st.markdown(
                    f'<div class="metric-card"><h3>{avg_fps:.1f}</h3><p>Avg FPS</p></div>',
                    unsafe_allow_html=True
                )
            
            st.markdown("---")
            
            # Display video
            st.subheader("Processed Video")
            st.video(output_path)
            
            # Download button
            with open(output_path, 'rb') as f:
                st.download_button(
                    label="📥 Download Processed Video",
                    data=f,
                    file_name="face_detection_output.mp4",
                    mime="video/mp4"
                )
    
    else:  # Webcam
        st.header("📹 Webcam Detection")
        st.info("🚧 Webcam feature requires local deployment. Use the command line interface for webcam detection.")
        st.code("python src/infer.py --model weights/best.pt --source 0 --display", language="bash")


if __name__ == "__main__":
    main()
