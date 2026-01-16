# Christopher Esther, Hill Lab, 1/9/2026
from ..utilities.walk_dir import walk_dir
from ..visual.normalize_video_brightness import normalize_video_brightness
from ..utilities.print_progress_bar import print_progress_bar

def batch_normalize_video_brightness(folder_path, type='avi', **kwargs):

    """
    Performs video brightness normalization on all videos of a certain
    type within a folder. 
    
    ARGUMENTS:
        folder_path (str): the path to the folder containing the videos
        type (str): the file extension of the video files to process
    """

    # Walk the folder to find all videos
    all_videos = walk_dir(folder_path, type=type)
    n_videos = len(all_videos)

    # Iterate over each video
    for i, video in enumerate(all_videos):

        # Print a progress bar
        print_progress_bar(progress=i+1, total=n_videos, title='Normalizing videos')

        # Run normalization
        normalize_video_brightness(video_path=video, **kwargs)
