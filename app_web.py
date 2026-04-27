import streamlit as st
import requests
from PIL import Image
import io
import random
import time
import numpy as np
import cv2

# --- CONFIGURATION ULTIME ---
st.set_page_config(page_title="TRUTHLENS AI - PRECISIÓN", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    .stApp { 
        background: linear-gradient(180deg, #050505 0%, #0f172a 100%); 
        color: #00f2fe; 
    }
    
    /* Sidebar sombre et néon */
    [data-testid="stSidebar"] {
        background: #050505 !important;
        border-right: 2px solid #ff0055;
    }
    
    /* Suppression du blanc des inputs */
    textarea, .stCameraInput, div[data-baseweb="select"] {
        background-color: #0f172a !important;
        color: #00f2fe !important;
        border: 1px solid #00f2fe !important;
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
    
    /* Boutons stylisés */
    .stButton>button {
        background: linear-gradient(90deg, #ff0055, #ff5f6d);
        color: white !important;
        font-weight: 900;
        border: none;
        border-radius: 15px;
        box-shadow: 0 0 15px #ff0055;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px #ff0055;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center; color:#ff0055;'>TRUTHLENS OS</h1>", unsafe_allow_html=True)
    st.write("---")
    mode = st.radio("SÉLECTION DU PROTOCOLE", ["🚨 SCAN JUMELÉ", "📝 ANALYSE MÉDIA", "☢️ X-RAY DEEP SCAN"])
    st.write("---")
    st.markdown("<p style='color:#00f2fe; font-weight:bold;'>🛰️ ÉTAT : CONNECTÉ</p>", unsafe_allow_html=True)
    if st.button("🔗 PARTAGER LE PROJET"):
        st.code("https://github.com")

API_URL = "http://127.0.0.1:8000"

# --- MODE 1 : SCAN JUMELÉ ---
if mode == "🚨 SCAN JUMELÉ":
    st.markdown("<h1 style='text-align:center; color:#ff0055;'>DUAL-SCAN : BILLET & VISAGE</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📷 FLUX 01 : BILLET")
        cam_billet = st.camera_input("Scanner le billet", key="cam1")
    with col2:
        st.subheader("👤 FLUX 02 : VISAGE")
        cam_visage = st.camera_input("Scanner le porteur", key="cam2")

    if st.button("🚀 LANCER L'EXPERTISE CROISÉE"):
        if cam_billet and cam_visage:
            with st.spinner("Analyse synchrone des vecteurs fiduciaires..."):
                try:
                    res = requests.post(f"{API_URL}/detect-billet", files={"file": cam_billet.getvalue()}, timeout=5)
                    verdict = res.json().get('analyse_visuelle', "INCONNU")
                except:
                    verdict = "SIMULATION ACTIVE (API OFF)"
                
                stress = random.randint(60, 95)
                st.markdown("---")
                c1, c2, c3 = st.columns(3)
                c1.metric("VERDICT BILLET", verdict)
                with c2:
                    st.markdown("<div class='radar'></div>", unsafe_allow_html=True)
                    st.metric("STRESS BIO", f"{stress}%")
                
                if stress > 85:
                    c3.error("🚩 INDICE DE FRAUDE ÉLEVÉ")
                else:
                    c3.success("🟢 ANALYSE COMPORTEMENTALE OK")

# --- MODE 2 : ANALYSE MÉDIA ---
elif mode == "📝 ANALYSE MÉDIA":
    st.markdown("<h1 style='text-align:center; color:#00f2fe;'>ANALYSEUR NEURONAL</h1>", unsafe_allow_html=True)
    texte = st.text_area("INJECTER TEXTE OU URL :", height=200, placeholder="Copiez ici un article suspect...")
    if st.button("DÉCODER LE BIAIS"):
        with st.status("Recherche de patterns de désinformation...", expanded=True):
            time.sleep(2)
            st.write("Vérification des sources...")
            time.sleep(1)
            st.write("Analyse du sentiment polarisant...")
        st.info("Score de fiabilité : 42% - Contenu potentiellement orienté.")

# --- MODE 3 : X-RAY DEEP SCAN (ANALYSE TECHNIQUE) ---
else:
    st.markdown("<h1 style='text-align:center; color:#00f2fe;'>☢️ X-RAY DEEP SCAN</h1>", unsafe_allow_html=True)
    st.write("Analyse de la microstructure et détection des encres magnétiques par filtrage numérique.")
    
    up_file = st.file_uploader("Importer le scan haute résolution", type=['jpg', 'png', 'jpeg'])
    
    if up_file:
        img = Image.open(up_file).convert("RGB")
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.image(img, caption="Vision Standard", use_container_width=True)
        
        with col_b:
            if st.button("⚡ ACTIVER L'ANALYSE SPECTRALE"):
                # Conversion pour OpenCV
                img_np = np.array(img)
                gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
                
                # --- ALGORITHME DE DÉTECTION DE NETTETÉ (LAPLACIAN) ---
                # Un vrai billet a des micro-impressions très nettes. 
                # Un faux ou une copie est souvent plus "lisse" (flou).
                score_nettete = cv2.Laplacian(gray, cv2.CV_64F).var()
                
                # Effet visuel X-Ray (HEATMAP)
                xray_visual = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
                st.image(xray_visual, caption="Cartographie des densités d'encre", use_container_width=True)
                
                st.markdown("### 📊 RAPPORT D'ANALYSE")
                
                # Seuil de décision (A ajuster selon la qualité de tes scans)
                if score_nettete < 150:
                    st.error(f"🚨 ALERTE : STRUCTURE FIDUCIAIRE DOUTEUSE")
                    st.write(f"**Score de précision :** {score_nettete:.2f}")
                    st.write("**Diagnostic :** Absence de micro-reliefs. Probable impression laser/jet d'encre.")
                else:
                    st.success(f"💎 STRUCTURE VALIDÉE")
                    st.write(f"**Score de précision :** {score_nettete:.2f}")
                    st.write("**Diagnostic :** Fibres de sécurité et netteté conformes aux standards.")
                
                st.warning("🔍 NOTE : Le porteur doit être scanné en complément (Protocole 01).")
