# Christopher Esther, Hill Lab, 1/9/2026
import numpy as np
from scipy.signal import find_peaks

def calculate_AFV(position_data, fps):

    """
    When provided the position_data dataframe for one bead (which is output
    from the primary_analysis function), this function will calculate
    the amplitude, velocity, and frequency of this beads oscillation/movement.

    ARGUMENTS:
        position_data (pandas.DataFrame): a dataframe containing (at minimum)
            values for the PCA and speed of the particle at each frame as
            saved in the 'positions' table produced by the primary analysis 
            function.
        fps (int): the sampling rate of the data in frames per second.

    RETURNS:
        afv (dict): a dictionary containing various calculations of the
            amplitude, frequency, and velocity.
    """

    afv = {}  # create dict to save results

    # Pull the PCA from the position data
    pca = position_data['pca'].reset_index()['pca']

    # <<<<< CALCULATE AMPLITUDE >>>>>
    # Find peaks in PCA signal
    hipeaks_index, _ = find_peaks(pca, prominence=1)
    lopeaks_index, _ = find_peaks(-pca, prominence=1)

    if (len(hipeaks_index) == 0) or (len(lopeaks_index) == 0):
        afv['amplitude_abs'] = None
        afv['amplitude_mean'] = None
        afv['amplitude_quar'] = None
    else:
        # Pull the values from these peak indices
        hipeaks = pca[hipeaks_index]
        lopeaks = pca[lopeaks_index]
        hipeaks_mean = np.mean(hipeaks)
        lopeaks_mean = np.mean(lopeaks)
    
        # High quartile
        if hipeaks.size == 0:
            hi_quartile_mean = np.nan
        else:
            p75 = np.percentile(hipeaks, 75)
            hi_quartile_mean = np.mean(hipeaks[hipeaks >= p75])
        
        # Low quartile
        if lopeaks.size == 0:
            lo_quartile_mean = np.nan
        else:
            p25 = np.percentile(lopeaks, 25)
            lo_quartile_mean = np.mean(lopeaks[lopeaks <= p25])
        
        # Save values to dict
        afv['amplitude_abs'] = max(hipeaks) - min(lopeaks)
        afv['amplitude_mean'] = hipeaks_mean - lopeaks_mean
        afv['amplitude_quar'] = hi_quartile_mean - lo_quartile_mean

    # <<<<< CALCULATE FREQUENCY >>>>>
    # Pad the PCA signal to a length equal to a power of two for a faster FFT
    n = len(pca)
    target_length = 1 << (n - 1).bit_length()  # next power of two
    pca_padded = np.pad(pca, (0, target_length - n), mode='constant')
    
    # Run FFT on the data
    freqs = np.fft.rfftfreq(n, d=1 / fps)  # frequency axis
    fft_vals = np.fft.rfft(pca_padded)
    power = np.abs(fft_vals)**2            # power spectrum
    
    # Find the peaks in the PSD
    trim_length = int((len(pca) / 2) + 1)
    freqs_trimmed = freqs[:trim_length]
    power_trimmed = power[:trim_length]
    f_peaks, f_properties = find_peaks(power_trimmed, prominence=300)
    
    # Safe execution in the event that no peaks were found
    if len(f_peaks) == 0:
        frequency = None
    else:
        dominant_peak = f_peaks[np.argmax(f_properties['prominences'])]
        frequency = freqs_trimmed[dominant_peak]
    
    # Save value to dict
    afv['frequency'] = frequency

    # <<<<< CALCULATE VELOCITY >>>>>
    # Calculate differences between subsequent values and direction
    diff = np.diff(pca)
    trends = np.sign(diff)
    
    # Calculate speeds of up- and downstrokes separately
    speeds = position_data['speed'].to_numpy()
    up_speeds = []
    down_speeds = []
    for i, trend in enumerate(trends):
    
        # Pull the speed value and make sure it isn't a nan
        speed_value = speeds[i]
        if np.isnan(speed_value):
            continue
        
        # Save speed to appropriate list depending on direction
        if trend > 0:
            up_speeds.append(speed_value)
        else:
            down_speeds.append(speed_value)
    
    # Save values to dict
    afv['velocity_up_mean'] = np.mean(up_speeds)
    afv['velocity_down_mean'] = np.mean(down_speeds)
    afv['velocity_up_med'] = np.median(up_speeds)
    afv['velocity_down_med'] = np.median(down_speeds) 

    return afv
