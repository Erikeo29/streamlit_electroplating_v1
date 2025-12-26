# Welcome to the Electrochemical Simulation Platform

This interactive application brings together advanced modeling tools for studying complex electrochemical phenomena. It is designed as an academic and technical reference for numerical simulation.

## Platform Objectives
- **Visualize** concentration gradients and potential distributions.
- **Compare** different numerical approaches (Finite Element via Python/Firedrake vs Finite Volume via OpenFOAM).
- **Analyze** the impact of physical parameters on experimental results (Voltammograms, Deposition Thickness).

---

## 1. Cyclic Voltammetry (CV)
CV is a powerful electroanalytical technique. Here we model unsteady mass transport coupled with a reversible redox reaction.
- **Python (Firedrake)**: Uses the Finite Element Method (FEM) for high spatial precision.
- **OpenFOAM**: Fluid mechanics-oriented approach for complex geometries.

## 2. Electroplating
Simulation of Nickel electrolytic deposition on specific geometries (3-pad).
- **Galvanostatic Mode**: Automatic search for anode potential to reach a target current density (DDC).
- **Uniformity**: Analysis of thickness distribution and process optimization.

---
*Developed for R&D Projects - Version 1.0.0*