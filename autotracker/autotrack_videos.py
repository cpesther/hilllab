# Christopher Esther, Hill Lab, 8/15/2025
import os
import time
import platform
from datetime import datetime

from tkinter import filedialog
from IPython.display import clear_output
import pandas as pd
from scipy.io import savemat  # for saving MatLab files
import numpy as np  # for math and data processing
import trackpy as tp  # for particle tracking
import pims  # python image sequence library for manipulating videos

def autotrack_videos(video_path=None, save_path=None, bead_size_pixels=21, 
                     trajectory_fraction=1.0, max_travel_pixels=5, memory=0,
                     invert=False, performance_mode='safe', 
                     return_file_details=False):

    """
    Automatically processes and tracks particles in a batch of AVI 
    videos.

    This function opens a file browser window, walks through all 
    subdirectories to identify AVI files, performs grayscale conversion, 
    detects and links particles using TrackPy, filters the results, 
    and saves the output as a VRPN file in the .mat format.

    ARGUMENTS:
        video_path (str): path to the folder with videos
        save_path (str): path to the folder where VRPNs should be saved
        bead_size_pixels (int, optional): Estimated diameter of the 
            particles in pixels. Default is 21.
        trajectory_fraction (float, optional): Minimum fraction of frames a 
            particle must appear in to be retained after filtering. 
            Default is 1.0.
        max_travel_pixels (int, optional): Maximum number of pixels a particle 
            can travel between frames for TrackPy to consider it to be
            the same particle. Default is 5. 
        memory (int, optional): Memory parameter for TrackPy's linking, 
            specifying how long particles are remembered between frames. 
            Default is 0.
        invert (bool, optional): when false, bright spots on a dark background
            will be tracked. When true, dark spots on a bright background
            will be tracked. 
        performance_mode (string, 'safe', 'slow', or 'fast'): Controls 
            how many processes are used by TrackPy to allow this task to
            be run safely in the background or sped up on demand. 
        return_file_details (bool, optional): allows the function to 
            return a dict containing file details useful for higher level
            functions. Defaults to false. 

    OUTPUTS:
        Saves one `.vrpn.mat` file per video in `save_path`. These 
        contain particle position data in a structure compatible with 
        VRPN-based systems or legacy MATLAB tracking tools.
    """

    # Start by asking for the video and save directories, if needed
    if not video_path:
        video_path = filedialog.askdirectory(title=f'Select a folder with videos')
    if not save_path:
        save_path = filedialog.askdirectory(title=f'Select a destination folder')

    # Make sure paths were provided
    if not video_path or not save_path:
        print('Missing one or more path values')
        return

    # Walk the provided directory to determine the total number of files
    flist = [] # array of obnoxiously long, full filenames
    for root, _, files in os.walk(video_path):
        for file in files:
            if file.endswith(".avi"):
                flist.append(os.path.join(root, file))

    # Calculate total number of files and print some messages
    nfiles = len(flist)

    # Set some invert text
    if invert:
        tracking_text = 'Dark spots on a white background'
    else:
        tracking_text = 'Bright spots on a black background'

    # Print out these paths and the input variables and require confirmation
    print('Please confirm the parameters below:')
    print(f'Input Folder:    {video_path}')
    print(f'Output Folder:   {save_path}')
    print(f'Bead Size:       {bead_size_pixels} pixels')
    print(f'Bead Color:      {tracking_text}')
    print(f'Videos Found:    {nfiles}')

    confirmation = input('\nAre the values correct? (y/n):')
    if confirmation.upper() != 'Y':
        print('Parameters not confirmed')
        return
    
    # Print a message to start
    clear_output(wait=True)  # clear all print outputs
    print('Beginning batch autotracking')
    batch_start_time = time.time()  # start a timer for the whole batch    

    # Before we begin iterating, we'll define and wrap a pims function
    # that takes just the green channel from any provided image. 
    @pims.pipeline
    def gray(image):
        return image[:, :, 1]  # take just the green channel
    
    # Create a dict for storing file details
    file_details = {}

    # Now we can iterate over each individual movie
    for file in flist:

        # First we'll determine file name by splitting the path
        file_name = os.path.basename(file)
        print(f'Starting processing on {file_name}')

        # Convert the file to grayscale and extract the frames
        print(f'Converting file to grayscale')
        
        frames = gray(pims.PyAVReaderIndexed(file))
        fv = []
        for fr in range(len(frames)):
            frame = frames[fr]
            fv.append(frame)

        # Start a time and print a message before we begin tracking
        track_start_time = time.time()  # start a timer for this video
        print('\n')  # to start a new line after the progress bar above
        print(f'Finding particle positions in frames')

        # Determine how many processes to allow TrackPy to use
        if performance_mode == 'slow':
            num_processes = os.cpu_count() / 2
        elif performance_mode == 'fast':
            num_processes = os.cpu_count()
        else:  # 'safe' mode, or any other value
            num_processes = os.cpu_count() - 2

        # Track the video
        minmass_value = 750 * (bead_size_pixels / 21) ** 3
        particle_positions = tp.batch(fv, bead_size_pixels, 
            minmass=minmass_value, processes=int(num_processes), invert=invert)

        # Once finished tracking, display the time taken
        total_track_time = (time.time() - track_start_time)
        print(f'Finished finding particles in {total_track_time / 60} minutes')

        # Now that we have all the particle positions, let's link them 
        # into trajectories which track how individual particles are 
        # moving from frame to frame.
        print('Linking particle positions to create trajectories')
        try:
            t = tp.link(particle_positions, max_travel_pixels, memory=memory)
        except:
            print('Unable to link beads in this video')
            continue

        # Now with the trajectories created, let's filter out those
        # that have fewer points than a given threshold (i.e. they
        # don't last long enough to be valuable).
        clear_output(wait=True)
        print(f'Applying filters to {file_name}')

        # Calculate the minimum number of frames that a trajectory must
        # persist in order to be kept
        frame_threshold = len(frames) * trajectory_fraction
        
        # Do the filtering in three steps
        # STEP 1: Remove trajectories that do not persist long enough
        n_raw = t['particle'].nunique()
        print(f'{n_raw} trajectories present before filtering')

        t1 = tp.filter_stubs(t, frame_threshold)
        n_t1 = t1['particle'].nunique()
        print(f'{n_t1} trajectories present after filter 1')

        # STEP 2: Now remove trajectories that do not match the expected
        # characteristics of the beads. Here we filter out based on mass, 
        # the size of the beads, and the eccentricity (a measure of elongation).
        size_lower = 3.5 * (bead_size_pixels / 21)
        size_upper = 7.5 * (bead_size_pixels / 21)

        # Here's the code for the second filter
        t2 = t1[
            (t1['mass'] < 35000) &
            (t1['size'] > size_lower) &
            (t1['size'] < size_upper) &
            (t1['ecc'] < 0.3)
        ]
        
        n_t2 = t2['particle'].nunique()
        print(f'{n_t2} trajectories present after filter 2')

        # STEP 3: Some particles might have had enough frames in t1 but 
        # dropped below the threshold in t2 due to filtering. This step 
        # ensures all remaining trajectories are still valid and long enough.
        t3 = tp.filter_stubs(t2, frame_threshold)
        n_t3 = t3['particle'].nunique()
        print(f'{n_t3} trajectories present after filter 3')

        # Now we can take all of the DataFrames from trackpy and format 
        # them into .vrpn.mat files that use a similar structure to that
        # produced by SpotTracker. This conversion process will require 
        # us to create a 2D array (named vrpn_out) and iteratively add 
        # all of the data to it.
        print('Converting and exporting data...')

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
        vrpn_out = np.zeros((len(frames) * n_t3, 10))

        # Take the t3 particle trajectories and create a pivot table
        # using the frame and particle attributes as the index. Since 
        # we need to pull data from this table in each step, formatting
        # it as a multi-index table will make this must faster
        part_pos_lookup = t3.set_index(['frame', 'particle'])[['x', 'y']]

        # Here's where we iteratively add the data from the trackpy DFs 
        # into the big array.
        print(f'Building VRPN...')
        vrpn_index = 0  # counter value used for tracking the row index in the VRPN file

        # For every frame in the dataset 
        for frame_number in t3['frame'].unique():

            # For each particle within this frame
            for particle_index, particle_id in enumerate(t3['particle'].unique()):
                
                # Try to find the particle position from the lookup table
                try:
                    pos = part_pos_lookup.loc[(frame_number, particle_id)]
                    x, y = pos['x'], pos['y']  # unpack the x and y positions

                except KeyError:
                    # If this particle can be found, set x and y to None
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
        reference_df = pd.DataFrame(list(reference.items()), columns=["Column", "Description"])

        # Store some information about the computer and script
        from .. import __version__
        system_info = {
            "File Tracked": str(datetime.now().replace(microsecond=0)),
            "OS": platform.system(),
            "OS Version": platform.version(),
            "Machine": platform.machine(),
            "Processor": platform.processor(),
            "Node Name": platform.node(),
            "Python Version": platform.python_version(),
            "hilllab Module Version": __version__
        }
        system_info_df = pd.DataFrame(list(system_info.items()), columns=["Item", "Value"])

        info = {'vrpnLogToMatlabVersion': '05.00',
                'matOutputFileName': f'{file}.vrpn.mat',
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
        print(f'Saving results for {file}...')
        save_name = os.path.join(save_path, f'{file_name[:-4]}.vrpn.mat')
        savemat(save_name, vrpn, long_field_names=True)

        # Some final messages for this file
        print(f'Saved {file_name} to {save_name}')

        total_file_time = time.time() - track_start_time
        print(f'Finished processing in {total_file_time / 60} minutes!')
        
        # Save these file details to the dict
        file_details[file]['save_name'] = save_name

        # Wait one second and clear all printed outputs
        time.sleep(1)
        clear_output(wait=True)

    print(f'Finished processing all files in {video_path}')
    
    total_batch_time = time.time() - batch_start_time
    print(f'Finished processing batch in {round(total_batch_time / 60, 2)} minutes')
    print(f'VRPNs saved to {save_path}')

    if return_file_details:
        return file_details
