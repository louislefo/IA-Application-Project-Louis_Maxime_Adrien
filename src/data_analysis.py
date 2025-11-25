import pandas as pd
import numpy as np
import os

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