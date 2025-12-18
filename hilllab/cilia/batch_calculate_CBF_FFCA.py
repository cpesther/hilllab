# Christopher Esther, Hill Lab, 10/13/2025
import os
import gc
from ..cilia.calculate_CBF_FFCA import calculate_CBF_FFCA
from ..utilities.current_timestamp import current_timestamp

# This try/except allows the function to run in a non-Jupyter environment
try:
    from IPython.display import clear_output
except Exception:
    pass


def batch_calculate_CBF_FFCA(path, sampling_rate=60, power_threshold=5,
                             skip_existing=True, bypass_confirmation=False):

    """
    Runs the calculate_CBF_FFCA function on a batch of videos. 

    ARGUMENTS:
        path (string): a path to a folder containing the AVI videos that
            should be processed.
        sampling_rate (int): Frame rate of the video.
        power_threshold (int): Minimum PSD value a pixel must exceed to 
            be considered ciliated.
        skip_existing (bool): whether a video should be skipped if a 
            MATLAB file already exists with the same name. 
        bypass_confirmation (bool): allows the function to skip the 
            confirmation step that typically requires user input. 
    """

    # Walk the provided directory to determine the total number of files
    flist = []  # array of obnoxiously long, full filenames
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".avi"):
                flist.append(os.path.join(root, file))

    # Print out these paths and the input variables and require confirmation
    print('Please confirm the parameters below:')
    print(f'Input Folder:    {path}')
    print(f'Sampling Rate:   {sampling_rate} Hz (fps)')
    print(f'Power Threshold: {power_threshold}')
    print(f'Videos Found:    {len(flist)}')

    if bypass_confirmation:
        confirmation = 'Y'
    else:
        confirmation = input('\nAre the values correct? (y/n): ')

    if confirmation.upper() != 'Y':
        print('Parameters not confirmed')
        return
    
    # Print a message to start
    try:
        clear_output(wait=True)  # clear all print outputs
    except:
        pass

    # Run the calculation on each video
    start_time = current_timestamp()
    print(f'Started batch CBF/FFCA on {start_time}')
    for index, video_path in enumerate(flist):

        # Brief status message
        print(f'Starting video {index + 1} of {len(flist)} on {current_timestamp()}')

        # Run the calculations
        calculate_CBF_FFCA(video_path=video_path, sampling_rate=sampling_rate, 
                           power_threshold=power_threshold,
                           skip_existing=skip_existing)
        
        # Do some manual garbage collection for tighter memory management
        _ = gc.collect()

        # Try to clear the Jupyter output
        try:
            clear_output(wait=True)
        except:
            pass

    print(f'Started batch CBF/FFCA on {start_time}')
    print(f'{len(flist)} videos processed')
    print(f'Finished batch CBF/FFCA on {current_timestamp()}')
    