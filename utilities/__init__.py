# __init__.py for the utilities subpackage.
# Initializes package-level imports and configuration.

"""
A group of miscellaneous functions that help with various 
non-computational tasks.
"""

# Generic Python imports
import platform
import os
from datetime import datetime

# Import all the functions included in this subpackage
# Display stuff
from .format_duration import format_duration
from .progress_bar import progress_bar
from .print_dict_table import print_dict_table
from .pretty_timestamp import pretty_timestamp

# Messages and recording
from .record_message import record_message
from .record_memory_snapshot import record_memory_snapshot
from .record_cpu_usage import record_cpu_usage

# Caching and appdata
from .cache_clear import cache_clear
from .cache_view import cache_view

# We also need to do some initialization of the location where certain
# analytics and logging data is stored. We'll do that here. 

# Detect what platform we're running on
system = platform.system()

# Determine the path to the app data folder based on the system
if system == 'Windows':  # Windows
    base = os.getenv('APPDATA')
elif system == 'Darwin':  # macOS
    base = os.path.expanduser('~/Library/Application Support')
else:  # Linux/Unix
    base = os.path.expanduser('~/.config')

# Create the path to the app data folder
# This variable will be referenced by other 'record_' functions so that
# they know where to write their data.
APP_DATA_FOLDER = os.path.join(base, 'particlehill')

# If this folder doesn't already exist...
if not os.path.exists(APP_DATA_FOLDER):

    # Then we'll create it
    os.makedirs(APP_DATA_FOLDER, exist_ok=True)

# Once we've ensured that this folder exists...
current_datetime = str(datetime.now().timestamp()).replace('.', '_')

# Set the log file path
log_name = f'log_{current_datetime}.csv'
LOG_FILE_PATH = os.path.join(APP_DATA_FOLDER, log_name)
record_message('Utilities log initialized!', print_message=False)

# Create a folder to store any captured memory snapshots
snapshot_folder_name = f'snapshots_{current_datetime}'
SNAPSHOT_FOLDER_PATH = os.path.join(APP_DATA_FOLDER, snapshot_folder_name)
os.makedirs(SNAPSHOT_FOLDER_PATH, exist_ok=True)

# Create a folder to store CPU usage data
cpu_folder_name = f'cpu_{current_datetime}'
CPU_FOLDER_PATH = os.path.join(APP_DATA_FOLDER, cpu_folder_name)
os.makedirs(CPU_FOLDER_PATH, exist_ok=True)
