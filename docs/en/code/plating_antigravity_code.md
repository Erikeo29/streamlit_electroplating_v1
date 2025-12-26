# Source Code: Electroplating (Antigravity)

Excerpts from the optimized galvanostatic solver.

## 1. Laplace Equation & Butler-Volmer
```python
# Potential in electrolyte
F_form = sigma * inner(grad(phi_solve), grad(v)) * dx

# Activation Overpotential
eta = phi_solve - Constant(E_eq)

# Butler-Volmer Current Density
j_bv = j0 * (exp(alpha_a * f * eta) - exp(-alpha_c * f * eta))

# Adding source term at cathode surface
F_form += j_bv * v * ds(cathode_marker)
```

## 2. Bisection Loop (Galvanostatic Mode)
```python
for iteration in range(max_iterations):
    V_anode_mid = (V_anode_min + V_anode_max) / 2
    V_anode_const.assign(V_anode_mid)
    
    solver.solve()
    j_obtained = compute_cathode_current()
    
    if j_obtained < j_target:
        V_anode_max = V_anode_mid
    else:
        V_anode_min = V_anode_mid
```

## 3. Thickness Calculation (Faraday's Law)
```python
# Conversion factor to thickness (microns)
faraday_factor = (time_deposition * M_Ni * efficiency * 1e6) / (n * F_const * rho_Ni)
thickness = np.abs(j_cathode) * faraday_factor
```