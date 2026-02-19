# Christopher Esther, Hill Lab, 2/12/2026
from ..visual._get_camera_info import _get_camera_info

def _format_vrpn(data, fps, camera, magnification, units='um'):

    """
    Takes the dataframe from a loaded VRPN and formats it to the expected 
    structure used in PTMR processing as well as converting coordinates
    into micrometers instead of pixels. 

    Key Changes:
        1. Convert timestamp column to actual values using frame number
        and fps
        2. Drop the microseconds column
        3. Sort by particle ID and frame number
        4. Convert coordinates into units of um using the u

    ARGUMENTS:
        data (pandas.DataFrame): the dataframe with the data from the loaded
            VRPN.
        fps (int): the frame rate of the VRPN used for converting frame 
            numbers to timestamps. 
        camera (str): the three charcter code used for pulling the 
            pixel width of the camera for converting the coordiantes 
            into um from pixels.
        magnification (float): the factor of magnification applied when
            this video was recorded. 
        units (string): the units that the coordiates should be returned
            using. Defaults to 'um', but valid values include 'm', 'cm', 
            'mm', 'um', and 'nm'. Any other value will return the
            coordinates in their native unit of pixels. 

    RETURNS:
        data (pandas.DataFrame): the loaded data with all
            formatting changes applied. 
    """

    # Convert the frame numbers into seconds values using the FPS
    data['timestamp'] = data['frame'] * (1 / fps)

    # Get rid of the microseconds column; we don't need it
    data.drop(columns=['microseconds'], inplace=True)

    # Sort by the particle ID and frame number
    data.sort_values(by=['particle_id', 'frame'], inplace=True)

    # Pull the magnified pixel width using the camera and magnification values
    camera_info = _get_camera_info(camera=camera, magnification=magnification)
    magnified_pixel_width_um = camera_info['magnified_pixel_width_um']

    # Determine the conversion factor to be used on the coordinates based on
    # the provided pixel argument
    if units == 'm':
        conversion_factor = magnified_pixel_width_um / 1e6
    elif units == 'cm':
        conversion_factor = magnified_pixel_width_um / 1e4
    elif units == 'mm':
        conversion_factor = magnified_pixel_width_um / 1e3
    elif units == 'um':
        conversion_factor = magnified_pixel_width_um
    elif units == 'nm':
        conversion_factor = magnified_pixel_width_um * 1e3
    else:
        conversion_factor = 1  # otherwise just return in pixels

    # Apply this conversion factor to the coordinate data (X, Y, and Z)
    for column in ['x', 'y', 'z']:
        data[column] = data[column] * conversion_factor

    return data
