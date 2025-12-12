# Christopher Esther, Hill Lab, 8/15/2025
from datetime import datetime
import os
import psutil

def record_cpu_usage(interval=1, stop_event=None):

    """
    Periodically record the current CPU usage percentage to a file in
    the app data folder.

    ARGUMENTS:
        interval (float): Number of seconds between each CPU usage sample.
        stop_event (threading.Event): Event used to signal the function 
            to stop tracking.
    """

    # Get the path to the CPU monitoring folder
    from utilities import CPU_FOLDER_PATH

    # Create a file that we'll use to store CPU data
    cpu_file_name = f'{str(datetime.now().timestamp()).split('.')[0]}.csv'
    cpu_file_path = os.path.join(CPU_FOLDER_PATH, cpu_file_name)

    # Until the function is killed by the stop event
    while not stop_event.is_set():

        # Capture CPU usage
        cpu = psutil.cpu_percent(interval=interval)

        # Write it to the file
        with open(cpu_file_path, 'a') as f:
            f.write(f'{str(cpu)}\n')
