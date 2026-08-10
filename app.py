"""
Komara Agency 🇬🇳 — Application Flask principale
Agent IA Générative d'Image & Retouche Photo + Telegram Bot
"""

from flask import Flask, request, jsonify, send_file
import logging
import re
import os
import requests
from typing import Dict, Optional
from core.generator import ImageGenerator
from core.retoucher import PhotoRetoucher
from core.styles import StyleManager

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

generator = ImageGenerator()
retoucher = PhotoRetoucher()
style_manager = StyleManager()

RESPONSES: Dict[str, str] = {
    "bonjour": "Bonjour! Bienvenue chez Komara Agency 🇬🇳 Comment puis-je vous aider?",
    "salut": "Salut! Komara Agency 🇬🇳 à votre service. Que puis-je faire pour vous?",
    "service": (
        "Nos services :\n"
        "1. Génération d'images IA\n"
        "2. Retouche photo professionnelle\n"
        "3. Restauration de photos anciennes\n"
        "4. Styles multiples (réaliste, 3D, cinématique, illustratif)"
    ),
    "prix": "Pour les tarifs, laissez votre numéro WhatsApp et un conseiller vous contacte.",
    "tarif": "Pour les tarifs, laissez votre numéro WhatsApp et un conseiller vous contacte.",
    "contact": "WhatsApp: +224 XXX | Conakry, Guinée 🇬🇳",
    "style": "Styles disponibles : photoréaliste, portrait studio, lifestyle, e-commerce, illustration, 3D, cinématique, noir & blanc, vintage.",
    "help": "Tapez 'service' pour voir nos offres, 'style' pour les styles disponibles, ou décrivez l'image que vous souhaitez générer.",
}

INTENT_PATTERNS = {
    k: re.compile(rf"\b{re.escape(k)}\b", flags=re.IGNORECASE)
    for k in RESPONSES.keys()
}

def detect_intent(message: str) -> str:
    if not message:
        return "Je suis l'agent de Komara Agency 🇬🇳. Tapez 'service' pour voir nos offres."
    for key, pattern in INTENT_PATTERNS.items():
        if pattern.search(message):
            return RESPONSES[key]
    gen_keywords = ["génère", "genere", "crée", "cree", "image", "photo", "visuel", "dessine"]
    if any(kw in message.lower() for kw in gen_keywords):
        return f"Prêt à générer votre image! Envoyez votre prompt sur /generate avec le paramètre 'prompt'."
    return "Je suis l'agent de Komara Agency 🇬🇳. Tapez 'service' pour voir nos offres."

def send_telegram_message(chat_id, text):
    if not TELEGRAM_TOKEN:
        logging.error("TELEGRAM_TOKEN not set")
        return
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        logging.exception("Failed to send telegram message: %s", e)

@app.route("/", methods=["GET"])
def home():
    return "Komara Agency 🇬🇳 — Agent IA Générative d'Image en ligne"

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "Komara Agency 🇬🇳",
        "version": "2.0.0"
    })

@app.route("/chat", methods=["POST"])
def chat():
    if not request.is_json:
        logging.warning("Non-JSON request to /chat from %s", request.remote_addr)
        return jsonify({"error": "Content-Type must be application/json."}), 400
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Corps de requête JSON invalide ou manquant."}), 400
    user_message = data.get("message")
    if not isinstance(user_message, str) or not user_message.strip():
        return jsonify({"error": "Le champ 'message' est requis et doit être une chaîne non vide."}), 400
    user_message = user_message.strip()
    logging.info("Received message from %s: %s", request.remote_addr, user_message)
    try:
        reply = detect_intent(user_message)
        return jsonify({"reply": reply})
    except Exception as e:
        logging.exception("Error while processing message from %s", request.remote_addr)
        return jsonify({"error": "Erreur interne du serveur."}), 500

@app.route("/generate", methods=["POST"])
def generate():
    return jsonify({"error": "Not implemented"}), 501

@app.route(f"/webhook/{TELEGRAM_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if not data:
        return "ok", 200
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"].get("text", "")
        reply = detect_intent(user_text)
        send_telegram_message(chat_id, reply)
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
