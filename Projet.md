

Notebook summary (src/analyse.ipynb):
- Loads the football players CSV (expects it in `data/`, see `file_path` in code).
- Displays a 5-row sample with columns like name/full_name, positions, ratings, physical metrics, and technical stats.
- Prints dataframe info: ~17.9k rows, 51 columns (mix of object, float, int), highlights missing values in monetary/national team fields.
- Outputs descriptive statistics for numeric columns (age, height/weight, ratings, wages/value, skill attributes).
- Purpose: quick EDA checkpoint to inspect schema, completeness, and value ranges before feature engineering and modeling.

![alt text](image.png)
