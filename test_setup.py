#!/usr/bin/env python3
"""
Script de test pour vérifier que tout fonctionne correctement
"""

import os
import sys
import pandas as pd
import numpy as np

# Ajouter le chemin du projet
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))

def check_data_files():
    """Vérifier que les fichiers de données existent"""
    print("🔍 Vérification des fichiers de données...")
    
    data_path = os.path.join(PROJECT_ROOT, 'data', 'fifa_players.csv')
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        print(f"  ✅ fifa_players.csv trouvé ({len(df)} lignes)")
        return True
    else:
        print(f"  ❌ fifa_players.csv introuvable à {data_path}")
        return False

def check_models():
    """Vérifier que les modèles existent"""
    print("🔍 Vérification des modèles...")
    
    models_dir = os.path.join(PROJECT_ROOT, 'models')
    reg_path = os.path.join(models_dir, 'regression_model.pkl')
    clf_path = os.path.join(models_dir, 'classification_model.pkl')
    
    reg_exists = os.path.exists(reg_path)
    clf_exists = os.path.exists(clf_path)
    
    if reg_exists:
        print(f"  ✅ regression_model.pkl trouvé")
    else:
        print(f"  ❌ regression_model.pkl introuvable")
    
    if clf_exists:
        print(f"  ✅ classification_model.pkl trouvé")
    else:
        print(f"  ❌ classification_model.pkl introuvable")
    
    return reg_exists and clf_exists

def check_dependencies():
    """Vérifier que les dépendances sont installées"""
    print("🔍 Vérification des dépendances...")
    
    required_packages = {
        'streamlit': 'Streamlit',
        'xgboost': 'XGBoost',
        'pandas': 'Pandas',
        'numpy': 'NumPy',
        'sklearn': 'Scikit-learn',
        'joblib': 'Joblib'
    }
    
    all_installed = True
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"  ✅ {name} installé")
        except ImportError:
            print(f"  ❌ {name} NON INSTALLÉ")
            all_installed = False
    
    return all_installed

def test_models():
    """Tester que les modèles fonctionnent"""
    print("🔍 Test des modèles...")
    
    try:
        import joblib
        
        models_dir = os.path.join(PROJECT_ROOT, 'models')
        reg_model = joblib.load(os.path.join(models_dir, 'regression_model.pkl'))
        clf_model = joblib.load(os.path.join(models_dir, 'classification_model.pkl'))
        
        # Test data
        test_data = pd.DataFrame({
            'age': [25],
            'height_cm': [180],
            'weight_kgs': [75],
            'finishing': [80],
            'dribbling': [85],
            'short_passing': [75],
            'acceleration': [85],
            'sprint_speed': [87],
            'stamina': [80],
            'strength': [70]
        })
        
        # Test predictions
        rating = reg_model.predict(test_data)[0]
        future_class = clf_model.predict(test_data)[0]
        
        print(f"  ✅ Régression OK - Note prédite: {rating:.2f}")
        print(f"  ✅ Classification OK - Classe prédite: {future_class}")
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors du test des modèles: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("🚀 VÉRIFICATION DU PROJET AI FOOTBALL ANALYZER")
    print("="*60 + "\n")
    
    results = {
        "Fichiers de données": check_data_files(),
        "Modèles": check_models(),
        "Dépendances": check_dependencies(),
        "Test des modèles": test_models() if check_models() else False
    }
    
    print("\n" + "="*60)
    print("📊 RÉSUMÉ")
    print("="*60)
    
    for check, result in results.items():
        status = "✅ OK" if result else "❌ ERREUR"
        print(f"{check}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ TOUT EST OK ! Vous pouvez lancer l'application :")
        print("   streamlit run src/application.py")
    else:
        print("❌ ERREURS DÉTECTÉES")
        print("\nÉtapes de correction :")
        if not results["Fichiers de données"]:
            print("  1. Téléchargez les données FIFA et placez-les dans data/fifa_players.csv")
        if not results["Modèles"]:
            print("  2. Entraînez les modèles: python src/ml_analysis.py")
        if not results["Dépendances"]:
            print("  3. Installez les dépendances: pip install -r requirements.txt")
    print("="*60 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
