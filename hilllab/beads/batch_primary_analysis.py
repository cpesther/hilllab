# Christopher Esther, Hill Lab, 12/8/2025
import os
from pathlib import Path
import pandas as pd
import numpy as np

from ..utilities.print_progress_bar import print_progress_bar
from ..beads.primary_analysis import primary_analysis

def batch_primary_analysis(folder_path, fps, pixel_width, compile=True, skip_existing=True):

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

    # Create list to store the outputs from all files if compiling
    summary_all_dfs = []
    positions_all_dfs = []
    metadata_all_dicts = []

    # Iterate over each subfolder
    processing_count = 0
    for sub_index, subfolder in enumerate(folders.keys()):
        vrpn_files = folders[subfolder]  # get the paths within this subfolder

        # Generate the save names for this subfolder
        name = Path(subfolder).name
        subfolder_excel_file_path = os.path.join(subfolder, f'{name}.xlsx')
        subfolder_h5_file_path = os.path.join(subfolder, f'{name}.h5')

        # Check if the processing files already exist, and skip if requested
        if (os.path.exists(subfolder_h5_file_path)) and skip_existing:
            print(f'Results already exist. Skipping folder {subfolder}')
            processing_count += len(vrpn_files)
            continue
        
        # Create some variables to store the results just within this subfolder
        summary_subfolder_dfs = []
        positions_subfolder_dfs = []
        metadata_subfolder_dicts = []
        
        # Run primary analysis on each VRPN file
        for file_index, sub_file in enumerate(vrpn_files):

            # Print a progress bar
            processing_count += 1
            print_progress_bar(progress=processing_count, total=file_count, title=f'Primary analysis ({processing_count} of {file_count})')
            
            # Run analysis
            one_summary_data, one_positions_data, one_metadata = primary_analysis(path=sub_file, fps=fps, pixel_width=pixel_width)

            # Save the results
            summary_subfolder_dfs.append(one_summary_data)
            positions_subfolder_dfs.append(one_positions_data)
            metadata_subfolder_dicts.append(one_metadata)

        # Compile the resuts into their dfs for this subfolder
        summary_subfolder = pd.concat(summary_subfolder_dfs)
        positions_subfolder = pd.concat(positions_subfolder_dfs)
        metadata_sub = pd.DataFrame(metadata_subfolder_dicts)
        
        # Only save the subfolder results if compiling all the data afterwards
        if compile:
            summary_all_dfs.append(summary_subfolder)
            positions_all_dfs.append(positions_subfolder)
            metadata_all_dicts.extend(metadata_subfolder_dicts)

        # Save the results to Excel files for this subfolder
        with pd.ExcelWriter(subfolder_excel_file_path, engine='openpyxl') as writer:
            summary_subfolder.to_excel(writer, sheet_name='Summary Data', index=False)
            metadata_sub.to_excel(writer, sheet_name='Metadata', index=False)

        # And save the results to H5 files for this subfolder
        # Save to H5 as well
        summary_subfolder.to_hdf(subfolder_h5_file_path, key='summary', mode='w', format='table',
                            data_columns=['uuid', 'path', 'particle_id'])

        # Replace None with NaN for instantaneous data
        positions_subfolder = positions_subfolder.map(lambda x: np.nan if x is None else x)
        positions_subfolder.to_hdf(subfolder_h5_file_path, key='positions', mode='a', format='table',
                                    data_columns=['uuid', 'path', 'particle_id'])

        metadata_sub.to_hdf(subfolder_h5_file_path, key='metadata', mode='a', format='table',
                                data_columns=['path'])

    # Compile these Excel files into one, if requested
    if compile:

        print('\nSaving data. This may take a minute...')
        compiled_summary = pd.concat(summary_all_dfs)  # compile the data
        compiled_positions = pd.concat(positions_all_dfs)
        compiled_metadata = pd.DataFrame(metadata_all_dicts)

        # Generate the save name and paths
        compiled_name = Path(folder_path).name
        compiled_excel_path = os.path.join(folder_path, f'{compiled_name}.xlsx')
        compiled_h5_path = os.path.join(folder_path, f'{compiled_name}.h5')
        
        # Save the compiled data to Excel file
        with pd.ExcelWriter(compiled_excel_path, engine='openpyxl') as writer:
            compiled_summary.to_excel(writer, sheet_name='summary', index=False)
            compiled_metadata.to_excel(writer, sheet_name='metadata', index=False)

        # Save to H5 as well
        compiled_summary.to_hdf(compiled_h5_path, key='summary', mode='w', format='table',
                            data_columns=['uuid', 'path', 'particle_id'])

        # Replace None with NaN for instantaneous data
        compiled_positions = compiled_positions.map(lambda x: np.nan if x is None else x)
        compiled_positions.to_hdf(compiled_h5_path, key='positions', mode='a', format='table',
                                    data_columns=['uuid', 'path', 'particle_id'])

        compiled_metadata.to_hdf(compiled_h5_path, key='metadata', mode='a', format='table',
                                data_columns=['path'])
        print('Data save completed!')
