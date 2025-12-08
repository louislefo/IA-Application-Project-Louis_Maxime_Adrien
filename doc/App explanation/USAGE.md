# 🚀 Usage Guide - AI Football Performance Analyzer

## Quick Start

### 1️⃣ Train the Models
Before launching the application, you must first train the XGBoost models:

```bash
cd src
python ml_analysis.py
```

This will:
- Load and clean the FIFA data
- Train the **XGBoost Regressor** (predict overall rating)
- Train the **Logistic Regression Classifier** (predict career trajectory)
- Save the models in `models/regression_model.pkl` and `models/classification_model.pkl`

### 2️⃣ Launch the Web Application
Once the models are trained, launch the Streamlit application:

```bash
streamlit run src/application.py
```

The application will automatically open in your browser at `http://localhost:8501`.

---

## 📱 Application Usage Guide

### 🎮 Main Interface

The application consists of two main sections:

#### **Sidebar - Input Form**

Complete all fields to evaluate a player:

1. **General Information**
   - 🎫 **Player Name**: Enter the name of the player to analyze
   - 🎂 **Age**: Between 15 and 40 years (slider)
   - 📏 **Height**: Between 150 cm and 210 cm
   - ⚖️ **Weight**: Between 50 kg and 100 kg

2. **Technical & Physical Attributes**
   - 🎯 **Finishing**: Ability to score goals (0-100)
   - 🎮 **Dribbling**: Ball control and trickery (0-100)
   - 📤 **Short Passing**: Accuracy of short passes (0-100)
   - 💨 **Acceleration**: Quick burst of speed (0-100)
   - 🏃 **Sprint Speed**: Top linear speed (0-100)
   - ⚡ **Stamina**: Match endurance (0-100)
   - 💪 **Strength**: Physical power (0-100)

#### **Main Area - Results Display**

After clicking **"🔍 Analyze Player"**:

1. **Player Profile Table**
   - Displays all entered attributes

2. **Visualization Chart**
   - Bar chart showing all attributes
   - Helps visually identify strong and weak points

3. **Analysis Results**
   - **📈 Estimated Overall Rating**: The score predicted by XGBoost (0-100)
   - **⚡ Strongest Attribute**: The player's highest attribute
   - **📊 Attribute to Improve**: The attribute with the lowest score

4. **🔮 Career Trajectory Prediction**

   The model classifies players into 4 categories:

   - **✨ FUTURE SUPERSTAR** (High Growth)
     - Young player with enormous potential
     - Significant expected progress
     - A must-recruit/develop

   - **📈 SOLID POTENTIAL** (Likely Improve)
     - Player can improve significantly
     - Good career trajectory
     - Interesting investment

   - **⚖️ STABLE PLAYER** (Stable)
     - Player reached their peak/cruising level
     - No major expected progression
     - Reliable for short term

   - **📉 DECLINING** (Decline)
     - Aging or stagnating player
     - Future performance may decrease
     - Monitor closely

5. **Class Probabilities**
   - Displays the percentage probability for each category

### 💾 Add to Database

Once the analysis is done, click **"💾 Add to Database"** to:
- Save the player to `data/history.csv`
- Include the predicted rating and career category
- Record the date/time of addition

### 📚 Player Database

The bottom section displays:
- **Full list** of all added players
- **Global statistics**:
  - Total players added
  - Average player rating
  - Average age
  - Number of future superstars

---

## 🔧 Technical Details

### Models Used

#### **XGBoost Regressor** (Overall Rating)
- **Performance**: R² > 0.85 (very good)
- **Advantages**:
  - Captures non-linear relationships
  - Better accuracy than Linear Regression
  - Robust to real-world data
  - Integrated feature importance

#### **Logistic Regression Classifier** (Trajectory)
- **Classes**: 4 career categories
- **Advantages**:
  - Well-calibrated probabilities
  - High interpretability
  - Fast and reliable

### File Structure

```
project/
├── src/
│   ├── application.py          # Main Streamlit Application
│   ├── ml_analysis.py          # Training Script
│   ├── ml_analysis.ipynb       # Analysis Notebook
│   └── ml_advanced_models.ipynb # Advanced Notebook
├── data/
│   ├── fifa_players.csv        # Original Data
│   └── history.csv             # Added Players (via App)
├── models/
│   ├── regression_model.pkl    # XGBoost Model
│   └── classification_model.pkl# Logistic Regression Model
└── requirements.txt            # Python Dependencies
```

---

## 🐛 Troubleshooting

### Error: "Models not found"
**Solution**: First run `python ml_analysis.py` in the `src/` folder to train the models.

### Error: "Module streamlit not found"
**Solution**: Install dependencies: `pip install -r requirements.txt`

### Slow Application
**Solution**: Models are cached. The first run is normal to be slower, subsequent runs will be fast.

---

## 📊 Usage Examples

### Example 1: Young Talent
```
Name: Vinicius Jr
Age: 20
Height: 180 cm
Weight: 73 kg
Attributes: Dribbling 88, Speed 90, Stamina 82
→ Predicted Rating: ~78-80
→ Class: HIGH_GROWTH ✨
```

### Example 2: Established Player
```
Name: Benzema
Age: 35
Height: 185 cm
Weight: 80 kg
Attributes: Finishing 92, Short Pass 88, Stamina 75
→ Predicted Rating: ~83-85
→ Class: STABLE ⚖️
```

---

## 💡 Usage Tips

1. **Enter realistic data**: Attributes should be consistent with each other.
2. **Use visual tools**: The bar chart helps identify inconsistencies.
3. **Check probabilities**: They show the model's confidence.
4. **Compare players**: Add multiple players to compare them in the database.

---

## 📞 Support

For any questions or bugs, refer to the main project README.

Happy Scouting! ⚽🚀
