import streamlit as st
import pandas as pd
import joblib
import os

# 1. Configuration de la page
st.set_page_config(page_title="AI Football Scout", layout="wide")
st.title("⚽ AI Football Performance Analyzer")

# 2. Chargement des modèles (mis en cache pour la rapidité)
@st.cache_resource
def load_models():
    reg = joblib.load('models/regression_model.pkl')
    clf = joblib.load('models/classification_model.pkl')
    return reg, clf

try:
    reg_model, clf_model = load_models()
except:
    st.error("Modèles introuvables. Lance d'abord l'entraînement !")
    st.stop()

# 3. Formulaire de saisie (Sidebar)
st.sidebar.header("Nouveau Joueur")

def user_input_features():
    # Infos générales
    name = st.sidebar.text_input("Nom du joueur", "Mbappé Jr.")
    age = st.sidebar.slider("Age", 15, 40, 19)
    height = st.sidebar.slider("Taille (cm)", 150, 210, 180)
    weight = st.sidebar.slider("Poids (kg)", 50, 100, 75)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Attributs Techniques")
    
    # Basé sur tes features dans code_explanation.md
    finishing = st.sidebar.slider("Finishing", 0, 100, 70)
    dribbling = st.sidebar.slider("Dribbling", 0, 100, 75)
    short_passing = st.sidebar.slider("Short Passing", 0, 100, 70)
    acceleration = st.sidebar.slider("Acceleration", 0, 100, 80)
    sprint_speed = st.sidebar.slider("Sprint Speed", 0, 100, 80)
    stamina = st.sidebar.slider("Stamina", 0, 100, 70)
    strength = st.sidebar.slider("Strength", 0, 100, 65)

    data = {
        'age': age, 'height_cm': height, 'weight_kgs': weight,
        'finishing': finishing, 'dribbling': dribbling, 'short_passing': short_passing,
        'acceleration': acceleration, 'sprint_speed': sprint_speed, 
        'stamina': stamina, 'strength': strength
    }
    return name, pd.DataFrame(data, index=[0])

name, input_df = user_input_features()

# 4. Affichage principal
col1, col2 = st.columns(2)

with col1:
    st.subheader("Profil du Joueur")
    st.write(input_df)

    # BOUTON D'ACTION
    if st.button("🔍 Analyser & Sauvegarder"):
        
        # --- PREDICTION ---
        predicted_rating = reg_model.predict(input_df)[0]
        future_class = clf_model.predict(input_df)[0]
        
        st.success(f"Analyse terminée pour **{name}**")
        
        # Affichage des résultats avec métriques visuelles
        st.metric(label="Note Globale Estimée (Overall)", value=f"{predicted_rating:.1f}")
        
        st.subheader("🔮 Prédiction de Carrière")
        if future_class == "high_growth":
            st.success("🌟 FUTURE SUPERSTAR (High Growth)")
        elif future_class == "likely_improve":
            st.info("📈 Potentiel Solide (Likely Improve)")
        elif future_class == "stable":
            st.warning("⚖️ Joueur Stable")
        else:
            st.error("📉 En déclin")

        # --- SAUVEGARDE DANS CSV ---
        # On prépare la ligne à ajouter
        save_row = input_df.copy()
        save_row['player_name'] = name
        save_row['predicted_overall'] = predicted_rating
        save_row['predicted_future'] = future_class
        
        # Chemin vers ton fichier CSV (Attention au chemin relatif)
        csv_path = 'data/football_players.csv' 
        
        # Ajout sans écraser l'existant (mode='a')
        if os.path.exists(csv_path):
            save_row.to_csv(csv_path, mode='a', header=False, index=False)
            st.toast("✅ Joueur ajouté à la base de données !", icon="💾")
        else:
            save_row.to_csv(csv_path, mode='w', header=True, index=False)
            st.toast("Base de données créée et joueur ajouté !", icon="💾")

with col2:
    # Bonus : Visualisation radar ou comparaison
    st.subheader("Statistiques Clés")
    st.bar_chart(input_df.T)
    
    st.markdown("### Aperçu de la Base de Données")
    # Afficher les 5 derniers joueurs ajoutés
    if os.path.exists('data/football_players.csv'):
        try:
            df_full = pd.read_csv('data/football_players.csv')
            st.dataframe(df_full.tail(5))
        except:
            st.write("Erreur de lecture du CSV.")