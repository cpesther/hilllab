# Christopher Esther, Hill Lab, 12/8/2025
import os
from pathlib import Path
import pandas as pd
import numpy as np

from ..utilities.print_progress_bar import print_progress_bar
from ..beads.primary_analysis import primary_analysis

def batch_primary_analysis(folder_path, fps, pixel_width, compile=True):

    """
    Runs the primary_analysis function on a batch of folders containing
    videos and exports the results to Excel files for each subfolder.
    For more details, see the primary_analysis function docstring.

    ARGUMENTS:
        path (string): the path to the VRPN file
        fps (int): the frame rate of the video
        pixel_width (float): if provided, distance-related 
            values will be converted with this factor allowing the conversion
            of pixels into any arbitrary unit.

    RETURNS:
        Outputs a .xlsx file within each subfolder containing the
            compiled data from each VRPN. Certain data is also saved
            to pickle files for faster loading. 
    """

    # Get all the subfolders and their files
    folders = {}
    file_count = 0
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.vrpn.mat'):
                full_path = os.path.join(root, file)
                if root not in folders:
                    folders[root] = []
                folders[root].append(full_path)
                file_count += 1

    # Iterate over each subfolders
    processing_count = 0
    summary_all_dfs = []  # list to store dfs if compiling
    inst_data_all_dfs = []
    metadata_final_dicts = []
    for sub_index, subfolder in enumerate(folders.keys()):
        vrpn_files = folders[subfolder]  # get the paths within this subfolder

        # Create some variables to store the results
        summary_data_dfs = []
        inst_data_dfs_sub = []
        metadata_dict = {}
        
        # Run primary analysis on each VRPN file
        for file_index, sub_file in enumerate(vrpn_files):

            # Print a progress bar
            processing_count += 1
            print_progress_bar(progress=processing_count, total=file_count, title=f'Primary analysis ({processing_count} of {file_count})')
            
            # Run analysis
            one_summary_data, one_inst_data, one_metadata = primary_analysis(path=sub_file, fps=fps, pixel_width=pixel_width)

            # Save the results
            summary_data_dfs.append(one_summary_data)
            inst_data_dfs_sub.append(one_inst_data)
            metadata_dict[sub_file] = one_metadata

        # Compile the resuts into their dfs
        summary_data = pd.concat(summary_data_dfs)
        inst_data_sub = pd.concat(inst_data_dfs_sub)
        name = Path(subfolder).name
        excel_file_path = os.path.join(subfolder, f'{name}.xlsx')
        
        # Only save the dataframe if compiling the data afterwards
        if compile:
            summary_all_dfs.append(summary_data)
            inst_data_all_dfs.append(inst_data_sub)
            metadata_final_dicts.append(metadata_dict)

        # Save the results to Excel files
        with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
            summary_data.to_excel(writer, sheet_name='Summary Data', index=False)

    # Compile these Excel files into one, if requested
    if compile:

        compiled_data = pd.concat(summary_all_dfs)  # compile the data
        compiled_instantaneous = pd.concat(inst_data_all_dfs)

        # Generate the save name and paths
        compiled_name = Path(folder_path).name
        compiled_excel_path = os.path.join(folder_path, f'{compiled_name}.xlsx')
        compiled_h5_path = os.path.join(folder_path, f'{compiled_name}.h5')
        
        # Save the compiled data to Excel file
        print('\n')
        print('Saving data. This may take a minute...')
        with pd.ExcelWriter(compiled_excel_path, engine='openpyxl') as writer:
            compiled_data.to_excel(writer, sheet_name='summary', index=False)

        # Save to H5 as well for faster access
        compiled_data.to_hdf(compiled_h5_path, key='summary', mode='w', format='table')

        # Save all the instantaneous data to a H5 file for later access
        # First we must clean up any None values into NaNs
        compiled_instantaneous = compiled_instantaneous.map(lambda x: np.nan if x is None else x)
        inst_data_h5_path = os.path.join(folder_path, f'{compiled_name}.positions.h5')
        compiled_instantaneous.to_hdf(inst_data_h5_path, key='positions', mode='w', format='table')
