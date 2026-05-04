# Christopher Esther, Hill Lab, 5/4/2026
import pandas as pd
import os
from pathlib import Path
import json

from ..utilities.print_dict_table import print_dict_table

def _load_with_groups(h5_path, groups_path=None, expectations=None):

    """
    Loads the summary table from an h5 file and incorporates the groups
    column based on those assigned in the JSON file located at the gropus
    path.

    ARGUMENTS:
        h5_path (string): the path to the h5 file to be loaded
        groups_path (string): the path to the .groups.json file to be 
            used for group assignment. If None, the most recently modified
            .groups.json file in the same directory as the h5 file will
            be used, or if none exist, groups will be the same as the 
            identifier. 
        expectations (list): a list of strings indicating what features
            of the data (such as classification or identification) are 
            exepcted to be included, allowing for quick error handling
            and user guidance. 
    """

    # Load the summary data
    summary = pd.read_hdf(h5_path, key='summary')

    # Check our expectations first
    if 'identifier' in expectations:
        if 'identifier' not in summary.columns:
            pass

    # If a groups path was not provided, go through the default selection logic
    if groups_path is None:
        
        # Search for any .groups.json files in the same directory
        neighbor_files = os.listdir(Path(h5_path).parent)
        groups_files = [f for f in neighbor_files if '.groups.json' in f]

        # Check if any were found
        if len(groups_files) > 0:

            # Sort groups files by the time they were last modified
            modified_times = {}
            for file in groups_files:
                full_path = Path(h5_path).parent / file
                modified_times[os.path.getmtime(full_path)] = full_path
                
            # And select the one that was modified most recently
            selected_groups_path = modified_times[max(modified_times.keys())]
            if len(groups_files) > 1:
                print('Selecting most recent groups file...')

        # Otherwise, no groups can be assigned
        else:
            selected_groups_path = None

    # If a groups path was provided, just use that 
    else:
        selected_groups_path = groups_path

    # Now we can use this groups path (if present) to create the groups column in the data
    if selected_groups_path is not None:
        
        # Load that JSON file
        with open(selected_groups_path, 'r', encoding='utf-8') as f:
            groups_data = json.load(f)
        
        # Build reverse lookup using identifier to get group name
        id_to_group = {
            identifier: group
            for group, ids in groups_data.items()
            for identifier in ids
        }
        
        # Map group names into dataframe
        summary['group'] = summary['identifier'].map(id_to_group)
        print(f'Loaded groups from {selected_groups_path}')
        print_dict_table(groups_data, title='Groups')

    # If there is no groups path, we'll just populate the groups column with
    # the data from the identifiers column for consistency
    else:
        summary['group'] = summary['identifier']
        print('No groups loaded')

    return summary
