# Christopher Esther, Hill Lab, 1/16/2026
import numpy as np

from ._identifier_from_path import _identifier_from_path

def create_identifiers(summary, split1, split2, name_only=False, numeric_only=False):

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
        summary (pandas.DataFrame): the summary table from an h5 dynamics file
        split1 (string): the string where the path should be split first
        split2 (string): the string where the last fragment of the previous
            path split should be split again.
        name_only (bool): if true, the identifier extraction will be
            performed only on the file name, not the entire path
        numeric_only (bool): if true, only numerical characters in the 
            identifier will be included
    """
    
    # Extract and save the plate numbers from the path
    identifiers = summary['path'].apply(_identifier_from_path, args=(split1, split2, name_only, numeric_only,))
    unique_identifiers = np.unique(identifiers)
    
    # Confirm the identifiers before proceeding
    print('The following identifiers have been extracted from the path data.')
    print(unique_identifiers)
    confirmation = input('Proceed with these identifiers? [y]/n: ')
    
    # Proceed with input and return whether extraction was successful
    if (confirmation.upper() == 'Y') or (confirmation.upper() == ''):
        summary['identifier'] = identifiers
        print('Identifiers applied!')
        return True, summary
    else:
        return False, None
