# Glossary: Electroplating

**Table of Contents:**
1. General Acronyms
2. Electrochemical Acronyms
3. Dimensionless Numbers
4. Physical Symbols
5. Technical Terms
6. Software and Libraries
7. SI Units

---

## 1. General Acronyms

| Acronym | Full Name | Description |
|---------|-----------|-------------|
| **FEM** | Finite Element Method | Numerical method for solving PDEs |
| **FVM** | Finite Volume Method | Alternative numerical method |
| **BC** | Boundary Condition | Constraint at domain boundaries |
| **IC** | Initial Condition | Starting state of the system |
| **PDE** | Partial Differential Equation | Governing equations |
| **DOF** | Degrees of Freedom | Number of independent variables |
| **SI** | International System | Standard unit system |
| **CV%** | Coefficient of Variation | Relative dispersion measure |

---

## 2. Electrochemical Acronyms

| Acronym | Full Name | Description |
|---------|-----------|-------------|
| **ED** | Electrodeposition | Electrolytic metal deposition |
| **CD** | Current Density | Current per unit area |
| **WE** | Working Electrode | Electrode of interest (cathode in ED) |
| **CE** | Counter Electrode | Auxiliary electrode (anode in ED) |
| **BV** | Butler-Volmer | Charge transfer kinetic equation |
| **SCD** | Secondary Current Distribution | Distribution with activation overpotential |
| **PCD** | Primary Current Distribution | Ohmic-only distribution |
| **TCD** | Tertiary Current Distribution | Distribution with mass transport |

---

## 3. Dimensionless Numbers

| Symbol | Name | Expression | Physical Meaning |
|--------|------|------------|------------------|
| $Wa$ | Wagner | $\frac{\partial \eta / \partial j}{\kappa / L}$ | Kinetics / Ohmic resistance |
| $Wa$ | Wagner (simplified) | $\frac{RT/(\alpha n F j_0)}{\rho L}$ | Deposit uniformity |

**Wagner Number Interpretation:**
- $Wa \gg 1$: Uniform distribution (kinetics-dominated)
- $Wa \ll 1$: Non-uniform distribution (ohmic-dominated)
- $Wa \approx 1$: Mixed regime

---

## 4. Physical Symbols

### Electrical Parameters

| Symbol | Name | SI Unit |
|--------|------|---------|
| $\phi$ | Electric potential | V |
| $\phi_s$ | Solid potential (electrode) | V |
| $\phi_l$ | Liquid potential (electrolyte) | V |
| $\eta$ | Overpotential ($\phi_s - \phi_l - E^0$) | V |
| $I$ | Total current | A |
| $j$ | Current density | A/m² |
| $j_0$ | Exchange current density | A/m² |

### Transport Parameters

| Symbol | Name | SI Unit |
|--------|------|---------|
| $\sigma$ | Electrolyte conductivity | S/m |
| $\rho$ | Resistivity ($1/\sigma$) | Ω·m |
| $\kappa$ | Conductivity (alternative notation) | S/m |

### Kinetic Parameters

| Symbol | Name | SI Unit | Typical Values |
|--------|------|---------|----------------|
| $\alpha$ | Transfer coefficient | - | 0.4 - 0.6 |
| $n$ | Number of electrons | - | 2 (Ni²⁺/Ni) |
| $F$ | Faraday constant | C/mol | 96485 |
| $R$ | Gas constant | J/(mol·K) | 8.314 |
| $T$ | Temperature | K | 298 (25°C) |

### Deposition Parameters

| Symbol | Name | SI Unit |
|--------|------|---------|
| $\delta$ | Deposit thickness | m (or µm) |
| $\dot{\delta}$ | Growth rate | m/s |
| $M$ | Metal molar mass | kg/mol |
| $\rho_m$ | Metal density | kg/m³ |
| $t$ | Deposition time | s |

---

## 5. Technical Terms

| Term | Definition |
|------|------------|
| **Cathode** | Electrode where reduction occurs (metal deposition) |
| **Anode** | Electrode where oxidation occurs |
| **Primary Distribution** | Current distribution governed only by geometry and ohmic resistance |
| **Secondary Distribution** | Distribution including activation overpotentials (Butler-Volmer) |
| **Tertiary Distribution** | Distribution including mass transport (concentration gradients) |
| **Galvanostatic Mode** | Total current control (automatic potential search) |
| **Potentiostatic Mode** | Applied potential control |
| **Faradaic Efficiency** | Ratio of actual deposited mass to theoretical (Faraday) |
| **Throwing Power** | Ability to deposit uniformly in recesses |
| **Uniformity** | Ability to achieve constant thickness over entire surface |

---

## 6. Software and Libraries

| Tool | Type | Usage |
|------|------|-------|
| **Firedrake** | Python FEM | PDE solving |
| **GMSH** | Mesher | 2D/3D mesh generation |
| **PyVista** | Visualization | Post-processing and 3D rendering |
| **PETSc** | Solver | High-performance linear algebra |
| **NumPy** | Computing | Python numerical computing |
| **Pandas** | Data | Tabular data manipulation |

---

## 7. SI Units

| Quantity | SI Unit | Symbol | Common Conversion |
|----------|---------|--------|-------------------|
| Current | Ampere | A | - |
| Potential | Volt | V | - |
| Resistance | Ohm | Ω | - |
| Conductivity | Siemens/meter | S/m | 1 S/cm = 100 S/m |
| Current density | A/m² | A/m² | 1 A/dm² = 100 A/m² |
| Thickness | meter | m | 1 µm = 10⁻⁶ m |
| Time | second | s | 1 min = 60 s |
| Temperature | Kelvin | K | T(K) = T(°C) + 273.15 |
