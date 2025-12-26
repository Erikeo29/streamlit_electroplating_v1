# CV Modeling: OpenFOAM

The OpenFOAM approach relies on the Finite Volume Method (FVM), standard in computational fluid dynamics (CFD).

## Solver: `electroChemFoam`
The solver is an adaptation of `laplacianFoam` or `scalarTransportFoam` to include specific electrochemical boundary conditions.

## Specifics
- **Case Structure**: Uses standard directories `0/`, `constant/`, and `system/`.
- **Transport Properties**: Diffusion coefficient $D$ is defined in `constant/transportProperties`.
- **Boundary Conditions (BC)**: Butler-Volmer law implementation via `codedFixedValue` or external libraries (`echemFvPatchFields`).

## Advantages
OpenFOAM allows for easy transition from 2D to full 3D simulation and coupling electrochemistry with hydrodynamics (electrochemistry under flow), which is a natural extension of this project.
