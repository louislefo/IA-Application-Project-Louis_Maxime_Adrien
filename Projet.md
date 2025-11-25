# Projet IA - Analyse de Joueurs de Football

**Date de mise à jour :** 25 Novembre 2025

## Description du Projet

Ce projet a pour but d'analyser un jeu de données de joueurs de football (FIFA) afin de :

1.  **Comprendre les données** : Exploration et visualisation des statistiques des joueurs.
2.  **Prédire la performance actuelle** : Utilisation d'un modèle de régression pour estimer la note globale (`overall_rating`) en fonction des attributs physiques et techniques.
3.  **Prédire le développement futur** : Classification des joueurs en catégories de croissance (`high_growth`, `likely_improve`, `stable`, `decline`) basée sur leur potentiel et leur âge.

## Structure du Projet

### Scripts Python (`src/`)

- **`ml_analysis.py`** : Script principal.
  - Charge et nettoie les données.
  - Entraîne un modèle de Régression Linéaire pour prédire le `overall_rating`.
  - Crée une classe cible `future_class` et entraîne une Régression Logistique pour la prédire.
  - Évalue les modèles et teste sur un joueur exemple.
  - Génère un graphique `reg_true_vs_pred.png`.
- **`data_analysis.py`** : Script utilitaire pour vérifier le chargement des données et afficher les informations de base (colonnes, types).

### Notebooks

- **`analyse.ipynb`** : Notebook d'Analyse Exploratoire de Données (EDA).
  - Chargement du CSV.
  - Visualisation des premières lignes et des types de données.
  - Statistiques descriptives (moyenne, écart-type, etc.) pour comprendre la distribution des attributs.

### Données

- `data/fifa_players.csv` : Le jeu de données brut contenant les informations des joueurs.

### Documentation

- `code_explanation.md` : Explication détaillée du fonctionnement du code.
- `Projet.md` : Ce fichier, résumé du projet.
