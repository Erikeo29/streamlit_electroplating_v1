# Key Equations: Cyclic Voltammetry (CV)

Modeling cyclic voltammetry relies on solving mass transport of electroactive species coupled with charge transfer kinetics at the electrode/electrolyte interface.

## 1. Mass Transport
In an excess supporting electrolyte, migration is neglected. Transport is governed by Fick's diffusion law:

$$ \frac{\partial c_i}{\partial t} = D_i \nabla^2 c_i $$

Where:
- $c_i$ is the concentration of species $i$ (Oxidant $O$ or Reductant $R$) [mol/m³].
- $D_i$ is the diffusion coefficient [m²/s].

## 2. Electrode Kinetics (Butler-Volmer)
The molar flux at the Working Electrode (WE) surface is defined by the Butler-Volmer relation:

$$ J = k_0 \left[ c_R \exp\left(\frac{\alpha n F}{RT} \eta\right) - c_O \exp\left(-\frac{(1-\alpha) n F}{RT} \eta\right) \right] $$

With overpotential $\eta = E(t) - E^0$.

### Simulation Parameters:
- Faraday Constant $F = 96485$ C/mol
- Temperature $T = 298.15$ K
- Transfer Coefficient $\alpha = 0.5$
- Standard Reaction Rate $k_0 \approx 10^{-5}$ m/s

## 3. Potential Signal (Cycles)
The applied potential $E(t)$ follows a periodic triangular waveform. An experiment often consists of several consecutive cycles ($N > 1$):

$$ E(t) = \begin{cases} E_{start} + v \cdot t & \text{Forward (Anodic)} \\ E_{vertex} - v \cdot t & \text{Reverse (Cathodic)} \end{cases} $$

Recording multiple cycles helps verify system stability (electrode conditioning) or observe secondary reactions (adsorption, passivation).

## 4. Morphological Analysis: Origin of the Shape
The characteristic "duck-shaped" voltammogram results from a competition between two opposing phenomena:

1.  **Current Rise (Kinetic Control):** Initially, the increasing potential ($\eta$) exponentially accelerates the electron transfer rate (Butler-Volmer law). The current rises.
2.  **Peak and Decay (Diffusion Control):** As the reactant at the surface is consumed, its local concentration drops to zero (`depletion`). A **diffusion layer** creates, with thickness $\delta(t)$ increasing over time ($\delta \propto \sqrt{Dt}$). The concentration gradient softens, and the mass flux decreases, causing the current to fall after the peak (Cottrell behavior in $t^{-1/2}$). 

## 5. Diagnostics: Reversibility and Scan Rate
Analyzing peak shape qualifies the system.

### A. Peak Separation ($\Delta E_p$)
This is the potential difference between the anodic and cathodic peaks: $\Delta E_p = |E_{pa} - E_{pc}|$.
- **Reversible System (Fast):** Electron transfer is instantaneous compared to diffusion.
  $$ \Delta E_p \approx \frac{59 \text{ mV}}{n} \quad (\text{at } 25^\circ\text{C}) $$
  This separation is constant, regardless of scan rate $v$.
- **Quasi-Reversible / Irreversible System (Slow):** Kinetics ($k_0$) limit the reaction. Peaks separate further as scan rate $v$ increases.

### B. Influence of Scan Rate ($v$)
For a reversible diffusion-controlled system, the peak current follows the **Randles-Sevcik** equation:

$$ I_p = (2.69 \times 10^5) \, n^{3/2} \, A \, D^{1/2} \, C^* \, v^{1/2} $$

- If $I_p$ is proportional to $\sqrt{v}$, the process is controlled by pure diffusion.
- If $I_p$ is proportional to $v$, the process involves adsorbed species (capacitive).
