# Christopher Esther, Hill Lab, 2/16/2026
from pathlib import Path
import json

def _get_camera_info(camera, magnification=None):

    """
    Returns various information about a specific camera, most often used
    for calculating the pixel size given a certain magnification. 

    ARGUMENTS:
        camera (string): the three character code indicating what camera
            properties should be returned.
        magnification (float): the factor of magnification applied when
            this video was recorded. For example, a value of 40 
            indicates 40x magnification.

    RETURNS:
        camera_data (dict): a dictionary of camera data

    NOTES:
        Uses the cameras.json file stored in this same submodule. 
    """

    # Load the library of camera dataLibrary of raw pixel sizes for each camera
    module_dir = Path(__file__).parent
    json_path = module_dir / 'cameras.json'

    with open(json_path, 'r', encoding='utf-8') as f:
        all_camera_data = json.load(f)

    # Pull the information using the requested camera code
    camera_data = all_camera_data[camera]

    # Calculate pixel size if given a magnification
    if magnification is not None:

        # Check appropriateness of magnification value
        if magnification < 1:
            raise ValueError(f'{magnification} is not a valid value for magnification')
        
        # Calculate magnified pixel width
        magnified_pixel_width_um = camera_data['pixel_width_um'] / magnification

        # Add this value to the camera data dictionary
        camera_data['magnified_pixel_width_um'] = magnified_pixel_width_um

    return camera_data
