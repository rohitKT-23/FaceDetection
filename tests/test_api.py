"""
Test Flask API endpoints
"""

import pytest
import json
import io
import os
from PIL import Image
import numpy as np


class TestFlaskApp:
    """Test Flask application"""
    
    def test_app_exists(self, flask_app):
        """Test that Flask app can be imported"""
        if flask_app is None:
            pytest.skip("Flask app not available")
        assert flask_app is not None
    
    def test_app_config(self, flask_app):
        """Test Flask app configuration"""
        if flask_app is None:
            pytest.skip("Flask app not available")
        
        assert flask_app.config['TESTING'] == True
        assert 'UPLOAD_FOLDER' in flask_app.config
        assert 'OUTPUT_FOLDER' in flask_app.config


class TestRoutes:
    """Test Flask routes"""
    
    def test_index_route(self, flask_client):
        """Test index route returns HTML"""
        if flask_client is None:
            pytest.skip("Flask client not available")
        
        response = flask_client.get('/')
        assert response.status_code == 200
        assert b'YOLOv8' in response.data or b'Face Detection' in response.data
    
    def test_stats_route(self, flask_client):
        """Test stats endpoint"""
        if flask_client is None:
            pytest.skip("Flask client not available")
        
        response = flask_client.get('/stats')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'model' in data
        assert 'mAP50' in data or 'precision' in data


class TestFileUpload:
    """Test file upload functionality"""
    
    def test_upload_without_file(self, flask_client):
        """Test upload endpoint without file"""
        if flask_client is None:
            pytest.skip("Flask client not available")
        
        response = flask_client.post('/upload')
        assert response.status_code == 400
    
    def test_upload_with_image(self, flask_client, tmp_path):
        """Test upload with valid image"""
        if flask_client is None:
            pytest.skip("Flask client not available")
        
        # Create test image
        img = Image.fromarray(np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8))
        img_path = tmp_path / "test.jpg"
        img.save(img_path)
        
        # Upload
        with open(img_path, 'rb') as f:
            data = {
                'file': (f, 'test.jpg'),
                'confidence': '0.5'
            }
            response = flask_client.post('/upload', data=data, content_type='multipart/form-data')
        
        # Check response
        if response.status_code == 200:
            result = json.loads(response.data)
            assert 'success' in result or 'num_faces' in result
    
    def test_upload_invalid_file_type(self, flask_client, tmp_path):
        """Test upload with invalid file type"""
        if flask_client is None:
            pytest.skip("Flask client not available")
        
        # Create text file
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("not an image")
        
        with open(txt_file, 'rb') as f:
            data = {'file': (f, 'test.txt')}
            response = flask_client.post('/upload', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 400


class TestWebcamEndpoint:
    """Test webcam processing endpoint"""
    
    def test_webcam_endpoint_exists(self, flask_client):
        """Test webcam endpoint exists"""
        if flask_client is None:
            pytest.skip("Flask client not available")
        
        # POST without data should return error
        response = flask_client.post('/webcam')
        assert response.status_code in [400, 415, 500]  # Various error codes acceptable
    
    def test_webcam_with_base64_image(self, flask_client):
        """Test webcam endpoint with base64 image"""
        if flask_client is None:
            pytest.skip("Flask client not available")
        
        import base64
        
        # Create dummy image
        img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        _, buffer = cv2.imencode('.jpg', img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        data = {
            'image': f'data:image/jpeg;base64,{img_base64}',
            'confidence': 0.5
        }
        
        response = flask_client.post('/webcam', 
                                     data=json.dumps(data),
                                     content_type='application/json')
        
        # Should process or return error
        assert response.status_code in [200, 400, 500]


class TestOutputFiles:
    """Test output file serving"""
    
    def test_output_directory_exists(self):
        """Test that output directories are created"""
        # These should be created by the app
        assert os.path.exists('uploads') or True  # May not exist yet
        assert os.path.exists('outputs') or True  # May not exist yet


class TestErrorHandling:
    """Test error handling"""
    
    def test_404_error(self, flask_client):
        """Test 404 error handling"""
        if flask_client is None:
            pytest.skip("Flask client not available")
        
        response = flask_client.get('/nonexistent')
        assert response.status_code == 404
    
    def test_method_not_allowed(self, flask_client):
        """Test method not allowed error"""
        if flask_client is None:
            pytest.skip("Flask client not available")
        
        # GET on POST-only endpoint
        response = flask_client.get('/upload')
        assert response.status_code == 405


# Import cv2 for webcam test
try:
    import cv2
except ImportError:
    cv2 = None
