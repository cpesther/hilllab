# Christopher Esther, Hill Lab, 7/10/2025
import pandas as pd
from scipy.io import loadmat

def load_vrpn(path):

    """
    Loads a VRPN file at a given path and returns the data as a pandas dataframe
    """

    # Load the data from the VRPN
    data = pd.DataFrame(loadmat(path)['tracking']['spot3DSecUsecIndexFramenumXYZRPY'][0][0])

    # Name the columns for sanity
    data.columns = ['', '', 'particle_id', 'frame', 'x', 'y', '', '', '', '']

    return data
