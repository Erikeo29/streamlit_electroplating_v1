# Electroplating Modeling: Python (Antigravity)

This module simulates the growth of a Nickel layer on a complex substrate.

## Secondary Current Distribution
The model solves the Laplace equation for electric potential. Butler-Volmer kinetics impose a non-linear relationship between local potential and current density.

## Galvanostatic Algorithm (DDC Search)
To match experimental conditions where total current is imposed (e.g., 8 A/dm²), the code uses an **optimized bisection method**:
1. Estimate an anode potential.
2. Solve the potential field.
3. Integrate current over the cathode.
4. Iteratively adjust anode potential until the target current is reached.

## Simulation Results
- **Thickness Map**: 3D visualization (exportable to VTK) of deposited thickness.
- **Uniformity**: Calculation of standard deviation of thickness over the entire surface.
- **Histogram**: Statistical analysis of metal distribution.