# Christopher Esther, Hill Lab, 1/16/2026
import pandas as pd
import numpy as np
from pathlib import Path
import shutil

from ._identifier_from_path import _identifier_from_path

def create_identifiers(h5_path, split1, split2, name_only=False, numeric_only=False):

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
        h5_path (string): the file path to the h5 file to test identifier extraction
        split1 (string): the string where the path should be split first
        split2 (string): the string where the last fragment of the previous
            path split should be split again.
        name_only (bool): if true, the identifier extraction will be
            performed only on the file name, not the entire path
        numeric_only (bool): if true, only numerical characters in the 
            identifier will be included
    """

    # Load the summary data
    summary = pd.read_hdf(h5_path, key='summary')

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

    # Create a new file to save the identifications to
    print('Creating new identifications file. This may take a minute...')
    identified_name = f'{Path(h5_path).stem}.identify.h5'
    identified_path = Path(h5_path).parent / identified_name
    shutil.copy(h5_path, identified_path)

    # Save the identifications to a file
    print('Saving identifications to file...')
    with pd.HDFStore(identified_path, mode='a') as store:
        store.put(
            'summary',
            summary,
            format='table',
            data_columns=['uuid', 'path', 'particle_id']
        )

    print('Identification finished!')
    