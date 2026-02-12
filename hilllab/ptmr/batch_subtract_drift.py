# Christopher Esther, Hill lab, 2/12/2026
from pathlib import Path
import os
import pandas as pd
from ..utilities.load_vrpn import load_vrpn
from ._format_vrpn import _format_vrpn
from .drift._subtract_linear_drift import _subtract_linear_drift

def batch_subtract_drift(files, fps, method='linear', drift_start_time=None, 
                         drift_end_time=None, skip_existing=True, pipeline='python'):

    """
    Docstring for batch_subtract_drift
    
    :param vrpn_files: Description
    :param method: Description
    """

    # Iterate over every path in the list of VRPN files
    for path in files:

        # Generate the appropriate output path based on the pipeline
        stem = Path(path).name.split('.')[0]
        if pipeline == 'python':
            drift_subtracted_path = Path(path).parent / f'{stem}.drift.track.csv'
        
        elif pipeline == 'matlab':
            drift_subtracted_path = Path(path).parent / f'{stem}.evt.evt.mat'

        else:
            raise ValueError(f"'{pipeline}' is not a valid pipeline value")
        
        # Check whether this output path exists, and skip if true and requested
        if (os.path.exists(drift_subtracted_path) and (skip_existing)):
            continue
        
        # Load the file type depending on the pipeline
        if pipeline == 'matlab':
            data = load_vrpn(path)    # load from .vrpn.mat
        else:
            data = pd.read_csv(path)  # load from .track.csv

        # Format the VRPN data
        data = _format_vrpn(data=data, fps=fps)

        # Determine the default drift window if none was provided
        if drift_start_time is None:
            drift_start_time = data['timestamp'].min()  # beginning of the video

        if drift_end_time is None:
            drift_end_time = data['timestamp'].max()  # end of the video

        # Apply the requested method of drift subtraction
        if method == 'linear':
            drift_subtracted_data = _subtract_linear_drift(data, drift_start_time, drift_end_time)
        else:
            raise ValueError(f"'{method}' is not a valid value for method.")
        
        # And finally export the files based on the pipeline
        if pipeline == 'matlab':
            pass
            # TODO implement this

        else:
            drift_subtracted_data.to_csv(drift_subtracted_path, header=True, index=False)
        