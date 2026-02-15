"""
Test examples for Mangolint - Indigenous Linguist and Brand Anthropologist

This file contains example inputs and expected JSON output structures
to demonstrate the system's capabilities.
"""

EXAMPLE_INPUTS = {
    "mango": {
        "input": "mango",
        "expected_structure": {
            "text": "mango",
            "type": "cultural",
            "category": "fruit",
            "description": "Tropical stone fruit with deep cultural significance...",
            "indigenous_synonyms": [
                {
                    "term": "Manga",
                    "language": "Portuguese",
                    "culture": "Brazilian/Portuguese",
                    "definition": "Derived from Malayalam 'māṅṅa'...",
                    "context": "Ripeness matters: 'manga verde' (green mango) for pickles..."
                },
                {
                    "term": "Aam",
                    "language": "Hindi/Urdu",
                    "culture": "North Indian/Pakistani",
                    "definition": "Sacred fruit in Hindu tradition...",
                    "context": "Ripeness stages: 'kairi' (raw/green), 'aam' (ripe)..."
                },
                {
                    "term": "Māṅgāy/Māmpalam",
                    "language": "Tamil",
                    "culture": "South Indian/Tamil",
                    "definition": "Etymology root of English 'mango'...",
                    "context": "Green mango ('māṅgāy') for pickles and chutneys..."
                }
            ],
            "brand_insights": "Authenticity opportunity: Specify ripeness stage...",
            "traditional_uses": "Culinary (fresh, dried, pickled), medicinal...",
            "authenticity_markers": [
                "Specify variety (Alphonso, Ataulfo, Tommy Atkins)",
                "Indicate ripeness stage",
                "Reference traditional preparation methods"
            ]
        }
    },
    
    "turmeric": {
        "input": "turmeric",
        "expected_synonyms": [
            "Haldi (Hindi/Urdu)",
            "Manjal (Tamil)",
            "Pasupu (Telugu)",
            "Arisina (Kannada)",
            "Kurkuma (German/Dutch)",
            "Curcuma (French/Spanish)"
        ],
        "expected_context": "Fresh vs dried, culinary vs medicinal, ceremonial use in Hindu weddings"
    },
    
    "corn": {
        "input": "corn",
        "expected_synonyms": [
            "Maíz (Spanish)",
            "Mahiz (Taíno - original)",
            "Elote (Nahuatl - on the cob)",
            "Choclo (Quechua/Andean)",
            "Milho (Portuguese)"
        ],
        "expected_context": "Fresh (elote), dried (maíz), ground (masa), sacred crop in Mesoamerican cultures"
    },
    
    "coconut": {
        "input": "coconut",
        "expected_synonyms": [
            "Nariyal (Hindi)",
            "Thengai (Tamil)",
            "Kobbari (Telugu)",
            "Kelapa (Malay/Indonesian)",
            "Coco (Spanish/Portuguese)"
        ],
        "expected_context": "Young (tender coconut water), mature (copra), sacred in Hindu rituals"
    },
    
    "vanilla": {
        "input": "vanilla",
        "expected_synonyms": [
            "Vainilla (Spanish)",
            "Tlilxochitl (Nahuatl - 'black flower')",
            "Vanille (French)",
            "Wanilia (Swahili)"
        ],
        "expected_context": "Cured vs extract, Madagascar vs Tahitian vs Mexican varieties, labor-intensive cultivation"
    }
}

COMPLEX_TEXT_EXAMPLES = [
    {
        "input": "Our skincare line uses organic mango butter, turmeric extract, and coconut oil.",
        "expected_entities": ["mango", "turmeric", "coconut"],
        "expected_categories": ["fruit", "spice", "fruit/oil"]
    },
    {
        "input": "Traditional recipe includes corn masa, vanilla beans, and cinnamon.",
        "expected_entities": ["corn", "vanilla", "cinnamon"],
        "expected_categories": ["grain", "spice", "spice"]
    },
    {
        "input": "The tea blend contains ginger, cardamom, and black pepper.",
        "expected_entities": ["ginger", "cardamom", "black pepper"],
        "expected_categories": ["spice", "spice", "spice"]
    }
]

def print_example_output():
    """Print formatted example output for documentation"""
    import json
    
    print("=" * 80)
    print("MANGOLINT - Example Output Structure")
    print("=" * 80)
    print("\nInput: 'mango'\n")
    print("Expected JSON Output:")
    print(json.dumps([EXAMPLE_INPUTS["mango"]["expected_structure"]], indent=2))
    print("\n" + "=" * 80)

if __name__ == "__main__":
    print_example_output()
