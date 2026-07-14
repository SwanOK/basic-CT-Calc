# Open Cooling Tower Rating Engine (`basic-CT-Calc`)

An open-source, mathematically rigorous cooling tower performance simulation tool built using Python and standard ASHRAE psychrometric physics. 

This project reverse-engineers black-box thermal rating software by isolating individual physical domains into sequential code modules rather than relying on entangled multi-variable regressions.

---

## 🏗 Development Roadmap

- [x] **Phase 1: Thermal Conditions & Air Properties Engine** - [ ] **Phase 2: Tower Geometry & Air Inlet Aerodynamics**
- [x] **Phase 4: Plenum, Eliminators & Fan Mechanics**
- [ ] **Phase 5: Iterative System Solver & Merkel Integration**
- [ ] **Phase 6: Web UI Dashboard Deployment**

---

## 🧪 Phase 1: Thermal & Psychrometric Verification

Phase 1 establishes the baseline boundary conditions for the tower. Because downstream pressure equations multiply against air mass, calculating an un-biased, non-overfitted air density is paramount. 

Using an iterative bisection root-finder coupled with `psychrolib`, Phase 1 perfectly replicates the target commercial software outputs:

| Property | Core Engine Result | Software Target | Margin of Error |
| :--- | :--- | :--- | :--- |
| **Hot Water Temp (HWT)** | **98.60 °F** | 98.60 °F | 0.00% |
| **Approach** | **5.40 °F** | 5.40 °F | 0.00% |
| **Inlet Dry Bulb (DBT)** | **93.0 °F** | 93.0 °F | 0.00% |
| **Air Inlet Density** | **0.0689 lb/ft³** | 0.0689 lb/ft³ | 0.00% |
| **Air Inlet Specific Volume**| **14.87 ft³/lb** | 14.87 ft³/lb | 0.00% |

---

## Installation & Execution

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR_USERNAME/basic-CT-Calc.git](https://github.com/YOUR_USERNAME/basic-CT-Calc.git)
```

### 2. Install dependencies
```bash
cd basic-CT-Calc
```

### 3. Run the CLI App
```bash
python main.py
```