# Christopher Esther, Hill Lab, 9/26/2025
from tkinter import filedialog

from autotrack_videos import autotrack_videos

def autotrack_synced_videos(video_dir=None, save_dir=None, **kwargs):
    
    """
    Runs the standard autotrack_videos.py function but also adds in 
    timestamp data to the VRPN files for time-synced experiments using
    timestamps saved by record_sync_video.m. 
    
    ARGUMENTS:
        video_dir (str): path to the folder with videos
        save_dir (str): path to the folder where VRPNs should be saved
        **kwargs: passed down to autotrack_videos

    OUTPUTS:
        Saves one `.vrpn.mat` file per video in `save_dir`. These 
        contain particle position data in a structure compatible with 
        VRPN-based systems or legacy MATLAB tracking tools.
    """

    # Start by asking for the video and save directories, if needed
    if not video_dir:
        video_dir = filedialog.askdirectory(title=f'Select a folder with videos')
    if not save_dir:
        save_dir = filedialog.askdirectory(title=f'Select a destination folder')

    # Make sure paths were provided
    if not video_dir or not save_dir:
        print('Missing one or more path values')
        return

    # The first step is actually tracking the vidoes
    autotrack_videos(video_dir=video_dir, save_dir=save_dir, **kwargs)

    # Now that the videos are tracked, we can add in the timestamps