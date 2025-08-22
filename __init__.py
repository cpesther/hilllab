# __init__.py for the hilllab package.

# Rebuilt by Christopher Esther in July 2025. 
# Based on origial code and/or concepts by Matt Markovetz (9/2016) and 
# Matthew Combs (5/2015).

__version__ = '0.0.1'
__all__ = ['autotracker', 'beads', 'cilia', 'migration', 'utilities']

from .autotracker import *
from .beads import *
from .cilia import *
from .migration import *
from .utilities import *

print('|   ▏  ▎  ▍  ▎  ▏  |    ▏  ▎  ▍  ▎  ▏  |')
print(f'             hilllab (version {__version__})')
print('|   ▏  ▎  ▍  ▎  ▏  |    ▏  ▎  ▍  ▎  ▏  |')
