# Christopher Esther, Hill Lab, 12/10/2025
import os

def walk_dir(path, type=None):
    
    """
    Walks a directory and all subfolder and returns a list of all files.
    
    ARGUMENTS:
        path (string): the path to the root folder to be walked
        type (string): allows the specification of a certain file 
            extension to record, filtering out all other file types

    RETURNS:
        flist (list): a list of the full file path of each file found 
            within the root path and its subfolders
    """
    
    flist = []
    for root, _, files in os.walk(path):
        
        # Iterate over every file in the walk
        for file in files:

            # Only append if it matches
            if file.endswith(type):
                flist.append(os.path.join(root, file))
                
    return flist
        
