# Christopher Esther, Hill Lab, 7/10/2025
import pandas as pd
from scipy.io import loadmat
from pathlib import Path

def load_vrpn(path):

    """
    Loads a VRPN file at a given path and returns the data as a pandas dataframe
    """

    # Load the data from the VRPN
    data = pd.DataFrame(loadmat(path)['tracking']['spot3DSecUsecIndexFramenumXYZRPY'][0][0])

    # Determine the full suffix of the file so we can decide how to 
    # name the columns
    full_suffix = ''.join(Path(path).suffixes)

    # Name the columns for sanity
    # Plain VRPNs have everything
    if full_suffix == '.vrpn.mat':
        column_names = ['timestamp', 'microseconds', 'particle_id', 'frame', 'x', 'y', 'z', 'roll', 'pitch', 'yaw']

    # VRPNs with an evt have the microsecond column dropped
    elif full_suffix == '.vrpn.evt.evt.mat':
        column_names = ['timestamp', 'particle_id', 'frame', 'x', 'y', 'z', 'roll', 'pitch', 'yaw']

    # Give up if otherwise
    else:
        raise ValueError('Unable to interpret file extension for column naming')
    
    # Name the columns if data is present
    if data.shape[0] > 0:
        data.columns = column_names

    # If the VRPN has no data, simply return an empty dataframe with teh 
    # appropriate labels.
    else:
        data = pd.DataFrame(columns=column_names)

    return data
