# Christopher Esther, Hill Lab, 5/11/2026
from pathlib import Path

from .generate_safe_name import generate_safe_name

def generate_neighbor_path(path, extension, prefix=None, suffix=None, name=None, check_safety=False):

    """
    Generates a path for a file in the same folder as the provided file 
    path. Useful when wanting to save a figure or file to the same folder
    as another but with a different or modified name, such as saving 
    PNG figures to the same folder as the Excel file from which they
    were created. 

    ARGUMENTS:
        path (string): the full path to the file which the resultant
            path should be a neighbor to.
        extension (string): the file extension which this new path should
            use (with or without preceeding period)
        prefix (string): a string to append at the front of the new file's
            name.
        suffix (string): a string to append at the end of the new file's
            name before the extension. 
        name (string): an entirely custom name to give the newly generated
            file path. If none is provided, the name of the file provided
            in the path argument will be used along with any provided
            prefix or suffix.
        check_safety (bool): if True, the function will automatically
            check if a file with this path already exists, and if so, it
            will add an increment to the end of the file name until 
            no collision is found. 

    RETURNS:
        full_path (string): the full path to the new neighboring file
    """

    # Get the path to the parent folder
    folder = Path(path).parent

    # Determine name for the file
    if name is None:
        base_name = Path(path).stem.split('.')[0]
    else:
        base_name = name

    # Add prefix and suffix (if provided)
    full_name = f"{prefix or ''}{base_name}{suffix or ''}"

    # Make sure extension has a dot at the front
    if '.' not in extension:
        extension = f'.{extension}'

    # And add to file name
    final_name = full_name + extension

    # Create the full path
    full_path = folder / final_name

    # Check safety, if requested
    if check_safety:
        _, final_path = generate_safe_name(name=full_path.stem, folder=full_path.parent)
    else:
        final_path = full_path
    
    return final_path
