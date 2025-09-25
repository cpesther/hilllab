# Christopher Esther, Hill Lab, 8/22/2025
import numpy as np
from scipy.optimize import curve_fit  # curve optimization
from scipy.signal import find_peaks  # signal peak localization
from matplotlib import pyplot as plt

def _plate_profile_curve(values, plot=False):

    """
    A backend function that locates and returns the index of the peak of 
    the suspected Gaussain cuvrve as well as the index of the end of the
    curve for a given array of data using a penalty-based weighting 
    system. This is the basic function that is called on every curve 
    during the data preparation step. 
    
    ARGUMENTS:
        values (list): a list of intensity values containing a 
            Gaussain cuve
        plot (bool): controls whether the data and weights are displayed
            once the function finishes execution. Defaults to False.
    
    REUTRNS:
        peak_index (int): the index of the peak of the Gaussian curve
        end_index (int): the index of the end of the Gaussian curve
    """
    
    # A simple Gaussian function used for testing the peak locations
    def gaussian(x, a, mu, sigma):
        return a * np.exp(-(x - mu)**2 / (2 * sigma ** 2))
    
    # Create an array of the possible indices of the peak (0 to 4)
    candidate_indices = np.arange(0, 5, 1)

    # Normalize and slice down the data to just the first 8 values
    normalized_values = np.array(values) / max(values)
    clean_values = np.array(normalized_values[:8])
    
    # Here we iterate over each 'candidate' index where the peak could
    # possibly be located and fit a curve at that location, recording 
    # the error of each one as a method of determining which is the best
    # location for a Gaussian (i.e. the one with the least error).
    all_errors = []   # the SSE values of each fit
    all_y_fits = []   # the y-values of each fit
    all_pars = []     # the Gaussian parameters of each fit
    for index in candidate_indices:
        
        # Grab our y-values (the clean data), and generate the x values
        y = clean_values[index:]
        x = np.arange(index, len(clean_values))
    
        # Fit a Gaussian to this data
        try:
            p0 = [clean_values[index], index, 3]  # initial guess params
            bounds = ([0, index - 0.5, 0],[1, index + 0.5, 20])
            
            # pars array stores the returned a, mu, and sigma values
            pars, _ = curve_fit(gaussian, x, y, p0=p0, bounds=bounds, maxfev=2000)
        
            # Calculate fit error (SSE)
            y_fit = gaussian(x, *pars)
            y_errors = np.abs((y - y_fit) / y)
            error = np.sum(y_errors)
            
            # Save everything to its respective list
            all_y_fits.append(y_fit)
            all_pars.append(pars)
            all_errors.append(error)

        # Handle failed fit gracefully
        except RuntimeError:
            all_y_fits.append(np.repeat(0, 8))  # all zeroes
            all_pars.append([0, 0, 0])          # all zeroes
            all_errors.append(float('inf'))     # infinite error

    # Checking the error of Gaussian fits is a good start, but there is
    # more fine-tuning that can be done to the localization process. We 
    # will now create and apply a series of penalties (i.e. increasing
    # the error values) based on several other mathematical observations.
    # The penalties that are assigned during each step are mathematically
    # arbitrary, but have been optimized and chosen via trial and error. 
    
    # <<<<< SIGNAL PEAK PENALTY >>>>>
    # Scan for a peak in the signal and assign penalties to highly favor 
    # the location of any detected peak.
    peaks = find_peaks(clean_values, distance=4)[0]
    
    # If no peaks are found, it could mean the "peak" is at the 0-index
    if len(peaks) == 0:
        peak_penalties = np.array([0.5, 1, 1, 1, 1])  # favor 0-index
    
    # If we did find a peak, lower the penalty for that index
    else:
        peak_penalties = np.array([1,1,1,1,1])  # template penalties
    
        # Only use peaks less than the 5th index 
        if peaks[0] < 5:
            peak_penalties[peaks[0]] = 0.1  # reduce its penalty
        
    # <<<<< DISTANCE FROM MAXIMUM PENALTY >>>
    # Apply higher penalties to indices that are further away from the 
    # maximum value of the dataset. We'll start with some logic to 
    # remove large peaks caused by valap that could be misinterpreted as
    # the maximum.
    sorted_data = np.sort(clean_values)[::-1]  # sort to compare peaks

    # Check if the largest peak is at least twice as big as the next 
    # largest. If so, it may be an artifact (valap peak) rather than a 
    # real maximum. Remove it by replacing it with 0.
    if sorted_data[0] * 0.5 >= sorted_data[1]:
        np.put(clean_values, 0, np.argmax(clean_values))
    
    # Increase the penalty for every additional index a value is away 
    # from the peak of the data
    dmax_mult = 0.4  # the amount added to the penalty per index away
    maximum_index = np.argmax(clean_values)
    dmax_penalties = [(abs(maximum_index - index) + 1) * dmax_mult for index in candidate_indices]

    # <<<<< DYNAMIC RANGE PENALTY >>>>>
    # Apply higher penalties to locations whose Gaussian fit at that 
    # location has a dynamic range significantly smaller than the raw data.
    range_penalties = []

    # Compute by comparing the spread of the raw data to each fit
    data_range = np.ptp(clean_values)  # peak-to-peak (max - min)
    range_penalties = [
        np.abs(1 - (data_range / np.ptp(y_fit)) / 1.5)
        for y_fit in all_y_fits]

    # <<<<< FREQUENCY PENALTY >>>>>
    # Apply frequency-based penalization (i.e. peaks at index 1 are far 
    # more likely than at index 4, so  this adjust the errors to favor 
    # the most likely locations based on experimental frequencies).
    frequency_penalties = np.array([0.98, 0.45, 0.87, 0.96, 1.06])
    
    # <<<<< PEAK INDEX DECISION >>>>>
    # After all of the penalties have been applied, multiply them together. 
    combined_penalties = peak_penalties * frequency_penalties * dmax_penalties * range_penalties
    
    # And then apply them to the error values and select the lowest
    penalized_errors = all_errors * combined_penalties
    peak_index = np.argmin(penalized_errors)  # smallest error wins
    
    # <<<<< GAUSSIAN END LOCALIZATION >>>>>
    # Now that we know where the Gaussian curve starts (its peak), we 
    # must also deteremine where it ends. For this determination, we have
    # several methods (i.e. calculations) that each decide their own
    # location where the curve shoudl end. We run all of these methods
    # and also assign each of them a weight controlling how much influence
    # their "opinion" has over the final decision. This allows us to 
    # favor certain methods as more accurate than others. 

    method_weights = []  # the weights (influence) of each method
    final_indices = []   # the suggested Gaussian end index of each method
    
    # The try/except blocks seen in the following sections are designed 
    # to gracefully bypass certain calculations in the event that they 
    # can't find an appropriate index to use. 

    # <<<<< DERIVATIVE LOCALIZATION >>>>>
    # End the Gaussian where the curve starts inflecting up (i.e. where
    # the derivative goes negative to positive).)
    try:
        # Calculate the first dervative of the data
        x = np.arange(0, 16, 1)
        derf = np.gradient(values, x)
        derf_index = np.where(derf[peak_index + 1:] > 0)[0][0]
        final_indices.append(derf_index)
        method_weights.append(0.8)
    except:
        pass
    
    # <<<<< FRACTION OF MAXIMUM >>>>>
    # A good point for the end of the curve is where the values go below
    # 5% of the value at the peak of the curve
    try:
        p_threshold = 0.02
        frac_index = np.where(values < values[peak_index] * p_threshold)[0][1:][0]
        final_indices.append(frac_index)
        method_weights.append(0.4)
    except:
        pass
    
    # <<<<< STANDARD DEVIATION >>>>>
    # Use the standard deviation from the Gaussian calculated at the best 
    # peak location. A Gaussian is effectively 0 after 3 standard deviations. 
    try:
        t_pars = np.transpose(pars)
        stdev_index = round(peak_index + (t_pars[2][peak_index] * 3))
        final_indices.append(stdev_index)
        method_weights.append(1.0)
    except:
        pass
    
    # <<<<< GAUSSIAN END DECISION >>>>>
    # If every method failed to determine a peak index (unlikely)
    if len(final_indices) == 0:
        raw_gaussian_end = 7  # a common, reasonable value
    else:
        # Otherwise we can calculate the weighted average
        raw_gaussian_end = round(np.average(final_indices, weights=method_weights))
    
    # Make sure that the selected Gaussian end value is neither too short
    # (not enough points to fit) nor too long (extending beyond capillary).
    min_length = 4   # minimum width required
    max_length = 11  # maximum width allowed
    end_index = max(min(raw_gaussian_end, max_length), peak_index + min_length)

    # Return a plot, if requested
    if plot:
        plt.plot(values, c='magenta')
        y_fit = all_y_fits[peak_index] * max(values)  # un-normalize the y-fit
        plt.plot(np.arange(peak_index, 8, 1), y_fit, c='blue')
        plt.plot([peak_index, peak_index], [0, max(values)], color='green', lw=1.5, linestyle='-')
        plt.plot([end_index, end_index], [0, max(values)], color='red', lw=1.5, linestyle='-')
    
    return peak_index, end_index
