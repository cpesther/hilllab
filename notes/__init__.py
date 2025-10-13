# __init__.py for the notes subpackage.
# Initializes package-level imports and configuration.

"""
This folder contains a bunch of boilerplate text and readme files that 
are either read from by other functions or copied into folder locations 
for informational purposes. The included _create_file.py function is 
used as a central handler for creating new files at a desired location 
based on the boilerplate text files. 
"""

from ._note_manager import _create_note, _append_note
