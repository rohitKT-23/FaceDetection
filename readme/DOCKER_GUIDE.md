# 🐳 Docker Deployment Guide

Complete guide for deploying the Face Detection application using Docker.

## 📦 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- 2GB+ available disk space
- Model files: `best_yolov8_face.pt` (required)

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

Access at: **http://localhost:5000**

### Option 2: Docker Run

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

# View logs
docker logs -f face-detection-app

# Stop
docker stop face-detection-app
docker rm face-detection-app
```

## 📋 Detailed Instructions

### 1. Build Docker Image

```bash
# Build with tag
docker build -t face-detection:latest .

# Build with specific version
docker build -t face-detection:v1.0.0 .

# Build with no cache
docker build --no-cache -t face-detection .
```

### 2. Run Container

#### Basic Run

```bash
docker run -d \
  -p 5000:5000 \
  --name face-detection-app \
  face-detection
```

#### With Volume Mounts

```bash
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/outputs:/app/outputs \
  -v $(pwd)/best_yolov8_face.pt:/app/best_yolov8_face.pt:ro \
  --name face-detection-app \
  face-detection
```

#### With Environment Variables

```bash
docker run -d \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e PYTHONUNBUFFERED=1 \
  --name face-detection-app \
  face-detection
```

### 3. Docker Compose

#### Start Services

```bash
# Start in background
docker-compose up -d

# Start with build
docker-compose up -d --build

# Start with nginx
docker-compose --profile with-nginx up -d
```

#### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web

# Last 100 lines
docker-compose logs --tail=100 web
```

#### Stop Services

```bash
# Stop containers
docker-compose stop

# Stop and remove
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## 🔧 Configuration

### Environment Variables

| Variable           | Default    | Description             |
| ------------------ | ---------- | ----------------------- |
| `FLASK_ENV`        | production | Flask environment       |
| `FLASK_APP`        | app.py     | Flask app file          |
| `PYTHONUNBUFFERED` | 1          | Python output buffering |

### Volumes

| Host Path               | Container Path             | Purpose           |
| ----------------------- | -------------------------- | ----------------- |
| `./uploads`             | `/app/uploads`             | Uploaded files    |
| `./outputs`             | `/app/outputs`             | Processed results |
| `./best_yolov8_face.pt` | `/app/best_yolov8_face.pt` | Model weights     |

### Ports

| Host | Container | Service          |
| ---- | --------- | ---------------- |
| 5000 | 5000      | Flask web app    |
| 80   | 80        | Nginx (optional) |

## 🏥 Health Checks

### Container Health

```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' face-detection-app

# View health logs
docker inspect --format='{{json .State.Health}}' face-detection-app | jq
```

### Manual Health Check

```bash
# Inside container
docker exec face-detection-app python -c "import requests; print(requests.get('http://localhost:5000/stats').json())"

# From host
curl http://localhost:5000/stats
```

## 📊 Monitoring

### View Container Stats

```bash
# Real-time stats
docker stats face-detection-app

# One-time stats
docker stats --no-stream face-detection-app
```

### View Logs

```bash
# Follow logs
docker logs -f face-detection-app

# Last 100 lines
docker logs --tail=100 face-detection-app

# Since timestamp
docker logs --since 2024-01-01T00:00:00 face-detection-app
```

## 🔍 Debugging

### Enter Container

```bash
# Interactive shell
docker exec -it face-detection-app /bin/bash

# Run command
docker exec face-detection-app ls -la /app
```

### Check Files

```bash
# List files
docker exec face-detection-app ls -la /app

# Check model
docker exec face-detection-app ls -lh /app/*.pt

# View logs
docker exec face-detection-app cat /app/app.log
```

### Test Inference

```bash
# Run CLI inside container
docker exec face-detection-app python detect.py --help
```

## 🚀 Production Deployment

### With Nginx Reverse Proxy

```bash
# Start with nginx
docker-compose --profile with-nginx up -d

# Access via nginx
curl http://localhost/stats
```

### With Custom Domain

```yaml
# docker-compose.override.yml
services:
  nginx:
    environment:
      - VIRTUAL_HOST=face-detection.example.com
      - LETSENCRYPT_HOST=face-detection.example.com
      - LETSENCRYPT_EMAIL=admin@example.com
```

### With Resource Limits

```bash
docker run -d \
  -p 5000:5000 \
  --memory="2g" \
  --cpus="2.0" \
  --name face-detection-app \
  face-detection
```

## 🔐 Security

### Run as Non-Root User

Add to Dockerfile:

```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

### Read-Only Root Filesystem

```bash
docker run -d \
  -p 5000:5000 \
  --read-only \
  --tmpfs /tmp \
  --tmpfs /app/uploads \
  --tmpfs /app/outputs \
  face-detection
```

### Network Isolation

```bash
# Create custom network
docker network create face-detection-net

# Run with custom network
docker run -d \
  -p 5000:5000 \
  --network face-detection-net \
  face-detection
```

## 📈 Performance Optimization

### Multi-Stage Build

```dockerfile
# Build stage
FROM python:3.10-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.10-slim
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app
CMD ["python", "app.py"]
```

### Layer Caching

```bash
# Build with cache
docker build -t face-detection .

# Build without cache
docker build --no-cache -t face-detection .
```

## 🧪 Testing

### Test Build

```bash
# Build test image
docker build -t face-detection:test .

# Run tests in container
docker run --rm face-detection:test python -m pytest tests/
```

### Test Container

```bash
# Start container
docker-compose up -d

# Wait for health check
sleep 10

# Test endpoint
curl http://localhost:5000/stats

# Stop container
docker-compose down
```

## 📦 Image Management

### List Images

```bash
# All images
docker images

# Face detection images
docker images face-detection
```

### Remove Images

```bash
# Remove specific image
docker rmi face-detection:latest

# Remove all unused images
docker image prune -a
```

### Save/Load Images

```bash
# Save image to file
docker save face-detection:latest > face-detection.tar

# Load image from file
docker load < face-detection.tar
```

## 🌐 Registry

### Tag for Registry

```bash
# Tag for Docker Hub
docker tag face-detection:latest username/face-detection:latest

# Tag for private registry
docker tag face-detection:latest registry.example.com/face-detection:latest
```

### Push to Registry

```bash
# Login
docker login

# Push
docker push username/face-detection:latest
```

### Pull from Registry

```bash
# Pull latest
docker pull username/face-detection:latest

# Pull specific version
docker pull username/face-detection:v1.0.0
```

## 🔄 Updates

### Update Application

```bash
# Pull latest code
git pull

# Rebuild image
docker-compose build

# Restart services
docker-compose up -d
```

### Update Dependencies

```bash
# Update requirements.txt
# Rebuild image
docker-compose build --no-cache

# Restart
docker-compose up -d
```

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs face-detection-app

# Check events
docker events --filter container=face-detection-app

# Inspect container
docker inspect face-detection-app
```

### Port Already in Use

```bash
# Find process using port
lsof -i :5000  # Linux/Mac
netstat -ano | findstr :5000  # Windows

# Use different port
docker run -p 5001:5000 face-detection
```

### Out of Disk Space

```bash
# Clean up
docker system prune -a

# Remove unused volumes
docker volume prune

# Check disk usage
docker system df
```

## 📝 Best Practices

1. **Use .dockerignore**: Exclude unnecessary files
2. **Multi-stage builds**: Reduce image size
3. **Health checks**: Monitor container health
4. **Volume mounts**: Persist data
5. **Environment variables**: Configure at runtime
6. **Resource limits**: Prevent resource exhaustion
7. **Logging**: Use structured logging
8. **Security**: Run as non-root user

## 📊 Benchmarks

| Metric       | Value       |
| ------------ | ----------- |
| Image Size   | ~1.5 GB     |
| Build Time   | ~5 minutes  |
| Startup Time | ~10 seconds |
| Memory Usage | ~500 MB     |
| CPU Usage    | 1-2 cores   |

## ✅ Checklist

Before deployment:

- [ ] Model files present
- [ ] Docker installed
- [ ] Ports available
- [ ] Sufficient disk space
- [ ] Environment variables set
- [ ] Volumes configured
- [ ] Health checks working
- [ ] Logs accessible

## 🔗 Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Status**: ✅ Production Ready  
**Image**: face-detection:latest  
**Size**: ~1.5 GB
