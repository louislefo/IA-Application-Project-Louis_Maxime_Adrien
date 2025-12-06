# src/ml_player_analysis.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score, classification_report
import xgboost as xgb


# ---------- Chemins relatifs propres ----------

# Déterminer le répertoire de base du projet
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "fifa_players.csv")


def build_future_label(row):
    """
    Crée une étiquette 'future_class' à partir de potential - overall_rating + âge.
    """
    overall = row["overall_rating"]
    potential = row["potential"]
    age = row["age"]

    gap = potential - overall

    if gap >= 10 and age <= 23:
        return "high_growth"
    elif gap >= 4:
        return "likely_improve"
    elif gap >= -2:
        return "stable"
    else:
        return "decline"


def main():
    # 1) Charger les données
    print(f"Chargement des données depuis : {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)

    print("=== Aperçu des données ===")
    print(df.head(), "\n")

    print("=== Infos colonnes ===")
    print(df.info(), "\n")

    # 2) Choix des features et des cibles
    target_overall = "overall_rating"
    target_potential = "potential"
    col_age = "age"

    feature_cols = [
        "age",
        "height_cm",
        "weight_kgs",
        "finishing",
        "dribbling",
        "short_passing",
        "acceleration",
        "sprint_speed",
        "stamina",
        "strength",
    ]

    # Vérifier que tout existe
    for c in feature_cols + [target_overall, target_potential, col_age]:
        if c not in df.columns:
            raise ValueError(f"La colonne '{c}' est introuvable dans le CSV.")

    # Retirer les lignes avec des NaN dans ce qu'on utilise
    df_clean = df.dropna(subset=feature_cols + [target_overall, target_potential, col_age])

    print(f"\nNombre de joueurs après nettoyage : {len(df_clean)}")

    # 3) Modèle de RÉGRESSION : prédire overall_rating
    X = df_clean[feature_cols]
    y = df_clean[target_overall]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # XGBoost Regressor - MEILLEUR MODÈLE
    # XGBoost surpasse Linear Regression en capturant les relations non-linéaires
    # et en fournissant une meilleure précision (R² plus élevé, RMSE plus faible)
    reg_model = xgb.XGBRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )
    reg_model.fit(X_train, y_train)

    y_pred = reg_model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("\n=== Modèle de régression XGBoost (overall_rating) ===")
    print(f"MSE : {mse:.2f}")
    print(f"R²  : {r2:.3f}")

    print("\nImportance des features (impact sur la prédiction) :")
    feature_importance = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': reg_model.feature_importances_
    }).sort_values('Importance', ascending=False)
    print(feature_importance.to_string(index=False))

    # Graphique vrai vs prédit
    plt.figure()
    plt.scatter(y_test, y_pred, alpha=0.3)
    plt.xlabel("Vraies notes (overall_rating)")
    plt.ylabel("Notes prédites")
    plt.title("Régression : vrai vs prédit (overall_rating)")

    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], "r--")  # diagonale parfaite

    plt.tight_layout()
    
    # Créer le dossier pour les images ML si nécessaire
    ml_images_dir = os.path.join(PROJECT_ROOT, "Images", "ml")
    os.makedirs(ml_images_dir, exist_ok=True)
    
    out_path_plot = os.path.join(ml_images_dir, "reg_true_vs_pred.png")
    plt.savefig(out_path_plot)
    print(f"Graphique 'reg_true_vs_pred.png' sauvegardé dans : {out_path_plot}")

    # 4) Modèle de CLASSIFICATION : prédire future_class
    df_clean["future_class"] = df_clean.apply(build_future_label, axis=1)

    print("\nRépartition des classes futures :")
    print(df_clean["future_class"].value_counts(), "\n")

    X_cls = df_clean[feature_cols]
    y_cls = df_clean["future_class"]

    Xc_train, Xc_test, yc_train, yc_test = train_test_split(
        X_cls, y_cls, test_size=0.2, random_state=42, stratify=y_cls
    )

    clf = LogisticRegression(
        max_iter=1000,
        multi_class="multinomial"
    )
    clf.fit(Xc_train, yc_train)

    yc_pred = clf.predict(Xc_test)

    print("=== Modèle de classification (future_class) ===")
    print(classification_report(yc_test, yc_pred))

    # 5) Exemple : analyse d'un joueur artificiel
    example_player = {
        "age": 20,
        "height_cm": 175.0,
        "weight_kgs": 70.0,
        "finishing": 78,
        "dribbling": 85,
        "short_passing": 82,
        "acceleration": 88,
        "sprint_speed": 90,
        "stamina": 80,
        "strength": 65,
    }

    example_df = pd.DataFrame([example_player])

    overall_pred_example = reg_model.predict(example_df[feature_cols])[0]
    future_class_example = clf.predict(example_df[feature_cols])[0]
    future_proba_example = clf.predict_proba(example_df[feature_cols])[0]
    classes = clf.classes_

    print("\n=== Analyse d'un joueur d'exemple ===")
    print("Données du joueur :")
    for k, v in example_player.items():
        print(f"  {k:15s} = {v}")

    print(f"\nNote globale prédite           : {overall_pred_example:.1f}")
    print(f"Classe future prédite          : {future_class_example}")
    print("Probabilités par classe :")
    for cls, proba in zip(classes, future_proba_example):
        print(f"  {cls:15s} -> {proba:.3f}")

    # Sauvegarder le modèle de régression (note actuelle)
    models_dir = os.path.join(PROJECT_ROOT, 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    joblib.dump(reg_model, os.path.join(models_dir, 'regression_model.pkl'))
        
    # Sauvegarder le modèle de classification (futur)
    joblib.dump(clf, os.path.join(models_dir, 'classification_model.pkl'))
    print("Modèles sauvegardés !")


if __name__ == "__main__":
    main()
