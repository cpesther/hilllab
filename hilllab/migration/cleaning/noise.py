# Christopher Esther, Hill Lab, 2/26/2026

def simple_shift(data):
    
    """
    Adjusts data to compensate for background noise/fluorescence by simply
    measuring the minimum intensity in the non-fluorescent regions and 
    reducing the values by that amount. 

    ARGUMENTS:
        data (list): the list of unshifted data points
    
    RETURNS:
        shifted_data (array): array of shifted data
    """
        
    # Find the minimum of the raw data in range 7 to 11
    noise_shift_value = min(data[7:11])
        
    # Shift the data by this amount
    shifted_data = data - abs(noise_shift_value)
    return shifted_data
