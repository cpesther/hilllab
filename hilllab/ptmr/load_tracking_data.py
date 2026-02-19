# Christopher Esther, Hill Lab, 2/16/2026
import pandas as pd

from ..utilities.load_vrpn import load_vrpn
from ..ptmr._format_vrpn import _format_vrpn

def load_tracking_data(path, fps, camera, magnification, 
                       pipeline='python', units='um'):

    """
    Loads tracking data from either the MATLAB or Python pipeline and 
    applies all formatting expected by other functions in this module.

    ARGUMENTS:
        fps (int): the frame rate of the VRPN used for converting frame 
            numbers to timestamps. 
        camera (str): the three charcter code used for pulling the 
            pixel width of the camera for converting the coordiantes 
            into um from pixels.
        magnification (float): the factor of magnification applied when
            this video was recorded. 
        units (string): the units that the coordiates should be returned
            using. Defaults to 'um', but valid values include 'm', 'cm', 
            'mm', 'um', and 'nm'.
    """

    # Load the tracking data
    if pipeline == 'matlab':
        raw_data = load_vrpn(path)
    else:
        vrpn_data = pd.read_csv(path)

    # Format the data
    vrpn_data = _format_vrpn(raw_data, fps=fps, camera=camera, 
                    magnification=magnification, units=units)
    
    return vrpn_data
