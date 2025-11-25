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

- `code_explanation.md` : Explication détaillée du fonctionnement du code.
- `Projet.md` : Ce fichier, résumé du projet.
