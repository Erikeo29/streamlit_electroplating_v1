# Équations clés

**Sommaire :**
1. Distribution du Potentiel
2. Cinétique à la Cathode (Butler-Volmer)
3. Loi de Faraday (Épaisseur du dépôt)

La simulation de l'électrodéposition du Nickel (Ni) utilise un modèle de distribution de courant secondaire (Secondary Current Distribution).

---

## 1. Distribution du Potentiel

Dans l'électrolyte, la conservation de la charge suit la loi d'Ohm avec une conductivité $\sigma$ constante :

$$ \nabla \cdot (-\sigma \nabla \phi) = 0 $$

Où :
- $\sigma$ = conductivité de l'électrolyte [S/m]
- $\phi$ = potentiel électrique dans l'électrolyte [V]

---

## 2. Cinétique à la Cathode (Butler-Volmer)

La densité de courant locale $j$ à la surface de la cathode est régie par l'équation de Butler-Volmer :

$$ j = j_0 \left[ \exp\left(\frac{\alpha_a n F}{RT} \eta\right) - \exp\left(-\frac{\alpha_c n F}{RT} \eta\right) \right] $$

Où :
- $j$ = densité de courant locale [A/m²]
- $j_0$ = densité de courant d'échange [A/m²]
- $\alpha_a$, $\alpha_c$ = coefficients de transfert anodique et cathodique
- $n$ = nombre d'électrons échangés
- $F$ = constante de Faraday (96485 C/mol)
- $R$ = constante des gaz parfaits (8.314 J/(mol·K))
- $T$ = température [K]
- $\eta = \phi - E_{eq}$ = surtension d'activation [V]

---

## 3. Loi de Faraday (Épaisseur du dépôt)

L'épaisseur locale du dépôt $h$ après un temps $t$ est proportionnelle à la densité de courant locale et à l'efficacité faradique :

$$ h = \frac{j \cdot M \cdot t_{dep} \cdot \varepsilon}{n \cdot F \cdot \rho} $$

Où :
- $M$ est la masse molaire du Nickel (58.69 g/mol).
- $\rho$ est la masse volumique du Nickel (8908 kg/m³).
- $\varepsilon$ est l'efficacité cathodique ($\approx 0.98$).
- $t_{dep}$ est le temps de déposition [s].
