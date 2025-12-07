import pandas as pd
import numpy as np
import os
# --- NEW IMPORTS ---
print("DEBUG: script start", flush=True)
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
# ------------------------

file_path = os.path.join(os.path.dirname(__file__), '../data/fifa_players.csv') 

# 1. Data Loading
try:
    # Reading the CSV file
    df = pd.read_csv(file_path)
    print("File successfully loaded.")
except FileNotFoundError:
    print(f"ERROR: The file '{file_path}' was not found. Check the name and location.")
    exit()

print("-" * 50)

# 2. Data Preview
print("Preview of the first 5 rows of the dataset (df.head()):")
print(df.head())

print("-" * 50)

# 3. Information about columns and missing values
print("Column information (df.info()):")
# verbose=False and memory_usage="deep" provide a quick and precise overview.
df.info(verbose=False, memory_usage="deep")


# --- Data Preprocessing Step (cleaning improper values from the CSV) ---

# 1. Convert 'national_rating' to numeric
# 'errors='coerce'' replaces any non-numeric values with NaN.
df['national_rating'] = pd.to_numeric(df['national_rating'], errors='coerce') 

# 2. Convert financial columns to float
financial_cols = ['value_euro', 'wage_euro', 'release_clause_euro']
for col in financial_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 3. Imputation (Replace missing values)
# For values/salaries, replace NaN by the median (less sensitive to outliers)
for col in ['value_euro', 'wage_euro']:
    median_val = df[col].median()
    df[col].fillna(median_val, inplace=True)
    
# For release clause and national ratings, replace NaN with 0
# (Indicates absence of clause or no national team selection)
df['release_clause_euro'].fillna(0, inplace=True)
df['national_rating'].fillna(0, inplace=True)

# 4. Verification after cleaning
print("Verification of the first 5 rows after cleaning:")
print(df[['value_euro', 'wage_euro', 'release_clause_euro', 'national_rating']].head(), flush=True)

print("-" * 50)

# --- Feature Engineering Step ---
# One-Hot encoding converts a textual (categorical) column into several binary columns (0 or 1).

# 1. Extract the main position (the first in the list)
df['main_position'] = df['positions'].apply(lambda x: str(x).split(',')[0].strip())

# 2. Apply One-Hot Encoding
df_encoded = pd.get_dummies(df, columns=['main_position'], prefix='pos')

# 3. Select columns for the model
# Target variable (Y) and Feature variables (X)
y = df_encoded['overall_rating']

# Removing irrelevant or identification columns
cols_to_drop = [
    'overall_rating', 'id', 'url', 'name', 'full_name', 'birth_date', 
    'nationality', 'positions', 'preferred_foot', 'body_type', 
    'national_team', 'national_team_position', 'national_jersey_number'
]
X = df_encoded.drop(columns=cols_to_drop, errors='ignore')

# 4. Final NaN handling (replace any remaining NaN with the column mean)
X = X.fillna(X.mean())

print("Model Preparation Completed:")
print(f"  - Features (X) ready: {X.shape[0]} rows, {X.shape[1]} columns.")
print(f"  - Target variable (Y) ready: {y.shape[0]} rows.")

print("-" * 50)


# --- Modeling Step ---

# Task 8.1: Train/Test Split
# test_size=0.2 means 20% of the data will be used for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Train/Test Split:")
print(f"  - Training Set: {X_train.shape[0]} players")
print(f"  - Test Set: {X_test.shape[0]} players")
print("-" * 50)

# Task 8.2: Training and Evaluating the Model (Random Forest Regressor)

# 1. Instantiate the model
model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1) 

# 2. Training 🧠
print("Starting Random Forest model training...")
model.fit(X_train, y_train)
print("Training Completed.")

# 3. Prediction
y_pred = model.predict(X_test)

# 4. Performance Evaluation (Section IV. Evaluation & Analysis)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("-" * 50)
print("Modeling Results (Random Forest Regressor):")
print(f"  - Mean Absolute Error (MAE): {mae:.3f} points")
print(f"  - R-squared (R2 Score): {r2:.4f} (Prediction quality)")
print("-" * 50)