# Christopher Esther, Hill Lab, 5/7/2026

def sweep_db(dbconnection):

    """
    Cleans up the database by removing duplicate files, deleting 
    orphaned keywords, and freeing up space. 
    """

    # <<<<< REMOVE DUPLICATE FILES >>>>>
    query = """
    DELETE FROM files
    WHERE id NOT IN (
        SELECT id FROM (
            SELECT id
            FROM files f1
            INNER JOIN (
                SELECT path, MAX(scanned_time) AS max_time
                FROM files
                GROUP BY path
            ) f2 ON f1.path = f2.path AND f1.scanned_time = f2.max_time
        )
    )
    """
    dbconnection.cursor.execute(query)
    num_duplicate_files = dbconnection.cursor.rowcount

    return num_duplicate_files
