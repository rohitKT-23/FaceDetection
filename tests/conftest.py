"""
Test configuration and fixtures
"""

import pytest
import os
import sys
import numpy as np
import cv2
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def model_path():
    """Path to test model"""
    return 'best_yolov8_face.pt'


@pytest.fixture
def test_image_path(tmp_path):
    """Create a test image"""
    img = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
    img_path = tmp_path / "test_image.jpg"
    cv2.imwrite(str(img_path), img)
    return str(img_path)


@pytest.fixture
def test_image_with_face():
    """Path to real test image with faces"""
    # Use the test image from earlier tests
    test_img = "C:/Users/rohit/.gemini/antigravity/brain/03b289f1-3e0f-45e6-a287-5e86b7e4af9a/test_group_photo_1767692770609.png"
    if os.path.exists(test_img):
        return test_img
    return None


@pytest.fixture
def test_video_path(tmp_path):
    """Create a test video"""
    video_path = tmp_path / "test_video.mp4"
    
    # Create a simple video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(video_path), fourcc, 10, (640, 480))
    
    for _ in range(30):  # 30 frames
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        out.write(frame)
    
    out.release()
    return str(video_path)


@pytest.fixture
def output_dir(tmp_path):
    """Temporary output directory"""
    out_dir = tmp_path / "outputs"
    out_dir.mkdir()
    return str(out_dir)


@pytest.fixture
def flask_app():
    """Flask app instance for testing"""
    try:
        from app import app
        app.config['TESTING'] = True
        return app
    except ImportError:
        return None


@pytest.fixture
def flask_client(flask_app):
    """Flask test client"""
    if flask_app:
        return flask_app.test_client()
    return None
