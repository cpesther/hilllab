# Christopher Esther, Hill Lab, 7/17/2026
import json

def parse_json(full_path):
    
    """JSON file parser"""

    try:
        words = []
        with open(full_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # Recursively walk the JSON structure
            def extract_strings(obj):
                if isinstance(obj, dict):
                    for value in obj.values():
                        extract_strings(value)
                elif isinstance(obj, list):
                    for item in obj:
                        extract_strings(item)
                elif isinstance(obj, str):
                    if obj.strip():
                        words.append(obj)

            extract_strings(data)

        return words

    except Exception:
        return None
