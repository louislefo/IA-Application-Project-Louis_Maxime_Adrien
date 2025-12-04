# 🚀 Guide d'Utilisation - AI Football Performance Analyzer

## Démarrage Rapide

### 1️⃣ Entraîner les Modèles
Avant de lancer l'application, vous devez d'abord entraîner les modèles XGBoost :

```bash
cd src
python ml_analysis.py
```

Cela va :
- Charger et nettoyer les données FIFA
- Entraîner le modèle **XGBoost Regressor** (prédire la note globale)
- Entraîner le modèle **Logistic Regression Classifier** (prédire la trajectoire de carrière)
- Sauvegarder les modèles dans `models/regression_model.pkl` et `models/classification_model.pkl`

### 2️⃣ Lancer l'Application Web
Une fois les modèles entraînés, lancez l'application Streamlit :

```bash
streamlit run src/application.py
```

L'application s'ouvrira automatiquement dans votre navigateur à `http://localhost:8501`

---

## 📱 Guide d'Utilisation de l'Application

### 🎮 Interface Principale

L'application se compose de deux sections principales :

#### **Barre Latérale (Sidebar) - Formulaire d'Entrée**

Complétez tous les champs pour évaluer un joueur :

1. **Informations Générales**
   - 🎫 **Nom du joueur** : Entrez le nom du joueur à analyser
   - 🎂 **Âge** : Entre 15 et 40 ans (slider)
   - 📏 **Taille** : Entre 150 cm et 210 cm
   - ⚖️ **Poids** : Entre 50 kg et 100 kg

2. **Attributs Techniques & Physiques**
   - 🎯 **Finishing** : Capacité à finir les occasions (0-100)
   - 🎮 **Dribbling** : Dribble et contrôle du ballon (0-100)
   - 📤 **Short Passing** : Précision des passes courtes (0-100)
   - 💨 **Acceleration** : Accélération rapide (0-100)
   - 🏃 **Sprint Speed** : Vitesse en ligne droite (0-100)
   - ⚡ **Stamina** : Endurance pendant le match (0-100)
   - 💪 **Strength** : Force physique (0-100)

#### **Zone Principale - Affichage des Résultats**

Après avoir cliqué sur **"🔍 Analyser le Joueur"** :

1. **Tableau des Profils du Joueur**
   - Affiche tous les attributs entrés

2. **Graphique de Visualisation**
   - Graphique en barres montrant tous les attributs
   - Aide à identifier les points forts et faibles visuellement

3. **Résultats d'Analyse**
   - **📈 Note Globale Estimée** : La note prédite par XGBoost (0-100)
   - **⚡ Attribut Fort** : L'attribut le plus élevé du joueur
   - **📊 Attribut à Travailler** : L'attribut avec le score le plus faible

4. **🔮 Prédiction de Trajectoire Professionnelle**

   Le modèle classe les joueurs en 4 catégories :

   - **✨ FUTURE SUPERSTAR** (High Growth)
     - Jeune joueur avec énorme potentiel
     - Progression attendue très importante
     - À absolument recruter/développer

   - **📈 POTENTIEL SOLIDE** (Likely Improve)
     - Joueur pouvant s'améliorer significativement
     - Bonne trajectoire professionnelle
     - Investissement intéressant

   - **⚖️ JOUEUR STABLE** (Stable)
     - Joueur ayant atteint son niveau de croisière
     - Pas de progression majeure prévisible
     - Fiable pour le court terme

   - **📉 EN DÉCLIN** (Decline)
     - Joueur vieillissant ou stagnant
     - Performance future peut diminuer
     - À surveiller attentivement

5. **Probabilités par Classe**
   - Affiche la probabilité en pourcentage pour chaque catégorie

### 💾 Ajouter à la Base de Données

Une fois l'analyse effectuée, cliquez sur **"💾 Ajouter à la Base de Données"** pour :
- Sauvegarder le joueur dans `data/added_players.csv`
- Inclure la note prédite et la catégorie de carrière
- Enregistrer la date/heure d'ajout

### 📚 Base de Données des Joueurs

La section en bas affiche :
- **Liste complète** des tous les joueurs ajoutés
- **Statistiques globales** :
  - Total de joueurs ajoutés
  - Note moyenne des joueurs
  - Âge moyen
  - Nombre de futures superstars

---

## 🔧 Détails Techniques

### Modèles Utilisés

#### **XGBoost Regressor** (Note Globale)
- **Performance** : R² > 0.85 (très bon)
- **Avantages** :
  - Capture les relations non-linéaires
  - Meilleure précision que Linear Regression
  - Robuste aux données réelles
  - Feature importance intégrée

#### **Logistic Regression Classifier** (Trajectoire)
- **Classes** : 4 catégories de carrière
- **Avantages** :
  - Probabilités bien calibrées
  - Interprétabilité élevée
  - Rapide et fiable

### Structure des Fichiers

```
project/
├── src/
│   ├── application.py          # Application Streamlit principale
│   ├── ml_analysis.py          # Script d'entraînement
│   ├── ml_analysis.ipynb       # Notebook d'analyse
│   └── ml_advanced_models.ipynb # Notebook avancé
├── data/
│   ├── fifa_players.csv        # Données originales
│   └── added_players.csv       # Joueurs ajoutés via l'app
├── models/
│   ├── regression_model.pkl    # Modèle XGBoost
│   └── classification_model.pkl# Modèle Logistic Regression
└── requirements.txt            # Dépendances Python
```

---

## 🐛 Dépannage

### Erreur : "Modèles introuvables"
**Solution** : Exécutez d'abord `python ml_analysis.py` dans le dossier `src/` pour entraîner les modèles.

### Erreur : "Module streamlit non trouvé"
**Solution** : Installez les dépendances : `pip install -r requirements.txt`

### Application lente
**Solution** : Les modèles sont mis en cache. La première exécution est normale.

---

## 📊 Exemples d'Utilisation

### Exemple 1 : Jeune talent
```
Nom: Vinicius Jr
Âge: 20
Taille: 180 cm
Poids: 73 kg
Attributs: Dribbling 88, Speed 90, Stamina 82
→ Note prédite: ~78-80
→ Classe: HIGH_GROWTH ✨
```

### Exemple 2 : Joueur établi
```
Nom: Benzema
Âge: 35
Taille: 185 cm
Poids: 80 kg
Attributs: Finishing 92, Short Pass 88, Stamina 75
→ Note prédite: ~83-85
→ Classe: STABLE ⚖️
```

---

## 💡 Conseils d'Utilisation

1. **Entrez des données réalistes** : Les attributs doivent être cohérents entre eux
2. **Utilisez la visualisation** : Le graphique en barres aide à identifier les incohérences
3. **Consultez les probabilités** : Elles montrent la confiance du modèle
4. **Comparez les joueurs** : Ajoutez plusieurs joueurs pour les comparer dans la base de données

---

## 📞 Support

Pour toute question ou bug, consultez le README principal du projet.

Bon scouting! ⚽🚀
