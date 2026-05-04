# Christopher Esther, Hill Lab, 5/1/2026
import pandas as pd
import numpy as np

from ._identifier_from_path import _identifier_from_path

def test_create_identifiers(h5_path, split1, split2, name_only=True, numeric_only=False):

    """
    Serves as a test function for the create_identifiers function allowing
    the user to gain an in-depth look into how identifiers are extracted
    from the paths before applying them to the real data. 

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

    # Grab some random examples for display
    random_examples = np.array(summary['path'].sample(7))

    # Print a header and instructions
    print('Please verify these example identifier extractions\n')

    # Perform extraction on each of these examples
    cut_length = 65
    for example_path in random_examples:
        identifier = _identifier_from_path(example_path, split1, split2, name_only, numeric_only)
        
        # Add ellipsis to front of path if we're shortening it
        if len(example_path) > cut_length:
            ellipsis = '...'
        else:
            ellipsis = ''

        # Print the path and the identifier it became
        print(f'{ellipsis}{example_path[-cut_length:]}    >>>    {identifier}')

    # Ask for user verification
    verification = input('\nDo these identifiers look correct? [y]/n:')

    # Test this extraction on all paths and show unique values if verified
    if ((verification.upper()) == 'Y' or (verification == '')):
        
        # Run identification on all
        all_identifiers = []
        for i, p in enumerate(summary['path']):
            print(f"Extracting {i+1}/{len(summary['path'])}", end='\r')
            all_identifiers.append(_identifier_from_path(p, split1, split2, name_only, numeric_only))

        # Display final unique results
        print('\nAll paths will be extracted to one of the following identifiers:')
        print(np.unique(all_identifiers))
