# 👤 YOLOv8 Face Detection Web App

A beautiful, real-time face detection web application powered by YOLOv8 and Flask.

![mAP](https://img.shields.io/badge/mAP@0.5-65.3%25-brightgreen)
![Precision](https://img.shields.io/badge/Precision-83.8%25-blue)
![Speed](https://img.shields.io/badge/GPU-340_FPS-red)
![Size](https://img.shields.io/badge/Model-6.2_MB-orange)

## 🌟 Features

### 📁 Upload & Process

- **Image Detection**: Upload images and detect all faces
- **Video Processing**: Process entire videos with face detection
- **Drag & Drop**: Easy file upload with drag-and-drop support
- **Confidence Control**: Adjustable confidence threshold (0-1)

### 📹 Real-time Webcam

- **Live Detection**: Real-time face detection from webcam
- **FPS Counter**: Monitor processing speed
- **Face Counter**: See number of detected faces
- **Confidence Display**: View confidence scores for each detection

### 🎨 Beautiful UI

- **Modern Design**: Gradient backgrounds and glassmorphism
- **Responsive**: Works on desktop, tablet, and mobile
- **Animated**: Smooth transitions and loading states
- **Dark Mode Ready**: Professional color scheme

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the App

```bash
python app.py
```

### 3. Open Browser

```
http://localhost:5000
```

## 📊 Model Performance

| Metric           | Value   |
| ---------------- | ------- |
| **mAP@0.5**      | 65.3%   |
| **mAP@0.5:0.95** | 35.8%   |
| **Precision**    | 83.8%   |
| **Recall**       | 57.3%   |
| **Speed (GPU)**  | 340 FPS |
| **Speed (CPU)**  | 10 FPS  |
| **Model Size**   | 6.2 MB  |

## 🎯 Usage Examples

### Upload Image

1. Click or drag-drop an image
2. Adjust confidence threshold
3. Click "Detect Faces"
4. View results with bounding boxes

### Upload Video

1. Upload MP4/AVI video file
2. Set confidence threshold
3. Process video
4. Download processed video

### Webcam Detection

1. Click "Start Webcam"
2. Allow camera access
3. See real-time face detection
4. Adjust confidence as needed

## 🛠️ Technical Stack

- **Backend**: Flask (Python)
- **Model**: YOLOv8n (Ultralytics)
- **Frontend**: HTML5, CSS3, JavaScript
- **Computer Vision**: OpenCV
- **Dataset**: WIDER FACE (12,872 train + 3,222 val)

## 📁 Project Structure

```
FaceDetection/
├── app.py                      # Flask backend
├── templates/
│   └── index.html             # Frontend UI
├── best_yolov8_face.pt        # Trained model
├── requirements.txt           # Dependencies
├── uploads/                   # Uploaded files
└── outputs/                   # Processed results
```

## 🔧 API Endpoints

### POST /upload

Upload and process image/video

```json
{
  "file": <file>,
  "confidence": 0.5
}
```

### POST /webcam

Process webcam frame

```json
{
  "image": "data:image/jpeg;base64,...",
  "confidence": 0.5
}
```

### GET /stats

Get model statistics

```json
{
  "model": "YOLOv8n Face Detection",
  "mAP50": "65.3%",
  "precision": "83.8%",
  ...
}
```

## 🎓 Training Details

- **Dataset**: WIDER FACE
- **Training Time**: 2.3 hours on Tesla T4
- **Epochs**: 50
- **Batch Size**: 16
- **Optimizer**: AdamW
- **Platform**: Kaggle GPU

## 🚀 Deployment

### Local Development

```bash
python app.py
```

### Production (Gunicorn)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 🐳 Docker (Recommended)

#### Quick Start with Docker Compose

```bash
# Start application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop application
docker-compose down
```

Access at: **http://localhost:5000**

#### Docker Run

```bash
# Build image
docker build -t face-detection .

# Run container
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/outputs:/app/outputs \
  --name face-detection-app \
  face-detection
```

#### With Nginx Reverse Proxy

```bash
# Start with nginx
docker-compose --profile with-nginx up -d
```

Access at: **http://localhost** (port 80)

**📖 See [DOCKER_GUIDE.md](DOCKER_GUIDE.md) for complete Docker documentation**

### Cloud Deployment

- **AWS**: ECS, EC2, or Lambda
- **GCP**: Cloud Run, Compute Engine
- **Azure**: Container Instances, App Service
- **Heroku**: Container deployment

## 📸 Screenshots

### Upload Interface

- Drag & drop file upload
- Confidence threshold slider
- Real-time processing status

### Webcam Detection

- Live video feed
- FPS counter
- Face count display
- Detection confidence badges

### Results Display

- Annotated images/videos
- Detection statistics
- Confidence scores
- Bounding box coordinates

## 💡 Use Cases

1. **Security Systems**: Real-time surveillance
2. **Attendance Systems**: Automated face counting
3. **Photo Organization**: Automatic face tagging
4. **Video Analytics**: Face detection in videos
5. **Research**: Computer vision experiments

## 🔮 Future Enhancements

- [ ] Face Recognition (identify specific people)
- [ ] Age & Gender Detection
- [ ] Emotion Recognition
- [ ] Multiple Face Tracking
- [ ] Export to ONNX for faster inference
- [ ] Batch Processing
- [ ] REST API with authentication
- [ ] Cloud Deployment (AWS/GCP)

## 📝 License

MIT License - Feel free to use for personal and commercial projects

## 👨‍💻 Author

**Rohit**

- GitHub: [@rohitKT-23](https://github.com/rohitKT-23)
- Project: [FaceDetection](https://github.com/rohitKT-23/FaceDetection)

## 🙏 Acknowledgments

- **YOLOv8**: Ultralytics team
- **Dataset**: WIDER FACE dataset creators
- **Training**: Kaggle for free GPU resources

## 📞 Support

For issues or questions:

1. Open an issue on GitHub
2. Check existing documentation
3. Review training logs

---

**Made with ❤️ using YOLOv8 and Flask**

**Status**: ✅ Production Ready | 🚀 Real-time Performance | 💯 High Accuracy
