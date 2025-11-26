# Christopher Esther, Hill Lab, 11/13/2025
import pandas as pd
import numpy as np
import string

def _load_file(path, channels=2):

    """
    Loads and formats data from swelling experiments.
    """

    # Load the raw data from the weird, Excel-esque format
    raw_data = pd.read_csv(path, sep='\t', encoding='utf-16', lineterminator='\r', 
                           header=2, skipinitialspace=True)

    # Generate new names for the columns
    new_names = []
    for i in range(24):
        new_names.append(f'Column {i + 1}')

    # Define a helper function to get these tables nicely formatted
    def _format_table(t):
        
        # Replace all NaN values with zero
        t.fillna(0, inplace=True)
    
        # Remove the one extra spacer row in the n*17th spot for each read
        t = t.drop(t.index[16::17])
    
        # Rename every column and add and set the index
        t.columns = new_names
        length = t.shape[0]
        t['<>'] = (list(string.ascii_uppercase[:-10]) * int(length / 16))[:length]
        t = t.set_index('<>')
        return t
    
    # Split the data into separate channels, if needed
    if channels == 2:
        c1 = raw_data.loc[:, [str(i) for i in range(1, 25)]].iloc[:-4]
        c2 = raw_data.loc[:, [str(i) for i in np.arange(1.1, 25.1)]].iloc[:-4]
        
        # Run this helper function on the data and calculate the number of reads
        c1 = _format_table(c1)
        c2 = _format_table(c2)
        num_reads = int((c1.shape[0] / 16) - 1)

        return c1, c2, num_reads

    else:
        formatted_data = _format_table(raw_data)
        num_reads = int((formatted_data.shape[0] / 16) - 1)
        return formatted_data, num_reads
