# Christopher Esther, Hill Lab, 1/16/2026
from pathlib import Path
import re
import numpy as np

def create_identifiers(summary, identifier_name, identifier_split):

    """
    Uses the path values saved from the primary analysis function to
    extract and save a more sensible label for each bead. This function 
    splits the file name on the identifier_split string and then captures
    the numerical values immediately following. These numerical values
    are saved to the summary data in a column with the identifier_name
    argument.

    For example, the file name Plate16Culture1_0001.vrpn.mat
    with the identifier_split = 'Plate' returns a value of 16.

    ARGUMENTS:
        identifier_name (string): this is the name of the column in the 
            summary data table in which the identifier values will be 
            saved
        identifier_split (string): this is the string within the file
            name which is immediately followed by the numerical values
            desired for use as the identifier.
    """

    # Here's our helper function that can actually be applied to the df
    def _identifier_from_path(path, identifier_split=identifier_split):
    
        # Split the string on the path
        post_split_string = Path(path).name.split(identifier_split)[-1]
        return re.match(r'^[-+]?\d*\.?\d+', post_split_string).group(0)  # return following numericals
    
    # Extract and save the plate numbers from the path
    identifiers = summary['path'].apply(_identifier_from_path, args=(identifier_split,))
    unique_identifiers = np.unique(identifiers)
    
    # Confirm the identifiers before proceeding
    print('The following identifiers have been extracted from the path data.')
    print(unique_identifiers)
    confirmation = input('Proceed with these identifiers? [y]/n: ')
    
    # Proceed with input and return whether extraction was successful
    if (confirmation.upper() == 'Y') or (confirmation.upper() == ''):
        summary[identifier_name] = identifiers
        print('Identifiers applied!')
        return True, summary
    else:
        return False, None
