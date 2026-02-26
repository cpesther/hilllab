# Christopher Esther, Hill Lab, 11/13/2025
import numpy as np
import math
from scipy.special import erfcinv
import pandas as pd

def remove_outliers(array=[], info=True, paste_mode=True, delimiter=None):
    
    """
    Removes outliers from an array of data. Outliers are defined as 
    being more than three scaled MADs away from the median. 
    
    ARGUMENTS:
        array (list): Array of data containing outliers
        paste_mode (bool): controls whether the function is run in a mode
            where data can be pasted directly from Excel.
        info (bool): Whether a print message should be displayed with
            information about the removed outliers. 
        delimiter (string): the value used for separating the data pasted 
            when paste_mode is set to True. This is only used if the function
            cannot regonize the delimiter automatically. 
    
    RETURNS:
        filtered_array (list): Array of values without outliers. 
        removed_values (list): Array of the removed outlier values. 
        removed_indices (list): Array of the indices of the outliers.
    """
    
    # Paste mode allows the user to paste data from Excel into an input box
    # which will be automatically formatted (assuming it's space delimited)
    # instad of having to type out the data or structure it into an comma
    # delimited array. 
    if paste_mode:
        print('Paste values in the field below.')
        input_values = input()
    
        if '\t' in input_values:
            split_values = np.array(input_values.split('\t'))
            format = 'row'
        elif ' ' in input_values:
            split_values = np.array(input_values.split(' '))
            format = 'column'
        elif delimiter is not None:
            split_values = np.array(input_values.split(delimiter))
            format = 'column'
        else:
            raise ValueError('Unknown file delimeter')

        # Check that the values got separated properly
        try:
            array = split_values.astype(float)
        except ValueError:
            print('ERROR: Unable to parse pasted values')
            return
    else:
        pass
    
    # Calculate the median absolute deviation and scale it
    mad = np.median(abs(array - np.median(array)))
    scale = -1 / (math.sqrt(2) * erfcinv(3/2))
    s_mad3 = (mad * scale) * 3
    median = np.median(array)
    
    # For every value in the array
    removed_values = []
    removed_indices = []
    filtered_array = []
    for index, value in enumerate(array):
        if abs(median - value) > s_mad3:
            removed_values.append(value)
            removed_indices.append(index)
        else:
            filtered_array.append(value)
    
    # Create the Excel paste data, if requested
    if paste_mode:
    
        # Replace the outliers with none values
        final = np.array(array)
        for index in removed_indices:
            final[index] = None
    
        # Create the copy dataframe based on the format argument
        if format == 'column':
            copy_df = pd.DataFrame({'values': final})
        else:
            copy_df = pd.DataFrame([final])
    
        copy_df.to_clipboard(excel=True, header=False, index=False)
    
    else:
        pass
    
    # Give some print outputs, if requested
    if info:
        print(f"{len(removed_values)} outliers removed.")
    else:
        pass
    return filtered_array, removed_values, removed_indices
