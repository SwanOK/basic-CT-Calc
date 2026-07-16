# main.py
import sys
try:
    from thermal_engine import calculate_phase_1
    from geometry_engine import run_phase_2
except ImportError as e:
    print(f"[!] Critical Error: Missing engine module -> {e}")
    print("    Ensure 'thermal_engine.py' and 'geometry_engine.py' are in the same directory.")
    sys.exit(1)

def get_input(prompt: str, default_val: float) -> float:
    """
    Safely captures user input from the command line. 
    Returns the default value if the user presses Enter without typing.
    """
    try:
        val = input(f"  {prompt} [{default_val}]: ").strip()
        if not val:
            return float(default_val)
        return float(val)
    except ValueError:
        print(f"    [!] Invalid format entered. Defaulting to: {default_val}")
        return float(default_val)

def main():
    print("\n" + "="*60)
    print("      COOLING TOWER RATING ENGINE: PHASE 1 & 2 SUITE      ")
    print("="*60)
    print(" Press [Enter] to accept default verified screenshot values.\n")
    
    # ---------------------------------------------------------
    # 1. COLLECT PHASE 1 INPUTS (THERMAL & PSYCHROMETRICS)
    # ---------------------------------------------------------
    print("--- [ STEP 1: THERMAL CONDITIONS & AIR PROPERTIES ] ---")
    cwt = get_input("Cold Water Temperature (°F)", 89.60)
    wbt = get_input("Wet Bulb Temperature (°F)", 84.20)
    rh_percent = get_input("Relative Humidity (%)", 70.00)
    range_deg = get_input("Temperature Range (°F)", 9.00)
    altitude_ft = get_input("Elevation / Altitude (ft)", 750.0)
    
    # ---------------------------------------------------------
    # 2. COLLECT PHASE 2 INPUTS (GEOMETRY & AERODYNAMICS)
    # ---------------------------------------------------------
    print("\n--- [ STEP 2: TOWER GEOMETRY & AIR INLET CONFIG ] ---")
    length_ft = get_input("Cell Length (ft)", 18.00)
    width_ft = get_input("Cell Width (ft)", 18.00)
    height_ft = get_input("Inlet Louver Height (ft)", 3.50)
    open_faces = int(get_input("Number of Open Inlet Faces (2 or 4)", 4))
    obstruction = get_input("Inlet Obstruction Derate (%)", 5.0)
    louver_k = get_input("Louver Loss Coefficient (K)", 1.00)
    
    # Note: In the final Phase 5 integrated app, airflow will be solved dynamically.
    # For Phase 1 & 2 boundary testing, we input the local design airflow at the inlet face.
    airflow_cfm = get_input("Test Airflow at Inlet Face (CFM)", 180914.6)

    # ---------------------------------------------------------
    # 3. EXECUTE ENGINE 1: THERMAL & PSYCHROMETRICS
    # ---------------------------------------------------------
    print("\n[i] Executing Phase 1 Thermodynamic Engine...")
    p1_results = calculate_phase_1(cwt, wbt, rh_percent, range_deg, altitude_ft)
    
    # Extract calculated inlet density to pipe into Engine 2
    calc_density = p1_results["inlet_density_lb_ft3"]

    # ---------------------------------------------------------
    # 4. EXECUTE ENGINE 2: GEOMETRY & AERODYNAMICS
    # ---------------------------------------------------------
    print("[i] Executing Phase 2 Aerodynamic & Geometry Engine...")
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
    # 5. GENERATE FINAL VERIFICATION DASHBOARD
    # ---------------------------------------------------------
    print("\n" + "="*60)
    print("                 SYSTEM VERIFICATION DASHBOARD             ")
    print("="*60)
    print("  [ PHASE 1: THERMAL & PSYCHROMETRIC BOUNDARIES ]")
    print(f"    Hot Water Temp (HWT):        {p1_results['hwt']:>8.2f} °F")
    print(f"    Approach:                    {p1_results['approach']:>8.2f} °F")
    print(f"    Barometric Pressure:         {p1_results['atm_pressure_psia']:>8.4f} psia")
    print(f"    Inlet Dry Bulb (DBT):        {p1_results['inlet_dbt']:>8.1f} °F")
    print(f"    Air Inlet Density (ρ):       {p1_results['inlet_density_lb_ft3']:>8.4f} lb/ft³")
    print(f"    Air Inlet Specific Volume:   {p1_results['inlet_sp_vol_ft3_lb']:>8.2f} ft³/lb")
    print(" -" + "-"*58)
    print("  [ PHASE 2: INLET GEOMETRY & AERODYNAMIC PERFORMANCE ]")
    print(f"    Gross Intake Perimeter:      {p2_results['perimeter_ft']:>8.2f} ft")
    print(f"    Gross Intake Face Area:      {p2_results['gross_area_ft2']:>8.2f} ft²")
    print(f"    Net Breathing Area (A_net):  {p2_results['net_area_ft2']:>8.2f} ft²")
    print(f"    Air Inlet Velocity:          {p2_results['inlet_velocity_fpm']:>8.1f} FPM")
    print(f"    Velocity Pressure (VP):      {p2_results['inlet_vp_inwg']:>8.4f} in.wg")
    print(f"    Static Pressure Drop (dP):   {p2_results['inlet_dp_inwg']:>8.4f} in.wg")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()