# Christopher Esther, Hill Lab, 7/13/2026
from pathlib import Path
import os
from datetime import datetime

from .models import File
from .utilities import windows_long_path
from .parse import parser_dispatch, clean_parse

def scan(path):

    """Scans one file and returns an incomplete database item."""

    # Convert to path object
    path = Path(path)

    # Basic path and type information
    file = File()
    file.path = str(path)
    file.dir_path = str(path.parent)
    file.filename = str(path.stem)
    file.is_directory = path.is_dir()
    file.extension = str(path.suffix)
    file.suffixes = ''.join(path.suffixes)

    # Existence information
    try:
        os_stats = os.stat(path)
    except FileNotFoundError:
        try:
            path = windows_long_path(path)
            os_stats = os.stat(path)
        except FileNotFoundError:
            return None

    file.exists = True
    file.size = os_stats.st_size
    file.dt_created = datetime.fromtimestamp(os_stats.st_ctime)
    file.dt_modified = datetime.fromtimestamp(os_stats.st_mtime)

    # File system parameters
    file.ino = str(os_stats.st_ino)
    file.dev_id = str(os_stats.st_dev)
    file.nlink = str(os_stats.st_nlink)
    file.uid = str(os_stats.st_uid)
    file.gid = str(os_stats.st_gid)

    # Check extension to determine if eligible for keyword parsing
    clean_extension = file.extension.replace('.', '')
    selected_parser = parser_dispatch(clean_extension)

    # If a parser is found, trigger keyword parsing
    if selected_parser:
        raw_parse_results = selected_parser(path)

        # Load the list of stopwords
        stopwords_path = Path(__file__).parent / 'parsers/stopwords.txt'
        with open (stopwords_path, 'r', encoding='utf-8') as sws:
            stopwords = set([line.strip() for line in sws if line.strip()])

        # Clean results and remove stopwords
        if raw_parse_results is not None:
            keywords, keywords_present = clean_parse(parse_results=raw_parse_results, stopwords=stopwords)
            return file, keywords, keywords_present
        
        else:
            return file, None, False

    else:
        return file, None, False


def traverse(traverse_path):
        
    """
    Traverses the provided scan path, yielding one file or directory path 
    at a time for rule evaluation and potential scanning.
    """
    for dirpath, dirnames, filenames in os.walk(traverse_path):
        # Yield directories first
        for dirname in dirnames:
            dir_path = Path(os.path.join(dirpath, dirname)).as_posix()
            yield dir_path
        
        # Yield files next
        for filename in filenames:
            file_path = Path(os.path.join(dirpath, filename)).as_posix()
            yield file_path
