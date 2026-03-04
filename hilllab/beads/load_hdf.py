# ellen han, 2/27/2026

import pandas as pd

def load_hdf(path):
    """
    Loads a HDF file, sorts summary and position dataframes by bead UUID.
    Returns groupby objects for summary and position, along with metadata dataframe.
    Also returns max xy position, for plotting purposes.

    """

    df_summary = pd.read_hdf(path, key='/summary')
    df_positions = pd.read_hdf(path, key='/positions')
    df_metadata = pd.read_hdf(path, key='/metadata')
    
    groupby_summary = df_summary.groupby('uuid') 
    groupby_positions = df_positions.groupby('uuid') 
    
    # bounds
    xmax = df_positions['x'].max() 
    ymax = df_positions['y'].max() 
    bounds = {'x': xmax,
              'y': ymax}
    
    return groupby_summary, groupby_positions, df_metadata, bounds