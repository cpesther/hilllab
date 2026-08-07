# Christopher Esther, Hill Lab, 7/17/2026
from PyPDF2 import PdfReader

def parse_pdf(full_path):

    """PDF file parser"""

    try:
        words = []
        reader = PdfReader(full_path)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                for line in text.splitlines():
                    line = line.strip()
                    if line:
                        words.append(line)
        return words

    except Exception:
        return None
