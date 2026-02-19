# Christopher Esther, Hill Lab, 2/12/2026
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from .load_tracking_data import load_tracking_data
from ..utilities.custom_axes import custom_axes

def calculate_bead_msd(path, fps, camera, magnification, units='um', lag_frames=None, 
                       plot=False, save_plot=False, pipeline='python'):

    """
    Calculates and returns the ensemble MSD (mean squared displacement)
    of the beads in a VRPN file.

    ARGUMENTS:
        path (string):
        fps (int): the frame rate of the VRPN used for converting frame 
            numbers to timestamps. 
        camera (str): the three charcter code used for pulling the 
            pixel width of the camera for converting the coordiantes 
            into um from pixels.
        magnification (float): the factor of magnification applied when
            this video was recorded. 
        units (string): the units that the MSD values should use
        lag_frames (list): a list of frame indices which should be used
            to calculate the MSD.
        plot (bool): whether a plot of the MSD over time should be created
        save_plot (bool): whether the MSD plot created should be saved 
            as a PNG to the same directory as the VRPN
        pipeline (string): either 'python' or 'matlab'. Controls whether
            files are saved as MATLAB files compatible with legacy code
            or as CSV and Excel docs compatible with this Python library.

    RETUNRS:
        ensemble_msd (pandas.DataFrame): a dataframe containing the ensemble
            MSD, its standard deviation, and the timestamp. 
        msd (pandas.DataFrame): a dataframe containing the MSDs for each
            particle individually. 

    NOTES:
        The ensemble MSD value is simply the average of the MSD of each
        individual bead at each provided lag frame. 
    """

    # Set the lag_frames default values if none were provided
    if lag_frames is None:
        lag_frames = np.array([1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 1001])
    else:
        lag_frames = np.asarray(lag_frames)

    # Load the tracking data
    vrpn_data = load_tracking_data(path=path, fps=fps, camera=camera, 
                                   magnification=magnification, pipeline=pipeline)

    # Calculate a few random things
    unique_ids = np.unique(vrpn_data['particle_id']).astype(int)  # all unique bead IDs

    # Generate a dataframe for storing the calculated MSD for each particle
    # at each lag frame
    msd = pd.DataFrame(columns=lag_frames)
    msd['particle_id'] = unique_ids
    msd = msd.set_index('particle_id')
    n_beads = len(unique_ids)

    # Iterate over every bead in the data
    for bead_index, bead_id in enumerate(unique_ids):

        # Pull just the data from this bead
        bead_data = vrpn_data[vrpn_data['particle_id'] == bead_id]

        # Calculate the number of frames in which this bead appears
        n_frames = bead_data.shape[0]

        # Pull the X and Y coordinate values
        x = bead_data['x'].to_numpy()
        y = bead_data['y'].to_numpy()

        # Loop over each lag value to calculate the MSD
        for lag_index, lag in enumerate(lag_frames):

            # If this lag values is longer than the particle's lifetime
            if lag >= n_frames:
                continue  # skip

            # Calculate distances traveled with X and Y coordinates
            dx = x[lag:n_frames] - x[:n_frames - lag]
            dy = y[lag:n_frames] - y[:n_frames - lag]

            # Calculate squared displacement
            squared_displacement = dx**2 + dy**2
            
            # Save this squared displacement value into the MSD dataframe
            msd.loc[bead_index, lag] = np.mean(squared_displacement)

    # Calculate ensemble (all beads) MSD and standard deviation
    ensemble_msd_mean = msd.mean(axis=0)
    ensemble_msd_std = msd.std(axis=0)
    timestamps = lag_frames / fps

    # Format a as dataframe for output
    ensemble_msd = pd.DataFrame({'ensemble_msd_mean': ensemble_msd_mean,
                                 'ensemble_msd_std': ensemble_msd_std,
                                 'timestamp': timestamps})

    # Create a plot, if requested
    if plot:
        fig, ax = custom_axes(log=True, xlabel='t (seconds)', ylabel=f'msd ({units})',
                            title=Path(path).stem, subtitle=path)
        
        # Display every beads MSD as a subtle line
        for i, row in msd.iterrows():

            # Only add label to first one for cleaner legend
            if i == 0:
                label = f'Bead MSDs (n = {n_beads})'
            else:
                label = None

            # Plot each MSD
            ax.loglog(timestamps, row, label=label, c=(0.7, 0.7, 0.7, 0.3), linestyle='-')

        # Plot the ensemble MSD with error bars representing the STDEV
        ax.errorbar(x=timestamps, y=ensemble_msd_mean, yerr=ensemble_msd_std, lw=2, c='r', 
                    capsize=5, capthick=2, label='Ensemble MSD')

        # Add a legend
        ax.legend(loc='upper left', bbox_to_anchor=(0.05, 1), fontsize=14, frameon=False)

        # Save the figure, if requested
        if save_plot:
            plt.savefig(Path(path).parent / f'{Path(path).stem}.png', dpi=300, bbox_inches='tight')

    # Slightly adjust the structure of the MSD table for cleaner access
    # (bead IDs as columns instead of rows)
    msd = msd.transpose()
    msd.index = timestamps        # use timestamps as index
    msd.index.name = 'timestamp'  # and rename appropriately

    return ensemble_msd, msd
        