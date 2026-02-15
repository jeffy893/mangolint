"""
Integration tests for Flask application
"""
import unittest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


class TestFlaskApp(unittest.TestCase):
    """Test cases for Flask application endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_index_route(self):
        """Test main index route"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Mangolint', response.data)
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'mangolint')
    
    def test_model_info_endpoint(self):
        """Test model info endpoint"""
        response = self.client.get('/model-info')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('model_id', data)
        self.assertIn('region', data)
    
    def test_lint_endpoint_empty_text(self):
        """Test lint endpoint with empty text"""
        response = self.client.post('/lint',
                                   data=json.dumps({'text': ''}),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 0)
    
    def test_lint_endpoint_short_text(self):
        """Test lint endpoint with short text (< 3 chars)"""
        response = self.client.post('/lint',
                                   data=json.dumps({'text': 'ab'}),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 0)
    
    def test_analyze_endpoint_no_text(self):
        """Test analyze endpoint without text"""
        response = self.client.post('/analyze',
                                   data=json.dumps({}),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_lint_endpoint_invalid_json(self):
        """Test lint endpoint with invalid JSON"""
        response = self.client.post('/lint',
                                   data='invalid json',
                                   content_type='application/json')
        # Flask returns 500 for JSON decode errors, which is acceptable
        self.assertIn(response.status_code, [400, 500])


if __name__ == '__main__':
    unittest.main()
