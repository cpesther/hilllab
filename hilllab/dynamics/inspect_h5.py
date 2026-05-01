# Christopher Esther, 5/1/2026
import pandas as pd
from pathlib import Path
import numpy as np

from ..utilities.print_dict_table import print_dict_table

def inspect_h5(h5_path, show_parents=True):

    """
    Displays various information about the dataset contained with in 
    an h5 file produced in the dynamics pipeline. 

    ARGUMENTS:
        h5_path (string): the file path to the h5 file to inspect
        show_parents (bool): controls whether the parent folders of 
            every VRPN included in the h5 file should be printed. 
    """

    # Load the summary table
    summary = pd.read_hdf(h5_path, key='summary')

    # Compile information about this H5 file
    file_info = {}

    file_info['Name'] = Path(h5_path).stem
    file_info['# Beads'] = summary.shape[0]
    file_info['# VRPNs Compiled'] = len(np.unique(summary['path']))

    # Get list of parent folders
    parents = np.unique([Path(p).parent for p in np.unique(summary['path'])])
    file_info['# Parent Folders'] = len(parents)

    # Print the details table
    print_dict_table(file_info, title='H5 File Inspection')

    # Print all parent folders, if requested
    if show_parents:
        print('------ PARENT FOLDERS ------')
        for parent in parents:
            print(parent)
    return
