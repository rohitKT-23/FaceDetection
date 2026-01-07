"""
Test face detection inference
"""

import pytest
import os
import cv2
import numpy as np


class TestImageInference:
    """Test face detection on images"""
    
    def test_detect_on_random_image(self, model_path, test_image_path):
        """Test detection on random image"""
        try:
            from ultralytics import YOLO
            
            model = YOLO(model_path)
            results = model(test_image_path, verbose=False)
            
            assert results is not None
            assert len(results) > 0
            
        except ImportError:
            pytest.skip("Ultralytics not installed")
    
    def test_detect_with_real_faces(self, model_path, test_image_with_face):
        """Test detection on image with real faces"""
        if test_image_with_face is None:
            pytest.skip("Real test image not available")
        
        try:
            from ultralytics import YOLO
            
            model = YOLO(model_path)
            results = model(test_image_with_face, verbose=False)[0]
            boxes = results.boxes
            
            # Should detect at least one face
            assert len(boxes) > 0, "No faces detected in test image"
            
            # Check confidence scores
            for box in boxes:
                conf = float(box.conf[0])
                assert 0 <= conf <= 1, f"Invalid confidence: {conf}"
            
        except ImportError:
            pytest.skip("Ultralytics not installed")
    
    def test_bounding_box_format(self, model_path, test_image_with_face):
        """Test bounding box format"""
        if test_image_with_face is None:
            pytest.skip("Real test image not available")
        
        try:
            from ultralytics import YOLO
            
            model = YOLO(model_path)
            results = model(test_image_with_face, verbose=False)[0]
            boxes = results.boxes
            
            if len(boxes) > 0:
                box = boxes[0]
                x1, y1, x2, y2 = box.xyxy[0]
                
                # Check coordinates are valid
                assert x1 < x2, "Invalid x coordinates"
                assert y1 < y2, "Invalid y coordinates"
                assert x1 >= 0 and y1 >= 0, "Negative coordinates"
                
        except ImportError:
            pytest.skip("Ultralytics not installed")
    
    def test_confidence_threshold(self, model_path, test_image_with_face):
        """Test confidence threshold filtering"""
        if test_image_with_face is None:
            pytest.skip("Real test image not available")
        
        try:
            from ultralytics import YOLO
            
            model = YOLO(model_path)
            
            # Low confidence
            results_low = model(test_image_with_face, conf=0.3, verbose=False)[0]
            
            # High confidence
            results_high = model(test_image_with_face, conf=0.8, verbose=False)[0]
            
            # High confidence should have fewer or equal detections
            assert len(results_high.boxes) <= len(results_low.boxes)
            
        except ImportError:
            pytest.skip("Ultralytics not installed")


class TestVideoInference:
    """Test face detection on videos"""
    
    def test_detect_on_video(self, model_path, test_video_path):
        """Test detection on video file"""
        try:
            from ultralytics import YOLO
            
            model = YOLO(model_path)
            cap = cv2.VideoCapture(test_video_path)
            
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                results = model(frame, verbose=False)
                assert results is not None
            
        except ImportError:
            pytest.skip("Ultralytics not installed")


class TestBatchInference:
    """Test batch processing"""
    
    def test_batch_processing(self, model_path, tmp_path):
        """Test processing multiple images"""
        try:
            from ultralytics import YOLO
            
            # Create multiple test images
            images = []
            for i in range(3):
                img = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
                img_path = tmp_path / f"test_{i}.jpg"
                cv2.imwrite(str(img_path), img)
                images.append(str(img_path))
            
            model = YOLO(model_path)
            results = model(images, verbose=False)
            
            assert len(results) == 3
            
        except ImportError:
            pytest.skip("Ultralytics not installed")


class TestInferencePerformance:
    """Test inference performance"""
    
    def test_inference_speed(self, model_path, test_image_path):
        """Test that inference completes in reasonable time"""
        try:
            from ultralytics import YOLO
            import time
            
            model = YOLO(model_path)
            
            # Warmup
            _ = model(test_image_path, verbose=False)
            
            # Measure
            start = time.time()
            _ = model(test_image_path, verbose=False)
            elapsed = time.time() - start
            
            # Should complete in less than 5 seconds on CPU
            assert elapsed < 5.0, f"Inference too slow: {elapsed:.2f}s"
            
        except ImportError:
            pytest.skip("Ultralytics not installed")
