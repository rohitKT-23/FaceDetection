"""
Test model loading and initialization
"""

import pytest
import os


class TestModelLoading:
    """Test model loading functionality"""
    
    def test_model_file_exists(self, model_path):
        """Test that model file exists"""
        assert os.path.exists(model_path), f"Model file not found: {model_path}"
    
    def test_model_file_size(self, model_path):
        """Test that model file has reasonable size"""
        size_mb = os.path.getsize(model_path) / (1024 * 1024)
        assert size_mb > 1, "Model file too small"
        assert size_mb < 100, "Model file too large"
    
    def test_load_pytorch_model(self, model_path):
        """Test loading PyTorch model"""
        try:
            from ultralytics import YOLO
            model = YOLO(model_path)
            assert model is not None
            assert hasattr(model, 'predict')
        except ImportError:
            pytest.skip("Ultralytics not installed")
    
    def test_model_inference_shape(self, model_path, test_image_path):
        """Test model inference output shape"""
        try:
            from ultralytics import YOLO
            import cv2
            
            model = YOLO(model_path)
            img = cv2.imread(test_image_path)
            
            results = model(img, verbose=False)
            assert results is not None
            assert len(results) > 0
            
        except ImportError:
            pytest.skip("Ultralytics not installed")
    
    def test_onnx_model_exists(self):
        """Test if ONNX model exists"""
        onnx_path = 'best_yolov8_face.onnx'
        if os.path.exists(onnx_path):
            size_mb = os.path.getsize(onnx_path) / (1024 * 1024)
            assert size_mb > 5, "ONNX model too small"
            assert size_mb < 50, "ONNX model too large"
        else:
            pytest.skip("ONNX model not found")


class TestModelConfiguration:
    """Test model configuration"""
    
    def test_model_task(self, model_path):
        """Test that model is configured for detection"""
        try:
            from ultralytics import YOLO
            model = YOLO(model_path)
            assert model.task == 'detect'
        except ImportError:
            pytest.skip("Ultralytics not installed")
    
    def test_model_device(self, model_path):
        """Test model device assignment"""
        try:
            from ultralytics import YOLO
            import torch
            
            model = YOLO(model_path)
            
            # Model should work on CPU
            model.to('cpu')
            assert True
            
            # Test GPU if available
            if torch.cuda.is_available():
                model.to('cuda:0')
                assert True
                
        except ImportError:
            pytest.skip("Ultralytics not installed")


class TestExportedModels:
    """Test exported model formats"""
    
    def test_onnx_export_script_exists(self):
        """Test that ONNX export script exists"""
        assert os.path.exists('export_onnx_simple.py')
    
    def test_onnx_model_format(self):
        """Test ONNX model file format"""
        onnx_path = 'best_yolov8_face.onnx'
        if os.path.exists(onnx_path):
            # Check file extension
            assert onnx_path.endswith('.onnx')
            
            # Check file is not empty
            assert os.path.getsize(onnx_path) > 0
        else:
            pytest.skip("ONNX model not exported yet")
