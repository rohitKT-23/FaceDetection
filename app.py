from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from ultralytics import YOLO
import base64
from pathlib import Path
import json
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}

# Create folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Load model
MODEL_PATH = 'best_yolov8_face.pt'
model = YOLO(MODEL_PATH)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def is_video(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in {'mp4', 'avi', 'mov'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    # Save uploaded file
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}_{filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Get confidence threshold
    conf_threshold = float(request.form.get('confidence', 0.5))
    
    # Process based on file type
    if is_video(filename):
        result = process_video(filepath, filename, conf_threshold)
    else:
        result = process_image(filepath, filename, conf_threshold)
    
    return jsonify(result)

def process_image(filepath, filename, conf_threshold=0.5):
    """Process single image"""
    # Run inference
    results = model(filepath, conf=conf_threshold)[0]
    
    # Get detections
    boxes = results.boxes
    num_faces = len(boxes)
    
    # Draw boxes on image
    img = cv2.imread(filepath)
    detections = []
    
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        
        # Draw rectangle
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Draw confidence
        label = f'{conf:.2f}'
        cv2.putText(img, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.5, (0, 255, 0), 2)
        
        detections.append({
            'bbox': [x1, y1, x2, y2],
            'confidence': conf
        })
    
    # Save output image
    output_filename = f'output_{filename}'
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
    cv2.imwrite(output_path, img)
    
    return {
        'success': True,
        'num_faces': num_faces,
        'detections': detections,
        'output_image': f'/outputs/{output_filename}',
        'type': 'image'
    }

def process_video(filepath, filename, conf_threshold=0.5):
    """Process video file"""
    cap = cv2.VideoCapture(filepath)
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Output video
    output_filename = f'output_{filename}'
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    frame_count = 0
    total_detections = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Run inference
        results = model(frame, conf=conf_threshold, verbose=False)[0]
        boxes = results.boxes
        
        # Draw boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f'{conf:.2f}'
            cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX,
                       0.5, (0, 255, 0), 2)
            
            total_detections += 1
        
        out.write(frame)
        frame_count += 1
    
    cap.release()
    out.release()
    
    return {
        'success': True,
        'total_frames': total_frames,
        'processed_frames': frame_count,
        'total_detections': total_detections,
        'avg_faces_per_frame': total_detections / frame_count if frame_count > 0 else 0,
        'output_video': f'/outputs/{output_filename}',
        'type': 'video'
    }

@app.route('/webcam', methods=['POST'])
def process_webcam():
    """Process webcam frame"""
    data = request.json
    image_data = data['image'].split(',')[1]
    conf_threshold = float(data.get('confidence', 0.5))
    
    # Decode base64 image
    img_bytes = base64.b64decode(image_data)
    nparr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Run inference
    results = model(frame, conf=conf_threshold, verbose=False)[0]
    boxes = results.boxes
    
    # Draw boxes
    detections = []
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f'{conf:.2f}'
        cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX,
                   0.5, (0, 255, 0), 2)
        
        detections.append({
            'bbox': [x1, y1, x2, y2],
            'confidence': conf
        })
    
    # Encode result
    _, buffer = cv2.imencode('.jpg', frame)
    result_base64 = base64.b64encode(buffer).decode('utf-8')
    
    return jsonify({
        'success': True,
        'num_faces': len(boxes),
        'detections': detections,
        'image': f'data:image/jpeg;base64,{result_base64}'
    })

@app.route('/outputs/<filename>')
def serve_output(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

@app.route('/stats')
def get_stats():
    """Get model statistics"""
    return jsonify({
        'model': 'YOLOv8n Face Detection',
        'parameters': '3M',
        'size': '6.2 MB',
        'mAP50': '65.3%',
        'precision': '83.8%',
        'recall': '57.3%',
        'speed_gpu': '340 FPS',
        'speed_cpu': '10 FPS'
    })

if __name__ == '__main__':
    print("="*60)
    print("🚀 Face Detection Web App Starting...")
    print("="*60)
    print(f"Model: {MODEL_PATH}")
    print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"Output folder: {app.config['OUTPUT_FOLDER']}")
    print("="*60)
    print("Open browser: http://localhost:5000")
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5000)
