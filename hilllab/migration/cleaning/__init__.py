# __init__.py for the migration cleaning subpackage.
# Initializes package-level imports and configuration.

"""
Functions that aid in the cleaning and smoothening of the 1DMA data. 
Each of the included functions works on a individual curve, and they are
often implemented within the _plate_prepare_data function. s
"""

from .noise import simple_shift
from .peak import move_peak

__all__ = ['simple_shift', 'move_peak']
