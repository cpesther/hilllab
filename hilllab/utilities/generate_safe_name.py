# Christopher Esther, Hill Lab, 5/4/2026
import os
from pathlib import Path

def generate_safe_name(name, folder):

    """
    Given a file name (with extensions) and a folder, generates a safe 
    file name by appending a counter to avoid unintentionally overwriting
    files. 

    ARGUMENTS:
        name (string): the desired name for the file (including any file extensions)
        folder (string): the path to the folder where this file will
            eventually be saved. 

    RETUNRS:
        new_file_name (string): the safe name of the file with any 
            counters appended
        new_file_path (string): the full path to the safe file location
            including the parent folder. 
    """

    # Get list of all file names in this folder
    all_files = os.listdir(folder)

    safe_name_found = False
    increment = 0
    while not safe_name_found:

        # Generate the new file name to try
        if increment == 0:
            new_file_name = name
        else:

            new_file_name = f"{name.split('.')[0]}_{increment}{''.join(Path(name).suffixes)}"

        # Check if this name is in the folder already
        if new_file_name not in all_files:
            safe_name_found = True

        # Increase increment to try again
        increment += 1

        # Limit iterations
        if increment > 100:
            raise ValueError('Unable to find unique file name in 100 tries')

    # Assemble the full path as a courtesy return
    new_file_path = os.path.join(folder, new_file_name)
    return new_file_name, new_file_path
            