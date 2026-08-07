# Christopher Esther, Hill Lab, 7/17/2026
from bs4 import BeautifulSoup

def parse_html(full_path):

    """HTML file parser"""

    try:
        words = []
        with open(full_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            text = soup.get_text()
            for line in text.splitlines():
                line = line.strip()
                if line:
                    words.append(line)
        return words

    except Exception:
        return None
