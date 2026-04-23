# ellen han, 4/20/2026

import os
import keras

def load_models(path):
    """
    loads a bunch of models into a list.
    
    ARGUMENTS:
        path (str): path to folder where models are
        
    RETURNS:
        models (list): list of models
    """

    if not os.path.isdir(path):
        raise SyntaxError('path not found.')

    models = []
    
    for file in os.listdir(path):
        if file.endswith('.keras'):
            file_path = os.path.join(path, file)
            try:
                model = keras.models.load_model(file_path)
                models.append(model)
            except Exception:
                pass
                
    print(f'loaded {len(models)} models.')
    
    return models