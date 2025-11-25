import pandas as pd
import numpy as np
import os
# --- NOUVEAUX IMPORTS ---
print("DEBUG: script start", flush=True)
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
# ------------------------

file_path = os.path.join(os.path.dirname(__file__), '../data/fifa_players.csv') 

# 1. Chargement des données
try:
    # Lecture du fichier CSV
    df = pd.read_csv(file_path)
    print("Fichier chargé avec succès.")
except FileNotFoundError:
    print(f"ERREUR : Le fichier '{file_path}' n'a pas été trouvé. Vérifiez le nom et l'emplacement.")
    exit()

print("-" * 50)

# 2. Aperçu des données
print("Aperçu des 5 premières lignes du jeu de données (df.head()) :")
print(df.head())

print("-" * 50)

# 3. Informations sur les colonnes et les valeurs manquantes
print("Information sur les colonnes (df.info()) :")
# verbose=False et memory_usage="deep" permettent un aperçu rapide et précis.
df.info(verbose=False, memory_usage="deep")


# --- Étape de Prétraitement des Données (nettoyage des données impropres du csv) ---

# 1. Convertir 'national_rating' en numérique
# 'errors='coerce'' remplace toutes les valeurs non numériques par NaN.
df['national_rating'] = pd.to_numeric(df['national_rating'], errors='coerce') 

# 2. Convertir les colonnes financières en float.
financial_cols = ['value_euro', 'wage_euro', 'release_clause_euro']
for col in financial_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 3. Imputation (Remplacer les valeurs manquantes)
# Pour les valeurs/salaires, on remplace les NaN par la médiane (moins sensible aux extrêmes)
for col in ['value_euro', 'wage_euro']:
    median_val = df[col].median()
    df[col].fillna(median_val, inplace=True)
    
# Pour les clauses libératoires et les notes nationales, on remplace les NaN par 0.
# (Absence de clause ou absence de sélection nationale)
df['release_clause_euro'].fillna(0, inplace=True)
df['national_rating'].fillna(0, inplace=True)

# 4. Vérification après nettoyage
print("Vérification des 5 premières lignes après nettoyage des valeurs :")
print(df[['value_euro', 'wage_euro', 'release_clause_euro', 'national_rating']].head(), flush=True)

print("-" * 50)

# --- Étape d'Ingénierie des Fonctionnalités ---
# L'encodage One-Hot convertit une colonne textuelle (catégorielle) en plusieurs colonnes binaires (0 ou 1).

# 1. Extraire la position principale (la première dans la liste)
df['main_position'] = df['positions'].apply(lambda x: str(x).split(',')[0].strip())

# 2. Appliquer le One-Hot Encoding
df_encoded = pd.get_dummies(df, columns=['main_position'], prefix='pos')

# 3. Sélection des colonnes pour le modèle
# Variables Cibles (Y) et Variables Prédictives (X)
y = df_encoded['overall_rating']

# Suppression des colonnes inutiles ou d'identification
cols_to_drop = [
    'overall_rating', 'id', 'url', 'name', 'full_name', 'birth_date', 
    'nationality', 'positions', 'preferred_foot', 'body_type', 
    'national_team', 'national_team_position', 'national_jersey_number'
]
X = df_encoded.drop(columns=cols_to_drop, errors='ignore')

# 4. Gestion finale des NaN (remplacer les éventuels NaN restants par la moyenne de la colonne)
X = X.fillna(X.mean())

print("Préparation du Modèle Terminé :")
print(f"  - Caractéristiques (X) prêtes : {X.shape[0]} lignes, {X.shape[1]} colonnes.")
print(f"  - Variable Cible (Y) prête : {y.shape[0]} lignes.")

print("-" * 50)


# --- Étape de Modélisation ---

# Tâche 8.1 : Séparation des données (Train/Test Split)
# test_size=0.2 signifie 20% des données seront utilisées pour tester le modèle
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Séparation des données (Train/Test Split) :")
print(f"  - Ensemble d'Entraînement : {X_train.shape[0]} joueurs")
print(f"  - Ensemble de Test : {X_test.shape[0]} joueurs")
print("-" * 50)

# Tâche 8.2 : Entraînement et Évaluation du Modèle (Random Forest Regressor)

# 1. Instancier le Modèle
model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1) 

# 2. Entraînement 🧠
print("Début de l'entraînement du modèle Random Forest...")
model.fit(X_train, y_train)
print("Entraînement Terminé.")

# 3. Prédiction
y_pred = model.predict(X_test)

# 4. Évaluation des Performances (Section IV. Evaluation & Analysis)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("-" * 50)
print("Résultats de la Modélisation (Random Forest Regressor) :")
print(f"  - Mean Absolute Error (MAE) : {mae:.3f} points")
print(f"  - R-squared (R2 Score) : {r2:.4f} (Qualité de la prédiction)")
print("-" * 50)