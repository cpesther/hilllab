import h5py
from scipy.io import loadmat

def load_matlab(file_path):

    """
    Just a simple function used to load MATLAB files. Uses both h5py and
    scipy to ensure compatabiltiy with older and newer MATLAB files. 
    """

    try:
        with h5py.File(file_path, "r") as f:
            return {k: f[k][:] for k in f.keys()}
    except OSError:
        return loadmat(file_path)
