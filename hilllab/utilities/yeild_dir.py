# Christopher Esther, Hill Lab, 5/7/2026
import os
from pathlib import Path

def yield_dir(path):
    
    """
    Traverses a provided path, yielding one file or directory path 
    at a time.
    """
    
    # Iterate over every top level directory
    for dirpath, dirnames, filenames in os.walk(path):
       
        # Yield folders first
        for dirname in dirnames:
            dir_path = Path(os.path.join(dirpath, dirname)).as_posix()
            yield dir_path
        
        # Yield files next
        for filename in filenames:
            file_path = Path(os.path.join(dirpath, filename)).as_posix()
            yield file_path
            