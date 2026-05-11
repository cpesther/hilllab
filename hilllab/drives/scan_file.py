# Christopher Esther, Hill Lab, 5/7/2026
from pathlib import Path
import os
import time

from .safe_execute import safe_execute

def scan_file(file_path, dbconnection, trigger=None, update_queue=None):

    """
    Collects detailed metadata about one given file or directory path The 
    collected information is then formatted and inserted into the 'files' 
    table of the .db file specified via the DBConnection object. 

    ARGUMENTS:
        file_path (string): the path to the file to be scanned
        dbconnection (DBConnection): the database connection object used
            to write the data to the .db file. 
        trigger (string): controls how the data from this scan is used. 
            A value of 'build' will force data entry into the connected
            database, while a value of 'verify' will only return the item
            info without touching the database. 
    
    NOTES: 
        The changes to the database are not committed during this function.
        This process needs to be handled by whichever function calls
        this one (and is presumabably iterating over many files to be
        scanned).

    """
    
    # A dict to store our item information
    item_info = {}

    # Calculate the path of this item relative to the database 
    raw_path = Path(os.path.realpath(file_path))
    base_path = Path(os.path.realpath(Path(dbconnection.db_path).parent))
    relative_path = raw_path.relative_to(base_path)

    # Start compiling some information
    item_info['path'] = relative_path.as_posix()
    item_info['dir_path'] = os.path.dirname(relative_path.as_posix())
    item_info['name'] = relative_path.stem

    # Scan metadata
    item_info['scanned_time'] = time.time()
    item_info['scan_trigger'] = trigger
    item_info['scan_source'] = os.getlogin()
    
    # Try to gather all of the relevant metadata
    try:
        item_stats = os.stat(raw_path)
        item_info['modified_time'] = safe_execute(lambda: item_stats.st_mtime)
        item_info['created_time'] = safe_execute(lambda: item_stats.st_ctime)
        item_info['ino'] = safe_execute(lambda: str(item_stats.st_ino))
        item_info['dev_id'] = safe_execute(lambda: str(item_stats.st_dev))
        item_info['nlink'] = safe_execute(lambda: str(item_stats.st_nlink))
        item_info['uid'] = safe_execute(lambda: str(item_stats.st_uid))
        item_info['gid'] = safe_execute(lambda: str(item_stats.st_gid))
        
        # If the item is a folder
        if os.path.isdir(raw_path):
            item_info['is_directory'] = True
        
        # If the item isn't a folder
        else:
            item_info['is_directory'] = False
            extension = safe_execute(lambda: relative_path.suffix)
            item_info['extension'] = extension
            item_info['suffixes'] = safe_execute(lambda: ''.join(relative_path.suffixes))
            item_info['size'] = safe_execute(lambda: item_stats.st_size)

        # If we made it through all the scans, set success to true
        item_info['success'] = True

    # If any of the scanning failed
    except Exception:
        item_info['success'] = False
    
    # Now that our scanning is done, let's decide what to do with this 
    # file's information, chiefly by determining whether this file already
    # exists in the connected database.

    # If we just want to verify the details of this file (not write it 
    # to any database), then we can just return the details here.
    if trigger == 'verify':
        return item_info

    # If scanning in build mode (creating a new database), this file
    # does not already exists. 
    if trigger == 'build':
        exists = False
    else:
        # Search for this file in the db via relative path
        dbconnection.cursor.execute('SELECT 1 FROM files WHERE path = ?', (str(relative_path),))
        exists = dbconnection.cursor.fetchone() is not None

    # Determine what to do with the data depending on if the file exists
    if exists:  # if the file already exists

        # Try to update this file's info in the database
        try:
            update_columns = ', '.join([f"{k} = ?" for k in item_info if k != 'path'])
            update_values = tuple(item_info[k] for k in item_info if k != 'path')
            sql = f"UPDATE files SET {update_columns} WHERE path = ?"
            dbconnection.cursor.execute(sql, update_values + (item_info['path'],))
        except Exception as e:
            print(f"Insert failed: {e} on {raw_path}")
    
    # If it doesn't exist, add it to the database
    else:
        try:  # inset a new row
            columns = ', '.join(item_info.keys())
            placeholders = ', '.join(['?'] * len(item_info))
            values = tuple(item_info.values())
            sql = f"INSERT INTO files ({columns}) VALUES ({placeholders})"
            dbconnection.cursor.execute(sql, values)
        except Exception as e:
            print(f"Insert failed: {e} on {raw_path}")
