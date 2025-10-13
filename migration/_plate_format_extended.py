# Christopher Esther, Hill Lab, 8/21/2025
import numpy as np
import pandas as pd

def _plate_format_extended(input_data, num_reads):
    
    """
    A backend function that adjusts the loaded_data table into an 
    extended format, which takes the four extra rows at the bottom of
    the well plate and turns them into two additional columns each, with 
    the outside edges of each row being the top of the columns. 

    ARGUMENTS:
        input_data (pandas.DataFrame): the dataframe containing the 
            raw data. 

    RETURNS:
        extended (pandas.DataFrame): the dataframe reformatted with
            the bottom four rows formatted as eight additional columns.
    """

    # This list will store a bunch of dataframes for each extended read
    # so that we can concat them to the main df all at once
    extended_read_dfs = []

    # Now we'll run through each read and separate out the columns
    for read_number in range(num_reads):

        # Calculate the indices of this read and pull it
        read_start_index = int(read_number * 16)
        read_end_index = int(read_start_index + 16)
        one_read = input_data[read_start_index:read_end_index]

        # We'll address columns 1 through 24 first
        one_read_as_array = one_read.to_numpy()  # convert to array
        trimmed = one_read_as_array[:-4, :]  # drop last 4 rows
        padding = np.zeros((4, one_read_as_array.shape[1]))  # create 4 rows of zeros
        extended = np.vstack([trimmed, padding])  # stack them back together
        one_extended_read = pd.DataFrame(extended, columns=one_read.columns)  # rebuild
        
        # With the first 24 columns saved, we can now add in the extended
        # 8 sourced from the last four rows (two per row).
        rows = ['M', 'N', 'O', 'P']  # last 4 rows
        for i, row in enumerate(rows, start=25):  # start column numbering at 25
            values = one_read.loc[row].to_numpy()

            # Left slot = first 12 values + 4 zeros
            left_slot = np.r_[values[:12], np.zeros(4)]

            # Right slot = reversed last 12 values + 4 zeros
            right_slot = np.r_[values[12:][::-1], np.zeros(4)]

            # Assign new columns
            one_extended_read[f'Column {i}'] = left_slot
            one_extended_read[f'Column {i+4}'] = right_slot

        # Now sort the read table so that the columns are in ascending order
        one_extended_read = one_extended_read[sorted(one_extended_read.columns, 
            key=lambda x: int(x.split()[1]))]
    
        # Append this extended read to the list
        extended_read_dfs.append(one_extended_read)
    
    # With all of the individual extended dataframes created for each 
    # read, now all that we have to do is update the column names and 
    # concat them all together. 
    extended = pd.concat(extended_read_dfs, ignore_index=True).set_index(input_data.index)

    return extended
