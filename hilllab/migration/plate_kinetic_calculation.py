# Christopher Esther, Hill Lab, 9/11/2025
import numpy as np
import pandas as pd

from ._plate_load_wrapper import _plate_load_wrapper
from .plate_endpoint_calculation import plate_endpoint_calculation
from ..utilities.print_progress_bar import print_progress_bar


def plate_kinetic_calculation(path=None, bundle=None, data_type='SPE', **kwargs):
    
    """
    Calculates the best fit Gaussain curve and associated values
    for every read in the data. 
    
    ARGUMENTS:
        path (str): path to the file to be loaded
        bundle (migration.Bundle): The data bundle to be used if not
            loading from a path. 
        data_type (string): Specifies the type model used to collect the 
            data. Options include 'SPE' (default), 'TEC', and 'PRE'.
            
    RETURNS:
        final_df (pd.DataFrame): table with calculation results
    """
    
    # First thing we need to do is load the data and pass down all of 
    # the important arguments if a bundle wasn't provided
    if bundle is None:
        bundle = _plate_load_wrapper(path, data_type=data_type, **kwargs)

    if bundle is None and path is None:
        print('ERROR: You must provide either a path or a bundle')

    # Generate an array of read numbers
    all_read_numbers = np.arange(0, bundle.data.num_reads, 1)

    # This is used for mapping the names of the results rows from the endpoint
    # calculation to the names of the results tables in the bundle. 
    table_map = {
        'plate_eta': 'eta (mPa•s)',
        'plate_Dt': 'Dt (m²)',
        'plate_D': 'D (m²/s)',
        'plate_nrmse': 'NRMSE',
        'plate_peak': 'Peak'
    }

    # Initialize the results tables with the column names
    for table, key in table_map.items():
        setattr(bundle.results, table, pd.DataFrame(columns=bundle.data.clean.columns))

    # Run the calculations of each of those read numbers
    for read_number in all_read_numbers:
        
        # Run the endpoint calculation on the timepoint
        print_progress_bar(progress=read_number, total=max(all_read_numbers), title='Calculating fits')
        endpoint_results = plate_endpoint_calculation(bundle=bundle, read=read_number, nested=True)

        # Map the results from the endpoint calculation into the bundle results
        for table, key in table_map.items():
            getattr(bundle.results, table).loc[len(getattr(bundle.results, table))] = endpoint_results.loc[key]

    return bundle

