# History of Voltammetry: From Mercury Drops to Supercomputers

Cyclic Voltammetry (CV) is now the "king" of electrochemical tools, often compared to spectroscopy for its ability to reveal system identity and dynamics. But its history is one of slow maturation.

## 1. The Era of Polarography (1922-1950)
It all started in Prague in 1922. **Jaroslav Heyrovský** invented polarography using a dropping mercury electrode (DME). This constantly renewed surface allowed for reproducible current-potential curves.
*   **1959**: Heyrovský receives the **Nobel Prize in Chemistry**, establishing electroanalysis as a major discipline.
*   *Limitation*: Classical polarography worked at constant potential or very slow variation.

## 2. The Birth of "Cyclic Voltammetry" (1948-1964)
The shift to solid electrodes (Pt, Au, C) and modern electronics allowed for fast triangular signals.
*   **1948**: **Randles** (UK) and **Sevcik** (Czechoslovakia) independently publish the famous peak current equation for linear diffusion:
    $$ I_p = 2.69 \times 10^5 n^{3/2} A D^{1/2} C v^{1/2} $$
*   **1964**: The seminal paper. **Nicholson and Shain** publish in *Analytical Chemistry* the "theory of stationary electrode polarography". They tabulate diagnostic criteria ($\Delta E_p$, $I_{pa}/I_{pc}$) to distinguish reversible, irreversible, and coupled mechanisms (EC, ECE). Modern CV is born.

## 3. The Digital Revolution (1960s-1990s)
Analytical equations becoming too complex for real systems, numerical simulation took over.
*   **Stephen Feldberg** introduces the explicit finite difference method to simulate electrochemical diffusion.
*   **Rudolph Marcus** (Nobel Prize 1992) develops electron transfer theory, providing the microscopic framework that CV measures macroscopically.

## 4. Today: Multi-scale Modeling
Today, CV is no longer interpreted just "by eye". Software (DigiElch, COMSOL, and our Firedrake codes) couples CV with:
*   Convection (Hydrodynamics).
*   Complex 3D geometry (Microelectrodes, MEA).
*   Quantum chemistry (DFT) to predict standard Redox potentials ($E^0$).

CV has evolved from a lab curiosity involving toxic mercury to the standard tool for designing tomorrow's Lithium-Ion batteries.
