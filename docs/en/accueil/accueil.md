&nbsp;

**Author's note** — *This project was designed entirely by the author, from a blank slate through to publication. Content creation was carried out with the support of artificial intelligence tools, particularly for writing and debugging code and for internet research.
All results shown in this project are derived from analytical and deterministic physical models solved by validated numerical solvers.
This work is released as open-source: it may be freely copied, duplicated, and adapted for learning purposes or for the use of the physical and numerical models presented here.*

&nbsp;

---

**Contents:**
1. Platform Objective
2. Electroplating
3. Navigation
4. Methodological Note

---

## 1. Platform Objective

This interactive application gathers Python-based numerical solving tools for the study of electroplating.

- **Visualize** thickness gradients and current density distributions.
- **Analyze** the impact of electrochemical parameters on deposited thickness.
- **Optimize** designs and deposition conditions.

---

## 2. Electroplating

Simulation of Nickel electrolytic deposition on electrodes with variable geometry.
- **Galvanostatic Mode**: Automatic search for anode potential to reach a target current density (CD).
- **Parametric Study**: Analysis of parameter influence (CD, σ, j₀, α) on thickness distribution.

---

## 3. Navigation

The application is structured around several tools:

1. **Side menu (left)**: main navigation between project sections.
   - **Introduction**: scientific context and electroplating system presentation.
   - **Plating page**: contains Physics, Code and Results tabs to explore the modeling.
   - **Appendices**: conclusion, glossary, key equations and bibliographical references.

2. **Floating navigation buttons (right)**: quick scroll up/down.

3. **AI Assistant (side menu)**: answers questions about the physics or numerical methods.

---

## 4. Methodological Note

The results presented come from **pre-computed** simulations. The project was carried out on a standard laptop: Linux environment via WSL2, 1.5-3.5 GHz processor, 6 CPU / 12 threads, 32 GB RAM. The 2D FEM simulations were performed with various parameter combinations (CD, conductivity, exchange current density, transfer coefficients) as a parametric study.

This application is therefore a **results viewer**, not a real-time simulator. Indeed, running these simulations requires specific environment configurations and Python packages (Firedrake). The codes are available in the "Code" tab so they can be copied and used to reproduce these simulations on other machines.
