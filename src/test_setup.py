#!/usr/bin/env python3
"""
Test script to verify that everything in the project works correctly
"""

import os
import sys
import pandas as pd
import numpy as np

# Add the project path so we can import from src when running this file directly.
# This makes "src" behave like an importable package when you run this file from the project root.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))


def check_data_files():
    """Check that the data files exist and can be loaded"""
    # High-level check: makes sure the main CSV is present and readable.
    print("🔍 Checking data files...")
    
    data_path = os.path.join(PROJECT_ROOT, 'data', 'fifa_players.csv')
    if os.path.exists(data_path):
        # If the file exists, we also try to load it to catch encoding / parsing issues early.
        df = pd.read_csv(data_path)
        print(f"  ✅ fifa_players.csv found ({len(df)} rows)")
        return True
    else:
        # If this fails, the rest of the ML pipeline will not work because it depends on this file.
        print(f"  ❌ fifa_players.csv NOT FOUND at {data_path}")
        return False


def check_models():
    """Check that the saved model files exist"""
    # This checks that you already trained and saved the models (regression & classification).
    print("🔍 Checking models...")
    
    models_dir = os.path.join(PROJECT_ROOT, 'models')
    reg_path = os.path.join(models_dir, 'regression_model.pkl')
    clf_path = os.path.join(models_dir, 'classification_model.pkl')
    
    reg_exists = os.path.exists(reg_path)
    clf_exists = os.path.exists(clf_path)
    
    # One message per model so you immediately see which one is missing.
    if reg_exists:
        print(f"  ✅ regression_model.pkl found")
    else:
        print(f"  ❌ regression_model.pkl NOT FOUND")
    
    if clf_exists:
        print(f"  ✅ classification_model.pkl found")
    else:
        print(f"  ❌ classification_model.pkl NOT FOUND")
    
    # Only returns True if BOTH models are present.
    return reg_exists and clf_exists


def check_dependencies():
    """Check that the required Python dependencies are installed"""
    # This gives a quick overview of the Python environment status.
    print("🔍 Checking dependencies...")
    
    # Keys = import names, values = human-readable names printed to the user.
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
            # __import__ dynamically imports a module by its string name.
            __import__(package)
            print(f"  ✅ {name} installed")
        except ImportError:
            # If one dependency is missing, we keep going to show the full list of problems.
            print(f"  ❌ {name} NOT INSTALLED")
            all_installed = False
    
    # True only if every required package was successfully imported.
    return all_installed


def test_models():
    """Test that the models can be loaded and used for predictions"""
    # This is like a mini end-to-end test of the ML pipeline.
    print("🔍 Testing models...")
    
    try:
        import joblib
        
        models_dir = os.path.join(PROJECT_ROOT, 'models')
        reg_model = joblib.load(os.path.join(models_dir, 'regression_model.pkl'))
        clf_model = joblib.load(os.path.join(models_dir, 'classification_model.pkl'))
        
        # Small dummy input to check end-to-end predictions.
        # ⚠️ The columns here must match the features used during training.
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
        
        # Test predictions with both models:
        # - regression: predicts an overall rating (float)
        # - classification: predicts a future class label (string)
        rating = reg_model.predict(test_data)[0]
        future_class = clf_model.predict(test_data)[0]
        
        print(f"  ✅ Regression OK - Predicted rating: {rating:.2f}")
        print(f"  ✅ Classification OK - Predicted class: {future_class}")
        return True
        
    except Exception as e:
        # Any error here usually means:
        # - models are incompatible with the current code,
        # - feature names do not match,
        # - or the pickle files are corrupted / missing.
        print(f"  ❌ Error while testing models: {e}")
        return False


def main():
    # Pretty header to clearly delimit the global check in the terminal.
    print("\n" + "="*60)
    print("🚀 PROJECT CHECK: AI FOOTBALL ANALYZER")
    print("="*60 + "\n")
    
    # Run all checks and collect the results in a dict.
    # Keys stay in French because they are reused in messages later.
    results = {
        "Fichiers de données": check_data_files(),
        "Modèles": check_models(),
        "Dépendances": check_dependencies(),
        "Test des modèles": test_models() if check_models() else False
    }
    
    # Global summary of all checks.
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    
    for check, result in results.items():
        status = "✅ OK" if result else "❌ ERROR"
        print(f"{check}: {status}")
    
    # Global success flag: True only if ALL checks passed.
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        # Everything is good: user can launch the Streamlit app.
        print("✅ EVERYTHING IS OK! You can launch the application with:")
        print("   streamlit run src/application.py")
    else:
        # At least one check failed: display actionable next steps.
        print("❌ ERRORS DETECTED")
        print("\nSteps to fix:")
        if not results["Fichiers de données"]:
            print("  1. Download the FIFA data and place it in data/fifa_players.csv")
        if not results["Modèles"]:
            print("  2. Train the models: python src/ml_analysis.py")
        if not results["Dépendances"]:
            print("  3. Install dependencies: pip install -r requirements.txt")
    print("="*60 + "\n")
    
    # Exit code convention:
    # 0 = success, 1 = something is wrong (useful in CI or shell scripts).
    return 0 if all_passed else 1


if __name__ == "__main__":
    # sys.exit propagates the return code so that the shell/CI can detect failures.
    sys.exit(main())