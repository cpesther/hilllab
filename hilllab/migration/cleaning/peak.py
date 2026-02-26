# Christopher Esther, Hill Lab, 2/26/2026
import numpy as np

def move_peak(data, peak_index):
        
        """
        Adjusts one curve of data based on the provided peak_index so 
        the peak is located in the appropriate location (first index). 
    
        ARGUMENTS:
            data (list): the array of unshifted data
            peak_index (int): the amount that the data should be shifted
                as given by the profile number
        
        RETURNS:
            moved_data (list): array of shifted data
        """
    
        # Begin by converting the peak location (aka the profile number)
        # into a value indicating how much and in which direction we need
        # to shift the data
    
        if peak_index <= 4:
            shift = (-1 * peak_index) + 1
    
        # A peak location of 5 indicates an empty column, so no shifting is needed
        elif peak_index == 5:
            shift = 0

        # If we get some other value for peak, just don't shift
        else:
            shift = 0

        # Perform the various shifts on the data
        # Mirror the 1 index value to create a peak and remove the last
        if shift == 1:
            mirrored_array = np.insert(data, 0, data[1])
            moved_data = mirrored_array[:-1]

        # If no shift is needed
        elif shift == 0:
            moved_data = data
            
        # Here's the right shifts
        elif shift < 1:
            # Drop first value(s) and repeat last value(s)
            moved_data = np.append(data[-shift:], data[shift:])
    
        # If shift equals anything else (including 0) don't shift the data
        else:
            moved_data = data
        
        return moved_data