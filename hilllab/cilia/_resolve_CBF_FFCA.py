# Christopher Esther, Hill Lab, 1/22/2026
from matplotlib import gridspec
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def _resolve_CBF_FFCA(psd_map, frequency_vector, power_threshold, output_path, plot=False):

    """
    Takes a 3D array containing the PSDs for every pixel in a video and 
    calculates the CBF and FFCA values. This logic is stored in this 
    separate function so it can be shared between both the C# and pure
    Python calculation methods. It will also output the calculated
    values to a file, if requested. 

    ARGUMENTS:
        psd_map (3D array): an array containing the PSD values for every
            pixel in a video. 
    """

    # Average all the PSDs together to get one PSD representative of the
    # whole video
    avg_psd = np.mean(psd_map, axis=(0, 1))

    # The CBF is the frequency of the maximum PSD value from the average
    cbf = frequency_vector[np.argmax(avg_psd)]

    # Calculate the percent ciliation by counting how many are above a certain
    # power threshold (fraction of functional ciliated area). 
    max_psd_map = np.max(psd_map, axis=2)
    ffca = np.sum(max_psd_map > power_threshold) / max_psd_map.size

    # Save the results to a dataframe and write to CSV
    results = pd.DataFrame(data={'cbf': [cbf],'ffca': [ffca]})
    results.to_csv(output_path, index=False)

    # Create figure (if requested)
    if plot:
        fig = plt.figure(figsize=(10, 8))
        gs = gridspec.GridSpec(2, 2, height_ratios=[2, 1])  # 2 rows, 2 columns

        ax_top = fig.add_subplot(gs[0, :])
        ax_top.plot(frequency_vector, avg_psd)
        ax_top.set_title("Top long plot")
        ax_top.grid(True)
        ax_top.set_title(f'{output_path}\nCBF and FFCA')
        ax_top.set_xlabel('Frequency (Hz)')
        ax_top.set_ylabel('Power')

        ax_bottom1 = fig.add_subplot(gs[1, 0])
        ax_bottom1.set_title('Max PSD Power Map')
        ax_bottom1.imshow(max_psd_map)

        ax_bottom2 = fig.add_subplot(gs[1, 1])
        ax_bottom2.set_title('FFCA Map')
        #ax_bottom2.imshow(ffca_map, cmap='RdGy_r')
        
    return cbf, ffca
