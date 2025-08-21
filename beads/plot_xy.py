# Christopher Esther, Hill Lab, 8/15/2025
import os
from pathlib import Path
import pandas as pd
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt

def plot_xy_beads(path, save=False, label_beads=True, bead=None):

    """
    Plots the XY position of every bead in a VRPN file. If a path directly
    to a VRPN file is provided, it will plot just the beads in that file, 
    or if a path to a folder is given it will make a unique plot for 
    every VRPN file in that folder. 

    ARGUMENTS:
        path (str): the path to the file or folder that should be plotted
        save (bool): whether the plots should be saved as PNGs to the 
            path provided.
        label_beads (bool): when true, prints the index of each bead on 
            the plot next to its trace. Defaults to True.
        bead (int): the 0-based index of one bead that should be 
            plotted by itself. 
    """

    # Some initial path parsing logic
    if os.path.isfile(path):   # if a direct path, we just have one file
        all_files = [path]
    elif os.path.isdir(path):  # if a folder path, get all VRPNs inside
        all_files = [os.path.join(path, file) for file in Path(path).glob('*.vrpn.mat')]
        print(f'Plotting beads for {len(all_files)} file(s).')
    else:
        print('ERROR: Path does not exist or is not a regular file/folder.')


    # Iterate over each video and plot each bead
    for file in all_files:  # file iterator
        
        # Load the data and init the plot
        data = pd.DataFrame(loadmat(file)['tracking']['spot3DSecUsecIndexFramenumXYZRPY'][0][0])
        fig, ax = plt.subplots(figsize=(12, 8))

        # If only one bead was requested
        all_beads = np.unique(data[2]).astype(int)
        if bead and bead in all_beads:
            beads_to_plot = [bead]
        elif bead and bead not in all_beads:
            print(f"ERROR: Bead index '{bead}' does not exist in this file")
            print(f'       The maximum bead index is {max(all_beads)}')
            beads_to_plot = np.unique(data[2])
        else:
            beads_to_plot = np.unique(data[2])

        # Iterate over every bead
        for bead in beads_to_plot:
            bead_data = data[data[2] == bead]
            clean_bead_data = bead_data[~np.isnan(bead_data[4])]  # remove NaNs
            ax.plot(clean_bead_data[4], clean_bead_data[5])

            # Add index label to beads, if requested
            if label_beads:
                start_cords = clean_bead_data.iloc[0]
                ax.text(start_cords[4], start_cords[5], str(int(bead)), fontsize=8)

        # Add in the stuff to make the graph pretty
        ax.set(xlabel='X Position (pixels)', ylabel='Y Position (pixels)')
        ax.set_title(f'{file[-120:]}\nPlot XY: {max(all_beads) + 1} total beads', fontsize=10)

        # Save plot if requested
        if save:
            save_path = os.path.join(os.path.dirname(file), f'{Path(file).stem}.png')
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            