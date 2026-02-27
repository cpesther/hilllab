# Christopher Esther, Hill Lab, 2/27/2026
from pathlib import Path
import json

from ._get_camera_info import _get_camera_info
from ..utilities.print_dict_table import print_dict_table

def show_camera_info():

    """
    Prints out all of the specifications for every camera included in
    cameras.json.
    """

    # Load the library of camera dataLibrary of raw pixel sizes for each camera
    module_dir = Path(__file__).parent
    json_path = module_dir / 'cameras.json'

    with open(json_path, 'r', encoding='utf-8') as f:
        all_camera_info = json.load(f)

    for camera in list(all_camera_info.keys()):
    
        # Pull the camera info
        camera_info = _get_camera_info(camera=camera)

        # Print the camera info
        print_dict_table(dict=camera_info, title=camera)
        print('\n')
