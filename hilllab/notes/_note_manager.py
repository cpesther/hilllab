# Christopher Esther, Hill Lab, 10/2/2025
import importlib.resources
import os
from datetime import datetime

def _create_note(folder_path, file_name, boilerplate, avoid_rewrite=True):

    """
    Create a file at a requested location given a folder path and name 
    using boilerplate in the notes module.

    ARGUMENTS:
        path (string): the path to the folder where the file should be
            created
        file_name (string): the name for the file at this location,
            excluding the file extension. 
        boilerplate (string): the name of the text file that should be
            used as the boilerplate for the newly created file.
        avoid_rewrite (bool): prevents the function from creating a new
            file if one already exists at this location. 
    """

    # Sanitize file name and create full path
    sanitized_name = file_name.split('.')[0]
    new_file = os.path.join(folder_path, f'{sanitized_name}.txt')

    # If this path already exists and we're avoiding a rewrite, do nothing
    if os.path.exists(new_file) and avoid_rewrite:
        return new_file

    # Read the boilerplate text
    with importlib.resources.open_text(__package__, f'{boilerplate}.txt') as f:
        text = f.read()

    # Ensure the target directory exists
    os.makedirs(folder_path, exist_ok=True)

    # Write the text to the new file
    with open(new_file, 'w') as f_new:
        f_new.write(text)
    return new_file


def _append_note(path, text, include_timestamp=True):

    """
    Appends a line of text to a text file at a given path location. This
    function does nothing crazy, it's just me being lazy and not wanting
    to write the 5 lines of code required to write to a text file each
    time it's needed. 

    ARGUMENTS:
        path (string): the path to the file that should be appended
        text (string): the text to append
        include_timestamp (bool, optional): whether a timestamp should be
            prepended to the text message.
    """

    # Format the text with a timestamp, if requested
    if include_timestamp:
        full_message = f'[{str(datetime.now().replace(microsecond=0))}] {text}'
    else:
        full_message = text

    # Append this message to the requested file
    with open(path, 'a') as f:
        f.write(f'\n{full_message}')
        