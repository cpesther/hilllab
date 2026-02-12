# Christopher Esther, Hill Lab, 2/12/2026
from ...utilities.walk_dir import walk_dir
from .vrpn_to_csv import vrpn_to_csv
from ...utilities.print_progress_bar import print_progress_bar

def batch_vrpn_to_csv(folder):
    
    """
    Converts all VRPNs in a folder and its subfolders into CSVs.

    ARGUMENTS:
        folder (string): the path to the folder containing CSVs.
    """

    # Find all VRPNs in the folder and its subdirectories
    all_vrpns = walk_dir(folder, extension=['vrpn.evt.evt.mat', 'vrpn.mat'])
    n_vrpns = len(all_vrpns)

    # Convert all VRPNs to CSV files
    for i, vrpn in enumerate(all_vrpns):

        # Convert the file to a CSV
        vrpn_to_csv(path=vrpn)
        
        # Print progress bar
        print_progress_bar(progress=i+1, total=n_vrpns, title='Converting files')
