# Christopher Esther, Hill Lab, 5/4/2026
import pandas as pd
import numpy as np
from pathlib import Path
import json

from ..utilities.generate_safe_name import generate_safe_name

def create_groups(h5_path):

    """
    Create a templated JSON file used to assign groups before processing.

    ARGUMENTS:
        h5_path (string): the path to the h5 batch file for which the
            groups will be created.
    """

    # Load the summary data
    summary = pd.read_hdf(h5_path, key='summary')

    # Catch dataset that do not have identifiers
    try:
        unique_identifiers = np.unique(summary['identifier'])
    except KeyError:
        raise ValueError('Identifiers have not yet been applied to this dataset.')

    # Variable for storing JSON template
    groups_json = {}

    # Create some dummy groups to serve as an example
    dummy_groups = np.array_split(unique_identifiers, 5)

    # Iterate over each and add it to the example json
    for i, dummy_group in enumerate(dummy_groups):
        groups_json[f'Example Group {i + 1}'] = list(dummy_group)

    # Create the json file for defining groups
    json_name = f"{Path(h5_path).stem.split('.')[0]}.groups.json"

    # Check and receive the actual safe name for this file
    _, json_path = generate_safe_name(name=json_name, folder=Path(h5_path).parent)

    # Write this example data to a json file
    with open(json_path, 'w') as f:
        json.dump(groups_json, f, indent=4, default=int)

    # Write out some information so the user knows what to do
    print('Groups file successfully created!')
    print('Please open and edit this file to assign groups before continuing with processing.\n')
    print(json_path)
