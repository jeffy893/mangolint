import boto3
import json
import os
from typing import List, Dict, Any


class BedrockLinter:
    """
    A linter that uses Amazon Bedrock's Claude 3 model to identify natural ingredients
    and suggest indigenous synonyms with cultural context.
    """
    
    def __init__(self, region_name: str = 'us-east-1', profile_name: str = None):
        """
        Initialize the Bedrock client.
        Uses AWS credentials from ~/.aws/credentials
        
        Args:
            region_name: AWS region for Bedrock service (default: us-east-1)
            profile_name: AWS profile name from ~/.aws/credentials (default: None uses default profile)
        """
        self.region_name = region_name
        self.profile_name = profile_name
        
        # Create session with profile if specified
        if profile_name:
            session = boto3.Session(profile_name=profile_name)
            self.bedrock_runtime = session.client(
                service_name='bedrock-runtime',
                region_name=region_name
            )
        else:
            # boto3 will automatically use credentials from ~/.aws/credentials (default profile)
            self.bedrock_runtime = boto3.client(
                service_name='bedrock-runtime',
                region_name=region_name
            )
        
        self.model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
    
    def _construct_prompt(self, text: str) -> str:
        """
        Construct a prompt for Claude 3 to analyze text for natural ingredients
        and provide indigenous synonyms with cultural context.
        
        Args:
            text: The text to analyze
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""You are an Indigenous Linguist and Brand Anthropologist with deep expertise in:
- Traditional ecological knowledge across global indigenous cultures
- Ethnobotany and cultural food systems
- Linguistic anthropology and semantic evolution of ingredient names
- Brand storytelling through cultural authenticity

Your role is to analyze text and identify natural ingredients (fruits, vegetables, herbs, spices, plants, minerals, natural materials), then provide rich cultural-linguistic context.

ANALYSIS FRAMEWORK:

For each natural ingredient identified:
1. Extract the exact word/phrase from the input text
2. Provide indigenous/traditional synonyms from diverse cultures (Native American, African, Asian, Latin American, Pacific Islander, Middle Eastern, etc.)
3. Include contextual nuances: ripeness stages, preparation methods, seasonal variations, medicinal vs culinary uses
4. Explain cultural significance, traditional uses, and brand storytelling potential
5. Categorize by type and provide authenticity markers

EXAMPLE OUTPUT LOGIC:
Input: "mango"
Output:
{{
  "text": "mango",
  "type": "cultural",
  "category": "fruit",
  "description": "Tropical stone fruit with deep cultural significance across South Asia, Latin America, and Africa. Known as 'king of fruits' in many cultures.",
  "indigenous_synonyms": [
    {{
      "term": "Manga",
      "language": "Portuguese",
      "culture": "Brazilian/Portuguese",
      "definition": "Derived from Malayalam 'māṅṅa'. Used in Brazilian cuisine for both ripe (sweet) and green (savory) preparations.",
      "context": "Ripeness matters: 'manga verde' (green mango) for pickles, 'manga madura' (ripe mango) for desserts"
    }},
    {{
      "term": "Aam",
      "language": "Hindi/Urdu",
      "culture": "North Indian/Pakistani",
      "definition": "Sacred fruit in Hindu tradition. Over 1000 varieties cultivated. 'Aam ka mausam' (mango season) is culturally significant.",
      "context": "Ripeness stages: 'kairi' (raw/green), 'aam' (ripe). Raw used for 'aam panna' (summer drink), ripe for 'aam ras' (mango pulp)"
    }},
    {{
      "term": "Māṅgāy/Māmpalam",
      "language": "Tamil",
      "culture": "South Indian/Tamil",
      "definition": "Etymology root of English 'mango'. Integral to Tamil cuisine and Ayurvedic medicine.",
      "context": "Green mango ('māṅgāy') for pickles and chutneys, ripe ('palam') for fresh eating. Leaves used in religious ceremonies"
    }},
    {{
      "term": "Mangga",
      "language": "Tagalog/Malay",
      "culture": "Filipino/Southeast Asian",
      "definition": "National fruit of Philippines. Green mango with bagoong (fermented shrimp paste) is iconic street food.",
      "context": "Preference for semi-ripe to green mangoes in Filipino cuisine, contrasting with Western preference for fully ripe"
    }}
  ],
  "brand_insights": "Authenticity opportunity: Specify ripeness stage and cultural preparation method. 'Aam' signals premium Indian heritage. 'Manga verde' appeals to Latin American markets.",
  "traditional_uses": "Culinary (fresh, dried, pickled), medicinal (digestive aid, vitamin C source), ceremonial (leaves in Hindu/Buddhist rituals)",
  "authenticity_markers": ["Specify variety (Alphonso, Ataulfo, Tommy Atkins)", "Indicate ripeness stage", "Reference traditional preparation methods"]
}}

OUTPUT FORMAT:
Return a JSON array of detected ingredients. Each ingredient must follow this structure:
[
  {{
    "text": "exact word from input text",
    "type": "cultural",
    "category": "fruit/vegetable/herb/spice/plant/mineral/material/grain/legume/nut/seed",
    "description": "comprehensive explanation of ingredient and cultural significance",
    "indigenous_synonyms": [
      {{
        "term": "indigenous/traditional term",
        "language": "specific language name",
        "culture": "cultural/regional context",
        "definition": "meaning, etymology, and traditional knowledge",
        "context": "ripeness stages, preparation methods, seasonal/medicinal/culinary distinctions"
      }}
    ],
    "brand_insights": "how brands can leverage cultural authenticity",
    "traditional_uses": "culinary, medicinal, ceremonial, or other traditional applications",
    "authenticity_markers": ["specific markers that signal cultural authenticity"]
  }}
]

IMPORTANT RULES:
- Return ONLY valid JSON, no markdown, no explanations, no additional text
- If no natural ingredients found, return empty array: []
- Provide at least 3-5 indigenous synonyms per ingredient when possible
- Always include ripeness/preparation context where relevant
- Focus on cultural authenticity and brand storytelling potential

TEXT TO ANALYZE:
{text}"""
        
        return prompt
    
    def analyze_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Analyze text using Claude 3 to identify natural ingredients and suggest
        indigenous synonyms with definitions.
        
        Args:
            text: The text to analyze
            
        Returns:
            List of dictionaries containing detected entities with indigenous synonyms
        """
        if not text or not text.strip():
            return []
        
        try:
            prompt = self._construct_prompt(text)
            
            # Prepare the request body for Claude 3
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4096,
                "temperature": 0.3,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            # Invoke the model
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            # Parse the response
            response_body = json.loads(response['body'].read())
            
            # Extract the text content from Claude's response
            content = response_body.get('content', [])
            if content and len(content) > 0:
                response_text = content[0].get('text', '[]')
            else:
                response_text = '[]'
            
            # Parse the JSON response from Claude
            entities = json.loads(response_text)
            
            # Format entities for frontend
            formatted_entities = []
            for entity in entities:
                formatted_entity = {
                    'text': entity.get('text', ''),
                    'type': entity.get('type', 'cultural'),
                    'category': entity.get('category', ''),
                    'description': entity.get('description', ''),
                    'indigenous_synonyms': entity.get('indigenous_synonyms', []),
                    'brand_insights': entity.get('brand_insights', ''),
                    'traditional_uses': entity.get('traditional_uses', ''),
                    'authenticity_markers': entity.get('authenticity_markers', [])
                }
                formatted_entities.append(formatted_entity)
            
            return formatted_entities
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return []
        except Exception as e:
            print(f"Error analyzing text with Bedrock: {e}")
            raise
    
    def get_model_info(self) -> Dict[str, str]:
        """
        Get information about the current model configuration.
        
        Returns:
            Dictionary with model information
        """
        return {
            'model_id': self.model_id,
            'region': self.region_name,
            'service': 'Amazon Bedrock'
        }
    
    def generate_brand_statement(self, original_text: str, entities: List[Dict[str, Any]]) -> str:
        """
        Generate an enhanced brand statement that integrates indigenous terms.
        
        Args:
            original_text: The original product description
            entities: List of detected entities with indigenous synonyms
            
        Returns:
            Enhanced brand statement as a string
        """
        if not entities:
            return original_text
        
        # Build context about the entities
        entity_context = []
        for entity in entities:
            synonyms = entity.get('indigenous_synonyms', [])
            if synonyms:
                # Get the first synonym as the primary one to use
                primary_synonym = synonyms[0]
                entity_context.append({
                    'original': entity.get('text', ''),
                    'indigenous_term': primary_synonym.get('term', ''),
                    'language': primary_synonym.get('language', ''),
                    'culture': primary_synonym.get('culture', ''),
                    'context': primary_synonym.get('context', '')
                })
        
        # Construct prompt for brand statement generation
        prompt = f"""You are a creative brand copywriter specializing in culturally authentic product descriptions.

TASK: Rewrite the following product description to be more expressive and culturally rich by integrating indigenous/traditional terms where appropriate.

ORIGINAL TEXT:
{original_text}

INDIGENOUS TERMS TO INTEGRATE:
{json.dumps(entity_context, indent=2)}

GUIDELINES:
1. Maintain the core message and intent of the original text
2. Naturally integrate indigenous terms where they add authenticity and cultural depth
3. Include the indigenous term in italics followed by the English term in parentheses when first introduced
4. Make the description more evocative and expressive
5. Keep it concise and brand-appropriate (2-4 sentences)
6. Emphasize cultural heritage and authenticity
7. Make it sound premium and appealing

EXAMPLE:
Original: "Our pizza uses fresh mushrooms, peppers, and onions"
Enhanced: "Our artisan pizza celebrates the earth's bounty with fresh hongos (mushrooms), vibrant chiles (peppers), and aromatic cebollas (onions) - a harmonious blend of traditional ingredients crafted with cultural reverence."

Return ONLY the enhanced brand statement text, no explanations or additional commentary."""

        try:
            # Prepare the request body for Claude 3
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 500,
                "temperature": 0.7,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            # Invoke the model
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            # Parse the response
            response_body = json.loads(response['body'].read())
            
            # Extract the text content from Claude's response
            content = response_body.get('content', [])
            if content and len(content) > 0:
                brand_statement = content[0].get('text', original_text)
            else:
                brand_statement = original_text
            
            return brand_statement.strip()
            
        except Exception as e:
            print(f"Error generating brand statement: {e}")
            return original_text
