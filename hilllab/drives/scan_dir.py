# Christopher Esther, Hill Lab, 5/7/2026

from ..utilities.yeild_dir import yield_dir
from .scan_file import scan_file
from .sweep_db import sweep_db
from .compile_db import compile_db

def scan_dir(path, dbconnection, trigger):

    """
    This function will scan all files located within a given directory
    and all of its sub directories. 
    
    ARGUMENTS:
        path (str): the path at which scanning should begin
        dbconnection (DBConnection): the database connection object used
            to write the data to the .db file. 
        trigger (string): controls how the data from this scan is used. 
            A value of 'build' will force data entry into the connected
            database, while a value of 'verify' will only return the item
            info without touching the database. 
    """

    # Set up some counters 
    scan_counter = 0
    failed_scan_counter = 0
    consecutive_failures = 0

    # Iterate over each file
    for file_path in yield_dir(path=path):

        # Perform the scan
        scan_counter += 1
        try:
            scan_file(file_path=file_path, dbconnection=dbconnection, trigger=trigger)
            consecutive_failures = 0  # reset consecutive on success
        
        # Handle scanning errors
        except Exception as e:
            failed_scan_counter += 1
            consecutive_failures += 1
            print(f'FAIL {e}')

        # Check to make sure we dont have too many consecutive failures
        if consecutive_failures > 10:
            raise SystemError('Scan ended due to too many consecutive failures')
        
        # Commit changes ever 100 files scanned
        if scan_counter % 100 == 0:
            print(f'Total files scanned: {scan_counter}', end='\r')
            dbconnection.conn.commit()
        
    # Clean up any mess by running sweep and compile
    print('Vacuuming database. This may take a minute...')
    sweep_db(dbconnection=dbconnection)
    compile_db(dbconnection=dbconnection)

    # Do one last commit
    dbconnection.conn.commit()

    # Print confirmation
    print(f'Completed scan of {path}')
