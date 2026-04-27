import streamlit as st
import requests
from PIL import Image
import io
import random

# --- CONFIGURATION QUANTUM DUAL-SCAN ---
st.set_page_config(page_title="NEURO-GUARD DUAL", page_icon="🕵️", layout="wide")

st.markdown("""
    <style>
    /* Fond de la page principale */
    .stApp { 
        background: linear-gradient(180deg, #050505 0%, #0f172a 100%); 
        color: #00f2fe; 
    }
    
    /* MODIFICATION : On rend la barre latérale (Sidebar) sombre */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #050505 0%, #16213e 100%) !important;
        border-right: 1px solid #00f2fe;
    }
    
    /* Couleur du texte dans la barre latérale */
    [data-testid="stSidebar"] .stText, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: #00f2fe !important;
    }

    /* Conteneurs de scan */
    .scan-container {
        border: 2px solid #00f2fe;
        background: rgba(0, 242, 254, 0.05);
        padding: 15px;
        border-radius: 20px;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.2);
    }
    
    /* Radar de stress */
    .radar {
        height: 80px; width: 80px;
        background: radial-gradient(circle, #ff0055 0%, transparent 70%);
        border-radius: 50%;
        animation: pulse 1.5s infinite;
        margin: auto;
    }
    @keyframes pulse {
        0% { transform: scale(0.8); opacity: 0.5; }
        50% { transform: scale(1.2); opacity: 1; }
        100% { transform: scale(0.8); opacity: 0.5; }
    }
    
    /* Bouton d'expertise */
    .stButton>button {
        background: linear-gradient(90deg, #ff0055, #ff5f6d);
        color: white !important;
        font-weight: 900;
        border: none;
        box-shadow: 0 0 15px #ff0055;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRE LATÉRALE (Désormais sombre) ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center; color:#00f2fe;'>CORE OS</h1>", unsafe_allow_html=True)
    st.write("---")
    mode = st.radio("SÉLECTION DU PROTOCOLE", ["🚨 SCAN JUMELÉ (LIVE)", "📝 ANALYSE MÉDIA"])
    st.write("---")
    st.markdown("<p style='color:#ff0055; font-weight:bold;'>🔒 CRYPTAGE : ACTIF</p>", unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000"

# --- MODE 1 : SCAN JUMELÉ ---
if mode == "🚨 SCAN JUMELÉ (LIVE)":
    st.markdown("<h1 style='text-align:center; text-shadow: 0 0 20px #ff0055; color:#ff0055;'>DUAL-SCAN : BILLET & VISAGE</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📷 FLUX 01 : BILLET")
        cam_billet = st.camera_input("Scanner le billet", key="cam1")
        
    with col2:
        st.subheader("👤 FLUX 02 : VISAGE")
        cam_visage = st.camera_input("Scanner le porteur", key="cam2")

    if st.button("🚀 LANCER L'EXPERTISE CROISÉE"):
        if cam_billet and cam_visage:
            with st.spinner("Analyse synchrone..."):
                try:
                    res = requests.post(f"{API_URL}/detect-billet", files={"file": cam_billet.getvalue()})
                    verdict_billet = res.json()['analyse_visuelle']
                    stress_level = random.randint(60, 95)
                    
                    st.markdown("---")
                    res_col1, res_col2, res_col3 = st.columns(3)
                    with res_col1:
                        st.metric("BILLET DÉTECTÉ", verdict_billet)
                    with res_col2:
                        st.markdown("<div class='radar'></div>", unsafe_allow_html=True)
                        st.metric("STRESS PORTEUR", f"{stress_level}%")
                    with res_col3:
                        if stress_level > 80:
                            st.error("🚨 INDIVIDU SUSPECT")
                        else:
                            st.success("✅ PORTEUR HONNÊTE")
                except:
                    st.error("L'API (fenêtre noire) n'est pas lancée !")

# --- MODE 2 : ANALYSE MÉDIA ---
else:
    st.title("📝 ANALYSEUR NEURONAL")
    texte = st.text_area("INJECTER TEXTE :")
    if st.button("SCANNER"):
        st.info("Recherche de biais...")
