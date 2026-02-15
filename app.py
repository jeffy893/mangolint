from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import hashlib
from functools import lru_cache

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Simple in-memory cache for analysis results
analysis_cache = {}
MAX_CACHE_SIZE = 100

def get_cache_key(text):
    """Generate a cache key from text"""
    return hashlib.md5(text.strip().lower().encode()).hexdigest()

def get_cached_analysis(text):
    """Get cached analysis result if available"""
    cache_key = get_cache_key(text)
    return analysis_cache.get(cache_key)

def cache_analysis(text, result):
    """Cache analysis result"""
    cache_key = get_cache_key(text)
    
    # Simple cache size management
    if len(analysis_cache) >= MAX_CACHE_SIZE:
        # Remove oldest entry (first key)
        first_key = next(iter(analysis_cache))
        del analysis_cache[first_key]
    
    analysis_cache[cache_key] = result

# Try to initialize real Bedrock linter, fall back to mock if credentials fail
bedrock_region = os.getenv('BEDROCK_REGION') or os.getenv('AWS_REGION', 'us-east-1')
aws_profile = os.getenv('AWS_PROFILE')  # Optional: specify AWS profile from ~/.aws/credentials
use_mock = os.getenv('USE_MOCK_LINTER', 'false').lower() == 'true'

if use_mock:
    from linter_mock import MockBedrockLinter
    linter = MockBedrockLinter(region_name=bedrock_region)
    print("🎭 Using Mock Linter (Demo Mode)")
else:
    try:
        from linter import BedrockLinter
        linter = BedrockLinter(region_name=bedrock_region, profile_name=aws_profile)
        print(f"✅ Using Real Bedrock Linter (Region: {bedrock_region}, Profile: {aws_profile or 'default'})")
    except Exception as e:
        print(f"⚠️  Bedrock initialization failed: {e}")
        print("🎭 Falling back to Mock Linter (Demo Mode)")
        from linter_mock import MockBedrockLinter
        linter = MockBedrockLinter(region_name=bedrock_region)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Endpoint to analyze text for natural ingredients and indigenous synonyms.
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Check cache first
        cached_result = get_cached_analysis(text)
        if cached_result is not None:
            return jsonify({
                'success': True,
                'entities': cached_result,
                'count': len(cached_result),
                'cached': True
            })
        
        # Analyze the text using Bedrock
        entities = linter.analyze_text(text)
        
        # Cache the result
        cache_analysis(text, entities)
        
        return jsonify({
            'success': True,
            'entities': entities,
            'count': len(entities),
            'cached': False
        })
        
    except Exception as e:
        print(f"Error in /analyze endpoint: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/lint', methods=['POST'])
def lint():
    """
    Real-time linting endpoint for debounced keyup events.
    Lightweight version of /analyze for real-time feedback.
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text or len(text.strip()) < 3:
            return jsonify({
                'success': True,
                'entities': [],
                'count': 0
            })
        
        # Check cache first
        cached_result = get_cached_analysis(text)
        if cached_result is not None:
            return jsonify({
                'success': True,
                'entities': cached_result,
                'count': len(cached_result),
                'cached': True
            })
        
        # Analyze the text
        try:
            entities = linter.analyze_text(text)
            
            # Cache the result
            cache_analysis(text, entities)
            
            return jsonify({
                'success': True,
                'entities': entities,
                'count': len(entities),
                'cached': False
            })
        except Exception as bedrock_error:
            print(f"Bedrock error: {bedrock_error}")
            # Return empty result on error instead of failing
            return jsonify({
                'success': True,
                'entities': [],
                'count': 0,
                'error': 'Analysis temporarily unavailable'
            })
        
    except Exception as e:
        print(f"Error in /lint endpoint: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'entities': []
        }), 500

@app.route('/generate-brand-statement', methods=['POST'])
def generate_brand_statement():
    """
    Generate an enhanced brand statement using indigenous terms.
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        entities = data.get('entities', [])
        
        if not text or not entities:
            return jsonify({'error': 'Text and entities required'}), 400
        
        # Check cache first
        cache_key = get_cache_key(f"brand_statement_{text}")
        cached_result = analysis_cache.get(cache_key)
        if cached_result is not None:
            return jsonify({
                'success': True,
                'brand_statement': cached_result,
                'cached': True
            })
        
        # Generate brand statement using Bedrock
        try:
            brand_statement = linter.generate_brand_statement(text, entities)
            
            # Cache the result
            analysis_cache[cache_key] = brand_statement
            
            return jsonify({
                'success': True,
                'brand_statement': brand_statement,
                'cached': False
            })
        except Exception as bedrock_error:
            print(f"Bedrock error generating brand statement: {bedrock_error}")
            return jsonify({
                'success': False,
                'error': 'Brand statement generation temporarily unavailable'
            }), 500
        
    except Exception as e:
        print(f"Error in /generate-brand-statement endpoint: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/model-info', methods=['GET'])
def model_info():
    """
    Endpoint to get information about the current model configuration.
    """
    try:
        info = linter.get_model_info()
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint for monitoring and load balancers.
    """
    return jsonify({
        'status': 'healthy',
        'service': 'mangolint',
        'version': '1.0.0'
    }), 200

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    app.run(debug=debug, host=host, port=port)
