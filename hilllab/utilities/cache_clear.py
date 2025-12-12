# Christopher Esther, Hill Lab, 8/15/2025
import shutil

def cache_clear():
    
    """
    Deletes the particlehill app data folder and all contents.
    """

    # Import the path to the app data folder
    from . import APP_DATA_FOLDER

    # And try to delete it
    try:
        shutil.rmtree(APP_DATA_FOLDER)
        print('Cache cleared!')

    except:
        print('Unable to clear cache')
