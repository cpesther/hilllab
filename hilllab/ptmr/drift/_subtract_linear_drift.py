# Christopher Esther, Hill Lab, 1/12/2026
import numpy as np
import pandas as pd

def _subtract_linear_drift(data, drift_start_time=None, drift_end_time=None):

    """
    Remove linear drift from 3D bead tracking data.

    For each bead in the dataset, this function fits a linear trend 
    (drift) to its X and Y positions over the specified time window, and 
    then subtracts that trend from the bead's trajectory. 

    ARGUMENTS:
        data (pandas.DataFrame): the data from the VRPN. Must be run through
            the _format_vrpn function first.
        drift_start_time (float): start time for computing drift (seconds). 
            Only frames at or after this time are included in the drift fit.
        drift_end_time (float): snd time for computing drift (seconds). 
            Only frames at or before this time are included in the drift fit.

    RETURNS:
        cleaned_data (pandas.DataFrame): the data from the VRPN with
            the X and Y columns replaced by the cleaned, drift subtracted
            data. 
        
    NOTES:
        1. Beads with fewer than three frames in the specified time window 
        are skipped.
        2. Drift is removed independently for each bead.
        3. This method assumes that drift is approximately linear over 
        the chosen time range. For non-linear drift, other methods 
        (e.g., center-of-mass) may be more appropriate.
    """

    # If there are no beads in this data, simply return the empty table
    if data.shape[0] == 0:
        return data

    # Get unique particle IDs from the data so we can iterate on them
    unique_ids = np.unique(data['particle_id'])

    # A list for storing dataframes with the drift corrected data. They'll
    # be concatenated at the end of the function. 
    clean_bead_dfs = []

    # Iterate over each bead in this data
    for bead_id in unique_ids:
        
        # Grab just the data for this bead from the main table
        bead_data = data[data['particle_id'] == bead_id]

        # Shift time so first timestamp is zero.
        # This does not change the drift slope, but it makes the linear fit's 
        # intercept correspond to the bead's starting position. Without this, 
        # subtracting the fit would introduce an artificial offset and shift 
        # the entire trajectory.
        t = bead_data['timestamp']
        t0 = t.iloc[0]
        t = t - t0  # this is the time array that we'll use now

        # Find the indices of the rows inside the provided drift time window
        time_mask = (t >= (drift_start_time - t0)) & (t <= (drift_end_time - t0))
        drift_indices = np.where(time_mask)[0]

        # Make sure there are at least two points left for the linear regression
        if len(drift_indices) <= 2:
            continue  # skip if less than two

        # Extract the timestamp and X and Y coordinate data only within the 
        # calculated drift indices
        drift_start_index = drift_indices[0]
        drift_end_index = drift_indices[-1] + 1
        x_data = bead_data['x'][drift_start_index:drift_end_index]
        y_data = bead_data['y'][drift_start_index:drift_end_index]
        t_data = t[drift_start_index:drift_end_index]
        
        # Fit a linear regression to X and Y coordinates. The polyfit runtion
        # returns the slope and intercept of the linear curve.
        fit_x = np.polyfit(t_data, x_data, 1)
        fit_y = np.polyfit(t_data, y_data, 1)

        # Now we'll take this linear fit and subtract it from the coordinate data
        x_clean = x_data - np.polyval(fit_x, t_data) + fit_x[1]
        y_clean = y_data - np.polyval(fit_y, t_data) + fit_y[1]

        # Save these clean coordinates to a new dataframe and append that
        # dataframe to the main list
        clean_bead_data = bead_data.copy()      # make a copy of the bead data
        clean_bead_data['x'] = x_clean          # replcae the X and Y data
        clean_bead_data['y'] = y_clean
        clean_bead_dfs.append(clean_bead_data)  # save to list

    # Once every bead has been cleaned, combine all the data back together
    if len(clean_bead_data) == 1:
        return clean_bead_data[0]
    elif len(clean_bead_data) == 0:
        return data
    else:
        return pd.concat(clean_bead_dfs, ignore_index=True)
