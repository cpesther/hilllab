# Christopher Esther, Hill Lab, 11/13/2025
import pandas as pd
import numpy as np

from ..utilities.format_spectra_table import format_spectra_table

def _load_file(path, channels=2):

    """
    Loads and formats data from swelling experiments.
    """

    # Load the raw data from the weird, Excel-esque format
    raw_data = pd.read_csv(path, sep='\t', encoding='utf-16', lineterminator='\r', 
                           header=2, skipinitialspace=True)
    
    # Split the data into separate channels, if needed
    if channels == 2:
        c1 = raw_data.loc[:, [str(i) for i in range(1, 25)]].iloc[:-4]
        c2 = raw_data.loc[:, [str(i) for i in np.arange(1.1, 25.1)]].iloc[:-4]
        
        # Run this helper function on the data and calculate the number of reads
        c1 = format_spectra_table(c1)
        c2 = format_spectra_table(c2)
        num_reads = int((c1.shape[0] / 16) - 1)

        return c1, c2, num_reads

    else:
        formatted_data = format_spectra_table(raw_data)
        num_reads = int((formatted_data.shape[0] / 16) - 1)
        return formatted_data, num_reads
