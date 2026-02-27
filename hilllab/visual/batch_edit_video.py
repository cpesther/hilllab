# Christopher Esther, Hill Lab, 2/27/2026
import os
from pathlib import Path

from ..utilities.walk_dir import walk_dir
from ..utilities.print_progress_bar import print_progress_bar
from .edit_video import edit_video

def batch_edit_video(input_folder, output_folder, **kwargs):

    """
    Runs the edit_video function on all videos found within a folder and
    its subfolders. 

    ARGUMETNS:
        input_folder (string): the path to the folder containing videos and/or
            containing subfolders with videos
        output_folder (string): the path to the folder where the converted
            videos should be saved. 
    """

    # Find all video files
    all_files = walk_dir(input_folder, extension=['avi', 'mp4'])

    # Iterate over all and convert
    for i, file in enumerate(all_files):

        # Print a progress bar
        print_progress_bar(title='Editing videos', total=len(all_files), progress=i+1)

        # Calculate the relative path of this video within the input folder
        rel = os.path.relpath(file, input_folder)

        # Create the output path using this relative path
        raw_output_path = Path(output_folder) / Path(rel)
        output_path = raw_output_path.parent / f'{raw_output_path.stem}.avi'

        # Make sure the parent folder exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Run the conversion
        edit_video(video_path=file, output_path=output_path, show_preview=False, **kwargs)

    # Final message
    print(f'\nEditing of {len(all_files)} videos complete!')
