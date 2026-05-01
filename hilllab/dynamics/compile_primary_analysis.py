# Christopher Esther, Hill Lab, 1/9/2026
from pathlib import Path
import os
import datetime
import pandas as pd
import numpy as np

from ..utilities.walk_dir import walk_dir
from ..utilities.print_progress_bar import print_progress_bar

def compile_primary_analysis(folder_path, save_file=True):

    """
    Compiles the H5 files produced by the primary analysis functions
    into one combined dataframe, with options to save it as a file or 
    just return it for further processing. 

    ARGUMENTS:
        folder_path (string): a path to the parent folder containing
            H5 files, or containing subfolders with H5 files.
        save_file (bool): controls whether the compiled dataset is saved
            to an H5 file or just returned. 
    """

    # First, create the path to the compiled file and check if it exists
    if save_file:
        test_compiled_path = Path(folder_path) / f'{Path(folder_path).name}.batch.h5'

        if os.path.exists(test_compiled_path):
            print('ALERT: A compiled file already exists in this folder!')
            overwrite = input('Overwrite existing file? y/[n]:')

            if overwrite.upper() == 'Y':
                os.remove(test_compiled_path)
                compiled_path = test_compiled_path
            else:
                datetime_string = str(datetime.datetime.now().replace(microsecond=0)).replace(':', '_')
                compiled_path = test_compiled_path.parent / f'{test_compiled_path.stem} {datetime_string}.batch.h5'

        else:
            compiled_path = test_compiled_path

    # Walk the directory for h5 files
    h5_files = walk_dir(folder_path, extension='h5')

    # Create some arrays to save our loaded dataframes
    summary_dfs = []
    positions_dfs = []
    metadata_dfs = []
    exceptions = []  # and a list of any errors we encounter

    # Iterate over each file and load the data
    for i, file in enumerate(h5_files):

        print_progress_bar(total=len(h5_files), progress=i + 1, title='Reading data')

        # Open each table and read the data into the lists
        try:
            summary_dfs.append(pd.read_hdf(file, key='summary'))
            positions_dfs.append(pd.read_hdf(file, key='instantaneous'))
            metadata_dfs.append(pd.read_hdf(file, key='metadata'))
        except Exception:
            exceptions.append({file: Exception})

    # Concat the data into each respective dataframe and reset index 
    compiled_summary = pd.concat(summary_dfs).reset_index(drop=True)
    compiled_instantaneous = pd.concat(positions_dfs).reset_index(drop=True)
    compiled_metadata = pd.concat(metadata_dfs).reset_index(drop=True)

    # Save the file, if requested
    if save_file:
        # Save the compiled H5 file to the initial directory
        print('\nSaving data. This may take a minute...')
        compiled_summary.to_hdf(compiled_path, key='summary', mode='w', format='table',
                            data_columns=['uuid', 'path', 'particle_id'])

        # Save the instantaneous data, and replace None with NaN first
        compiled_instantaneous = compiled_instantaneous.map(lambda x: np.nan if x is None else x)
        compiled_instantaneous.to_hdf(compiled_path, key='instantaneous', mode='a', format='table',
                                    data_columns=['uuid', 'path', 'particle_id'])

        # Save the metadata
        compiled_metadata.to_hdf(compiled_path, key='metadata', mode='a', format='table',
                                data_columns=['path'])

        # Some final prints
        print(f'Saved compiled data as {compiled_path}')

    # Otherwise just return the compiled dataframes
    else:
        return compiled_summary, compiled_instantaneous, compiled_metadata
    