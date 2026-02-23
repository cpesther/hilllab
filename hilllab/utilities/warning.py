# Christopher Esther, Hill Lab, 2/23/2026
import warnings


def enable_simple_warnings():

    """Used to set a cleaner warning format without a bunch of unneeded
    kernel information. """

    # A warning format to clean up unneeded information
    def _simple_warning_format(message, category, filename, lineno, file=None, line=None):
        return f'{category.__name__}: {message}\n'
    
    # Set the format to the above function
    warnings.formatwarning = _simple_warning_format


def warn(msg, category=UserWarning, stacklevel=2):

    """Throws a warning using a simple, cleaned up format."""

    enable_simple_warnings()
    warnings.warn(msg, category, stacklevel=stacklevel)
