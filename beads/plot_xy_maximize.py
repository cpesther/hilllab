# Christopher Esther, Hill Lab, 8/15/2025
import os
from pathlib import Path
import pandas as pd
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt

def plot_xy_beads_maximize(path, save=False, label_beads=True):

    """
    Plots the maximized XY position of every bead in a VRPN file. If a 
    path directly to a VRPN file is provided, it will plot just the 
    beads in that file, or if a path to a folder is given it will make a 
    unique plot for every VRPN file in that folder. 

    ARGUMENTS:
        path (str): the path to the file or folder that should be plotted
        save (bool): whether the plots should be saved as PNGs to the 
            path provided.
        label_beads (bool): when true, prints the index of each bead on 
            the plot next to its trace. Defaults to True.
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
        beads_to_plot = np.unique(data[2]).astype(int)

        # Spacing parameters
        beads_per_row = 6
        col_x_offset = 0
        row_y_offset = 0
        max_height_in_row = 0  # track tallest bead in current row
        
        for i, bead in enumerate(beads_to_plot):
            bead_data = data[data[2] == bead]
            bead_data = bead_data[~np.isnan(bead_data[4])]
        
            range_x = bead_data[4].max() - bead_data[4].min()
            range_y = bead_data[5].max() - bead_data[5].min()
        
            # bead-specific spacing
            horizontal_spacing = range_x * 1.3
            vertical_spacing = range_y * 1.3
        
            shifted_x = bead_data[4] - bead_data[4].min() + col_x_offset
            shifted_y = bead_data[5] - bead_data[5].min() + row_y_offset
        
            ax.plot(shifted_x, shifted_y)
        
            if label_beads:
                ax.text(shifted_x.iloc[0], shifted_y.iloc[0], str(bead), fontsize=8)
        
            # update offsets for next bead
            col_x_offset += horizontal_spacing
            max_height_in_row = max(max_height_in_row, vertical_spacing)
        
            # move to next row after every 5 beads
            if (i + 1) % beads_per_row == 0:
                col_x_offset = 0
                row_y_offset += max_height_in_row
                max_height_in_row = 0
                
        # Add in the stuff to make the graph pretty
        ax.set(xlabel='Relative X Position (pixels)', ylabel='Relative Y Position (pixels)')
        ax.set_title(f'{file[-120:]}\nPlot XY Maximize:{max(beads_to_plot) + 1} total beads', fontsize=10)

        # Save plot if requested
        if save:
            save_path = os.path.join(os.path.dirname(file), f'{Path(file).stem}.png')
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
