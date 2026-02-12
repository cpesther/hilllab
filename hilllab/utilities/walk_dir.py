# Christopher Esther, Hill Lab, 12/10/2025
import os
from pathlib import Path

def walk_dir(path, extension=None):
    
    """
    Walks a directory and all subfolder and returns a list of all files.
    
    ARGUMENTS:
        path (string): the path to the root folder to be walked
        extension (list): allows the specification of a certain file 
            extension types to record, filtering out all others

    RETURNS:
        flist (list): a list of the full file path of each file found 
            within the root path and its subfolders
    """

    # Prepend period to all extensions
    if extension is not None:
        extension = [f'.{e}' for e in extension]
    
    # Walk directories
    flist = []
    for root, _, files in os.walk(path):
        
        # Iterate over every file in the walk
        for file in files:

            # Only append if it matches or no extension specified
            full_suffix = ''.join(Path(file).suffixes)
            if extension is not None:
                if (full_suffix in extension):
                   flist.append(os.path.join(root, file))
            else:
                flist.append(os.path.join(root, file))
                
    return flist
        