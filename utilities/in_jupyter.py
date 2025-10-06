# Christopher Esther, Hill Lab, 10/2/2025

def in_jupyter():

    """Detects whether is being run in a Jupyter environment."""

    try:
        get_ipython  # type: ignore
        return True
    except NameError:
        return False
