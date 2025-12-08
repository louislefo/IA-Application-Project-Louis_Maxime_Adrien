# 🚀 Application Quick Start

## ✅ Startup Checklist

### Step 1: Verify Installation
```bash
python test_setup.py
```

This will verify:
- ✅ Data files
- ✅ XGBoost models
- ✅ Python dependencies
- ✅ That everything is working

### Step 2: Install Dependencies (if necessary)
```bash
pip install -r requirements.txt
```

### Step 3: Train Models (first time only)
```bash
cd src
python ml_analysis.py
```

**Expected Output:**
```
Number of players after cleaning: XXXX

=== XGBoost Regression Model (overall_rating) ===
MSE : XXX.XX
R²  : 0.XXX

Feature Importance:
         Feature  Importance
0  sprint_speed    0.XXXX
1  acceleration    0.XXXX
...

=== Classification Model (future_class) ===
              precision    recall  f1-score   support

    high_growth       0.XX      0.XX      0.XX       XXX
   likely_improve     0.XX      0.XX      0.XX       XXX
         stable       0.XX      0.XX      0.XX       XXX
         decline       0.XX      0.XX      0.XX       XXX

Models saved!
```

### Step 4: Launch Application
```bash
streamlit run src/application.py
```

**Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://XXX.XXX.XXX.XXX:8501
```

The application will automatically open in your browser! 🎉

---

## 📋 Basic Usage

1. **Enter player data** in the sidebar form
2. **Click "🔍 Analyze Player"**
3. **View results**:
   - Estimated Overall Rating
   - Predicted Career Trajectory
   - Key Attributes
4. **Click "💾 Add to Database"** to save

---

## 🎯 Use Cases

### Case 1: Evaluate an Existing Player
```
1. Find player stats (e.g., Transfermarkt, FIFA)
2. Enter data into the app
3. Check the XGBoost rating and career prediction
4. Compare with other players in the database
```

### Case 2: Create a Fictional Profile
```
1. Imagine stats (young talent, developed player, etc.)
2. Enter data
3. Verify if the prediction makes sense
4. Save for future comparison
```

### Case 3: Analyze a Cohort
```
1. Add multiple players to the database
2. Check global statistics at the bottom
3. Identify patterns (average age, best rating, etc.)
```

---

## 🔧 Useful Commands

### Restart Application
```bash
streamlit run src/application.py --logger.level=debug
```

### Clear Local Database
```bash
rm data/history.csv
# The application will create a new one on next save
```

### Verify Trained Models
```bash
cd src
python -c "import joblib; reg = joblib.load('../models/regression_model.pkl'); print('XGBoost Model OK ✅')"
```

---

## ⚠️ Common Issues

### "Module streamlit not found"
```bash
pip install streamlit --upgrade
```

### "Port 8501 already in use"
```bash
# Use a different port
streamlit run src/application.py --server.port 8502
```

### "Models not found"
- Ensure `models/` exists
- Run `python src/ml_analysis.py` to create models
- Verify that `.pkl` files exist

### App slow on first start
This is normal! Models are being loaded and cached. It won't happen again.

---

## 📊 Data Structure

### Input (Form)
```
Name: string
Age: 15-40
Height: 150-210 cm
Weight: 50-100 kg
Finishing, Dribbling, Short Passing, Acceleration, Sprint Speed, Stamina, Strength: 0-100
```

### Output (Predictions)
```
Overall Rating: 0-100 (float)
Class: "high_growth" | "likely_improve" | "stable" | "decline"
Probabilities: [0.0-1.0] for each class
```

### Database (history.csv)
```
player_name, age, height_cm, weight_kgs, finishing, dribbling, short_passing,
acceleration, sprint_speed, stamina, strength, predicted_overall_rating,
predicted_future_class, date_added
```

---

## 🎓 For More Info

- Consult `USAGE.md` for the full guide
- Consult `README.md` for methodology
- Examine `src/ml_analysis.py` for training code
- Examine `src/ml_analysis.ipynb` for detailed analysis

---

**Happy Scouting! ⚽🚀**
