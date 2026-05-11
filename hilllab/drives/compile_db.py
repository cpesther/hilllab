# Christopher Esther, Hill Lab, 5/7/2026

def compile_db(dbconnection):

    """
    Makes various edits and updates to the database mostly in regards
    to keeping folder sizes and file counts correct. 
    """

    # Update folder file counts and sizes
    def iterate_directories(dbconnection):

        """
        Iterates over entries where is_directory is True and yields one id
        at a time
        """
        
        dbconnection.cursor.execute("SELECT id, path FROM files WHERE is_directory = 1")

        for id, path in dbconnection.cursor:
            yield (id, path)

    # Iterate overy every directory in the database
    inner_cursor = dbconnection.conn.cursor()  # different cursors so the state of the main on is saved
    update_cursor = dbconnection.conn.cursor()

    # Iterate over each directory
    for directory in iterate_directories(dbconnection=dbconnection):

        dir_id, path = directory

        # Calculate file count
        inner_cursor.execute("""SELECT COUNT(*) FROM files WHERE dir_path = ?""", (path,))
        file_count = inner_cursor.fetchone()[0]

        # Query all files recursively (in folder and its subfolers)
        size = 0
        file_count_recursive = 0

        # Request all files within this directory
        inner_cursor.execute(
            "SELECT size FROM files WHERE dir_path = ? OR dir_path LIKE ?",
            (path, f"{path}/%")
        )

        # Calculate file count and size
        for row in inner_cursor:
            file_count_recursive += 1
            size += row['size'] or 0

        # Add these values into the database
        sql = """UPDATE files SET file_count = ?, file_count_recursive = ?, size = ? WHERE id = ?"""
        update_cursor.execute(sql, (file_count, file_count_recursive, size, dir_id))

    # Commit changes
    dbconnection.conn.commit()
