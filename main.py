# main.py
from thermal_engine import calculate_phase_1
from geometry_engine import run_phase_2

def get_input(prompt: str, default_val: float) -> float:
    """Safely captures CLI input from user, falling back to defaults if blank."""
    try:
        val = input(f"{prompt} [{default_val}]: ").strip()
        if not val:
            return float(default_val)
        return float(val)
    except ValueError:
        print(f"  [!] Invalid input. Using default: {default_val}")
        return float(default_val)

def main():
    print("\n=======================================================")
    print("   COOLING TOWER ENGINE - PHASE 1 & 2 BOUNDARY SUITE   ")
    print("=======================================================")
    print("Press [Enter] to accept default verified test values.\n")
    
    # --- PHASE 1 INPUTS ---
    print("--- STEP 1: THERMAL & PSYCHROMETRIC INPUTS ---")
    cwt = get_input("Cold Water Temp (°F)", 89.60)
    wbt = get_input("Wet Bulb Temp (°F)", 84.20)
    rh_percent = get_input("Relative Humidity (%)", 70.00)
    range_deg = get_input("Temperature Range (°F)", 9.00)
    altitude_ft = get_input("Altitude (ft)", 750.0)
    
    # --- PHASE 2 INPUTS ---
    print("\n--- STEP 2: TOWER GEOMETRY & AIR INLET INPUTS ---")
    length_ft = get_input("Cell Length (ft)", 18.00)
    width_ft = get_input("Cell Width (ft)", 18.00)
    height_ft = get_input("Inlet Height (ft)", 3.50)
    open_faces = int(get_input("Number of Open Inlet Faces (2 or 4)", 4))
    obstruction = get_input("Inlet Obstruction Derate (%)", 5.0)
    louver_k = get_input("Louver Loss Coefficient (K)", 1.00)
    
    # Note: In future phases, airflow_cfm will be solved dynamically by Phase 5.
    # For Phase 1 & 2 boundary testing, we input the design airflow at the inlet face.
    airflow_cfm = get_input("Test Airflow at Inlet Face (CFM)", 180914.6)

    # ---------------------------------------------------------
    # EXECUTE ENGINE 1: THERMAL & PSYCHROMETRICS
    # ---------------------------------------------------------
    p1_results = calculate_phase_1(cwt, wbt, rh_percent, range_deg, altitude_ft)
    
    # Extract calculated density to feed into Engine 2
    calc_density = p1_results["inlet_density_lb_ft3"]

    # ---------------------------------------------------------
    # EXECUTE ENGINE 2: GEOMETRY & AERODYNAMICS
    # ---------------------------------------------------------
    p2_results = run_phase_2(
        cell_length_ft=length_ft,
        cell_width_ft=width_ft,
        inlet_height_ft=height_ft,
        num_open_faces=open_faces,
        obstruction_percent=obstruction,
        airflow_cfm=airflow_cfm,
        inlet_density_lb_ft3=calc_density,
        louver_k_factor=louver_k
    )

    # ---------------------------------------------------------
    # OUTPUT VERIFICATION DASHBOARD
    # ---------------------------------------------------------
    print("\n=======================================================")
    print("              COMPLETE SYSTEM OUTPUT                   ")
    print("=======================================================")
    print(" [ PHASE 1: THERMAL & AIR PROPERTIES ]")
    print(f"  Hot Water Temp (HWT):       {p1_results['hwt']:.2f} °F")
    print(f"  Approach:                   {p1_results['approach']:.2f} °F")
    print(f"  Inlet Dry Bulb (DBT):       {p1_results['inlet_dbt']:.1f} °F")
    print(f"  Air Inlet Density (ρ):      {p1_results['inlet_density_lb_ft3']:.4f} lb/ft³")
    print("-------------------------------------------------------")
    print(" [ PHASE 2: INLET GEOMETRY & AERODYNAMICS ]")
    print(f"  Gross Intake Area:          {p2_results['gross_area_ft2']:.2f} ft²")
    print(f"  Net Breathing Area:         {p2_results['net_area_ft2']:.2f} ft²")
    print(f"  Air Inlet Velocity:         {p2_results['inlet_velocity_fpm']:.1f} FPM")
    print(f"  Velocity Pressure (VP):     {p2_results['inlet_vp_inwg']:.4f} in.wg")
    print(f"  Static Pressure Drop (dP):  {p2_results['inlet_dp_inwg']:.4f} in.wg")
    print("=======================================================\n")

if __name__ == "__main__":
    main()