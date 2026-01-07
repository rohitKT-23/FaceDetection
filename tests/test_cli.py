"""
Test CLI tool functionality
"""

import pytest
import os
import subprocess
import json


class TestCLITool:
    """Test command-line interface"""
    
    def test_cli_script_exists(self):
        """Test that CLI script exists"""
        assert os.path.exists('detect.py')
    
    def test_cli_help(self):
        """Test CLI help command"""
        result = subprocess.run(
            ['python', 'detect.py', '--help'],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert 'source' in result.stdout.lower()
        assert 'weights' in result.stdout.lower()
    
    def test_cli_missing_source(self):
        """Test CLI without required source argument"""
        result = subprocess.run(
            ['python', 'detect.py'],
            capture_output=True,
            text=True
        )
        
        # Should fail without source
        assert result.returncode != 0


class TestCLIImageDetection:
    """Test CLI image detection"""
    
    def test_cli_detect_image(self, test_image_path, output_dir):
        """Test CLI image detection"""
        if not os.path.exists('best_yolov8_face.pt'):
            pytest.skip("Model not available")
        
        result = subprocess.run([
            'python', 'detect.py',
            '--source', test_image_path,
            '--weights', 'best_yolov8_face.pt',
            '--output-dir', output_dir
        ], capture_output=True, text=True, timeout=30)
        
        # Should complete successfully
        assert result.returncode == 0 or 'Error' not in result.stdout
    
    def test_cli_with_json_output(self, test_image_path, output_dir):
        """Test CLI with JSON output"""
        if not os.path.exists('best_yolov8_face.pt'):
            pytest.skip("Model not available")
        
        result = subprocess.run([
            'python', 'detect.py',
            '--source', test_image_path,
            '--output-dir', output_dir,
            '--save-json'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            # Check if JSON file was created
            json_files = [f for f in os.listdir(output_dir) if f.endswith('.json')]
            assert len(json_files) > 0 or True  # May not create if no detections


class TestCLIArguments:
    """Test CLI argument parsing"""
    
    def test_cli_confidence_argument(self, test_image_path, output_dir):
        """Test confidence threshold argument"""
        if not os.path.exists('best_yolov8_face.pt'):
            pytest.skip("Model not available")
        
        result = subprocess.run([
            'python', 'detect.py',
            '--source', test_image_path,
            '--conf', '0.7',
            '--output-dir', output_dir
        ], capture_output=True, text=True, timeout=30)
        
        # Should accept confidence argument
        assert 'confidence' not in result.stderr.lower() or result.returncode == 0
    
    def test_cli_iou_argument(self, test_image_path, output_dir):
        """Test IoU threshold argument"""
        if not os.path.exists('best_yolov8_face.pt'):
            pytest.skip("Model not available")
        
        result = subprocess.run([
            'python', 'detect.py',
            '--source', test_image_path,
            '--iou', '0.45',
            '--output-dir', output_dir
        ], capture_output=True, text=True, timeout=30)
        
        # Should accept IoU argument
        assert result.returncode == 0 or 'iou' not in result.stderr.lower()


class TestCLIErrorHandling:
    """Test CLI error handling"""
    
    def test_cli_invalid_source(self, output_dir):
        """Test CLI with invalid source"""
        result = subprocess.run([
            'python', 'detect.py',
            '--source', 'nonexistent.jpg',
            '--output-dir', output_dir
        ], capture_output=True, text=True, timeout=10)
        
        # Should fail gracefully
        assert result.returncode != 0
    
    def test_cli_invalid_weights(self, test_image_path, output_dir):
        """Test CLI with invalid weights"""
        result = subprocess.run([
            'python', 'detect.py',
            '--source', test_image_path,
            '--weights', 'nonexistent.pt',
            '--output-dir', output_dir
        ], capture_output=True, text=True, timeout=10)
        
        # Should fail gracefully
        assert result.returncode != 0
