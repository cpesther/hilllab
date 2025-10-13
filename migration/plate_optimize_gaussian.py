# Christopher Esther, Hill Lab, 8/25/2025
import numpy as np
import pandas as pd
from scipy.optimize import minimize
import matplotlib.pyplot as plt

from ._plate_calculate_gaussian import _plate_calculate_gaussian

def plate_optimize_gaussian(bundle=None, column=None, read=None, curve=None, end_index=6,
                            interval_minutes=15, load_rate_minutes=1.5, delay_minutes=0, radius_nm=1, temperature_K=297,
                            plot_fit=False):
    
    """
    Optimizes the _plate_calculate_gaussian_curve function to find the 
    best-fit parameters (A and Dt) for the requested curve. Then
    calculates and returns the Dt, D, and eta values. This function
    can also be manually provided data (not as a part of a bundle).
        
    ARGUMENTS:
        bundle (migration.Bunlde): the data bundle
        read (int): the number of the read to process
        column (string): the name of the column to process

    RETURNS:
        results (dict): a dictionary with a variety of results values.
    """

    # Depending on whether we're running this function using a bundle
    # or manually provided arguments, we will define some key variables
    # slightly differently. 

    # If a curve was provided manually, we'll use all the provided args
    if curve is not None:
        curve = pd.Series(curve)
        column_number = 0

    # Otherwise pull the arguments from the bundle
    else:
        one_read = bundle._load_read(read_number=read, type='clean')
        curve = one_read[column]
        end_index = bundle.data.ranges_final.at[read, column]
        interval_minutes = bundle.data.interval_minutes
        column_number = bundle.data.clean.columns.get_loc(column)
        load_rate_minutes = bundle.data.load_rate_minutes
        delay_minutes = bundle.data.delay_minutes
        radius_nm = bundle.data.radii_nm[column]
        temperature_K = bundle.data.temperature_K

    # Now let's set up our guesses for each parameter and their 
    # respective bounds. We'll start with A, the curve's peak.
    A_guess = curve.iloc[1]  # simple enough
    A_drift = 0.05  # allow the peak to drift 5% up or down
    A_lo_bound = A_guess * (1 - A_drift)
    A_hi_bound = A_guess * (1 + A_drift)

    # And now the Dt guess bounds. These values are somewhat arbitrary 
    # but work well. Note that Dt scales with x², not just x. 
    Dt_guess = 1e-6
    Dt_lo_bound = 1e-9
    Dt_hi_bound = 1e-1

    # Pack up all of the guess values and bounds for optimization
    guess_values = [A_guess, Dt_guess]
    bounds = [(A_lo_bound, A_hi_bound), (Dt_lo_bound, Dt_hi_bound)]
    
    # Here's the actual optimization of the Gaussian curve
    result = minimize(_plate_calculate_gaussian, 
                          options={"disp": False}, 
                          args=(curve, end_index), 
                          x0=guess_values,
                          method='L-BFGS-B',
                          bounds=bounds)
    
    # Pull results from optimization
    optimization_results = result.x  # optimized Gaussian values
    best_A = optimization_results[0]
    best_Dt = optimization_results[1]
    best_nrmse = result.fun  # the function result (the error)
    
    # Calculate the fit curve using these values
    params = (best_A, best_Dt)
    _, fit_curve = _plate_calculate_gaussian(params=params, curve=curve, end_index=end_index,
                                             return_fit=True)

    # Now that we have these optimized results, let's calculate some
    # diffusion and viscosity values.

    # Calculate the time value while accounting for the load rate and 
    # any added delay
    raw_time = read * interval_minutes
    load_rate_minutes = column_number * load_rate_minutes
    time_minutes = raw_time + load_rate_minutes + delay_minutes
    time_seconds = time_minutes * 60
        
    # Calculate our eta and D values
    # At the zero timepoint, return a zero
    if best_Dt == 0 or time_seconds == 0:
        D = 0  # in m²/s
        viscosity_Pas = 0  # in Pascal seconds
    else:
        # Diffusion coefficient (m²/s)
        D = best_Dt / time_seconds

        # Stokes-Einstein viscosity (Pa·s)
        boltzmann = 1.380649e-23  # Boltzmann constant
        radius_m = radius_nm * 1e-9
        viscosity_Pas = (boltzmann * temperature_K) / (6 * np.pi * radius_m * D)

    # Convert viscosity to milli-Pascal·seconds for reporting
    viscosity_mPas = viscosity_Pas * 1000

    # Create a dictionary with which we return the results
    results = {
        'eta (mPa•s)': viscosity_mPas,
        'Dt (m²)': best_Dt,
        'D (m²/s)': D,
        'NRMSE': best_nrmse,
        'Peak': best_A
    }
    
    # If a plot of the fit was requested
    if plot_fit:
        plt.plot(curve, label='Raw Data')
        plt.plot(fit_curve, label='Best Fit')
        plt.legend()

    return results