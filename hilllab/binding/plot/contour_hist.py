# Christopher Esther, Hill Lab, 2/27/2026
import matplotlib.pyplot as plt
import numpy as np

from ...utilities.custom_axes import custom_axes

def contour_hist(counts, file=None, save_path=None):

    # Pull all values from the counts for a histogram
    all_values = []
    for key in list(counts.keys()):
        all_values.extend(counts[key])
    
    # Limit values for histogram
    all_values_hist = [s for s in all_values if s < 1000]
    
    # Calculate bins
    bin_width = 1
    bins = np.arange(min(all_values_hist), max(all_values_hist) + bin_width, bin_width)
    
    # Create custom axis
    fig, ax = custom_axes(xlabel='Contour Size (pixels²)', ylabel='# Contours', 
                          title='Contour Counts', subtitle=file)
    
    # Set histogram region colors
    regions = {
        'small': 'red',
        'expected': 'green',
        'large': 'blue',
    }
    
    # Plot histogram in three regions
    for size in regions.keys():
        ax.hist(counts[size], bins=bins, color=regions[size], alpha=0.7, 
                label=f"{size.capitalize()} (n={len(counts[size])})")
    
    # Couple plot appearance things
    ax.set_xlim(left=0, right=110)
    ax.legend(loc='upper right', fontsize=14, frameon=False)
    
    # Save the figure(
    if save_path is not None:
        plt.savefig(save_path, bbox_inches='tight', 
                    pad_inches=0.5, dpi=300)
        plt.close()
