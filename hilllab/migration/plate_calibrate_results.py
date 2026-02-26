# Christopher Esther, Hill Lab, 2/26/2026
import numpy as np
import pandas as pd

from .plate_extract_result import plate_extract_result
from ..utilities.remove_outliers import remove_outliers
from .stokes_einstein import r, D, eta
from ..utilities.warning import warn

def plate_calibrate_results(bundle):

    """
    Calibrates the results in a bundle given the radii and calibration
    columns dictionaries.

    ARGUMENTS:
        bundle (migration.Bundle): the bundle containing the results 
            that should be calibrated. 

    RETURNS:
        bundle (migration.Bundle): the same bundle with the calibrated
            results.
    """

    # Pull the calibration columns from the bundle
    calibration_columns = bundle.data.calibration_columns

    # Calibration is calculated on each individual radii value, so we'll go
    # though all calibration columns and calculate the new, calibrated radii
    # value for the old radii value, then average and apply them later.
    all_calibrated_radii = {}
    for column in calibration_columns.keys():

        # Extract the mean D value of the data in this column
        mean_D_value = plate_extract_result(bundle=bundle, column=column, table='D', 
                                            value='mean', end_only=True, end_hours=8)

        # Extract the expected eta value of this column
        expected_eta = calibration_columns[column]

        # Based on this D value, calculate the radius that would lead to the expected eta
        one_calibrated_radius = r(temperature_K=bundle.data.temperature_K, D_m2s=mean_D_value, 
                                eta_mPas=expected_eta)

        # Verify that this actual radius value has been created in the dict
        actual_radius = bundle.data.radii_nm[f'Column {column}']
        try:
            all_calibrated_radii[actual_radius]
        except KeyError:  # and create if not
            all_calibrated_radii[actual_radius] = []

        # Save this calibrated radius keyed by the actual radius
        all_calibrated_radii[actual_radius].append(one_calibrated_radius)

    # Now that we've calibrated the radius for (presumably) multiple columns
    # of the same radius we'll clean them and calculate the mean
    for actual_radius in all_calibrated_radii.keys():

        # Remove any outliers from the calibrated radii
        unclean_calibrated = all_calibrated_radii[actual_radius]
        cleaned_calibrated, _, _ = remove_outliers(array=unclean_calibrated, paste_mode=False, info=False)

        # Calculate the mean of these cleaned values as the final calibrated radius
        calibrated_radius = np.mean(cleaned_calibrated)

        # Save these results to the bundle
        bundle.results.radii_nm_calib[actual_radius] = calibrated_radius

    # Create a dict where we can search for column values by the radius
    # (instead of the other way around, which is how its typically stored.)
    columns_by_radii = {}

    # Create arrays in dict for every unique radius value
    for radius in np.unique(list(bundle.data.radii_nm.values())):
        columns_by_radii[radius] = []

    # Go through each column and populate the dict
    for column in bundle.data.radii_nm.keys():
        radius = bundle.data.radii_nm[column]
        columns_by_radii[radius].append(column)

    # Now that the radii have been calibrated, we can apply these calibrations 
    # to the actual data
    calibrated_eta_dfs = []
    calibrated_D_dfs = []

    # For each radius (since calibration is calculated individually for each radius value)
    for actual_radius in bundle.results.radii_nm_calib.keys():

        # Pull the results columns which use this radius
        uncalibrated_eta = bundle.results.plate_eta[columns_by_radii[actual_radius]]
        uncalibrated_D = bundle.results.plate_D[columns_by_radii[actual_radius]]

        # Pull the calibrated radius
        calibrated_radius = bundle.results.radii_nm_calib[actual_radius]

        # Now we can take this normalized radii value and recalculate the eta and D tables with it
        one_calibrated_eta = uncalibrated_D.map(lambda D_m2s: eta(bundle.data.temperature_K, D_m2s, calibrated_radius))
        one_calibrated_D = uncalibrated_eta.map(lambda eta_mPas: D(bundle.data.temperature_K, eta_mPas, calibrated_radius))

        # Save the calibrated dataframes to the list
        calibrated_eta_dfs.append(one_calibrated_eta)
        calibrated_D_dfs.append(one_calibrated_D)

    # Join all the dataframes back together
    calibrated_eta = pd.concat(calibrated_eta_dfs, axis=1)
    calibrated_D = pd.concat(calibrated_D_dfs, axis=1)

    # And save these calibrated dataframes into the bundle
    bundle.results.plate_eta_calib = calibrated_eta
    bundle.results.plate_D_calib = calibrated_D

    # Check for any columns that were not calibrated since there wasn't a 
    # calibration column with a matching radius.
    radii_values = np.unique(list(bundle.data.radii_nm.values()))
    calib_radii_values = list(all_calibrated_radii.keys())
    non_calibrated_columns = [r for r in radii_values if r not in calib_radii_values]

    # Send warning if any columns were not calibrated
    if len(non_calibrated_columns) > 0:
        msg = f"Column(s) {', '.join([str(c) for c in non_calibrated_columns])} were not calibrated " \
            "since there was no calibration column with a matching radius"
        warn(msg=msg)

    # Print a final message
    print('Calibration successful!')

    return bundle
