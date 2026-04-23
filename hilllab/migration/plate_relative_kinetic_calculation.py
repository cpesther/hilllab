# Christopher Esther, Hill Lab, 4/20/2026
import numpy as np
import pandas as pd

from .plate_kinetic_calculation import plate_kinetic_calculation
from ..utilities.print_progress_bar import print_progress_bar
from .stokes_einstein import eta
from ..utilities.remove_outliers import remove_outliers

def plate_relative_kinetic_calculation(path=None, bundle=None, data_type='SPE', 
                                       read_gap=30, **kwargs):

    """
    Calculates the best fit Gaussain curve and associated values
    for every read in the data.
    
    ARGUMENTS:
        path (str): path to the file to be loaded
        bundle (migration.Bundle): The data bundle to be used if not
            loading from a path. 
        data_type (string): Specifies the type model used to collect the 
            data. Options include 'SPE' (default), 'TEC', and 'PRE'.
        read_gap (int): the minimum number of reads by which two set of
            data must be separated to be included in the relative 
            calculations. 
            
    RETURNS:
        eta_results (pd.DataFrame): dataframe containing the calculated 
            eta value for each column
        all_eta_values (list): a list of 2D arrays containing every 
            calculated eta value (at each relative point) for every column. 
    """

    # First step is to run the basic kinetic calculation
    results = plate_kinetic_calculation(path=path, bundle=bundle, data_type=data_type, **kwargs)

    # Set up a couple things before iteration
    all_eta_means = []
    all_columns = results.data.clean.columns
    n_reads = results.data.num_reads
    all_eta_values = []

    # Iterate over each column
    for i, column in enumerate(all_columns):

        # Print progress bar
        print_progress_bar(progress=i+1, total=len(all_columns), title='Performing relative calculations')

        # 2D array for storing all relative viscosities
        eta_values = np.full((n_reads, n_reads), np.nan)
        radius_nm = results.data.radii_nm[column]

        # Iterate for each read as read 1 (r1)
        for r1 in range(n_reads):

            # And iterate with each read as read 2 (r2)
            for r2 in range(n_reads):

                # Don't do relative calculations between identical reads
                if r1 == r2:
                    continue

                # Get the Dt values
                Dt1 = results.results.plate_Dt[column][r1]
                Dt2 = results.results.plate_Dt[column][r2]
                
                # Calculate timepoints in seconds
                t1 = r1 * results.data.interval_minutes * 60
                t2 = r2 * results.data.interval_minutes * 60
                
                # Calculate D between the two reads
                D_value = (Dt2 - Dt1) / (2 * (t2 - t1))
                
                # Calculate eta
                eta_value = eta(temperature_K=297, D_m2s=D_value, radius_nm=radius_nm)
            
                # Save the results
                if abs(r2 - r1) > read_gap:
                    eta_values[r1][r2] = eta_value

        # Flatten, remove nans, and drop negative values
        flat = eta_values.flatten()
        clean = flat[~np.isnan(flat)]
        trimmed = clean[clean > 0]

        # Remove outliers from the trimmed data
        final_data, _, _ = remove_outliers(trimmed, paste_mode=False, info=False)
        final_data = np.array(final_data)

        # Save mean value to array
        all_eta_means.append(np.mean(final_data))

        # Save the 2D eta values array to the list 
        all_eta_values.append(eta_values)

    # Format all eta values into data frame
    eta_results = pd.DataFrame([all_eta_means], columns=np.array(results.data.clean.columns))
    return eta_results, all_eta_values
