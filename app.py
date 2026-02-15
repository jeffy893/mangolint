from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Try to initialize real Bedrock linter, fall back to mock if credentials fail
bedrock_region = os.getenv('BEDROCK_REGION') or os.getenv('AWS_REGION', 'us-east-1')
use_mock = os.getenv('USE_MOCK_LINTER', 'false').lower() == 'true'

if use_mock:
    from linter_mock import MockBedrockLinter
    linter = MockBedrockLinter(region_name=bedrock_region)
    print("🎭 Using Mock Linter (Demo Mode)")
else:
    try:
        from linter import BedrockLinter
        linter = BedrockLinter(region_name=bedrock_region)
        print("✅ Using Real Bedrock Linter")
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
        
        # Analyze the text using Bedrock
        entities = linter.analyze_text(text)
        
        return jsonify({
            'success': True,
            'entities': entities,
            'count': len(entities)
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
        
        # Analyze the text
        try:
            entities = linter.analyze_text(text)
        except Exception as bedrock_error:
            print(f"Bedrock error: {bedrock_error}")
            # Return empty result on error instead of failing
            return jsonify({
                'success': True,
                'entities': [],
                'count': 0,
                'error': 'Analysis temporarily unavailable'
            })
        
        return jsonify({
            'success': True,
            'entities': entities,
            'count': len(entities)
        })
        
    except Exception as e:
        print(f"Error in /lint endpoint: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'entities': []
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
