# Christopher Esther, Hill Lab, 7/17/2026
import re

from . import parsers

def parser_dispatch(extension):

    # This dict defines what extensions get handled by which parsers
    valid_parsers = {
        'csv': parsers.p_csv.parse_csv,
        'xlsx': parsers.excel.parse_excel,
        'xls': parsers.excel.parse_excel,
        'html': parsers.html.parse_html,
        'htm': parsers.html.parse_html,
        'json': parsers.json.parse_json,
        'geojson': parsers.json.parse_json,
        'har': parsers.json.parse_json,
        'pdf': parsers.pdf.parse_pdf,
        'pptx': parsers.powerpoint.parse_powerpoint,
        'potx': parsers.powerpoint.parse_powerpoint,
        'ppsx': parsers.powerpoint.parse_powerpoint,
        'txt': parsers.txt.parse_txt,
        'md': parsers.txt.parse_txt,
        'log': parsers.txt.parse_txt,
        'ini': parsers.txt.parse_txt,
        'cfg': parsers.txt.parse_txt,
        'conf': parsers.txt.parse_txt,
        'docx': parsers.word.parse_word,
        'dotx': parsers.word.parse_word,
        'yaml': parsers.yaml.parse_yaml,
        'yml': parsers.yaml.parse_yaml
    }

    # Check if the provided extension is included
    if extension in valid_parsers:
        selected_parser = valid_parsers[extension]

    # Otherwise return None
    else:
        selected_parser = None

    return selected_parser

def clean_parse(parse_results, stopwords):

    """Cleans file parse results by removing irrelevant characters, numbers,
    and symbols, as well as filtering out a large collection of stop words."""

    # Start by making sure the results are split by words and flattened
    raw_words = []
    for line in parse_results:
        # Split on whitespace into individual words
        for word in line.split():
            if word:
                raw_words.append(word.lower())

    # Now remove any "unclean" entries
    cleaned_results = []

    # For each word
    for word in raw_words:
        # Remove non-printable characters
        word = ''.join(c for c in word if c.isprintable())

        # Remove anything that's not a letter or space
        word = re.sub(r'[^a-zA-Z\s]', '', word)

        # Collapse multiple spaces and strip
        word = re.sub(r'\s+', ' ', word).strip()

        if word:  # skip empty lines
            cleaned_results.append(word)

    # Filter through every word by exclude stopwords
    filtered_keywords = [word for word in cleaned_results if word not in stopwords]

    # Check if there are keywords present
    keywords_present = (len(filtered_keywords) > 0)
    
    return filtered_keywords, keywords_present
    