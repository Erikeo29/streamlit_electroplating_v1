# Lexique : Électrodéposition

**Sommaire :**
1. Acronymes Généraux
2. Acronymes Électrochimiques
3. Nombres Adimensionnels
4. Symboles Physiques
5. Termes Techniques
6. Logiciels et Bibliothèques
7. Unités SI

---

## 1. Acronymes Généraux

| Acronyme | Signification | Description |
|----------|---------------|-------------|
| **FEM** | Finite Element Method | Méthode des éléments finis |
| **FVM** | Finite Volume Method | Méthode des volumes finis |
| **BC** | Boundary Condition | Condition aux limites |
| **IC** | Initial Condition | Condition initiale |
| **PDE** | Partial Differential Equation | Équation aux dérivées partielles |
| **DOF** | Degrees of Freedom | Degrés de liberté |
| **SI** | Système International | Système d'unités international |
| **CV%** | Coefficient of Variation | Mesure de dispersion relative |

---

## 2. Acronymes Électrochimiques

| Acronyme | Signification | Description |
|----------|---------------|-------------|
| **ED** | Electrodeposition | Électrodéposition |
| **DDC** | Densité De Courant | Courant par unité de surface |
| **WE** | Working Electrode | Électrode de travail (cathode en ED) |
| **CE** | Counter Electrode | Électrode auxiliaire (anode en ED) |
| **BV** | Butler-Volmer | Équation cinétique de transfert de charge |
| **SCD** | Secondary Current Distribution | Distribution de courant secondaire |
| **PCD** | Primary Current Distribution | Distribution de courant primaire |
| **TCD** | Tertiary Current Distribution | Distribution de courant tertiaire |

---

## 3. Nombres Adimensionnels

| Symbole | Nom | Expression | Signification physique |
|---------|-----|------------|------------------------|
| $Wa$ | Wagner | $\frac{\partial \eta / \partial j}{\kappa / L}$ | Cinétique / Résistance ohmique |
| $Wa$ | Wagner (simplifié) | $\frac{RT/(\alpha n F j_0)}{\rho L}$ | Uniformité du dépôt |

**Interprétation du nombre de Wagner :**
- $Wa \gg 1$ : Distribution uniforme (cinétique dominante)
- $Wa \ll 1$ : Distribution non uniforme (ohmique dominant)
- $Wa \approx 1$ : Régime mixte

---

## 4. Symboles Physiques

### Paramètres Électriques

| Symbole | Nom | Unité SI |
|---------|-----|----------|
| $\phi$ | Potentiel électrique | V |
| $\phi_s$ | Potentiel du solide (électrode) | V |
| $\phi_l$ | Potentiel du liquide (électrolyte) | V |
| $\eta$ | Surtension ($\phi_s - \phi_l - E^0$) | V |
| $I$ | Courant total | A |
| $j$ | Densité de courant | A/m² |
| $j_0$ | Densité de courant d'échange | A/m² |

### Paramètres de Transport

| Symbole | Nom | Unité SI |
|---------|-----|----------|
| $\sigma$ | Conductivité électrolyte | S/m |
| $\rho$ | Résistivité ($1/\sigma$) | Ω·m |
| $\kappa$ | Conductivité (notation alternative) | S/m |

### Paramètres Cinétiques

| Symbole | Nom | Unité SI | Valeurs typiques |
|---------|-----|----------|------------------|
| $\alpha$ | Coefficient de transfert | - | 0.4 - 0.6 |
| $n$ | Nombre d'électrons | - | 2 (Ni²⁺/Ni) |
| $F$ | Constante de Faraday | C/mol | 96485 |
| $R$ | Constante des gaz | J/(mol·K) | 8.314 |
| $T$ | Température | K | 298 (25°C) |

### Paramètres de Dépôt

| Symbole | Nom | Unité SI |
|---------|-----|----------|
| $\delta$ | Épaisseur de dépôt | m (ou µm) |
| $\dot{\delta}$ | Vitesse de croissance | m/s |
| $M$ | Masse molaire du métal | kg/mol |
| $\rho_m$ | Masse volumique du métal | kg/m³ |
| $t$ | Temps de dépôt | s |

---

## 5. Termes Techniques

| Terme | Définition |
|-------|------------|
| **Cathode** | Électrode où se produit la réduction (dépôt du métal) |
| **Anode** | Électrode où se produit l'oxydation |
| **Distribution Primaire** | Distribution de courant régie uniquement par la géométrie et la résistance ohmique |
| **Distribution Secondaire** | Distribution intégrant les surtensions d'activation (Butler-Volmer) |
| **Distribution Tertiaire** | Distribution intégrant le transport de masse (gradients de concentration) |
| **Mode Galvanostatique** | Contrôle du courant total appliqué (recherche automatique du potentiel) |
| **Mode Potentiostatique** | Contrôle du potentiel appliqué |
| **Efficacité Faradique** | Rapport masse déposée réelle / masse théorique (Faraday) |
| **Throwing Power** | Capacité à déposer uniformément dans les recoins |
| **Uniformité** | Capacité à obtenir une épaisseur constante sur toute la surface |

---

## 6. Logiciels et Bibliothèques

| Outil | Type | Usage |
|-------|------|-------|
| **Firedrake** | FEM Python | Résolution équations aux dérivées partielles |
| **GMSH** | Mailleur | Génération de maillages 2D/3D |
| **PyVista** | Visualisation | Post-traitement et rendu 3D |
| **PETSc** | Solveur | Algèbre linéaire haute performance |
| **NumPy** | Calcul | Calcul numérique Python |
| **Pandas** | Données | Manipulation de données tabulaires |

---

## 7. Unités SI

| Grandeur | Unité SI | Symbole | Conversion courante |
|----------|----------|---------|---------------------|
| Courant | Ampère | A | - |
| Potentiel | Volt | V | - |
| Résistance | Ohm | Ω | - |
| Conductivité | Siemens/mètre | S/m | 1 S/cm = 100 S/m |
| Densité de courant | A/m² | A/m² | 1 A/dm² = 100 A/m² |
| Épaisseur | mètre | m | 1 µm = 10⁻⁶ m |
| Temps | seconde | s | 1 min = 60 s |
| Température | Kelvin | K | T(K) = T(°C) + 273.15 |
