# Key Equations

**Table of Contents:**
1. Potential Distribution
2. Cathode Kinetics (Butler-Volmer)
3. Faraday's Law (Deposition Thickness)

Simulation of Nickel (Ni) electrodeposition uses a Secondary Current Distribution model.

---

## 1. Potential Distribution

In the electrolyte, charge conservation follows Ohm's law with constant conductivity $\sigma$:

$$ \nabla \cdot (-\sigma \nabla \phi) = 0 $$

Where:
- $\sigma$ = electrolyte conductivity [S/m]
- $\phi$ = electric potential in the electrolyte [V]

---

## 2. Cathode Kinetics (Butler-Volmer)

Local current density $j$ at the cathode surface is governed by the Butler-Volmer equation:

$$ j = j_0 \left[ \exp\left(\frac{\alpha_a n F}{RT} \eta\right) - \exp\left(-\frac{\alpha_c n F}{RT} \eta\right) \right] $$

Where:
- $j$ = local current density [A/m²]
- $j_0$ = exchange current density [A/m²]
- $\alpha_a$, $\alpha_c$ = anodic and cathodic transfer coefficients
- $n$ = number of electrons transferred
- $F$ = Faraday constant (96485 C/mol)
- $R$ = universal gas constant (8.314 J/(mol·K))
- $T$ = temperature [K]
- $\eta = \phi - E_{eq}$ = activation overpotential [V]

---

## 3. Faraday's Law (Deposition Thickness)

Local deposition thickness $h$ after time $t$ is proportional to local current density and Faradaic efficiency:

$$ h = \frac{j \cdot M \cdot t_{dep} \cdot \varepsilon}{n \cdot F \cdot \rho} $$

Where:
- $M$ is the molar mass of Nickel (58.69 g/mol).
- $\rho$ is the density of Nickel (8908 kg/m³).
- $\varepsilon$ is the cathodic efficiency ($\approx 0.98$).
- $t_{dep}$ is the deposition time [s].
