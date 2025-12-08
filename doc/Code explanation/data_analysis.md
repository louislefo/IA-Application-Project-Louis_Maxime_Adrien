# Comprehensive Explanation of `src/data_analysis.py`

This document explains the `data_analysis.py` script. Unlike `ml_analysis.py`, which is built for the final application, this script is an **experimental laboratory**. It uses different techniques (like Random Forest and One-Hot Encoding) to explore the data and test hypothesis.

---

## 1. Imports and Setup
The script imports libraries for data manipulation and a specific machine learning model.

```python
import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
```

*   **`pandas` & `numpy`**: The standard tools for handling data tables and numbers.
*   **`RandomForestRegressor`**: A different AI model than the one in the main app. It uses hundreds of "decision trees" voting together to make a prediction. It is often more accurate but slower than XGBoost.

---

## 2. Data Loading
The script locates and reads the CSV file.

```python
file_path = os.path.join(os.path.dirname(__file__), '../data/fifa_players.csv') 
df = pd.read_csv(file_path)
```

**Note**: It uses `../data` which means "go up one folder, then into data". This assumes the script is running from the `src/` folder.

---

## 3. Advanced Data Cleaning
This script performs more complex cleaning than the main app, specifically for financial data.

### Converting Text to Numbers
The raw data often has messy values. The script forces them to be numbers.

```python
# Convert 'national_rating' and financial columns
df['national_rating'] = pd.to_numeric(df['national_rating'], errors='coerce') 
financial_cols = ['value_euro', 'wage_euro', 'release_clause_euro']
for col in financial_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
```

*   **`errors='coerce'`**: This is important. It tells Python: "If you find a value that isn't a number (like 'N/A' or 'Free'), turn it into `NaN` (Empty) instead of crashing."

### Filling Missing Values (Imputation)
Instead of just deleting empty rows, this script tries to guess the missing values.

```python
# Replace missing salaries with the Median (middle value)
for col in ['value_euro', 'wage_euro']:
    median_val = df[col].median()
    df[col].fillna(median_val, inplace=True)

# Replace missing Release Clause with 0
df['release_clause_euro'].fillna(0, inplace=True)
```

*   **Why Median?**: If one player earns €100M, the *average* salary skews huge. The *median* is safer for money data.
*   **Why 0?**: If a player has no "Release Clause", it usually means they literally don't have one (0), not that the data is lost.

---

## 4. Feature Engineering
This script teaches the AI how to understand text information like "Positions".

```python
# 1. Extract the main position (e.g. "ST, LW" -> "ST")
df['main_position'] = df['positions'].apply(lambda x: str(x).split(',')[0].strip())

# 2. One-Hot Encoding
df_encoded = pd.get_dummies(df, columns=['main_position'], prefix='pos')
```

**"One-Hot Encoding" Explained**:
AI models can't understand words like "Striker" or "Defender". We convert them into numbers:
*   Original: `Position = "ST"`
*   Encoded: `pos_ST = 1`, `pos_CB = 0`, `pos_GK = 0`...

---

## 5. Preparing the "X" and "y"
We define what we want to predict (`y`) and what data we use to predict it (`X`).

```python
y = df_encoded['overall_rating']

# Drop columns that are answers or just labels
cols_to_drop = ['overall_rating', 'name', 'nationality', ...]
X = df_encoded.drop(columns=cols_to_drop)
```

We remove columns like `name` because a player's name doesn't make them play better!

---

## 6. Training the Random Forest
We split the data (80% train, 20% test) and train the model.

```python
# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Create and Train Model
model = RandomForestRegressor(n_estimators=100, n_jobs=-1) 
model.fit(X_train, y_train)
```

*   **`n_estimators=100`**: The AI builds 100 different decision trees.
*   **`n_jobs=-1`**: Uses all CPU cores to train faster.

---

## 7. Evaluation
Finally, we check how effective our complex cleaning and Random Forest were.

```python
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error (MAE): {mae:.3f}")
print(f"R-squared (R2 Score): {r2:.4f}")
```

*   **MAE**: On average, how many rating points is the AI wrong by? (e.g., if real is 85 and pred is 84, error is 1).
*   **R²**: How well does it explain the data (closer to 1.0 is better).

---

## Summary
`data_analysis.py` is where we **experiment** with:
1.  **Smarter Cleaning**: Guessing missing money values instead of deleting them.
2.  **Smarter Features**: Converting text positions into math (One-Hot).
3.  **Different Models**: Using Random Forest to see if it beats XGBoost.

This script helps decide what ultimately goes into the final `ml_analysis.py`.
