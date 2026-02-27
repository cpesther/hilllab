# Christopher Esther, Hill Lab, 1/28/2026
from ..utilities.walk_dir import walk_dir
from ..utilities.print_progress_bar import print_progress_bar
from ..visual.bin_video import bin_video

def batch_bin_video(input_folder, bin_size, extension='avi'):

    """
    Runs the bin_video function on every video in a folder and its subfolders.
    
    ARGUMENTS:
        input_folder (str): the path to the folder of videos to bin
        bin_size (int): the size of the bins of pixels
        type (str): the file type extension of the videos to be binned. 
    """

    # List all files in directory and subfolders
    all_videos = walk_dir(input_folder, extension=extension)

    # Just to get it to display at 0 before iteration since each video can take a while
    print_progress_bar(progress=0, total=len(all_videos), title='Binning videos...') 
    
    # Run binning on each file 
    for i, video in enumerate(all_videos):
        bin_video(video_path=video, bin_size=bin_size, print_output=False)
        print_progress_bar(progress=i+1, total=len(all_videos), title='Binning videos...')
