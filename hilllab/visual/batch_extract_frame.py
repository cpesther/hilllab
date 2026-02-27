# Christopher Esther, Hill Lab, 1/22/2026
from ..utilities.walk_dir import walk_dir
from ..utilities.print_progress_bar import print_progress_bar
from ..visual.extract_frame import extract_frame

def batch_extract_frame(input_folder, output_folder, frame_index=0, scale_percent=100, extension='avi'):

    """
    Runs the extract_frame function on all videos within a folder and 
    its subfolders. 

    ARGUMENTS:
        input_folder (str): the path to the folder containing videos
        output_folder (str): Folder to save the PNGs.
        frame_index (int): the 0-based index of the frame to be saved.
        scale_percent (float): Percentage to downscale the frame (default 100 = no scaling).
        type (str): the file extension of the type of video to process. 
    """

    # Find all videos
    all_videos = walk_dir(input_folder, extension=extension)
    n_videos = len(all_videos)

    # Run extraction on every video
    for i, video_path in enumerate(all_videos):

        # Print a progress bar
        print_progress_bar(progress=i+1, total=n_videos, title='Extracting frames...')

        # Extract the frame
        extract_frame(video_path=video_path, output_folder=output_folder, 
                      frame_index=frame_index, scale_percent=scale_percent)
        