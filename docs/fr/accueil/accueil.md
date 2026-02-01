&nbsp;

**Note de l'auteur** — *Ce projet a été conçu intégralement par l'auteur, depuis une page blanche jusqu'à sa mise en ligne. La création du contenu a été réalisée avec le support d'outils d'intelligence artificielle en particulier pour la rédaction et la correction des codes et pour les recherches internet.
Tous les résultats montrés dans ce projet sont issus de modèles physiques analytiques et déterministes résolus par des solveurs numériques validés.
Ce travail est mis à disposition en open-source : il peut être librement copié, dupliqué et adapté à des fins d'apprentissage ou d'exploitation des modèles physiques et numériques présentés.*

&nbsp;

---

**Sommaire :**
1. Objectif de la plateforme
2. Électrodéposition (Plating)
3. Navigation
4. Note méthodologique

---

## 1. Objectif de la plateforme

Cette application interactive regroupe des outils de résolution numériques basés sur Python pour l'étude de l'électrodéposition.

- **Visualiser** les gradients d'épaisseur et les distributions de densité de courant.
- **Analyser** l'impact des paramètres électrochimiques sur l'épaisseur de dépôt.
- **Optimiser** les designs et les conditions de dépôt.

---

## 2. Électrodéposition (Plating)

Simulation du dépôt électrolytique de Nickel sur des électrodes à géométrie variable.
- **Mode Galvanostatique** : Recherche automatique du potentiel d'anode pour atteindre une densité de courant cible (DDC).
- **Étude paramétrique** : Analyse de l'influence des paramètres (DDC, σ, j₀, α) sur la distribution d'épaisseur.

---

## 3. Navigation

L'application est structurée autour de plusieurs outils :

1. **Menu latéral (à gauche)** : navigation principale entre les sections du projet.
   - **Introduction** : contexte scientifique et présentation du système d'électrodéposition.
   - **Page Plating** : contient des onglets Physique, Code et Résultats pour explorer la modélisation.
   - **Annexes** : conclusion, lexique technique, équations clés et références bibliographiques.

2. **Boutons de navigation flottants (à droite)** : déplacement rapide haut/bas de page.

3. **Assistant IA (menu latéral)** : réponses aux questions sur la physique ou les méthodes numériques.

---

## 4. Note méthodologique

Les résultats présentés proviennent de simulations **pré-calculées**. Le projet a été réalisé sur un PC portable standard : environnement Linux via WSL2, processeur 1.5-3.5 GHz, 6 CPU / 12 threads, 32 Go de RAM. Les simulations FEM 2D ont été réalisées avec différentes combinaisons de paramètres (DDC, conductivité, densité de courant d'échange, coefficients de transfert) sous forme d'étude paramétrique.

Cette application est donc un **visualiseur de résultats**, non un simulateur en temps réel. En effet, la réalisation de ces simulations nécessite des configurations spécifiques d'environnements et de packages Python (Firedrake). Les codes sont disponibles dans l'onglet "Code" afin de permettre leur reproduction sur d'autres machines.
