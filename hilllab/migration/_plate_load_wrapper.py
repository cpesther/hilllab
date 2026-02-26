# Christopher Esther, Hill Lab, 8/29/2025
import os
from pathlib import Path
from .load_file import load_file
from ._plate_prepare_data import _plate_prepare_data

def _plate_load_wrapper(path, data_type='SPE', **kwargs):

    """
    This function just wraps together all of the steps requried
    to load and pre-process a plate data file. Now we can call this 
    function and return a ready-to-go data bundle rather than having
    to call each step individually. 

    ARGUMENTS:
        path (string): a file path to automatically load a file without
            opening a file dialog window.
        data_type (string): Specifies the type model used to collect the 
            data. Options include 'SPE' (default), 'TEC', and 'PRE'.
        **kwargs: passed down to load_file() and _plate_prepare_data().
    RETURNS
        bundle (migration.Bundle): a bundled object containing the raw
            data and the attributes used for storing results.
    """

    # Create the path to a bundle for this file so we can check if 
    # one already exists and notify the user
    bundle_file_name = f'{Path(path).stem}.1dpre.xlsx'
    bundle_full_path = os.path.join(os.path.dirname(path), bundle_file_name)

    # If a bundle path already exists
    if os.path.exists(bundle_full_path):
        print('ALERT: A pre-saved bundle already exists for this data')
        print('       Would you like to load it instead?')
        decision = input('[y]/n')
        caps_decision = decision.upper()
        if (caps_decision == 'Y') or (caps_decision == ''):
            path_to_load = bundle_full_path
            data_type = 'PRE'
        # If deciding not to load the preprepared bundle
        else:  # just use the provided path
            print('ALERT: A new bundle will not be saved until the old one is removed or renamed')
            path_to_load = path
    else:
        path_to_load = path

    # Load the selected path
    l_bundle = load_file(path=path_to_load, data_type=data_type, **kwargs)

    # If not pre-prepared, prepare the data
    if data_type != 'PRE':
        bundle = _plate_prepare_data(l_bundle, **kwargs)
    else:
        bundle = l_bundle
    
    # Return the bundle
    return bundle
