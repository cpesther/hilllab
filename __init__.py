# __init__.py for the particlehill package.

# Rebuilt by Christopher Esther in July 2025. 
# Based on origial code and/or concepts by Matt Markovetz (9/2016) and 
# Matthew Combs (5/2015).

__version__ = '0.0.1'
__all__ = ['autotracker', 'beads', 'cilia', 'utilities']

from .autotracker import *
from .beads import *
from .cilia import *
from .utilities import *

print('|   ▏  ▎  ▍  ▎  ▏  |    ▏  ▎  ▍  ▎  ▏  |')
print(f'          particlehill (version {__version__})')
print('|   ▏  ▎  ▍  ▎  ▏  |    ▏  ▎  ▍  ▎  ▏  |')
