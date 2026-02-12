# Christopher Esther, Hill Lab, 8/29/2025
import pandas as pd

from .plate_optimize_gaussian import plate_optimize_gaussian
from ._plate_load_wrapper import _plate_load_wrapper

def plate_endpoint_calculation(hours=0, minutes=0, path=None, bundle=None, data_type='SPE', 
                               nested=False, read=0, **kwargs):
    
    """
    Calculates the best fit Gaussain curve and associated values
    for the data in one read. 
    
    ARGUMENTS:
        hours (float): number of hours in the desired timepoint
        minutes (int): number of minutes in the desired timepoint
        path (str): path to the file to be loaded
        bundle (migration.Bundle): The data bundle to be used if not
            loading from a path. 
        data_type (string): Specifies the type model used to collect the 
            data. Options include 'SPE' (default), 'TEC', and 'PRE'.
        nested (bool): indicates whether this function is being run from 
            within the plate_kinetic_calculation() function. This affects
            some minor data handling decisions. 
        read (int): used only when nested in the plate_kinetic_calculation()
            function to manually provide read numbers instead of calculating 
            them based on given time values.
            
    RETURNS:
        final_df (pd.DataFrame): table with calculation results
    """
    
    # First thing we need to do is load the data and pass down all of 
    # the important arguments if a bundle wasn't provided
    if bundle is None:
        bundle = _plate_load_wrapper(path, data_type=data_type, **kwargs)

    if bundle is None and path is None:
        print('ERROR: You must provide either a path or a bundle')
    
    # Check that the timepoint requested is a multiple of the interval
    if ((hours * 60) + minutes) % bundle.data.interval_minutes != 0:
        print('ERROR: The requested timepoint must be a multiple of the interval')
        return    
    
    # Now we'll pull the data from the requested read. If the function is
    # running in nested mode, the read number is provided and needn't be calculated
    if nested:
        read_number = read
        base_minutes = read_number * bundle.data.interval_minutes
    else:
        base_minutes = (hours * 60) + minutes
        read_number = (base_minutes / bundle.data.interval_minutes) - 1  # -1 for 0-based index

    # Note: the base_minutes argument represents the number of minutes 
    # of measurement in the first column. Delay and load rate compensation
    # will be applied in a later function. 
        
    # Check that the read number actually exists
    if read_number > bundle.data.num_reads - 1:  # -1 for 0-based index
        print('ERROR: The requested timepoint is beyond what exists in the data!')
        return

    # Create a table with the data from the specified timepiont
    one_read_data = bundle._load_read(read_number=read_number)
    
    # Create a dataframe to store and display the results
    results_df = pd.DataFrame(columns=['<>', 'Viscosity (mPa•s)',
                                   'Dt', 'D (m²/s)', 'NRMSE', 'Peak'])

    # Iterate through every column in this one_read_data 
    results_df = pd.DataFrame()
    for column in one_read_data.columns:

        # Perform calculation on this column
        column_results = plate_optimize_gaussian(bundle=bundle, column=column, read=read_number)

        # Add results to display df
        results_df[column] = column_results

    # If nested, we don't need any print statements
    if nested:
        return results_df
    
    # If run in isolation, format things a bit nicer
    else:
        print(f'Results (read {int(read_number + 1)}/{int(bundle.data.num_reads)})')
        print(results_df)
        print('Table copied to clipboard')
        results_df.to_clipboard(excel=True)
        return results_df
