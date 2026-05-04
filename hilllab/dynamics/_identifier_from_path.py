# Christopher Esther, Hill Lab, 5/1/2026
from pathlib import Path

def _identifier_from_path(path, split1, split2, name_only=False, numeric_only=False):

    """
    A helper function that takes a file path, performs a split at a certain
    point, and then returns the value immediately following the split.
    This is used for extracting identifiers from pathnames. 

    ARGUMENTS:
        path (string): the file path from which the identifier will be
            dervied. 
        split1 (string): the string where the path should be split first
        split2 (string): the string where the last fragment of the previous
            path split should be split again.
        name_only (bool): if true, the identifier extraction will be
            performed only on the file name, not the entire path
        numeric_only (bool): if true, only numerical characters in the 
            identifier will be included
    """

    # Split the string on the path
    # Work only on the file name, if requested
    if name_only:
        part_to_split = Path(path).name
    else:
        part_to_split = path
        
    # Perform the splits
    identifier = part_to_split.split(split1)[-1].split(split2)[0]

    # Extract only numerical characters, if requested
    if numeric_only:
        identifier = ''.join(c for c in identifier if c.isdigit())

    return identifier
