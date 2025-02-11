import math

def estimate_resistor_life(T_use, L0=100000, T_ref=343, Ea=0.5):
    """
    Estimate resistor life using the Arrhenius equation.

    Parameters:
    T_use (float): Operating temperature in Celsius
    L0 (float): Known life at reference temperature (default: 100,000 hours)
    T_ref (float): Reference temperature in Kelvin (default: 70°C = 343K)
    Ea (float): Activation energy in eV (default: 0.5 eV)

    Returns:
    float: Estimated life in hours
    """
    k = 8.617e-5  # Boltzmann constant in eV/K
    T_use_K = T_use + 273.15  # Convert to Kelvin

    LT = L0 * math.exp((Ea / k) * ((1 / T_use_K) - (1 / T_ref)))
    
    return LT

def compute_power_degradation(T_use, P_rated=1.0, T_threshold=70, T_max=155):
    """
    Compute usable power at a given temperature based on the derating curve.

    Parameters:
    T_use (float): Operating temperature in Celsius
    P_rated (float): Rated power at threshold temperature (default: 1.0W)
    T_threshold (float): Temperature where derating starts (default: 70°C)
    T_max (float): Maximum operating temperature (default: 155°C)

    Returns:
    float: Usable power at the given temperature
    """
    if T_use <= T_threshold:
        return P_rated
    elif T_use >= T_max:
        return 0.0
    else:
        return P_rated * ((T_max - T_use) / (T_max - T_threshold))
