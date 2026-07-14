# geometry_engine.py
import math

def calculate_inlet_geometry(
    cell_length_ft: float,
    cell_width_ft: float,
    inlet_height_ft: float,
    num_open_faces: int,
    obstruction_percent: float
) -> dict:
    """
    Computes physical dimensions and net airflow area of the tower inlet.
    """
    # Calculate active intake perimeter based on open faces (typically 2 or 4)
    if num_open_faces == 4:
        perimeter = 2 * (cell_length_ft + cell_width_ft)
    elif num_open_faces == 2:
        perimeter = 2 * cell_length_ft # Assuming intake along lengths
    else:
        perimeter = cell_length_ft * num_open_faces # Generalized fallback
        
    gross_area = perimeter * inlet_height_ft
    net_area = gross_area * (1.0 - (obstruction_percent / 100.0))
    
    return {
        "perimeter_ft": round(perimeter, 2),
        "gross_area_ft2": round(gross_area, 2),
        "net_area_ft2": round(net_area, 2)
    }

def calculate_inlet_aerodynamics(
    net_area_ft2: float,
    airflow_cfm: float,
    inlet_density_lb_ft3: float,
    louver_k_factor: float
) -> dict:
    """
    Computes velocity and static pressure drop across the air inlet section.
    Uses standard ASHRAE velocity pressure formula: dP = K * rho * (V / 1097.3)^2
    """
    # 1. Velocity through the net inlet opening (ft/min or FPM)
    inlet_velocity_fpm = airflow_cfm / net_area_ft2
    
    # 2. Velocity Pressure (in.wg)
    vp_inlet = inlet_density_lb_ft3 * math.pow(inlet_velocity_fpm / 1097.3, 2)
    
    # 3. Static Pressure Drop across louvers (in.wg)
    dp_inlet = louver_k_factor * vp_inlet
    
    return {
        "inlet_velocity_fpm": round(inlet_velocity_fpm, 1),
        "inlet_vp_inwg": round(vp_inlet, 4),
        "inlet_dp_inwg": round(dp_inlet, 4)
    }

def run_phase_2(
    cell_length_ft: float,
    cell_width_ft: float,
    inlet_height_ft: float,
    num_open_faces: int,
    obstruction_percent: float,
    airflow_cfm: float,
    inlet_density_lb_ft3: float,
    louver_k_factor: float
) -> dict:
    """
    Master execution function for Phase 2: Geometry & Air Inlet Aerodynamics.
    """
    geom_results = calculate_inlet_geometry(
        cell_length_ft, cell_width_ft, inlet_height_ft, num_open_faces, obstruction_percent
    )
    
    aero_results = calculate_inlet_aerodynamics(
        geom_results["net_area_ft2"], airflow_cfm, inlet_density_lb_ft3, louver_k_factor
    )
    
    # Combine results into a unified dictionary
    return {**geom_results, **aero_results}