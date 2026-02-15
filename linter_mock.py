"""
Mock Linter for Demo/Testing without AWS Bedrock
"""
import json
from typing import List, Dict, Any


class MockBedrockLinter:
    """
    Mock linter that returns predefined responses for demo purposes.
    Use this when AWS Bedrock credentials are not available.
    """
    
    def __init__(self, region_name: str = 'us-east-1'):
        self.region_name = region_name
        self.model_id = 'anthropic.claude-3-sonnet-20240229-v1:0 (MOCK)'
        
        # Predefined responses for common ingredients
        self.mock_responses = {
            'mango': self._get_mango_response(),
            'turmeric': self._get_turmeric_response(),
            'coconut': self._get_coconut_response(),
            'ginger': self._get_ginger_response(),
            'cardamom': self._get_cardamom_response(),
            'vanilla': self._get_vanilla_response(),
            'corn': self._get_corn_response(),
            'cinnamon': self._get_cinnamon_response(),
            'pepper': self._get_pepper_response(),
            'honey': self._get_honey_response(),
        }
    
    def _get_mango_response(self):
        return {
            "text": "mango",
            "type": "cultural",
            "category": "fruit",
            "description": "Tropical stone fruit with deep cultural significance across South Asia, Latin America, and Africa. Known as 'king of fruits' in many cultures.",
            "indigenous_synonyms": [
                {
                    "term": "Manga",
                    "language": "Portuguese",
                    "culture": "Brazilian/Portuguese",
                    "definition": "Derived from Malayalam 'māṅṅa'. Used in Brazilian cuisine for both ripe (sweet) and green (savory) preparations.",
                    "context": "Ripeness matters: 'manga verde' (green mango) for pickles and savory dishes, 'manga madura' (ripe mango) for desserts and fresh eating"
                },
                {
                    "term": "Aam",
                    "language": "Hindi/Urdu",
                    "culture": "North Indian/Pakistani",
                    "definition": "Sacred fruit in Hindu tradition. Over 1000 varieties cultivated. 'Aam ka mausam' (mango season) is culturally significant.",
                    "context": "Ripeness stages: 'kairi' (raw/green) used for 'aam panna' (summer cooling drink), 'aam' (ripe) for 'aam ras' (mango pulp dessert)"
                },
                {
                    "term": "Māṅgāy/Māmpalam",
                    "language": "Tamil",
                    "culture": "South Indian/Tamil",
                    "definition": "Etymology root of English 'mango'. Integral to Tamil cuisine and Ayurvedic medicine.",
                    "context": "Green mango ('māṅgāy') for pickles and chutneys, ripe ('palam') for fresh eating. Leaves used in religious ceremonies"
                },
                {
                    "term": "Mangga",
                    "language": "Tagalog/Malay",
                    "culture": "Filipino/Southeast Asian",
                    "definition": "National fruit of Philippines. Green mango with bagoong (fermented shrimp paste) is iconic street food.",
                    "context": "Preference for semi-ripe to green mangoes in Filipino cuisine, contrasting with Western preference for fully ripe"
                }
            ],
            "brand_insights": "Authenticity opportunity: Specify ripeness stage and cultural preparation method. 'Aam' signals premium Indian heritage. 'Manga verde' appeals to Latin American markets.",
            "traditional_uses": "Culinary (fresh, dried, pickled), medicinal (digestive aid, vitamin C source), ceremonial (leaves in Hindu/Buddhist rituals)",
            "authenticity_markers": ["Specify variety (Alphonso, Ataulfo, Tommy Atkins)", "Indicate ripeness stage", "Reference traditional preparation methods"]
        }
    
    def _get_turmeric_response(self):
        return {
            "text": "turmeric",
            "type": "cultural",
            "category": "spice",
            "description": "Golden spice central to South Asian cuisine and Ayurvedic medicine. Sacred in Hindu ceremonies.",
            "indigenous_synonyms": [
                {
                    "term": "Haldi",
                    "language": "Hindi/Urdu",
                    "culture": "North Indian",
                    "definition": "Essential in Hindu wedding ceremonies. Applied to bride and groom for purification and blessing.",
                    "context": "Fresh rhizome vs dried powder. 'Haldi ki rasam' (turmeric ceremony) is pre-wedding ritual"
                },
                {
                    "term": "Manjal",
                    "language": "Tamil",
                    "culture": "South Indian",
                    "definition": "Used in traditional medicine and religious offerings. Symbol of prosperity and fertility.",
                    "context": "Fresh turmeric ('manjal kizhangu') for medicinal use, dried for cooking"
                },
                {
                    "term": "Pasupu",
                    "language": "Telugu",
                    "culture": "Andhra Pradesh/Telangana",
                    "definition": "Sacred spice in Telugu culture. Essential in 'pasupu kumkuma' ceremony for married women.",
                    "context": "Ceremonial vs culinary use. Fresh paste for skin application, powder for cooking"
                }
            ],
            "brand_insights": "Highlight Ayurvedic heritage and ceremonial significance. Specify curcumin content for wellness products.",
            "traditional_uses": "Culinary (curry base, golden milk), medicinal (anti-inflammatory, wound healing), ceremonial (Hindu weddings, religious offerings)",
            "authenticity_markers": ["Specify origin (Alleppey vs Madras grade)", "Mention curcumin content", "Reference traditional preparation"]
        }
    
    def _get_coconut_response(self):
        return {
            "text": "coconut",
            "type": "cultural",
            "category": "fruit",
            "description": "Versatile tropical fruit called 'tree of life' in many cultures. Every part has traditional uses.",
            "indigenous_synonyms": [
                {
                    "term": "Nariyal",
                    "language": "Hindi",
                    "culture": "North Indian",
                    "definition": "Sacred offering in Hindu temples. Breaking coconut symbolizes ego destruction.",
                    "context": "Young coconut ('daab') for water, mature for copra and oil"
                },
                {
                    "term": "Thengai",
                    "language": "Tamil",
                    "culture": "South Indian",
                    "definition": "Essential in South Indian cuisine and religious rituals. Symbol of prosperity.",
                    "context": "Fresh grated for chutneys, dried for oil extraction, tender for water"
                },
                {
                    "term": "Kelapa",
                    "language": "Malay/Indonesian",
                    "culture": "Southeast Asian",
                    "definition": "Staple in Southeast Asian cooking. Used in both sweet and savory dishes.",
                    "context": "Young ('kelapa muda') for refreshing drink, mature for santan (coconut milk)"
                }
            ],
            "brand_insights": "Specify maturity stage (young vs mature) and part used (water, milk, oil, meat). Highlight traditional extraction methods.",
            "traditional_uses": "Culinary (milk, oil, water), medicinal (hydration, skin care), ceremonial (Hindu offerings, island traditions)",
            "authenticity_markers": ["Specify coconut stage (young/tender vs mature)", "Mention extraction method", "Reference traditional uses"]
        }
    
    def _get_ginger_response(self):
        return {
            "text": "ginger",
            "type": "cultural",
            "category": "spice",
            "description": "Pungent rhizome used globally in cuisine and traditional medicine. Ancient trade spice.",
            "indigenous_synonyms": [
                {
                    "term": "Adrak",
                    "language": "Hindi",
                    "culture": "North Indian",
                    "definition": "Essential in chai (tea) and Ayurvedic remedies. Warming spice for digestion.",
                    "context": "Fresh ('adrak') vs dried ('saunth'). Fresh for cooking, dried for medicine"
                },
                {
                    "term": "Inji",
                    "language": "Tamil",
                    "culture": "South Indian",
                    "definition": "Used in traditional medicine and cuisine. Key ingredient in rasam and chutneys.",
                    "context": "Young ginger tender and mild, mature ginger more pungent"
                },
                {
                    "term": "Shoga",
                    "language": "Japanese",
                    "culture": "Japanese",
                    "definition": "Essential in Japanese cuisine. Pickled ginger ('gari') served with sushi.",
                    "context": "Young ginger for pickling, mature for grating and cooking"
                }
            ],
            "brand_insights": "Specify fresh vs dried. Highlight warming properties and digestive benefits in Ayurvedic tradition.",
            "traditional_uses": "Culinary (spice, tea), medicinal (nausea relief, anti-inflammatory), ceremonial (Chinese New Year)",
            "authenticity_markers": ["Specify fresh vs dried", "Mention origin", "Reference traditional preparation"]
        }
    
    def _get_cardamom_response(self):
        return {
            "text": "cardamom",
            "type": "cultural",
            "category": "spice",
            "description": "Queen of spices. Aromatic pods used in sweet and savory dishes across cultures.",
            "indigenous_synonyms": [
                {
                    "term": "Elaichi",
                    "language": "Hindi",
                    "culture": "North Indian",
                    "definition": "Essential in chai, biryani, and desserts. Symbol of hospitality.",
                    "context": "Green cardamom for sweet dishes, black cardamom for savory"
                },
                {
                    "term": "Elakkai",
                    "language": "Tamil",
                    "culture": "South Indian",
                    "definition": "Used in filter coffee and traditional sweets. Breath freshener after meals.",
                    "context": "Whole pods vs ground. Pods for infusion, ground for baking"
                },
                {
                    "term": "Hel",
                    "language": "Arabic",
                    "culture": "Middle Eastern",
                    "definition": "Essential in Arabic coffee ('qahwa'). Symbol of hospitality and welcome.",
                    "context": "Lightly crushed pods for coffee, ground for spice blends"
                }
            ],
            "brand_insights": "Specify green vs black cardamom. Highlight origin (Kerala, Guatemala). Premium spice positioning.",
            "traditional_uses": "Culinary (chai, coffee, desserts), medicinal (digestive aid, breath freshener), ceremonial (hospitality rituals)",
            "authenticity_markers": ["Specify variety (green vs black)", "Mention origin", "Reference traditional use"]
        }
    
    def _get_vanilla_response(self):
        return {
            "text": "vanilla",
            "type": "cultural",
            "category": "spice",
            "description": "Labor-intensive orchid bean. Second most expensive spice after saffron.",
            "indigenous_synonyms": [
                {
                    "term": "Tlilxochitl",
                    "language": "Nahuatl",
                    "culture": "Aztec/Mexican",
                    "definition": "Means 'black flower'. Used by Aztecs to flavor chocolate drinks for royalty.",
                    "context": "Whole beans vs extract. Traditional curing process takes months"
                },
                {
                    "term": "Vainilla",
                    "language": "Spanish",
                    "culture": "Latin American",
                    "definition": "Diminutive of 'vaina' (sheath). Introduced to Europe by Spanish conquistadors.",
                    "context": "Mexican vs Tahitian vs Madagascar varieties have distinct flavor profiles"
                }
            ],
            "brand_insights": "Specify origin and variety. Highlight hand-pollination and curing process. Premium positioning.",
            "traditional_uses": "Culinary (desserts, beverages), medicinal (calming properties), ceremonial (Aztec chocolate rituals)",
            "authenticity_markers": ["Specify origin (Madagascar, Tahiti, Mexico)", "Mention curing process", "Whole bean vs extract"]
        }
    
    def _get_corn_response(self):
        return {
            "text": "corn",
            "type": "cultural",
            "category": "grain",
            "description": "Sacred crop in Mesoamerican cultures. Staple food for thousands of years.",
            "indigenous_synonyms": [
                {
                    "term": "Maíz",
                    "language": "Spanish",
                    "culture": "Latin American",
                    "definition": "From Taíno 'mahiz'. Central to Latin American cuisine and culture.",
                    "context": "Fresh ('elote'), dried ('maíz'), ground ('masa')"
                },
                {
                    "term": "Elote",
                    "language": "Nahuatl",
                    "culture": "Mexican/Aztec",
                    "definition": "Fresh corn on the cob. Street food tradition in Mexico.",
                    "context": "Grilled with lime, chili, and cheese. Seasonal delicacy"
                },
                {
                    "term": "Choclo",
                    "language": "Quechua",
                    "culture": "Andean",
                    "definition": "Large-kernel Andean corn. Sacred in Inca culture.",
                    "context": "Boiled or roasted. Larger kernels than common corn"
                }
            ],
            "brand_insights": "Highlight indigenous heritage and sacred significance. Specify variety and preparation method.",
            "traditional_uses": "Culinary (tortillas, tamales, polenta), ceremonial (Mayan/Aztec rituals), cultural (origin stories)",
            "authenticity_markers": ["Specify variety", "Mention nixtamalization process", "Reference cultural significance"]
        }
    
    def _get_cinnamon_response(self):
        return {
            "text": "cinnamon",
            "type": "cultural",
            "category": "spice",
            "description": "Ancient spice from tree bark. Prized in trade routes for millennia.",
            "indigenous_synonyms": [
                {
                    "term": "Dalchini",
                    "language": "Hindi",
                    "culture": "Indian",
                    "definition": "Warming spice in Ayurveda. Used in garam masala and chai.",
                    "context": "Ceylon vs Cassia varieties. Ceylon is 'true cinnamon'"
                },
                {
                    "term": "Kurundu",
                    "language": "Sinhalese",
                    "culture": "Sri Lankan",
                    "definition": "Ceylon cinnamon native to Sri Lanka. Prized for delicate flavor.",
                    "context": "Hand-rolled quills vs ground. Premium quality from Sri Lanka"
                }
            ],
            "brand_insights": "Specify Ceylon vs Cassia. Highlight origin and quality grade.",
            "traditional_uses": "Culinary (baking, beverages), medicinal (blood sugar regulation), ceremonial (ancient offerings)",
            "authenticity_markers": ["Specify variety (Ceylon vs Cassia)", "Mention origin", "Reference quality grade"]
        }
    
    def _get_pepper_response(self):
        return {
            "text": "pepper",
            "type": "cultural",
            "category": "spice",
            "description": "King of spices. Drove ancient trade routes and exploration.",
            "indigenous_synonyms": [
                {
                    "term": "Kali Mirch",
                    "language": "Hindi",
                    "culture": "Indian",
                    "definition": "Means 'black pepper'. Native to Kerala, India. Ancient trade commodity.",
                    "context": "Black, white, and green peppercorns from same plant, different processing"
                },
                {
                    "term": "Milagu",
                    "language": "Tamil",
                    "culture": "South Indian",
                    "definition": "Essential in rasam and traditional medicine. Warming spice in Siddha medicine.",
                    "context": "Whole peppercorns vs ground. Fresh ground for maximum flavor"
                }
            ],
            "brand_insights": "Specify variety (black, white, green, red). Highlight origin (Tellicherry, Malabar).",
            "traditional_uses": "Culinary (universal seasoning), medicinal (digestive aid, bioavailability enhancer), trade (ancient currency)",
            "authenticity_markers": ["Specify variety and grade", "Mention origin", "Reference traditional use"]
        }
    
    def _get_honey_response(self):
        return {
            "text": "honey",
            "type": "cultural",
            "category": "sweetener",
            "description": "Ancient sweetener produced by bees. Sacred in many cultures.",
            "indigenous_synonyms": [
                {
                    "term": "Shahad",
                    "language": "Hindi/Urdu",
                    "culture": "Indian/Middle Eastern",
                    "definition": "Mentioned in Ayurveda and Islamic medicine. Used for healing and nutrition.",
                    "context": "Raw vs processed. Floral source affects flavor and properties"
                },
                {
                    "term": "Miel",
                    "language": "Spanish/French",
                    "culture": "European/Latin American",
                    "definition": "Traditional sweetener before sugar. Each region has unique varieties.",
                    "context": "Monofloral (single flower) vs multifloral (wildflower)"
                }
            ],
            "brand_insights": "Specify floral source and origin. Highlight raw/unfiltered for authenticity.",
            "traditional_uses": "Culinary (sweetener, preservative), medicinal (wound healing, cough remedy), ceremonial (offerings, rituals)",
            "authenticity_markers": ["Specify floral source", "Mention raw vs processed", "Reference origin"]
        }
    
    def analyze_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Analyze text and return mock responses for known ingredients.
        """
        if not text or not text.strip():
            return []
        
        text_lower = text.lower()
        results = []
        
        # Check for each known ingredient
        for ingredient, response in self.mock_responses.items():
            if ingredient in text_lower:
                results.append(response)
        
        return results
    
    def get_model_info(self) -> Dict[str, str]:
        """Get model information"""
        return {
            'model_id': self.model_id,
            'region': self.region_name,
            'service': 'Mock Bedrock (Demo Mode)'
        }
