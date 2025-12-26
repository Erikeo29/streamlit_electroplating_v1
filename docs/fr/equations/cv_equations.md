# Équations Clés : Voltamétrie Cyclique (CV)

La modélisation de la voltamétrie cyclique repose sur la résolution du transport de masse des espèces électroactives couplé à la cinétique de transfert de charge à l'interface électrode/électrolyte.

## 1. Transport de Masse
Dans une solution support en excès, la migration est négligée. Le transport est régi par la loi de diffusion de Fick :

$$ \frac{\partial c_i}{\partial t} = D_i \nabla^2 c_i $$

Où :
- $c_i$ est la concentration de l'espèce $i$ (Oxydant $O$ ou Réducteur $R$) [mol/m³].
- $D_i$ est le coefficient de diffusion [m²/s].

## 2. Cinétique à l'Électrode (Butler-Volmer)
Le flux molaire à la surface de l'électrode de travail (WE) est défini par la relation de Butler-Volmer :

$$ J = k_0 \left[ c_R \exp\left(\frac{\alpha n F}{RT} \eta\right) - c_O \exp\left(-\frac{(1-\alpha) n F}{RT} \eta\right) \right] $$

Avec la surtension $\eta = E(t) - E^0$.

### Paramètres de simulation :
- Constante de Faraday $F = 96485$ C/mol
- Température $T = 298.15$ K
- Coefficient de transfert $\alpha = 0.5$
- Vitesse de réaction standard $k_0 \approx 10^{-5}$ m/s

## 3. Signal de Potentiel (Cycles)
Le potentiel appliqué $E(t)$ suit un signal triangulaire périodique. Une expérience peut comporter plusieurs cycles consécutifs ($N > 1$) :

$$ E(t) = \begin{cases} E_{start} + v \cdot t & \text{Aller (Anodique)} \\ E_{vertex} - v \cdot t & \text{Retour (Cathodique)} \end{cases} $$

L'enregistrement de plusieurs cycles permet de vérifier la stabilité du système (conditionnement de l'électrode) ou d'observer des réactions secondaires (adsorption, passivation).

## 4. Analyse Morphologique : D'où vient la forme ?
L'allure caractéristique en "bec de canard" du voltammogramme résulte d'une compétition entre deux phénomènes antagonistes :

1.  **La Montée du Courant (Contrôle Cinétique) :** Au début, l'augmentation du potentiel ($\eta$) accélère exponentiellement la vitesse de transfert d'électrons (loi de Butler-Volmer). Le courant augmente.
2.  **Le Pic et la Chute (Contrôle Diffusif) :** À force de consommer l'espèce réactive à la surface, sa concentration locale chute vers zéro (`déplétion`). Il se crée une **couche de diffusion** dont l'épaisseur $\delta(t)$ augmente avec le temps ($\delta \propto \sqrt{Dt}$). Le gradient de concentration s'adoucit, et le flux de matière diminue, provoquant la chute du courant après le pic (loi de Cottrell en $t^{-1/2}$). 

## 5. Diagnostics : Réversibilité et Vitesse
L'analyse de la forme des pics permet de qualifier le système.

### A. L'écart de Pic ($\Delta E_p$)
C'est la différence de potentiel entre le pic anodique et le pic cathodique : $\Delta E_p = |E_{pa} - E_{pc}|$.
- **Système Réversible (Rapide) :** Le transfert d'électrons est instantané devant la diffusion.
  $$ \Delta E_p \approx \frac{59 \text{ mV}}{n} \quad (\text{à } 25^\circ\text{C}) $$
  Cet écart est constant, quelle que soit la vitesse de balayage $v$.
- **Système Quasi-Réversible / Irréversible (Lent) :** La cinétique ($k_0$) limite la réaction. Les pics s'écartent l'un de l'autre lorsque la vitesse $v$ augmente.

### B. Influence de la Vitesse ($v$)
Pour un système réversible contrôlé par la diffusion, le courant de pic suit l'équation de **Randles-Sevcik** :

$$ I_p = (2.69 \times 10^5) \, n^{3/2} \, A \, D^{1/2} \, C^* \, v^{1/2} $$

- Si $I_p$ est proportionnel à $\sqrt{v}$, le processus est contrôlé par la diffusion pure.
- Si $I_p$ est proportionnel à $v$, le processus implique des espèces adsorbées (capacitif).