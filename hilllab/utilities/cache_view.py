# Christopher Esther, 08/15/2025
import os
import subprocess
import platform

def cache_view():

    """Open the cache/appdata folder in the system file browser."""

    from . import APP_DATA_FOLDER
    
    # Check the system we're running on
    system = platform.system()

    if system == "Windows":
        os.startfile(APP_DATA_FOLDER)
    elif system == "Darwin":  # macOS
        subprocess.run(["open", APP_DATA_FOLDER])
    else:  # Linux and others
        subprocess.run(["xdg-open", APP_DATA_FOLDER])
