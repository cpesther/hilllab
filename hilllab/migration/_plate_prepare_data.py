# Christopher Esther, Hill Lab, 8/25/2025
import numpy as np
import pandas as pd

from ._plate_profile_curve import _plate_profile_curve
from .plate_export_bundle import plate_export_bundle
from ..utilities.print_progress_bar import print_progress_bar
from .plate_define_radii import plate_define_radii

def _plate_prepare_data(bundle, columns_include=None, columns_exclude=None, radius_nm=0, 
                       interval_minutes=15, delay_minutes=0, load_rate_minutes=1.5, 
                       temperature_K=297, method='individual', export=False, **kwargs):
    
    """
    Iterates over every curve in the dataset and adjusts the values
    to ensure accurate localization of the Gaussian peaks. 
    
    ARGUMENTS:
        bundle (migration.Bundle): the data bundle
        columns_include (list): indicates which columns should be 
            included in processing.
        columns_exclude (list): list of columns that should be exluded
            from processing. 
        radius_nm (float or list): radius of the probe in nanometers or
            list of radius for each selected column.
        temperature_K (float): temperature of the system in Kelvin.
        interval_minutes (int): number of minutes between each read
        delay_minutes (float): number of minutes after loading was 
            completed that measurement began.
        load_rate_minutes (float): the average number of minutes taken 
            to load each capillary. Defaults to 1.5.
        method (string): the way in which the adjustment(s)
            for the data should be determined based on the results from
            the profiling method. Options include 'average', 
            'consensus', 'individual', and 'manual'.
        export (bool): controls whether the data is exported to an Excel
            file after pre-processing.
    """

    # This is arguably one of if not the most important function in this
    # calculation process. Here we adjust the raw data so that it appears
    # in a consistent pattern that the fitting algorithm is expecting 
    # to see. This function is what replaces the need for human 
    # intervention that normally requires a subjective analysis of the
    # data in order to control the fit parameters. Since we're trying to
    # think like a human, this is a pretty long function.

    # This function also takes in all the remaining arguments to add to
    # the bundle, this way our bundle is now fully complete and can be 
    # run through any processing functions without the need for any 
    # additional inputs. Let's save those here. 
    bundle.data.interval_minutes = interval_minutes
    bundle.data.delay_minutes = delay_minutes
    bundle.data.load_rate_minutes = load_rate_minutes

    # <<<<< GETTING EVERYTHING SET UP >>>>>
    # Let's start by selecting which columns we'll be processing
    # Note that we're working with the numbers associated with the column
    # names here, not the column indices.
    all_column_numbers = np.arange(1, bundle.data.num_columns + 1)
    if columns_include and columns_exclude:
        print('ERROR: columns_include and columns_exclude cannot be used at the same time')
        print('       Please pass values to only one of these arguments')
        return
    
    elif columns_include:
        if len(columns_include) == 0:  # if none provided, include all
            selected_column_numbers = all_column_numbers
        else:
            selected_column_numbers = columns_include
    
    elif columns_exclude:  # remove excluded columns from all
        selected_column_numbers = np.setdiff1d(all_column_numbers, columns_exclude)
    
    else:
        print('ALERT: Invalid columns argument(s), processing all')
        selected_column_numbers = all_column_numbers

    # Now we'll take these column numbers and actually grab the full
    # names of the columns from the table itself.
    selected_column_indices = np.array(selected_column_numbers) - 1
    selected_columns = bundle.data.raw.columns.take(selected_column_indices)

    # Now use the radii definintion function to handle creating the radii values
    radii_nm = plate_define_radii(bundle=bundle, radius_nm=radius_nm)
    bundle.data.radii_nm = radii_nm  # save the radii to the bundle

    # <<<<< NORMALIZING THE DATA >>>>>
    # This normalized data is what is used in the peak profiling process 
    # since it is more standardized and less likely to cause issues due
    # to differences in the magnitude of the fluorescence intensity. 

    # A list for storing all of our normalized dataframes
    normalized_dfs = []
    for read in range(bundle.data.num_reads):  
        
        # Load this read’s raw data
        one_read_data = bundle._load_read(read_number=read, type="raw")
        print_progress_bar(progress=read, total=bundle.data.num_reads-1, title='Normalizing data')

        # Prepare container for normalized columns
        one_read_data_normalized = pd.DataFrame(index=one_read_data.index, columns=selected_columns)

        for column in selected_columns:
            one_column = one_read_data[column].to_numpy(dtype=float)
            max_value = one_column.max()

            # Normalize unless the column is empty
            one_column_norm = one_column if max_value == 0 else one_column / max_value

            # Compute percent differences in the back half (indices 8–15)
            percent_diffs = one_column_norm[8:16] / (one_column_norm[7:15] + 1e-9)
            above_threshold = np.where(percent_diffs > 100)[0] + 8

            if len(above_threshold) == 1:
                peak_index = above_threshold[0]
                # Replace peak with neighbor(s)
                if peak_index == len(one_column_norm) - 1:  # last point
                    one_column_norm[peak_index] = one_column_norm[peak_index - 1]
                else:
                    one_column_norm[peak_index] = (one_column_norm[peak_index - 1] 
                                                   + one_column_norm[peak_index + 1]) / 2

            elif len(above_threshold) > 1:
                one_column_norm[above_threshold] = one_column_norm.min()

            # Re-normalize after peak removal (skip if column was empty)
            if one_column_norm.max() > 0:
                one_column_norm /= one_column_norm.max()

            # Store normalized data
            one_read_data_normalized[column] = one_column_norm

        # Save this normalized df into the main array
        normalized_dfs.append(one_read_data_normalized)

    print('\nData normalization complete')

    # Once fininshed iterating over each read, combine all the dfs and save
    bundle.data.normalized = pd.concat(normalized_dfs, ignore_index=True)
    bundle.data.normalized.index = bundle.data.raw.index

    # <<<<< GENERATING THE AVERAGE CURVES >>>>>
    # Generate a curve that represents the average of each column across
    # all reads. This average data may be used in several steps, so 
    # we'll go ahead and calculate it here first.
    bundle.data.average = pd.DataFrame(columns=bundle.data.normalized.columns)
    for column in selected_columns:
    
        # Reshape the data into each read (groups of 16 rows)
        all_reads = bundle.data.normalized[column].to_numpy().reshape(-1, 16)
    
        # Calculate the mean of every read to get an average curve
        average_curve = np.mean(all_reads, axis=0)

        # Store this average curve to a table for future reference
        bundle.data.average[column] = average_curve

    # <<<<< PERFORM CURVE PROFILING >>>>>
    # Now we can perform profiling using the requested method

    # The average method performs the profiling on the average curve. It
    # is very fast and works on consistent datasets, but is unreliable
    # on data with more variation. 
    if method == 'average':
        
        # Generate a composite (average) curve of each read for every column
        for column in bundle.data.average:
        
            # Pull the raw data
            one_average_curve = bundle.data.average[column].to_numpy()

            # Run the localization calculations 
            peak_location, gaussian_end = _plate_profile_curve(values=one_average_curve)

            # Save the results to the raw peaks table
            peaks_array = np.repeat(peak_location, bundle.data.num_reads)
            ends_array = np.repeat(gaussian_end, bundle.data.num_reads)
            bundle.data.peaks_raw[column] = peaks_array
            bundle.data.ranges_raw[column] = ends_array
    
            # And just copy the raw profile values over to the final dfs 
            # since no further adjustment is needed
            bundle.data.peaks_final = bundle.data.peaks_raw
            bundle.data.ranges_final = bundle.data.ranges_raw

    # Both consensus and individual methods require that we profile each
    # curve in the dataset. For indiviual method, we just use those raw
    # profile values for each curve individually, whereas in consensus
    # we take a vote on which values are the best for each column.
    elif method == 'consensus' or method == 'individual':
    
        # Since these methods append rows to the profiling tables, we 
        # need to go ahead and add the column labels before starting.
        bundle.data.peaks_raw = pd.DataFrame(columns=selected_columns)
        bundle.data.ranges_raw = pd.DataFrame(columns=selected_columns)
        
        # Calculate the profile for each curve
        for read in range(bundle.data.num_reads):
        
            # Pull that read's data from the main dataframe and set up some 
            # lists to store the results
            print_progress_bar(progress=read, total=bundle.data.num_reads-1, title='Localizing data  ')
            one_read_data = bundle._load_read(read_number=read, type='normalized')
            one_column_peaks = []
            one_column_ranges = []
        
            # For each read in that column
            for column in selected_columns:
        
                # Pull the data and fit it using the chosen method
                one_curve = one_read_data[column].to_numpy()

                # Run the localization calculations 
                peak_index, end_index = _plate_profile_curve(values=one_curve)
            
                # Append the decision and probabiltiy to the array
                one_column_peaks.append(peak_index)
                one_column_ranges.append(end_index)
        
            # Append the results arrays (rows) to the main dataframes
            bundle.data.peaks_raw.loc[len(bundle.data.peaks_raw)] = one_column_peaks
            bundle.data.ranges_raw.loc[len(bundle.data.ranges_raw)] = one_column_ranges
        
        # If we're using the consensus method
        if method == 'consensus':
        
            # Take a 'vote' for the most common profile in each column
            for column in bundle.data.peaks_raw.columns:
            
                # Count the number of unique values in the array
                p_unique, p_counts = np.unique(bundle.data.peaks_raw[column], return_counts=True)
                r_unique, r_counts = np.unique(bundle.data.ranges_raw[column], return_counts=True)

                # Find the most frequent value and add it to the master table
                p_most_frequent_value = np.unique[np.argmax(p_counts)]
                profiles_array = np.repeat(p_most_frequent_value, bundle.data.num_reads)
                r_most_frequent_value = np.unique[np.argmax(r_counts)]
                ranges_array = np.repeat(r_most_frequent_value, bundle.data.num_reads)
                
                bundle.data.peaks_final[column] = profiles_array
                bundle.data.ranges_final[column] = ranges_array
        
        # Otherwise if we're using the individual method
        else:
            # We can just copy over the raw values to the final ones
            bundle.data.peaks_final = bundle.data.peaks_raw
            bundle.data.ranges_final = bundle.data.ranges_raw

    # If some other argument was given for peak_method
    else:
        print("ERROR: An unknown value for 'method' was provided")
        return
    
    print('\nData profiling complete')

    # Now that the data has been profiled (peak only, Gaussain range 
    # profiling comes later), we can actually make adjustments
    # based on these saved profiles. We will first define some functions
    # that will be used to make the necessary changes. Here's a generic 
    # function that can be used to move an array of data when given the 
    # location of its peak.
    
    def move_peak(curve_data, peak_index):
        
        """
        Adjusts one curve of data based on the provided peak_index so 
        the peak is located in the appropriate location (first index). 
    
        ARGUMENTS:
            data (list): the array of unshifted data
            peak_index (int): the amount that the data should be shifted
                as given by the profile number
        
        RETURNS:
            moved_array (array): array of shifted data
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
            mirrored_array = np.insert(curve_data, 0, curve_data[1])
            moved_curve_data = mirrored_array[:-1]

        # If no shift is needed
        elif shift == 0:
            moved_curve_data = curve_data
            
        # Here's the right shifts
        elif shift < 1:
            # Drop first value(s) and repeat last value(s)
            moved_curve_data = np.append(curve_data[-shift:], curve_data[shift:])
    
        # If shift equals anything else (including 0) don't shift the data
        else:
            moved_curve_data = curve_data
        
        return moved_curve_data
    
    # And we'll also define a function that can apply a noise shift 
    def noise_shift(curve_data):
    
        """
        Adjusts data to compensate for background noise/fluorescence
    
        ARGUMENTS:
            array (array): the array of unshifted data
        
        RETURNS:
            shifted_array (array): array of shifted data
        """
            
        # Find the minimum of the raw data in range 7 to 11
        noise_shift_value = min(curve_data[7:11])
            
        # Shift the data by this amount
        shifted_array = curve_data - abs(noise_shift_value)
        return shifted_array
        
    # Now that we have some generic functions to adjust the data, we will
    # iterate through each read of the raw data, make adjustments using
    # the values in the peak profiles table, and store the cleaned data 
    # to the data.clean dataframe. During this process, since were going
    # through all of the work to access the data iteratively, we'll go 
    # ahead and perform Gaussian localization on each curve. The function
    # defined below will do that for us. 
    
    # A list for storing all of our clean dataframes
    clean_dfs = []
    
    # For every read in the raw data
    for read in range(bundle.data.num_reads):
    
        # Pull the data from that read
        print_progress_bar(progress=read, total=bundle.data.num_reads-1, title='Cleaning data   ')
        one_read_data = bundle._load_read(read_number=read, type='raw')
        one_read_data_cleaned = pd.DataFrame(columns=selected_columns)
    
        # For each column in the data
        for column in selected_columns:
    
            # Pull that column of data and its peak location
            one_array = one_read_data[column].to_numpy().astype(float)
            peak_location = bundle.data.peaks_final.at[read, column]
    
            # Run the move_peak and noise_shift function on the data
            moved_array = move_peak(one_array, peak_location)
            cleaned_array = noise_shift(moved_array)

            # Make sure the data has no negative values, shift if needed
            if any(value < 0 for value in cleaned_array):
                # Find that value and add its abs to all values
                finished_array = cleaned_array + (abs(min(cleaned_array)))
            else:
                finished_array = cleaned_array

            # Add the cleaned column into the read df
            one_read_data_cleaned[column] = finished_array

        # Append the entire df into the list
        clean_dfs.append(one_read_data_cleaned)

    # Once fininshed iterating over each read, combine all the dfs and save
    bundle.data.clean = pd.concat(clean_dfs, ignore_index=True)
    bundle.data.clean.index = bundle.data.raw.index
    
    print('\nData preparation complete')

    # Export the bundle
    plate_export_bundle(bundle=bundle)
    
    return bundle
