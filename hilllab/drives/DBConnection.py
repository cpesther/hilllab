# Christopher Esther, Hill Lab, 5/7/2026
import sqlite3
from pathlib import Path

class DBConnection():

    """
    A class used for connecting to and interacting with a sqlite database
    file. 
    """

    def __init__(self, db_path=None):
        
        # Connect to the database
        self.db_path = db_path  # save the database path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # to allow dict-like parameter access
        self.cursor = self.conn.cursor()

        # Get the path to the default sql schema file
        sql_path = Path(__file__).parent / 'schema.sql'

        # Read and execute the schema file
        with open(sql_path, 'r') as f:
            sql_script = f.read()
        
            # Execute the SQL schema script
            self.cursor.executescript(sql_script)
        
        # Commit changes
        self.conn.commit()
    