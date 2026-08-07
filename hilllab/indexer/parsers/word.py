# Christopher Esther, Hill Lab, 7/17/2026
from docx import Document

def parse_word(full_path):

    """Word file parser"""

    try:
        # Load the document
        doc = Document(full_path)
        words = []
        for para in doc.paragraphs:
            if para.text.strip():  # skip empty lines
                split_text = para.text.strip().split(' ')
                words.append(split_text)

        # Flatten the list
        flat_words = [item for sublist in words for item in sublist]

        return flat_words

    except Exception:
        return None
