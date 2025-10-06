# Christopher Esther, Hill Lab, 10/06/2025
import os
from tkinter import filedialog

from ..utilities.pretty_timestamp import pretty_timestamp
from ..utilities.print_dict_table import print_dict_table

try:
    from IPython.display import clear_output, display
except:
    pass

def autotrack_select_paths():

    """
    Opens file explorer windows to allow the user to select video and 
    save directory paths. 
    """

    # Open the video path window
    print('Select a folder containing videos using the file dialog window.')
    video_path = filedialog.askdirectory(title=f'Select a folder with videos')
    
    # Walk that path for some verification
    flist = []  # array of obnoxiously long, full filenames
    for root, _, files in os.walk(video_path):
        for file in files:
            if file.endswith(".avi"):
                flist.append(os.path.join(root, file))
    
    if len(flist) == 0:
        print('ALERT: No .avi files found in this folder.')

    # Select the save path
    print('Select a folder containing videos using the file dialog window.')
    save_path = filedialog.askdirectory(title=f'Select a destination folder')

    try:
        clear_output(wait=True)
    except:
        pass

    if len(video_path) < 1:
        print('ERROR: No video path selected.')
        return (None, None)  # this triggers a handled error in the autotracker
    
    if len(save_path) < 1:
        print('ERROR: No save path selected.')
        return (None, None)
    
    # Format all this information and print
    info = {
        'Video Path': video_path,
        'Save Path': save_path,
        'Videos Found': len(flist),
        'Time Selected': pretty_timestamp()
    }
    print_dict_table(dict=info, title='PATH INFO')

    # Otherwise we can just return the selected paths
    return video_path, save_path
