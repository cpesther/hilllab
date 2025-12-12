# Christopher Esther, 11/6/2025
from datetime import datetime
import platform
import numpy as np
import os
import pandas as pd
from scipy.io import savemat  # for saving MatLab files

def _generate_VRPN(data, path, file_name, nframes, nparticles):
        
    """
    Generates a VRPN file for the given tracking data at the given path
    in the standard format used by our downstream MATLAB scripts. 

    ARGUMENTS:
        data (pandas.DataFrame): the dataframe containing the particle
            trajectories.
        path (string): the path where the VRPN should be saved.
        file_name (string): the name of the file being processed
        nframes (int): the number of frames in the video that produced
            this VRPN.
        nparticles (int): the number of particles to be saved in this
            VRPN. 
    """

    # Let's set some constants first. We don't need timestamps in our
    # VRPN since the frame number is our unit of time, so we'll just
    # set the required seconds and microseconds fields to zero. The
    # PLACEHOLDER value is also used to populate some extra columns
    # in the VRPN format that we don't need to use (Z, roll, pitch, yaw)
    SEC = 0
    USEC = 0
    PLACEHOLDER = [0, 0, 0, 0]

    # Create an array with ten columns, allocating one row for each
    # particle in every frame (pre-allocating memory is faster).
    vrpn_out = np.zeros((nframes * nparticles, 10))

    # Take the particle trajectories and create a pivot table
    # using the frame and particle attributes as the index. Since 
    # we need to pull data from this table in each step, formatting
    # it as a multi-index table will make this must faster
    part_pos_lookup = data.set_index(['frame', 'particle'])[['x', 'y']]

    # Here's where we iteratively add the data from the trackpy DFs 
    # into the big array.
    vrpn_index = 0  # counter value used for tracking the row index in the VRPN file

    # For every frame in the dataset
    print('Building VRPN...')
    for frame_number in data['frame'].unique():

        # For each particle within this frame
        for particle_index, particle_id in enumerate(data['particle'].unique()):
            
            # Try to find the particle position from the lookup table
            try:
                pos = part_pos_lookup.loc[(frame_number, particle_id)]
                x, y = pos['x'], pos['y']  # unpack the x and y positions

            except KeyError:
                # If this particle can't be found, set x and y to None
                x, y = np.NAN, np.NAN

            # Add this data to the main VRPN array
            vrpn_out[vrpn_index, :] = [SEC, USEC, particle_index, frame_number, x, y, *PLACEHOLDER]
            vrpn_index += 1  # bump the VRPN index so we add to the next row next time

    # Now that all the data has been collected, there's some final 
    # formatting that needs to be done before export
    # We'll create this little key in case anyone needs to manually
    # explore the VRPN structure later on
    reference = {
        'Column 1': 'Timestamp (seconds since epoch)',
        'Column 2': 'Microseconds (unused)',
        'Column 3': 'Particle Index',
        'Column 4': 'Frame Number',
        'Column 5': 'X Position (in pixels)',
        'Column 6': 'Y Position (in pixels)',
        'Column 7': 'Z Position (unused)',
        'Column 8': 'Roll (unused)',
        'Column 9': 'Pitch (unused)',
        'Column 10': 'Yaw (unused)',
    }
    reference_df = pd.DataFrame(list(reference.items()), columns=['Column', 'Description'])

    # Store some information about the computer and code
    system_info = {
        'Date Tracked': str(datetime.now().replace(microsecond=0)),
        'OS': platform.system(),
        'OS Version': platform.version(),
        'Username': os.getlogin(),
        'Machine': platform.machine(),
        'Processor': platform.processor(),
        'Node Name': platform.node(),
        'Python Version': platform.python_version(),
    }
    system_info_df = pd.DataFrame(list(system_info.items()), columns=['Item', 'Value'])

    info = {'vrpnLogToMatlabVersion': '05.00',
            'matOutputFileName': f'{file_name}.vrpn.mat',
            'reference': reference_df,
            'systemInfo': system_info_df}
    
    # Package the data into a nested dictionary structure expected 
    # by the VRPN MATLAB parser, including both metadata and tracking data.
    tracking = {'info': info,
                'spot3DSecUsecIndexFramenumXYZRPY': vrpn_out}
    
    # Top-level container for export
    vrpn = {'tracking': tracking}

    # Now save that container as a .vrpn.mat file
    print('\n')
    print(f'Saving results for {file_name}...')
    savemat(path, vrpn, long_field_names=True)
    return
