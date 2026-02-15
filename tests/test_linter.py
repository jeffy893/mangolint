"""
Unit tests for BedrockLinter class
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from linter import BedrockLinter


class TestBedrockLinter(unittest.TestCase):
    """Test cases for BedrockLinter"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.linter = BedrockLinter(region_name='us-east-1')
    
    def test_initialization(self):
        """Test linter initialization"""
        self.assertEqual(self.linter.region_name, 'us-east-1')
        self.assertEqual(self.linter.model_id, 'anthropic.claude-3-sonnet-20240229-v1:0')
        self.assertIsNotNone(self.linter.bedrock_runtime)
    
    def test_construct_prompt(self):
        """Test prompt construction"""
        text = "mango"
        prompt = self.linter._construct_prompt(text)
        
        self.assertIn("Indigenous Linguist and Brand Anthropologist", prompt)
        self.assertIn("mango", prompt)
        self.assertIn("indigenous_synonyms", prompt)
        self.assertIn("ripeness", prompt)
    
    def test_empty_text_handling(self):
        """Test handling of empty text"""
        result = self.linter.analyze_text("")
        self.assertEqual(result, [])
        
        result = self.linter.analyze_text("   ")
        self.assertEqual(result, [])
    
    @patch('linter.boto3.client')
    def test_analyze_text_with_mock(self, mock_boto_client):
        """Test analyze_text with mocked Bedrock response"""
        # Mock the Bedrock response
        mock_response = {
            'body': MagicMock()
        }
        
        mock_entity = {
            "text": "mango",
            "type": "cultural",
            "category": "fruit",
            "description": "Tropical stone fruit",
            "indigenous_synonyms": [
                {
                    "term": "Aam",
                    "language": "Hindi",
                    "culture": "North Indian",
                    "definition": "Sacred fruit",
                    "context": "Ripeness stages: kairi (raw), aam (ripe)"
                }
            ],
            "brand_insights": "Specify ripeness stage",
            "traditional_uses": "Culinary, medicinal",
            "authenticity_markers": ["Specify variety"]
        }
        
        mock_response['body'].read.return_value = json.dumps({
            'content': [{'text': json.dumps([mock_entity])}]
        }).encode('utf-8')
        
        mock_client = MagicMock()
        mock_client.invoke_model.return_value = mock_response
        mock_boto_client.return_value = mock_client
        
        # Create new linter with mocked client
        linter = BedrockLinter()
        linter.bedrock_runtime = mock_client
        
        result = linter.analyze_text("mango")
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['text'], 'mango')
        self.assertEqual(result[0]['category'], 'fruit')
        self.assertIn('indigenous_synonyms', result[0])
    
    def test_get_model_info(self):
        """Test model info retrieval"""
        info = self.linter.get_model_info()
        
        self.assertIn('model_id', info)
        self.assertIn('region', info)
        self.assertIn('service', info)
        self.assertEqual(info['service'], 'Amazon Bedrock')


if __name__ == '__main__':
    unittest.main()
