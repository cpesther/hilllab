# Christopher Esther, Hill Lab, 11/13/2025
import pandas as pd
import numpy as np
import string

from ..migration._plate_format_extended import _plate_format_extended

def _load_file(path, channels=2):

    """
    Loads and formats data from swelling experiments.
    """

    # Load the raw data from the weird, Excel-esque format
    raw_data = pd.read_csv(path, sep='\t', encoding='utf-16', lineterminator='\r', 
                        header=2, skipinitialspace=True)

    # Drop last four rows
    raw_data = raw_data.iloc[:-4]

    # Replace all NaN values with zero
    raw_data.fillna(0, inplace=True)

    # Remove the one extra spacer row in the n*17th spot for each read
    raw_data = raw_data.drop(raw_data.index[16::17])

    # Add new alphabetical index
    length = raw_data.shape[0]
    raw_data['<>'] = (list(string.ascii_uppercase[:-10]) * int(length / 16))[:length]
    raw_data = raw_data.set_index('<>')

    # Generate new names for the columns
    new_names = []
    for i in range(24):
        new_names.append(f'Column {i + 1}')

    # Split the data into separate channels, if needed
    c1 = raw_data.loc[:, [str(i) for i in range(1, 25)]]
    c2 = raw_data.loc[:, [str(i) for i in np.arange(1.1, 25.1)]]
    c1.columns = new_names
    c2.columns = new_names

    # Format as extended by default
    num_reads = int(raw_data.shape[0] / 16)
    c1 = _plate_format_extended(c1, num_reads)
    c2 = _plate_format_extended(c2, num_reads)
    
    # Run this helper function on the data and calculate the number of reads
    #c1 = format_spectra_table(c1)
    #c2 = format_spectra_table(c2)

    return c1, c2, num_reads

