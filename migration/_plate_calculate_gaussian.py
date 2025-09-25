# Christopher Esther, Hill Lab, 8/25/2025
import numpy as np
from sklearn.metrics import mean_squared_error

def _plate_calculate_gaussian(params, curve, end_index, return_fit=False, 
                              delta_x_m=4.5e-3):
    
    """
    Calculates a Gaussian curve based on y = A * exp(-(x-x0)^2 / 2Dt) 
    and returns the error relative to a provided curve.

    ARGUMENTS:
        params (tuple): (A, Dt) values to optimize.
        curve (array-like): raw data values to compare.
        end_index (int): index up to which to calculate the error.
        delta_x_m (float): spacing along the x-axis (meters per point).
        return_fit (bool): if True, also return the fitted curve.

    RETURNS:
        nrmse (float): normalized root mean squared error between curve 
            and fit.
        fit_curve (np.array, optional): values of the calculated Gaussian 
            curve.
    """

    A, Dt = params  # amplitude and Dt

    x_vals = np.arange(len(curve)) * delta_x_m
    x0 = delta_x_m  # peak position fixed at first point (can be parameterized if needed)

    # Gaussian equation
    fit_curve = A * np.exp(-((x_vals - x0) ** 2) / (2 * Dt))

    # Only consider the range of interest we calculated earlier
    start_index = 1
    curve_ranged = np.array(curve[start_index:end_index], dtype=float)
    fit_curve_ranged = fit_curve[start_index:end_index]

    # Normalized RMSE
    rmse = np.sqrt(mean_squared_error(curve_ranged, fit_curve_ranged))
    mean_curve = np.mean(np.abs(curve_ranged))  # avoids division by near-zero
    if mean_curve != 0:
        nrmse = (rmse / mean_curve)
    else:
        nrmse = rmse

    if return_fit:
        return nrmse, fit_curve
    else:
        return nrmse
