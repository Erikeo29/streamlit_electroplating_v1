# Electroplating Simulation Platform

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40-FF4B4B)
![Status](https://img.shields.io/badge/Status-Stable-green)

Plateforme interactive de simulation pour l'électrodéposition (Nickel), intégrant des modèles numériques avancés et une visualisation 3D.

## 🚀 Fonctionnalités

*   **Simulation Galvanostatique** : Modélisation du dépôt sous densité de courant imposée.
*   **Visualisation 3D Interactive** : Rendu PyVista (Firedrake) intégré pour explorer la répartition de l'épaisseur.
*   **Support Bilingue** : Interface complète en Français et Anglais.
*   **Architecture Modulaire** : Séparation claire entre la physique, le code et les résultats.

## 🛠️ Stack Technique

*   **Interface** : Streamlit
*   **Physique** : Python (Firedrake) & Antigravity (Backend interne)
*   **Visualisation** : PyVista (3D), Matplotlib (2D)

## 📦 Installation

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📂 Structure

*   `app.py` : Point d'entrée de l'application.
*   `assets/` : Ressources statiques (Images, CSS, Modèles 3D HTML).
*   `docs/` : Documentation scientifique (Markdown).
