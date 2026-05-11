# Christopher Esther, Hill Lab, 5/7/2026

def safe_execute(function):

    """
    Safely evaluates a function and returns its result, or returns None 
    if any exception occurs.

    This function is useful for accessing file system metadata or other 
    operations that may raise exceptions, such as missing files, 
    permission errors, or transient I/O issues. Instead of wrapping each 
    access in a try/except block, pass the operation as a lambda or callable.

    ARGUMENTS:
        function (callable): A no-argument function or lambda that 
        performs a potentially unsafe operation.

    RETURNS:
        The result of the callable if successful, or None if any 
        exception is raised.
    
    NOTES:
        size = safe(lambda: os.path.getsize('path/to/file'))
    """

    # Try to run the requested function/lambda
    try:
        return function()

    # Return None if it fails
    except Exception:
        return None
    