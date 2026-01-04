This module simulates Nickel layer growth on a complex substrate in galvanostatic mode.

---

## 1. Secondary Current Distribution

The model solves the **Laplace equation** for electric potential $\phi$ in the electrolyte:

$$\nabla \cdot (-\sigma \nabla \phi) = 0$$

Where:
- $\sigma$ = electrolyte conductivity [S/m]
- $\phi$ = electric potential [V]

**Boundary conditions:**
- **Anode**: $\phi = V_{anode}$ (Dirichlet, imposed potential)
- **Cathode**: flux imposed by Butler-Volmer kinetics (nonlinear Neumann)
- **Walls**: zero flux $\nabla \phi \cdot \mathbf{n} = 0$

---

## 2. Butler-Volmer Kinetics

Local current density $j$ at the cathode surface follows the Butler-Volmer equation:

$$j = j_0 \left[ \exp\left(\frac{\alpha_a n F}{RT} \eta\right) - \exp\left(-\frac{\alpha_c n F}{RT} \eta\right) \right]$$

Where:
| Symbol | Description | Typical Value |
|--------|-------------|---------------|
| $j_0$ | Exchange current density | 0.34 - 1.36 A/m² |
| $\alpha_a, \alpha_c$ | Transfer coefficients | 0.4 - 0.6 |
| $n$ | Electrons exchanged | 2 (Ni²⁺) |
| $F$ | Faraday constant | 96485 C/mol |
| $R$ | Gas constant | 8.314 J/(mol·K) |
| $T$ | Temperature | 298 K |
| $\eta$ | Activation overpotential | $\phi_{local} - E_{eq}$ |
| $E_{eq}$ | Equilibrium potential Ni²⁺/Ni | -0.257 V vs SHE |

**Numerical protection**: To avoid exponential overflow, $\eta$ is clamped:
$$\eta_{safe} = \text{clip}(\eta, -\eta_{max}, +\eta_{max})$$ with $\eta_{max} = 0.5$ V

---

## 3. Galvanostatic Algorithm (DDC Search)

In galvanostatic mode, the **target DDC** (nominal Current Density) is imposed and the code searches for the corresponding anode potential using **bisection**.

### Bisection principle:

```
1. Initialize [V_min, V_max] = [-2.0, 2.0] V
2. For each iteration:
   a. V_mid = (V_min + V_max) / 2
   b. Solve Laplace equation with φ_anode = V_mid
   c. Compute j_avg on cathode via Butler-Volmer
   d. Convert to DDC: DDC_obtained = j_avg / 100
   e. If |DDC_obtained - DDC_target| < tolerance → STOP
   f. If j_avg < j_target → V_max = V_mid (reduce potential)
      Else → V_min = V_mid (increase potential)
3. Keep best solution (minimum error)
```

### Numerical parameters:
| Parameter | Value | Description |
|-----------|-------|-------------|
| Tolerance | 1% | Acceptable relative error |
| Max iterations | 30 | Maximum bisection steps |
| Solver | Newton-Raphson (SNES) | For nonlinear problem |
| Preconditioner | ILU | Incomplete LU factorization |

---

## 4. Faraday's Law (Deposit Thickness)

Local deposit thickness $h$ after time $t_{dep}$:

$$h = \frac{|j| \cdot M \cdot t_{dep} \cdot \varepsilon}{n \cdot F \cdot \rho}$$

Where:
| Symbol | Description | Value |
|--------|-------------|-------|
| $M$ | Ni molar mass | 58.69 g/mol |
| $\rho$ | Ni density | 8908 kg/m³ |
| $\varepsilon$ | Cathodic efficiency | ~0.98 |
| $t_{dep}$ | Deposition time | 300 s (study) |

**Simplified Faraday factor**:
$$\text{faraday\_factor} = \frac{M \cdot t_{dep} \cdot \varepsilon}{n \cdot F \cdot \rho} \times 10^6 \quad [\mu m / (A/m^2)]$$

---

## 5. Uniformity Metrics

### Coefficient of Variation (CV)
$$CV = \frac{\sigma_h}{\bar{h}} \times 100\%$$

Where $\sigma_h$ is the standard deviation and $\bar{h}$ the mean thickness.

| CV | Interpretation |
|----|----------------|
| < 5% | Excellent |
| 5-10% | Good |
| 10-20% | Acceptable |
| > 20% | Needs optimization |

---

## 6. Simulation Results

- **Thickness map**: 3D visualization (VTK exportable) of deposited thickness
- **Current density map**: Spatial distribution of $j$ on cathode
- **Histogram**: Statistical analysis of metal distribution
- **Interactive 3D view**: HTML export via PyVista
