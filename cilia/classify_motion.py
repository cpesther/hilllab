# Christopher Esther, Hill Lab, 8/15/2025
import os
from pathlib import Path
import pandas as pd
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt

def classify_motion(path, plot=False, save=False, label_beads=True):

    """
    Given a VRPN file, this function will examine each bead and determine
    whether it is transitting (moving in a direction) or oscillating. 
    These classifications are returned as a dataframe.

    ARGUMENTS:
        path (str): the path to the VRPN file that should be analyzed. 
        plot (bool): whether a plot should be displayed.
        save (bool): whether the plot should be saved as PNGs to the 
            path provided.
        label_beads (bool): when true, prints the index of each bead on 
            the plot next to its trace. Defaults to True.
    """
    
    # Load the data and isolate the components
    data = pd.DataFrame(loadmat(path)['tracking']['spot3DSecUsecIndexFramenumXYZRPY'][0][0])
    clean_data = data[~np.isnan(data[4])]  # remove NaNs
    all_beads = np.unique(data[2]).astype(int)
    classifications = pd.DataFrame(columns=['bead', 'transporting'])
    
    if plot:  # if plotting, init the plot
        fig, ax = plt.subplots(figsize=(12, 8))
    
    for bead in all_beads:
        bead_data = clean_data[clean_data[2] == bead]
        x = np.array(bead_data[4])
        y = np.array(bead_data[5])
        
        # Calculate a few parameters that will help us determine whether the motion state
        # Net displacement
        delta_r = np.linalg.norm([x[-1] - x[0], y[-1] - y[0]])
        
        # Total path length
        path_length = np.sum(np.sqrt(np.diff(x)**2 + np.diff(y)**2))
        
        # Straightness
        straightness = delta_r / path_length if path_length > 0 else 0
        
        # Radius of gyration
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        rg = np.sqrt(np.mean((x - x_mean)**2 + (y - y_mean)**2))
        
        # Do the actual classification here
        straightness_thresh = 0.07
        rg_thresh = 3
        if straightness > straightness_thresh and rg > rg_thresh:
            transporting = True
            plot_color = 'green'
        else:
            transporting = False
            plot_color = 'red'
    
        if plot:
            ax.plot(bead_data[4], bead_data[5], color=plot_color)
    
            # Add index label to beads, if requested
            if label_beads:
                start_cords = bead_data.iloc[0]
                ax.text(start_cords[4], start_cords[5], str(int(bead)), fontsize=8)

            # Save plot if requested
            if save:
                save_path = os.path.join(os.path.dirname(path), f'{Path(path).stem}.png')
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
        # Append the classification to the dataframe
        classifications.loc[len(classifications)] = [bead, transporting]
    
    if not plot:
        return classifications, clean_data
    else:
        # Add in the stuff to make the graph pretty
        ax.set(xlabel='X Position (pixels)', ylabel='Y Position (pixels)')
        ax.set_title(f'{path[-120:]}\nClassify Motion: {max(all_beads) + 1} total beads', fontsize=10)
        print(classifications['transporting'].value_counts())
