# Christopher Esther, Hill Lab 2/27/2026
from ..utilities.warning import warn

def _validate_size(bead_size_pixels):

    """Simply ensure that the bead size in pixels is an odd number, 
    as trackpy requires it to be. If not, rounds up to nearest odd number
    and warns the user."""

    # If odd
    if not bead_size_pixels % 2:

        # Round up
        bead_size_pixels += 1

        # Show warning
        warn(msg=f'bead_size_pixels must be odd. Rounding up to {bead_size_pixels}')

    return bead_size_pixels
