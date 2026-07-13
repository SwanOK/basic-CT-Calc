# engine.py
import math
import psychrolib

# Set psychrolib to use Imperial units (Fahrenheit, psi, ft, lb)
psychrolib.SetUnitSystem(psychrolib.IP)

def solve_dbt_from_wbt_rh(wbt: float, rh_percent: float, pressure: float) -> float:
    """
    Iterative Bisection Solver to find the Dry Bulb Temperature (DBT)
    given Wet Bulb Temperature (WBT), Relative Humidity (RH), and Pressure.
    """
    target_rh = rh_percent / 100.0
    low_dbt = wbt
    high_dbt = wbt + 100.0
    
    for _ in range(100):
        mid_dbt = (low_dbt + high_dbt) / 2.0
        try:
            hum_ratio = psychrolib.GetHumRatioFromTWetBulb(mid_dbt, wbt, pressure)
            calc_rh = psychrolib.GetRelHumFromHumRatio(mid_dbt, hum_ratio, pressure)
            
            if calc_rh > target_rh:
                low_dbt = mid_dbt
            else:
                high_dbt = mid_dbt
        except ValueError:
            high_dbt = mid_dbt
            
    return (low_dbt + high_dbt) / 2.0

def calculate_phase_1(cwt: float, wbt: float, rh_percent: float, range_deg: float, altitude_ft: float) -> dict:
    """
    Phase 1 Core Engine: Computes water temperatures and inlet air properties.
    """
    # 1. Water Thermodynamics
    hwt = cwt + range_deg
    approach = cwt - wbt

    # 2. Atmospheric Pressure Calculation from Altitude
    atm_pressure_psia = psychrolib.GetStandardAtmPressure(altitude_ft)
    
    # 3. Psychrometrics (Air Inlet Properties)
    inlet_dbt = solve_dbt_from_wbt_rh(wbt, rh_percent, atm_pressure_psia)
    hum_ratio = psychrolib.GetHumRatioFromTWetBulb(inlet_dbt, wbt, atm_pressure_psia)
    sp_vol_dry = psychrolib.GetMoistAirVolume(inlet_dbt, hum_ratio, atm_pressure_psia)
    density_moist = psychrolib.GetMoistAirDensity(inlet_dbt, hum_ratio, atm_pressure_psia)

    return {
        "hwt": hwt,
        "approach": approach,
        "atm_pressure_psia": atm_pressure_psia,
        "inlet_dbt": inlet_dbt,
        "inlet_density_lb_ft3": density_moist,
        "inlet_sp_vol_ft3_lb": sp_vol_dry
    }