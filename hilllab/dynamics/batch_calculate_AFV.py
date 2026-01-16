# Christopher Esther, Hill Lab, 1/9/2026
import pandas as pd
import numpy as np
from pathlib import Path

from ..utilities.print_progress_bar import print_progress_bar
from .calculate_AFV import calculate_AFV

def batch_calculate_AFV(path):

    """
    Runs AFV calculations on every bead in a H5 file output from the
    primary analysis function. AFV data is saved as a separate H5 file
    in the same directory.
    
    ARGUMENTS:
        path (str): the path to the H5 file with primary analysis data
    """

    # Open the summary and metadata tables
    summary = pd.read_hdf(path, key='summary')
    metadata = pd.read_hdf(path, key='metadata')

    # Create list for storing AFV dfs and calculate total beads
    afv_dfs = []
    total = len(summary['uuid'])

    # Iterate over each bead and run calculation
    for i, particle_uuid in enumerate(summary['uuid']):

        # Print a progress bar
        print_progress_bar(progress=i+1, total=total, title='Calculating AFV')
        
        # Load the particle data
        position_data = pd.read_hdf(path, key='positions', where=f"uuid == '{particle_uuid}'")

        if i > 100:
            break
            
        # Calculate AFV
        fps = metadata.loc[metadata['path'] == np.unique(position_data['path'])[0], 'fps'].iloc[0]
        afv_values = calculate_AFV(position_data=position_data, fps=fps)
        
        # Save the AFV values as dataframe to the list
        afv_values['uuid'] = particle_uuid
        one_afv_df = pd.DataFrame([afv_values])
        afv_dfs.append(one_afv_df)

    # Drop all-NA columns in each DataFrame before concatenation
    clean_dfs = [df.dropna(axis=1, how='all') for df in afv_dfs]

    # Only concatenate if there's at least one DataFrame with columns left
    clean_dfs = [df for df in clean_dfs if not df.empty]

    all_afv = pd.concat(clean_dfs, ignore_index=True)

    # Write these values to a H5 file in the same folder
    output_path = Path(path).parent / f'{Path(path).stem}_AFV.h5'
    all_afv = all_afv.map(lambda x: np.nan if x is None else x)
    all_afv.to_hdf(output_path, key='afv', mode='w', format='table',
                                data_columns=['uuid'])
    