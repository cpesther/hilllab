# Christopher Esther, Hill Lab, 7/17/2026
def parse_txt(full_path):

    """TXT file parser"""

    try:
        words = []
        with open(full_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    words.append(line)
        return words

    except Exception:
        return None
