# Electroplating Simulation Platform

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40-FF4B4B)
![Firedrake](https://img.shields.io/badge/Firedrake-FEM-orange)
![License](https://img.shields.io/badge/License-MIT-green)

Interactive simulation platform for Nickel electrodeposition, featuring secondary current distribution modeling and 3D visualization.

## Features

- **Galvanostatic Simulation**: Deposit modeling under imposed current density (DDC)
- **81 Parametric Simulations**: Pre-computed results varying DDC, conductivity, exchange current density, and transfer coefficient
- **Side-by-Side Comparison**: Compare two simulations with different parameters
- **Interactive 3D Visualization**: PyVista-rendered thickness maps (extruded x1000)
- **Bilingual Interface**: Full support for French and English
- **Jupyter-Style Code Documentation**: Complete simulation code with block-by-block explanations

## Physics

The platform implements a **Secondary Current Distribution** model:

- **Laplace Equation**: Potential distribution in the electrolyte
- **Butler-Volmer Kinetics**: Non-linear electrode kinetics at the cathode
- **Faraday's Law**: Thickness calculation from local current density
- **Bisection Algorithm**: Galvanostatic mode to achieve target DDC

Key equations:

```
Potential:  div(-sigma * grad(phi)) = 0
Kinetics:   j = j0 * [exp(alpha_a*f*eta) - exp(-alpha_c*f*eta)]
Thickness:  h = |j| * M * t * epsilon / (n * F * rho)
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| FEM Solver | Firedrake + PETSc |
| 3D Visualization | PyVista |
| 2D Plots | Matplotlib |

## Installation

```bash
# Clone the repository
git clone https://github.com/Erikeo29/streamlit_electroplating_v1.git
cd streamlit_electroplating_v1

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Project Structure

```
streamlit_electroplating_v1/
|-- app.py                 # Main Streamlit application
|-- assets/
|   |-- style.css          # Custom styling
|   |-- plating/
|       |-- study_results/ # 81 simulation results (PNG + HTML)
|-- data/
|   |-- ED_mapping.csv     # Simulation parameter mapping
|-- docs/
|   |-- fr/                # French documentation
|   |-- en/                # English documentation
|       |-- physics/       # Detailed equations
|       |-- code/          # Jupyter-style code docs
|       |-- biblio/        # Bibliography with free resources
```

## Parametric Study

The platform includes 81 pre-computed simulations with the following parameter ranges:

| Parameter | Symbol | Values | Unit |
|-----------|--------|--------|------|
| Current Density | DDC | 4, 8, 12 | A/dm² |
| Conductivity | sigma | 10, 25, 40 | S/m |
| Exchange Current | j0 | 0.34, 0.68, 1.36 | A/m² |
| Transfer Coeff. | alpha | 0.4, 0.5, 0.6 | - |

Each simulation includes:
- Thickness map (PNG)
- Current density distribution (PNG)
- 3D isometric view (PNG)
- Interactive 3D visualization (HTML)

## Screenshots

### Comparison View
Select parameters for two simulations and compare thickness maps, current density distributions, and 3D views side by side.

### Physics Documentation
Detailed equations with parameter tables, boundary conditions, and the galvanostatic bisection algorithm.

### Code Documentation
Complete Firedrake simulation code presented in Jupyter-style cells with explanations for each block.

## Bibliography

The platform includes curated resources:
- **MIT OpenCourseWare**: Butler-Volmer kinetics lecture
- **Internet Archive**: Newman's "Electrochemical Systems" (free borrowing)
- **EchemFEM**: Firedrake electrochemistry package documentation
- **Chemistry LibreTexts**: Electrode kinetics theory

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.3.0 | Jan 2026 | Enhanced bibliography, detailed physics, Jupyter-style code |
| 1.2.0 | Jan 2026 | Side-by-side comparison, 81 simulations, compact layout |
| 1.1.0 | Dec 2025 | Initial release with basic visualization |

## License

MIT License - See LICENSE file for details.

## Author

Developed for electrodeposition R&D applications.
