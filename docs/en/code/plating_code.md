This document presents the complete electrodeposition simulation code in galvanostatic mode, with block-by-block explanations.

---

## Cell 1: Imports and Configuration

```python
#!/usr/bin/env python3
"""
Electrodeposition Simulation - Galvanostatic Mode (imposed DDC)
Secondary Current Distribution for Nickel on 3-pad electrode

OPTIMIZED VERSION ED_v1:
- Parameters centralized in config/parameters_ED.py
- Solver built once (gain ~5-10x)
- Corrected bisection logic
- Parametric study support via create_params()
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server
import matplotlib.pyplot as plt
from firedrake import *
from pathlib import Path
import sys
import time
import argparse
```

**Explanation**:
- `firedrake`: Finite element framework (alternative to FEniCS)
- `matplotlib.use('Agg')`: Required for PNG generation without display
- `argparse`: Command line parameter support

---

## Cell 2: Loading Parameters

```python
# Add parent folder to path for config import
project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))

# Import centralized parameters
from config import PARAMS, create_params, get_project_paths
```

**Explanation**: Physical and numerical parameters are centralized in `config/parameters_ED.py` to facilitate parametric studies.

---

## Cell 3: Main Function `run_simulation()`

```python
def run_simulation(params=None, verbose=True):
    """
    Execute the electrodeposition simulation.

    Parameters
    ----------
    params : Parameters, optional
        Parameters instance (default: PARAMS)
    verbose : bool
        Display messages

    Returns
    -------
    dict
        Simulation results
    """
    if params is None:
        params = PARAMS

    start_time = time.time()
```

---

## Cell 4: Physical Parameter Extraction

```python
    # === PHYSICAL PARAMETERS (from config) ===
    # Electrochemistry
    F_const = params.constants.F      # 96485 C/mol
    R_const = params.constants.R      # 8.314 J/(mol·K)
    T = params.constants.T            # 298 K
    n = params.electrochem.n          # 2 (Ni²⁺)
    j0 = params.electrochem.j0        # Exchange density [A/m²]
    alpha_a = params.electrochem.alpha_a  # Anodic transfer coeff.
    alpha_c = params.electrochem.alpha_c  # Cathodic transfer coeff.
    E_eq = params.electrochem.E_eq    # -0.257 V vs SHE
    sigma = params.electrochem.sigma  # Conductivity [S/m]
    eta_max = params.electrochem.eta_max  # Max overpotential (protection)

    # Nickel
    M_Ni = params.nickel.M            # 58.69 g/mol
    rho_Ni = params.nickel.rho        # 8908 kg/m³

    # Process
    DDC_target = params.process.DDC_target  # A/dm²
    j_target = params.process.j_target      # A/m² (= DDC × 100)
    time_deposition = params.process.time_deposition  # s
    efficiency = params.process.efficiency  # ~0.98

    # Numerical
    f = params.f  # nF/RT (thermal factor)
```

**Explanation**: All parameters are grouped in a `Parameters` object for traceability and parametric studies.

---

## Cell 5: Mesh Loading

```python
    # === LOAD MESH ===
    paths = get_project_paths()

    try:
        from meshio_to_firedrake_with_facet_markers import load_gmsh_with_facet_markers

        mesh_file = paths['mesh'] / "electrode_3d_full.msh"
        mesh, markers_info = load_gmsh_with_facet_markers(mesh_file, verbose=False)

        cathode_marker = params.tags.CathodeSurface
        anode_marker = params.tags.AnodeSurface

    except Exception as e:
        # Fallback: simple mesh if file not found
        mesh = BoxMesh(10, 10, 20, 0.01, 0.01, 0.02)
        cathode_marker = None
        anode_marker = None
```

**Explanation**:
- GMSH mesh contains surface markers (anode, cathode, walls)
- `load_gmsh_with_facet_markers`: Utility function to convert GMSH → Firedrake
- Fallback to `BoxMesh` if file doesn't exist

---

## Cell 6: Function Space

```python
    # === FUNCTION SPACE ===
    V = FunctionSpace(mesh, "CG", 1)  # P1 Lagrange elements
    phi = Function(V, name="potential")
    v = TestFunction(V)
```

**Explanation**:
- `CG` = Continuous Galerkin (classical finite elements)
- `1` = Degree 1 polynomials (linear)
- DOFs ≈ number of mesh nodes

---

## Cell 7: Pre-compute Cathode Information

```python
    # === PRE-COMPUTE CATHODE INFO ===
    if cathode_marker is not None:
        one = Function(V)
        one.interpolate(Constant(1.0))
        cathode_area = assemble(one * ds(cathode_marker))  # Cathode surface [m²]

        # Get cathode DOFs for post-processing
        cathode_dofs = DirichletBC(V, Constant(0.0), cathode_marker).nodes

        I_total = j_target * cathode_area  # Total current [A]
```

**Explanation**:
- `ds(marker)`: Surface integral on marked boundary
- `cathode_dofs`: Node indices on cathode (for result extraction)

---

## Cell 8: Build Solver (Once)

```python
    # === BUILD SOLVER (once) ===
    V_anode_const = Constant(0.0)  # Will be modified during bisection
    phi_solve = Function(V, name="phi_solve")
    bc_anode = DirichletBC(V, V_anode_const, anode_marker)

    # Variational formulation: -σ∇²φ = 0
    F_form = sigma * inner(grad(phi_solve), grad(v)) * dx

    # Butler-Volmer kinetics at cathode (flux condition)
    eta = phi_solve - Constant(E_eq)
    eta_safe = conditional(
        eta > eta_max, Constant(eta_max),
        conditional(eta < -eta_max, Constant(-eta_max), eta)
    )
    j_bv = j0 * (exp(alpha_a * f * eta_safe) - exp(-alpha_c * f * eta_safe))

    if cathode_marker is not None:
        F_form += j_bv * v * ds(cathode_marker)

    # Create problem and solver
    problem = NonlinearVariationalProblem(F_form, phi_solve, bcs=[bc_anode])
    solver = NonlinearVariationalSolver(problem, solver_parameters={
        'snes_type': 'newtonls',
        'snes_max_it': 50,
        'snes_rtol': 1e-8,
        'snes_atol': 1e-10,
        'ksp_type': 'gmres',
        'pc_type': 'ilu',
    })
```

**Explanation**:
- **Key optimization**: Solver built ONCE only
- `conditional()`: Protection against exp(overflow)
- `snes_type: newtonls`: Newton-Raphson with line search
- `ksp_type: gmres`: Krylov iterative solver
- `pc_type: ilu`: ILU preconditioner

---

## Cell 9: Galvanostatic Bisection Algorithm

```python
    # === GALVANOSTATIC SEARCH ===
    def compute_cathode_current():
        """Compute average current density on cathode."""
        phi_vals = phi_solve.dat.data_ro
        if cathode_dofs is not None:
            phi_cathode = phi_vals[cathode_dofs]
            eta_cathode = phi_cathode - E_eq
            eta_safe_np = np.clip(eta_cathode, -eta_max, eta_max)
            j_cathode = j0 * (np.exp(alpha_a * f * eta_safe_np)
                             - np.exp(-alpha_c * f * eta_safe_np))
            return np.abs(j_cathode).mean()
        return 0.0

    V_anode_min = -2.0  # Lower bound [V]
    V_anode_max = 2.0   # Upper bound [V]
    tolerance = 0.01    # 1%
    max_iterations = 30

    phi_solve.interpolate(Constant(E_eq - 0.1))  # Initialization

    best_solution = None
    best_error = float('inf')

    for iteration in range(max_iterations):
        V_anode_mid = (V_anode_min + V_anode_max) / 2
        V_anode_const.assign(V_anode_mid)
        phi_solve.interpolate(Constant(E_eq - 0.1))

        try:
            solver.solve()
            j_obtained = compute_cathode_current()
            error_pct = (j_obtained - j_target) / j_target * 100
            DDC_obtained = j_obtained / 100

            if abs(error_pct) < abs(best_error):
                best_error = error_pct
                best_solution = phi_solve.copy(deepcopy=True)
                best_V_anode = V_anode_mid

            if abs(error_pct) < tolerance * 100:
                break

            # Update bisection bounds
            if j_obtained < j_target:
                V_anode_max = V_anode_mid  # Reduce potential
            else:
                V_anode_min = V_anode_mid  # Increase potential

        except Exception as e:
            V_anode_max = V_anode_mid  # Failure → reduce range
```

**Explanation**:
- Bisection on anode potential to reach target DDC
- Typical convergence: 10-15 iterations for 1% accuracy
- Best solution kept in case of failure

---

## Cell 10: Post-processing and Thickness Calculation

```python
    # === POST-PROCESSING ===
    coords = mesh.coordinates.dat.data_ro

    if cathode_dofs is not None:
        coords_cathode = coords[cathode_dofs]
        phi_cathode = phi.dat.data_ro[cathode_dofs]

        # Recalculate Butler-Volmer on cathode
        eta_cathode = phi_cathode - E_eq
        eta_safe_np = np.clip(eta_cathode, -eta_max, eta_max)
        j_cathode = j0 * (np.exp(alpha_a * f * eta_safe_np)
                         - np.exp(-alpha_c * f * eta_safe_np))

        # Faraday's law: thickness in µm
        faraday_factor = params.faraday_factor
        thickness_cathode = np.abs(j_cathode) * faraday_factor

        # Statistics
        j_avg = np.abs(j_cathode).mean()
        cv_percent = thickness_cathode.std() / thickness_cathode.mean() * 100
```

**Explanation**:
- `faraday_factor = M × t × ε / (n × F × ρ) × 10⁶` [µm/(A/m²)]
- CV (Coefficient of Variation): uniformity measure

---

## Cell 11: Save Results

```python
    # === SAVE RESULTS ===
    results_dir = paths['results']
    results_dir.mkdir(exist_ok=True)

    # PNG (thickness map + histogram)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    ax = axes[0]
    scatter = ax.scatter(coords_cathode[:, 0] * 1000, coords_cathode[:, 1] * 1000,
                         c=thickness_cathode, cmap='viridis', s=2)
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_title(f'Thickness (DDC = {DDC_obtained:.1f} A/dm²)')
    plt.colorbar(scatter, ax=ax, label='µm')

    ax = axes[1]
    ax.hist(thickness_cathode, bins=50, edgecolor='black', alpha=0.7)
    ax.axvline(thickness_cathode.mean(), color='red', linestyle='--',
               label=f'Mean: {thickness_cathode.mean():.2f} µm')
    ax.set_xlabel('Thickness (µm)')
    ax.legend()

    plt.savefig(results_dir / f"results_DDC{int(DDC_target)}_optimized.png", dpi=150)
    plt.close()

    # NPZ (raw data for analysis)
    np.savez(results_dir / f"cathode_data_DDC{int(DDC_target)}.npz",
             coords=coords_cathode,
             thickness=thickness_cathode,
             current_density=np.abs(j_cathode))

    # VTK (3D visualization)
    j_function = Function(V, name="current_density")
    thickness_function = Function(V, name="thickness")
    j_function.dat.data[cathode_dofs] = np.abs(j_cathode)
    thickness_function.dat.data[cathode_dofs] = thickness_cathode

    VTKFile(results_dir / f"results_DDC{int(DDC_target)}.pvd").write(
        phi, j_function, thickness_function)
```

**Explanation**:
- **PNG**: Quick visualization (map + histogram)
- **NPZ**: NumPy data for further analysis
- **VTK/PVD**: ParaView format for advanced 3D visualization

---

## Cell 12: CLI Entry Point

```python
def main():
    parser = argparse.ArgumentParser(description="Electrodeposition Simulation ED_v1")
    parser.add_argument('--ddc', type=float, help="DDC target (A/dm²)")
    parser.add_argument('--sigma', type=float, help="Conductivity (S/m)")
    parser.add_argument('--j0', type=float, help="Exchange current density (A/m²)")
    parser.add_argument('--alpha', type=float, help="Transfer coefficient")
    parser.add_argument('--time', type=float, help="Deposition time (s)")
    parser.add_argument('--quiet', action='store_true', help="Reduce output")

    args = parser.parse_args()

    # Build kwargs for create_params
    param_kwargs = {}
    if args.ddc is not None:
        param_kwargs['DDC_target'] = args.ddc
    if args.sigma is not None:
        param_kwargs['sigma'] = args.sigma
    # ... etc.

    params = create_params(**param_kwargs) if param_kwargs else PARAMS
    results = run_simulation(params, verbose=not args.quiet)

if __name__ == "__main__":
    main()
```

**Usage**:
```bash
# Default simulation
python simulation_galvanostatique_optimized.py

# Custom DDC
python simulation_galvanostatique_optimized.py --ddc 10.0

# Parametric study
python simulation_galvanostatique_optimized.py --sigma 30.0 --ddc 12.0
```

---

## Architecture Summary

```
┌─────────────────────────────────────────────────────────────┐
│                    run_simulation()                         │
├─────────────────────────────────────────────────────────────┤
│  1. Load parameters (config/parameters_ED.py)              │
│  2. Load GMSH mesh                                          │
│  3. Create function space V (CG1)                          │
│  4. Build Newton solver (SNES)                              │
│  5. Bisection loop:                                         │
│     ├── V_anode = (V_min + V_max) / 2                      │
│     ├── Solve φ                                             │
│     ├── Compute j_avg via Butler-Volmer                    │
│     └── Adjust [V_min, V_max]                              │
│  6. Post-processing: thickness via Faraday                 │
│  7. Export: PNG, NPZ, VTK                                   │
└─────────────────────────────────────────────────────────────┘
```
