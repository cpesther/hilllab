# ellen han, 4/23/2026

import numpy as np
import matplotlib.pyplot as plt

from .load_hdf import load_hdf

def bead_traj(bead_uuid,path,ax=None,color=None):
    """
    plots a simple bead trajectory to use for classification examples.
    
    ARGUMENTS: 
        bead_uuid (str or int): uuid or index of the bead to be plotted
        path (str): path to h5 file for plate with bead
        ax (matplotlib.axes.Axes): opt, specify to plot in subplots
        color (cmap): opt, aesthetics
    
    good beads:
        plate 3, bead 499: stuck
        plate 3, bead 365: transiting
        plate 3, bead 339: oscillating
        plate 1, bead 313: discard

    """
    groupby_summary,groupby_positions,*_ = load_hdf(path)
    
    # indices
    all_beads = list(groupby_summary.groups.keys()) # list of all uuid
    if isinstance(bead_uuid,int): # if index provided instead of uuid
        bead_uuid = all_beads[bead_uuid]
    else: pass

    # get data
    bead_data = groupby_positions.get_group(bead_uuid)
    bead_x = bead_data['x']
    bead_y = bead_data['y']
    
    time_data = groupby_summary.get_group(bead_uuid)
    dt = time_data['lifetime_seconds']/time_data['lifetime_frames']
    time = np.arange(0,time_data['lifetime_seconds'].iloc[0],dt.iloc[0])
    
    # mismatch exception
    if (len(bead_data['x']) != len(bead_data['y']) 
        or len(bead_data['x']) != len(time) 
        or len(bead_data['y']) != len(time)):
        raise Exception('mismatch')
    
    # plot
    if ax is None:
        fig,ax = plt.subplots(figsize=(8,8))

    ax.plot(bead_x, bead_y, color=color, lw=2)
    
    # xy range
    x_range = max(bead_x)-min(bead_x)
    y_range = max(bead_y)-min(bead_y)
    
    ax.text(0.05, 0.95, f'{x_range:.2f} x {y_range:.2f} px', 
             transform=ax.transAxes, va='top', ha='left', fontsize=15)
    
    #ax.set(xlabel='X Position (px)', ylabel='Y Position (px)')
           
    ax.set(xticks=[],yticks=[],aspect='equal',adjustable='datalim')

    
    return ax
