# ⚡ Cheat Sheet - AI Football Performance Analyzer

## 🚀 Quick Launch

```bash
# Standard Launch
streamlit run src/application.py

# First Time Setup
cd src
python ml_analysis.py
cd ..
streamlit run src/application.py
```

---

## 📋 Filling the Form

### General Information
| Field | Min | Max | Tip |
|-------|-----|-----|-----|
| **Name** | - | - | Required! |
| **Age** | 15 | 40 | Performance Peak: 27-31 |
| **Height (cm)** | 150 | 210 | Typical: 175-185 |
| **Weight (kg)** | 50 | 100 | Depending on height |

### Technical Attributes (0-100)
| Attribute | Poor | Average | Good | Excellent |
|-----------|------|---------|------|-----------|
| **Finishing** | <50 | 50-70 | 70-85 | >85 |
| **Dribbling** | <50 | 50-70 | 70-85 | >85 |
| **Short Pass** | <50 | 50-70 | 70-85 | >85 |
| **Acceleration** | <50 | 50-70 | 70-85 | >85 |
| **Sprint Speed** | <50 | 50-70 | 70-85 | >85 |
| **Stamina** | <50 | 50-70 | 70-85 | >85 |
| **Strength** | <50 | 50-70 | 70-85 | >85 |

---

## 📊 Interpreting Results

### Overall Rating
```
✅ 80-100  🟢 Excellent (World Class Striker)
✅ 65-79   🟡 Good (Solid Player)
⚠️  50-64   🔴 Average (Development Needed)
❌ <50     ⚫ Poor (Ignore)
```

### Career Prediction

| Class | Emoji | Meaning | Action |
|-------|-------|---------|--------|
| **high_growth** | ✨ | Future superstar | RECRUIT! |
| **likely_improve** | 📈 | Good progression | Interesting |
| **stable** | ⚖️ | No change | Short term |
| **decline** | 📉 | Declining | Monitor |

### Probabilities
- **> 80%:** Model Confident ✅
- **60-80%:** Model Fairly Confident ⚠️
- **<60%:** Model Uncertain ❓

---

## 💡 Tip: Classic Profiles

### Young Talent
```
Name: Vinícius Jr
Age: 20
Height: 180 cm
Weight: 73 kg
Finishing: 75 | Dribbling: 90 | Short Pass: 75
Acceleration: 90 | Sprint Speed: 92 | Stamina: 85 | Strength: 70
→ Rating: 78-80 🟡
→ Class: high_growth ✨
```

### Elite Striker
```
Name: Mbappé
Age: 24
Height: 178 cm
Weight: 73 kg
Finishing: 92 | Dribbling: 88 | Short Pass: 82
Acceleration: 96 | Sprint Speed: 96 | Stamina: 90 | Strength: 78
→ Rating: 89-91 🟢
→ Class: high_growth ✨
```

### Solid Defender
```
Name: Van Dijk
Age: 32
Height: 188 cm
Weight: 82 kg
Finishing: 40 | Dribbling: 60 | Short Pass: 90
Acceleration: 78 | Sprint Speed: 77 | Stamina: 88 | Strength: 95
→ Rating: 84-86 🟢
→ Class: stable ⚖️
```

### Aging Player
```
Name: Cristiano Jr
Age: 37
Height: 187 cm
Weight: 84 kg
Finishing: 85 | Dribbling: 78 | Short Pass: 80
Acceleration: 75 | Sprint Speed: 75 | Stamina: 78 | Strength: 80
→ Rating: 84-85 🟢
→ Class: decline 📉
```

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **Ctrl+R** | Reload App |
| **F11** | Full Screen Mode |
| **Ctrl+S** | Save (Manual) |

---

## 🔄 Typical Workflow

```
1. Open App (streamlit run...)
   ↓
2. Enter Player Data
   ↓
3. Click "🔍 Analyze"
   ↓
4. Check Rating & Prediction
   ↓
5. Click "💾 Add" to Save
   ↓
6. Compare in Database
```

**Time per player: ~2 minutes** ⏱️

---

## 🛠️ Quick Troubleshooting

| Issue | Command | Time |
|-------|---------|------|
| App didn't open | `streamlit run src/application.py` | 10s |
| Port Busy | `streamlit run ... --server.port 8502` | 5s |
| Missing Models | `cd src && python ml_analysis.py` | 2-3 min |
| Missing Module | `pip install -r requirements.txt` | 2-3 min |

---

## 📊 Useful Formulas

### Estimated Rating (Approx)
```
Rating ≈ 30 + (short_pass × 0.40) + (age × 0.45) 
         + (dribbling × 0.10) + (others × 0.05)
```

### Future Class (Approx)
```
gap = potential - overall_rating

if gap ≥ 10 and age ≤ 23:
    class = "high_growth"
elif gap ≥ 4:
    class = "likely_improve"
elif gap ≥ -2:
    class = "stable"
else:
    class = "decline"
```

---

## 🎯 Realistic Goals

### Realistic Goals by Age
| Age | Expected Rating | Probable Class |
|-----|-----------------|----------------|
| 17-20 | 60-75 | high_growth |
| 21-25 | 70-82 | likely_improve |
| 26-30 | 75-88 | stable |
| 31-35 | 70-85 | stable/decline |
| 35+ | 60-80 | decline |

---

## 📈 KPIs to Track

```
Database:
├── Total Players: _____
├── Average Rating: _____
├── Average Age: _____
└── Superstars: _____

Top 3 Key Attributes:
1. Short Passing (43.7%)
2. Age (21.9%)
3. Dribbling (9.8%)
```

---

## 🔐 Important Notes

⚠️ **ATTENTION:**
- Data is saved in a local CSV
- No cloud synchronization
- Backup `data/history.csv` regularly!

✅ **GOOD TO KNOW:**
- Model caches (1st run = slow)
- You can add as many players as you want
- Probabilities are calibrated (reliable)
- Short Passing is the KEY attribute

---

## 📱 Power User Commands

```bash
# View detailed logs
streamlit run src/application.py --logger.level=debug

# Change port
streamlit run src/application.py --server.port 9000

# Dev mode
streamlit run src/application.py --logger.level=debug --client.showErrorDetails=true

# Clean models (retrain)
rm models/*.pkl
cd src && python ml_analysis.py
```

---

## 🎓 Quick Learning

### In 5 minutes
- Open App
- Analyze 1 Player
- Understand Results

### In 30 minutes
- Add 10 Players
- Consult Database
- Identify Patterns

### In 2 hours
- Read Documentation
- Understand Models
- Explore Code

### In 1 day
- Master Application
- Can Teach It
- Adapt to Needs

---

## 🏃 Quick Reference

```
App: http://localhost:8501
Data: data/history.csv
Models: models/*.pkl
Logs: Streamlit console
```

---

## 💾 Data Backup

```bash
# Backup your database
cp data/history.csv backups/history_$(date +%Y%m%d).csv

# Restore backup
cp backups/history_20231204.csv data/history.csv
```

---

## 🎯 Daily Checklist

- [ ] App open? (streamlit run...)
- [ ] Data ready? (CSV file)
- [ ] Models loaded? (check status)
- [ ] Reliable predictions? (probas > 60%)
- [ ] Players saved? (database up to date)

---

**Print this page or bookmark it! 📌**

Version: 1.0 | Last Update: December 8, 2025
