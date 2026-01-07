# 📁 Project Structure

Complete file and folder organization for the Face Detection project.

## 🗂️ Root Directory

```
FaceDetection/
├── 📄 README.md                      # Main project documentation
├── 📄 requirements.txt               # Python dependencies
├── 📄 pytest.ini                     # Pytest configuration
├── 📄 .gitignore                     # Git ignore rules
├── 📄 .dockerignore                  # Docker ignore rules
│
├── 🐳 Docker Files
│   ├── Dockerfile                    # Production Docker image
│   ├── docker-compose.yml            # Multi-service setup
│   └── nginx.conf                    # Nginx reverse proxy config
│
├── 🌐 Web Application
│   ├── app.py                        # Flask backend (main app)
│   └── templates/
│       └── index.html                # Frontend UI
│
├── 🔧 CLI & Tools
│   ├── detect.py                     # CLI detection tool
│   ├── export_onnx.py                # Full ONNX export script
│   └── export_onnx_simple.py         # Simple ONNX export
│
├── 🤖 Model Files
│   ├── best_yolov8_face.pt           # PyTorch model (6.2 MB)
│   ├── last_yolov8_face.pt           # Last epoch model
│   └── best_yolov8_face.onnx         # ONNX model (11.67 MB)
│
├── 📊 Training Results
│   ├── training_results.csv          # Training metrics
│   ├── training_plots.png            # Training graphs
│   └── facedetection.ipynb           # Kaggle training notebook
│
├── 🧪 Tests
│   └── tests/
│       ├── __init__.py               # Package init
│       ├── conftest.py               # Pytest fixtures
│       ├── test_model.py             # Model loading tests
│       ├── test_inference.py         # Detection tests
│       ├── test_api.py               # Flask API tests
│       ├── test_cli.py               # CLI tool tests
│       └── fixtures/                 # Test data
│
├── 📚 Documentation
│   └── readme/
│       ├── CLI_GUIDE.md              # CLI usage guide
│       ├── DOCKER_GUIDE.md           # Docker deployment
│       ├── TESTING_GUIDE.md          # Testing instructions
│       ├── ONNX_EXPORT_GUIDE.md      # ONNX export guide
│       ├── PROJECT_COMPLIANCE_REPORT.md  # Compliance analysis
│       └── PROJECT_COMPLETE.md       # Completion summary
│
├── ⚙️ CI/CD
│   └── .github/
│       └── workflows/
│           └── tests.yml             # GitHub Actions workflow
│
├── 📁 Runtime Directories
│   ├── uploads/                      # Uploaded files (gitignored)
│   ├── outputs/                      # Processed results (gitignored)
│   └── __pycache__/                  # Python cache (gitignored)
│
└── 🗑️ Temporary (gitignored)
    ├── test_images/                  # Test images
    ├── .pytest_cache/                # Pytest cache
    └── data/                         # Dataset (if present)
```

## 📊 File Count Summary

| Category           | Count | Size   |
| ------------------ | ----- | ------ |
| **Python Scripts** | 4     | ~30 KB |
| **Model Files**    | 3     | ~24 MB |
| **Documentation**  | 7     | ~60 KB |
| **Tests**          | 5     | ~15 KB |
| **Config Files**   | 6     | ~5 KB  |
| **Templates**      | 1     | ~15 KB |
| **Total Files**    | ~26   | ~25 MB |

## 🔍 File Descriptions

### Core Application

| File                   | Purpose                       | Size    |
| ---------------------- | ----------------------------- | ------- |
| `app.py`               | Flask web server, REST API    | 7.4 KB  |
| `detect.py`            | CLI tool for batch processing | 13.2 KB |
| `templates/index.html` | Web UI frontend               | 15 KB   |

### Model Export

| File                    | Purpose                            | Size   |
| ----------------------- | ---------------------------------- | ------ |
| `export_onnx.py`        | Full ONNX export with verification | 8.8 KB |
| `export_onnx_simple.py` | Simple export (Python 3.14)        | 2.8 KB |

### Models

| File                    | Format  | Size     | Use Case                |
| ----------------------- | ------- | -------- | ----------------------- |
| `best_yolov8_face.pt`   | PyTorch | 6.2 MB   | Training, GPU inference |
| `last_yolov8_face.pt`   | PyTorch | 6.2 MB   | Last epoch checkpoint   |
| `best_yolov8_face.onnx` | ONNX    | 11.67 MB | CPU optimization        |

### Tests

| File                | Tests  | Coverage        |
| ------------------- | ------ | --------------- |
| `test_model.py`     | 8      | Model loading   |
| `test_inference.py` | 10     | Face detection  |
| `test_api.py`       | 12     | Flask endpoints |
| `test_cli.py`       | 8      | CLI tool        |
| **Total**           | **38** | **80%+**        |

### Documentation

| File                           | Pages | Purpose             |
| ------------------------------ | ----- | ------------------- |
| `README.md`                    | 1     | Main documentation  |
| `CLI_GUIDE.md`                 | 3     | CLI usage           |
| `DOCKER_GUIDE.md`              | 4     | Docker deployment   |
| `TESTING_GUIDE.md`             | 3     | Testing guide       |
| `ONNX_EXPORT_GUIDE.md`         | 2     | ONNX export         |
| `PROJECT_COMPLIANCE_REPORT.md` | 5     | Compliance analysis |
| `PROJECT_COMPLETE.md`          | 4     | Completion summary  |

### Configuration

| File                 | Purpose                 |
| -------------------- | ----------------------- |
| `requirements.txt`   | Python dependencies     |
| `pytest.ini`         | Pytest configuration    |
| `.gitignore`         | Git ignore rules        |
| `.dockerignore`      | Docker ignore rules     |
| `Dockerfile`         | Docker image definition |
| `docker-compose.yml` | Multi-service setup     |
| `nginx.conf`         | Nginx proxy config      |

## 🎯 Important Files

### Must Have (Essential)

1. ✅ `app.py` - Main application
2. ✅ `best_yolov8_face.pt` - Trained model
3. ✅ `requirements.txt` - Dependencies
4. ✅ `README.md` - Documentation
5. ✅ `templates/index.html` - Frontend

### Should Have (Recommended)

6. ✅ `detect.py` - CLI tool
7. ✅ `Dockerfile` - Containerization
8. ✅ `tests/` - Test suite
9. ✅ `.gitignore` - Git configuration

### Nice to Have (Optional)

10. ✅ `best_yolov8_face.onnx` - ONNX model
11. ✅ `docker-compose.yml` - Easy deployment
12. ✅ `readme/` - Additional docs
13. ✅ `.github/workflows/` - CI/CD

## 📦 Deployment Files

### Local Development

- `app.py`
- `requirements.txt`
- `best_yolov8_face.pt`

### Docker Deployment

- `Dockerfile`
- `docker-compose.yml`
- `.dockerignore`
- `nginx.conf` (optional)

### CLI Usage

- `detect.py`
- `best_yolov8_face.pt`

## 🗑️ Gitignored Directories

These are created at runtime and not tracked:

- `uploads/` - User uploaded files
- `outputs/` - Processed results
- `__pycache__/` - Python cache
- `.pytest_cache/` - Test cache
- `data/` - Dataset files
- `runs/` - Training outputs
- `test_images/` - Temporary test files

## 📏 Size Breakdown

```
Total Project Size: ~25 MB

Models:          24 MB (96%)
Documentation:   60 KB (0.2%)
Code:           50 KB (0.2%)
Config:         10 KB (0.04%)
Other:          900 KB (3.6%)
```

## 🔄 Git Tracking

### Tracked Files (in git)

- ✅ All Python scripts
- ✅ Documentation
- ✅ Configuration files
- ✅ Model files (essential ones)
- ✅ Templates
- ✅ Tests

### Not Tracked (gitignored)

- ❌ Python cache (`__pycache__/`)
- ❌ Virtual environments
- ❌ Dataset files
- ❌ Uploaded files
- ❌ Output files
- ❌ Test cache
- ❌ Logs

## 🚀 Quick Navigation

### For Users

- Start here: `README.md`
- Web app: `python app.py`
- CLI tool: `python detect.py --help`

### For Developers

- Tests: `tests/`
- Documentation: `readme/`
- CI/CD: `.github/workflows/`

### For DevOps

- Docker: `Dockerfile`, `docker-compose.yml`
- Config: `requirements.txt`, `pytest.ini`
- Deployment: `readme/DOCKER_GUIDE.md`

## ✅ Verification Checklist

Before deployment, ensure:

- [ ] All essential files present
- [ ] Model files available
- [ ] Dependencies installable
- [ ] Tests passing
- [ ] Documentation complete
- [ ] Docker builds successfully
- [ ] .gitignore configured
- [ ] No sensitive data committed

## 📝 File Naming Conventions

- **Python scripts**: `lowercase_with_underscores.py`
- **Documentation**: `UPPERCASE_WITH_UNDERSCORES.md`
- **Config files**: `lowercase.ext` or `.dotfile`
- **Models**: `descriptive_name_version.ext`

---

**Last Updated**: January 7, 2026  
**Total Files**: 26  
**Total Size**: ~25 MB  
**Status**: ✅ Clean and Organized
