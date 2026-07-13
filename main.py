# main.py
from thermal_engine import calculate_phase_1

def get_input(prompt: str, default_val: float) -> float:
    """Safely captures user inputs via CLI, falling back to defaults if blank."""
    try:
        val = input(f"{prompt} [{default_val}]: ").strip()
        if not val:
            return float(default_val)
        return float(val)
    except ValueError:
        print(f"  [!] Invalid input format. Defaulting to: {default_val}")
        return float(default_val)

def main():
    print("\n=======================================================")
    print("   COOLING TOWER RATING ENGINE - PHASE 1: THERMAL      ")
    print("=======================================================")
    print("Press [Enter] to accept default screenshot values.\n")
    
    # User Inputs (Phase 1 specific parameters)
    cwt = get_input("Cold Water Temperature (°F)", 89.60)
    wbt = get_input("Wet Bulb Temperature (°F)", 84.20)
    rh_percent = get_input("Relative Humidity (%)", 70.00)
    range_deg = get_input("Temperature Range (°F)", 9.00)
    altitude_ft = get_input("Elevation / Altitude (ft)", 750.0)

    # Execute calculations using the engine module
    results = calculate_phase_1(cwt, wbt, rh_percent, range_deg, altitude_ft)

    # Output Presentation Table
    print("\n=======================================================")
    print("             PHASE 1 OUTPUT VERIFICATION               ")
    print("=======================================================")
    print(f"Hot Water Temp (HWT):    {results['hwt']:.2f} °F")
    print(f"Approach:                {results['approach']:.2f} °F")
    print(f"Barometric Pressure:     {results['atm_pressure_psia']:.4f} psia")
    print("-------------------------------------------------------")
    print(f"Inlet Dry Bulb (DBT):    {results['inlet_dbt']:.1f} °F")
    print(f"Air Inlet Density:       {results['inlet_density_lb_ft3']:.4f} lb/ft³")
    print(f"Air Inlet Sp. Volume:    {results['inlet_sp_vol_ft3_lb']:.2f} ft³/lb")
    print("=======================================================\n")

if __name__ == "__main__":
    main()