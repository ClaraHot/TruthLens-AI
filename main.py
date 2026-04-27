from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from transformers import pipeline
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = FastAPI(title="IA Multi-Détecteur")

# --- CHARGEMENT DES MODÈLES (Texte) ---
print("Chargement de l'IA Texte...")
bias_classifier = pipeline("text-classification", model="himel7/bias-detector")
fake_classifier = pipeline("text-classification", model="dhruvpal/fake-news-bert")

# --- CHARGEMENT DU MODÈLE (Vision pour les billets) ---
print("Chargement de l'IA Vision...")
# MobileNetV2 est parfait pour reconnaître les objets/images
vision_model = tf.keras.applications.MobileNetV2(weights="imagenet")

class TextInput(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "L'API est prête !"}

# --- ROUTE 1 : DÉTECTION DE BIAIS ---
@app.post("/detect-biais")
def detect_biais(input: TextInput):
    text = input.text.strip()
    
    # Analyse avec l'IA
    bias_result = bias_classifier(text[:500])[0]
    fake_result = fake_classifier(text[:500])[0]
    
    score_biais = round(bias_result['score'], 4)
    est_fake = fake_result['label'] == "FAKE" or fake_result['label'] == "LABEL_1"

    # Ta logique personnalisée (les mots "toujours" et "jamais")
    mots_cles = ["toujours", "jamais", "tous les", "chaque fois"]
    alerte_mots = any(m in text.lower() for m in mots_cles)

    if (bias_result['label'] == "LABEL_1" and score_biais > 0.7) or alerte_mots:
        interpretation = "⚠️ Texte probablement biaisé"
        biais_detecte = True
    else:
        interpretation = "✅ Neutre"
        biais_detecte = False

    return {
        "texte": text,
        "biais_detecte": biais_detecte,
        "score_biais": score_biais,
        "interpretation": interpretation,
        "fake_news_detecte": est_fake,
        "conseil": "Vérifie les sources officielles."
    }

# --- ROUTE 2 : DÉTECTION DE BILLETS ---
@app.post("/detect-billet")
async def detect_billet(file: UploadFile = File(...)):
    # Lecture et préparation de l'image
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB").resize((224, 224))
    
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

    # Prédiction
    preds = vision_model.predict(img_array)
    decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=1)[0][0]

    # Simulation de vérification (ex: si l'objet est identifié comme de l'argent/papier)
    # decoded[1] contient le nom de l'objet détecté
    objet = decoded[1]
    confiance = float(decoded[2])

    return {
        "objet_detecte": objet,
        "confiance": round(confiance, 4),
        "analyse_visuelle": f"L'IA voit : {objet}",
        "message": "Vérification des filigranes conseillée."
    }
