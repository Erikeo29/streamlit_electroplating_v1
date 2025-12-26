# CV Modeling: Python & Firedrake

The Firedrake implementation leverages the power of the Finite Element Method (FEM) to solve diffusion-reaction equations.

## Model Configuration
- **Mesh**: Unstructured 2D mesh generated with GMSH, featuring local refinement at the electrode/electrolyte interface (micrometer scale).
- **Elements**: Use of Lagrange degree 2 (P2) elements for better accuracy on concentration gradients.
- **Time Scheme**: Implicit Euler (Backward Euler) for unconditional stability, crucial during fast scans.

## Numerical Resolution
The non-linear system resulting from the Butler-Volmer condition is solved at each time step via a Newton-Raphson solver with LU preconditioning:
- `snes_type`: `newtonls`
- `pc_type`: `lu`

## Typical Results
The simulation yields the Ferrocyanide concentration profile over time. We observe the formation of the diffusion layer extending into the "bulk" solution.
The resulting voltammogram shows characteristic anodic and cathodic peaks, whose separation (Delta Ep) indicates kinetic reversibility.