# Christopher Esther, Hill Lab, 8/15/2025
import os
from pathlib import Path
import pandas as pd
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt

def plot_component_trace(path, save=False, bead=0):

    """
    Plots the maximized XY position of every bead in a VRPN file. If a 
    path directly to a VRPN file is provided, it will plot just the 
    beads in that file, or if a path to a folder is given it will make a 
    unique plot for every VRPN file in that folder. 

    ARGUMENTS:
        path (str): the path to the file or folder that should be plotted
        save (bool): whether the plots should be saved as PNGs to the 
            path provided.
        bead (int): the 0-based index of one bead that should be 
            plotted.
    """

    # Load the data and init the plot
    data = pd.DataFrame(loadmat(path)['tracking']['spot3DSecUsecIndexFramenumXYZRPY'][0][0])
    fig, ax = plt.subplots(figsize=(12, 5))

    # Make sure the requested bead actually exists
    all_beads = np.unique(data[2]).astype(int)
    if bead not in all_beads:
        print(f"ERROR: Bead index '{bead}' does not exist in this file")
        print(f'       The maximum bead index is {max(all_beads)}')
        return
    else:
        pass

    # Pull out the traces
    bead_data = data[data[2] == bead]
    x_component = bead_data[4]
    y_component = bead_data[5]
    frame_numbers = np.arange(0, len(x_component))

    # First axis (x-component using the left y-axis)
    ax.plot(frame_numbers, x_component, color='red')
    ax.set_ylabel('X Position (pixels)', color='red')
    ax.tick_params(axis='y', labelcolor='red')

    # Second axis (y-component using the right y-axis)
    ax2 = ax.twinx()  # create a new y-axis sharing the same x-axis
    ax2.plot(frame_numbers, y_component, color='blue')
    ax2.set_ylabel('Y Position (pixels)', color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')

    # Add in the stuff to make the graph pretty
    ax.set_title(f'{path[-130:]}\nComponent Trace: Bead index {bead} of {int(max(data[2]))}', fontsize=10)
    ax.set_xlabel('Frame Number');

    # Save plot if requested
    if save:
        save_path = os.path.join(os.path.dirname(path), f'{Path(path).stem}.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
