# Machine Learning Models

This directory contains the trained models used by the AI Football Performance Analyzer.

##  The 2 Models Explained

### 1. Regression Model (`regression_model.pkl`)
- **Type:** **XGBoost Regressor** (Gradient Boosting)
- **Goal:** Predict a **continuous number**: the **Overall Rating** (0-100).
- **How it works:** 
  - It builds hundreds of decision trees sequentially.
  - Each new tree corrects the errors of the previous ones.
  - It is excellent at capturing complex, non-linear relationships (e.g., "High speed is very valuable, but *only* if you also have good dribbling").
- **Output:** A single floating-point number (e.g., `82.4`).

### 2. Classification Model (`classification_model.pkl`)
- **Type:** **Logistic Regression** (Multinomial)
- **Goal:** Predict a **category**: the **Career Trajectory**.
- **The 4 Classes:**
  1. `high_growth` ✨ (Future Superstar)
  2. `likely_improve` 📈 (Solid Potential)
  3. `stable` ⚖️ (Established/Peak)
  4. `decline` 📉 (Regression)
- **How it works:** 
  - It calculates the weighted sum of inputs mapped to a probability curve (Sigmoid/Softmax).
  - It gives us the **probability** (%) for each class.
- **Output:** One class label (e.g., `high_growth`) + Probabilities (e.g., `85%`).

---

## 📂 What is the `.pkl` extension?

The extension **`.pkl`** stands for **Pickle**.

- **Definition:** It is a binary serialization format specific to Python.
- **Analogy:** Think of it as "freeze-drying" the model.
  1. We train the model (which takes time/computation).
  2. We "pickle" (save) the complex model object into a file.
  3. Later, the application "unpickles" (loads) it instantly, restoring it exactly as it was.
- **Why use it?** 
  - **Speed:** Loading a `.pkl` takes milliseconds, while training might take minutes or hours.
  - **Portability:** You can move the file to another computer and use the model without needing the original training data.

> [!WARNING]
> **Security Note:** Never load a `.pkl` file from an untrusted source, as it can execute arbitrary code during loading. Only load models you or your team have created.
