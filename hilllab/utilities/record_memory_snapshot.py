# Christopher Esther, Hill Lab, 8/15/2025
import tracemalloc  # for tracing memory allocations
import pickle  # for dumping memory snapshots
from datetime import datetime
import os
tracemalloc.start()  # start memory tracing

def record_memory_snapshot(breakpoint=None, active=True):

    """
    Captures a memory allocation snapshot using tracemalloc and dumps
    the snapshot as a pkl file into the app data folder.

    ARGUMENTS:
        breakpoint (str): a value that can be added to the file name
            to more clearly indicate where the snapshot is being taken.
        active (bool): allows us to "turn off" monitoring easily when
            incorporated into other functions without needing to nest 
            this function within a conditional.
    """

    if active:

        # Take the snapshot
        snapshot = tracemalloc.take_snapshot()

        # Import the folder to which the snapshots are saved
        from . import SNAPSHOT_FOLDER_PATH

        # Create the breakpoint text
        if not breakpoint:  # If none provided, use an empty string
            breakpoint_text = ''
        else:  # Otherwise the text is just the provided breakpoint
            breakpoint_text = breakpoint

        # Calculate our file name and file path
        current_datetime = str(datetime.now().timestamp())
        file_name = f'snapshot_{breakpoint_text}_{current_datetime}.pkl'
        snapshot_file_path = os.path.join(SNAPSHOT_FOLDER_PATH, file_name)
        
        # Save the snapshot as a pickle file
        with open(snapshot_file_path, 'wb') as f:
            pickle.dump(snapshot, f)
