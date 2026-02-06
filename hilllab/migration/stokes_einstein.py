# Christopher Esther, Hill Lab, 9/18/2025
import math

def D(temperature_K, eta_mPas, radius_nm):
    
    """ 
    Solves for the diffusion coefficient using the Stokes-Einstein 
    equation.
    
    ARGUMENTS:
        temperature_K (int): temperature of the experiment in Kelvin
        eta_mPas (float): solvent viscosity in units of mPa * s
        radius_nm (float): radius of the probe in nanometers
        
    RETURNS:
        D_m2s (float): diffusion coefficient in units of m^2/s
    """

    boltzmann = 1.380649e-23
    eta_Pas = eta_mPas / 1000
    radius_m = radius_nm / 1e9

    # Handle eta values of 0 gracefully
    if eta_mPas != 0:
        D_m2s = (boltzmann * temperature_K) / (6 * math.pi * eta_Pas * radius_m)
    else:
        D_m2s = float('inf')
    return D_m2s


def eta(temperature_K, D_m2s, radius_nm):
    
    """ 
    Solves for the viscosity using the Stokes-Einstein equation.
    
    ARGUMENTS:
        temperature_K (int): temperature of the experiment in Kelvin
        D_m2s (float): diffusion coefficient in units of m^2/s
        radius_nm (float): radius of the probe in nanometers
        
    RETURNS:
        eta_mPas (float): solvent viscosity in units of mPa * s
    """

    boltzmann = 1.380649e-23
    radius_m = radius_nm / 1e9

    # Handle D values of 0 gracefully
    if D_m2s != 0:
        eta_Pas = (boltzmann * temperature_K) / (6 * math.pi * D_m2s * radius_m)
    else:
        eta_Pas = float('inf')

    eta_mPas = eta_Pas * 1000
    return eta_mPas


def r(temperature_K, D_m2s, eta_mPas):
    
    """ 
    Solves for the probe radius using the Stokes-Einstein equation.
    
    ARGUMENTS:
        temperature_K (int): temperature of the experiment in Kelvin
        D_m2s (float): diffusion coefficient in units of m^2/s
        eta_mPas (float): solvent viscosity in units of mPa * s
        
    RETURNS:
        radius_nm (float): radius of the probe in nanometers
    """

    boltzmann = 1.380649e-23
    eta_Pas = eta_mPas / 1000

    # Handle D or eta values of 0 gracefully
    if (D_m2s != 0) and (eta_mPas != 0):
        radius_m = (boltzmann * temperature_K) / (6 * math.pi * D_m2s * eta_Pas)
    else:
        radius_m = float('inf')
        
    radius_nm = radius_m * 1e9
    return radius_nm


def T(D_m2s, eta_mPas, radius_nm):
    
    """ 
    Solves for the temperature using the Stokes-Einstein equation.
    
    ARGUMENTS:
        D_m2s (float): diffusion coefficient in units of m^2/s
        eta_mPas (float): solvent viscosity in units of mPa * s
        radius_nm (float): radius of the probe in nanometers
        
    RETURNS:
        temperature_K (float): temperature in Kelvin
    """

    boltzmann = 1.380649e-23
    eta_Pas = eta_mPas / 1000
    radius_m = radius_nm / 1e9
    temperature_K = (6 * math.pi * eta_Pas * radius_m * D_m2s) / boltzmann
    return temperature_K
