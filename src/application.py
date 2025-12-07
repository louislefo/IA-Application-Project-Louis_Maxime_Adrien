import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
import xgboost as xgb
import csv

# 1. Page configuration
st.set_page_config(page_title="AI Football Scout", layout="wide", initial_sidebar_state="expanded")
st.title("⚽ AI Football Performance Analyzer")
st.markdown("### Player Performance Analysis & Prediction with XGBoost")

# Define the project root path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. Load models (cached for speed)
@st.cache_resource
def load_models():
    try:
        models_dir = os.path.join(PROJECT_ROOT, 'models')
        reg_model = joblib.load(os.path.join(models_dir, 'regression_model.pkl'))
        clf_model = joblib.load(os.path.join(models_dir, 'classification_model.pkl'))
        return reg_model, clf_model
    except FileNotFoundError:
        return None, None

reg_model, clf_model = load_models()

if reg_model is None or clf_model is None:
    st.error("❌ Models not found! Please run training with 'ml_analysis.py' first")
    st.stop()

# Define paths
# PROJECT_ROOT is already defined above
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "fifa_players.csv")
PLAYERS_DB_PATH = os.path.join(PROJECT_ROOT, "data", "history.csv")

# Create directory if needed
os.makedirs(os.path.dirname(PLAYERS_DB_PATH), exist_ok=True)

# 3. Function to load the added players database
# @st.cache_data removed to ensure real-time updates
def load_added_players():
    if os.path.exists(PLAYERS_DB_PATH):
        return pd.read_csv(PLAYERS_DB_PATH)
    return pd.DataFrame()

# 4. Input Form (Sidebar)
st.sidebar.header("➕ Add a New Player")
st.sidebar.markdown("Complete the form to evaluate and predict the player's career")

def user_input_features():
    st.sidebar.markdown("### 📋 General Information")
    name = st.sidebar.text_input("Player Name *", "Test Player", key="player_name")
    age = st.sidebar.slider("Age *", 15, 40, 22, key="age")
    height = st.sidebar.slider("Height (cm) *", 150, 210, 180, key="height")
    weight = st.sidebar.slider("Weight (kg) *", 50, 100, 75, key="weight")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ Technical & Physical Attributes")
    
    finishing = st.sidebar.slider("🎯 Finishing", 0, 100, 70, key="finishing")
    dribbling = st.sidebar.slider("🎮 Dribbling", 0, 100, 75, key="dribbling")
    short_passing = st.sidebar.slider("📤 Short Passing", 0, 100, 70, key="short_passing")
    acceleration = st.sidebar.slider("💨 Acceleration", 0, 100, 80, key="acceleration")
    sprint_speed = st.sidebar.slider("🏃 Sprint Speed", 0, 100, 80, key="sprint_speed")
    stamina = st.sidebar.slider("⚡ Stamina", 0, 100, 70, key="stamina")
    strength = st.sidebar.slider("💪 Strength", 0, 100, 65, key="strength")

    data = {
        'age': age, 
        'height_cm': height, 
        'weight_kgs': weight,
        'finishing': finishing, 
        'dribbling': dribbling, 
        'short_passing': short_passing,
        'acceleration': acceleration, 
        'sprint_speed': sprint_speed, 
        'stamina': stamina, 
        'strength': strength
    }
    
    return name, pd.DataFrame(data, index=[0])

name, input_df = user_input_features()

# 5. Main Display
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 👤 Player Profile")
    st.write(f"**Name:** {name}")
    
    # Display stats in a table
    stats_display = pd.DataFrame({
        'Attribute': ['Age', 'Height (cm)', 'Weight (kg)', 'Finishing', 'Dribbling', 'Short Passing', 
                     'Acceleration', 'Sprint Speed', 'Stamina', 'Strength'],
        'Value': [
            int(input_df['age'][0]), int(input_df['height_cm'][0]), int(input_df['weight_kgs'][0]),
            int(input_df['finishing'][0]), int(input_df['dribbling'][0]), int(input_df['short_passing'][0]),
            int(input_df['acceleration'][0]), int(input_df['sprint_speed'][0]), 
            int(input_df['stamina'][0]), int(input_df['strength'][0])
        ]
    })
    st.dataframe(stats_display, use_container_width=True, hide_index=True)

with col2:
    st.markdown("### 📊 Attribute Visualization")
    
    # Prepare data for chart
    chart_data = {
        'Finishing': int(input_df['finishing'][0]),
        'Dribbling': int(input_df['dribbling'][0]),
        'Short Pass': int(input_df['short_passing'][0]),
        'Accel': int(input_df['acceleration'][0]),
        'Speed': int(input_df['sprint_speed'][0]),
        'Stamina': int(input_df['stamina'][0]),
        'Strength': int(input_df['strength'][0])
    }
    
    st.bar_chart(pd.DataFrame(list(chart_data.items()), columns=['Attribute', 'Score']).set_index('Attribute'))

# 6. Action Button - Analyze
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

with col_btn1:
    analyze_button = st.button("🔍 Analyze Player", use_container_width=True, type="primary")

with col_btn2:
    pass

with col_btn3:
    pass

# 7. Analysis Results Display
# 7. Analysis Results Display
if analyze_button:
    if not name or name.strip() == "":
        st.error("❌ Please enter the player name!")
    else:
        # PREDICTIONS with XGBoost
        predicted_rating = reg_model.predict(input_df)[0]
        future_class = clf_model.predict(input_df)[0]
        
        # Probabilities for the classifier
        try:
            future_proba = clf_model.predict_proba(input_df)[0]
            classes = clf_model.classes_
        except:
            future_proba = None
            classes = []

        # Store results in session_state
        st.session_state['analysis_results'] = {
            'name': name,
            'input_df': input_df.copy(), # Important: keep a copy of inputs at analysis time
            'predicted_rating': predicted_rating,
            'future_class': future_class,
            'future_proba': future_proba,
            'classes': classes,
            'chart_data': chart_data # Keep chart data as well
        }
        st.success(f"✅ Analysis complete for **{name}**")

# Display based on session_state (persistent on reload)
if 'analysis_results' in st.session_state:
    results = st.session_state['analysis_results']
    
    # Retrieve variables from state
    res_name = results['name']
    predicted_rating = results['predicted_rating']
    future_class = results['future_class']
    future_proba = results['future_proba']
    classes = results['classes']
    res_chart_data = results['chart_data']
    res_input_df = results['input_df']
    
    # Display predictions
    # Display predictions
    result_col1, result_col2, result_col3 = st.columns(3)
    
    with result_col1:
        # Rating color
        if predicted_rating >= 80:
            color = "🟢"
        elif predicted_rating >= 65:
            color = "🟡"
        else:
            color = "🔴"
        
        st.metric(
            label="📈 Estimated Overall Rating",
            value=f"{predicted_rating:.1f}/100",
            delta=None
        )
        st.markdown(f"{color} {'⭐ Excellent' if predicted_rating >= 80 else '👍 Good' if predicted_rating >= 65 else '⚠️ Needs Development'}")
    
    with result_col2:
        st.metric(
            label="⚡ Strongest Attribute",
            value=f"{max(res_chart_data.items(), key=lambda x: x[1])[0]}",
            delta=f"{max(res_chart_data.values())}/100"
        )
    
    with result_col3:
        st.metric(
            label="📊 Attribute to Improve",
            value=f"{min(res_chart_data.items(), key=lambda x: x[1])[0]}",
            delta=f"{min(res_chart_data.values())}/100"
        )
    
    # Career Prediction
    st.markdown("---")
    st.markdown("### 🔮 Career Trajectory Prediction")
    
    if future_class == "high_growth":
        st.success("""
        ✨ **FUTURE SUPERSTAR** (Very High Potential)
        
        - Young player with enormous potential
        - Significant growth expected
        - Must recruit/develop
        """)
    elif future_class == "likely_improve":
        st.info("""
        📈 **SOLID POTENTIAL** (Good growth margin)
        
        - Player can improve significantly
        - Good career trajectory expected
        - Interesting investment
        """)
    elif future_class == "stable":
        st.warning("""
        ⚖️ **STABLE PLAYER** (Little change expected)
        
        - Player reached their peak/cruise level
        - No major progression foreseeable
        - Reliable for short term
        """)
    else:
        st.error("""
        📉 **DECLINING** (Regression expected)
        
        - Aging or stagnating player
        - Future performance may decrease
        - Monitor closely
        """)
    
    # Display probabilities if available
    if future_proba is not None:
        st.markdown("**Class Probabilities:**")
        proba_col1, proba_col2, proba_col3, proba_col4 = st.columns(4)
        
        proba_dict = dict(zip(classes, future_proba))
        with proba_col1:
            st.metric("High Growth", f"{proba_dict.get('high_growth', 0)*100:.1f}%")
        with proba_col2:
            st.metric("Likely Improve", f"{proba_dict.get('likely_improve', 0)*100:.1f}%")
        with proba_col3:
            st.metric("Stable", f"{proba_dict.get('stable', 0)*100:.1f}%")
        with proba_col4:
            st.metric("Decline", f"{proba_dict.get('decline', 0)*100:.1f}%")
    
    # Save to database
    st.markdown("---")
    save_col1, save_col2 = st.columns(2)
    
    with save_col1:
        if st.button("💾 Add to Database", use_container_width=True):
            # Prepare row to add from stored results
            save_row = res_input_df.copy()
            save_row['player_name'] = res_name
            save_row['predicted_overall_rating'] = round(predicted_rating, 2)
            save_row['predicted_future_class'] = future_class
            save_row['date_added'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Add to database (Append Mode with CSV module)
            try:
                print(f"Saving attempt for: {res_name}")
                
                # Prepare list of values in CSV column order
                # Columns: player_name,age,height_cm,weight_kgs,finishing,dribbling,short_passing,acceleration,sprint_speed,stamina,strength,predicted_overall_rating,predicted_future_class,date_added
                
                # Explicit re-mapping to ensure order
                c_age = save_row['age'][0]
                c_h = save_row['height_cm'][0]
                c_w = save_row['weight_kgs'][0]
                c_fin = save_row['finishing'][0]
                c_drib = save_row['dribbling'][0]
                c_pass = save_row['short_passing'][0]
                c_acc = save_row['acceleration'][0]
                c_spd = save_row['sprint_speed'][0]
                c_sta = save_row['stamina'][0]
                c_str = save_row['strength'][0]
                c_rat = save_row['predicted_overall_rating'][0]
                c_cls = save_row['predicted_future_class'][0]
                c_date = save_row['date_added'][0]
                
                # Strict order of history.csv:
                final_csv_row = [res_name, c_age, c_h, c_w, c_fin, c_drib, c_pass, c_acc, c_spd, c_sta, c_str, c_rat, c_cls, c_date]
                
                # Check if file exists to know if we need header
                file_exists = os.path.exists(PLAYERS_DB_PATH)
                
                with open(PLAYERS_DB_PATH, mode='a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    # If file is empty or doesn't exist, write headers
                    if not file_exists or os.path.getsize(PLAYERS_DB_PATH) == 0:
                        headers = ['player_name','age','height_cm','weight_kgs','finishing','dribbling','short_passing','acceleration','sprint_speed','stamina','strength','predicted_overall_rating','predicted_future_class','date_added']
                        writer.writerow(headers)
                        
                    writer.writerow(final_csv_row)
                
                print(f"SUCCESS: Player {res_name} saved to {PLAYERS_DB_PATH}")
                st.success(f"✅ {res_name} successfully added to history!")
                st.balloons()
                
            except PermissionError:
                print(f"ERROR: Permission denied writing to {PLAYERS_DB_PATH}. File open?")
                st.error("❌ Cannot save: history.csv is probably open in Excel. Close it and try again.")
            except Exception as e:
                print(f"CRITICAL ERROR: {e}")
                st.error(f"❌ Error while saving: {e}")

# 8. Display Added Players Database
st.markdown("---")
st.markdown("### 📚 Analysis History")

try:
    players_df = load_added_players()
    if not players_df.empty:
        st.dataframe(players_df, use_container_width=True)
        
        # Statistics
        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
        with stats_col1:
            st.metric("Total Players", len(players_df))
        with stats_col2:
            st.metric("Average Rating", f"{players_df['predicted_overall_rating'].mean():.1f}")
        with stats_col3:
            st.metric("Average Age", f"{players_df['age'].mean():.1f}")
        with stats_col4:
            superstars = len(players_df[players_df['predicted_future_class'] == 'high_growth'])
            st.metric("Future Superstars", superstars)
    else:
        st.info("📭 No players added yet. Start by analyzing a player!")
except Exception as e:
    st.warning(f"⚠️ Unable to load database: {e}")
