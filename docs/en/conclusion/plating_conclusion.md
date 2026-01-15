# Conclusion and Perspectives

**Table of Contents:**
1. Results Summary
2. Approach Strengths
3. Current Limitations
4. Development Perspectives

---

## 1. Results Summary

The secondary current distribution approach implemented with Firedrake enables estimation and visualization of Nickel thickness distribution based on a few studied parameters (CD, σ, j₀, α).

### Main Results from the Parametric Study (81 simulations)

| Parameter | Range Studied | Impact on CV% |
|-----------|---------------|---------------|
| CD (A/dm²) | 4 - 12 | Low direct impact |
| σ (S/m) | 10 - 40 | **Strong impact**: CV ↓ when σ ↑ |
| j₀ (A/m²) | 0.34 - 1.36 | Moderate impact: CV ↓ when j₀ ↑ |
| α | 0.4 - 0.6 | Low impact |

---

## 2. Approach Strengths

- **Automatic galvanostatic mode**: The anode potential search algorithm eliminates manual tuning, ensuring the imposed total current.

- **Butler-Volmer / Faraday coupling**: Butler-Volmer kinetics coupled with Faraday's law provides physically realistic thickness maps.

- **Statistical analysis**: Histograms and coefficient of variation (CV%) are valuable decision-support tools for quality control.

- **Interactive 3D visualization**: PyVista HTML export enables detailed inspection of deposit topology.

---

## 3. Current Limitations

| Limitation | Description | Impact |
|------------|-------------|--------|
| Secondary distribution only | No mass transport | Uniformity overestimation at high CD |
| Simplified 2D geometry | Linear extrusion | Edge effects not captured |
| Fixed mesh | No adaptive remeshing | Limited resolution at corners |

---

## 4. Development Perspectives

### Physical Modeling
- **Tertiary distribution**: Integration of mass transport (Nernst-Planck) to capture metal ion depletion at the surface, particularly critical for high CDs.
- **Multiphysics coupling**: Integration of thermal and hydrodynamic effects.

### Numerical and Meshing
- **Mesh sensitivity analysis**: Convergence study to optimize the accuracy/computation time trade-off.
- **Real 3D geometries**: Extension to complex industrial parts (connectors, PCBs).

### Time Evolution
- **Dynamic tracking**: Tracking deposit growth over time.
- **Experimental validation**: Comparison with profilometric measurements.

### Optimization
- **Inverse optimization**: Automatic search for optimal parameters for a target uniformity.
- **Machine Learning**: Rapid CV% prediction from input parameters.
