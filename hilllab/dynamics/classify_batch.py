# Christopher Esther, Hill Lab, 5/1/2026
from pathlib import Path
import shutil
import pandas as pd

from .classify_GMM import classify_GMM

def classify_batch(h5_path, method='gmm'):

    """
    Takes the primary analysis data from a h5 file and classifies each 
    bead as either transiting, oscillating, or stuck. Two methods for this
    method exist: 'gmm' uses a Gaussian mixture model based on the
    parameters from the summary table, while 'model' uses a machine learning
    model on the instantaneous position data of each particle. 

    ARGUMENTS:
        h5_path (string): the file path to the h5 file to classify
        method (string): either 'gmm' for the Gaussian mixture model 
            method or 'model' for the machine learning model method.
    """

    # If using the Gaussian mixture model method
    if method.upper() == 'GMM':
        classified_summary, _ = classify_GMM(h5_path)

    # If using the machine learning model method
    elif method.upper() == 'MODEL':
        raise ValueError('Model classification is not yet implemented')

    # Handle unknown method inputs
    else:
        raise ValueError(f"'{method}' is not a valid method method")
    
    # Create a copy of the provided h5 file with a new name to store the classifications
    print('Creating new classifications file. This may take a minute...')
    classified_name = f'{Path(h5_path).stem}.classify.h5'
    classified_path = Path(h5_path).parent / classified_name
    shutil.copy(h5_path, classified_path)

    # Save the new summary table with classifications into this new h5 file
    print('Saving classifications to file...')
    with pd.HDFStore(classified_path, mode='a') as store:
        store.put(
            'summary',
            classified_summary,
            format='table',
            data_columns=['uuid', 'path', 'particle_id']
        )

    print('Classification finished!')
