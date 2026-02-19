# Christopher Esther, Hill Lab, 2/9/2026
from pathlib import Path
from .batch_subtract_drift import batch_subtract_drift

def process_vrpns(folder, camera='GS3', magnification=40, bead_size=1, fps=120, long_video=False, 
                  drift_subtraction='linear', pipeline='python'):

    """
    Docstring for process_VRPNs

    ARGUMENTS:
        folder (string): highest level directory containing subdirectories 
            with VRPNs
        camera (string): camera identifier, expected 'GS3' or 'FL3'
        bead_size (int): bead size in pixels
        long_video (bool): True if long video, False otherwise
        drift_subtraction (None or string): controls the method of drift
            subtraction applied to the VRPNs. If None, then no drift
            subtraction will be applied. 
        pipeline (string): either 'python' or 'matlab'. Controls whether
            files are saved as MATLAB files compatible with legacy code
            or as CSV and Excel docs compatible with this Python library. 
    """

    



