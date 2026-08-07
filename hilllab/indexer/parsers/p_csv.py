# Christopher Esther, Hill Lab, 7/17/2026
import csv

def parse_csv(full_path):

    """CSV file parser"""

    try:
        words = []
        with open(full_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                for cell in row:
                    if cell.strip():
                        words.append(cell)
        return words

    except Exception:
        return None
