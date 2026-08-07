# Christopher Esther, Hill Lab, 7/17/2026
import pandas as pd

def parse_excel(full_path):

    """Excel file parser"""

    try:
        # Load the excel file
        df = pd.read_excel(full_path)
    
        # List to hold found words
        words = []
        
        # Iterate through all cells
        for col in df.columns:
            for item in df[col]:
                if isinstance(item, str) and item.strip():
                    words.append(item)
    
        # Return the list of words
        return words
    
    except Exception:
        return None
    