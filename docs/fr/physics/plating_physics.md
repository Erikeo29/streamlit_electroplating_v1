Ce module simule la croissance d'une couche de Nickel sur un substrat complexe en mode galvanostatique.

---

## 1. Distribution Secondaire de Courant

Le modèle résout l'équation de **Laplace** pour le potentiel électrique $\phi$ dans l'électrolyte :

$$\nabla \cdot (-\sigma \nabla \phi) = 0$$

Où :
- $\sigma$ = conductivité de l'électrolyte [S/m]
- $\phi$ = potentiel électrique [V]

**Conditions aux limites :**
- **Anode** : $\phi = V_{anode}$ (Dirichlet, potentiel imposé)
- **Cathode** : flux imposé par cinétique Butler-Volmer (Neumann non-linéaire)
- **Parois** : flux nul $\nabla \phi \cdot \mathbf{n} = 0$

---

## 2. Cinétique Butler-Volmer

La densité de courant locale $j$ à la surface de la cathode suit l'équation de Butler-Volmer :

$$j = j_0 \left[ \exp\left(\frac{\alpha_a n F}{RT} \eta\right) - \exp\left(-\frac{\alpha_c n F}{RT} \eta\right) \right]$$

Où :
| Symbole | Description | Valeur typique |
|---------|-------------|----------------|
| $j_0$ | Densité de courant d'échange | 0.34 - 1.36 A/m² |
| $\alpha_a, \alpha_c$ | Coefficients de transfert | 0.4 - 0.6 |
| $n$ | Nombre d'électrons échangés | 2 (Ni²⁺) |
| $F$ | Constante de Faraday | 96485 C/mol |
| $R$ | Constante des gaz | 8.314 J/(mol·K) |
| $T$ | Température | 298 K |
| $\eta$ | Surtension d'activation | $\phi_{local} - E_{eq}$ |
| $E_{eq}$ | Potentiel d'équilibre Ni²⁺/Ni | -0.257 V vs SHE |

**Protection numérique** : Pour éviter les débordements exponentiels, $\eta$ est limité :
$$\eta_{safe} = \text{clip}(\eta, -\eta_{max}, +\eta_{max})$$ avec $\eta_{max} = 0.5$ V

---

## 3. Algorithme Galvanostatique (Recherche de DDC)

En mode galvanostatique, on impose la **DDC cible** (Densité de Courant nominale) et le code recherche le potentiel d'anode correspondant par **bissection**.

### Principe de la bissection :

```
1. Initialiser [V_min, V_max] = [-2.0, 2.0] V
2. Pour chaque itération :
   a. V_mid = (V_min + V_max) / 2
   b. Résoudre l'équation de Laplace avec φ_anode = V_mid
   c. Calculer j_avg sur la cathode via Butler-Volmer
   d. Convertir en DDC : DDC_obtenue = j_avg / 100
   e. Si |DDC_obtenue - DDC_cible| < tolérance → STOP
   f. Si j_avg < j_cible → V_max = V_mid (réduire le potentiel)
      Sinon → V_min = V_mid (augmenter le potentiel)
3. Conserver la meilleure solution (erreur minimale)
```

### Paramètres numériques :
| Paramètre | Valeur | Description |
|-----------|--------|-------------|
| Tolérance | 1% | Erreur relative acceptable |
| Max iterations | 30 | Nombre maximal de bissections |
| Solveur | Newton-Raphson (SNES) | Pour le problème non-linéaire |
| Préconditionneur | ILU | Incomplete LU factorization |

---

## 4. Loi de Faraday (Épaisseur du dépôt)

L'épaisseur locale du dépôt $h$ après un temps $t_{dep}$ :

$$h = \frac{|j| \cdot M \cdot t_{dep} \cdot \varepsilon}{n \cdot F \cdot \rho}$$

Où :
| Symbole | Description | Valeur |
|---------|-------------|--------|
| $M$ | Masse molaire Ni | 58.69 g/mol |
| $\rho$ | Masse volumique Ni | 8908 kg/m³ |
| $\varepsilon$ | Efficacité cathodique | ~0.98 |
| $t_{dep}$ | Temps de déposition | 300 s (étude) |

**Facteur de Faraday simplifié** :
$$\text{faraday\_factor} = \frac{M \cdot t_{dep} \cdot \varepsilon}{n \cdot F \cdot \rho} \times 10^6 \quad [\mu m / (A/m^2)]$$

---

## 5. Métriques d'Uniformité

### Coefficient de Variation (CV)
$$CV = \frac{\sigma_h}{\bar{h}} \times 100\%$$

Où $\sigma_h$ est l'écart-type et $\bar{h}$ la moyenne de l'épaisseur.

| CV | Interprétation |
|----|----------------|
| < 5% | Excellent |
| 5-10% | Bon |
| 10-20% | Acceptable |
| > 20% | À optimiser |

---

## 6. Résultats de Simulation

- **Carte d'épaisseur** : Visualisation 3D (exportable en VTK) de l'épaisseur déposée
- **Carte de densité de courant** : Distribution spatiale de $j$ sur la cathode
- **Histogramme** : Analyse statistique de la répartition du métal
- **Vue 3D interactive** : Export HTML via PyVista
