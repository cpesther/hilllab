# Christopher Esther, Hill Lab, 2/12/2026

def _format_vrpn(data, fps):

    """
    Takes the dataframe from a loaded VRPN and formats it to the expected 
    structure used in PTMR processing. 

    Key Changes:
        1. Convert timestamp column to actual values using frame number
        and fps
        2. Drop the microseconds column
        3. Sort by particle ID and frame number

    ARGUMENTS:
        data (pandas.DataFrame): the dataframe with the data from the loaded
            VRPN.
        fps (int): the frame rate of the VRPN used for converting frame 
            numbers to timestamps. 

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
    return data
