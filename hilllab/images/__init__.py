# __init__.py for the images subpackage.
# Initializes package-level imports and configuration.

"""
Generic functions that handle a variety of image processing operations.
"""

from .calculate_mean_brightness import calculate_mean_brightness

__all__ = ['calculate_mean_brightness']
