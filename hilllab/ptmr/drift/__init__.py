# __init__.py for the drift subpackage in the PTMR subpackage.
# Initializes package-level imports and configuration.

"""
Several functions used for removing drift from VRPNs. Each uses slightly
different calculates to achieve the same conceptual result. This corrects 
for slow systematic motion of the sample or imaging system that is not 
part of the bead's true movement.
"""

from ._subtract_linear_drift import _subtract_linear_drift

__all__ = ['_subtract_linear_drift']
