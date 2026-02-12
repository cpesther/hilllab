# Christopher Esther, Hill Lab, 2/12/2026
from pathlib import Path
import os

from ...utilities.load_vrpn import load_vrpn

def vrpn_to_csv(path, skip_existing=True):

    """
    Converts a VRPN file to a CSV file. Intended to be used when converting
    files from the old MATLAB pipeline for use in the new Python pipeline.
    
    ARGUMENTS:
        path (string): the path to the VRPN file
        skip_existing (bool): when True, any CSVs that already exist 
            will be bypassed during conversion so as not to create
            duplicate CSV files for the same VRPN.
    """

    # Determine the file path and suffix
    full_suffix = ''.join(Path(path).suffixes)
    stem = Path(path).stem.split('.')[0]

    # We'll use the suffix of the VRPN file to determine the suffix of
    # the CSV file to create. It doesn't actually change how the data
    # is exported, but since we use file extensions to keep track of 
    # which processing steps have been applied to the data, taking this
    # step helps make sure those stay consistent.

    # If just a plain .vrpn.mat, then drift subtraction has not been applied
    # so it will be saved as a .track.csv. 
    if full_suffix == '.vrpn.mat':
        data = load_vrpn(path)
        csv_path = Path(path).parent / f'{stem}.track.csv'

    # If it has the evt suffixes, then drift subtraction has been applied so 
    # it should be saved as a .drift.track.csv.
    elif full_suffix == '.vrpn.evt.evt.mat':
        csv_path = Path(path).parent / f'{stem}.drift.track.csv'

    # Check if a CSV file for this VRPN already exists, and skip if so
    # and requested.
    if (os.path.exists(csv_path)) and (skip_existing):
        return

    # Load the VRPN
    data = load_vrpn(path)
    
    # Save the data to the CSV using the predtermined path
    data.to_csv(csv_path, header=True, index=False)
