# src/ml_player_analysis.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score, classification_report
import xgboost as xgb


# ---------- Clean relative paths ----------

# Determine the base directory of the project dynamically.
# This ensures the script works even if run from different working directories.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Path to the CSV file containing FIFA player data
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "fifa_players.csv")


def build_future_label(row):
    """
    Creates a 'future_class' label based on the difference between potential and overall rating,
    while also considering age.

    Logic:
    - Young players (≤ 23) with large potential jump (≥ 10) are considered "high growth".
    - Decent potential improvement (≥ 4) becomes "likely_improve".
    - Small difference (≥ -2) is considered "stable".
    - Negative progression suggests "decline".

    This classification helps predict a career trajectory rather than a numeric value.
    """
    overall = row["overall_rating"]
    potential = row["potential"]
    age = row["age"]

    gap = potential - overall  # Improvement margin

    if gap >= 10 and age <= 23:
        return "high_growth"
    elif gap >= 4:
        return "likely_improve"
    elif gap >= -2:
        return "stable"
    else:
        return "decline"


def main():
    # 1) Load dataset
    print(f"Loading data from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)

    # Show first rows to validate structure
    print("=== Data preview ===")
    print(df.head(), "\n")

    # Show column types, non-null counts, memory usage, etc.
    print("=== Column info ===")
    print(df.info(), "\n")

    # Define target columns and feature list
    target_overall = "overall_rating"
    target_potential = "potential"
    col_age = "age"

    # Selected technical and physical attributes used as predictors
    # These features are numerical and suitable for ML models.
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

    # Ensure all required columns exist in the dataset
    for c in feature_cols + [target_overall, target_potential, col_age]:
        if c not in df.columns:
            raise ValueError(f"Column '{c}' was not found in the CSV.")

    # Remove rows containing missing values in essential columns
    df_clean = df.dropna(subset=feature_cols + [target_overall, target_potential, col_age])

    print(f"\nNumber of players after cleaning: {len(df_clean)}")

    # 3) REGRESSION MODEL — predicting overall rating
    # Extract features and labels
    X = df_clean[feature_cols]
    y = df_clean[target_overall]

    # Split the dataset into train and test sets
    # test_size=0.3 → 30% of data for evaluation
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # XGBoost is chosen because it handles nonlinear relationships
    # and typically gives superior performance compared to linear models.
    reg_model = xgb.XGBRegressor(
        n_estimators=100,        # Number of trees
        learning_rate=0.1,       # Step size shrinkage
        max_depth=5,             # Controls tree complexity
        random_state=42          # Reproducibility
    )
    reg_model.fit(X_train, y_train)

    # Predict overall ratings for the test set
    y_pred = reg_model.predict(X_test)

    # Evaluate model performance
    mse = mean_squared_error(y_test, y_pred)  # Measures prediction error
    r2 = r2_score(y_test, y_pred)             # Measures explained variance

    print("\n=== XGBoost Regression Model (overall_rating) ===")
    print(f"MSE: {mse:.2f}")
    print(f"R² : {r2:.3f}")

    # Display feature importance sorted from highest to lowest
    print("\nFeature importance (prediction impact):")
    feature_importance = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': reg_model.feature_importances_
    }).sort_values('Importance', ascending=False)
    print(feature_importance.to_string(index=False))

    # Scatter plot to compare true ratings vs predicted ones
    plt.figure()
    plt.scatter(y_test, y_pred, alpha=0.3)
    plt.xlabel("True scores (overall_rating)")
    plt.ylabel("Predicted scores")
    plt.title("Regression: true vs predicted (overall_rating)")

    # Diagonal line for perfect predictions
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], "r--")

    plt.tight_layout()
    
    # Ensure output image directory exists
    ml_images_dir = os.path.join(PROJECT_ROOT, "Images", "ml")
    os.makedirs(ml_images_dir, exist_ok=True)
    
    # Save the regression plot
    out_path_plot = os.path.join(ml_images_dir, "reg_true_vs_pred.png")
    plt.savefig(out_path_plot)
    print(f"Plot 'reg_true_vs_pred.png' saved in: {out_path_plot}")

    # 4) CLASSIFICATION — predicting future class
    df_clean["future_class"] = df_clean.apply(build_future_label, axis=1)

    print("\nFuture class distribution:")
    print(df_clean["future_class"].value_counts(), "\n")

    # Features and labels for the classification model
    X_cls = df_clean[feature_cols]
    y_cls = df_clean["future_class"]

    # stratify=y_cls ensures all classes are represented proportionally
    Xc_train, Xc_test, yc_train, yc_test = train_test_split(
        X_cls, y_cls, test_size=0.2, random_state=42, stratify=y_cls
    )

    # Multinomial logistic regression → handles multi-class classification
    clf = LogisticRegression(
        max_iter=1000,            # Increase iterations to ensure convergence
        multi_class="multinomial" # Enables softmax classification
    )
    clf.fit(Xc_train, yc_train)

    yc_pred = clf.predict(Xc_test)

    print("=== Classification Model (future_class) ===")
    print(classification_report(yc_test, yc_pred))

    # 5) Example prediction using a manually created player profile
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

    # Predict regression and classification outputs
    overall_pred_example = reg_model.predict(example_df[feature_cols])[0]
    future_class_example = clf.predict(example_df[feature_cols])[0]
    future_proba_example = clf.predict_proba(example_df[feature_cols])[0]
    classes = clf.classes_

    print("\n=== Example Player Analysis ===")
    print("Player data:")
    for k, v in example_player.items():
        print(f"  {k:15s} = {v}")

    print(f"\nPredicted overall rating     : {overall_pred_example:.1f}")
    print(f"Predicted future class       : {future_class_example}")
    print("Class probabilities:")

    # Print probability distribution across all possible classes
    for cls, proba in zip(classes, future_proba_example):
        print(f"  {cls:15s} -> {proba:.3f}")

    # Create output directory for models if needed
    models_dir = os.path.join(PROJECT_ROOT, 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    # Save trained models for later use
    joblib.dump(reg_model, os.path.join(models_dir, 'regression_model.pkl'))
    joblib.dump(clf, os.path.join(models_dir, 'classification_model.pkl'))
    print("Models saved!")


if __name__ == "__main__":
    main()