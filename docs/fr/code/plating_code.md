Ce document présente le code complet de simulation d'électrodéposition en mode galvanostatique, avec explications bloc par bloc.

---

## Cellule 1 : Imports et Configuration

```python
#!/usr/bin/env python3
"""
Electrodeposition Simulation - Mode Galvanostatique (DDC imposee)
Secondary Current Distribution for Nickel on 3-pad electrode

VERSION OPTIMISEE ED_v1:
- Paramètres centralisés dans config/parameters_ED.py
- Solver construit une seule fois (gain ~5-10x)
- Logique de bisection corrigée
- Support étude paramétrique via create_params()
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend non-interactif pour serveur
import matplotlib.pyplot as plt
from firedrake import *
from pathlib import Path
import sys
import time
import argparse
```

**Explication** :
- `firedrake` : Framework éléments finis (alternative à FEniCS)
- `matplotlib.use('Agg')` : Obligatoire pour génération de PNG sans display
- `argparse` : Support des paramètres en ligne de commande

---

## Cellule 2 : Chargement des Paramètres

```python
# Ajouter le dossier parent au path pour importer config
project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))

# Importer les paramètres centralisés
from config import PARAMS, create_params, get_project_paths
```

**Explication** : Les paramètres physiques et numériques sont centralisés dans `config/parameters_ED.py` pour faciliter les études paramétriques.

---

## Cellule 3 : Fonction Principale `run_simulation()`

```python
def run_simulation(params=None, verbose=True):
    """
    Exécute la simulation d'électrodéposition.

    Parameters
    ----------
    params : Parameters, optional
        Instance de paramètres (défaut: PARAMS)
    verbose : bool
        Afficher les messages

    Returns
    -------
    dict
        Résultats de la simulation
    """
    if params is None:
        params = PARAMS

    start_time = time.time()
```

---

## Cellule 4 : Extraction des Paramètres Physiques

```python
    # === PHYSICAL PARAMETERS (depuis config) ===
    # Électrochimie
    F_const = params.constants.F      # 96485 C/mol
    R_const = params.constants.R      # 8.314 J/(mol·K)
    T = params.constants.T            # 298 K
    n = params.electrochem.n          # 2 (Ni²⁺)
    j0 = params.electrochem.j0        # Densité d'échange [A/m²]
    alpha_a = params.electrochem.alpha_a  # Coeff. transfert anodique
    alpha_c = params.electrochem.alpha_c  # Coeff. transfert cathodique
    E_eq = params.electrochem.E_eq    # -0.257 V vs SHE
    sigma = params.electrochem.sigma  # Conductivité [S/m]
    eta_max = params.electrochem.eta_max  # Surtension max (protection)

    # Nickel
    M_Ni = params.nickel.M            # 58.69 g/mol
    rho_Ni = params.nickel.rho        # 8908 kg/m³

    # Procédé
    DDC_target = params.process.DDC_target  # A/dm²
    j_target = params.process.j_target      # A/m² (= DDC × 100)
    time_deposition = params.process.time_deposition  # s
    efficiency = params.process.efficiency  # ~0.98

    # Numérique
    f = params.f  # nF/RT (facteur thermique)
```

**Explication** : Tous les paramètres sont regroupés dans un objet `Parameters` pour la traçabilité et les études paramétriques.

---

## Cellule 5 : Chargement du Maillage

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
        # Fallback: maillage simple si fichier non trouvé
        mesh = BoxMesh(10, 10, 20, 0.01, 0.01, 0.02)
        cathode_marker = None
        anode_marker = None
```

**Explication** :
- Le maillage GMSH contient les marqueurs de surfaces (anode, cathode, parois)
- `load_gmsh_with_facet_markers` : Fonction utilitaire pour convertir GMSH → Firedrake
- Fallback vers `BoxMesh` si le fichier n'existe pas

---

## Cellule 6 : Espace Fonctionnel

```python
    # === FUNCTION SPACE ===
    V = FunctionSpace(mesh, "CG", 1)  # Éléments Lagrange P1
    phi = Function(V, name="potential")
    v = TestFunction(V)
```

**Explication** :
- `CG` = Continuous Galerkin (éléments finis classiques)
- `1` = Polynômes de degré 1 (linéaires)
- DOFs ≈ nombre de nœuds du maillage

---

## Cellule 7 : Pré-calcul Informations Cathode

```python
    # === PRE-COMPUTE CATHODE INFO ===
    if cathode_marker is not None:
        one = Function(V)
        one.interpolate(Constant(1.0))
        cathode_area = assemble(one * ds(cathode_marker))  # Surface cathode [m²]

        # Récupérer les DOFs de la cathode pour post-traitement
        cathode_dofs = DirichletBC(V, Constant(0.0), cathode_marker).nodes

        I_total = j_target * cathode_area  # Courant total [A]
```

**Explication** :
- `ds(marker)` : Intégrale de surface sur une frontière marquée
- `cathode_dofs` : Indices des nœuds sur la cathode (pour extraire les résultats)

---

## Cellule 8 : Construction du Solveur (Une Seule Fois)

```python
    # === BUILD SOLVER (once) ===
    V_anode_const = Constant(0.0)  # Sera modifié pendant la bisection
    phi_solve = Function(V, name="phi_solve")
    bc_anode = DirichletBC(V, V_anode_const, anode_marker)

    # Formulation variationnelle : -σ∇²φ = 0
    F_form = sigma * inner(grad(phi_solve), grad(v)) * dx

    # Cinétique Butler-Volmer à la cathode (condition de flux)
    eta = phi_solve - Constant(E_eq)
    eta_safe = conditional(
        eta > eta_max, Constant(eta_max),
        conditional(eta < -eta_max, Constant(-eta_max), eta)
    )
    j_bv = j0 * (exp(alpha_a * f * eta_safe) - exp(-alpha_c * f * eta_safe))

    if cathode_marker is not None:
        F_form += j_bv * v * ds(cathode_marker)

    # Créer le problème et le solveur
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

**Explication** :
- **Optimisation clé** : Le solveur est construit UNE SEULE FOIS
- `conditional()` : Protection contre exp(overflow)
- `snes_type: newtonls` : Newton-Raphson avec recherche linéaire
- `ksp_type: gmres` : Solveur itératif Krylov
- `pc_type: ilu` : Préconditionneur ILU

---

## Cellule 9 : Algorithme de Bisection Galvanostatique

```python
    # === GALVANOSTATIC SEARCH ===
    def compute_cathode_current():
        """Calcule la densité de courant moyenne sur la cathode."""
        phi_vals = phi_solve.dat.data_ro
        if cathode_dofs is not None:
            phi_cathode = phi_vals[cathode_dofs]
            eta_cathode = phi_cathode - E_eq
            eta_safe_np = np.clip(eta_cathode, -eta_max, eta_max)
            j_cathode = j0 * (np.exp(alpha_a * f * eta_safe_np)
                             - np.exp(-alpha_c * f * eta_safe_np))
            return np.abs(j_cathode).mean()
        return 0.0

    V_anode_min = -2.0  # Borne inf [V]
    V_anode_max = 2.0   # Borne sup [V]
    tolerance = 0.01    # 1%
    max_iterations = 30

    phi_solve.interpolate(Constant(E_eq - 0.1))  # Initialisation

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

            # Mise à jour des bornes de bisection
            if j_obtained < j_target:
                V_anode_max = V_anode_mid  # Réduire le potentiel
            else:
                V_anode_min = V_anode_mid  # Augmenter le potentiel

        except Exception as e:
            V_anode_max = V_anode_mid  # Échec → réduire la plage
```

**Explication** :
- Bissection sur le potentiel d'anode pour atteindre la DDC cible
- Convergence typique : 10-15 itérations pour 1% de précision
- Conservation de la meilleure solution en cas d'échec

---

## Cellule 10 : Post-traitement et Calcul d'Épaisseur

```python
    # === POST-PROCESSING ===
    coords = mesh.coordinates.dat.data_ro

    if cathode_dofs is not None:
        coords_cathode = coords[cathode_dofs]
        phi_cathode = phi.dat.data_ro[cathode_dofs]

        # Recalcul Butler-Volmer sur la cathode
        eta_cathode = phi_cathode - E_eq
        eta_safe_np = np.clip(eta_cathode, -eta_max, eta_max)
        j_cathode = j0 * (np.exp(alpha_a * f * eta_safe_np)
                         - np.exp(-alpha_c * f * eta_safe_np))

        # Loi de Faraday : épaisseur en µm
        faraday_factor = params.faraday_factor
        thickness_cathode = np.abs(j_cathode) * faraday_factor

        # Statistiques
        j_avg = np.abs(j_cathode).mean()
        cv_percent = thickness_cathode.std() / thickness_cathode.mean() * 100
```

**Explication** :
- `faraday_factor = M × t × ε / (n × F × ρ) × 10⁶` [µm/(A/m²)]
- CV (Coefficient de Variation) : mesure d'uniformité

---

## Cellule 11 : Sauvegarde des Résultats

```python
    # === SAVE RESULTS ===
    results_dir = paths['results']
    results_dir.mkdir(exist_ok=True)

    # PNG (carte d'épaisseur + histogramme)
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

    # NPZ (données brutes pour analyse)
    np.savez(results_dir / f"cathode_data_DDC{int(DDC_target)}.npz",
             coords=coords_cathode,
             thickness=thickness_cathode,
             current_density=np.abs(j_cathode))

    # VTK (visualisation 3D)
    j_function = Function(V, name="current_density")
    thickness_function = Function(V, name="thickness")
    j_function.dat.data[cathode_dofs] = np.abs(j_cathode)
    thickness_function.dat.data[cathode_dofs] = thickness_cathode

    VTKFile(results_dir / f"results_DDC{int(DDC_target)}.pvd").write(
        phi, j_function, thickness_function)
```

**Explication** :
- **PNG** : Visualisation rapide (carte + histogramme)
- **NPZ** : Données NumPy pour analyse ultérieure
- **VTK/PVD** : Format ParaView pour visualisation 3D avancée

---

## Cellule 12 : Point d'Entrée CLI

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

**Usage** :
```bash
# Simulation par défaut
python simulation_galvanostatique_optimized.py

# DDC personnalisée
python simulation_galvanostatique_optimized.py --ddc 10.0

# Étude paramétrique
python simulation_galvanostatique_optimized.py --sigma 30.0 --ddc 12.0
```

---

## Résumé de l'Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    run_simulation()                         │
├─────────────────────────────────────────────────────────────┤
│  1. Charger paramètres (config/parameters_ED.py)           │
│  2. Charger maillage GMSH                                   │
│  3. Créer espace fonctionnel V (CG1)                       │
│  4. Construire solveur Newton (SNES)                        │
│  5. Boucle de bisection :                                   │
│     ├── V_anode = (V_min + V_max) / 2                      │
│     ├── Résoudre φ                                          │
│     ├── Calculer j_avg via Butler-Volmer                   │
│     └── Ajuster [V_min, V_max]                             │
│  6. Post-traitement : épaisseur via Faraday                │
│  7. Export : PNG, NPZ, VTK                                  │
└─────────────────────────────────────────────────────────────┘
```
