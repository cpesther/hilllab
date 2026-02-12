# Christopher Esther, Hill Lab, 1/22/2026
import pandas as pd
from pathlib import Path
import os
import numpy as np

from ..utilities.walk_dir import walk_dir
from ..utilities.print_progress_bar import print_progress_bar

def compile_CBF_FFCA(folder, compile_all=True):

    """
    Compiles all CSV files output from the calculate_CBF_FFCA function
    into one CSV either for every file or for each subfolder individually.
    
    ARGUMENTS:
        folder (string): the path to the folder containing CBF/FFCA CSV files.
    """
    
    # Define a helper function to allow us to reuse some logic
    def _compile_files(all_csvs, output_folder):
        """A helper function to allow us to reuse the file I/O logic for
        both complete and subfolder compilations."""
        
        all_dfs = []
        num_csvs = len(all_csvs)
        for i, csv in enumerate(all_csvs):
            
            # Load the data
            if '_CBF_FFCA' in csv:
                data = pd.read_csv(csv, usecols=['cbf', 'ffca', 'method', 'flag'])
                
                # Determine the name for this file
                raw_name = Path(csv).stem
                final_name = raw_name.replace('_CBF_FFCA', '')
                
                # Save the data
                data['file'] = final_name
                all_dfs.append(data)
            else:
                print(f'Skipped file {csv}')

            # Print progress bar
            print_progress_bar(progress=i+1, total=num_csvs, title='Compiling data...')

        # Compile and export the data
        compiled_data = pd.concat(all_dfs)
        save_name = f'{Path(output_folder).stem}.csv'
        save_path = os.path.join(output_folder, save_name)
        compiled_data.to_csv(save_path, index=False)
        return save_path
    
    # List all CSVs
    all_csvs = walk_dir(folder, extension='csv')

    if compile_all:
        save_path = _compile_files(all_csvs, output_folder=folder)
        print(f'CBF/FFCA files successfully compiled to \n{save_path}')

    # If compiling on a subfolder-based level
    else:
        
        # Calculate all the paths to each subfolder and compile each individually
        all_subfolders = np.unique([Path(path).parent for path in all_csvs])
        save_paths = []
        for subfolder in all_subfolders:
        
            # List the CSVs in this directory and compile on those
            subfolder_csvs = walk_dir(subfolder, extension='csv')
            save_path = _compile_files(subfolder_csvs, output_folder=subfolder)
            save_paths.append(save_path)

        # Final prints
        print('CBF/FFCA files successfully compiled to each subfolder below.\n')
        [print(file) for file in save_paths];  # noqa: E703
