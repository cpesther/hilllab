# Christopher Esther, Hill Lab, 7/17/2026
import yaml

def parse_yaml(full_path):

    """YAML file parser"""

    try:
        words = []
        with open(full_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

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
