# Christopher Esther, Hill Lab, 1/16/2026

def dynamics_pipeline():

    """
    Runs a series of bead dynamics calculations on all VRPN files within 
    a folder and its subfolders. Skips files for which processing has
    already completed to allow for iterative expansion of datasets.

    ARGUMENTS:
        folder_path (str): path (string): the path to the VRPN file
        fps (int): the frame rate of the video
        pixel_width (float): if provided, distance-related 
            values will be converted with this factor allowing the conversion
            of pixels into any arbitrary unit.
         
    """

    try:
        from IPython.display import clear_output
        in_jupyter = True
    except ModuleNotFoundError:
        in_jupyter = False