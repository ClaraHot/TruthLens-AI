# TRUTHLENS AI - PRECISION

## Description
TRUTHLENS AI est une application de surveillance et d'analyse de sécurité développée avec Streamlit. Le système permet d'effectuer des vérifications croisées entre des documents fiduciaires (billets de banque) et l'analyse biométrique des porteurs. Il intègre également un module d'analyse spectrale numérique pour détecter les anomalies de texture et de netteté sur les documents scannés.

## Fonctionnalités principales

### 1. Scan Jumele
Ce protocole permet une capture synchrone du document et du visage du porteur via des flux caméras distincts. Une analyse de stress simulée est effectuée pour évaluer la fiabilité de la transaction.

### 2. Analyseur Neuronal
Un module dédié à l'analyse de texte permettant de détecter les biais sémantiques et les vecteurs de désinformation dans les contenus médiatiques injectés.

### 3. X-Ray Deep Scan
Utilisation de la bibliothèque OpenCV pour l'analyse technique des documents :
- Conversion spectrale (Heatmap de densité d'encre).
- Calcul du score de netteté via l'algorithme de Laplacian.
- Détection des micro-perforations et de la qualité d'impression.

## Installation et Configuration

### Prerequis
- Python 3.10 ou version superieure
- Pip (Gestionnaire de paquets Python)

### Installation des dependances
Lancez la commande suivante pour installer les bibliotheques necessaires :
pip install streamlit requests Pillow opencv-python numpy fastapi uvicorn python-multipart

### Lancement de l'application
1. Demarrez le serveur API :
python main.py

2. Lancez l'interface utilisateur Streamlit :
streamlit run app_web.py

## Architecture technique
- Frontend : Streamlit (CSS personnalise pour interface de type OS securise)
- Backend : FastAPI
- Traitement d'image : OpenCV et Pillow
- Communication : Protocoles HTTP / JSON

## Note de securite
Ce projet est une preuve de concept (PoC). Les scores de stress et certaines analyses spectrales sont bases sur des algorithmes de traitement d'image numerique et doivent etre completes par une expertise humaine pour toute decision critique.
