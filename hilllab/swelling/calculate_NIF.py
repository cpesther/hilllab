# Christopher Esther, Hill Lab, 11/13/2025
import numpy as np
from ..swelling._access_read import _access_read
from scipy import integrate
import pandas as pd

from ..utilities.print_progress_bar import print_progress_bar

def calculate_NIF(channel_data, num_reads):

    """
    Calculates the normalized integrated fluorescence (NIF) for each sample
    in a two-channel swelling assay. 

    ARGUMENTS:
        channel_data (pd.DataFrame): the dataframe containing the data
            to be analyzed. 

    RETURNS:
        integrals_df (pd.DataFrame): dataframe with the integrals of the
            fluorescence curve at each timepoint. 
    """
    
    # The x distances along the capillary, in mm
    x_distances = np.arange(0, 70, 4.5)
    integrals = []  # and a list to store all integrals
    
    # Iterate over every read
    for read in range(1, num_reads):
        
        # Print a progress bar
        print_progress_bar(progress=read+1, total=num_reads, title='Calculating integrals')

        # Load the data
        read_data = _access_read(read, channel_data)
        one_read_integrals = []  # an array to store this read's integrals
        
        # Iterate overy each column in this read
        for i in range(1, 25):
    
            # Pull the column's data and calculate the integral
            column_data = np.array(read_data[f'Column {i}'])
            one_integral = integrate.simpson(y=column_data, x=x_distances)
            one_read_integrals.append(one_integral)
    
        # Append this read's integrals onto the main array
        integrals.append(one_read_integrals)
    
    # Format it into a datagram
    integrals_df = pd.DataFrame(integrals)
    integrals_df.columns = channel_data.columns
    
    return integrals_df
