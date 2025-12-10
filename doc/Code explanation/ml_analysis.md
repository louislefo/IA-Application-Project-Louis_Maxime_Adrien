# Comprehensive Explanation of `src/ml_analysis.py`

This document provides a detailed, step-by-step explanation of the `ml_analysis.py` script. It is designed to understand the libraries used, the logic behind the machine learning models, and how data flows through the program.

---

## 1. Imports and Libraries
The script starts by importing necessary tools. Here is the code and what it does:

```python
import os
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score, classification_report
import xgboost as xgb
```

*   **`os`**: Standard library for file paths. It makes sure your code works on Windows, Mac, and Linux without breaking.
*   **`pandas`**: Used for handling the data. It loads the CSV into a "DataFrame" (a table in memory).
*   **`matplotlib`**: Used to draw the scatter plot graph at the end.
*   **`joblib`**: A tool to "save" your AI. Once trained, you save the model to a file so you don't have to retrain it every time you use the app.
*   **`sklearn` (Scikit-Learn)**: The toolkit for standard ML tasks (splitting data, linear models, metrics).
*   **`xgboost`**: A powerful "Machine Learning" library known for looking at tables of data and finding complex patterns. We use it for the rating prediction.

---

## 2. Dynamic Path Setup
This section ensures the script can find the data file no matter where you run it from.

```python
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "fifa_players.csv")
```

**Explanation**: 
Instead of hardcoding `C:/Users/Louis/...`, we use `os.path` to calculate the location relative to the script itself. `PROJECT_ROOT` becomes the parent folder of `src`, allowing us to cleanly navigate to `data/fifa_players.csv`.

---

## 3. The "Future Class" Logic
This custom function defines correct answers for our classification model.

```python
def build_future_label(row):
    overall = row["overall_rating"]
    potential = row["potential"]
    age = row["age"]

    gap = potential - overall  # How much can they improve?

    if gap >= 10 and age <= 23:
        return "high_growth"
    elif gap >= 4:
        return "likely_improve"
    elif gap >= -2:
        return "stable"
    else:
        return "decline"
```

**Explanation**:
Before we can train the AI to predict a player's future, we must define what "future" means using the data we already have.
*   If a player is young (<= 23) and has a huge gap (10+) between current and potential rating, they are labeled **`high_growth`**.
*   If they have decent room to grow (4+), they are **`likely_improve`**.
*   If they are already near their peak, they are **`stable`**.
*   Otherwise, they are in **`decline`**.

---

## 4. Main Execution: Data Cleaning
Now starts the `main()` function.

```python
def main():
    # 1. Load Data
    df = pd.read_csv(DATA_PATH)

    # 2. Select Features (Inputs)
    feature_cols = [
        "age", "height_cm", "weight_kgs","finishing", "dribbling", 
        "short_passing", "acceleration", "sprint_speed", 
        "stamina", "strength"
    ]
    
    # 3. Clean Data (Remove Empty Rows)
    df_clean = df.dropna(subset=feature_cols + ["overall_rating", "potential", "age"])
```

**Description**:
*   The script reads the CSV file.
*   It defines "features" (inputs for the AI) like `dribbling`, `acceleration`, etc.
*   It removes any player (row) that has missing numbers (NaN) in these columns, because AI models cannot handle empty values.

---

## 5. Task 1: Regression (Predicting Exact Rating)
We want to predict the `overall_rating` number (e.g., 82, 65, 90).

```python
    # Prepare Data
    X = df_clean[feature_cols]       # The Input (Skills)
    y = df_clean["overall_rating"]   # The Target (Rating)

    # Split: 70% for Training, 30% for Testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Create and Train Model
    reg_model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5)
    reg_model.fit(X_train, y_train)
```

**Explanation**: 
*   **X (Features)**: The stats the AI gets to see.
*   **y (Target)**: The answer the AI tries to guess.
*   **`train_test_split`**: We hide 30% of the data. The AI learns from the 70% (`train`), and then we test it on the hidden 30% (`test`) to cheat-proof it.
*   **`XGBRegressor`**: This is the "brain". We set it up with 100 "estimators" (decision trees) and tell it to `fit` (learn) the relationship between skills (X) and rating (y).

---

## 6. Evaluating the Regression
We check how well the AI did.

```python
    y_pred = reg_model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"MSE: {mse:.2f}")  # Error margin
    print(f"R² : {r2:.3f}")   # Accuracy score (1.0 is perfect)
```

**Description**:
*   `mse`: How far off the predictions are on average (squared).
*   `r2`: A percentage of "correctness". If R² is 0.95, the model explains 95% of the variation in player ratings.

**Visualization**:
The script also draws a graph:
```python
    plt.scatter(y_test, y_pred, alpha=0.3)
    plt.plot([min, max], [min, max], "r--") # The perfect line
    plt.savefig(out_path_plot)
```
This saves an image where valid predictions cluster around a diagonal red line.

---

## 7. Task 2: Classification (Predicting Career Class)
Now we predict the category: `high_growth`, `stable`, etc.

```python
    # Create the labels first
    df_clean["future_class"] = df_clean.apply(build_future_label, axis=1)

    # Split for Classification
    X_cls = df_clean[feature_cols]
    y_cls = df_clean["future_class"]
    
    # Stratify ensure we have equal % of "high_growth" players in Train and Test
    Xc_train, Xc_test, yc_train, yc_test = train_test_split(..., stratify=y_cls)

    # Train Logistic Regression
    clf = LogisticRegression(max_iter=1000, multi_class="multinomial")
    clf.fit(Xc_train, yc_train)
```

**Explanation**:
*   We use the function from Section 3 to generate the "truth" column.
*   We use **Logistic Regression** (Multinomial). It's great for calculating probabilities (e.g., "70% chance stable, 30% chance decline").

---

## 8. Saving the Models
Finally, we save the trained brains so the main app can use them.

```python
    joblib.dump(reg_model, os.path.join(models_dir, 'regression_model.pkl'))
    joblib.dump(clf, os.path.join(models_dir, 'classification_model.pkl'))
```

**Why?**: Training takes time. By saving the result to a `.pkl` file, the main application can simply "load" the AI in 0.1 seconds and start making predictions immediately.

---

## Summary of Logic Flow
1.  **Imports**: Get tools.
2.  **Load**: Read CSV.
3.  **Clean**: Remove bad rows.
4.  **Train Regression**: Teach XGBoost to predict Rating (Number) from Stats.
5.  **Evaluate**: Check if XGBoost is accurate.
6.  **Train Classification**: Teach Logistic Regression to predict Career Path (Label) from Stats.
7.  **Save**: Store the trained models in the `models/` folder.
