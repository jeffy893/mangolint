# Mangolint

A cultural linguistics linter powered by an Indigenous Linguist and Brand Anthropologist AI persona. Uses Amazon Bedrock's Claude 3 to identify natural ingredients in text and provide indigenous synonyms with rich cultural context, ripeness stages, and brand authenticity insights.

## Persona

The AI operates as an **Indigenous Linguist and Brand Anthropologist** with expertise in:
- Traditional ecological knowledge across global indigenous cultures
- Ethnobotany and cultural food systems
- Linguistic anthropology and semantic evolution
- Brand storytelling through cultural authenticity

## Features

- Modern, clean web interface with premium text editor
- Real-time text analysis using Claude 3 via Amazon Bedrock
- Identifies natural ingredients (fruits, herbs, spices, plants, minerals, materials)
- Provides indigenous synonyms from diverse cultures with language attribution
- Contextual nuances: ripeness stages, preparation methods, seasonal variations
- Brand insights for authentic marketing and storytelling
- Traditional uses (culinary, medicinal, ceremonial)
- Authenticity markers for cultural validation

## Example Output

**Input:** "mango"

**Output JSON:**
```json
{
  "text": "mango",
  "type": "cultural",
  "category": "fruit",
  "description": "Tropical stone fruit with deep cultural significance across South Asia, Latin America, and Africa.",
  "indigenous_synonyms": [
    {
      "term": "Manga",
      "language": "Portuguese",
      "culture": "Brazilian/Portuguese",
      "definition": "Derived from Malayalam 'māṅṅa'. Used in Brazilian cuisine for both ripe and green preparations.",
      "context": "Ripeness matters: 'manga verde' (green mango) for pickles, 'manga madura' (ripe mango) for desserts"
    },
    {
      "term": "Aam",
      "language": "Hindi/Urdu",
      "culture": "North Indian/Pakistani",
      "definition": "Sacred fruit in Hindu tradition. Over 1000 varieties cultivated.",
      "context": "Ripeness stages: 'kairi' (raw/green), 'aam' (ripe). Raw used for 'aam panna', ripe for 'aam ras'"
    },
    {
      "term": "Māṅgāy/Māmpalam",
      "language": "Tamil",
      "culture": "South Indian/Tamil",
      "definition": "Etymology root of English 'mango'. Integral to Tamil cuisine and Ayurvedic medicine.",
      "context": "Green mango for pickles and chutneys, ripe for fresh eating. Leaves used in ceremonies"
    }
  ],
  "brand_insights": "Authenticity opportunity: Specify ripeness stage and cultural preparation method.",
  "traditional_uses": "Culinary (fresh, dried, pickled), medicinal (digestive aid), ceremonial (leaves in rituals)",
  "authenticity_markers": [
    "Specify variety (Alphonso, Ataulfo, Tommy Atkins)",
    "Indicate ripeness stage",
    "Reference traditional preparation methods"
  ]
}
```

## Setup

1. Run the setup script to create a virtual environment and install dependencies:
```bash
./setup.sh
```

2. Copy `.env.example` to `.env` and configure your AWS credentials:
```bash
cp .env.example .env
```

3. Edit `.env` with your AWS credentials:
```env
AWS_ACCESS_KEY_ID=your_aws_access_key_id_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key_here
BEDROCK_REGION=us-east-1
SECRET_KEY=your-secret-key-here-change-in-production
```

## Running the Application

1. Activate the virtual environment:
```bash
source venv/bin/activate
```

2. Run the Flask application:
```bash
python app.py
```

3. Open your browser to `http://localhost:5000`

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions for:
- Heroku
- AWS Elastic Beanstalk
- Docker
- Production configuration and best practices

## Usage

1. Type or paste text into the editor
2. Real-time linting activates automatically (500ms debounce after typing)
3. Natural ingredients are underlined with colored highlights
4. Click underlined words to jump to their details in the sidebar
5. View indigenous synonyms, cultural context, and brand insights
6. Use "Analyze Text" button for immediate analysis

### Real-time Features

- Debounced keyup detection (500ms) for smooth performance
- Visual overlay with underlined suggestions
- Color-coded highlights by entity type
- Click-to-scroll interaction between editor and sidebar
- Character and word count tracking

## Requirements

- Python 3.10+
- AWS Account with Bedrock access
- Claude 3 model access in Amazon Bedrock

## Testing

Run the comprehensive test suite:
```bash
source venv/bin/activate
python3.10 run_tests.py
```

This generates a detailed test report covering:
- Unit tests for BedrockLinter
- Integration tests for Flask endpoints
- Error handling and edge cases

See [TESTING.md](TESTING.md) for detailed testing guide and [example_usages.txt](example_usages.txt) for 20 ready-to-use examples.

## Project Structure

```
mangolint/
├── app.py                 # Flask application
├── linter.py             # BedrockLinter class
├── requirements.txt      # Python dependencies
├── setup.sh             # Setup script
├── .env.example         # Environment variables template
├── static/
│   ├── css/
│   │   └── style.css    # Styles
│   └── js/
│       └── main.js      # Frontend logic
└── templates/
    └── index.html       # Main interface
```

## API Endpoints

- `GET /` - Main interface
- `POST /analyze` - Full analysis (triggered by "Analyze Text" button)
- `POST /lint` - Real-time linting (debounced keyup events)
- `GET /model-info` - Get model configuration info

### /lint Endpoint

Real-time endpoint optimized for debounced keyup events:

**Request:**
```json
{
  "text": "Our product uses mango and turmeric"
}
```

**Response:**
```json
{
  "success": true,
  "entities": [...],
  "count": 2
}
```

## License

MIT
