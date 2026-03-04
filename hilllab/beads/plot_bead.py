# ellen han, 2/25/2026

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from load_hdf import load_hdf

def plot_bead(bead_uuid, groupby=None, path=None, pixel_width=1):
    """
    Plots individual bead trajectory. Includes:
        zoomed-out x vs y, zoomed-in x vs y, x vs time, and y vs time.
    
    ARGUMENTS:
        bead_uuid: the unique identifier assigned to a bead (str)
                    or the index of the bead in the file (int)
        groupby (tuple): tuple containing load_hdf return
        path (str): path to a .h5 file with bead data to run load_hdf
        pixel_width (int): opt micron/pixel conversion (default to 1)
        
    """
    
    # read data
    if path is None: # given groupby
        (groupby_summary,groupby_positions,_,bounds) = groupby
    if groupby is None: # given path
        groupby_summary,groupby_positions,_,bounds = load_hdf(path)
        
    # either groupby or path must be given
    if groupby is None and path is None == None:
        raise Exception('either groupby or file path must be defined')
    
    # indices
    all_beads = list(groupby_summary.groups.keys()) # list of all uuid
    if isinstance(bead_uuid,int): # if index provided instead of uuid
        i = bead_uuid
        bead_uuid = all_beads[bead_uuid]
    else: i = all_beads.index(bead_uuid)
    
    # position bounds
    xmax = bounds['x'] * pixel_width
    ymax = bounds['y'] * pixel_width

    # get data
    bead_data = groupby_positions.get_group(bead_uuid)
    bead_x = bead_data['x'] * pixel_width
    bead_y = bead_data['y'] * pixel_width
    
    units = 'px' if pixel_width == 1 else 'µm'
    
    time_data = groupby_summary.get_group(bead_uuid)
    dt = time_data['lifetime_seconds']/time_data['lifetime_frames']
    time = np.arange(0,time_data['lifetime_seconds'].iloc[0],dt.iloc[0])
    
    # mismatch exception
    if (len(bead_data['x']) != len(bead_data['y']) 
        or len(bead_data['x']) != len(time) 
        or len(bead_data['y']) != len(time)):
        raise Exception('mismatch')

    # plot bead
    fig = plt.figure(figsize=(18, 8))
    gs = GridSpec(2,2,figure=fig,height_ratios=[2,1])
    fig.suptitle(f'bead {i}/{len(all_beads)-1} | uuid: {bead_uuid}',fontsize=20)
    
    # xy zoomed out
    ax1 = fig.add_subplot(gs[:,0])
    ax1.plot(bead_x, bead_y,linewidth=3)
    ax1.set(xlim=(0,1.2*xmax),ylim=(0,1.2*ymax))
    ax1.set(xlabel=f'X Position ({units})', ylabel=f'Y Position ({units})',
            aspect='equal')
    
    # xy zoomed in
    ax2 = fig.add_subplot(gs[0,1])
    ax2.plot(bead_x, bead_y)
    ax2.set(xlabel=f'X Position ({units})', ylabel=f'Y Position ({units})')
    # xy range
    x_range = max(bead_x)-min(bead_x)
    y_range = max(bead_y)-min(bead_y)
    ax2.text(0.05, 0.95, f'{x_range:.2f} x {y_range:.2f} {units}', 
             transform=ax2.transAxes, va='top', ha='left', fontsize=20)
    
    # x vs time
    subgs = gs[1, 1].subgridspec(1,2,wspace=0.2)
    ax3 = fig.add_subplot(subgs[0,0])
    ax3.plot(time, bead_x)
    ax3.set(xlabel='Time (s)', ylabel=f'X Position ({units})')

    # y vs time
    ax4 = fig.add_subplot(subgs[0,1])
    ax4.plot(time, bead_y)
    ax4.set(xlabel='Time (s)', ylabel=f'Y Position ({units})')
    
    plt.tight_layout()
    plt.show()
    