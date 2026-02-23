# Christopher Esther, Hill Lab, 2/23/2026
import pandas as pd
import numpy as np
import csv
from pathlib import Path

from ..utilities.format_spectra_table import format_spectra_table
from ..utilities.warning import warn

def plate_split_channels(path, n_channels=4):

    """
    Used to extract each channel (wavelength) from a SpectraMax file
    that contains multiple wavelengths in the same read. This is useful
    for separating data when running 1D with multiple beads. 

    ARGUMENTS:
        path (string): the path to the file containing multiple chanenls
            of data. 
        n_channels (int): the number of channels in the file

    RETURNS:
        channel_info (dict): a dict with the excitation wavelength as 
            the key and the path to the exported split file as the value. 
    """

    # Validate the n_channels argument
    if n_channels < 2:
        raise ValueError('The n_channels argument must be greater than 1.')

    # Read the raw data
    raw_data = pd.read_csv(path, sep='\t', encoding='utf-16', 
                           lineterminator='\r', header=2, skipinitialspace=True)
    
    # A file used in with this function has minimum two channels
    c1 = raw_data.loc[:, [str(i) for i in range(1, 25)]].iloc[:-4]
    c2 = raw_data.loc[:, [str(i) for i in np.arange(1.1, 25.1)]].iloc[:-4]

    # Format these two tables
    c1 = format_spectra_table(c1)
    c2 = format_spectra_table(c2)
    all_channels = [c1, c2]

    # Load a third channel if present
    if n_channels >= 3:
        columns = np.arange(1.2, 25.2).round(1)  # rounding required for floating point safety
        c3 = raw_data.loc[:, [str(i) for i in columns]].iloc[:-4]
        c3 = format_spectra_table(c3)
        all_channels.append(c3)

    # Load a fourth channel if present
    if n_channels >= 4:
        columns = np.arange(1.3, 25.3).round(1)  # rounding required for floating point safety
        c4 = raw_data.loc[:, [str(i) for i in columns]].iloc[:-4]
        c4 = format_spectra_table(c4)
        all_channels.append(c4)

    # Reopen the file to pull the excitation values so we can give each of these
    # channels and meaningful name. 
    with open(path, newline='', encoding='utf-16') as f:
        reader = csv.reader(f)

        # Read just the first few rows
        rows = [row for i, row in enumerate(reader) if i < 5]

    # Pull the row with the excitation and emission values
    exem_row = rows[1]
    excitation_values_string = exem_row[0].split('\t')[16]

    # Pull the excitation values as list
    excitation_values = excitation_values_string.strip().split(' ')

    # Verify the appropriate number 
    if len(excitation_values) != n_channels:
        
        # Display a warning
        warn('The number of channels specified in the file does not match the n_channels value.\n'
            'Please interrupt this process or input the correct excitation values below.')

        # Iterate through each channel and prompt for the excitation value
        excitation_values = []
        for i in range(n_channels):
            one_ex_value = input(f'Excitation value for channel {i + 1}:')
            excitation_values.append(one_ex_value)

    # Now we'll export each channel table as an Excel file to the same directory
    channel_info = {}
    for i, c in enumerate(all_channels):

        # Print a status message
        ex_value = excitation_values[i]
        print(f'Exporting {ex_value} nm channel ({i+1} of {n_channels})')
        
        # Create the file path
        folder_path = Path(path).parent
        file_name = f'{ex_value}nm_{Path(path).stem}.xlsx'
        file_path = folder_path / file_name

        # Save the data as an Excel file
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            c.to_excel(writer, sheet_name='data', index=True)

        # Save export information to dictionary so it can be returned
        channel_info[ex_value] = file_path

    # Print a final message
    print('Export complete!')

    return channel_info
