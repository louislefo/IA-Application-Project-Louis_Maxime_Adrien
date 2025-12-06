# 🚀 Démarrage Rapide de l'Application

## ✅ Checklist de Démarrage

### Étape 1: Vérifier l'Installation
```bash
python test_setup.py
```

Cela va vérifier :
- ✅ Les fichiers de données
- ✅ Les modèles XGBoost
- ✅ Les dépendances Python
- ✅ Que tout fonctionne

### Étape 2: Installer les Dépendances (si nécessaire)
```bash
pip install -r requirements.txt
```

### Étape 3: Entraîner les Modèles (première fois seulement)
```bash
cd src
python ml_analysis.py
```

**Output attendu:**
```
Nombre de joueurs après nettoyage : XXXX

=== Modèle de régression XGBoost (overall_rating) ===
MSE : XXX.XX
R²  : 0.XXX

Importance des features (impact sur la prédiction) :
         Feature  Importance
0  sprint_speed    0.XXXX
1  acceleration    0.XXXX
...

=== Modèle de classification (future_class) ===
              precision    recall  f1-score   support

    high_growth       0.XX      0.XX      0.XX       XXX
   likely_improve     0.XX      0.XX      0.XX       XXX
         stable       0.XX      0.XX      0.XX       XXX
         decline       0.XX      0.XX      0.XX       XXX

Modèles sauvegardés !
```

### Étape 4: Lancer l'Application
```bash
streamlit run src/application.py
```

**Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://XXX.XXX.XXX.XXX:8501
```

L'application s'ouvrira automatiquement dans votre navigateur! 🎉

---

## 📋 Utilisation Basique

1. **Entrez les données du joueur** dans le formulaire du sidebar
2. **Cliquez sur "🔍 Analyser le Joueur"**
3. **Consultez les résultats** :
   - Note globale estimée
   - Trajectoire de carrière prédite
   - Attributs clés
4. **Cliquez sur "💾 Ajouter à la Base de Données"** pour sauvegarder

---

## 🎯 Cas d'Usage

### Cas 1: Évaluer un Joueur Existant
```
1. Trouvez les stats du joueur (ex: Transfermarkt, FIFA)
2. Entrez les données dans l'application
3. Consultez la note XGBoost et la prédiction de carrière
4. Comparez avec d'autres joueurs dans la base
```

### Cas 2: Créer un Profil Fictif
```
1. Imaginez des stats (jeune talent, joueur développé, etc.)
2. Entrez les données
3. Vérifiez que la prédiction a du sens
4. Sauvegardez pour comparaison future
```

### Cas 3: Analyser une Cohorte
```
1. Ajoutez plusieurs joueurs à la base
2. Consultez les statistiques globales en bas
3. Identifiez les patterns (âge moyen, meilleure note, etc.)
```

---

## 🔧 Commandes Utiles

### Redémarrer l'Application
```bash
streamlit run src/application.py --logger.level=debug
```

### Nettoyer la Base de Données Locale
```bash
rm data/added_players.csv
# L'application en créera une nouvelle à la prochaine sauvegarde
```

### Vérifier les Modèles Entraînés
```bash
cd src
python -c "import joblib; reg = joblib.load('../models/regression_model.pkl'); print('Modèle XGBoost OK ✅')"
```

---

## ⚠️ Problèmes Courants

### "Module streamlit not found"
```bash
pip install streamlit --upgrade
```

### "Port 8501 already in use"
```bash
# Utiliser un port différent
streamlit run src/application.py --server.port 8502
```

### "Models not found"
- Assurez-vous que `models/` existe
- Lancez `python src/ml_analysis.py` pour créer les modèles
- Vérifiez que les fichiers `.pkl` existent

### Application lente au premier démarrage
C'est normal! Les modèles sont chargés et mis en cache. Cela n'arrivera plus après.

---

## 📊 Structure des Données

### Input (Formulaire)
```
Nom: string
Âge: 15-40
Taille: 150-210 cm
Poids: 50-100 kg
Finishing, Dribbling, Short Passing, Acceleration, Sprint Speed, Stamina, Strength: 0-100
```

### Output (Prédictions)
```
Note Globale: 0-100 (float)
Classe: "high_growth" | "likely_improve" | "stable" | "decline"
Probabilités: [0.0-1.0] pour chaque classe
```

### Base de Données (added_players.csv)
```
player_name, age, height_cm, weight_kgs, finishing, dribbling, short_passing,
acceleration, sprint_speed, stamina, strength, predicted_overall_rating,
predicted_future_class, date_added
```

---

## 🎓 Pour Plus d'Info

- Consultez `USAGE.md` pour le guide complet
- Consultez `README.md` pour la méthodologie
- Examinez `src/ml_analysis.py` pour le code d'entraînement
- Examinez `src/ml_analysis.ipynb` pour l'analyse détaillée

---

**Bon scouting! ⚽🚀**
