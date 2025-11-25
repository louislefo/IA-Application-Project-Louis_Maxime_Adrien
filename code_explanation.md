# Summary

**Date de mise à jour :** 25 Novembre 2025

This script loads a football players dataset, trains two machine learning models, and evaluates a player's current performance and expected future development. It uses a linear regression model to predict the player's overall rating and a logistic regression model to classify the player's future growth based on potential, age, and key attributes.

---

# Explanation of `ml_analysis.py`

## Purpose

This script performs three main tasks:

1. Load and clean football player data from a CSV file.
2. Train two machine learning models:
   - A regression model to estimate current performance (`overall_rating`).
   - A classification model to predict a player's future development (`future_class`).
3. Evaluate both models on a sample player and display predictions.

---

## Imports

- pandas: dataset loading and manipulation
- matplotlib: performance visualization
- scikit-learn: machine learning models and evaluation tools
- os: path handling to access the data file

---

## Data Loading

- Builds a clean relative path to `data/football_players.csv`.
- Loads the dataset with `pd.read_csv()`.
- Displays basic dataset information (`df.head()`, `df.info()`).

---

## Feature Selection and Cleaning

### Targets

- `overall_rating`: regression target (current performance)
- `future_class`: classification target (future progression)

### Input Features

- `age`, `height_cm`, `weight_kgs`
- `finishing`, `dribbling`, `short_passing`
- `acceleration`, `sprint_speed`, `stamina`, `strength`

### Cleaning

- Removes rows containing missing values in essential columns.

---

## Model 1: Regression (Current Performance)

- Inputs: selected player attributes
- Target: `overall_rating`
- Model: `LinearRegression()`
- Train/test split (80/20)
- Metrics:
  - Mean Squared Error (MSE)
  - R² Score

Outputs:

- Regression model coefficients
- Scatter plot comparing real vs predicted ratings (`reg_true_vs_pred.png`)

---

## Creating the `future_class` Label

Rule-based classification using:

- Gap between potential and overall (`gap = potential - overall_rating`)
- Player age

Classes:

- `high_growth`: gap ≥ 10 and age ≤ 23
- `likely_improve`: gap ≥ 4
- `stable`: -2 ≤ gap < 4
- `decline`: otherwise

---

## Model 2: Classification (Future Development)

- Inputs: same features as regression
- Target: `future_class`
- Model: `LogisticRegression(multi_class="multinomial")`
- Stratified train/test split
- Evaluation using `classification_report` (precision, recall, F1-score)

---

## Example Player Evaluation

The script generates a sample player and computes:

- Predicted overall rating
- Predicted future class
- Probability distribution across all future classes

---

## Final Output

The script provides:

- A regression-based evaluation of a player's current performance
- A classification-based prediction of future development
- A saved visualization of prediction accuracy
- A clear example demonstrating practical player analysis using the models

---

# Explanation of `data_analysis.py`

## Purpose

This script is a simple utility to verify data accessibility and structure.

## Steps

1.  **Load Data**: Attempts to read `fifa_players.csv` (note: the script currently expects the file in the same directory or needs the path updated to `data/fifa_players.csv`).
2.  **Preview**: Prints the first 5 rows (`df.head()`).
3.  **Info**: Prints column information and memory usage (`df.info()`).

---

# Explanation of `ml_analysis.ipynb`

## Purpose

# Summary

**Date de mise à jour :** 25 Novembre 2025

This script loads a football players dataset, trains two machine learning models, and evaluates a player's current performance and expected future development. It uses a linear regression model to predict the player's overall rating and a logistic regression model to classify the player's future growth based on potential, age, and key attributes.

---

# Explanation of `ml_analysis.py`

## Purpose

This script performs three main tasks:

1. Load and clean football player data from a CSV file.
2. Train two machine learning models:
   - A regression model to estimate current performance (`overall_rating`).
   - A classification model to predict a player's future development (`future_class`).
3. Evaluate both models on a sample player and display predictions.

---

## Imports

- pandas: dataset loading and manipulation
- matplotlib: performance visualization
- scikit-learn: machine learning models and evaluation tools
- os: path handling to access the data file

---

## Data Loading

- Builds a clean relative path to `data/football_players.csv`.
- Loads the dataset with `pd.read_csv()`.
- Displays basic dataset information (`df.head()`, `df.info()`).

---

## Feature Selection and Cleaning

### Targets

- `overall_rating`: regression target (current performance)
- `future_class`: classification target (future progression)

### Input Features

- `age`, `height_cm`, `weight_kgs`
- `finishing`, `dribbling`, `short_passing`
- `acceleration`, `sprint_speed`, `stamina`, `strength`

### Cleaning

- Removes rows containing missing values in essential columns.

---

## Model 1: Regression (Current Performance)

- Inputs: selected player attributes
- Target: `overall_rating`
- Model: `LinearRegression()`
- Train/test split (80/20)
- Metrics:
  - Mean Squared Error (MSE)
  - R² Score

Outputs:

- Regression model coefficients
- Scatter plot comparing real vs predicted ratings (`reg_true_vs_pred.png`)

---

## Creating the `future_class` Label

Rule-based classification using:

- Gap between potential and overall (`gap = potential - overall_rating`)
- Player age

Classes:

- `high_growth`: gap ≥ 10 and age ≤ 23
- `likely_improve`: gap ≥ 4
- `stable`: -2 ≤ gap < 4
- `decline`: otherwise

---

## Model 2: Classification (Future Development)

- Inputs: same features as regression
- Target: `future_class`
- Model: `LogisticRegression(multi_class="multinomial")`
- Stratified train/test split
- Evaluation using `classification_report` (precision, recall, F1-score)

---

## Example Player Evaluation

The script generates a sample player and computes:

- Predicted overall rating
- Predicted future class
- Probability distribution across all future classes

---

## Final Output

The script provides:

- A regression-based evaluation of a player's current performance
- A classification-based prediction of future development
- A saved visualization of prediction accuracy
- A clear example demonstrating practical player analysis using the models

---

# Explanation of `data_analysis.py`

## Purpose

This script is a simple utility to verify data accessibility and structure.

## Steps

1.  **Load Data**: Attempts to read `fifa_players.csv` (note: the script currently expects the file in the same directory or needs the path updated to `data/fifa_players.csv`).
2.  **Preview**: Prints the first 5 rows (`df.head()`).
3.  **Info**: Prints column information and memory usage (`df.info()`).

---

# Explanation of `ml_analysis.ipynb`

## Purpose

This Jupyter Notebook is an interactive version of `ml_analysis.py`. It allows for step-by-step execution and immediate visualization of results.

## Key Differences from the Script

- **Interactive**: Code is split into cells for better flow.
- **Language**: Comments and markdown explanations are in **English**.
- **Visualization**: Plots (like the regression scatter plot) are displayed directly in the notebook output.

---

# Explanation of `analyse.ipynb`

## Purpose

This notebook performs an in-depth Exploratory Data Analysis (EDA) of the football players dataset.

## Key Features

- **Data Loading & Overview**: Checks data structure, types, and missing values.
- **Descriptive Statistics**: Summarizes numerical features.
- **Advanced Visualizations (Seaborn)**:
  - **Distributions**: Histograms for Age, Overall Rating, and Potential.
  - **Correlations**: Heatmap showing top features correlated with Overall Rating.
  - **Trends**: Line plot of Age vs. Overall Rating.
  - **Value Analysis**: Scatter plot of Rating vs. Market Value.
  - **Demographics**: Bar chart of top nationalities.
