# Christopher Esther, Hill Lab, 11/13/2025

def _access_read(read_number, channel_table):

    """
    A generic helper function to access data based on its read numbers.
    """

    # Calculate the indices in the main dataframe for the start and end 
    # of the requested read
    read_start_index = int(read_number * 16)
    read_end_index = int(read_start_index + 16)
    
    # Pull and return read from the specified table
    return channel_table[read_start_index:read_end_index]
    