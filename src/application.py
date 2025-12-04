import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
import xgboost as xgb

# 1. Configuration de la page
st.set_page_config(page_title="AI Football Scout", layout="wide", initial_sidebar_state="expanded")
st.title("⚽ AI Football Performance Analyzer")
st.markdown("### Analyse et Prédiction de Performance des Joueurs avec XGBoost")

# 2. Chargement des modèles (mis en cache pour la rapidité)
@st.cache_resource
def load_models():
    try:
        reg_model = joblib.load('models/regression_model.pkl')
        clf_model = joblib.load('models/classification_model.pkl')
        return reg_model, clf_model
    except FileNotFoundError:
        return None, None

reg_model, clf_model = load_models()

if reg_model is None or clf_model is None:
    st.error("❌ Modèles introuvables! Veuillez d'abord exécuter l'entraînement avec 'ml_analysis.py'")
    st.stop()

# Définir les chemins
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "fifa_players.csv")
PLAYERS_DB_PATH = os.path.join(PROJECT_ROOT, "data", "added_players.csv")

# Créer le dossier si nécessaire
os.makedirs(os.path.dirname(PLAYERS_DB_PATH), exist_ok=True)

# 3. Fonction pour charger la base de joueurs ajoutés
@st.cache_data
def load_added_players():
    if os.path.exists(PLAYERS_DB_PATH):
        return pd.read_csv(PLAYERS_DB_PATH)
    return pd.DataFrame()

# 4. Formulaire de saisie (Sidebar)
st.sidebar.header("➕ Ajouter un Nouveau Joueur")
st.sidebar.markdown("Complétez le formulaire pour évaluer et prédire la carrière d'un joueur")

def user_input_features():
    st.sidebar.markdown("### 📋 Informations Générales")
    name = st.sidebar.text_input("Nom du joueur *", "Joueur Test", key="player_name")
    age = st.sidebar.slider("Âge *", 15, 40, 22, key="age")
    height = st.sidebar.slider("Taille (cm) *", 150, 210, 180, key="height")
    weight = st.sidebar.slider("Poids (kg) *", 50, 100, 75, key="weight")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ Attributs Techniques & Physiques")
    
    finishing = st.sidebar.slider("🎯 Finishing (Finition)", 0, 100, 70, key="finishing")
    dribbling = st.sidebar.slider("🎮 Dribbling", 0, 100, 75, key="dribbling")
    short_passing = st.sidebar.slider("📤 Short Passing (Passes courtes)", 0, 100, 70, key="short_passing")
    acceleration = st.sidebar.slider("💨 Acceleration", 0, 100, 80, key="acceleration")
    sprint_speed = st.sidebar.slider("🏃 Sprint Speed (Vitesse)", 0, 100, 80, key="sprint_speed")
    stamina = st.sidebar.slider("⚡ Stamina (Endurance)", 0, 100, 70, key="stamina")
    strength = st.sidebar.slider("💪 Strength (Force)", 0, 100, 65, key="strength")

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

# 5. Affichage principal en deux colonnes
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 👤 Profil du Joueur")
    st.write(f"**Nom:** {name}")
    
    # Affichage des stats en tableau
    stats_display = pd.DataFrame({
        'Attribut': ['Âge', 'Taille (cm)', 'Poids (kg)', 'Finishing', 'Dribbling', 'Short Passing', 
                     'Acceleration', 'Sprint Speed', 'Stamina', 'Strength'],
        'Valeur': [
            int(input_df['age'][0]), int(input_df['height_cm'][0]), int(input_df['weight_kgs'][0]),
            int(input_df['finishing'][0]), int(input_df['dribbling'][0]), int(input_df['short_passing'][0]),
            int(input_df['acceleration'][0]), int(input_df['sprint_speed'][0]), 
            int(input_df['stamina'][0]), int(input_df['strength'][0])
        ]
    })
    st.dataframe(stats_display, use_container_width=True, hide_index=True)

with col2:
    st.markdown("### 📊 Visualisation des Attributs")
    
    # Préparer les données pour le graphique
    chart_data = {
        'Finishing': int(input_df['finishing'][0]),
        'Dribbling': int(input_df['dribbling'][0]),
        'Short Pass': int(input_df['short_passing'][0]),
        'Accel': int(input_df['acceleration'][0]),
        'Speed': int(input_df['sprint_speed'][0]),
        'Stamina': int(input_df['stamina'][0]),
        'Strength': int(input_df['strength'][0])
    }
    
    st.bar_chart(pd.DataFrame(list(chart_data.items()), columns=['Attribut', 'Score']).set_index('Attribut'))

# 6. Bouton d'action - Analyser
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

with col_btn1:
    analyze_button = st.button("🔍 Analyser le Joueur", use_container_width=True, type="primary")

with col_btn2:
    pass

with col_btn3:
    pass

# 7. Affichage des résultats d'analyse
if analyze_button:
    if not name or name.strip() == "":
        st.error("❌ Veuillez entrer le nom du joueur!")
    else:
        # PREDICTIONS avec XGBoost
        predicted_rating = reg_model.predict(input_df)[0]
        future_class = clf_model.predict(input_df)[0]
        
        # Probabilités pour le classificateur
        try:
            future_proba = clf_model.predict_proba(input_df)[0]
            classes = clf_model.classes_
        except:
            future_proba = None
        
        st.success(f"✅ Analyse réalisée pour **{name}**")
        
        # Affichage des prédictions
        result_col1, result_col2, result_col3 = st.columns(3)
        
        with result_col1:
            # Rating couleur selon la note
            if predicted_rating >= 80:
                color = "🟢"
            elif predicted_rating >= 65:
                color = "🟡"
            else:
                color = "🔴"
            
            st.metric(
                label="📈 Note Globale Estimée",
                value=f"{predicted_rating:.1f}/100",
                delta=None
            )
            st.markdown(f"{color} {'⭐ Excellent' if predicted_rating >= 80 else '👍 Bon' if predicted_rating >= 65 else '⚠️ À développer'}")
        
        with result_col2:
            st.metric(
                label="⚡ Attribut Fort",
                value=f"{max(chart_data.items(), key=lambda x: x[1])[0]}",
                delta=f"{max(chart_data.values())}/100"
            )
        
        with result_col3:
            st.metric(
                label="📊 Attribut à Travailler",
                value=f"{min(chart_data.items(), key=lambda x: x[1])[0]}",
                delta=f"{min(chart_data.values())}/100"
            )
        
        # Prédiction de carrière
        st.markdown("---")
        st.markdown("### 🔮 Prédiction de Trajectoire Professionnelle")
        
        if future_class == "high_growth":
            st.success("""
            ✨ **FUTURE SUPERSTAR** (Potentiel très élevé)
            
            - Jeune joueur avec un énorme potentiel
            - Progression attendue très importante
            - À absolument recruter/développer
            """)
        elif future_class == "likely_improve":
            st.info("""
            📈 **POTENTIEL SOLIDE** (Bonne marge de progression)
            
            - Joueur pouvant s'améliorer significativement
            - Bonne trajectoire professionnelle attendue
            - Investissement intéressant
            """)
        elif future_class == "stable":
            st.warning("""
            ⚖️ **JOUEUR STABLE** (Peu de changement attendu)
            
            - Joueur ayant atteint son niveau de croisière
            - Pas de progression majeure prévisible
            - Fiable pour le court terme
            """)
        else:
            st.error("""
            📉 **EN DÉCLIN** (Régression attendue)
            
            - Joueur vieillissant ou stagnant
            - Performance future peut diminuer
            - À surveiller attentivement
            """)
        
        # Afficher les probabilités si disponibles
        if future_proba is not None:
            st.markdown("**Probabilités par classe:**")
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
        
        # Sauvegarde dans la base de données
        st.markdown("---")
        save_col1, save_col2 = st.columns(2)
        
        with save_col1:
            if st.button("💾 Ajouter à la Base de Données", use_container_width=True):
                # Préparer la ligne à ajouter
                save_row = input_df.copy()
                save_row['player_name'] = name
                save_row['predicted_overall_rating'] = round(predicted_rating, 2)
                save_row['predicted_future_class'] = future_class
                save_row['date_added'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Ajouter à la base de données
                try:
                    if os.path.exists(PLAYERS_DB_PATH):
                        existing_df = pd.read_csv(PLAYERS_DB_PATH)
                        updated_df = pd.concat([existing_df, save_row], ignore_index=True)
                    else:
                        updated_df = save_row
                    
                    updated_df.to_csv(PLAYERS_DB_PATH, index=False)
                    st.success(f"✅ {name} ajouté avec succès à la base de données!")
                    st.balloons()
                    
                    # Réinitialiser le cache
                    st.cache_data.clear()
                    
                except Exception as e:
                    st.error(f"❌ Erreur lors de la sauvegarde: {e}")

# 8. Affichage de la base de données des joueurs ajoutés
st.markdown("---")
st.markdown("### 📚 Base de Données des Joueurs Ajoutés")

try:
    players_df = load_added_players()
    if not players_df.empty:
        st.dataframe(players_df, use_container_width=True)
        
        # Statistiques
        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
        with stats_col1:
            st.metric("Total de Joueurs", len(players_df))
        with stats_col2:
            st.metric("Note Moyenne", f"{players_df['predicted_overall_rating'].mean():.1f}")
        with stats_col3:
            st.metric("Âge Moyen", f"{players_df['age'].mean():.1f}")
        with stats_col4:
            superstars = len(players_df[players_df['predicted_future_class'] == 'high_growth'])
            st.metric("Futures Superstars", superstars)
    else:
        st.info("📭 Aucun joueur ajouté pour le moment. Commencez par analyser un joueur!")
except Exception as e:
    st.warning(f"⚠️ Impossible de charger la base de données: {e}")
