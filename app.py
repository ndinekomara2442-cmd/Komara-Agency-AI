"""
Komara Agency 🇬🇳 — Application Flask principale
Agent IA Générative d'Image & Retouche Photo
"""

from flask import Flask, request, jsonify, send_file
import logging
import re
import os
from typing import Dict, Optional
from core.generator import ImageGenerator
from core.retoucher import PhotoRetoucher
from core.styles import StyleManager

app = Flask(__name__)

# Limit request size (bytes) — 16MB for image uploads
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Initialize modules
generator = ImageGenerator()
retoucher = PhotoRetoucher()
style_manager = StyleManager()

# Intent -> response mapping (lowercase keys)
RESPONSES: Dict[str, str] = {
    "bonjour": "Bonjour ! Bienvenue chez Komara Agency 🇬🇳 Comment puis-je vous aider ?",
    "salut": "Salut ! Komara Agency 🇬🇳 à votre service. Que puis-je faire pour vous ?",
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

# Precompile regex patterns for whole-word matching
INTENT_PATTERNS = {
    k: re.compile(rf"\b{re.escape(k)}\b", flags=re.IGNORECASE)
    for k in RESPONSES.keys()
}


def detect_intent(message: str) -> str:
    """Detect simple intent by matching whole words against known keywords."""
    if not message:
        return "Je suis l'agent de Komara Agency 🇬🇳. Tapez 'service' pour voir nos offres."
    for key, pattern in INTENT_PATTERNS.items():
        if pattern.search(message):
            return RESPONSES[key]
    # Check if message looks like an image generation request
    gen_keywords = ["génère", "genere", "crée", "cree", "image", "photo", "visuel", "dessine"]
    if any(kw in message.lower() for kw in gen_keywords):
        return f"Prêt à générer votre image ! Envoyez votre prompt sur /generate avec le paramètre 'prompt'."
    return "Je suis l'agent de Komara Agency 🇬🇳. Tapez 'service' pour voir nos offres."


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
    """Générer une image depuis un prompt texte."""
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json."}), 400

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Corps de requête JSON invalide."}), 400

    prompt = data.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        return jsonify({"error": "Le champ 'prompt' est requis."}), 400

    style = data.get("style", "photorealistic")
    aspect_ratio = data.get("aspect_ratio", "9:16")

    # Validate style
    if not style_manager.is_valid_style(style):
        return jsonify({
            "error": f"Style invalide. Styles disponibles: {style_manager.list_styles()}"
        }), 400

    try:
        result = generator.generate(
            prompt=prompt.strip(),
            style=style,
            aspect_ratio=aspect_ratio
        )
        logging.info("Image generated for prompt: %s", prompt[:100])
        return jsonify(result)
    except Exception as e:
        logging.exception("Generation error")
        return jsonify({"error": f"Erreur de génération: {str(e)}"}), 500


@app.route("/retouch", methods=["POST"])
def retouch():
    """Retoucher une image uploadée."""
    if "image" not in request.files:
        return jsonify({"error": "Aucune image fournie. Utilisez multipart/form-data avec un champ 'image'."}), 400

    image_file = request.files["image"]
    instructions = request.form.get("instructions", "")

    if not instructions.strip():
        return jsonify({"error": "Le champ 'instructions' est requis."}), 400

    try:
        result = retoucher.retouch(
            image_file=image_file,
            instructions=instructions.strip()
        )
        logging.info("Image retouched: %s", instructions[:100])
        return jsonify(result)
    except Exception as e:
        logging.exception("Retouch error")
        return jsonify({"error": f"Erreur de retouche: {str(e)}"}), 500


@app.route("/restore", methods=["POST"])
def restore():
    """Restaurer une photo abîmée ou ancienne."""
    if "image" not in request.files:
        return jsonify({"error": "Aucune image fournie."}), 400

    image_file = request.files["image"]

    try:
        result = retoucher.restore(image_file=image_file)
        logging.info("Image restored")
        return jsonify(result)
    except Exception as e:
        logging.exception("Restore error")
        return jsonify({"error": f"Erreur de restauration: {str(e)}"}), 500


@app.route("/styles", methods=["GET"])
def styles():
    """Lister tous les styles disponibles."""
    return jsonify({
        "styles": style_manager.list_styles(),
        "default": "photorealistic"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
