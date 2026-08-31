import json
import re

def parse_response(text):
    """Parses the JSON response from the AI model, handling formatting issues."""
    if not text:
        return None
    text = re.sub(r'^```json\s*', '', text.strip())
    text = re.sub(r'\s*```$', '', text.strip())
    try:
        data = json.loads(text)
        required_keys = ["summary", "relevant_law", "legal_position", "case_law", "possible_steps", "sources", "disclaimer"]
        for key in required_keys:
            if key not in data:
                data[key] = None if key in ["relevant_law"] else ([] if key in ["case_law", "sources"] else "")
        return data
    except json.JSONDecodeError:
        return {
            "summary": "",
            "relevant_law": None,
            "legal_position": "",
            "case_law": [],
            "possible_steps": "",
            "sources": [],
            "disclaimer": "Unable to parse AI response. Please try again."
        }